# GoreeCloud PDF Manager — Tracked binary asset evidence

**Evidence status:** Source metadata only. **No individual asset redistribution or trademark rights are verified.** Not an approval to publish binary bundles, fonts, logos, icons, documents, libraries or model weights.

The bounded standard-library [asset evidence collector](../scripts/tracked_asset_evidence.py) uses Git's tracked-path index to select files whose extensions match bundled fonts, images, PDF fixtures, native binaries and model formats. It hashes the bytes of each regular tracked file with SHA-256, records size, path and category, and explicitly labels **every asset** as `license_status=UNVERIFIED`. It checks each path component for symlinks, verifies resolved checkout containment and, on POSIX GitHub CI, uses no-follow directory descriptors to avoid reading symlinked parent directories even if a working-tree path changes after inspection. Non-POSIX manual runs retain a best-effort component/containment check and should run against a quiescent trusted checkout. It does not deliberately open symlink targets, execute the files, install dependencies, scan untracked private files, or access a network.

To reproduce against an authorized local checkout:

    python3 -m unittest discover -s scripts/tests -p test_tracked_asset_evidence.py -v
    python3 scripts/tracked_asset_evidence.py --output tracked-asset-evidence.json

The generated JSON is not committed, so changing package or source assets automatically changes the evidence. The [read-only GitHub workflow](../.github/workflows/asset-evidence.yml) reruns eight regression tests, independently produces byte-identical output twice and retains a nonpublishing report for **seven days**.

## Current checked source snapshot

At the initial PR baseline, 389 tracked files matched the binary-asset/document extensions: **47 fonts, 246 image/icon assets and 96 PDF fixtures**. The font files represent approximately 41.7 MB. The repository contains a Noto Sans OFL notice for part of the frontend font tree and an icon-license notice, **but these files do not prove that every matching asset is covered**. Source name, a known font family or a checksum cannot prove right-to-redistribute, trademark rights, modification permissions or attribution completeness. Treat any image/logo or PDF fixture with no directly verified provenance as **review required**.

## Adjacent license-notice candidate review queue

The [adjacent notice metadata collector](../scripts/asset_notice_review_queue.py)
compares only **tracked Git pathnames** with the existing 389-asset
inventory. It proposes same-directory plaintext notice candidates matching
narrow LICENSE/LICENCE/COPYING/NOTICE/OFL naming rules, excludes source code
and JSON license-policy configuration files, and **does not read or interpret
the license text**. It never uses the root license as a substitute for a
separate font/image/document notice.

In the November 8 snapshot, **one asset**
(frontend/public/fonts/NotoSans-Regular.ttf) has the adjacent candidate
frontend/public/fonts/NotoSans-OFL.txt. The remaining **388 assets lack
a same-directory candidate under these narrow rules**; that is not evidence
they lack licenses elsewhere. **All 389 remain redistribution-rights
UNVERIFIED**, including Noto Sans, and no asset has been cleared by this
tool.

Reproduce with:

    python3 -m unittest discover -s scripts/tests -p test_asset_notice_review_queue.py -v
    python3 scripts/asset_notice_review_queue.py --output asset-license-notice-queue.json

The existing read-only asset workflow repeats the seven synthetic notice
tests, independently writes and byte-compares two reports, and retains the
nonrelease queue alongside the existing asset evidence for seven days.
No external lookup, license-text assessment or permission conclusion is made.

## Known exclusions and release blockers

The scanner is evidence of tracked source paths, not a release artifact SBOM. It does not identify every asset loaded at runtime, dynamically downloaded dependencies, assets within JAR/ZIP files, generated binaries, untracked files, third-party source snippets, font name-table license contents, or assets in excluded commercial modules. Existing license files are candidates to inspect but not automatically assigned to asset files. Before any public or commercial release, review each high-impact/third-party font, PDF fixture, logo, SVG and binary; identify its upstream origin, applicable license and attribution, and document whether the exact shipped version is permitted for redistribution. That legal and provenance work remains open under [release issue #1](https://github.com/GoreeCloud/pdf-manager/issues/1).
