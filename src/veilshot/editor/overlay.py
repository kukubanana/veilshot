from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, QPointF, QRect, QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QCursor,
    QKeyEvent,
    QMouseEvent,
    QPainter,
    QPen,
    QPixmap,
    QRegion,
    QScreen,
)
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

from veilshot.editor.annotations import (
    ArrowAnnotation,
    HighlightAnnotation,
    RedactionAnnotation,
)
from veilshot.editor.annotations.base import Annotation
from veilshot.editor.canvas import Interaction, InteractionKind
from veilshot.editor.commands import (
    AddAnnotationCommand,
    DeleteAnnotationCommand,
    ReplaceAnnotationCommand,
    UndoStack,
)
from veilshot.editor.model import EditorModel, OverlayState, Tool
from veilshot.services.clipboard import ClipboardKeeper
from veilshot.services.exporter import render_flattened
from veilshot.services.filename import screenshot_filename
from veilshot.ui.toolbar import EditorToolbar


class OverlayWindow(QWidget):
    MIN_SELECTION = 6.0

    def __init__(
        self,
        pixmap: QPixmap,
        screen: QScreen,
        clipboard_keeper: ClipboardKeeper,
        edit_existing: bool,
    ) -> None:
        super().__init__()
        self._source_pixmap = pixmap
        self._source_image = pixmap.toImage()
        self._screen = screen
        self._clipboard_keeper = clipboard_keeper
        self._edit_existing = edit_existing
        self._state = OverlayState.EDITING if edit_existing else OverlayState.SELECTING_REGION
        self._model = EditorModel()
        self._undo = UndoStack()
        self._interaction = Interaction()
        self._selection_start: QPointF | None = None
        self._selection_rect = QRectF()
        self._eyedropper_pending = False

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        self.setGeometry(screen.geometry())

        self._base_rect = self._calculate_base_rect()
        if edit_existing:
            self._selection_rect = QRectF(self._base_rect)

        self._toolbar = EditorToolbar(self)
        self._toolbar.hide()
        self._toolbar.tool_selected.connect(self._set_tool)
        self._toolbar.color_selected.connect(self._set_color)
        self._toolbar.eyedropper_requested.connect(self._start_eyedropper)
        self._toolbar.undo_requested.connect(self._undo_action)
        self._toolbar.redo_requested.connect(self._redo_action)
        self._toolbar.copy_requested.connect(self._copy)
        self._toolbar.save_requested.connect(self._save)
        self._toolbar.close_requested.connect(self._cancel)

    @classmethod
    def for_capture(
        cls, pixmap: QPixmap, screen: QScreen, clipboard_keeper: ClipboardKeeper
    ) -> "OverlayWindow":
        return cls(pixmap, screen, clipboard_keeper, edit_existing=False)

    @classmethod
    def for_existing_image(
        cls, pixmap: QPixmap, screen: QScreen, clipboard_keeper: ClipboardKeeper
    ) -> "OverlayWindow":
        return cls(pixmap, screen, clipboard_keeper, edit_existing=True)

    def _calculate_base_rect(self) -> QRectF:
        screen_size = self._screen.geometry().size()
        if not self._edit_existing:
            return QRectF(0, 0, screen_size.width(), screen_size.height())
        margin = 60.0
        available_w = max(100.0, screen_size.width() - margin * 2)
        available_h = max(100.0, screen_size.height() - margin * 2 - 60)
        logical_source = self._source_pixmap.deviceIndependentSize()
        scale = min(available_w / logical_source.width(), available_h / logical_source.height(), 1.0)
        width = logical_source.width() * scale
        height = logical_source.height() * scale
        return QRectF(
            (screen_size.width() - width) / 2,
            (screen_size.height() - height) / 2 - 20,
            width,
            height,
        )

    def show_overlay(self) -> None:
        # Bind the native window to the target monitor before entering full screen.
        self.winId()
        if self.windowHandle() is not None:
            self.windowHandle().setScreen(self._screen)
        self.setGeometry(self._screen.geometry())
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        self.setFocus(Qt.FocusReason.ActiveWindowFocusReason)
        if self._edit_existing:
            self._enter_editing()

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt API
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#080b12"))
        painter.drawPixmap(self._base_rect, self._source_pixmap, QRectF(self._source_pixmap.rect()))

        if self._state == OverlayState.SELECTING_REGION:
            self._paint_selection(painter)
        else:
            self._paint_editor(painter)

    def _paint_selection(self, painter: QPainter) -> None:
        painter.fillRect(self._base_rect, QColor(0, 0, 0, 115))
        if self._selection_rect.isEmpty():
            return
        source_rect = self._display_rect_to_source(self._selection_rect)
        painter.drawPixmap(self._selection_rect, self._source_pixmap, source_rect)
        painter.setPen(QPen(QColor("#ffffff"), 1.2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self._selection_rect)
        label = f"{round(source_rect.width())} × {round(source_rect.height())}"
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self._selection_rect.topLeft() + QPointF(5, -7), label)

    def _paint_editor(self, painter: QPainter) -> None:
        if self._selection_rect.isEmpty():
            return
        # Dim everything outside the selected image region.
        painter.save()
        outside = QRegion(self.rect()).subtracted(QRegion(self._selection_rect.toAlignedRect()))
        painter.setClipRegion(outside)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 125))
        painter.restore()

        painter.save()
        painter.setClipRect(self._selection_rect)
        painter.translate(self._selection_rect.topLeft())
        selected = self._model.selected_index
        for index, annotation in enumerate(self._model.annotations):
            annotation.draw(painter, selected=index == selected)
        if self._interaction.draft is not None:
            self._interaction.draft.draw(painter, selected=False)
        painter.restore()

        painter.setPen(QPen(QColor(255, 255, 255, 180), 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self._selection_rect)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() != Qt.MouseButton.LeftButton:
            return
        point = event.position()
        if self._state == OverlayState.SELECTING_REGION:
            if not self._base_rect.contains(point):
                return
            self._selection_start = self._clamp_to_rect(point, self._base_rect)
            self._selection_rect = QRectF(self._selection_start, self._selection_start)
            self.update()
            return
        if self._state != OverlayState.EDITING:
            return
        if self._eyedropper_pending:
            self._sample_color(point)
            return
        if not self._selection_rect.contains(point):
            self._model.set_selected(None)
            self.update()
            return

        local = point - self._selection_rect.topLeft()
        selected = self._model.selected()
        if selected is not None:
            handle = selected.handle_at(local)
            if handle is not None:
                self._begin_modify(local, InteractionKind.RESIZE, handle)
                return

        hit_index = self._hit_annotation(local)
        if hit_index is not None:
            self._model.set_selected(hit_index)
            self._begin_modify(local, InteractionKind.MOVE, None)
            self._sync_toolbar()
            self.update()
            return

        self._model.set_selected(None)
        self._begin_create(local)
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        point = event.position()
        if self._state == OverlayState.SELECTING_REGION and self._selection_start is not None:
            current = self._clamp_to_rect(point, self._base_rect)
            self._selection_rect = QRectF(self._selection_start, current).normalized()
            self.update()
            return
        if self._state != OverlayState.EDITING:
            return
        if self._eyedropper_pending:
            return
        if self._interaction.kind == InteractionKind.NONE:
            return

        local = point - self._selection_rect.topLeft()
        bounds = QRectF(0, 0, self._selection_rect.width(), self._selection_rect.height())
        local = self._clamp_to_rect(local, bounds)

        if self._interaction.kind == InteractionKind.CREATE:
            self._update_draft(local)
        elif self._interaction.kind == InteractionKind.MOVE:
            annotation = self._model.selected()
            if annotation is not None and self._interaction.last_point is not None:
                annotation.move_by(local - self._interaction.last_point, bounds)
                self._interaction.last_point = local
        elif self._interaction.kind == InteractionKind.RESIZE:
            annotation = self._model.selected()
            if annotation is not None and self._interaction.handle is not None:
                annotation.resize_handle(self._interaction.handle, local, bounds)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() != Qt.MouseButton.LeftButton:
            return
        if self._state == OverlayState.SELECTING_REGION and self._selection_start is not None:
            self._selection_start = None
            if (
                self._selection_rect.width() >= self.MIN_SELECTION
                and self._selection_rect.height() >= self.MIN_SELECTION
            ):
                self._enter_editing()
            else:
                self._selection_rect = QRectF()
            self.update()
            return
        if self._state != OverlayState.EDITING:
            return

        if self._interaction.kind == InteractionKind.CREATE:
            draft = self._interaction.draft
            if draft is not None and self._annotation_is_meaningful(draft):
                self._undo.push(AddAnnotationCommand(self._model, draft))
        elif self._interaction.kind in (InteractionKind.MOVE, InteractionKind.RESIZE):
            index = self._interaction.annotation_index
            before = self._interaction.before
            current = self._model.selected()
            if index is not None and before is not None and current is not None:
                after = current.clone()
                if before.state_key() != after.state_key():
                    self._undo.push_completed(
                        ReplaceAnnotationCommand(self._model, index, before, after)
                    )
        self._interaction.reset()
        self._sync_toolbar()
        self.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        modifiers = event.modifiers()
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self._cancel()
            return
        if self._state != OverlayState.EDITING:
            return
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            if key == Qt.Key.Key_C:
                self._copy()
                return
            if key == Qt.Key.Key_Z:
                if modifiers & Qt.KeyboardModifier.ShiftModifier:
                    self._redo_action()
                else:
                    self._undo_action()
                return
            if key == Qt.Key.Key_S and modifiers & Qt.KeyboardModifier.ShiftModifier:
                self._save()
                return
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._copy()
        elif key == Qt.Key.Key_Delete:
            self._delete_selected()
        elif key == Qt.Key.Key_A:
            self._set_tool(Tool.ARROW)
        elif key == Qt.Key.Key_H:
            self._set_tool(Tool.HIGHLIGHT)
        elif key == Qt.Key.Key_R:
            self._set_tool(Tool.REDACTION)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._position_toolbar()

    def _enter_editing(self) -> None:
        self._state = OverlayState.EDITING
        self.setCursor(Qt.CursorShape.CrossCursor)
        self._model.active_tool = Tool.REDACTION
        self._toolbar.show()
        self._position_toolbar()
        self._sync_toolbar()
        self.update()

    def _set_tool(self, tool: Tool) -> None:
        self._eyedropper_pending = False
        self._model.active_tool = tool
        self.setCursor(Qt.CursorShape.CrossCursor)
        self._sync_toolbar()

    def _set_color(self, color: QColor) -> None:
        tool = self._model.active_tool
        normalized = QColor(color)
        if tool == Tool.REDACTION:
            normalized.setAlpha(255)
        selected = self._model.selected()
        if selected is not None:
            index = self._model.selected_index
            before = selected.clone()
            selected.set_color(normalized)
            after = selected.clone()
            if index is not None and before.state_key() != after.state_key():
                self._undo.push_completed(
                    ReplaceAnnotationCommand(self._model, index, before, after)
                )
        self._model.tool_colors[tool] = normalized
        self._sync_toolbar()
        self.update()

    def _start_eyedropper(self) -> None:
        self._eyedropper_pending = True
        self.setCursor(Qt.CursorShape.CrossCursor)

    def _sample_color(self, display_point: QPointF) -> None:
        if not self._base_rect.contains(display_point):
            return
        source_point = self._display_point_to_source(display_point)
        x = min(max(round(source_point.x()), 0), self._source_image.width() - 1)
        y = min(max(round(source_point.y()), 0), self._source_image.height() - 1)
        self._eyedropper_pending = False
        self._set_color(self._source_image.pixelColor(x, y))

    def _begin_create(self, point: QPointF) -> None:
        self._interaction.reset()
        self._interaction.kind = InteractionKind.CREATE
        self._interaction.press_point = point
        self._interaction.last_point = point
        self._update_draft(point)

    def _update_draft(self, point: QPointF) -> None:
        start = self._interaction.press_point
        if start is None:
            return
        color = QColor(self._model.tool_colors[self._model.active_tool])
        if self._model.active_tool == Tool.ARROW:
            self._interaction.draft = ArrowAnnotation(start, point, color)
        else:
            rect = QRectF(start, point).normalized()
            if self._model.active_tool == Tool.HIGHLIGHT:
                self._interaction.draft = HighlightAnnotation(rect, color)
            else:
                color.setAlpha(255)
                self._interaction.draft = RedactionAnnotation(rect, color)

    def _begin_modify(
        self, point: QPointF, kind: InteractionKind, handle: str | None
    ) -> None:
        selected = self._model.selected()
        if selected is None or self._model.selected_index is None:
            return
        self._interaction.reset()
        self._interaction.kind = kind
        self._interaction.press_point = point
        self._interaction.last_point = point
        self._interaction.annotation_index = self._model.selected_index
        self._interaction.handle = handle
        self._interaction.before = selected.clone()

    def _hit_annotation(self, point: QPointF) -> int | None:
        for index in range(len(self._model.annotations) - 1, -1, -1):
            if self._model.annotations[index].hit_test(point):
                return index
        return None

    def _delete_selected(self) -> None:
        index = self._model.selected_index
        selected = self._model.selected()
        if index is None or selected is None:
            return
        self._undo.push(DeleteAnnotationCommand(self._model, index, selected.clone()))
        self._sync_toolbar()
        self.update()

    def _undo_action(self) -> None:
        self._undo.undo()
        self._sync_toolbar()
        self.update()

    def _redo_action(self) -> None:
        self._undo.redo()
        self._sync_toolbar()
        self.update()

    def _render(self):
        return render_flattened(
            source=self._source_image,
            base_rect=self._base_rect,
            selection_rect=self._selection_rect,
            annotations=self._model.annotations,
        )

    def _copy(self) -> None:
        if self._state != OverlayState.EDITING:
            return
        self._state = OverlayState.COPYING
        try:
            image = self._render()
            self._toolbar.hide()
            self.hide()
            self._clipboard_keeper.copy_image_and_wait(image)
        except Exception as exc:
            self._state = OverlayState.EDITING
            self.show()
            self._toolbar.show()
            QMessageBox.warning(self, "Veilshot", f"Could not copy image:\n{exc}")

    def _save(self) -> None:
        if self._state != OverlayState.EDITING:
            return
        self._state = OverlayState.SAVING
        default_path = str(Path.home() / screenshot_filename())
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save screenshot",
            default_path,
            "PNG image (*.png)",
        )
        if not filename:
            self._state = OverlayState.EDITING
            self.activateWindow()
            self.setFocus(Qt.FocusReason.ActiveWindowFocusReason)
            return
        if not filename.lower().endswith(".png"):
            filename += ".png"
        try:
            if not self._render().save(filename, "PNG"):
                raise OSError("Qt could not write the PNG file")
        except Exception as exc:
            self._state = OverlayState.EDITING
            QMessageBox.warning(self, "Veilshot", f"Could not save image:\n{exc}")
            return
        self._state = OverlayState.CLOSING
        self.close()
        from PySide6.QtWidgets import QApplication

        QApplication.instance().quit()

    def _cancel(self) -> None:
        self._state = OverlayState.CLOSING
        self.close()
        from PySide6.QtWidgets import QApplication

        QApplication.instance().quit()

    def _sync_toolbar(self) -> None:
        self._toolbar.set_active_tool(self._model.active_tool)
        self._toolbar.set_color(self._model.tool_colors[self._model.active_tool])
        self._toolbar.set_history_enabled(self._undo.can_undo, self._undo.can_redo)
        self._position_toolbar()

    def _position_toolbar(self) -> None:
        if not hasattr(self, "_toolbar"):
            return
        self._toolbar.adjustSize()
        width = self._toolbar.width()
        height = self._toolbar.height()
        x = round((self.width() - width) / 2)
        y = self.height() - height - 22
        if not self._selection_rect.isEmpty():
            below = round(self._selection_rect.bottom() + 12)
            above = round(self._selection_rect.top() - height - 12)
            if below + height <= self.height() - 12:
                y = below
            elif above >= 12:
                y = above
        self._toolbar.move(max(8, x), max(8, y))
        self._toolbar.raise_()

    def _display_point_to_source(self, point: QPointF) -> QPointF:
        x = (point.x() - self._base_rect.left()) * self._source_image.width() / self._base_rect.width()
        y = (point.y() - self._base_rect.top()) * self._source_image.height() / self._base_rect.height()
        return QPointF(x, y)

    def _display_rect_to_source(self, rect: QRectF) -> QRectF:
        top_left = self._display_point_to_source(rect.topLeft())
        bottom_right = self._display_point_to_source(rect.bottomRight())
        return QRectF(top_left, bottom_right).normalized()

    @staticmethod
    def _clamp_to_rect(point: QPointF, rect: QRectF) -> QPointF:
        return QPointF(
            min(max(point.x(), rect.left()), rect.right()),
            min(max(point.y(), rect.top()), rect.bottom()),
        )

    @staticmethod
    def _annotation_is_meaningful(annotation: Annotation) -> bool:
        key = annotation.state_key()
        if isinstance(annotation, ArrowAnnotation):
            return abs(annotation.end.x() - annotation.start.x()) + abs(annotation.end.y() - annotation.start.y()) >= 5
        if isinstance(annotation, (HighlightAnnotation, RedactionAnnotation)):
            return annotation.normalized_rect().width() >= 4 and annotation.normalized_rect().height() >= 4
        return bool(key)
