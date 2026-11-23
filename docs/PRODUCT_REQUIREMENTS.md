# Product requirements document

## Product

**Name:** Veilshot
**Status:** Fedora Wayland source release
**Primary platform:** Fedora Workstation / GNOME / Wayland

## Problem

Existing Linux screenshot tools can expose too many tools, menus, customizations, and multi-window flows for users who mainly need to capture, point, conceal, and copy quickly.

## Product promise

Veilshot reduces the common screenshot workflow to a small, predictable interaction that normally takes 5–8 seconds.

## Primary user flow

```text
Global shortcut
→ frozen screen
→ select region
→ optionally arrow, highlight, or redact
→ Ctrl+C / Enter
→ paste into another application
```

## Functional requirements

### Capture

- On Wayland, let the user approve one monitor through the system Portal.
- On X11, capture the monitor under the pointer.
- Show a frozen full-screen representation.
- Allow one rectangular selection within that monitor.
- Do not write an automatic capture file.

### Annotation

- Arrow with fixed initial styling.
- Rectangular translucent highlight.
- Rectangular fully opaque redaction.
- Compact color set: white, black, red, yellow, eyedropper.
- Select, move, resize, delete.
- Undo and redo.

### Export

- Copy flattened output to clipboard through button, `Ctrl+C`, or `Enter`.
- Save through a system file dialog with `Ctrl+Shift+S`.
- Redaction pixels must not remain recoverable as editable layers.

### Desktop integration

- Application launcher.
- Tray process with Capture and Exit.
- Tray autostart after login.
- External GNOME custom shortcut.

## Non-functional requirements

- Local-only operation.
- No telemetry or network use.
- No screenshot-content logging.
- No automatic file creation.
- Fast startup and interaction.
- Minimal interface with no settings window.
- Correct coordinate handling on supported monitor configurations.

## Out of scope for the current product

- Cross-monitor selection.
- Capture history.
- Text and freehand tools.
- Blur and pixelation.
- OCR or sensitive-data detection.
- Cloud upload and share links.
- Accounts and synchronization.
- Plugin architecture.

## Success criteria for the Fedora release

- Installation succeeds from documented steps on Fedora Workstation.
- Core capture/copy flow works in browser and at least one messenger.
- Redaction export regression tests remain green.
- No private screenshots are included in repository or test assets.
- A user can install without editing source files.
- Known limitations are visible before download.
- The system permission dialog is shown for each Wayland capture.
