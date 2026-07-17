import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from veilshot.resources import app_icon_path, tray_icon_path


def test_svg_icons_render_at_target_sizes() -> None:
    app = QApplication.instance() or QApplication([])
    app_icon = QIcon(str(app_icon_path())).pixmap(64, 64)
    tray_icon = QIcon(str(tray_icon_path())).pixmap(22, 22)
    assert not app_icon.isNull()
    assert not tray_icon.isNull()
