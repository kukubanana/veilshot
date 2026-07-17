from __future__ import annotations

from pathlib import Path


_ASSET_DIR = Path(__file__).resolve().parent / "assets"


def app_icon_path() -> Path:
    return _ASSET_DIR / "veilshot.svg"


def tray_icon_path() -> Path:
    png = _ASSET_DIR / "veilshot-tray-22.png"
    return png if png.is_file() else _ASSET_DIR / "veilshot-tray.svg"
