import pytest

pytest.importorskip("PySide6")

import sys

from veilshot.tray import capture_command


def test_tray_uses_current_python_environment() -> None:
    executable, arguments = capture_command()
    assert executable == sys.executable
    assert arguments == ["-m", "veilshot"]
