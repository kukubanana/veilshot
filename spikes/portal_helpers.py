"""Pure helpers shared by the portal spike and its dependency-free tests."""

from __future__ import annotations

import os
import shutil


def request_path(unique_bus_name: str, handle_token: str) -> str:
    sender = unique_bus_name.lstrip(":").replace(".", "_")
    return f"/org/freedesktop/portal/desktop/request/{sender}/{handle_token}"


def check_host() -> list[str]:
    problems: list[str] = []
    if os.environ.get("XDG_SESSION_TYPE") != "wayland":
        problems.append("XDG_SESSION_TYPE is not wayland")
    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS"):
        problems.append("no D-Bus session bus is available")
    if shutil.which("gst-launch-1.0") is None:
        problems.append("gst-launch-1.0 is missing")
    return problems
