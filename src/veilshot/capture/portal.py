from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication, QImage, QPixmap

from veilshot.capture.base import CaptureResult


class PortalCaptureBackend:
    """One-shot Fedora/GNOME Wayland capture through Portal and PipeWire."""

    CAPTURE_TIMEOUT_SECONDS = 180

    @staticmethod
    def _host_python() -> str:
        base_executable = getattr(sys, "_base_executable", None)
        return str(base_executable or sys.executable)

    @staticmethod
    def _helper_path() -> Path:
        return Path(__file__).with_name("_portal_helper.py")

    @classmethod
    def capture_screen_under_cursor(cls) -> CaptureResult:
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            raise RuntimeError("Veilshot could not find an active display")

        try:
            completed = subprocess.run(
                [cls._host_python(), str(cls._helper_path())],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=cls.CAPTURE_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("Screen capture permission timed out") from exc

        if completed.returncode != 0:
            details = completed.stderr.decode(errors="replace").strip()
            raise RuntimeError(details or "Screen capture was not completed")

        image = QImage.fromData(completed.stdout, "PNG")
        if image.isNull():
            raise RuntimeError("ScreenCast Portal returned an invalid image")
        return CaptureResult(pixmap=QPixmap.fromImage(image), screen=screen)
