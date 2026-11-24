'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const dictionaryMatch = html.match(/<script id="embedded-cvdict-data"[^>]*>([\s\S]*?)<\/script>/);
assert.ok(dictionaryMatch, 'Embedded CVDICT data must be present');
const dictionary = JSON.parse(dictionaryMatch[1]);
const algorithmStart = html.indexOf('function pinyin18ToneFromInput(value){');
const algorithmEnd = html.indexOf('async function machineTranslate(text,source,target){', algorithmStart);
assert.ok(algorithmStart >= 0 && algorithmEnd > algorithmStart, 'Menu 3 source matcher must be present');

const context = vm.createContext({
  dictionary,
  buildSeed: () => dictionary,
  pinyinForChinese: () => '',
  MENU18_VERIFIED_SENTENCES: [],
  sentenceDeck: [],
  OFFLINE_SENTENCE_TRANSLATIONS: {}
});
context.window = context;
vm.runInContext(html.slice(algorithmStart, algorithmEnd), context, { timeout: 10000 });

function candidates(query) {
  return JSON.parse(JSON.stringify(context.pinyinToChineseCandidates(query)));
}

test('nǐ hǎo and ni hao return only the complete dictionary entry', () => {
  for (const query of ['nǐ hǎo', 'ni hao', 'ni3 hao3', 'ni3hao3', 'nǐhǎo']) {
    const results = candidates(query);
    assert.equal(results.length, 1, query);
    assert.equal(results[0].zh, '你好');
    assert.equal(results[0].py, 'nǐ hǎo');
    assert.match(results[0].vi, /xin chào/i);
    assert.equal(results[0].sourceRows[0][0], results[0].zh);
    assert.equal(results[0].sourceRows[0][2], results[0].py);
  }
});

test('dictionary-only matching does not compose unsupported syllable combinations', () => {
  const results = candidates('ni hao');
  const hanzi = new Set(results.map(item => item.zh));
  for (const unsupported of ['倪好', '拟好', '你壕', '你嗥', '你嚎']) {
    assert.equal(hanzi.has(unsupported), false, unsupported);
  }
  assert.equal(candidates('nǐ hāo').length, 0);
  assert.equal(candidates('zzqx').length, 0);
});

test('all source matches survive without a beam cap and retain unique source readings', () => {
  const results = candidates('yi');
  const ids = results.map(item => `${item.zh}|${item.py}`);
  assert.ok(results.length > 128, `Expected all source matches; got ${results.length}`);
  assert.equal(new Set(ids).size, ids.length);
  assert.ok(results.every(item =>
    item.sourceRows.length === 1 &&
    item.sourceRows[0][0] === item.zh &&
    item.sourceRows[0][2] === item.py &&
    item.vi.length > 0
  ));
});

test('explicit tones filter source readings without rewriting the source Pinyin', () => {
  const unmarked = candidates('yi');
  const thirdTone = candidates('yǐ');
  assert.ok(unmarked.some(item => item.zh === '一'));
  assert.ok(thirdTone.some(item => item.zh === '已'));
  assert.ok(thirdTone.every(item => context.pinyin18ToneFromInput(item.py) === 3));
});

test('compact Pinyin is segmented with dynamic programming from source syllables', () => {
  const syllables = context.getPinyin18SourceIndex().syllables;
  assert.equal(context.pinyin18CanSegment('nǐhǎo', syllables), true);
  assert.equal(context.pinyin18CanSegment('zzqx', syllables), false);
});

test('ambiguous compact segmentation returns source readings with original spacing', () => {
  const compact = candidates('xian');
  const separated = candidates('xi an');
  const compactIds = compact.map(item => `${item.zh}|${item.py}`).sort();
  const separatedIds = separated.map(item => `${item.zh}|${item.py}`).sort();
  assert.ok(compact.some(item => item.py.trim().split(/\s+/).length > 1));
  assert.ok(compact.some(item => item.py.trim().split(/\s+/).length === 1));
  assert.deepEqual(separatedIds, compactIds);
});

test('compact common words resolve through complete source dictionary readings', () => {
  const cases = [
    ['jintian', '今天', 2],
    ['zuotian', '昨天', 2],
    ['xihuan', '喜欢', 2]
  ];
  for (const [query, expectedHanzi, syllableCount] of cases) {
    const results = candidates(query);
    const match = results.find(item => item.zh === expectedHanzi);
    assert.ok(match, query + ' must retain the complete dictionary word ' + expectedHanzi);
    if (match.sourceRows?.length) {
      assert.equal(match.sourceRows[0][0], expectedHanzi);
      assert.equal(match.sourceRows[0][2], match.py);
    } else {
      assert.match(String(match.source || ''), /ưu tiên|xác minh|CVDICT/i);
    }
    assert.equal(match.py.trim().split(/\s+/).length, syllableCount);
    assert.ok(results.length <= 16, query + ' must not explode into dozens of component combinations');
  }
});

test('Menu 3 applies Menu 18 tone positions and shortest segmentation to compact words', () => {
  for (const [query, hanzi, expectedCount] of [
    ['jintian', '今天', 2],
    ['zuotian', '昨天', 2],
    ['xihuan', '喜欢', 2]
  ]) {
    const all = candidates(query);
    const selected = context.pinyin18SelectToneDiverse(all, query, 30);
    const match = selected.find(item => item.zh === hanzi);
    assert.ok(match, query + ' must retain its preferred whole word');
    assert.equal(match.py.trim().split(/\s+/).length, expectedCount);
  }
  const like = context.pinyin18SelectToneDiverse(candidates('xihuan'), 'xihuan', 30)
    .find(item => item.zh === '喜欢');
  const syllables = like.py.trim().split(/\s+/);
  assert.equal(context.pinyin18ToneFromInput(syllables[0]), 3,
    '喜欢 must carry third tone on xi');
  assert.notEqual(context.pinyin18ToneFromInput(syllables[1]), 3,
    'huan must not be assigned third tone in 喜欢');
});

test('whole-sentence candidate meanings are not assembled from isolated gloss fragments', () => {
  const results = candidates('wo bu xihuan ta');
  for (const item of results) {
    if (item.sourceRows?.length === 1) {
      assert.equal(item.sourceRows[0][0], item.zh);
      assert.equal(item.sourceRows[0][2], item.py);
    } else if (item.sourceRows?.length > 1) {
      assert.equal(item.vi, '',
        'multi-entry sentence composition must not concatenate isolated Vietnamese glosses');
    }
  }
});

test('Menu 3 lookup delegates to complete 10-per-page results with sentence-level meanings', () => {
  const runtime = fs.readFileSync(path.join(__dirname, '..', 'menu3-pinyin-fix-v42.10.23.js'), 'utf8');
  const renderStart = html.indexOf('async function renderHomework3xCandidates(candidates){');
  const renderEnd = html.indexOf('function looksLikeVietnamese3x(raw){', renderStart);
  assert.ok(renderStart >= 0 && renderEnd > renderStart);
  assert.match(html.slice(renderStart, renderEnd), /window\.renderHomework3xCandidatesV421023/);
  assert.match(runtime, /const pageSize=10/);
  assert.match(runtime, /window\.machineTranslate3x\(String\(item\.zh\),'zh-CN','vi'\)/);
  assert.match(runtime, /window\.openHomework3xCandidateModal\(item,index,complete\.length\)/);
  // The runtime preserves the exact user token boundaries while applying
  // dictionary tone marks to the source syllable group; it no longer pushes
  // the unformatted source slice directly.
  assert.match(runtime, /const sourceGroup=syllables\.slice\(at,at\+selected\.length\)/);
  assert.match(runtime, /groups\.push\(menu3FormatWord\(match\[0\],sourceGroup\.join\(''\)\)\)/);
  assert.doesNotMatch(runtime, /Chọn để dịch nghĩa/);
});
