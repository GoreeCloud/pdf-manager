#!/usr/bin/env node
// Guard the actual Storybook docgen dependency against incompatible glob/minimatch overrides.
// A dependency lockfile may install cleanly yet silently return no wildcard matches.
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const docgenRequire = createRequire(require.resolve('@joshwooding/vite-plugin-react-docgen-typescript'));
const globRequire = createRequire(docgenRequire.resolve('glob'));
const { globSync } = docgenRequire('glob');
assert.equal(typeof globSync, 'function', 'Docgen glob API is missing');
// Both resolution paths must reflect the *actual plugin's dependencies*:
// a lockfile may contain a patched minimatch elsewhere while the docgen glob
// still resolves a vulnerable older version.
const globVersion = globRequire('glob/package.json').version;
const minimatchVersion = globRequire('minimatch/package.json').version;
assert.equal(globVersion, '13.0.7', 'Docgen must use the reviewed glob 13 integration');
assert.equal(minimatchVersion, '11.0.1', 'Docgen glob must use patched minimatch 11.0.1');

const fixture = mkdtempSync(join(tmpdir(), 'goreecloud-docgen-glob-'));
try {
  mkdirSync(join(fixture, 'components'));
  writeFileSync(join(fixture, 'alpha.json'), '{"fixture":true}\n');
  writeFileSync(join(fixture, 'beta.json'), '{"fixture":true}\n');
  writeFileSync(join(fixture, 'components', 'Example.tsx'), 'export const Example = () => null;\n');
  writeFileSync(join(fixture, 'components', 'README.md'), 'synthetic fixture\n');

  const topLevel = globSync('*.json', { cwd: fixture, nodir: true }).sort();
  assert.deepEqual(topLevel, ['alpha.json', 'beta.json'], 'Docgen glob cannot enumerate wildcard JSON files');

  const nested = globSync('components/**/*.tsx', { cwd: fixture, nodir: true }).sort();
  assert.deepEqual(nested, ['components/Example.tsx'], 'Docgen glob cannot enumerate nested TSX files');

  assert.deepEqual(
    globSync('components/*.md', { cwd: fixture, nodir: true }),
    ['components/README.md'],
    'Docgen glob cannot enumerate sibling documentation files',
  );
  console.log('Storybook docgen glob/minimatch wildcard integration: PASS (synthetic fixture)');
} finally {
  rmSync(fixture, { recursive: true, force: true });
}
