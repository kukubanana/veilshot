# User guide

## Supported system

Current verified target: Fedora Workstation 45 / GNOME on Wayland.

The previous Pop!_OS 22.04 / GNOME / X11 path remains available.

Check the session:

```bash
echo "$XDG_SESSION_TYPE"
```

Both `wayland` and `x11` are supported. Fedora Wayland requires the system
packages listed in the README.

## Start capture

Use the configured global shortcut, select Veilshot from the application menu's capture action, or run:

```bash
~/.local/bin/veilshot
```

## Basic flow

1. Start Veilshot.
2. On Wayland, select one monitor in Fedora's permission dialog.
3. Drag to select a rectangular region on the frozen image.
4. Use an annotation tool or copy immediately.
5. Press `Ctrl+C` or `Enter`.
6. Paste into another application.

## Keyboard controls

| Key | Action |
|---|---|
| `A` | Arrow |
| `H` | Highlight |
| `R` | Opaque redaction |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Delete` | Delete selected annotation |
| `Ctrl+C` or `Enter` | Copy and hide |
| `Ctrl+Shift+S` | Save as PNG |
| `Esc` | Cancel |

## Tray

- Left click: capture.
- Right click: menu with capture and exit.
- The tray starts automatically after login when installed with `install-local.sh`.

## Redaction warning

Use the opaque redaction tool for sensitive information. Highlighting is translucent and is not a privacy tool.

## Known limitations

- Fedora shows the monitor permission dialog for every Wayland capture.
- One selected monitor per capture.
- No text, freehand drawing, OCR, blur, history, or cloud upload.
