from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from PySide6.QtCore import QPointF

from veilshot.editor.annotations.base import Annotation


class InteractionKind(Enum):
    NONE = auto()
    CREATE = auto()
    MOVE = auto()
    RESIZE = auto()


@dataclass
class Interaction:
    kind: InteractionKind = InteractionKind.NONE
    press_point: QPointF | None = None
    last_point: QPointF | None = None
    annotation_index: int | None = None
    handle: str | None = None
    before: Annotation | None = None
    draft: Annotation | None = None

    def reset(self) -> None:
        self.kind = InteractionKind.NONE
        self.press_point = None
        self.last_point = None
        self.annotation_index = None
        self.handle = None
        self.before = None
        self.draft = None
