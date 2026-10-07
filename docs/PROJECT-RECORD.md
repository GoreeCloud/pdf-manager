# Project Record — GoreeCloud PDF Manager

## Verified source identities

- Canonical repository: `GoreeCloud/pdf-manager`
- Initial repository base: `d6831aec77500190bdab4797f11064740811b34d`
- Stirling-PDF baseline: `973bff865cc19fbc268859e1fb13103c66c1f5a5`
- Glaze baseline: `GoreeCloud/glaze@9ab08060d723b022cdf07d001e8c95bca626a764`
- Branding tree observed: `GoreeCloud/branding-assets@8baba9c3b2761b5c4ff10a4f8ca4b46ebe9894c9`
- PDF Manager icon blob: `0da0138e02fcca224a0fb5363640da42bb547309`
- Lifecycle: Forge

## Source boundary

Only the upstream MIT core/common processing surface and required build infrastructure are adopted. Restricted upstream source and the proprietary-declared current frontend workspace remain outside the repository.

## Current development state

The Forge rebuild establishes the source boundary, GoreeCloud-owned Glaze shell, canonical branding, core-only Gradle graph, governance records, and CI/source-boundary controls. Exact-head build and workflow evidence must remain synchronized before lifecycle promotion.

## Authority boundary

GitHub is authoritative for repository source, feature state, review, checks, and exact revision identity. Stirling-PDF remains the external upstream for retained processing source. GoreeCloud/glaze is authoritative for Glaze. GoreeCloud/branding-assets is authoritative for product artwork.
