#!/usr/bin/env bash
set -euo pipefail

VENV_PYTHON="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.venv/bin/python"
pkill -f "$VENV_PYTHON -m veilshot --tray" 2>/dev/null || true
rm -f "$HOME/.local/bin/veilshot"
rm -f "$HOME/.local/share/applications/veilshot.desktop"
rm -f "$HOME/.config/autostart/veilshot-tray.desktop"
rm -f "$HOME/.local/share/icons/hicolor/scalable/apps/veilshot.svg"
rm -rf "$HOME/.local/share/veilshot"
echo "Removed Veilshot's local launcher, desktop entry, tray autostart, and icons."
