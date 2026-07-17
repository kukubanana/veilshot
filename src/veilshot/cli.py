from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="veilshot",
        description="Minimal screenshot annotation for Linux X11.",
    )
    parser.add_argument(
        "--edit",
        metavar="IMAGE",
        type=Path,
        help="Open an existing image directly in the editor.",
    )
    parser.add_argument(
        "--tray",
        action="store_true",
        help="Run Veilshot in the system tray.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the Veilshot version and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.version:
        from veilshot import __version__

        print(__version__)
        return 0

    if args.tray and args.edit is not None:
        print("Veilshot: --tray and --edit cannot be used together", file=sys.stderr)
        return 2

    if args.edit is not None and not args.edit.is_file():
        print(f"Veilshot: image not found: {args.edit}", file=sys.stderr)
        return 2

    if args.tray:
        from veilshot.tray import run_tray

        return run_tray()

    if args.edit is None and os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland":
        print(
            "Veilshot 0.2 supports screenshot capture on X11 only. "
            "Use --edit on Wayland, or log into an X11 session.",
            file=sys.stderr,
        )
        return 3

    from veilshot.application import run

    return run(edit_path=args.edit)
