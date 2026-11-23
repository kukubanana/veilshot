# Veilshot 0.3

Veilshot is a deliberately small, privacy-first screenshot tool for Linux. Its
main flow is: start capture, select a region, optionally annotate or redact, and
copy the result. No screenshot file is created unless Save is explicitly used.

## Current scope

- Fedora Workstation / GNOME / Wayland as the primary target.
- Pop!_OS 22.04 / GNOME / X11 compatibility retained.
- System monitor permission dialog on every Wayland capture.
- Frozen-screen rectangular region selection.
- Arrow, translucent highlight, and opaque redaction.
- White, black, red, yellow, and eyedropper colors.
- Move, resize, delete, undo, and redo.
- Clipboard-first flattened PNG output.
- Standard Save As dialog for explicit PNG files.
- Optional lightweight tray launcher and GNOME custom shortcut.
- No network, telemetry, history, accounts, or automatic screenshot files.

## Install on Fedora Workstation

Install the host components used for Portal, PipeWire, and the Wayland
clipboard:

```bash
sudo dnf install python3 python3-gobject gstreamer1 pipewire-gstreamer \
  gstreamer1-plugins-base gstreamer1-plugins-good wl-clipboard
```

Then prepare and install Veilshot for the current user:

```bash
git clone https://github.com/kukubanana/veilshot.git
cd veilshot
./setup.sh
./install-local.sh
```

The Python packages are installed only inside the repository's `.venv`.

## Run

Capture a screenshot:

```bash
~/.local/bin/veilshot
```

On Wayland, select one monitor in Fedora's permission dialog. Veilshot then
shows the captured monitor, lets you select a region, and opens the compact
editor.

Other modes:

```bash
~/.local/bin/veilshot --tray
~/.local/bin/veilshot --edit /path/to/image.png
~/.local/bin/veilshot --version
```

## Global shortcut

Open **Settings → Keyboard → View and Customize Shortcuts → Custom Shortcuts**.
Create a shortcut named `Veilshot` with this command:

```text
/home/YOUR_USERNAME/.local/bin/veilshot
```

`Super+Shift+S` is the suggested key combination.

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

## Development and tests

```bash
./setup.sh
QT_QPA_PLATFORM=offscreen .venv/bin/pytest
./run-dev.sh
```

Automated tests do not replace the real Fedora permission, capture, editor, and
clipboard smoke test.

## Privacy

Wayland frames travel from the system Portal through PipeWire into memory and
then directly into the editor. Veilshot does not create an intermediate image
file. Copy publishes the final flattened PNG to the system clipboard. Opaque
redactions replace the covered source pixels in that flattened result.

Veilshot does not upload images, use telemetry, keep screenshot history, or
access the network during capture.

## Known limitations

- Fedora asks for monitor permission on every Wayland capture by design.
- The Fedora MVP captures one selected monitor at a time.
- Cross-monitor region selection is not supported.
- Mixed-DPI and multi-monitor combinations need broader testing.
- Tray visibility on GNOME depends on AppIndicator/system-tray support; the
  global keyboard shortcut works without a visible tray.
- No text, freehand drawing, blur, pixelation, OCR, or screenshot history.

## X11 notes

The previous Qt/X11 capture backend remains available. On X11, Veilshot keeps
the invisible process alive until another application or clipboard manager has
taken the copied image, with a 120-second fallback timeout.

## License

MIT
