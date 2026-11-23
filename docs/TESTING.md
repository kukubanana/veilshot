# Testing strategy

## Automated tests

Run:

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/pytest
```

The suite should cover:

- CLI argument behavior.
- Annotation geometry and painting.
- Undo/redo commands.
- Flattened export.
- Opaque redaction pixel replacement.
- Filename generation.
- Overlay interaction smoke paths.
- Icon/resource availability.
- Desktop entry generation.
- Tray command and duplicate-process logic where practical.
- Wayland/X11 backend selection.
- Portal helper PNG decoding and failure propagation.
- Wayland clipboard PNG publication.

Do not treat offscreen tests as proof that real Portal permission, PipeWire
capture, X11 capture, tray display, clipboard ownership, or mixed-DPI behavior
works.

## Required manual smoke test

For each release candidate:

1. Start capture with the global shortcut.
2. On Wayland, approve one monitor in the system dialog.
3. Select a region.
4. Copy without annotations.
5. Add an arrow.
6. Add a highlight.
7. Add an opaque redaction.
8. Move and resize objects.
9. Undo and redo.
10. Delete an object.
11. Paste into a browser.
12. Paste into a messenger.
13. Save a PNG.
14. Confirm copy did not create a file.
15. Start capture from the tray.
16. Exit and restart tray mode.
17. Log out and confirm tray autostarts after login.
18. Start a second capture and confirm the permission dialog appears again.
19. Test the external monitor when available.

## Privacy regression check

Use a generated test image, cover a known pixel region with opaque redaction, export, and assert that every covered pixel equals the redaction color. Never use a real private screenshot as a committed fixture.

## Release matrix for the public alpha

Minimum suggested systems:

- Fedora Workstation 45 GNOME Wayland — primary.
- Pop!_OS 22.04 GNOME X11 — compatibility.
- One additional Fedora GNOME Wayland machine.

Record Python, Qt, monitor count, scaling, tray support, and results.
