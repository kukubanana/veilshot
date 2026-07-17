import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from veilshot.editor.annotations.redaction import RedactionAnnotation
from veilshot.editor.overlay import OverlayWindow
from veilshot.services.clipboard import ClipboardKeeper


def test_drag_creates_default_redaction_and_flattens_it() -> None:
    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    pixmap = QPixmap(500, 350)
    pixmap.fill(QColor("red"))
    screen = app.primaryScreen()
    assert screen is not None
    keeper = ClipboardKeeper(app, timeout_ms=100)
    overlay = OverlayWindow.for_existing_image(pixmap, screen, keeper)
    overlay.show_overlay()
    app.processEvents()

    start = overlay._selection_rect.topLeft().toPoint() + QPoint(30, 30)
    end = start + QPoint(80, 45)
    QTest.mousePress(overlay, Qt.MouseButton.LeftButton, pos=start)
    QTest.mouseMove(overlay, end, delay=10)
    QTest.mouseRelease(overlay, Qt.MouseButton.LeftButton, pos=end)
    app.processEvents()

    assert len(overlay._model.annotations) == 1
    assert isinstance(overlay._model.annotations[0], RedactionAnnotation)
    exported = overlay._render()
    source_point = start - overlay._selection_rect.topLeft().toPoint() + QPoint(10, 10)
    scale_x = exported.width() / overlay._selection_rect.width()
    scale_y = exported.height() / overlay._selection_rect.height()
    sampled = exported.pixelColor(round(source_point.x() * scale_x), round(source_point.y() * scale_y))
    assert sampled == QColor("white")
    overlay.close()
