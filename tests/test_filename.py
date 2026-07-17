from datetime import datetime

from veilshot.services.filename import screenshot_filename


def test_screenshot_filename_is_stable() -> None:
    value = screenshot_filename(datetime(2026, 7, 17, 10, 35, 42))
    assert value == "Screenshot_2026-07-17_10-35-42.png"
