# Veilshot 0.2

Veilshot is a deliberately small, privacy-first screenshot tool for Linux X11.
It captures the monitor under the pointer, lets you select a region, and offers
only three annotation tools: arrow, translucent highlight, and opaque redaction.
The result is copied to the clipboard by default; no file is created unless you
explicitly save it.

## Current scope

- Pop!_OS 22.04 / GNOME on X11
- Capture the monitor under the pointer
- Select a region in a frozen-screen overlay
- Arrow, rectangular highlight, opaque redaction
- Compact colors: white, black, red, yellow, eyedropper
- Move, resize, delete, undo, redo
- Copy flattened PNG to the X11 clipboard
- Save through the system file dialog
- Pop!_OS application launcher with a temporary app icon
- Background tray process with a separate 22 px-aware tray icon
- Tray menu: capture and exit
- Automatic tray start after login
- No network, telemetry, history, settings screen, or temporary screenshots

Wayland capture is intentionally not implemented yet.

## Install for development

```bash
cd veilshot
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -e '.[dev]'
```

No Python package is installed globally.

## Run

Capture a screenshot:

```bash
.venv/bin/python -m veilshot
```

Run the tray process:

```bash
.venv/bin/python -m veilshot --tray
```

Open an existing image while developing:

```bash
.venv/bin/python -m veilshot --edit /path/to/image.png
```

Check the version:

```bash
.venv/bin/python -m veilshot --version
```

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

## Install in Pop!_OS

After the virtual environment exists:

```bash
./install-local.sh
```

This creates:

- `~/.local/bin/veilshot`
- `~/.local/share/applications/veilshot.desktop`
- `~/.config/autostart/veilshot-tray.desktop`
- `~/.local/share/icons/hicolor/scalable/apps/veilshot.svg`

It also starts the tray process immediately. On the next login, the tray starts
automatically. The tray has only two actions: **Сделать скриншот** and **Выход**.

In Pop!_OS, search the application grid for **Veilshot**. Right-click it and use
**Add to Favorites** to pin it to the dock.

For a global shortcut, open **Settings → Keyboard → Customize Shortcuts → Custom
Shortcuts**, create a shortcut named `Veilshot`, and use:

```text
/home/YOUR_USERNAME/.local/bin/veilshot
```

A suggested key combination is `Super+Shift+S`.

## Tests

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/pytest
```

## Design assets

Temporary launcher and tray icons are included. Exact technical requirements for
replacing them, plus toolbar icon and font specifications, are documented in
[`DESIGN-ASSETS.md`](DESIGN-ASSETS.md).

## Important X11 clipboard behavior

On X11, clipboard data is normally owned by the process that copied it.
Veilshot hides immediately, keeps the clipboard image alive invisibly, and exits
when another process or clipboard manager takes ownership, with a 120-second
fallback timeout.

## Known limitations

- X11 capture only
- One monitor per capture: the monitor under the pointer
- No cross-monitor selection
- Tray visibility depends on AppIndicator/system-tray support in the desktop
- No text, freehand drawing, blur, pixelation, OCR, or history
- Mixed-DPI monitor setups need real-device testing

## Privacy

Veilshot does not use the network, does not upload images, does not create
capture files automatically, and does not log screenshot contents. Opaque
redactions replace the underlying pixels in the flattened exported PNG.

## License

MIT

## Troubleshooting on Pop!_OS 22.04

If virtual-environment creation reports that `ensurepip` is unavailable:

```bash
sudo apt install python3-venv
```

If Qt reports that the `xcb` platform plugin cannot be loaded and specifically
mentions `xcb-cursor`:

```bash
sudo apt install libxcb-cursor0
```

If the application launcher works but no tray icon appears, verify that Pop!_OS
has its AppIndicator support enabled. Existing tray icons such as Telegram are a
good practical indication that support is already active. The tray log is:

```text
${XDG_RUNTIME_DIR:-/tmp}/veilshot-tray.log
```
