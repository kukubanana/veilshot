#!/usr/bin/env python3
"""Portal/PipeWire helper executed by the host Python interpreter.

PNG bytes are written to stdout. Diagnostics go to stderr. Keeping this helper
standalone lets Veilshot's virtual environment use Fedora's system PyGObject
without bundling native GObject bindings into the Python package.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import uuid
from typing import Any

try:
    import gi

    gi.require_version("Gio", "2.0")
    from gi.repository import Gio, GLib
except (ImportError, ValueError) as exc:
    print(
        "PyGObject/GIO is required (Fedora package: python3-gobject)",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


PORTAL_BUS_NAME = "org.freedesktop.portal.Desktop"
PORTAL_OBJECT_PATH = "/org/freedesktop/portal/desktop"
SCREENCAST_INTERFACE = "org.freedesktop.portal.ScreenCast"
REQUEST_INTERFACE = "org.freedesktop.portal.Request"
SESSION_INTERFACE = "org.freedesktop.portal.Session"
SOURCE_MONITOR = 1
CURSOR_EMBEDDED = 2
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class PortalError(RuntimeError):
    pass


def _token(prefix: str) -> str:
    return f"veilshot_{prefix}_{uuid.uuid4().hex}"


def request_path(unique_bus_name: str, handle_token: str) -> str:
    sender = unique_bus_name.lstrip(":").replace(".", "_")
    return f"/org/freedesktop/portal/desktop/request/{sender}/{handle_token}"


class ScreenCastPortal:
    def __init__(self, timeout_seconds: int = 120) -> None:
        self.timeout_seconds = timeout_seconds
        self.connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self.proxy = Gio.DBusProxy.new_sync(
            self.connection,
            Gio.DBusProxyFlags.NONE,
            None,
            PORTAL_BUS_NAME,
            PORTAL_OBJECT_PATH,
            SCREENCAST_INTERFACE,
            None,
        )
        self.session_handle: str | None = None

    def _request(
        self,
        method: str,
        parameters: GLib.Variant,
        handle_token: str,
    ) -> dict[str, Any]:
        expected_path = request_path(
            self.connection.get_unique_name(), handle_token
        )
        response: dict[str, Any] = {}
        loop = GLib.MainLoop()

        def on_response(
            _connection: Gio.DBusConnection,
            _sender: str,
            _path: str,
            _interface: str,
            _signal: str,
            values: GLib.Variant,
            _user_data: object,
        ) -> None:
            response_code, results = values.unpack()
            response["code"] = response_code
            response["results"] = results
            loop.quit()

        subscription_id = self.connection.signal_subscribe(
            PORTAL_BUS_NAME,
            REQUEST_INTERFACE,
            "Response",
            expected_path,
            None,
            Gio.DBusSignalFlags.NONE,
            on_response,
            None,
        )
        timeout_id: int | None = None
        try:
            returned = self.proxy.call_sync(
                method,
                parameters,
                Gio.DBusCallFlags.NONE,
                -1,
                None,
            )
            returned_path = returned.unpack()[0]
            if returned_path != expected_path:
                raise PortalError(
                    f"Portal returned an unexpected request path: {returned_path}"
                )

            def on_timeout() -> bool:
                response["timeout"] = True
                loop.quit()
                return GLib.SOURCE_REMOVE

            timeout_id = GLib.timeout_add_seconds(
                self.timeout_seconds, on_timeout
            )
            loop.run()
            if not response.get("timeout"):
                GLib.source_remove(timeout_id)
                timeout_id = None
        finally:
            self.connection.signal_unsubscribe(subscription_id)
            if timeout_id is not None and not response.get("timeout"):
                GLib.source_remove(timeout_id)

        if response.get("timeout"):
            raise PortalError(f"{method} timed out")
        code = response.get("code")
        if code == 1:
            raise PortalError("Screen capture was cancelled")
        if code != 0:
            raise PortalError(f"{method} failed with portal response {code}")
        return response["results"]

    def create_session(self) -> None:
        handle_token = _token("create")
        results = self._request(
            "CreateSession",
            GLib.Variant(
                "(a{sv})",
                (
                    {
                        "handle_token": GLib.Variant("s", handle_token),
                        "session_handle_token": GLib.Variant(
                            "s", _token("session")
                        ),
                    },
                ),
            ),
            handle_token,
        )
        self.session_handle = str(results["session_handle"])

    def select_monitor(self) -> None:
        if self.session_handle is None:
            raise PortalError("ScreenCast session was not created")
        handle_token = _token("select")
        self._request(
            "SelectSources",
            GLib.Variant(
                "(oa{sv})",
                (
                    self.session_handle,
                    {
                        "handle_token": GLib.Variant("s", handle_token),
                        "types": GLib.Variant("u", SOURCE_MONITOR),
                        "multiple": GLib.Variant("b", False),
                        "cursor_mode": GLib.Variant("u", CURSOR_EMBEDDED),
                    },
                ),
            ),
            handle_token,
        )

    def start(self) -> int:
        if self.session_handle is None:
            raise PortalError("ScreenCast session was not created")
        handle_token = _token("start")
        results = self._request(
            "Start",
            GLib.Variant(
                "(osa{sv})",
                (
                    self.session_handle,
                    "",
                    {"handle_token": GLib.Variant("s", handle_token)},
                ),
            ),
            handle_token,
        )
        streams = results.get("streams", [])
        if len(streams) != 1:
            raise PortalError(
                f"Expected one monitor stream, received {len(streams)}"
            )
        return int(streams[0][0])

    def open_pipewire_remote(self) -> int:
        if self.session_handle is None:
            raise PortalError("ScreenCast session was not created")
        result, fd_list = self.proxy.call_with_unix_fd_list_sync(
            "OpenPipeWireRemote",
            GLib.Variant("(oa{sv})", (self.session_handle, {})),
            Gio.DBusCallFlags.NONE,
            -1,
            None,
            None,
        )
        return fd_list.get(result.unpack()[0])

    def close(self) -> None:
        if self.session_handle is None:
            return
        self.connection.call_sync(
            PORTAL_BUS_NAME,
            self.session_handle,
            SESSION_INTERFACE,
            "Close",
            None,
            None,
            Gio.DBusCallFlags.NONE,
            -1,
            None,
        )
        self.session_handle = None


def capture_png(pipewire_fd: int, node_id: int) -> bytes:
    gst_launch = shutil.which("gst-launch-1.0")
    if gst_launch is None:
        raise RuntimeError(
            "gst-launch-1.0 is required (Fedora packages: gstreamer1, "
            "pipewire-gstreamer, gstreamer1-plugins-good)"
        )
    completed = subprocess.run(
        [
            gst_launch,
            "-q",
            "pipewiresrc",
            f"fd={pipewire_fd}",
            f"path={node_id}",
            "num-buffers=1",
            "do-timestamp=true",
            "!",
            "videoconvert",
            "!",
            "pngenc",
            "snapshot=true",
            "!",
            "fdsink",
            "fd=1",
            "sync=false",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        pass_fds=(pipewire_fd,),
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        details = completed.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"PipeWire frame capture failed: {details}")
    if not completed.stdout.startswith(PNG_SIGNATURE):
        raise RuntimeError("PipeWire returned no valid image frame")
    return completed.stdout


def main() -> int:
    if os.environ.get("XDG_SESSION_TYPE", "").lower() != "wayland":
        print("ScreenCast Portal capture requires a Wayland session", file=sys.stderr)
        return 2

    portal: ScreenCastPortal | None = None
    pipewire_fd: int | None = None
    try:
        portal = ScreenCastPortal()
        portal.create_session()
        portal.select_monitor()
        node_id = portal.start()
        pipewire_fd = portal.open_pipewire_remote()
        png = capture_png(pipewire_fd, node_id)
    except (GLib.Error, OSError, PortalError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        if pipewire_fd is not None:
            os.close(pipewire_fd)
        if portal is not None:
            try:
                portal.close()
            except GLib.Error:
                pass

    sys.stdout.buffer.write(png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
