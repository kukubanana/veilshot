# Changelog

All notable changes to Veilshot are documented here. The project follows Semantic Versioning once public releases begin.

## [Unreleased]

### Planned

- Documentation and public repository preparation.
- Packaging evaluation for Flathub.
- Broader real-device testing on X11 distributions.

## [0.2.1] — 2026-07-17

### Added

- Background tray mode.
- Separate tray icon optimized for small display sizes.
- Application launcher icon in Pop!_OS.
- Login autostart entry for tray mode.
- Application menu action for capture.
- PNG fallbacks for launcher icons.
- Tray diagnostics and duplicate-process protection.

### Verified manually

- Pop!_OS application menu entry and current icon.
- Tray icon visibility.
- Global shortcut capture.
- Capture, annotation, copy, and save flow on Pop!_OS 22.04 X11.

## [0.1.0] — 2026-07-17

### Added

- X11 capture of the monitor under the pointer.
- Region-selection overlay.
- Arrow, highlight, and opaque redaction tools.
- Object selection, move, resize, delete, undo, and redo.
- Clipboard-first flattened PNG export.
- Save As dialog.
- Initial Pop!_OS local launcher integration.
