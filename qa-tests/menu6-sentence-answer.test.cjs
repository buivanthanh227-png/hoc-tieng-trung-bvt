'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

function loadVietnameseSentenceScorer() {
  const start = html.indexOf('function scoreVietnameseSentenceAnswer(');
  const end = html.indexOf('\nfunction handleSubmit()', start);
  assert.ok(start >= 0 && end > start, 'Vietnamese sentence scoring helper must exist');
  const body = html.slice(start, end);
  const calls = [];
  const context = vm.createContext({
    scoreAnswer(user, expected, aliases) {
      calls.push({ user, expected, aliases });
      const accepted = [expected, ...aliases].map(value => String(value).trim());
      return accepted.includes(String(user).trim()) ? 100 : 0;
    }
  });
  vm.runInContext(body + '\nthis.scoreVietnameseSentenceAnswer=scoreVietnameseSentenceAnswer;', context);
  return { score: context.scoreVietnameseSentenceAnswer, calls };
}

test('Chinese source sentence is not accepted as a Vietnamese answer in sentence practice', () => {
  const { score, calls } = loadVietnameseSentenceScorer();
  const sentence = { zh: '我爱你。', vi: 'Tôi yêu bạn.', py: 'wǒ ài nǐ' };
  assert.equal(score(sentence.zh, sentence), 0);
  assert.deepEqual(Array.from(calls[0].aliases), ['Tôi yêu bạn']);
  assert.equal(score('Tôi yêu bạn.', sentence), 100);
  assert.equal(score('Tôi yêu bạn', sentence), 100);
});

test('Menu 6 routes Chinese-to-Vietnamese sentence grading through the guarded scorer', () => {
  assert.match(html, /practiceMode==='zh-vi'\)\{expected=p\.sentence\.vi;score=scoreVietnameseSentenceAnswer\(user,p\.sentence\)/);
  assert.doesNotMatch(html, /expected=p\.sentence\.vi;score=scoreAnswer\(user,expected,\[[^\]]*p\.sentence\.zh/);
});
