from __future__ import annotations

import os
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QColor, QImage
from PySide6.QtWidgets import QApplication

from veilshot.services.clipboard import ClipboardKeeper


def test_wayland_clipboard_uses_wl_copy_with_png(monkeypatch) -> None:
    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    image = QImage(20, 10, QImage.Format.Format_ARGB32)
    image.fill(QColor("red"))
    observed: dict[str, object] = {}

    def fake_run(command, **kwargs):
        observed["command"] = command
        observed["input"] = kwargs["input"]
        return SimpleNamespace(returncode=0)

    monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
    monkeypatch.setattr(
        "veilshot.services.clipboard.shutil.which", lambda _name: "/usr/bin/wl-copy"
    )
    monkeypatch.setattr("veilshot.services.clipboard.subprocess.run", fake_run)

    keeper = ClipboardKeeper(app, timeout_ms=100)
    keeper.copy_image_and_wait(image)

    assert observed["command"] == ["/usr/bin/wl-copy", "--type", "image/png"]
    assert bytes(observed["input"]).startswith(b"\x89PNG\r\n\x1a\n")


def test_wayland_clipboard_falls_back_when_wl_copy_is_missing(monkeypatch) -> None:
    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    image = QImage(20, 10, QImage.Format.Format_ARGB32)
    image.fill(QColor("blue"))
    monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
    monkeypatch.setattr(
        "veilshot.services.clipboard.shutil.which", lambda _name: None
    )
    keeper = ClipboardKeeper(app, timeout_ms=100)

    assert keeper._copy_with_wayland_helper(image) is False
