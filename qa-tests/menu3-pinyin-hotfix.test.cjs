'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const patchPath = path.join(__dirname, '..', 'menu3-pinyin-fix-v42.10.22.1.js');
const patch = fs.readFileSync(patchPath, 'utf8');

function createHarness() {
  const rows = [
    ['今天', '今天', 'jīn tiān', '· hôm nay', 'HSK1'],
    ['我', '我', 'wǒ', 'tôi; mình', 'HSK1'],
    ['请', '請', 'qǐng', '· mời; xin', 'HSK1'],
    ['你', '你', 'nǐ', 'bạn', 'HSK1'],
    ['喝茶', '喝茶', 'hē chá', '· uống trà', '']
  ];
  const entries = rows.map((row, index) => ({
    zh: row[0], trad: row[1], py: row[2], vi: row[3],
    source: 'CVDICT', priority: 100, rowIndex: index, sourceRows: [row]
  }));
  const sourceIndex = {
    syllables: new Set(['jin', 'tian', 'wo', 'qing', 'ni', 'he', 'cha']),
    entries
  };

  const document = {
    getElementById(id) { return id === 'homework3x-query' ? {} : null; },
    querySelector(selector) {
      if (selector === '#panel-translate3 .quick-translate-intro') return { textContent: '' };
      if (selector === 'title') return { textContent: 'HỌC TIẾNG TRUNG · V42.10.22' };
      if (selector === '.bvt-footer-version-row-v2 strong') return { textContent: 'Phiên bản V42.10.22' };
      return null;
    },
    documentElement: { dataset: {} }
  };

  const context = vm.createContext({
    document,
    console,
    getPinyin18SourceIndex: () => sourceIndex,
    homework3xValidVietnameseMeaning: () => true,
    pinyin18Key(value) {
      return String(value || '').normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '').replace(/[üÜvV]/g, 'u')
        .replace(/[1-5]/g, '').toLowerCase().replace(/[^a-z]/g, '');
    },
    pinyin18InputToken(value) {
      const normalized = String(value || '').normalize('NFD').toLowerCase();
      const tones = [];
      let base = '', lastBaseIndex = -1;
      for (const char of normalized) {
        if (/[a-z]/.test(char)) {
          base += char === 'v' ? 'u' : char;
          lastBaseIndex = base.length - 1;
          continue;
        }
        if (char === '\u0304') tones.push({ offset: lastBaseIndex, tone: 1, numeric: false });
        else if (char === '\u0301') tones.push({ offset: lastBaseIndex, tone: 2, numeric: false });
        else if (char === '\u030c') tones.push({ offset: lastBaseIndex, tone: 3, numeric: false });
        else if (char === '\u0300') tones.push({ offset: lastBaseIndex, tone: 4, numeric: false });
        else if (/[1-5]/.test(char)) tones.push({ offset: base.length, tone: Number(char), numeric: true });
      }
      return { base: this.pinyin18Key(value), tones };
    },
    pinyin18ToneFromInput(value) {
      const token = String(value || '').trim().toLowerCase();
      const numbered = token.match(/([1-5])$/);
      if (numbered) return Number(numbered[1]);
      const marks = token.normalize('NFD');
      if (marks.includes('\u0304')) return 1;
      if (marks.includes('\u0301')) return 2;
      if (marks.includes('\u030c')) return 3;
      if (marks.includes('\u0300')) return 4;
      return null;
    },
    pinyin18InputInfosMatchSource(item, input) {
      const sourceTokens = String(item.py || '').split(/\s+/).filter(Boolean);
      const sourceMarks = [];
      let sourceOffset = 0;
      if (!input.length || !sourceTokens.length || input.some(token => !token.base)) return false;
      for (const rawToken of sourceTokens) {
        const parsed = this.pinyin18InputToken(rawToken);
        if (!parsed.base) return false;
        parsed.tones.forEach(mark => sourceMarks.push({ ...mark, offset: mark.offset + sourceOffset }));
        sourceOffset += parsed.base.length;
      }
      if (input.map(token => token.base).join('') !== sourceTokens.map(token => this.pinyin18Key(token)).join('')) return false;
      let offset = 0;
      for (const token of input) {
        const end = offset + token.base.length;
        const tones = sourceMarks.filter(mark => mark.offset >= offset && mark.offset < end);
        const sourceTone = tones.length ? tones[0].tone : null;
        for (const mark of token.tones) {
          if (mark.tone === 5 ? (sourceTone !== null && sourceTone !== 5) : sourceTone !== mark.tone) return false;
        }
        offset = end;
      }
      return true;
    }
  });
  context.window = context;
  vm.runInContext(
    'let pinyin3xComposerSourceIndex=null,pinyin3xComposerIndex=null;' +
    'const seed=[["今天","今天","jīn tiān","hôm nay","HSK1"],["我","我","wǒ","tôi","HSK1"],["请","請","qǐng","mời","HSK1"],["你","你","nǐ","bạn","HSK1"]];' +
    'const extraSeed=[];',
    context
  );
  vm.runInContext(patch, context, { timeout: 10000 });
  return context;
}

test('Menu 3 composes full sentence from dictionary phrases outside the HSK allowlist', () => {
  const app = createHarness();
  const result = app.composePinyinSentence3x('jintian wo qing ni he cha');
  assert.equal(result.status, 'ok');
  assert.equal(result.zh, '今天我请你喝茶');
  assert.equal(result.py, 'Jīntiān wǒ qǐng nǐ hē chá');
});

test('Menu 3 preserves original spaces and separators in displayed Pinyin', () => {
  const app = createHarness();
  const result = app.composePinyinSentence3x('jin tian  wo qing ni  he cha');
  assert.equal(result.status, 'ok');
  assert.equal(result.zh, '今天我请你喝茶');
  assert.equal(result.py, 'Jīn tiān  wǒ qǐng nǐ  hē chá');
});

test('Menu 3 preserves tone marks and numeric-tone input while composing', () => {
  const app = createHarness();
  const marked = app.composePinyinSentence3x('jīntiān wǒ qǐng nǐ hē chá');
  const numbered = app.composePinyinSentence3x('jin1tian1 wo3 qing3 ni3 he1 cha2');
  assert.equal(marked.status, 'ok');
  assert.equal(marked.zh, '今天我请你喝茶');
  assert.equal(numbered.status, 'ok');
  assert.equal(numbered.zh, '今天我请你喝茶');
  assert.equal(numbered.py, 'Jīntiān wǒ qǐng nǐ hē chá');
});

test('Menu 3 output formatter never rewrites Pinyin spacing', () => {
  const app = createHarness();
  assert.equal(app.formatHomework3xPinyinByWord('今天我请你喝茶', 'Jīn tiān  wǒ qǐng nǐ  hē chá'), 'Jīn tiān  wǒ qǐng nǐ  hē chá');
  assert.equal(app.document.documentElement.dataset.menu3PinyinFix, '42.10.22.1');
});
