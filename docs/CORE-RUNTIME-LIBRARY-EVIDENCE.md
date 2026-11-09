# GoreeCloud PDF Manager — Embedded core JAR library inventory

**Status:** Development-only evidence, nonpublishing and **not** a legal determination, complete CycloneDX SBOM, vulnerability scan, signed attestation, or release.

The public MIT-core source import includes third-party Java dependencies in the executable Spring Boot JAR. The [source-lockfile metadata inventory](LOCKFILE-INVENTORY.md) covers committed npm/Cargo dependency lockfiles, **not the resolved Java dependencies**. This additional gate closes that specific *artifact evidence* gap without pretending that it clears third-party licenses or security.

## Evidence recorded

From the actual JAR built by the existing required Java 25 CI job, `scripts/runtime_jar_inventory.py` records deterministic JSON containing the outer archive's SHA-256 and byte count and, for each nested `BOOT-INF/lib/*.jar`, its filename, uncompressed byte count and **SHA-256 of its actual binary content**. Every library explicitly carries:

- `license_status: UNVERIFIED`
- `vulnerability_status: NOT_ASSESSED`

The script rejects duplicate ZIP entries, malformed or nested library paths, symlink members, non-JAR or restricted upstream module names, missing libraries and oversized/invalid nested entries. It uses only Python's standard library and reads streams with bounded size checks; **no library is extracted or executed**. The input is a locally generated artifact of the controlled, temporary runner, not an untrusted externally supplied archive.

## Reproducible CI validation

The [Open-core build diagnostics](../.github/workflows/core-build.yml) compile and test the core, build the Spring Boot archive, validate archive structure, run **10 isolated synthetic archive regression tests**, and independently generate two library evidence reports. Byte-for-byte comparison with `cmp` is mandatory; only an unprivileged count summary is printed. The reports remain under `/tmp` on the ephemeral runner and are not uploaded, published or saved in the repository.

To rerun on an already verified local JAR:

```bash
python3 -m unittest discover -s scripts/tests -p test_runtime_jar_inventory.py -v
python3 scripts/runtime_jar_inventory.py --jar path/to/core.jar --output /tmp/core-libs-a.json
python3 scripts/runtime_jar_inventory.py --jar path/to/core.jar --output /tmp/core-libs-b.json
cmp /tmp/core-libs-a.json /tmp/core-libs-b.json
```

The output does **not** prove a deterministic Gradle rebuild, that the JAR libraries are trusted, that versions are patched, that all transitive native/shared libraries have been found, or that those libraries may legally be redistributed.

## Outstanding release gates

Correlate each embedded JAR hash with its verified Maven/Gradle coordinate, upstream source repository, POM and license text, package signatures and vulnerability advisories. Independently review runtime and native licenses, copied source/assets, executable packaging and distribution rights, and GoreeCloud Shield/Wardveil policies. These manual or governed gates remain **open**. Avoid uploading copyrighted dependency binaries to public repository history or marking licenses as cleared based only on filenames, POM labels or successful checks.
