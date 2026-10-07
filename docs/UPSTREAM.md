# Upstream Maintenance — Stirling-PDF

## Baseline

`Stirling-Tools/Stirling-PDF@973bff865cc19fbc268859e1fb13103c66c1f5a5`

## Sync procedure

Before every material upstream adoption:

1. Verify the current upstream license and directory-specific notices.
2. Review new/moved directories for licensing changes.
3. Ensure restricted source cannot enter GoreeCloud repository history.
4. Review security advisories, dependencies, migrations, and build changes.
5. Import only required open-source source.
6. Reconcile GoreeCloud build and UI boundaries.
7. Run source-boundary, build, test, security, and license checks.
8. Record the exact adopted revision in this file, `NOTICE.md`, and `CHANGELOGS.md`.
9. Validate the exact candidate head through the normal pull-request workflow.

The current upstream frontend workspace is excluded because its package metadata declares a proprietary-license reference. GoreeCloud maintains an independent interface.
