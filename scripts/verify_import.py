#!/usr/bin/env python3
"""Static guard for intentionally sanitized, open-core source imports."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
excluded = [
    'app/proprietary', 'app/saas', 'engine',
    'frontend/src/editor/proprietary', 'frontend/src/editor/desktop',
    'frontend/src/editor/saas', 'frontend/src/editor/cloud',
    'frontend/src/processor',
]
for path in excluded:
    assert not (ROOT / path).exists(), f'Restricted source path present: {path}'
assert 'MIT License' in (ROOT / 'LICENSE').read_text()
assert 'Copyright (c) 2025 Stirling PDF Inc.' in (ROOT / 'LICENSE').read_text()
assert '046f1a0e7163fae43ad9b687fdd1c697f05dda8d' in (ROOT / 'UPSTREAM.md').read_text()
assert 'GoreeCloud PDF Manager' in (ROOT / 'README.md').read_text()
assert "implementation project(':proprietary')" not in (ROOT / 'build.gradle').read_text()
for rel in ['app/.env.proprietary', 'app/.env.saas', 'frontend/.env', 'frontend/.env.proprietary', 'frontend/.env.saas', 'frontend/.env.desktop']:
    assert not (ROOT / rel).exists(), f'Unsafe inherited environment file: {rel}'
for path in ROOT.rglob('*'):
    if path.is_file() and path.suffix in {'.key', '.pem', '.p12', '.pfx'}:
        raise AssertionError(f'Bundled credential/test-key file: {path.relative_to(ROOT)}')
print('MIT-only source boundaries, sanitized credentials, and provenance: PASS')
