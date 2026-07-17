# User guide

## Supported system

Current verified target: Pop!_OS 22.04 / GNOME on X11.

Check the session:

```bash
echo "$XDG_SESSION_TYPE"
```

Screenshot capture currently requires `x11`.

## Start capture

Use the configured global shortcut, select Veilshot from the application menu's capture action, or run:

```bash
~/.local/bin/veilshot
```

## Basic flow

1. Move the pointer to the monitor you want to capture.
2. Start Veilshot.
3. Drag to select a rectangular region.
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

- X11 only.
- One monitor per capture.
- No text, freehand drawing, OCR, blur, history, or cloud upload.
