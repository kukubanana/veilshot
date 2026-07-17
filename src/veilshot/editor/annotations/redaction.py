from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen

from veilshot.editor.annotations.rect import RectAnnotation


@dataclass
class RedactionAnnotation(RectAnnotation):
    def draw(self, painter: QPainter, selected: bool = False) -> None:
        color = QColor(self.color)
        color.setAlpha(255)
        painter.save()
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(color)
        painter.drawRect(self.normalized_rect())
        painter.restore()
        if selected:
            self._draw_selection(painter)

    def set_color(self, color: QColor) -> None:
        opaque = QColor(color)
        opaque.setAlpha(255)
        self.color = opaque
