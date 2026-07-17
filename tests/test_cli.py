from veilshot.cli import build_parser


def test_cli_accepts_edit_path() -> None:
    args = build_parser().parse_args(["--edit", "example.png"])
    assert str(args.edit) == "example.png"


def test_cli_accepts_tray_mode() -> None:
    args = build_parser().parse_args(["--tray"])
    assert args.tray is True
