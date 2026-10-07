#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fail() { printf 'source-boundary: %s\n' "$*" >&2; exit 1; }

restricted=(
  "app/proprietary"
  "app/saas"
  "engine"
  "frontend"
)
for path in "${restricted[@]}"; do
  [[ ! -e "$ROOT/$path" ]] || fail "restricted or license-ambiguous path is present: $path"
done

grep -Fq "include 'stirling-pdf', 'common'" "$ROOT/settings.gradle" || fail "settings.gradle is not pinned to common/core only"
if grep -Eq "include .*proprietary|include .*saas|project\(':proprietary'\)|project\(':saas'\)" "$ROOT/settings.gradle"; then
  fail "settings.gradle contains a restricted project"
fi

if grep -Eq "implementation project\(':proprietary'\)|implementation project\(':saas'\)|dependsOn\(['\"]?:proprietary|dependsOn\(['\"]?:saas"   "$ROOT/build.gradle" "$ROOT/app/core/build.gradle"; then
  fail "build graph references a restricted project"
fi

expected_icon="0da0138e02fcca224a0fb5363640da42bb547309"
actual_icon="$(git -C "$ROOT" hash-object app/core/src/main/resources/static/goreecloud/pdf-manager-mark.svg)"
[[ "$actual_icon" == "$expected_icon" ]] || fail "PDF Manager icon drifted from canonical branding blob"

required_docs=(
  README.md
  NOTICE.md
  docs/README.md
  docs/PROJECT-SPECIFICATIONS.md
  docs/PROJECT-RECORD.md
  docs/IMPLEMENTED-FEATURES.md
  docs/PLANNED-FEATURES.md
  docs/CHANGELOGS.md
  docs/VALIDATION.md
  docs/ARCHITECTURE.md
  docs/SECURITY.md
  docs/PRIVACY.md
  docs/BRANDING.md
  docs/GLAZE-ADOPTION.md
  docs/UPSTREAM.md
  docs/USER-MANUAL.md
  docs/COMPETITIVE-OBJECTIVES.md
  docs/VALIDATION.md
  provenance/upstream.json
  provenance/glaze.json
  provenance/branding.json
  goreecloud.platform.yaml
)
for path in "${required_docs[@]}"; do
  [[ -f "$ROOT/$path" ]] || fail "required record missing: $path"
done

grep -Fq "GoreeCloud PDF Manager" "$ROOT/README.md" || fail "README product identity missing"
grep -Fq "GoreeCloud PDF Manager" "$ROOT/app/core/src/main/resources/static/api-landing.html" || fail "workbench product identity missing"
grep -Fq "/goreecloud/glaze/css/glaze.css" "$ROOT/app/core/src/main/resources/static/api-landing.html" || fail "Glaze stylesheet not wired"
grep -Fq "./glaze/js/glaze-v1.7.0.mjs" "$ROOT/app/core/src/main/resources/static/goreecloud/pdf-manager.js" || fail "Glaze V1.7 runtime not wired"

if grep -Eqi "https?://|google-analytics|googletagmanager|mixpanel|segment\.com|amplitude|hotjar"   "$ROOT/app/core/src/main/resources/static/api-landing.html"   "$ROOT/app/core/src/main/resources/static/goreecloud/pdf-manager.css"   "$ROOT/app/core/src/main/resources/static/goreecloud/pdf-manager.js"; then
  fail "GoreeCloud shell contains an unexpected external/tracking reference"
fi

for root_doc in ARCHITECTURE.md IMPLEMENTED-FEATURES.md PLANNED-FEATURES.md CHANGELOGS.md PRIVACY.md BRANDING.md USER-MANUAL.md PROJECT-RECORD.md PROJECT-SPECIFICATIONS.md COMPETITIVE-OBJECTIVES.md; do
  [[ ! -e "$ROOT/$root_doc" ]] || fail "human documentation must live under docs/: $root_doc"
done

printf 'source-boundary: PASS\n'
