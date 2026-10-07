# Notices and upstream provenance

## Stirling-PDF

GoreeCloud PDF Manager is derived in part from the MIT-licensed portions of:

- Project: Stirling-PDF
- Upstream repository: `Stirling-Tools/Stirling-PDF`
- Baseline revision: `973bff865cc19fbc268859e1fb13103c66c1f5a5`
- Baseline verified: 2026-10-07

The upstream root `LICENSE` identifies directory trees governed by a separate Stirling PDF User License. GoreeCloud does **not** import those restricted trees:

- `app/proprietary/`
- `app/saas/`
- `engine/`
- `frontend/editor/src/proprietary/`
- `frontend/editor/src/desktop/`
- `frontend/editor/src/saas/`
- `frontend/editor/src/cloud/`
- `frontend/editor/src/portal/`
- `frontend/editor/src/portal-saas/`

The current upstream `frontend/package.json` declares a proprietary-license reference, so the upstream frontend workspace is not imported. GoreeCloud maintains an independent browser UI.

## Glaze

Vendored runtime source:
- `GoreeCloud/glaze@9ab08060d723b022cdf07d001e8c95bca626a764`
- Shared target: Glaze V1.7 / `1.7.0`
- License: MIT

## Branding

Canonical PDF Manager application icon:
- Repository: `GoreeCloud/branding-assets`
- Branding tree revision observed: `8baba9c3b2761b5c4ff10a4f8ca4b46ebe9894c9`
- Asset: `products/pdf-manager/app-icon.svg`
- Asset blob: `0da0138e02fcca224a0fb5363640da42bb547309`

Local copies are derivatives of the branding authority and must remain synchronized with it.
