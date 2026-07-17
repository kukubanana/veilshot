#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed or is not available in PATH." >&2
  exit 1
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

Veilshot 0.2 is ready for a manual test.
Run:

  ./run-dev.sh --edit /path/to/any/image.png

or capture the current X11 screen:

  ./run-dev.sh

After the manual test succeeds, install the launcher, icons, and tray with:

  ./install-local.sh
MESSAGE
