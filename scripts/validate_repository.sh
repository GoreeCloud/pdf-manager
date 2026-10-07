#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"$ROOT/scripts/check_source_boundary.sh"

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
PY

printf 'repository-validation: PASS\n'
