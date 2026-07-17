# Decision log

## D-001 — Build a constrained tool, not a general screenshot editor

**Decision:** Veilshot will expose only arrow, highlight, and opaque redaction in the core editor.

**Reason:** Existing alternatives felt overloaded. Speed and predictability are the differentiator.

## D-002 — Clipboard-first behavior

**Decision:** Copy is the default completion path; no file is created unless Save is explicitly used.

**Reason:** Most captures are pasted into chats, browsers, or documents.

## D-003 — Opaque redaction instead of blur

**Decision:** The privacy tool replaces pixels with a solid color in flattened output.

**Reason:** Blur and pixelation are visual effects and should not be represented as reliable privacy removal.

## D-004 — X11-first MVP

**Decision:** Version 0.x initially targets the verified Pop!_OS X11 environment. Wayland capture is deferred behind a capture backend abstraction.

**Reason:** This reduced the first implementation risk and produced a working MVP quickly.

## D-005 — PySide6 / Qt Widgets

**Decision:** Use Python and PySide6 rather than Rust, C++, Electron, or a web stack.

**Reason:** Fastest path to a native working application for a first-time developer, with adequate X11 capture, drawing, dialogs, clipboard, and tray support.

## D-006 — Desktop environment owns global shortcuts

**Decision:** Do not implement a global keyboard hook. Users assign a GNOME custom shortcut to the launcher command.

**Reason:** Less privilege, fewer compatibility problems, no unnecessary settings UI.

## D-007 — Separate tray process and capture process

**Decision:** Tray mode remains available and launches capture through a detached process.

**Reason:** Capture can exit independently without losing the tray launcher.

## D-008 — Separate tray and launcher artwork

**Decision:** The tray icon is a dedicated 22×22-oriented design, not a reduced launcher image.

**Reason:** Full app icon geometry is not legible at tray size.

## D-009 — GitHub before store packaging

**Decision:** First public milestone should be a repository and source alpha for testers. Store packaging follows after broader testing and a reproducible release process.

**Reason:** A store package increases maintenance, metadata, sandboxing, and compatibility obligations.
