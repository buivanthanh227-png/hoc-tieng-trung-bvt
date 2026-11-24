'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const runtime = fs.readFileSync(path.join(root, 'menu3-pinyin-fix-v42.10.23.js'), 'utf8');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');

class Element {
  constructor(tagName = 'div') {
    this.tagName = tagName.toUpperCase();
    this.children = [];
    this.style = {};
    this.dataset = {};
    this.classList = { add() {}, remove() {} };
    this.listeners = {};
    this.hidden = false;
    this.disabled = false;
    this._text = '';
    this._html = '';
  }
  set textContent(value) { this._text = String(value ?? ''); this.children = []; }
  get textContent() { return this._text + this.children.map(child => child.textContent).join(''); }
  set innerHTML(value) {
    this._html = String(value);
    this.children = [];
    if (this._html.includes('data-page-prev')) {
      const previous = new Element('button');
      previous.dataset.pagePrev = '';
      const next = new Element('button');
      next.dataset.pageNext = '';
      this.children = [previous, next];
    }
  }
  get innerHTML() { return this._html; }
  append(...nodes) { this.children.push(...nodes); }
  appendChild(node) { this.children.push(node); return node; }
  replaceChildren(...nodes) { this.children = nodes; }
  addEventListener(type, listener) { (this.listeners[type] ||= []).push(listener); }
  dispatch(type, event = {}) { for (const listener of this.listeners[type] || []) listener(event); }
  querySelector(selector) {
    if (selector === '[data-page-prev]') return this.children.find(child => 'pagePrev' in child.dataset) || null;
    if (selector === '[data-page-next]') return this.children.find(child => 'pageNext' in child.dataset) || null;
    return null;
  }
}

function boot({ withLookup = false } = {}) {
  const host = new Element();
  const status = new Element();
  const input = new Element('input');
  const lookupButton = new Element('button');
  const ids = {
    'homework3x-candidates': host,
    'homework3x-status': status,
    'homework3x-query': input,
    'homework3x-lookup': lookupButton
  };
  const document = {
    documentElement: { dataset: {} },
    head: { appendChild() {} },
    body: { style: {}, appendChild() {} },
    createElement(tag) { return new Element(tag); },
    addEventListener() {},
    getElementById(id) { return ids[id] || null; },
    querySelector() { return null; }
  };
  const window = {
    pinyin18Key(value) {
      return String(value || '').normalize('NFD').toLowerCase()
        .replace(/u\u0308/g, 'v').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z]/g, '');
    },
    getPinyin18SourceIndex() { return { syllables: new Set(['wo', 'ai', 'ni', 'nihao', 'xin', 'hao']) }; },
    pinyin18SelectToneDiverse(items) { return items; }
  };
  const context = vm.createContext({ window, document, navigator: {}, console, Map, Set, setTimeout, clearTimeout });
  if (withLookup) {
    context.homework3xLookupToken = 0;
    window.lookupHomework3x = async () => {};
    window.menu3AnalyzeSentence = () => [];
  }
  vm.runInContext(runtime, context, { timeout: 10000 });
  return { context, window, document, host, status, input, lookupButton };
}

function candidateButtons(host) {
  const grid = host.children.find(child => child.className === 'homework3x-candidate-grid');
  return grid ? grid.children : [];
}

test('prevalidated candidates render as numbered complete results and every result routes to the same modal', async () => {
  const { window, host } = boot();
  const opened = [];
  window.openHomework3xCandidateModal = (...args) => opened.push(args);
  await window.renderHomework3xCandidatesV421023([
    { zh: '我爱你', py: 'wǒ ài nǐ', vi: 'Tôi yêu bạn.' },
    { zh: '你好', py: 'nǐ hǎo', vi: 'Xin chào.' }
  ]);
  const buttons = candidateButtons(host);
  assert.equal(buttons.length, 2);
  for (const [index, button] of buttons.entries()) {
    assert.equal(button.children[0].textContent, String(index + 1));
    const [pinyin, hanzi, meaning] = button.children[1].children;
    assert.ok(pinyin.textContent);
    assert.ok(hanzi.textContent);
    assert.ok(meaning.textContent);
    button.dispatch('click', { preventDefault() {}, stopPropagation() {} });
  }
  assert.deepEqual(opened.map(call => [call[1], call[2]]), [[0, 2], [1, 2]]);
  assert.match(host.children.find(child => child.className === 'homework3x-candidate-grid').textContent, /Tôi yêu bạn\./);
});

test('a missing meaning is translated before a candidate becomes visible', async () => {
  const { window, host, status } = boot();
  let finishTranslation;
  let translationCalls = 0;
  window.machineTranslate3x = () => {
    translationCalls++;
    return new Promise(resolve => { finishTranslation = resolve; });
  };
  const rendering = window.renderHomework3xCandidatesV421023([
    { zh: '我爱你', py: 'wǒ ài nǐ', vi: '' }
  ]);
  assert.match(status.textContent, /Đang hoàn thiện nghĩa tiếng Việt/i);
  assert.equal(candidateButtons(host).length, 0, 'unfinished candidates must not be shown');
  assert.equal(translationCalls, 1);
  finishTranslation({ text: 'Tôi yêu bạn.' });
  await rendering;
  const buttons = candidateButtons(host);
  assert.equal(buttons.length, 1);
  assert.equal(buttons[0].children[0].textContent, '1');
  assert.equal(buttons[0].children[1].children[2].textContent, 'Tôi yêu bạn.');
});

test('translation failure drops only the invalid candidate and retains verified meanings', async () => {
  const { window, host, status } = boot();
  window.machineTranslate3x = async hanzi => {
    if (hanzi === '坏') throw new Error('offline');
    return { text: 'Tôi yêu bạn.' };
  };
  await window.renderHomework3xCandidatesV421023([
    { zh: '你好', py: 'nǐ hǎo', vi: 'Xin chào.' },
    { zh: '坏', py: 'huài', vi: '' }
  ]);
  const buttons = candidateButtons(host);
  assert.equal(buttons.length, 1);
  assert.equal(buttons[0].children[0].textContent, '1');
  assert.match(buttons[0].textContent, /Xin chào\./);
  assert.doesNotMatch(host.textContent, /offline|Đang dịch|Chọn để dịch nghĩa/);
  assert.match(status.textContent, /1 kết quả hợp lệ/i);
});

test('direct card bridge and ambiguous composition branch both use the unified renderer', () => {
  const cardBlock = html.slice(html.indexOf('async function renderHomework3xCard('), html.indexOf('let homework3xCandidates=[];'));
  const ambiguousBlock = html.slice(html.indexOf('async function renderPinyinCompositionOptions3x('), html.indexOf('let homework3xLookupToken=0;'));
  assert.match(cardBlock, /return await renderer\(\[item\]\)/);
  assert.doesNotMatch(cardBlock, /homework3x-output-row|innerHTML/);
  assert.match(ambiguousBlock, /await renderer\(Array\.isArray\(options\)\?options:\[\]\)/);
  assert.doesNotMatch(ambiguousBlock, /Chọn để dịch nghĩa|addEventListener\('click'/);
  assert.doesNotMatch(html, /if\(!best\)\{status\.textContent='Chưa tìm được cách ghép Pinyin phù hợp\.'/);
  assert.match(html, /await renderPinyinCompositionOptions3x\(composed\.options,token\)/);
  assert.match(html, /await renderHomework3xCard\(local,local\.source\)/);
  assert.match(html, /await renderHomework3xCard\(\{zh:raw,py:pinyinForChinese\(raw\),vi:translated/);
});

test('new lookup request invalidates old renderer work and keeps the newest result', async () => {
  const { window, input, host } = boot({ withLookup: true });
  const resolvers = {};
  window.menu3AnalyzeSentence = query => [{ zh: query, py: 'nǐ hǎo', vi: '' }];
  window.machineTranslate3x = hanzi => new Promise(resolve => { resolvers[hanzi] = resolve; });
  input.value = 'old';
  const oldRequest = window.lookupHomework3x();
  input.value = 'new';
  const newRequest = window.lookupHomework3x();
  resolvers.new({ text: 'Xin chào.' });
  await newRequest;
  resolvers.old({ text: 'Tôi yêu bạn.' });
  await oldRequest;
  const buttons = candidateButtons(host);
  assert.equal(buttons.length, 1);
  assert.equal(buttons[0].children[1].children[1].textContent, 'new');
  assert.equal(buttons[0].children[1].children[2].textContent, 'Xin chào.');
});
