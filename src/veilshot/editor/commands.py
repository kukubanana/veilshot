from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from veilshot.editor.annotations.base import Annotation
from veilshot.editor.model import EditorModel


class Command(Protocol):
    def redo(self) -> None: ...
    def undo(self) -> None: ...


@dataclass
class AddAnnotationCommand:
    model: EditorModel
    annotation: Annotation
    index: int | None = None

    def redo(self) -> None:
        if self.index is None:
            self.index = len(self.model.annotations)
        self.model.annotations.insert(self.index, self.annotation.clone())
        self.model.selected_index = self.index

    def undo(self) -> None:
        if self.index is None:
            return
        self.model.annotations.pop(self.index)
        self.model.selected_index = None


@dataclass
class DeleteAnnotationCommand:
    model: EditorModel
    index: int
    annotation: Annotation

    def redo(self) -> None:
        self.model.annotations.pop(self.index)
        self.model.selected_index = None

    def undo(self) -> None:
        self.model.annotations.insert(self.index, self.annotation.clone())
        self.model.selected_index = self.index


@dataclass
class ReplaceAnnotationCommand:
    model: EditorModel
    index: int
    before: Annotation
    after: Annotation

    def redo(self) -> None:
        self.model.annotations[self.index] = self.after.clone()
        self.model.selected_index = self.index

    def undo(self) -> None:
        self.model.annotations[self.index] = self.before.clone()
        self.model.selected_index = self.index


class UndoStack:
    def __init__(self) -> None:
        self._undo: list[Command] = []
        self._redo: list[Command] = []

    @property
    def can_undo(self) -> bool:
        return bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo)

    def push(self, command: Command) -> None:
        command.redo()
        self._undo.append(command)
        self._redo.clear()

    def push_completed(self, command: Command) -> None:
        """Record a command whose visible state was already applied interactively."""
        self._undo.append(command)
        self._redo.clear()

    def undo(self) -> None:
        if not self._undo:
            return
        command = self._undo.pop()
        command.undo()
        self._redo.append(command)

    def redo(self) -> None:
        if not self._redo:
            return
        command = self._redo.pop()
        command.redo()
        self._undo.append(command)
