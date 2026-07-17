from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from PySide6.QtCore import QLockFile, QObject, QProcess, QStandardPaths, QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from veilshot.resources import app_icon_path, tray_icon_path


def capture_command() -> tuple[str, list[str]]:
    """Return the interpreter and arguments used by the tray to start capture."""
    return sys.executable, ["-m", "veilshot"]


def _runtime_lock_path() -> Path:
    runtime_dir = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.RuntimeLocation
    )
    base = Path(runtime_dir) if runtime_dir else Path(tempfile.gettempdir())
    return base / f"veilshot-tray-{os.getuid()}.lock"


class TrayController(QObject):
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self._app = app
        self._capture_enabled = True

        self._lock = QLockFile(str(_runtime_lock_path()))
        self._lock.setStaleLockTime(5000)
        if not self._lock.tryLock(50):
            raise RuntimeError("Veilshot tray is already running")

        icon_path = tray_icon_path()
        if not icon_path.is_file():
            raise RuntimeError(f"Tray icon not found: {icon_path}")

        self.tray = QSystemTrayIcon(QIcon(str(icon_path)), self)
        self.tray.setToolTip("Veilshot")

        menu = QMenu()
        self.capture_action = QAction("Сделать скриншот", menu)
        self.capture_action.triggered.connect(self.capture)
        menu.addAction(self.capture_action)
        menu.addSeparator()
        quit_action = QAction("Выход", menu)
        quit_action.triggered.connect(self._app.quit)
        menu.addAction(quit_action)
        self.tray.setContextMenu(menu)
        self._menu = menu

        self.tray.activated.connect(self._activated)
        self.tray.show()

    def _activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.capture()

    def capture(self) -> None:
        if not self._capture_enabled:
            return
        executable, arguments = capture_command()
        started = QProcess.startDetached(executable, arguments)
        if isinstance(started, tuple):
            ok = bool(started[0])
        else:
            ok = bool(started)
        if not ok:
            self.tray.showMessage(
                "Veilshot",
                "Не удалось запустить захват экрана.",
                QSystemTrayIcon.MessageIcon.Warning,
                3000,
            )
            return

        # Avoid accidental double launches from a double click.
        self._capture_enabled = False
        self.capture_action.setEnabled(False)
        QTimer.singleShot(700, self._reenable_capture)

    def _reenable_capture(self) -> None:
        self._capture_enabled = True
        self.capture_action.setEnabled(True)


def run_tray() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Veilshot")
    app.setOrganizationName("Veilshot")
    app.setWindowIcon(QIcon(str(app_icon_path())))
    app.setQuitOnLastWindowClosed(False)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print(
            "Veilshot: system tray is unavailable. "
            "On GNOME/Pop!_OS, enable AppIndicator support.",
            file=sys.stderr,
        )
        return 4

    try:
        controller = TrayController(app)
    except RuntimeError as exc:
        # A duplicate autostart should exit quietly; other errors remain visible in logs.
        if "already running" not in str(exc):
            print(f"Veilshot: {exc}", file=sys.stderr)
            return 5
        return 0

    app._veilshot_tray_controller = controller  # type: ignore[attr-defined]
    return app.exec()
