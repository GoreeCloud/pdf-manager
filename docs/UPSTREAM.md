# Upstream Maintenance — Stirling-PDF

## Current baseline

`Stirling-Tools/Stirling-PDF@973bff865cc19fbc268859e1fb13103c66c1f5a5`

## Sync procedure

Every material upstream update must:

1. Re-read the upstream root license and directory-specific license notices.
2. Review new or moved directories and frontend package metadata for license changes.
3. Fail closed if restricted source would enter GoreeCloud history.
4. Review security advisories, migrations, build changes, and dependency changes.
5. Import only required open-source source.
6. Reconcile GoreeCloud build, Glaze, branding, and product changes.
7. Run source-boundary, formatting, compile/test, security, and license checks.
8. Record the exact adopted revision in `NOTICE.md`, this record, and `CHANGELOGS.md`.
9. Validate the exact candidate head through pull-request checks.

The current upstream frontend workspace is not imported because its package metadata declares a proprietary license reference.
