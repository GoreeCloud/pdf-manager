# GoreeCloud PDF Manager — Lockfile Dependency Metadata Inventory

**Status:** Development-only inventory, not an approved release SBOM, signed attestation, license clearance, or vulnerability report.

## Purpose and operation

Run the maintained, Python 3.11+ standard-library-only generator from an authorized repository checkout:

```bash
python3 -m unittest discover -s scripts/tests -p test_locked_dependency_inventory.py -v
python3 scripts/locked_dependency_inventory.py --output lockfile-metadata.json
```

The script reads only the five committed npm and Cargo dependency lockfiles:

- `frontend/package-lock.json`
- `devTools/package-lock.json`
- `frontend/src-tauri/Cargo.lock`
- `frontend/src-tauri/provisioner/Cargo.lock`
- `frontend/src-tauri/thumbnail-handler/Cargo.lock`

It creates a reproducible CycloneDX 1.5 JSON **metadata inventory** containing the distinct package identities and versions, npm SRI and Cargo registry checksums when recorded, evidence paths, and input SHA-256 digests. It does not fetch software, invoke package managers, run project code, execute install hooks, access the network, or modify lockfiles.

## Limits and evidence boundaries

The inventory **does not** establish a complete, resolved, deployable application SBOM. In particular, it does not enumerate:

- Resolved Gradle/Java runtime and test dependency graphs
- Operating system libraries, Linux desktop GTK/WebKit packages, installers, containers, native binary bundles and dynamically loaded code
- Actual runtime reachability, built deployment artifacts, signing or verified distribution provenance
- CSS/fonts/icons/images, embedded assets, copied third-party source, or licensing terms outside the lockfiles
- Vulnerability status or license compliance

Npm lockfile `license` labels are stored only as **unverified hints**; they are not converted into asserted CycloneDX licensing statements. Local Cargo workspace packages and npm links without resolved versions are omitted. Repeated package identities in multiple lockfile paths are deduplicated, while evidence paths are preserved. The inventory includes source-file SHA-256 digests for reproducibility.

Any conflicting integrity digest for one package/version is a validation failure rather than a silently merged record. The six unit tests exercise deterministic output and malformed/missing/conflicting inputs. Passing tests demonstrates metadata parsing, **not** that every dependency is secure or legally redistributable.

## CI and release policy

The [Lockfile dependency metadata workflow](../.github/workflows/lockfile-metadata.yml) uses pinned read-only actions, reruns the six regressions, independently generates and byte-compares two outputs, and retains the resulting metadata JSON in GitHub Actions for **seven days**. It publishes no packages, images or deployed artifacts.

A release-grade SBOM will require the resolved Gradle/Java graph, native libraries, output artifacts, third-party asset inventory and independent license/security review. This record cannot substitute for those gates or for the canonical GoreeCloud Drive project documentation.
