from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from PySide6.QtGui import QPixmap, QScreen


@dataclass(frozen=True)
class CaptureResult:
    pixmap: QPixmap
    screen: QScreen


class CaptureBackend(Protocol):
    @staticmethod
    def capture_screen_under_cursor() -> CaptureResult:
        """Capture the screen containing the pointer."""
