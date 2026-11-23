from __future__ import annotations

import os
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QColor, QImage
from PySide6.QtWidgets import QApplication

from veilshot.capture import capture_backend_for_session
from veilshot.capture.portal import PortalCaptureBackend
from veilshot.capture.x11 import X11CaptureBackend


def _png_bytes() -> bytes:
    image = QImage(32, 24, QImage.Format.Format_ARGB32)
    image.fill(QColor("steelblue"))
    data = QByteArray()
    buffer = QBuffer(data)
    assert buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    assert image.save(buffer, "PNG")
    return bytes(data)


def test_backend_selection_uses_portal_on_wayland() -> None:
    assert capture_backend_for_session("wayland") is PortalCaptureBackend
    assert capture_backend_for_session("WAYLAND") is PortalCaptureBackend


def test_backend_selection_keeps_x11_backend() -> None:
    assert capture_backend_for_session("x11") is X11CaptureBackend
    assert capture_backend_for_session("") is X11CaptureBackend


def test_portal_backend_decodes_helper_png(monkeypatch) -> None:
    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    monkeypatch.setattr(
        "veilshot.capture.portal.subprocess.run",
        lambda *_args, **_kwargs: SimpleNamespace(
            returncode=0,
            stdout=_png_bytes(),
            stderr=b"",
        ),
    )

    capture = PortalCaptureBackend.capture_screen_under_cursor()

    assert capture.pixmap.size().width() == 32
    assert capture.pixmap.size().height() == 24
    assert capture.screen is app.primaryScreen()


def test_portal_backend_surfaces_helper_error(monkeypatch) -> None:
    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    monkeypatch.setattr(
        "veilshot.capture.portal.subprocess.run",
        lambda *_args, **_kwargs: SimpleNamespace(
            returncode=1,
            stdout=b"",
            stderr=b"Screen capture was cancelled\n",
        ),
    )

    try:
        PortalCaptureBackend.capture_screen_under_cursor()
    except RuntimeError as exc:
        assert str(exc) == "Screen capture was cancelled"
    else:
        raise AssertionError("Portal backend should reject a failed helper")
