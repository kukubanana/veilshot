# Fedora Wayland capture spike

`portal_pipewire_frame.py` is the original standalone proof for the Fedora
Wayland capture path:

```text
ScreenCast Portal → PipeWire remote fd + node id → GStreamer → one PNG frame
```

The script does not use Qt screen grabbing, does not invoke GNOME Screenshot,
and does not create a temporary screenshot. It writes only the explicit output
file requested on the command line.

## Fedora prerequisites

On Fedora Workstation the relevant packages are:

```bash
sudo dnf install python3-gobject gstreamer1 pipewire-gstreamer \
  gstreamer1-plugins-base gstreamer1-plugins-good wl-clipboard
```

Check the current session without opening a permission dialog:

```bash
python3 spikes/portal_pipewire_frame.py --check
```

## Manual GNOME Wayland test

Run this from a terminal inside the logged-in GNOME Wayland session:

```bash
python3 spikes/portal_pipewire_frame.py /tmp/veilshot-portal-frame.png
```

1. In GNOME's system picker, select one monitor and approve sharing.
2. Confirm that the command reports exactly one captured frame and exits.
3. Open `/tmp/veilshot-portal-frame.png` and verify that it contains the
   selected monitor, including the pointer.
4. Delete that explicit test output when finished.
5. Run the command a second time to observe the current permission/picker UX.

The production backend now uses the same Portal/PipeWire mechanism and
intentionally opens Fedora's permission dialog for every capture.
