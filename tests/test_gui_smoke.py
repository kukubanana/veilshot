import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")

from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QApplication

from veilshot.editor.overlay import OverlayWindow
from veilshot.services.clipboard import ClipboardKeeper


def test_existing_image_overlay_can_paint() -> None:
    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    pixmap = QPixmap(640, 480)
    pixmap.fill(QColor("steelblue"))
    screen = app.primaryScreen()
    assert screen is not None
    keeper = ClipboardKeeper(app, timeout_ms=100)
    overlay = OverlayWindow.for_existing_image(pixmap, screen, keeper)
    overlay.show_overlay()
    app.processEvents()
    rendered = overlay.grab()
    assert not rendered.isNull()
    overlay.close()
