# Support

## Before reporting a problem

Run:

```bash
~/.local/bin/veilshot --version
printf 'Session: %s\nDesktop: %s\n' "$XDG_SESSION_TYPE" "$XDG_CURRENT_DESKTOP"
QT_QPA_PLATFORM=offscreen .venv/bin/pytest
```

For tray issues:

```bash
pgrep -af 'veilshot.*--tray'
cat "${XDG_RUNTIME_DIR:-/tmp}/veilshot-tray.log"
```

## Current support boundary

The verified target is Pop!_OS 22.04 with GNOME on X11. Wayland screenshot capture is not currently supported.

## Bug reports

Use the repository bug-report template and remove all private information from screenshots, logs, paths, and clipboard examples.
