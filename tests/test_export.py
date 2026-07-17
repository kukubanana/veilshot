import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QImage

from veilshot.editor.annotations.redaction import RedactionAnnotation
from veilshot.services.exporter import render_flattened, source_crop_rect


def test_source_crop_rect_scales_from_display_coordinates() -> None:
    image = QImage(200, 100, QImage.Format.Format_ARGB32)
    crop = source_crop_rect(image, QRectF(0, 0, 100, 50), QRectF(10, 5, 20, 10))
    assert (crop.x(), crop.y(), crop.width(), crop.height()) == (20, 10, 40, 20)


def test_redaction_replaces_exported_pixels() -> None:
    source = QImage(100, 100, QImage.Format.Format_ARGB32)
    source.fill(QColor("red"))
    redaction = RedactionAnnotation(QRectF(10, 10, 20, 20), QColor("white"))
    result = render_flattened(
        source,
        QRectF(0, 0, 100, 100),
        QRectF(0, 0, 100, 100),
        [redaction],
    )
    assert result.pixelColor(15, 15) == QColor("white")
    assert result.pixelColor(5, 5) == QColor("red")
