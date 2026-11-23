'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

test('Menu 1 field order and tone controls', () => {
 const p=['meaning','hanzi','pinyin','tone'].map(x=>html.indexOf('id="dict-'+(x==='tone'?'tone-picker':'search-field-'+x)+'"'));
 assert.ok(p.every(x=>x>=0)&&p[0]<p[1]&&p[1]<p[2]&&p[2]<p[3]);
 for(const id of ['dict-search-meaning','dict-search-hanzi','dict-search-pinyin']){
  const at=html.indexOf('id="'+id+'"');
  assert.match(html.slice(at,at+200),/placeholder="Vui lòng nhập"/);
 }
 for(let n=1;n<=5;n++)assert.ok(html.includes('data-dict-tone="'+n+'"'));
});

test('Menu 1 count has green text and a transparent background',()=>{
 const at=html.indexOf('id="bvt-v4222-user-layout-fixes"'),css=html.slice(at,html.indexOf('</style>',at));
 assert.match(css,/#panel-dict \.section-title #count-pill[\s\S]*?background:transparent!important/);
 assert.match(css,/color:#15803d!important/);
});

test('Banner title is geometrically centered between flags',()=>{
 assert.ok(html.includes('id="bvt-v4222-banner-true-center"'));
 assert.ok(html.includes('bvt-v4222-banner-center-runtime'));
 assert.match(html,/ResizeObserver/);
 assert.match(html,/--bvt-banner-title-shift/);
});

test('Menu 3 modal copy buttons are bound for all three values',()=>{
 assert.ok(html.includes("modal.querySelectorAll('[data-homework3x-copy]')"));
 for(const kind of ['hanzi','pinyin','meaning'])assert.ok(html.includes('data-homework3x-copy="'+kind+'"'));
 assert.ok(html.includes('homework3x-copy-status'));
 assert.match(html,/const ok=await copy\(value\)/);
});

test('Menu 3 distinguishes Vietnamese from Pinyin and has fallback translation',()=>{
 assert.ok(html.includes('function looksLikeVietnamese3x(raw)'));
 assert.ok(html.includes('async function machineTranslate3x(text,source,target,options={})'));
 assert.ok(html.includes('api.mymemory.translated.net'));
 assert.ok(html.includes('translate.googleapis.com/translate_a/single'));
 assert.ok(html.includes('const translation=await machineTranslate3x(query,source,target)'));
});

test('Menu 1 wide desktop layout keeps Pinyin and tones on full-width rows',()=>{
 const at=html.indexOf('id="bvt-v4222-user-layout-fixes"');
 const css=html.slice(at,html.indexOf('</style>',at));
 assert.ok(at>=0);
 assert.ok(css.includes('grid-template-columns:repeat(2,minmax(0,1fr))!important'));
 assert.ok(css.includes('#panel-dict #dict-search-field-meaning{grid-column:1!important;grid-row:1!important}'));
 assert.ok(css.includes('#panel-dict #dict-search-field-hanzi{grid-column:2!important;grid-row:1!important}'));
 assert.ok(css.includes('#panel-dict #dict-search-field-pinyin{grid-column:1/-1!important;grid-row:2!important}'));
 assert.ok(css.includes('#panel-dict #dict-tone-picker{grid-column:1/-1!important;grid-row:3!important;min-width:0!important}'));
 assert.ok(html.includes('.dict-tone-buttons{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px}'));
 assert.match(css,/@media\(max-width:520px\)/);
 assert.doesNotMatch(css,/#panel-dict #dict-search-field-pinyin\{grid-column:3/);
});

test('Banner slogans share the actual flag edge anchors',()=>{
 const at=html.indexOf('id="bvt-v4222-banner-true-center"');
 const css=html.slice(at,html.indexOf('</style>',at));
 assert.ok(at>=0);
 assert.ok(css.includes('.topbar .brand>.brand-flag:first-child{grid-column:1!important;grid-row:1!important;justify-self:start!important}'));
 assert.ok(css.includes('.topbar .brand>.brand-flag:last-child{grid-column:3!important;grid-row:1!important;justify-self:end!important}'));
 assert.match(css,/.brand-slogan>span:first-child\{grid-column:1!important;grid-row:2!important;justify-self:stretch!important;width:100%!important;text-align:left!important\}/);
 assert.match(css,/.brand-slogan>span:last-child\{grid-column:3!important;grid-row:2!important;justify-self:stretch!important;width:100%!important;text-align:right!important\}/);
});

test('Menu 3 uses the existing server route and preserves long-text boundaries',()=>{
 assert.ok(html.includes("const result=await bvtMlTranslate(value,sourceCode,targetCode,()=>true,'',BVT_TRANSLATE_TIMING)"));
 assert.ok(html.includes("if(value.length>5000)throw new Error"));
 assert.ok(html.includes('function splitMenu3TranslationText(value,maxChars=4200)'));
 assert.ok(html.includes('async function translateLongText3x(text,target,statusEl,resultEl)'));
 assert.ok(html.includes('const chunks=splitMenu3TranslationText(raw,1500)'));
 const handlerStart=html.indexOf('<script id="menu3-independent-translation-handlers">');
 const handlerEnd=html.indexOf('</script>',handlerStart);
 const handlers=html.slice(handlerStart,handlerEnd);
 assert.match(handlers,/translateLongText3x\(/);
 assert.doesNotMatch(handlers,/await translateLongText\(/);

 const splitStart=html.indexOf('function splitMenu3TranslationText(value,maxChars=4200)');
 const splitEnd=html.indexOf('async function translateLongText3x',splitStart);
 const context=vm.createContext({});
 vm.runInContext(html.slice(splitStart,splitEnd),context,{timeout:10000});
 const source='First sentence, with a clause. Second sentence?\n\nThird sentence!';
 const chunks=context.splitMenu3TranslationText(source,40);
 assert.ok(chunks.length>1);
 assert.equal(chunks.map(chunk=>chunk.text+chunk.separator).join(''),source);
 assert.ok(chunks.some(chunk=>chunk.text.endsWith('.')));
 assert.ok(chunks.some(chunk=>chunk.text.includes('\n\n')||chunk.separator.includes('\n\n')));
});

test('Footer clock is centered, enlarged and red without changing release version',()=>{
 assert.ok(html.includes('bvt-footer-clock-main'));
 assert.match(html,/#app-footer-meta #bvt-clock-time[\s\S]*?font-size:clamp\(27px/);
 assert.match(html,/#app-footer-meta #bvt-clock-date[\s\S]*?font-size:clamp\(20px/);
 assert.ok(html.includes('HỌC TIẾNG TRUNG · Phiên bản V42.10.22'));
 assert.ok(html.includes('color:#dc2626!important'));
});

test('The banner still has two flags and the app version is unchanged',()=>{
 assert.equal((html.match(/class="brand-flag"/g)||[]).length,2);
 assert.equal((html.match(/id="count-pill"/g)||[]).length,1);
 assert.ok(html.includes('<title>HỌC TIẾNG TRUNG · V42.10.22</title>'));
});
