# Changelog

All notable changes to Veilshot are documented here. The project follows Semantic Versioning once public releases begin.

## [Unreleased]

### Planned

- Packaging evaluation for Flathub.
- Mixed-DPI and multi-monitor testing.

## [0.3.0] — 2026-11-23

### Added

- Fedora Workstation GNOME Wayland capture through ScreenCast Portal and
  PipeWire.
- Runtime selection between the Wayland portal backend and the existing X11
  backend.
- In-memory transfer from PipeWire to the existing Qt editor without a
  temporary screenshot file.
- Persistent Wayland image clipboard publishing through `wl-copy`.
- Fedora dependency checks and installation instructions.
- Automated coverage for backend selection, portal image decoding, failure
  reporting, and the Wayland clipboard path.

### Changed

- Veilshot intentionally asks for monitor permission on every Wayland capture.
- Product documentation now treats Fedora Workstation GNOME Wayland as the
  primary target.

### Verified manually

- Fedora Workstation 45, GNOME, Wayland.
- Portal monitor selection and one-frame PipeWire capture.
- Frozen-screen region selection and editor launch.
- Copy with Enter, application exit, and `image/png` availability in the
  Wayland clipboard after exit.
- Repeated capture with a fresh system permission dialog.

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
