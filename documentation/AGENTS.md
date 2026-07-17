# AGENTS.md — Veilshot development context

Read this file before changing code.

## Product in one sentence

Veilshot is a deliberately small, privacy-first screenshot annotation tool for Linux. The core flow is: **global shortcut → select region → optionally annotate or redact → copy**.

## Current verified state

- Version: `0.2.1`
- Primary target: Pop!_OS 22.04, GNOME, X11
- Python: 3.10+
- GUI: PySide6 / Qt Widgets
- The application launcher, tray icon, autostart, and GNOME custom shortcut have been manually verified on the maintainer's Pop!_OS machine.
- The current automated suite contains 14 tests in the documented 0.2.1 source package. Always report the number actually produced by the local run; never hard-code an expected count in user-facing instructions.

## Product principles

1. Typical operation should take 5–8 seconds.
2. Clipboard-first: do not create a file unless the user explicitly saves.
3. Minimal tools only: arrow, rectangular highlight, opaque redaction.
4. No cloud, account, telemetry, history, OCR, or automatic upload.
5. Opaque redaction must replace pixels in the flattened export.
6. Do not turn the interface into a general image editor.
7. Global shortcuts are configured by the desktop environment, not by a custom keyboard hook.
8. The tray is a lightweight launcher, not a settings center.

## Current scope

Implemented:

- Capture the monitor under the pointer on X11.
- Freeze the screen in a full-screen overlay.
- Select one region within one monitor.
- Arrow, translucent highlight, opaque redaction.
- White, black, red, yellow, and eyedropper color choices.
- Move, resize, select, delete, undo, redo.
- Copy a flattened image to the X11 clipboard.
- Save PNG with a system file dialog.
- Tray mode with Capture and Exit.
- Pop!_OS application launcher, icon, and login autostart.
- `--edit`, `--tray`, and `--version` CLI modes.

Intentionally not implemented:

- Wayland capture.
- Cross-monitor selection.
- Text, freehand drawing, blur, pixelation, OCR, history.
- Settings window, accounts, network features, plugins.

## Commands

```bash
# Development install
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'

# Tests
QT_QPA_PLATFORM=offscreen .venv/bin/pytest

# Capture
.venv/bin/python -m veilshot

# Tray
.venv/bin/python -m veilshot --tray

# Edit an existing image
.venv/bin/python -m veilshot --edit /path/to/image.png

# Local desktop integration
./install-local.sh
```

## Safety rules for coding agents

- Do not run `sudo` or modify system settings.
- Do not publish to GitHub, PyPI, Flathub, or any network service without explicit approval.
- Do not install Python packages globally.
- Do not log screenshot pixels, file contents, or clipboard data.
- Do not create temporary screenshots unless a technical requirement is documented first.
- Keep capture, annotations, export, clipboard, tray, and UI responsibilities separated.
- Add or update tests for non-trivial behavior.
- For GUI behavior that cannot be automated, provide a short manual test.
- Do not claim a GUI path works merely because imports or offscreen tests pass.

## Documentation map

- `README.md` — public project landing page.
- `docs/PROJECT_CONTEXT.md` — durable project handoff and history.
- `docs/PRODUCT_REQUIREMENTS.md` — product requirements.
- `docs/ARCHITECTURE.md` — code and runtime architecture.
- `docs/USER_GUIDE.md` — end-user instructions.
- `docs/DEVELOPMENT.md` — developer setup and workflow.
- `docs/TESTING.md` — automated and manual test strategy.
- `docs/DECISION_LOG.md` — important product and technical decisions.
- `docs/ROADMAP.md` — planned work without scope creep.
- `docs/RELEASE_PROCESS.md` — versioning and release checklist.
- `docs/DISTRIBUTION.md` — GitHub and store distribution plan.
- `DESIGN-ASSETS.md` — visual asset specifications.
