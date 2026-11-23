# Development guide

## Requirements

- Linux with Python 3.10 or newer.
- Fedora GNOME Wayland or a compatible X11 desktop.
- On Fedora Wayland: PyGObject, GStreamer PipeWire/video plugins, and
  `wl-clipboard` as listed in the README.

Pop!_OS 22.04 packages encountered on the original machine:

```bash
sudo apt install python3-venv
sudo apt install libxcb-cursor0
```

Only install system packages after reviewing why they are required.

## Setup

```bash
git clone REPOSITORY_URL
cd veilshot
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -e '.[dev]'
```

On Fedora, `./setup.sh` checks the host capture and clipboard dependencies
before preparing the virtual environment.

## Run

```bash
.venv/bin/python -m veilshot
.venv/bin/python -m veilshot --tray
.venv/bin/python -m veilshot --edit /path/to/image.png
```

## Test

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/pytest
```

Report the actual result. Test count changes as the suite grows.

## Local desktop integration

```bash
./install-local.sh
```

This is intended for development and personal use. It points `~/.local/bin/veilshot` to the project's `.venv`; moving or deleting the project breaks the launcher.

Remove local integration:

```bash
./uninstall-local.sh
```

## Working method

1. Create a branch.
2. Make one focused behavior change.
3. Add or update tests.
4. Run the automated suite.
5. Perform the relevant manual GUI check.
6. Update docs and changelog.
7. Commit with a focused message.

## Debugging tray integration

```bash
pgrep -af 'veilshot.*--tray'
cat "${XDG_RUNTIME_DIR:-/tmp}/veilshot-tray.log"
```

## Release-sensitive files

When changing version or installation behavior, review:

- `pyproject.toml`
- `src/veilshot/__init__.py`
- `README.md`
- `CHANGELOG.md`
- desktop templates
- app metadata and release notes
