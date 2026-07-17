from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from PySide6.QtGui import QColor

from veilshot.editor.annotations.base import Annotation


class OverlayState(Enum):
    SELECTING_REGION = auto()
    EDITING = auto()
    COPYING = auto()
    SAVING = auto()
    CLOSING = auto()


class Tool(Enum):
    ARROW = "arrow"
    HIGHLIGHT = "highlight"
    REDACTION = "redaction"


@dataclass
class EditorModel:
    annotations: list[Annotation] = field(default_factory=list)
    selected_index: int | None = None
    active_tool: Tool = Tool.REDACTION
    tool_colors: dict[Tool, QColor] = field(
        default_factory=lambda: {
            Tool.ARROW: QColor("#ef4444"),
            Tool.HIGHLIGHT: QColor("#facc15"),
            Tool.REDACTION: QColor("#ffffff"),
        }
    )

    def selected(self) -> Annotation | None:
        if self.selected_index is None:
            return None
        if 0 <= self.selected_index < len(self.annotations):
            return self.annotations[self.selected_index]
        self.selected_index = None
        return None

    def set_selected(self, index: int | None) -> None:
        self.selected_index = index
