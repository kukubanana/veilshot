# Fedora GNOME Wayland capture spike

## Result

On 2026-11-23 the standalone spike was run end to end on Fedora Workstation 45,
GNOME, Wayland. It successfully:

1. created an `org.freedesktop.portal.ScreenCast` session;
2. requested one monitor through GNOME's system picker;
3. opened the restricted PipeWire remote returned by the portal;
4. consumed one frame from the selected PipeWire node with GStreamer;
5. produced a valid 2560×1440 RGBA PNG entirely through stdout before writing
   the explicitly requested test output.

The first test frame was 682,648 bytes. A second run also succeeded and produced
a 690,460-byte frame, but showed the system picker again because the standalone
process created a new portal session.

The spike lives in `spikes/portal_pipewire_frame.py`; its manual procedure is in
`spikes/README.md`.

## What can be retained

- The Qt Widgets overlay and canvas.
- Annotation geometry and commands.
- Arrow, highlight, and opaque redaction implementations.
- Flatten/export behavior and editor keyboard controls.
- The capture abstraction boundary.

## What should change

- Replace direct `QScreen.grabWindow(0)` capture on Wayland.
- Select the capture backend from the desktop session instead of importing X11
  unconditionally in `application.py`.
- Revisit clipboard lifetime separately: Wayland clipboard behavior must not be
  assumed to match X11 ownership behavior.

## Editor integration decision

Do not feed PNG files through `--edit`; that would add disk I/O and violate the
clipboard-first privacy model. The production Wayland backend should return a
`QImage`/`QPixmap` created from an in-memory PipeWire frame and pass it through
the existing `CaptureResult` boundary to `OverlayWindow.for_capture()`.

The first Fedora release intentionally creates a new portal session for every
capture and accepts GNOME's monitor permission dialog. This avoids a background
capture session, stored restore tokens, and hidden permission state. The
maintainer explicitly chose this simpler and more transparent behavior after
the spike.

The production backend now passes the frame to the existing editor in memory.
Session persistence can be reconsidered later only if real use shows that the
system dialog is a larger problem than the extra lifecycle complexity.
