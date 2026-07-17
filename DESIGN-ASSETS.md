# Veilshot design asset specifications

This file is the handoff specification for replacing Veilshot's temporary visual assets.
The source artwork should stay editable and should not contain a baked checkerboard.
All exported images use an actual transparent alpha channel and the sRGB color space.

## 1. Application / launcher icon

Purpose: Pop!_OS application grid, dock, `.desktop` launcher, repositories, and future store listing.

- Master format: **SVG**
- Canvas / `viewBox`: **512 × 512** or **256 × 256**, square
- Safe area: keep the important silhouette inside the central **80–84%** of the canvas
- Background: transparent
- Recommended detail: readable when reduced to **32 × 32 px**
- Suggested maximum SVG size: **50 KB**; ideally below **20 KB**
- Do not embed raster images, fonts, metadata-heavy editor data, or a checkerboard background
- Convert strokes to paths before a public release if exact rendering across programs is important

Recommended PNG exports for testing and distribution:

- 16 × 16
- 24 × 24
- 32 × 32
- 48 × 48
- 64 × 64
- 128 × 128
- 256 × 256
- 512 × 512
- 1024 × 1024 only for a future store / press asset

Linux icon theme name: `veilshot`.
The scalable icon is installed as:

```text
~/.local/share/icons/hicolor/scalable/apps/veilshot.svg
```

## 2. System tray icon

Purpose: Pop!_OS top panel. This is a separate drawing, not a simple reduction of the launcher icon.

- Master format: **SVG**
- Exact canvas / `viewBox`: **22 × 22**
- Primary optical target: **22 × 22 px**
- Also test at: **16, 20, 24, and 32 px**
- Safe margin: **1.5–2 px** from every edge
- Main stroke: approximately **2–2.75 px** at the 22 px master size
- Stroke caps / joins: round
- Maximum number of colors: **2**
- No text, gradients, shadows, thin gaps, or details smaller than about **1.5 px**
- Suggested SVG size: below **10 KB**
- For Pop!_OS's dark top panel, use a light main silhouette; the accent may be purple

Optional PNG fallbacks:

- 16 × 16
- 22 × 22
- 24 × 24
- 32 × 32
- 44 × 44 for 2× preview / HiDPI testing

The tray icon should be checked at native size, not only enlarged in an editor.

## 3. Editor toolbar icons

Purpose: arrow, highlight, redaction, color, undo, redo, copy, save, close, eyedropper.

- Master format: **SVG**, one file per icon
- Canvas / `viewBox`: **24 × 24**
- Visible glyph area: normally **18–20 px**
- Safe margin: **2 px**
- Standard stroke: **2 px**
- Caps / joins: round
- Prefer one-color icons designed to inherit the UI foreground color
- Avoid filled micro-details smaller than **2 px**
- Suggested SVG size: below **5 KB** per icon
- Use consistent stroke, corner radius, optical weight, and visual center across the whole set

The current toolbar buttons are **38 × 38 px**, and the icon inside each button is rendered at **22 × 22 px**.
The future set should therefore be tested at both **22 px** and **24 px**.

Recommended states are produced by the interface rather than separate files:

- normal
- hover
- active / selected
- disabled

Only create separate SVG files for states when the geometry itself changes.

## 4. Cursors

For a future custom crosshair or eyedropper cursor:

- Preferred source: SVG
- Runtime export: transparent PNG
- Sizes: **32 × 32** and **64 × 64** for 2×
- Define and document the hotspot coordinate, for example `(16, 16)` for a centered crosshair or `(2, 29)` for an eyedropper tip
- Keep the hotspot on an exact pixel

## 5. Typography

Desktop applications should use **OTF** or **TTF** fonts. Do not supply WOFF or WOFF2; those are web formats.

Recommended minimal family set:

- Regular 400
- Medium 500
- Semibold 600

Use Bold 700 only when a real hierarchy requires it. A variable OTF/TTF is acceptable if Qt renders it correctly on Linux.

Practical UI sizes for later testing:

- Tooltips / helper text: 11–12 pt
- Standard UI text: 12–13 pt
- Menu actions: 12–13 pt
- Larger labels, if added: 14–16 pt

Before bundling a font, verify that its license permits redistribution inside an open-source application. A font file should not be committed merely because it is installed on the designer's computer.

## 6. Delivery checklist

For each custom icon provide:

1. Editable source file.
2. Clean optimized SVG.
3. PNG previews at the actual target sizes.
4. Name matching the project convention.
5. Confirmation that transparency is real.
6. License / author note.

Suggested filenames:

```text
veilshot.svg
veilshot-tray.svg
arrow.svg
highlight.svg
redaction.svg
color.svg
undo.svg
redo.svg
copy.svg
save.svg
close.svg
eyedropper.svg
```
