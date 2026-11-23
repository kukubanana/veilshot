from __future__ import annotations

import importlib.util
from pathlib import Path


HELPERS_PATH = Path(__file__).parents[1] / "spikes" / "portal_helpers.py"
SPEC = importlib.util.spec_from_file_location("portal_helpers", HELPERS_PATH)
assert SPEC is not None and SPEC.loader is not None
portal_helpers = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(portal_helpers)


def test_request_path_uses_portal_sender_encoding() -> None:
    assert portal_helpers.request_path(":1.42", "veilshot_test") == (
        "/org/freedesktop/portal/desktop/request/1_42/veilshot_test"
    )


def test_check_host_reports_missing_wayland_and_bus(monkeypatch) -> None:
    monkeypatch.delenv("XDG_SESSION_TYPE", raising=False)
    monkeypatch.delenv("DBUS_SESSION_BUS_ADDRESS", raising=False)
    monkeypatch.setattr(
        portal_helpers.shutil, "which", lambda _name: "/usr/bin/tool"
    )

    assert portal_helpers.check_host() == [
        "XDG_SESSION_TYPE is not wayland",
        "no D-Bus session bus is available",
    ]
