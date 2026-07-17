# Flathub packaging placeholder

No production Flatpak manifest is included yet.

A correct manifest must be created and tested after choosing a stable application ID and GitHub repository. Do not replace `YOUR_GITHUB_USERNAME` with a guess.

Likely app-ID pattern:

```text
io.github.YOUR_GITHUB_USERNAME.Veilshot
```

Packaging work must verify:

- PySide6 dependencies are fetched reproducibly.
- X11 socket access is limited to what capture requires.
- Tray/AppIndicator behavior works in the target desktop.
- Clipboard and file-dialog behavior work inside the sandbox.
- AppStream metadata validates.
- Screenshots contain no private information.
