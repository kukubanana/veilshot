# Architecture

## Overview

Veilshot is a Python 3 desktop application using PySide6 / Qt Widgets. The design separates capture, annotation models, UI, export, clipboard lifecycle, resources, and tray integration.

## Runtime modes

```text
veilshot                 Capture and edit
veilshot --edit IMAGE    Edit an existing image
veilshot --tray          Run the tray launcher
veilshot --version       Print version
```

## Main capture path

```text
CLI
→ application.run()
→ capture_backend_for_session()
→ PortalCaptureBackend (Wayland) or X11CaptureBackend
→ OverlayWindow
→ annotation model and commands
→ exporter
→ ClipboardKeeper or QFileDialog
```

## Tray path

```text
CLI --tray
→ TrayController
→ QSystemTrayIcon
→ QProcess.startDetached(python -m veilshot)
```

A `QLockFile` prevents duplicate tray processes. The tray is a launcher; capture runs in a separate process so the tray remains available.

## Major modules

### `capture/`

- `base.py`: capture abstraction.
- `portal.py`: invokes the host helper and converts its in-memory PNG into a Qt
  pixmap.
- `_portal_helper.py`: ScreenCast Portal requests, restricted PipeWire remote,
  and one-frame GStreamer pipeline. It writes PNG bytes to stdout and never
  creates a screenshot file.
- `x11.py`: Qt/X11 implementation that captures the screen under the pointer.

### `editor/`

- `overlay.py`: full-screen workflow and state coordination.
- `canvas.py`: painting and pointer interaction.
- `model.py`: annotation state.
- `commands.py`: undo/redo command model.
- `annotations/`: arrow, highlight, redaction, and shared geometry.

### `services/`

- `exporter.py`: flattened image generation.
- `clipboard.py`: Wayland `wl-copy` publication and X11 clipboard lifetime
  management.
- `filename.py`: default screenshot filenames.

### `ui/`

- `toolbar.py`: compact action toolbar.
- `icons.py`: current programmatic/editor icons.

### Desktop integration

- `tray.py`: tray process and capture launcher.
- `resources.py`: packaged icon paths.
- `packaging/*.desktop.in`: application and autostart templates.
- `install-local.sh`: per-user installation.

## Privacy properties

- Captured images are held in memory.
- Clipboard data is not deliberately persisted to disk.
- Redactions are painted into the flattened exported image.
- Network libraries and upload code are absent from the product scope.

## X11 clipboard lifecycle

On X11, clipboard ownership normally belongs to the source process. After copy, Veilshot hides the UI and keeps the process alive until ownership changes, with a fallback timeout. This is why copy cannot always be followed by immediate process termination.

## Wayland capture and clipboard lifecycle

Every capture creates a new ScreenCast Portal session, so GNOME presents its
monitor permission dialog each time. The portal returns a restricted PipeWire
remote containing only the approved stream. A host-Python helper consumes one
frame and transfers its PNG bytes to the Qt process over stdout.

After editing, `wl-copy` owns the flattened `image/png` clipboard payload, so
the Veilshot GUI can exit without losing the copied image. If `wl-copy` is not
available, Qt clipboard ownership remains as a timed fallback.

## Packaging boundary

The current installer is a per-user development/MVP installer tied to the project's `.venv`. A public distribution package must not assume the source directory and venv remain at a particular path. Flatpak or another self-contained package should own its runtime and desktop files.
