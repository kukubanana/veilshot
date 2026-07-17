# Release process

## Versioning

Use Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

Before 1.0, breaking behavior can still occur, but release notes must state it clearly. Pre-release tags may use:

```text
v0.2.1-alpha.1
v0.3.0-beta.1
```

## Release checklist

1. Confirm the release scope.
2. Update version in `pyproject.toml` and `src/veilshot/__init__.py`.
3. Update `CHANGELOG.md`.
4. Run the automated test suite and record the actual result.
5. Complete the manual smoke test in `docs/TESTING.md`.
6. Inspect `git status` and remove private files.
7. Verify no screenshot contents, local paths, `.venv`, or secrets are committed.
8. Verify license, copyright, brand-assets policy, and dependency licenses.
9. Create a signed or annotated Git tag when practical.
10. Create a GitHub Release with concise notes and supported-system warnings.
11. Attach only reviewed release artifacts.
12. Test the published artifact on a clean account or machine.

## Suggested public alpha artifact

Until Flatpak is ready, provide:

- Source archive generated from the Git tag.
- Checksums.
- Exact setup instructions.
- Supported OS/session statement.
- Known limitations.

The current `install-local.sh` is tied to a project `.venv`, so it should be described as an alpha/developer installer rather than a polished end-user package.

## Rollback

Never reuse a published version tag. Fix the issue and publish a new patch or pre-release version.
