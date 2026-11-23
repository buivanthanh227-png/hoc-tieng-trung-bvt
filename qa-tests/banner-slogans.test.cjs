'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

function clamp(min, preferred, max, viewportWidth) {
  return Math.round(Math.min(max, Math.max(min, preferred * viewportWidth / 100)) * 1000) / 1000;
}

test('mobile slogan font-size remains readable at supported phone widths', () => {
  assert.match(html, /@media\(max-width:600px\)\{\s*\.topbar \.brand-slogan>span\{\s*font-size:clamp\(11px,3\.15vw,12\.5px\)!important/s);
  assert.equal(clamp(11, 3.15, 12.5, 390), 12.285);
  assert.equal(clamp(11, 3.15, 12.5, 375), 11.813);
  assert.equal(clamp(11, 3.15, 12.5, 320), 11);
});

test('banner retains flag-aligned slogans and the centered title at tablet and desktop widths', () => {
  assert.match(html, /\.topbar \.brand-copy>h1\{[\s\S]*?grid-column:2!important;grid-row:1!important/);
  assert.match(html, /\.topbar \.brand-slogan>span:first-child\{[\s\S]*?grid-column:1!important;grid-row:2!important/);
  assert.match(html, /\.topbar \.brand-slogan>span:last-child\{[\s\S]*?grid-column:3!important;grid-row:2!important/);
  assert.equal(clamp(10, 1.35, 15, 768), 10.368);
  assert.equal(clamp(10, 1.35, 15, 1440), 15);
});
