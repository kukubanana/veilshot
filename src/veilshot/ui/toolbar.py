from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMenu,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from veilshot.editor.model import Tool
from veilshot.ui.icons import (
    arrow_icon,
    close_icon,
    copy_icon,
    eyedropper_icon,
    highlight_icon,
    redact_icon,
    save_icon,
    undo_icon,
)


class EditorToolbar(QFrame):
    tool_selected = Signal(object)
    color_selected = Signal(QColor)
    eyedropper_requested = Signal()
    undo_requested = Signal()
    redo_requested = Signal()
    copy_requested = Signal()
    save_requested = Signal()
    close_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("editorToolbar")
        self.setWindowFlags(Qt.WindowType.Widget)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet(
            """
            QFrame#editorToolbar {
                background: rgba(17, 24, 39, 235);
                border: 1px solid rgba(255, 255, 255, 35);
                border-radius: 12px;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 5px;
                background: transparent;
            }
            QPushButton:hover { background: rgba(255, 255, 255, 28); }
            QPushButton:checked { background: rgba(96, 165, 250, 100); }
            QPushButton:disabled { opacity: 0.35; }
            """
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(4)

        self._tool_buttons: dict[Tool, QPushButton] = {}
        self._add_tool(layout, Tool.ARROW, arrow_icon(), "Arrow (A)")
        self._add_tool(layout, Tool.HIGHLIGHT, highlight_icon(), "Highlight (H)")
        self._add_tool(layout, Tool.REDACTION, redact_icon(), "Redact (R)")

        self.color_button = self._button(QIcon(), "Color")
        self.color_button.clicked.connect(self._open_color_menu)
        layout.addWidget(self.color_button)

        layout.addWidget(self._separator())
        self.undo_button = self._button(undo_icon(), "Undo (Ctrl+Z)")
        self.redo_button = self._button(undo_icon(reverse=True), "Redo (Ctrl+Shift+Z)")
        self.undo_button.clicked.connect(self.undo_requested)
        self.redo_button.clicked.connect(self.redo_requested)
        layout.addWidget(self.undo_button)
        layout.addWidget(self.redo_button)

        layout.addWidget(self._separator())
        copy_button = self._button(copy_icon(), "Copy (Ctrl+C or Enter)")
        save_button = self._button(save_icon(), "Save as… (Ctrl+Shift+S)")
        close_button = self._button(close_icon(), "Cancel (Esc)")
        copy_button.clicked.connect(self.copy_requested)
        save_button.clicked.connect(self.save_requested)
        close_button.clicked.connect(self.close_requested)
        layout.addWidget(copy_button)
        layout.addWidget(save_button)
        layout.addWidget(close_button)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.set_active_tool(Tool.REDACTION)
        self.set_color(QColor("#ffffff"))
        self.set_history_enabled(False, False)

    def _button(self, icon: QIcon, tooltip: str) -> QPushButton:
        button = QPushButton(self)
        button.setIcon(icon)
        button.setIconSize(QSize(22, 22))
        button.setFixedSize(38, 38)
        button.setToolTip(tooltip)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        return button

    def _add_tool(self, layout: QHBoxLayout, tool: Tool, icon: QIcon, tooltip: str) -> None:
        button = self._button(icon, tooltip)
        button.setCheckable(True)
        button.clicked.connect(lambda checked=False, value=tool: self.tool_selected.emit(value))
        self._tool_buttons[tool] = button
        layout.addWidget(button)

    def _separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("color: rgba(255,255,255,40); margin: 6px 3px;")
        return separator

    def set_active_tool(self, tool: Tool) -> None:
        for candidate, button in self._tool_buttons.items():
            button.setChecked(candidate == tool)

    def set_history_enabled(self, can_undo: bool, can_redo: bool) -> None:
        self.undo_button.setEnabled(can_undo)
        self.redo_button.setEnabled(can_redo)

    def set_color(self, color: QColor) -> None:
        pixmap = QPixmap(22, 22)
        pixmap.fill(Qt.GlobalColor.transparent)
        from PySide6.QtGui import QPainter, QPen

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#e5e7eb"), 1))
        painter.setBrush(QColor(color))
        painter.drawEllipse(3, 3, 16, 16)
        painter.end()
        self.color_button.setIcon(QIcon(pixmap))

    def _open_color_menu(self) -> None:
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background:#111827; color:#f8fafc; padding:5px; }")
        for name, value in (
            ("White", "#ffffff"),
            ("Black", "#000000"),
            ("Red", "#ef4444"),
            ("Yellow", "#facc15"),
        ):
            action = menu.addAction(name)
            color = QColor(value)
            swatch = QPixmap(16, 16)
            swatch.fill(color)
            action.setIcon(QIcon(swatch))
            action.triggered.connect(lambda checked=False, c=color: self.color_selected.emit(c))
        menu.addSeparator()
        eyedropper = menu.addAction(eyedropper_icon(), "Pick from screenshot")
        eyedropper.triggered.connect(self.eyedropper_requested)
        menu.exec(self.color_button.mapToGlobal(self.color_button.rect().bottomLeft()))
