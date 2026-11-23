"""Screen-capture backend selection."""

from __future__ import annotations

import os
from typing import Type

from veilshot.capture.base import CaptureBackend


def capture_backend_for_session(
    session_type: str | None = None,
) -> Type[CaptureBackend]:
    current_session = (
        session_type
        if session_type is not None
        else os.environ.get("XDG_SESSION_TYPE", "")
    ).lower()
    if current_session == "wayland":
        from veilshot.capture.portal import PortalCaptureBackend

        return PortalCaptureBackend

    from veilshot.capture.x11 import X11CaptureBackend

    return X11CaptureBackend
