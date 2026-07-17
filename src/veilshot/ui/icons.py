from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap


def _icon(draw: Callable[[QPainter], None]) -> QIcon:
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    draw(painter)
    painter.end()
    return QIcon(pixmap)


def _pen() -> QPen:
    pen = QPen(QColor("#f8fafc"), 2.0)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    return pen


def arrow_icon() -> QIcon:
    def draw(p: QPainter) -> None:
        p.setPen(_pen())
        p.drawLine(QPointF(4, 19), QPointF(19, 5))
        p.drawLine(QPointF(19, 5), QPointF(18, 12))
        p.drawLine(QPointF(19, 5), QPointF(12, 6))
    return _icon(draw)


def highlight_icon() -> QIcon:
    def draw(p: QPainter) -> None:
        p.setPen(_pen())
        p.setBrush(QColor(250, 204, 21, 110))
        p.drawRoundedRect(QRectF(4, 6, 16, 12), 2, 2)
    return _icon(draw)


def redact_icon() -> QIcon:
    def draw(p: QPainter) -> None:
        p.setPen(_pen())
        p.setBrush(QColor("#f8fafc"))
        p.drawRoundedRect(QRectF(4, 7, 16, 10), 2, 2)
    return _icon(draw)


def undo_icon(reverse: bool = False) -> QIcon:
    def draw(p: QPainter) -> None:
        p.setPen(_pen())
        if reverse:
            p.drawArc(QRectF(4, 5, 15, 14), -30 * 16, 220 * 16)
            p.drawLine(QPointF(17, 5), QPointF(20, 9))
            p.drawLine(QPointF(17, 5), QPointF(13, 7))
        else:
            p.drawArc(QRectF(5, 5, 15, 14), -10 * 16, -220 * 16)
            p.drawLine(QPointF(7, 5), QPointF(4, 9))
            p.drawLine(QPointF(7, 5), QPointF(11, 7))
    return _icon(draw)


def copy_icon() -> QIcon:
    def draw(p: QPainter) -> None:
        p.setPen(_pen())
        p.drawRoundedRect(QRectF(8, 5, 11, 13), 1.5, 1.5)
        p.drawRoundedRect(QRectF(5, 8, 11, 11), 1.5, 1.5)
    return _icon(draw)


def save_icon() -> QIcon:
    def draw(p: QPainter) -> None:
        p.setPen(_pen())
        p.drawRoundedRect(QRectF(5, 4, 14, 16), 1.5, 1.5)
        p.drawRect(QRectF(8, 5, 7, 5))
        p.drawRoundedRect(QRectF(8, 14, 8, 5), 1, 1)
    return _icon(draw)


def close_icon() -> QIcon:
    def draw(p: QPainter) -> None:
        p.setPen(_pen())
        p.drawLine(QPointF(6, 6), QPointF(18, 18))
        p.drawLine(QPointF(18, 6), QPointF(6, 18))
    return _icon(draw)


def eyedropper_icon() -> QIcon:
    def draw(p: QPainter) -> None:
        p.setPen(_pen())
        p.drawLine(QPointF(7, 18), QPointF(17, 8))
        p.drawLine(QPointF(14, 5), QPointF(19, 10))
        p.drawLine(QPointF(5, 20), QPointF(8, 17))
    return _icon(draw)
