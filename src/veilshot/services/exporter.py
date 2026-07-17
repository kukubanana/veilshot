from __future__ import annotations

from PySide6.QtCore import QRect, QRectF
from PySide6.QtGui import QImage, QPainter

from veilshot.editor.annotations.base import Annotation


def source_crop_rect(source: QImage, base_rect: QRectF, selection_rect: QRectF) -> QRect:
    if base_rect.width() <= 0 or base_rect.height() <= 0:
        raise ValueError("Base display rectangle is empty")
    selection = selection_rect.intersected(base_rect)
    scale_x = source.width() / base_rect.width()
    scale_y = source.height() / base_rect.height()
    x = round((selection.left() - base_rect.left()) * scale_x)
    y = round((selection.top() - base_rect.top()) * scale_y)
    width = max(1, round(selection.width() * scale_x))
    height = max(1, round(selection.height() * scale_y))
    return QRect(x, y, width, height).intersected(source.rect())


def render_flattened(
    source: QImage,
    base_rect: QRectF,
    selection_rect: QRectF,
    annotations: list[Annotation],
) -> QImage:
    crop_rect = source_crop_rect(source, base_rect, selection_rect)
    result = source.copy(crop_rect).convertToFormat(QImage.Format.Format_ARGB32)
    if result.isNull():
        raise ValueError("Could not create the exported image")

    painter = QPainter(result)
    try:
        scale_x = result.width() / max(selection_rect.width(), 1.0)
        scale_y = result.height() / max(selection_rect.height(), 1.0)
        painter.scale(scale_x, scale_y)
        for annotation in annotations:
            annotation.draw(painter, selected=False)
    finally:
        painter.end()
    return result
