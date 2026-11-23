from __future__ import annotations

import os
import shutil
import subprocess

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QObject, QTimer, Signal
from PySide6.QtGui import QClipboard, QImage
from PySide6.QtWidgets import QApplication


class ClipboardKeeper(QObject):
    """Publish an image using the native clipboard lifecycle for the session."""

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
        if self._copy_with_wayland_helper(image):
            QTimer.singleShot(0, self._app.quit)
            return
        self._armed = False
        self._clipboard.setImage(image, QClipboard.Mode.Clipboard)
        QTimer.singleShot(250, self._arm)
        QTimer.singleShot(self._timeout_ms, self._app.quit)

    def _copy_with_wayland_helper(self, image: QImage) -> bool:
        if os.environ.get("XDG_SESSION_TYPE", "").lower() != "wayland":
            return False
        wl_copy = shutil.which("wl-copy")
        if wl_copy is None:
            # Qt remains the fallback. Keep the invisible process alive for the
            # full timeout because ownsClipboard() is unreliable on Wayland.
            return False

        data = QByteArray()
        buffer = QBuffer(data)
        if not buffer.open(QIODevice.OpenModeFlag.WriteOnly):
            return False
        if not image.save(buffer, "PNG"):
            return False
        try:
            completed = subprocess.run(
                [wl_copy, "--type", "image/png"],
                input=bytes(data),
                stdout=subprocess.DEVNULL,
                # wl-copy forks a background clipboard owner. A captured pipe
                # can stay inherited by that child and make communicate() wait.
                stderr=subprocess.DEVNULL,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        return completed.returncode == 0

    def _arm(self) -> None:
        self._armed = True
        if os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland":
            return
        # A clipboard manager may already have taken ownership while preserving data.
        if not self._clipboard.ownsClipboard():
            self._app.quit()

    def _on_clipboard_changed(self, mode: QClipboard.Mode) -> None:
        if mode != QClipboard.Mode.Clipboard or not self._armed:
            return
        if os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland":
            return
        if not self._clipboard.ownsClipboard():
            self._app.quit()
