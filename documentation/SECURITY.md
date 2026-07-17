# Security policy

## Supported versions

Veilshot is currently an early alpha. Security fixes target the latest version only.

## Reporting a vulnerability

Until a public security contact is configured, do not publish sensitive vulnerability details in a public issue. Contact the maintainer privately through the contact method listed on the repository profile.

Useful report contents:

- Veilshot version and commit.
- Linux distribution, desktop environment, and X11/Wayland session.
- Reproduction steps.
- Whether screenshot contents, clipboard contents, or redacted pixels can be exposed.
- Minimal non-sensitive test material.

## Security-sensitive invariants

- Opaque redaction must replace source pixels in flattened output.
- Screenshot contents must not be logged.
- Clipboard images must not be written to disk.
- Captures must not be uploaded or sent over the network.
- Temporary files should not be introduced without an explicit design review.
