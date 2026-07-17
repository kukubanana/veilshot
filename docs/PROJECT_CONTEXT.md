# Veilshot project context and handoff

This document preserves the useful product and development context from the initial ChatGPT-assisted build. It is the durable context for future work; the raw chat should be archived separately as described in `CHAT_ARCHIVE.md`.

## Origin

The project began as a first vibe-coded Linux desktop application for a user on Pop!_OS 22.04. The need came from dissatisfaction with existing screenshot tools:

- Flameshot felt overloaded and inconvenient for custom shortcuts.
- Ksnip appeared too close to a general image editor.
- iPhone screenshot markup was fast but lacked an obvious, safe redaction flow and simple arrows.
- Lightshot on macOS was remembered as fast and intuitive, but no suitable Linux version was available.

The product opportunity was defined as a deliberately constrained tool rather than a feature-complete competitor.

## Core user job

> Press a global shortcut, select an area, optionally point to or conceal something, and copy the result within 5–8 seconds.

## Product definition

Veilshot is a lightweight, privacy-first screenshot capture and annotation tool with three tools:

1. Arrow.
2. Rectangular translucent highlight.
3. Rectangular opaque redaction.

Copy is the default result. Saving is explicit.

## Target environment used during the first build

- ThinkPad T14 Gen 4 AMD.
- 32 GB RAM.
- Pop!_OS 22.04 LTS.
- `pop:GNOME` desktop.
- X11 session.
- Python 3.10.12.
- Built-in and external monitors may be used.

System dependencies encountered during installation:

```bash
sudo apt install python3-venv
sudo apt install libxcb-cursor0
```

These commands were required because Pop!_OS lacked Python venv support and Qt's XCB cursor library on the test machine. They are not run automatically by Veilshot.

## Current verified behavior

- Capture and overlay work on the target X11 machine.
- Arrow, highlight, and redaction render and export.
- Clipboard copying works in real use.
- The Pop!_OS application launcher displays the current icon.
- The tray icon appears and tray mode runs in the background.
- A GNOME custom global shortcut launches capture.
- The application starts after local installation.

## Installation evolution and lessons

The first installer only created a launcher and desktop entry. An attempted tray update was not actually applied, which was diagnosed because the old installer output and old test count remained. Version 0.2.1 replaced that update with a full package containing tray code, app/tray assets, autostart integration, and installation diagnostics.

Important process lesson:

- Never tell a user to expect a fixed test count without checking the exact source currently installed.
- Version, test output, installer output, and required files should be used together to confirm that an update was actually applied.

## Visual direction

Temporary app and tray icons were generated for the MVP. The tray icon is a separate simplified drawing optimized for 22×22 rather than a reduction of the launcher icon. The chosen direction uses screenshot-selection corners, a diagonal arrow, and a purple top-right bracket.

The maintainer plans to redraw permanent application, tray, toolbar, cursor, and typography assets. Technical specifications are in `DESIGN-ASSETS.md`.

## Legal status

The source is currently marked MIT. Trademark and final name/logo ownership checks were discussed but postponed. Before a public launch, confirm:

- Copyright notice and maintainer identity.
- Whether brand assets are included under MIT or reserved separately.
- Trademark clearance for `Veilshot`.
- Font and icon redistribution rights.

## Current product maturity

Status: early alpha / personal working MVP.

It is usable by the maintainer but not yet ready for a store submission because broader environment testing, packaging, support documentation, and a reproducible release process still need to be completed.

## Next recommended milestone

Create a public GitHub repository and a source release for technically confident early testers. Collect issues before investing in Flathub packaging and broader compatibility.
