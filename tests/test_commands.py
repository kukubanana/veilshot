import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor

from veilshot.editor.annotations.redaction import RedactionAnnotation
from veilshot.editor.commands import AddAnnotationCommand, UndoStack
from veilshot.editor.model import EditorModel


def test_add_undo_redo_annotation() -> None:
    model = EditorModel()
    stack = UndoStack()
    annotation = RedactionAnnotation(QRectF(1, 2, 30, 40), QColor("white"))

    stack.push(AddAnnotationCommand(model, annotation))
    assert len(model.annotations) == 1
    assert stack.can_undo

    stack.undo()
    assert model.annotations == []
    assert stack.can_redo

    stack.redo()
    assert len(model.annotations) == 1
