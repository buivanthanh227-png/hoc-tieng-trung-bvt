'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const dictionary = JSON.parse(html.match(/<script id="embedded-cvdict-data"[^>]*>([\s\S]*?)<\/script>/)[1]);

function sliceBetween(startMarker, endMarker) {
  const start = html.indexOf(startMarker);
  const end = html.indexOf(endMarker, start + startMarker.length);
  if (start < 0 || end < 0) throw new Error('Missing slice: ' + startMarker);
  return html.slice(start, end);
}

function boot() {
  const document = {
    documentElement: { dataset: {} },
    createElement() { return { appendChild() {}, classList: { add() {}, remove() {} }, style: {}, addEventListener() {}, dataset: {} }; },
    head: { appendChild() {} },
    getElementById() { return null; },
    addEventListener() {},
    querySelector() { return null; }
  };
  const context = {
    dictionary,
    document,
    console,
    MENU18_VERIFIED_SENTENCES: [],
    OFFLINE_SENTENCE_TRANSLATIONS: {},
    navigator: {},
    isSecureContext: true,
    setTimeout(cb) { return 0; },
    bvtSpeakLocale() {}
  };
  context.window = context;
  vm.createContext(context);
  vm.runInContext([
    sliceBetween('const seed = [', 'const roleHints'),
    sliceBetween('const sentenceDeck = [', 'function hskFromSeed'),
    sliceBetween('const extraSeed = [', 'function buildSeed'),
    sliceBetween('function pinyin18ToneFromInput(value){', 'async function machineTranslate(text,source,target){'),
    sliceBetween('function looksLikeVietnamese3x(raw){', 'async function machineTranslate3x(text,source,target,options={}){'),
    sliceBetween('function looksLikePinyin3x(raw,local){', 'async function acceptPinyinComposition3x(')
  ].join('\n'), context, { timeout: 20000 });
  vm.runInContext(fs.readFileSync(path.join(root, 'menu3-pinyin-fix-v42.10.23.js'), 'utf8'), context, { timeout: 20000 });
  return context;
}

const context = boot();

test('valid invitation and known sentences produce natural Vietnamese', () => {
  const invite = context.menu3AnalyzeSentence('zuotian ni qing wo he cha le');
  assert.ok(invite.length > 0);
  assert.equal(invite[0].zh, '昨天你请我喝茶了');
  assert.match(invite[0].vi, /mời/);

  const love = context.menu3AnalyzeSentence('wo ai ni');
  assert.ok(love.some(r => r.zh === '我爱你' && /yêu/.test(r.vi)));

  const drink = context.menu3AnalyzeSentence('jintian wo he cha le');
  assert.ok(drink.some(r => /trà/.test(r.vi)));
});

test('invalid structures produce no meaning', () => {
  for (const bad of ['wo cha', 'wo pingguo', 'jintian wo cha le', 'ni qing wo cha le']) {
    const rows = context.menu3AnalyzeSentence(bad);
    assert.equal(rows.length, 0, bad + ' should produce no meaning');
  }
});

test('and-construction and fallback still work', () => {
  const together = context.menu3AnalyzeSentence('wo he ni');
  assert.ok(together.some(r => r.zh === '我和你' && /và/.test(r.vi)));
});


test('unmarked ni xihuan he cha ma composes a grammatical Vietnamese question', () => {
  const rows = context.menu3AnalyzeSentence('ni xihuan he cha ma');
  const expected = rows.find(row => row.zh === '你喜欢喝茶吗');
  assert.ok(expected, 'must compose 你 + 喜欢 + 喝 + 茶 + 吗 from dictionary entries');
  assert.match(expected.vi, /^Bạn thích uống trà không\?$/i);
  assert.equal(
    context.formatByInputSpacing('ni xihuan he cha ma', 'nǐ xǐ huan hē chá ma'),
    'nǐ xǐhuan hē chá ma',
    'must preserve the five user-entered space-delimited groups'
  );
});
