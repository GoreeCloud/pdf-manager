#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"$ROOT/scripts/check_source_boundary.sh"

python3 "$ROOT/scripts/validate_workbench_contract.py"
node --check "$ROOT/app/core/src/main/resources/static/goreecloud/pdf-manager.js"

python3 - "$ROOT" <<'PY'
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

root = pathlib.Path(sys.argv[1])

for path in (
    root / "provenance/upstream.json",
    root / "provenance/glaze.json",
    root / "provenance/branding.json",
):
    json.loads(path.read_text(encoding="utf-8"))

ET.parse(root / "app/core/src/main/resources/static/goreecloud/pdf-manager-mark.svg")

entry = root / "app/core/src/main/resources/static/goreecloud/glaze/js/glaze-v1.7.0.mjs"
seen = set()
stack = [entry]
pattern = re.compile(r"(?:from\s+|import\s+)['\"](\./[^'\"]+)['\"]")
while stack:
    path = stack.pop()
    if path in seen:
        continue
    if not path.is_file():
        raise SystemExit(f"missing Glaze module: {path}")
    seen.add(path)
    text = path.read_text(encoding="utf-8")
    for rel in pattern.findall(text):
        target = (path.parent / rel).resolve()
        if target.suffix == "":
            target = target.with_suffix(".mjs")
        stack.append(target)

print(f"repository-validation: Glaze module closure OK ({len(seen)} modules)")

workbench_html = (root / "app/core/src/main/resources/static/api-landing.html").read_text(encoding="utf-8")
workbench_js = (root / "app/core/src/main/resources/static/goreecloud/pdf-manager.js").read_text(encoding="utf-8")

required_html_markers = {
    'id="guideButton"': "Guide replay control",
    'id="onboardingDialog"': "first-use onboarding dialog",
    'id="contextHint"': "contextual hint surface",
}
for marker, description in required_html_markers.items():
    if marker not in workbench_html:
        raise SystemExit(f"missing {description}: {marker}")

required_js_markers = {
    '"/api/v1/config/endpoints-availability"': "authoritative capability availability request",
    "tool.available !== true": "fail-closed tool execution gate",
    "storageKeys.onboarding": "persisted onboarding state",
    "storageKeys.hints": "persisted hint preference",
    "openOnboarding({ replay: true })": "onboarding replay control",
    "renderContextHint()": "contextual hint rendering",
}
for marker, description in required_js_markers.items():
    if marker not in workbench_js:
        raise SystemExit(f"missing {description}: {marker}")

print("repository-validation: capability truth and onboarding contract OK")
PY

printf 'repository-validation: PASS\n'
