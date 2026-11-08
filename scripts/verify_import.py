#!/usr/bin/env python3
"""Static guard for intentionally sanitized, open-core source imports."""
from pathlib import Path
import json
import tomllib
import subprocess
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
# Inspect Git's index rather than generated/ignored node_modules or build output.
tracked = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '-z', '--cached']).split(b'\0')
tracked = [Path(p.decode('utf-8')) for p in tracked if p]
for path in tracked:
    assert not any(path == Path(prefix) or Path(prefix) in path.parents for prefix in excluded), (
        f'Restricted tracked path: {path}'
    )
    assert path.suffix.lower() not in {'.key', '.pem', '.p12', '.pfx'}, f'Bundled key: {path}'
    assert path == Path('.task/.env') or path.name not in {'.env', '.env.local', '.env.proprietary', '.env.saas'}, (
        f'Bundled environment file: {path}'
    )
task_defaults = (ROOT / '.task/.env').read_text().splitlines()
for line in task_defaults:
    if line.strip() and not line.lstrip().startswith('#'):
        assert line.strip() == 'STIRLING_CHECK_JOBS=', 'Unexpected committed task environment value'
settings = (ROOT / 'settings.gradle').read_text()
assert "rootProject.name = 'GoreeCloud PDF Manager'" in settings
assert 'gradle.ext.disableAdditional = true' in settings
assert 'gradle.ext.enableSaas = false' in settings
assert 'MIT core flavor' in settings
root_gradle = (ROOT / 'build.gradle').read_text()
assert 'dependsOn(":proprietary:jar")' not in root_gradle
vite = (ROOT / 'frontend/vite.config.ts').read_text()
assert 'MIT_ONLY_CORE_BUILD' in vite
assert 'secure: true' in vite
cors = (ROOT / 'app/core/src/main/java/stirling/software/SPDF/config/WebMvcConfig.java').read_text()
assert '.allowedOriginPatterns("*")' not in cors, 'Wildcard credentialed CORS must be disabled'
assert 'CORS remains disabled' in cors
assert '.allowedOrigins(configuredOrigins.toArray(new String[0]))' in cors
defaults = (ROOT / 'app/core/src/main/resources/settings.yml.template').read_text()
for key in ['enableAnalytics', 'enablePosthog', 'enableScarf', 'enableFeedback', 'showUpdate', 'enableDesktopInstallSlide']:
    assert f'  {key}: false' in defaults, f'Unsafe default: {key}'
assert '    enabled: false # Self-signed server signing certificates' in defaults
updater = (ROOT / 'frontend/src/editor/core/services/updateService.ts').read_text()
assert 'supabase.stirling.com' not in updater
assert 'files.stirlingpdf.com' not in updater
assert 'return null;' in updater
assert 'GoreeCloud PDF Manager has no verified' in updater
tauri = json.loads((ROOT / 'frontend/src-tauri/tauri.conf.json').read_text())
assert tauri['productName'] == 'GoreeCloud PDF Manager'
assert tauri['bundle']['active'] is False
assert tauri['bundle']['createUpdaterArtifacts'] is False
assert 'updater' not in tauri['plugins'], 'Untrusted upstream Tauri update channel reintroduced'
rust_root = ROOT / 'frontend/src-tauri'
rust_manifest = tomllib.loads((rust_root / 'Cargo.toml').read_text())
assert rust_manifest['package']['name'] == 'goreecloud-pdf-manager'
assert rust_manifest['package']['license'] == 'MIT'
assert 'tauri-plugin-updater' not in rust_manifest['dependencies']
rust_packages = tomllib.loads((rust_root / 'Cargo.lock').read_text())['package']
assert not any(pkg['name'] in {'tauri-plugin-updater', 'zip'} for pkg in rust_packages), (
    'Unused vulnerable desktop updater dependency reintroduced'
)
permissions = json.loads((rust_root / 'capabilities/default.json').read_text())['permissions']
assert not any(str(permission).startswith('updater:') for permission in permissions)
assert 'tauri_plugin_updater' not in (rust_root / 'src/lib.rs').read_text()
commands = (rust_root / 'src/commands/updater.rs').read_text()
assert 'updater_disabled' in commands and 'Ok(None)' in commands

print('MIT-only source boundaries, sanitized credentials, and provenance: PASS')
