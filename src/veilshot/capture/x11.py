from __future__ import annotations

from PySide6.QtGui import QCursor, QGuiApplication

from veilshot.capture.base import CaptureResult


class X11CaptureBackend:
    """Qt-based screen capture for X11 sessions."""

    @staticmethod
    def capture_screen_under_cursor() -> CaptureResult:
        screen = QGuiApplication.screenAt(QCursor.pos()) or QGuiApplication.primaryScreen()
        if screen is None:
            raise RuntimeError("Veilshot could not find an active display")

        pixmap = screen.grabWindow(0)
        if pixmap.isNull():
            raise RuntimeError(
                "Screen capture failed. Veilshot 0.1 requires an X11 session."
            )
        return CaptureResult(pixmap=pixmap, screen=screen)
