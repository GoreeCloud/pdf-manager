#!/usr/bin/env node
// Lockfile metadata alone cannot establish the mocker used by Storybook.
// Verify the actual resolved package and the minimal safe mock-redirect API.
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const storybookRequire = createRequire(require.resolve('storybook'));
const manifest = JSON.parse(
  readFileSync(storybookRequire.resolve('@vitest/mocker/package.json'), 'utf8'),
);
assert.equal(manifest.version, '4.1.12', 'Storybook resolved an unreviewed mocker version');

const moduleFile = storybookRequire.resolve('@vitest/mocker/redirect');
const { findMockRedirect } = await import(pathToFileURL(moduleFile).href);
assert.equal(typeof findMockRedirect, 'function', 'Storybook redirect API missing');
assert.ok(storybookRequire.resolve('@vitest/mocker/browser'));
assert.ok(storybookRequire.resolve('@vitest/mocker'));

const fixtureRoot = mkdtempSync(join(tmpdir(), 'gcpdf-storybook-mocker-'));
try {
  const mockRoot = join(fixtureRoot, '__mocks__');
  mkdirSync(mockRoot);
  const mockFile = join(mockRoot, 'synthetic-service.js');
  writeFileSync(mockFile, 'export const value = 1;\n');
  assert.equal(
    findMockRedirect(fixtureRoot, 'synthetic-service', null),
    resolve(mockFile),
    'Storybook could not resolve a synthetic direct mock',
  );
  assert.equal(
    findMockRedirect(fixtureRoot, 'nonexistent-synthetic-service', null),
    null,
    'Unexpected unregistered mock',
  );
  // Keep the test strictly local: no private paths, network, package builds,
  // malicious mock payloads, persistence, or user-provided documents.
  console.log('Storybook mocker 4.1.12 resolved and synthetic redirect contract: PASS');
} finally {
  rmSync(fixtureRoot, { recursive: true, force: true });
}
