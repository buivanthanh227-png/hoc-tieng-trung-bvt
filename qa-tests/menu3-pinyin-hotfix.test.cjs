'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const patchPath = path.join(__dirname, '..', 'menu3-pinyin-fix-v42.10.22.1.js');
const patch = fs.readFileSync(patchPath, 'utf8');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

test('Menu 3 runtime is loaded directly by the application HTML', () => {
  assert.match(html, /id="bvt-v421023-menu3-runtime"/);
  assert.match(html, /menu3-pinyin-fix-v42\.10\.22\.1\.js\?v=42\.10\.23/);
});

test('Menu 3 hotfix does not replace the verified Menu 18-derived Pinyin mapper', () => {
  assert.doesNotMatch(patch, /window\.pinyinToChineseCandidates\s*=/);
  assert.doesNotMatch(patch, /window\.composePinyinSentence3x\s*=/);
  assert.doesNotMatch(patch, /function\s+(?:composeSentence|composeAll|segmentToken|buildInputOptions)\s*\(/);
  assert.match(html, /function pinyin18SyllablePaths\(raw,syllables\)/);
  assert.match(html, /function pinyin18SelectToneDiverse\(candidates,raw,limit=16\)/);
  assert.match(html, /return pinyin18SelectToneDiverse\(\[\.\.\.found\.values\(\)\],raw,found\.size\);/);
});

test('global press feedback is registered for pointer and keyboard interaction', () => {
  const listeners = {};
  const styleNodes = [];
  const document = {
    documentElement: { dataset: {} },
    head: { appendChild(node) { styleNodes.push(node); } },
    createElement(tag) { return { tag, id: '', textContent: '' }; },
    addEventListener(type, callback) { (listeners[type] ||= []).push(callback); },
    getElementById() { return null; }
  };
  const context = vm.createContext({
    document,
    window: { setTimeout(callback) { callback(); } },
    console
  });
  context.window = context.window;
  vm.runInContext(patch, context, { timeout: 10000 });

  assert.equal(styleNodes.length, 1);
  assert.match(styleNodes[0].textContent, /\.bvt-press-active/);
  for (const eventName of ['pointerdown', 'pointerup', 'pointercancel', 'keydown', 'keyup']) {
    assert.ok(listeners[eventName]?.length, eventName + ' listener must be installed');
  }

  const classes = new Set();
  const element = {
    disabled: false,
    classList: {
      add(value) { classes.add(value); },
      remove(value) { classes.delete(value); }
    },
    getAttribute() { return null; },
    closest() { return this; }
  };
  listeners.pointerdown[0]({ target: element, pointerId: 1 });
  assert.ok(classes.has('bvt-press-active'), 'pointerdown immediately depresses the control');
  listeners.pointerup[0]({ target: element, pointerId: 1 });
  assert.ok(!classes.has('bvt-press-active'), 'pointerup releases the control');
});
