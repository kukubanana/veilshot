from veilshot.resources import app_icon_path, tray_icon_path


def test_icon_assets_exist() -> None:
    assert app_icon_path().is_file()
    assert tray_icon_path().is_file()
    assert app_icon_path().suffix == ".svg"
    assert tray_icon_path().suffix in {".png", ".svg"}
