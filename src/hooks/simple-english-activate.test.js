#!/usr/bin/env node
'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert');

// Import the module
const {
 FALLBACK_CONTEXT,
 MAX_CHARS,
 buildContext,
 promptCandidates,
 readFirstFile,
 ruleBlock,
 stripFrontmatter,
} = require('./simple-english-activate.js');

describe('FALLBACK_CONTEXT', () => {
 it('should be a non-empty string', () => {
 assert.ok(FALLBACK_CONTEXT);
 assert.strictEqual(typeof FALLBACK_CONTEXT, 'string');
 assert.ok(FALLBACK_CONTEXT.length > 0);
 });
});

describe('MAX_CHARS', () => {
 it('should be 9500', () => {
 assert.strictEqual(MAX_CHARS, 9500);
 });
});

describe('stripFrontmatter', () => {
 it('should remove yaml frontmatter but keep body rules', () => {
 const input = `---
name: test
---
Some content
---
More content`;
 const result = stripFrontmatter(input);
 // The leading frontmatter block goes. A --- inside the body is a horizontal
 // rule that ruleBlock() uses to find the rule section, so it must survive.
 assert.ok(!result.includes('name: test'));
 assert.ok(!result.startsWith('---'));
 assert.ok(result.includes('Some content'));
 assert.ok(result.includes('More content'));
 });

 it('should return original if no frontmatter', () => {
 const input = 'Just some content';
 const result = stripFrontmatter(input);
 assert.strictEqual(result, input);
 });
});

describe('ruleBlock', () => {
 it('should extract content between --- markers', () => {
 const input = `# Title

Some intro text.

---
Rule block content here.
More rule content.
---

## Word-budget version

Tiny version`;
 const result = ruleBlock(input);
 assert.ok(result.includes('Rule block content'));
 assert.ok(result.includes('More rule content'));
 assert.ok(!result.includes('Title'));
 });
});

describe('buildContext', () => {
 it('should return FALLBACK_CONTEXT for empty input', () => {
 const result = buildContext('');
 assert.strictEqual(result, FALLBACK_CONTEXT);
 });

 it('should include HEADER in output', () => {
 const result = buildContext('# Simple English\n\n---\nRules here\n---');
 assert.ok(result.includes('SIMPLE ENGLISH SKILL ACTIVE'));
 });

 it('should truncate long content and use fallback', () => {
 const longContent = 'x'.repeat(MAX_CHARS * 2);
 const result = buildContext(longContent);
 assert.strictEqual(result, FALLBACK_CONTEXT);
 });
});

describe('promptCandidates', () => {
 it('should return an array of paths', () => {
 const candidates = promptCandidates('/plugin/root', '/hook/dir');
 assert.ok(Array.isArray(candidates));
 assert.ok(candidates.length > 0);
 assert.strictEqual(typeof candidates[0], 'string');
 });
});

describe('readFirstFile', () => {
 it('should return empty string for non-existent paths', () => {
 const result = readFirstFile(['/nonexistent/file.md']);
 assert.strictEqual(result, '');
 });
});

console.log('Running tests...');
