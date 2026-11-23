'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const start = html.indexOf('function bvtNativeVoices(){');
const end = html.indexOf("if('speechSynthesis'in window){", start);
assert.ok(start >= 0 && end > start, 'shared speech helper block must exist');
const helper = html.slice(start, end);

function makeRuntime() {
  const spoken = [];
  let resumeCalls = 0;
  const synth = {
    speaking: false, pending: false, paused: true,
    cancel() { this.speaking = false; this.pending = false; },
    resume() { resumeCalls++; this.paused = false; },
    speak(utterance) { spoken.push(utterance); this.pending = true; }
  };
  class Utterance {
    constructor(text) { this.text = text; this.lang = ''; this.rate = 1; this.pitch = 1; }
  }
  const context = vm.createContext({
    window: { speechSynthesis: synth },
    SpeechSynthesisUtterance: Utterance,
    console,
    Date
  });
  vm.runInContext(
    'let speechPlaybackToken=0; let speechPlaybackActive=false; let reflexLastSpeechEndedAt=0;\n' +
    helper +
    '\nglobalThis.api={speak,speakAuto,bvtSpeakQueue};',
    context
  );
  return { api: context.api, spoken, synth, get resumeCalls() { return resumeCalls; } };
}

test('Chinese playback uses zh-CN without pinning a device voice', () => {
  const runtime = makeRuntime();
  runtime.api.speak('你好');
  assert.equal(runtime.spoken.length, 1);
  assert.equal(runtime.spoken[0].lang, 'zh-CN');
  assert.equal(runtime.spoken[0].voice, undefined);
  assert.ok(runtime.resumeCalls > 0);
});

test('Vietnamese playback uses vi-VN even before voice enumeration', () => {
  const runtime = makeRuntime();
  runtime.api.speakAuto('Xin chào');
  assert.equal(runtime.spoken.length, 1);
  assert.equal(runtime.spoken[0].lang, 'vi-VN');
});

test('mixed Chinese and Vietnamese speech is queued sequentially', () => {
  const runtime = makeRuntime();
  runtime.api.speakAuto('你好 xin chào');
  assert.equal(runtime.spoken.length, 1);
  assert.equal(runtime.spoken[0].lang, 'zh-CN');
  runtime.spoken[0].onend();
  assert.equal(runtime.spoken.length, 2);
  assert.equal(runtime.spoken[1].lang, 'vi-VN');
});

test('unavailable regional voice retries with the base language locale', () => {
  const runtime = makeRuntime();
  runtime.api.speak('你好');
  runtime.spoken[0].onerror({ error: 'voice-unavailable' });
  assert.equal(runtime.spoken.length, 2);
  assert.equal(runtime.spoken[1].lang, 'zh');
});

test('the helper does not block when the device returns an empty voice list', () => {
  const runtime = makeRuntime();
  runtime.api.speakAuto('Xin chào');
  assert.equal(runtime.spoken.length, 1);
  assert.equal(runtime.spoken[0].lang, 'vi-VN');
});
