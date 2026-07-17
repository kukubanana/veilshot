from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPen

from veilshot.editor.annotations.base import Annotation, HANDLE_RADIUS, HIT_MARGIN


@dataclass
class RectAnnotation(Annotation):
    rect: QRectF
    color: QColor

    def normalized_rect(self) -> QRectF:
        return self.rect.normalized()

    def _handles(self) -> dict[str, QPointF]:
        r = self.normalized_rect()
        return {
            "nw": r.topLeft(),
            "n": QPointF(r.center().x(), r.top()),
            "ne": r.topRight(),
            "e": QPointF(r.right(), r.center().y()),
            "se": r.bottomRight(),
            "s": QPointF(r.center().x(), r.bottom()),
            "sw": r.bottomLeft(),
            "w": QPointF(r.left(), r.center().y()),
        }

    def hit_test(self, point: QPointF) -> bool:
        return self.normalized_rect().adjusted(-HIT_MARGIN, -HIT_MARGIN, HIT_MARGIN, HIT_MARGIN).contains(point)

    def handle_at(self, point: QPointF) -> str | None:
        for name, handle in self._handles().items():
            if (handle - point).manhattanLength() <= HANDLE_RADIUS * 2:
                return name
        return None

    def move_by(self, delta: QPointF, bounds: QRectF) -> None:
        r = self.normalized_rect().translated(delta)
        if r.left() < bounds.left():
            r.moveLeft(bounds.left())
        if r.top() < bounds.top():
            r.moveTop(bounds.top())
        if r.right() > bounds.right():
            r.moveRight(bounds.right())
        if r.bottom() > bounds.bottom():
            r.moveBottom(bounds.bottom())
        self.rect = r

    def resize_handle(self, handle: str, point: QPointF, bounds: QRectF) -> None:
        p = QPointF(
            min(max(point.x(), bounds.left()), bounds.right()),
            min(max(point.y(), bounds.top()), bounds.bottom()),
        )
        r = self.normalized_rect()
        left, top, right, bottom = r.left(), r.top(), r.right(), r.bottom()
        if "w" in handle:
            left = min(p.x(), right - 4.0)
        if "e" in handle:
            right = max(p.x(), left + 4.0)
        if "n" in handle:
            top = min(p.y(), bottom - 4.0)
        if "s" in handle:
            bottom = max(p.y(), top + 4.0)
        self.rect = QRectF(QPointF(left, top), QPointF(right, bottom)).normalized()

    def set_color(self, color: QColor) -> None:
        self.color = QColor(color)

    def _draw_selection(self, painter: QPainter) -> None:
        painter.save()
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(QPen(QColor("#111827"), 1.0))
        for point in self._handles().values():
            painter.drawEllipse(point, HANDLE_RADIUS, HANDLE_RADIUS)
        painter.restore()

    def state_key(self) -> tuple:
        r = self.normalized_rect()
        return (
            type(self).__name__,
            round(r.x(), 3),
            round(r.y(), 3),
            round(r.width(), 3),
            round(r.height(), 3),
            self.color.rgba(),
        )
