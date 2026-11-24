'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const runtime = fs.readFileSync(path.join(__dirname, '..', 'menu3-pinyin-fix-v42.10.23.js'), 'utf8');

function getSpeakText() {
  const start = runtime.indexOf('const speakText=(value,locale)=>{');
  const end = runtime.indexOf('window.openHomework3xCandidateModal=', start);
  assert.notEqual(start, -1, 'Menu 3 speakText must exist');
  assert.notEqual(end, -1, 'Menu 3 modal must follow speakText');
  return runtime.slice(start, end).replace('const speakText=', 'globalThis.__speakText=').trim();
}

function bootSpeech() {
  const spoken = [];
  let cancelCalls = 0;
  class FakeUtterance {
    constructor(text) { this.text = text; }
  }
  const synth = {
    cancel() { cancelCalls++; },
    speak(utterance) { spoken.push(utterance); },
    getVoices() { return []; }
  };
  const window = { speechSynthesis: synth };
  const context = vm.createContext({ window, SpeechSynthesisUtterance: FakeUtterance });
  vm.runInContext(getSpeakText(), context);
  return { speak: context.__speakText, spoken, getCancelCalls: () => cancelCalls };
}

test('Vietnamese pronunciation preserves the initial X in Xin chào', () => {
  const { speak, spoken, getCancelCalls } = bootSpeech();
  speak('Xin chào', 'vi');
  assert.equal(spoken.length, 1);
  assert.equal(spoken[0].text, 'Xin chào');
  assert.equal(spoken[0].lang, 'vi-VN');
  assert.equal(getCancelCalls(), 1);
});

test('Chinese pronunciation sends only the selected Hanzi text', () => {
  const { speak, spoken, getCancelCalls } = bootSpeech();
  speak('你好', 'zh');
  assert.equal(spoken.length, 1);
  assert.equal(spoken[0].text, '你好');
  assert.equal(spoken[0].lang, 'zh-CN');
  assert.equal(getCancelCalls(), 1);
});

test('only actual zero-width characters are removed; ordinary letters remain intact', () => {
  const { speak, spoken } = bootSpeech();
  speak('Xin\u200B chào\u200D', 'vi');
  assert.equal(spoken[0].text, 'Xin chào');
});

test('modal speech controls use a private data attribute, isolated from the page-wide data-speak listener', () => {
  const start = runtime.indexOf('window.openHomework3xCandidateModal=function');
  const end = runtime.indexOf('/* Let a newer lookup supersede', start);
  assert.notEqual(start, -1);
  assert.notEqual(end, -1);
  const modal = runtime.slice(start, end);

  assert.match(modal, /data-menu3-speak="zh"/);
  assert.match(modal, /data-menu3-speak="vi"/);
  assert.match(modal, /querySelectorAll\('\[data-menu3-speak\]'\)/);
  assert.match(modal, /button\.dataset\.menu3Speak==='zh'\?values\.hanzi:values\.meaning/);
  assert.doesNotMatch(modal, /data-speak=/);
  assert.doesNotMatch(modal, /querySelectorAll\('\[data-speak\]'\)/);
});
