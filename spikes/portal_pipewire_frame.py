#!/usr/bin/env python3
"""Capture one PNG frame through ScreenCast Portal and PipeWire.

This is deliberately a standalone technical spike.  It does not select a
Veilshot backend or open the editor yet.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

try:
    from spikes.portal_helpers import check_host, request_path
except ModuleNotFoundError:  # Direct execution: python3 spikes/portal_pipewire_frame.py
    from portal_helpers import check_host, request_path

try:
    import gi

    gi.require_version("Gio", "2.0")
    from gi.repository import Gio, GLib
except (ImportError, ValueError) as exc:  # pragma: no cover - host dependency
    raise SystemExit(
        "PyGObject/GIO is required (Fedora package: python3-gobject)"
    ) from exc


PORTAL_BUS_NAME = "org.freedesktop.portal.Desktop"
PORTAL_OBJECT_PATH = "/org/freedesktop/portal/desktop"
SCREENCAST_INTERFACE = "org.freedesktop.portal.ScreenCast"
REQUEST_INTERFACE = "org.freedesktop.portal.Request"
SESSION_INTERFACE = "org.freedesktop.portal.Session"

SOURCE_MONITOR = 1
CURSOR_EMBEDDED = 2
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class PortalError(RuntimeError):
    """Raised when the portal rejects or cannot complete a request."""


def _token(prefix: str) -> str:
    return f"veilshot_{prefix}_{uuid.uuid4().hex}"


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
        predicted_path = request_path(
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
            predicted_path,
            None,
            Gio.DBusSignalFlags.NONE,
            on_response,
            None,
        )

        try:
            returned = self.proxy.call_sync(
                method,
                parameters,
                Gio.DBusCallFlags.NONE,
                -1,
                None,
            )
            returned_path = returned.unpack()[0]
            if returned_path != predicted_path:
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
        finally:
            self.connection.signal_unsubscribe(subscription_id)

        if response.get("timeout"):
            raise PortalError(f"{method} timed out")

        code = response.get("code")
        if code == 1:
            raise PortalError(f"{method} was cancelled by the user")
        if code != 0:
            raise PortalError(f"{method} failed with portal response {code}")
        return response["results"]

    def create_session(self) -> str:
        handle_token = _token("create")
        session_token = _token("session")
        results = self._request(
            "CreateSession",
            GLib.Variant(
                "(a{sv})",
                (
                    {
                        "handle_token": GLib.Variant("s", handle_token),
                        "session_handle_token": GLib.Variant("s", session_token),
                    },
                ),
            ),
            handle_token,
        )
        self.session_handle = str(results["session_handle"])
        return self.session_handle

    def select_monitor(self) -> None:
        if self.session_handle is None:
            raise PortalError("CreateSession must run before SelectSources")
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
            raise PortalError("CreateSession must run before Start")
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
            raise PortalError(f"Expected one monitor stream, received {len(streams)}")
        return int(streams[0][0])

    def open_pipewire_remote(self) -> int:
        if self.session_handle is None:
            raise PortalError("CreateSession must run before OpenPipeWireRemote")
        result, fd_list = self.proxy.call_with_unix_fd_list_sync(
            "OpenPipeWireRemote",
            GLib.Variant("(oa{sv})", (self.session_handle, {})),
            Gio.DBusCallFlags.NONE,
            -1,
            None,
            None,
        )
        fd_handle = result.unpack()[0]
        return fd_list.get(fd_handle)

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


def capture_png(pipewire_fd: int, node_id: int, timeout_seconds: int = 30) -> bytes:
    gst_launch = shutil.which("gst-launch-1.0")
    if gst_launch is None:
        raise RuntimeError(
            "gst-launch-1.0 is required (Fedora packages: "
            "gstreamer1, pipewire-gstreamer, gstreamer1-plugins-good)"
        )

    command = [
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
    ]
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        pass_fds=(pipewire_fd,),
        timeout=timeout_seconds,
        check=False,
    )
    if completed.returncode != 0:
        details = completed.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"GStreamer frame capture failed: {details}")
    if not completed.stdout.startswith(PNG_SIGNATURE):
        details = completed.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"GStreamer returned no valid PNG frame: {details}")
    return completed.stdout


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=Path("portal-frame.png"),
        help="PNG output path (default: ./portal-frame.png)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="check host prerequisites without opening the portal dialog",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    problems = check_host()
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 2
    if args.check:
        print("Portal/PipeWire spike prerequisites are available")
        return 0

    output = args.output.expanduser().resolve()
    if not output.parent.is_dir():
        print(f"error: output directory does not exist: {output.parent}", file=sys.stderr)
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
        output.write_bytes(png)
    except (GLib.Error, OSError, PortalError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        if pipewire_fd is not None:
            os.close(pipewire_fd)
        if portal is not None:
            try:
                portal.close()
            except GLib.Error:
                pass

    print(f"Captured one frame to {output} ({len(png)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
