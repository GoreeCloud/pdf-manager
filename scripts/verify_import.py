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
assert tauri['mainBinaryName'] == 'goreecloud-pdf-manager'
assert tauri['version'] == '0.1.0'
assert tauri['build']['beforeBuildCommand'] == 'npx --no-install vite build --mode core'
assert '--mode core' in tauri['build']['beforeDevCommand']
assert '--host 127.0.0.1' in tauri['build']['beforeDevCommand']
assert tauri['build']['devUrl'] == 'http://127.0.0.1:5173'
alternate = json.loads((ROOT / 'frontend/src-tauri/tauri.conf.port5174.json').read_text())
assert '--mode core' in alternate['build']['beforeDevCommand']
assert '--host 127.0.0.1' in alternate['build']['beforeDevCommand']
assert alternate['build']['devUrl'] == 'http://127.0.0.1:5174'
assert tauri['bundle']['active'] is False
assert tauri['bundle']['resources'] == [], 'Preview must not require unavailable bundled server/JRE resources'
assert tauri['bundle']['createUpdaterArtifacts'] is False
assert 'updater' not in tauri['plugins'], 'Untrusted upstream Tauri update channel reintroduced'
rust_root = ROOT / 'frontend/src-tauri'
rust_manifest = tomllib.loads((rust_root / 'Cargo.toml').read_text())
assert rust_manifest['package']['name'] == 'goreecloud-pdf-manager'
assert rust_manifest['package']['license'] == 'MIT'
assert 'tauri-plugin-updater' not in rust_manifest['dependencies']
rust_packages = tomllib.loads((rust_root / 'Cargo.lock').read_text())['package']
# Keep Tauri public/native window-runtime APIs on the same minor release.
# tauri 2.11.1 with tauri-runtime-wry 2.12.3 did not compile on Linux.
locked_versions = {pkg['name']: pkg['version'] for pkg in rust_packages}
assert len({
    tuple(locked_versions[name].split('.')[:2])
    for name in ('tauri', 'tauri-runtime', 'tauri-runtime-wry')
}) == 1, (
    'Incompatible Tauri native runtime versions in Cargo.lock'
)
assert not any(pkg['name'] in {'tauri-plugin-updater', 'zip'} for pkg in rust_packages), (
    'Unused vulnerable desktop updater dependency reintroduced'
)
permissions = json.loads((rust_root / 'capabilities/default.json').read_text())['permissions']
assert not any(str(permission).startswith('updater:') for permission in permissions)
assert 'tauri_plugin_updater' not in (rust_root / 'src/lib.rs').read_text()
commands = (rust_root / 'src/commands/updater.rs').read_text()
assert 'updater_disabled' in commands and 'Ok(None)' in commands

# Chrome sandbox is required when rendering local/HTML templates with Puppeteer.
for rel in ['frontend/scripts/generate-og-image.mjs', 'frontend/scripts/sample-pdf/generate.mjs']:
    script = (ROOT / rel).read_text()
    assert '--no-sandbox' not in script and '--disable-setuid-sandbox' not in script
    assert 'headless: true' in script
devtools = json.loads((ROOT / 'devTools/package.json').read_text())
devtools_lock = json.loads((ROOT / 'devTools/package-lock.json').read_text())
assert devtools['name'] == devtools_lock['name'] == devtools_lock['packages']['']['name'] == 'goreecloud-pdf-manager-devtools'
assert not any('/app/proprietary/' in script for script in devtools.get('scripts', {}).values())
# Legal and privacy policy authority must not silently fall back to Stirling's policies.
assert '  termsAndConditions: ""' in defaults
assert '  privacyPolicy: ""' in defaults
for rel in [
    'app/core/src/main/java/stirling/software/SPDF/config/InitialSetup.java',
    'app/core/src/main/java/stirling/software/SPDF/config/OpenApiConfig.java',
    'frontend/src/editor/core/components/shared/Footer.tsx',
    'frontend/src/editor/core/components/shared/config/configSections/LegalSection.tsx',
]:
    legal_source = (ROOT / rel).read_text()
    assert 'stirlingpdf.com/terms' not in legal_source
    assert 'stirlingpdf.com/privacy-policy' not in legal_source
    assert 'stirling.com/terms' not in legal_source
    assert 'stirling.com/privacy' not in legal_source
assert 'GoreeCloud PDF Manager API' in (ROOT / 'app/core/src/main/java/stirling/software/SPDF/config/OpenApiConfig.java').read_text()
assert 'serviceLegalHref' in (ROOT / 'frontend/src/editor/core/components/shared/Footer.tsx').read_text()
assert 'serviceLegalHref' in (ROOT / 'frontend/src/editor/core/components/shared/config/configSections/LegalSection.tsx').read_text()
# The sanitized core deliberately lacks inherited pipeline preset resources.
# Optional preset setup cannot abort all unrelated PDF features on startup.
core_setup = (ROOT / 'app/core/src/main/java/stirling/software/SPDF/config/InitialSetup.java').read_text()
general_utils = (ROOT / 'app/common/src/main/java/stirling/software/common/util/GeneralUtils.java').read_text()
assert 'initBundledPipelinePresets();' in core_setup
assert 'GeneralUtils.hasBundledPipelineDefaults()' in core_setup
assert 'public boolean hasBundledPipelineDefaults()' in general_utils
assert 'public void extractPipeline() throws IOException' in general_utils
# Require the actual frontend CI job to exercise the Storybook docgen
# wildcard integration, not merely accept an npm lockfile after an unsafe
# transitive glob/minimatch major-version override.
docgen_contract = ROOT / 'frontend/scripts/verify-docgen-glob.mjs'
assert docgen_contract.is_file(), 'Missing docgen glob wildcard regression gate'
core_workflow = (ROOT / '.github/workflows/core-build.yml').read_text()
assert 'node scripts/verify-docgen-glob.mjs' in core_workflow, (
    'Docgen glob wildcard check must stay in required Node 24 CI'
)
# Keep semantic PDF page-count/text-order verification wired into the
# required Java job. Mere PDF magic bytes are insufficient for a merge smoke.
semantic_smoke = (ROOT / 'scripts/smoke_core_http.py').read_text()
core_workflow = (ROOT / '.github/workflows/core-build.yml').read_text()
assert 'inspect_synthetic_merge_result(merged, pdfinfo, pdftotext)' in semantic_smoke
assert 'test_smoke_pdf_semantics.py' in core_workflow
assert 'pdfinfo -v' in core_workflow and 'pdftotext -v' in core_workflow
# Keep malformed-input fail-closed behavior and post-error health recovery
# in the required Java CI smoke gate, not just local unit tests.
negative_smoke = (ROOT / 'scripts/smoke_core_http.py').read_text()
negative_ci = (ROOT / '.github/workflows/core-build.yml').read_text()
assert 'assert_malformed_pdf_is_rejected_and_server_remains_healthy(base)' in negative_smoke
assert 'test_smoke_invalid_upload.py' in negative_ci
merge_controller = (ROOT / 'app/core/src/main/java/stirling/software/SPDF/controller/api/MergeController.java').read_text()
assert 'if (!invalidIndexes.isEmpty())' in merge_controller
assert 'ExceptionUtils.createMultiplePdfCorruptedException(' in merge_controller
assert 'MalformedPdfMergeTest' in negative_ci
# Zero-file merges must not succeed with an invalid PDF response.
assert 'ExceptionUtils.createFileNullOrEmptyException()' in merge_controller
assert 'assert_no_file_merge_is_rejected(base)' in negative_smoke
assert 'MergeControllerMoreTest' in negative_ci
# The runnable JAR's actual embedded dependency manifest must be generated
# and deterministically compared in the existing required Java build job.
runtime_evidence_script = ROOT / 'scripts/runtime_jar_inventory.py'
assert runtime_evidence_script.is_file()
assert 'test_runtime_jar_inventory.py' in core_workflow
assert 'scripts/runtime_jar_inventory.py --jar' in core_workflow
assert 'cmp /tmp/gcpdf-core-libraries-a.json /tmp/gcpdf-core-libraries-b.json' in core_workflow
# Pin the proven MIT-core Storybook diagnostic to the actual reviewed
# plugin-to-glob-to-minimatch chain; never rely on npm install alone.
core_storybook = ROOT / 'frontend/.storybook-core/main.ts'
assert core_storybook.is_file()
assert 'Tokens.stories.tsx' in core_storybook.read_text()
assert 'storybook build --config-dir .storybook-core' in core_workflow
assert "assert.equal(minimatchVersion, '11.0.1'" in docgen_contract.read_text()
# Health UP alone is insufficient to show request-level recovery after
# both malformed-input and empty multipart upload rejection.
assert 'recovered = fetch_synthetic_merged_pdf(base)' in negative_smoke
assert 'inspect_synthetic_merge_result(recovered, pdfinfo, pdftotext)' in negative_smoke
# An adjacent license notice filename is only a candidate for manual review,
# never redistribution permission. Keep the conservative read-only CI gate.
asset_notice = ROOT / 'scripts/asset_notice_review_queue.py'
asset_workflow = (ROOT / '.github/workflows/asset-evidence.yml').read_text()
assert asset_notice.is_file()
assert 'redistribution_rights": "UNVERIFIED"' in asset_notice.read_text()
assert 'test_asset_notice_review_queue.py' in asset_workflow
assert 'asset-license-notice-queue.json' in asset_workflow
# Do not reintroduce Storybook's vulnerable Vitest mocker dependency without
# checking the exact module that Storybook itself resolves.
mocker_contract = ROOT / 'frontend/scripts/verify-storybook-mocker.mjs'
assert mocker_contract.is_file()
assert "manifest.version, '4.1.12'" in mocker_contract.read_text()
assert 'node scripts/verify-storybook-mocker.mjs' in core_workflow
# Cargo advisory paths are release review evidence, never a claim that an
# inherited GTK/PHF runtime vulnerability is fixed or safe to ship.
native_graph_script = ROOT / 'scripts/native_advisory_paths.py'
advisory_workflow = (ROOT / '.github/workflows/dependency-audit.yml').read_text()
assert native_graph_script.is_file()
assert 'test_native_advisory_paths.py' in advisory_workflow
assert 'native_advisory_paths.py --output' in advisory_workflow
assert 'retention-days: 7' in advisory_workflow
# Do not regress to the upstream 2GB multipart defaults or drop live HTTP 413.
application_properties = (ROOT / 'app/core/src/main/resources/application.properties').read_text()
assert 'SPRING_SERVLET_MULTIPART_MAX_FILE_SIZE:128MB' in application_properties
assert 'SPRING_SERVLET_MULTIPART_MAX_REQUEST_SIZE:256MB' in application_properties
assert 'assert_oversized_synthetic_upload_is_rejected(base)' in negative_smoke
assert '"oversized_synthetic_pdf_rejected_http_413": True' in negative_smoke
assert 'test_smoke_invalid_upload.py' in core_workflow
# Unused JS shell-open grants should never be inherited by the desktop
# webview; Rust's explicitly internal sidecar process API stays compiled.
desktop_gate = ROOT / 'scripts/verify_desktop_webview_permissions.py'
native_build_workflow = (ROOT / '.github/workflows/desktop-linux-compile.yml').read_text()
assert desktop_gate.is_file()
assert 'shell:allow-open' not in permissions
assert 'test_verify_desktop_webview_permissions.py' in native_build_workflow
assert 'verify_desktop_webview_permissions.py' in native_build_workflow
# The custom MultipartConfigElement must honor separate request/file caps.
multipart_java = (ROOT / 'app/core/src/main/java/stirling/software/SPDF/config/MultipartConfiguration.java').read_text()
assert 'DEFAULT_FILE_LIMIT = "128MB"' in multipart_java
assert 'DEFAULT_REQUEST_LIMIT = "256MB"' in multipart_java
assert 'factory.setMaxRequestSize(DataSize.ofBytes(requestBytes));' in multipart_java
assert 'factory.setMaxFileSize(DataSize.ofBytes(fileBytes));' in multipart_java
assert 'MultipartConfigurationTest' in core_workflow
assert 'assert_aggregate_synthetic_upload_is_rejected(base)' in negative_smoke
assert '"aggregate_synthetic_request_rejected_http_413": True' in negative_smoke
print('MIT-only source boundaries, sanitized credentials, and provenance: PASS')
