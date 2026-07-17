import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QColor, QImage, QPainter

from veilshot.editor.annotations.arrow import ArrowAnnotation
from veilshot.editor.annotations.highlight import HighlightAnnotation
from veilshot.editor.annotations.redaction import RedactionAnnotation


def test_all_annotations_draw_without_error() -> None:
    image = QImage(200, 120, QImage.Format.Format_ARGB32)
    image.fill(QColor("transparent"))
    painter = QPainter(image)
    try:
        ArrowAnnotation(QPointF(10, 20), QPointF(150, 80), QColor("red")).draw(painter, True)
        HighlightAnnotation(QRectF(20, 20, 60, 30), QColor("yellow")).draw(painter, True)
        RedactionAnnotation(QRectF(90, 20, 60, 30), QColor("white")).draw(painter, True)
    finally:
        painter.end()

    assert not image.isNull()


def test_arrow_stays_inside_bounds_when_moved() -> None:
    arrow = ArrowAnnotation(QPointF(10, 10), QPointF(20, 20), QColor("red"))
    arrow.move_by(QPointF(-50, -50), QRectF(0, 0, 100, 100))
    assert arrow.start.x() >= 0
    assert arrow.start.y() >= 0
