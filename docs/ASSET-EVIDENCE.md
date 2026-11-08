# GoreeCloud PDF Manager — Tracked binary asset evidence

**Evidence status:** Source metadata only. **No individual asset redistribution or trademark rights are verified.** Not an approval to publish binary bundles, fonts, logos, icons, documents, libraries or model weights.

The bounded standard-library [asset evidence collector](../scripts/tracked_asset_evidence.py) uses Git's tracked-path index to select files whose extensions match bundled fonts, images, PDF fixtures, native binaries and model formats. It hashes the bytes of each regular tracked file with SHA-256, records size, path and category, and explicitly labels **every asset** as `license_status=UNVERIFIED`. It does not open symlink targets, execute the files, install dependencies, scan untracked private files, or access a network.

To reproduce against an authorized local checkout:

    python3 -m unittest discover -s scripts/tests -p test_tracked_asset_evidence.py -v
    python3 scripts/tracked_asset_evidence.py --output tracked-asset-evidence.json

The generated JSON is not committed, so changing package or source assets automatically changes the evidence. The [read-only GitHub workflow](../.github/workflows/asset-evidence.yml) reruns seven regression tests, independently produces byte-identical output twice and retains a nonpublishing report for **seven days**.

## Current checked source snapshot

At the initial PR baseline, 389 tracked files matched the binary-asset/document extensions: **47 fonts, 246 image/icon assets and 96 PDF fixtures**. The font files represent approximately 41.7 MB. The repository contains a Noto Sans OFL notice for part of the frontend font tree and an icon-license notice, **but these files do not prove that every matching asset is covered**. Source name, a known font family or a checksum cannot prove right-to-redistribute, trademark rights, modification permissions or attribution completeness. Treat any image/logo or PDF fixture with no directly verified provenance as **review required**.

## Known exclusions and release blockers

The scanner is evidence of tracked source paths, not a release artifact SBOM. It does not identify every asset loaded at runtime, dynamically downloaded dependencies, assets within JAR/ZIP files, generated binaries, untracked files, third-party source snippets, font name-table license contents, or assets in excluded commercial modules. Existing license files are candidates to inspect but not automatically assigned to asset files. Before any public or commercial release, review each high-impact/third-party font, PDF fixture, logo, SVG and binary; identify its upstream origin, applicable license and attribution, and document whether the exact shipped version is permitted for redistribution. That legal and provenance work remains open under [release issue #1](https://github.com/GoreeCloud/pdf-manager/issues/1).
