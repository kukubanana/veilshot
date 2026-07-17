from pathlib import Path


def test_application_menu_starts_tray_and_offers_capture_action() -> None:
    template = Path("packaging/veilshot.desktop.in").read_text(encoding="utf-8")
    assert "Exec=@VEILSHOT_LAUNCHER@ --tray" in template
    assert "[Desktop Action Capture]" in template
    assert "Icon=veilshot" in template
