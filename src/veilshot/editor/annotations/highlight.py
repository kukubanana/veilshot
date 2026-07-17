from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QColor, QPainter, QPen

from veilshot.editor.annotations.rect import RectAnnotation


@dataclass
class HighlightAnnotation(RectAnnotation):
    def draw(self, painter: QPainter, selected: bool = False) -> None:
        color = QColor(self.color)
        color.setAlphaF(0.34)
        painter.save()
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(color)
        painter.drawRect(self.normalized_rect())
        painter.restore()
        if selected:
            self._draw_selection(painter)


from PySide6.QtCore import Qt  # Kept after class to keep imports visually compact.
