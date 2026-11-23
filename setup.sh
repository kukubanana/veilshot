#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed or is not available in PATH." >&2
  exit 1
fi

if [[ "${XDG_SESSION_TYPE:-}" == "wayland" ]]; then
  missing=()
  if ! python3 -c 'import gi' >/dev/null 2>&1; then
    missing+=(python3-gobject)
  fi
  if ! command -v gst-launch-1.0 >/dev/null 2>&1; then
    missing+=(gstreamer1)
  fi
  if ! gst-inspect-1.0 pipewiresrc >/dev/null 2>&1; then
    missing+=(pipewire-gstreamer)
  fi
  if ! gst-inspect-1.0 videoconvert >/dev/null 2>&1; then
    missing+=(gstreamer1-plugins-base)
  fi
  if ! gst-inspect-1.0 pngenc >/dev/null 2>&1; then
    missing+=(gstreamer1-plugins-good)
  fi
  if ! command -v wl-copy >/dev/null 2>&1; then
    missing+=(wl-clipboard)
  fi
  if (( ${#missing[@]} > 0 )); then
    printf 'Missing Fedora Wayland dependencies: %s\n' "${missing[*]}" >&2
    printf 'Install them with: sudo dnf install %s\n' "${missing[*]}" >&2
    exit 1
  fi
fi

if ! python3 -m venv .venv; then
  cat >&2 <<'MESSAGE'

Veilshot could not create a virtual environment.
On Pop!_OS 22.04 this usually means the python3-venv package is missing.
It provides Python's isolated-environment support; Veilshot will not install
packages globally. Install it manually, then rerun this script:

  sudo apt install python3-venv
MESSAGE
  exit 1
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -e '.[dev]'
QT_QPA_PLATFORM=offscreen .venv/bin/pytest

cat <<'MESSAGE'

Veilshot 0.3 is ready for a manual test.
Run:

  ./run-dev.sh

On Fedora GNOME Wayland, approve the monitor in the system dialog, select a
region, and press Enter to copy. To test only the editor, run:

  ./run-dev.sh --edit /path/to/any/image.png

After the manual test succeeds, install the launcher, icons, and tray with:

  ./install-local.sh
MESSAGE
