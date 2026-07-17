from __future__ import annotations

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QClipboard, QImage
from PySide6.QtWidgets import QApplication


class ClipboardKeeper(QObject):
    """Keep an X11 clipboard image alive after the overlay is hidden."""

    copy_failed = Signal(str)

    def __init__(self, app: QApplication, timeout_ms: int = 120_000) -> None:
        super().__init__()
        self._app = app
        self._clipboard = app.clipboard()
        self._timeout_ms = timeout_ms
        self._armed = False
        self._clipboard.changed.connect(self._on_clipboard_changed)

    def copy_image_and_wait(self, image: QImage) -> None:
        if image.isNull():
            self.copy_failed.emit("The exported image is empty")
            return
        self._armed = False
        self._clipboard.setImage(image, QClipboard.Mode.Clipboard)
        QTimer.singleShot(250, self._arm)
        QTimer.singleShot(self._timeout_ms, self._app.quit)

    def _arm(self) -> None:
        self._armed = True
        # A clipboard manager may already have taken ownership while preserving data.
        if not self._clipboard.ownsClipboard():
            self._app.quit()

    def _on_clipboard_changed(self, mode: QClipboard.Mode) -> None:
        if mode != QClipboard.Mode.Clipboard or not self._armed:
            return
        if not self._clipboard.ownsClipboard():
            self._app.quit()
