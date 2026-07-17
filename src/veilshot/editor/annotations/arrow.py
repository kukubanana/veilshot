from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, pi, sin

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen

from veilshot.editor.annotations.base import Annotation, HANDLE_RADIUS, HIT_MARGIN


@dataclass
class ArrowAnnotation(Annotation):
    start: QPointF
    end: QPointF
    color: QColor
    width: float = 4.0

    def draw(self, painter: QPainter, selected: bool = False) -> None:
        painter.save()
        pen = QPen(self.color, self.width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawLine(self.start, self.end)

        angle = atan2(self.end.y() - self.start.y(), self.end.x() - self.start.x())
        head = 12.0 + self.width
        left = QPointF(
            self.end.x() - head * cos(angle - pi / 6),
            self.end.y() - head * sin(angle - pi / 6),
        )
        right = QPointF(
            self.end.x() - head * cos(angle + pi / 6),
            self.end.y() - head * sin(angle + pi / 6),
        )
        path = QPainterPath(self.end)
        path.lineTo(left)
        path.lineTo(right)
        path.closeSubpath()
        painter.fillPath(path, self.color)
        painter.restore()

        if selected:
            painter.save()
            painter.setBrush(QColor("#ffffff"))
            painter.setPen(QPen(QColor("#111827"), 1.0))
            painter.drawEllipse(self.start, HANDLE_RADIUS, HANDLE_RADIUS)
            painter.drawEllipse(self.end, HANDLE_RADIUS, HANDLE_RADIUS)
            painter.restore()

    def hit_test(self, point: QPointF) -> bool:
        vx = self.end.x() - self.start.x()
        vy = self.end.y() - self.start.y()
        length_sq = vx * vx + vy * vy
        if length_sq == 0:
            return hypot(point.x() - self.start.x(), point.y() - self.start.y()) <= HIT_MARGIN
        t = ((point.x() - self.start.x()) * vx + (point.y() - self.start.y()) * vy) / length_sq
        t = max(0.0, min(1.0, t))
        projection = QPointF(self.start.x() + t * vx, self.start.y() + t * vy)
        return hypot(point.x() - projection.x(), point.y() - projection.y()) <= HIT_MARGIN

    def handle_at(self, point: QPointF) -> str | None:
        if (self.start - point).manhattanLength() <= HANDLE_RADIUS * 2:
            return "start"
        if (self.end - point).manhattanLength() <= HANDLE_RADIUS * 2:
            return "end"
        return None

    def move_by(self, delta: QPointF, bounds: QRectF) -> None:
        proposed_start = self.start + delta
        proposed_end = self.end + delta
        dx = delta.x()
        dy = delta.y()
        min_x = min(proposed_start.x(), proposed_end.x())
        max_x = max(proposed_start.x(), proposed_end.x())
        min_y = min(proposed_start.y(), proposed_end.y())
        max_y = max(proposed_start.y(), proposed_end.y())
        if min_x < bounds.left():
            dx += bounds.left() - min_x
        if max_x > bounds.right():
            dx -= max_x - bounds.right()
        if min_y < bounds.top():
            dy += bounds.top() - min_y
        if max_y > bounds.bottom():
            dy -= max_y - bounds.bottom()
        adjusted = QPointF(dx, dy)
        self.start += adjusted
        self.end += adjusted

    def resize_handle(self, handle: str, point: QPointF, bounds: QRectF) -> None:
        clamped = QPointF(
            min(max(point.x(), bounds.left()), bounds.right()),
            min(max(point.y(), bounds.top()), bounds.bottom()),
        )
        if handle == "start":
            self.start = clamped
        elif handle == "end":
            self.end = clamped

    def set_color(self, color: QColor) -> None:
        self.color = QColor(color)

    def state_key(self) -> tuple:
        return (
            type(self).__name__,
            round(self.start.x(), 3),
            round(self.start.y(), 3),
            round(self.end.x(), 3),
            round(self.end.y(), 3),
            self.color.rgba(),
            round(self.width, 3),
        )
