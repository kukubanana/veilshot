from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPainter


HANDLE_RADIUS = 6.0
HIT_MARGIN = 7.0


class Annotation(ABC):
    @abstractmethod
    def draw(self, painter: QPainter, selected: bool = False) -> None: ...

    @abstractmethod
    def hit_test(self, point: QPointF) -> bool: ...

    @abstractmethod
    def handle_at(self, point: QPointF) -> str | None: ...

    @abstractmethod
    def move_by(self, delta: QPointF, bounds: QRectF) -> None: ...

    @abstractmethod
    def resize_handle(self, handle: str, point: QPointF, bounds: QRectF) -> None: ...

    @abstractmethod
    def set_color(self, color) -> None: ...

    def clone(self) -> "Annotation":
        return deepcopy(self)

    @abstractmethod
    def state_key(self) -> tuple: ...
