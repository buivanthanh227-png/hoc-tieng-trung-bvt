'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const runtime = fs.readFileSync(path.join(root, 'menu3-pinyin-fix-v42.10.23.js'), 'utf8');

function extract(start, end) {
  const from = html.indexOf(start);
  const to = html.indexOf(end, from + start.length);
  assert.notEqual(from, -1, `missing source start: ${start}`);
  assert.notEqual(to, -1, `missing source end: ${end}`);
  return html.slice(from, to);
}

function boot({ forceTimeout = false } = {}) {
  const syllables = new Set(['ni', 'hao']);
  const status = { textContent: '' };
  const cards = [];
  const document = {
    documentElement: { dataset: {} },
    head: { appendChild() {} },
    createElement() { return { style: {}, classList: { add() {}, remove() {} }, setAttribute() {} }; },
    addEventListener() {},
    getElementById() { return null; },
    querySelector() { return null; }
  };
  const context = vm.createContext({
    document,
    navigator: {},
    console,
    Map,
    Set,
    setTimeout(callback, delay) {
      if (forceTimeout && delay === 15000) queueMicrotask(callback);
      return 1;
    },
    clearTimeout() {}
  });
  context.window = context;
  context.pinyin18Key = value => String(value || '').normalize('NFD').toLowerCase()
    .replace(/u\u0308/g, 'v').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z]/g, '');
  context.getPinyin18SourceIndex = () => ({ syllables });
  context.$ = () => status;
  context.renderHomework3xCard = item => cards.push(item);
  context.homework3xLookupToken = 17;
  vm.runInContext(runtime, context, { timeout: 10000 });
  vm.runInContext(extract(
    'async function acceptPinyinComposition3x(option,lookupToken){',
    'function renderPinyinCompositionOptions3x('
  ), context, { timeout: 10000 });
  return { context, status, cards };
}

const option = { zh: '你好', py: 'nǐ hǎo' };

test('composition translation success renders only the validated Vietnamese meaning', async () => {
  const { context, status, cards } = boot();
  context.machineTranslate3x = async () => ({ text: 'Xin chào.', provider: 'test translator' });
  await context.acceptPinyinComposition3x(option, 17);
  assert.equal(cards.length, 1);
  assert.equal(cards[0].vi, 'Xin chào.');
  assert.match(status.textContent, /xác minh nghĩa tiếng Việt/i);
});

test('composition translation failure does not render a fake Vietnamese meaning', async () => {
  const { context, status, cards } = boot();
  context.machineTranslate3x = async () => { throw new Error('network failed'); };
  await context.acceptPinyinComposition3x(option, 17);
  assert.equal(cards.length, 0);
  assert.match(status.textContent, /Không thể xác minh nghĩa tiếng Việt/i);
  assert.doesNotMatch(status.textContent, /Đang tra nghĩa|chưa lấy được nghĩa/i);
});

test('composition translation timeout does not render a result card', async () => {
  const { context, status, cards } = boot({ forceTimeout: true });
  context.machineTranslate3x = () => new Promise(() => {});
  await context.acceptPinyinComposition3x(option, 17);
  assert.equal(cards.length, 0);
  assert.match(status.textContent, /Không thể xác minh nghĩa tiếng Việt/i);
});

test('placeholder, error text, empty text and Pinyin echo are rejected as meanings', async () => {
  const invalid = [
    '',
    'Đang tra nghĩa tiếng Việt…',
    'Đã chuyển Pinyin sang chữ Hán; hiện chưa lấy được nghĩa tiếng Việt.',
    'Translation failed',
    'No translation found',
    'Error: service unavailable',
    'Hello world.',
    'nǐ hǎo'
  ];
  for (const text of invalid) {
    const { context, status, cards } = boot();
    context.machineTranslate3x = async () => ({ text, provider: 'test translator' });
    await context.acceptPinyinComposition3x(option, 17);
    assert.equal(cards.length, 0, `${JSON.stringify(text)} must not render as a meaning`);
    assert.match(status.textContent, /Không thể xác minh nghĩa tiếng Việt/i);
  }
});

test('an already-valid composition meaning is preserved without calling translation', async () => {
  const { context, cards } = boot();
  let calls = 0;
  context.machineTranslate3x = async () => { calls++; return { text: 'not used' }; };
  await context.acceptPinyinComposition3x({ ...option, vi: 'Xin chào.' }, 17);
  assert.equal(calls, 0);
  assert.equal(cards.length, 1);
  assert.equal(cards[0].vi, 'Xin chào.');
});

test('unaccented but recognizably Vietnamese text remains a valid meaning', async () => {
  const { context, cards } = boot();
  context.machineTranslate3x = async () => ({ text: 'Toi thich uong tra.' });
  await context.acceptPinyinComposition3x(option, 17);
  assert.equal(cards.length, 1);
  assert.equal(cards[0].vi, 'Toi thich uong tra.');
});

test('the exact Vietnamese verification failure notice is rejected as a meaning', () => {
  const { context } = boot();
  assert.equal(context.isValidHomework3xMeaning(
    'Không thể xác minh nghĩa tiếng Việt; kết quả chưa được hiển thị. Vui lòng thử lại.', option.py
  ), false);
});

test('Vietnamese status messages with diacritics are rejected as meanings', () => {
  const { context } = boot();
  const statuses = [
    'Không thể xác minh nghĩa tiếng Việt; kết quả chưa được hiển thị. Vui lòng thử lại.',
    'Đang xử lý bản dịch, vui lòng chờ trong giây lát.',
    'Đã nhận diện Pinyin và xác minh nghĩa tiếng Việt.',
    'Dịch vụ hiện không khả dụng, vui lòng thử lại sau.'
  ];
  for (const text of statuses) {
    assert.equal(context.isValidHomework3xMeaning(text, option.py), false, `${text} must be rejected`);
  }
});

test('French and Spanish text with accents are not accepted as Vietnamese meanings', () => {
  const { context } = boot();
  for (const text of ['Très bon, merci.', 'El niño está aquí.', 'La niña es muy feliz.']) {
    assert.equal(context.isValidHomework3xMeaning(text, option.py), false, `${text} must be rejected`);
  }
});

test('a late onStage callback after timeout cannot overwrite the final timeout status', async () => {
  const { context, status, cards } = boot({ forceTimeout: true });
  let lateStage;
  context.machineTranslate3x = (_text, _source, _target, options) => {
    lateStage = options.onStage;
    return new Promise(() => {});
  };
  await context.acceptPinyinComposition3x(option, 17);
  const finalStatus = status.textContent;
  assert.match(finalStatus, /Không thể xác minh nghĩa tiếng Việt/i);
  lateStage('Đang dịch rất tốt…');
  assert.equal(status.textContent, finalStatus);
  assert.equal(cards.length, 0);
});

test('an onStage callback after successful completion cannot overwrite the final success status', async () => {
  const { context, status, cards } = boot();
  let lateStage;
  context.machineTranslate3x = async (_text, _source, _target, options) => {
    lateStage = options.onStage;
    return { text: 'Xin chào.', provider: 'test translator' };
  };
  await context.acceptPinyinComposition3x(option, 17);
  const finalStatus = status.textContent;
  lateStage('Đang dịch…');
  assert.equal(status.textContent, finalStatus);
  assert.equal(cards.length, 1);
  assert.equal(cards[0].vi, 'Xin chào.');
});

test('a callback from a previous lookup cannot affect the newer query status', async () => {
  const { context, status, cards } = boot({ forceTimeout: true });
  let oldStage;
  context.machineTranslate3x = (_text, _source, _target, options) => {
    oldStage = options.onStage;
    return new Promise(() => {});
  };
  const oldOperation = context.acceptPinyinComposition3x(option, 17);
  context.homework3xLookupToken = 18;
  status.textContent = 'Đang xử lý truy vấn mới.';
  oldStage('Đang dịch rất tốt…');
  assert.equal(status.textContent, 'Đang xử lý truy vấn mới.');
  await oldOperation;
  assert.equal(cards.length, 0);
});
