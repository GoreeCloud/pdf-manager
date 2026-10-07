#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

restricted=(
  "app/proprietary"
  "app/saas"
  "engine"
  "frontend"
)

for path in "${restricted[@]}"; do
  if [[ -e "$path" ]]; then
    echo "ERROR: restricted or intentionally excluded upstream path is present: $path" >&2
    exit 1
  fi
done

if grep -RIn --exclude-dir=.git -E "project\(':(proprietary|saas)'\)|dependsOn\(['\"]:(proprietary|saas)" .; then
  echo "ERROR: build configuration references excluded proprietary/SaaS Gradle projects." >&2
  exit 1
fi

required_docs=(
  "docs/README.md"
  "docs/PROJECT-SPECIFICATIONS.md"
  "docs/PROJECT-RECORD.md"
  "docs/IMPLEMENTED-FEATURES.md"
  "docs/PLANNED-FEATURES.md"
  "docs/CHANGELOGS.md"
  "docs/ARCHITECTURE.md"
  "docs/SECURITY.md"
  "docs/PRIVACY.md"
  "docs/BRANDING.md"
  "docs/USER-MANUAL.md"
  "docs/COMPETITIVE-OBJECTIVES.md"
  "docs/UPSTREAM.md"
  "docs/GLAZE-ADOPTION.md"
)

for path in "${required_docs[@]}"; do
  [[ -s "$path" ]] || { echo "ERROR: required repository document is missing or empty: $path" >&2; exit 1; }
done

[[ -s "goreecloud.platform.yaml" ]] || { echo "ERROR: goreecloud.platform.yaml is missing." >&2; exit 1; }
[[ -s "NOTICE.md" ]] || { echo "ERROR: NOTICE.md is missing." >&2; exit 1; }

if grep -In -E "https?://" app/core/src/main/resources/static/goreecloud/pdf-manager.*; then
  echo "ERROR: GoreeCloud-owned UI contains a remote URL. Review privacy/external dependency implications." >&2
  exit 1
fi

if grep -In -Ei "posthog|google-analytics|googletagmanager|segment\.com|mixpanel|amplitude" app/core/src/main/resources/static/goreecloud/pdf-manager.*; then
  echo "ERROR: analytics/tracking reference found in GoreeCloud-owned UI." >&2
  exit 1
fi

node --check app/core/src/main/resources/static/goreecloud/pdf-manager.js
node -e "import(process.cwd() + '/app/core/src/main/resources/static/goreecloud/glaze/js/glaze-v1.7.0.mjs').then(m => { if (m.glazeV170?.version !== '1.7.0' || m.glazeV170?.consumerEligible !== true) process.exit(2); })"

echo "GoreeCloud PDF Manager source boundary: PASS"
