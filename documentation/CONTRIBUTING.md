# Contributing to Veilshot

Veilshot welcomes focused contributions that preserve its intentionally small scope.

## Before opening code

1. Read `AGENTS.md`.
2. Read `docs/PRODUCT_REQUIREMENTS.md` and `docs/DECISION_LOG.md`.
3. Search existing issues before proposing a feature.

## Scope test

A proposed feature should normally satisfy all three conditions:

- It shortens or improves the core screenshot flow.
- It does not turn Veilshot into a general-purpose image editor.
- It can be explained without adding a settings screen.

Large features such as OCR, cloud upload, history, plugins, and account systems are out of scope unless the product direction is explicitly reconsidered.

## Development setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -e '.[dev]'
QT_QPA_PLATFORM=offscreen .venv/bin/pytest
```

## Pull requests

- Keep changes small and focused.
- Explain the user problem, not only the implementation.
- Add tests for logic and regressions.
- Include manual test steps for GUI changes.
- Do not include private screenshots or clipboard data.
- Update documentation and `CHANGELOG.md` when behavior changes.

## Commit style

Use imperative, focused messages, for example:

```text
Fix tray duplicate-process detection
Add regression test for redaction export
Document X11 clipboard lifecycle
```
