# Distribution plan

## Recommended order

### Stage 1 — Public GitHub repository

GitHub is the source of truth for:

- Source code and history.
- Issues and feature discussion.
- Documentation.
- Tagged releases and downloadable assets.
- Automated tests.

A repository alone does not make Veilshot easy for non-technical users, but it is the correct first public step.

Recommended repository setup:

- Repository name: `veilshot`.
- Short description: `Minimal privacy-first screenshot annotation for Linux.`
- Topics: `linux`, `screenshot`, `wayland`, `pipewire`, `x11`, `pyside6`,
  `qt`, `privacy`, `redaction`.
- Public license: confirm MIT and brand-asset policy before publishing.
- Enable Issues and Discussions only if the maintainer is ready to review them.
- Protect the default branch after CI is configured.

### Stage 2 — GitHub alpha release

Publish a tagged pre-release for technically confident testers. State prominently:

- Fedora GNOME Wayland is the primary verified target.
- Fedora shows its monitor permission dialog for every capture.
- Pop!_OS 22.04 X11 remains a compatibility path.
- System packages may be required.
- The current installer uses a project-local Python virtual environment.

### Stage 3 — Flatpak / Flathub

For ordinary Linux users, Flathub is the strongest store-like destination. Once accepted, applications can be installed through Flathub and graphical software centers that use it.

Before submission, Veilshot needs:

- Stable reverse-DNS app ID, typically based on a controlled domain or GitHub identity.
- AppStream metadata.
- Flatpak manifest with reproducible dependencies.
- Screenshots and store description.
- Privacy and license metadata.
- Correct X11 and tray permissions.
- Clean sandbox testing on multiple systems.
- A stable release rather than a rapidly changing development snapshot.

The app should not be described as “uploaded directly to the Pop!_OS store” unless System76 provides a separate submission route. The practical cross-distribution route is Flathub; Pop!_OS users with Flathub enabled can install from their graphical software center or Flatpak.

### Optional packages later

- `.deb`: useful for Ubuntu/Pop!_OS but adds packaging and repository maintenance.
- AppImage: convenient standalone download but updates, desktop integration, and tray behavior require additional work.
- PyPI: useful for Python developers, not the primary end-user distribution channel.

## Information needed before creating packaging

- Final GitHub username or organization.
- Stable app ID.
- Public maintainer/contact identity.
- Final license and brand-asset policy.
- Whether the name `Veilshot` remains final.
- Minimum supported distributions and sessions.

## Publication readiness gate

Do not submit to Flathub until:

- External testers can install and use a tagged release.
- Critical capture, redaction, clipboard, and tray bugs are resolved.
- Packaging can be rebuilt from a clean environment.
- Store metadata and screenshots are final enough for public presentation.
