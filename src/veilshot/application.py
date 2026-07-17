from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QIcon, QImageReader, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox

from veilshot.capture.x11 import X11CaptureBackend
from veilshot.editor.overlay import OverlayWindow
from veilshot.resources import app_icon_path
from veilshot.services.clipboard import ClipboardKeeper


def _load_pixmap(path: Path) -> QPixmap:
    reader = QImageReader(str(path))
    reader.setAutoTransform(True)
    image = reader.read()
    if image.isNull():
        raise ValueError(reader.errorString() or "Unsupported or invalid image")
    return QPixmap.fromImage(image)


def run(edit_path: Path | None = None) -> int:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Veilshot")
    app.setOrganizationName("Veilshot")
    app.setWindowIcon(QIcon(str(app_icon_path())))
    app.setQuitOnLastWindowClosed(False)

    clipboard_keeper = ClipboardKeeper(app)

    try:
        if edit_path is not None:
            screen = QGuiApplication.primaryScreen()
            if screen is None:
                raise RuntimeError("No screen is available")
            pixmap = _load_pixmap(edit_path)
            overlay = OverlayWindow.for_existing_image(
                pixmap=pixmap,
                screen=screen,
                clipboard_keeper=clipboard_keeper,
            )
        else:
            capture = X11CaptureBackend.capture_screen_under_cursor()
            overlay = OverlayWindow.for_capture(
                pixmap=capture.pixmap,
                screen=capture.screen,
                clipboard_keeper=clipboard_keeper,
            )
    except Exception as exc:  # GUI boundary: show a useful error to a beginner.
        QMessageBox.critical(None, "Veilshot", str(exc))
        return 1

    # Keep Python references alive for the duration of the event loop.
    app._veilshot_overlay = overlay  # type: ignore[attr-defined]
    app._veilshot_clipboard_keeper = clipboard_keeper  # type: ignore[attr-defined]
    overlay.show_overlay()
    return app.exec()
