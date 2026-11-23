#!/usr/bin/env python3
from pathlib import Path
import re, subprocess, sys, tempfile
if len(sys.argv)!=2: raise SystemExit('Usage: test_menu18_independent_mapping.py <site/index.html>')
html=Path(sys.argv[1]).read_text(encoding='utf-8')
embedded=re.search(r'<script id="embedded-cvdict-data"[^>]*>(.*?)</script>',html,re.S)
if not embedded: raise SystemExit('Embedded CVDICT dataset not found')
for marker in ['MENU18_INDEPENDENT_TOKEN_MAPPING_V1','Các kết quả ánh xạ độc lập','tra từng mục nhập độc lập']:
 if marker not in html: raise SystemExit('Missing independent mapping marker: '+marker)
if 'tự xét nhiều thanh điệu và ghép thành một câu phù hợp nhất' in html:
 raise SystemExit('Retired sentence-composition instructions remain in Menu 18')
def extract(start,end):
 a=html.index(start);b=html.index(end,a);return html[a:b]
chunks=[
 'const dictionary = JSON.parse('+repr(embedded.group(1))+');',
 extract('const PINYIN18_COMMON_CHARACTERS={','function pinyin18ToneFromInput(value){'),
 extract('function pinyin18ToneFromInput(value){','function pinyin18Key(value){'),
 extract('function pinyin18Key(value){','function pinyin18LexiconKey(value){'),
 extract('function pinyin18LexiconKey(value){','function getPinyin18Lexicon(){'),
 extract('function getPinyin18Lexicon(){','function pinyin18Traditional(zh){'),
 extract('function pinyin18Traditional(zh){','function pinyin18SyllablePaths(raw,syllables){'),
 extract('function pinyin18SyllablePaths(raw,syllables){','function pinyin18SelectToneDiverse'),
 extract('function pinyinToChineseCandidates(raw){','function renderHomework18Card(result,sourceLabel=\'\'){')
]
js=r'''
const assert=require('node:assert/strict');
function pinyinForChinese(value){return String(value||'');}
'''+ '\n'.join(chunks)+r'''
const simple=pinyinToChineseCandidates('ni jin le ma');
assert.ok(simple.length>0);
assert.deepEqual([...new Set(simple.map(x=>x.inputToken))],['ni','jin','le','ma']);
assert.ok(simple.every(x=>!String(x.zh).includes(' ')));
assert.ok(simple.some(x=>x.inputToken==='jin'&&x.zh==='今'&&x.toneKey==='1'));
assert.ok(simple.some(x=>x.inputToken==='jin'&&x.zh==='仅'&&x.toneKey==='3'));
assert.ok(simple.some(x=>x.inputToken==='jin'&&x.zh==='进'&&x.toneKey==='4'));
const a=pinyinToChineseCandidates('a');
assert.deepEqual([...new Set(a.map(x=>x.toneKey))].sort(),['1','2','3','4']);
const ba=pinyinToChineseCandidates('ba');
assert.equal(ba.length,4);
assert.equal(pinyinToChineseCandidates('a ba').length,8);
const fixed=pinyinToChineseCandidates('jìn');
assert.ok(fixed.length>0&&fixed.every(x=>x.toneKey.split('-').includes('4')));
const compact=pinyinToChineseCandidates('jintian');
assert.ok(compact.some(x=>x.zh==='今天'&&x.py==='jīn tiān'));
const unknown=pinyinToChineseCandidates('zzzz');
assert.equal(unknown.length,0);
assert.deepEqual(unknown.unmatchedTokens,['zzzz']);
console.log('Menu 18 independent mapping regression: PASS');
'''
with tempfile.NamedTemporaryFile('w',suffix='.cjs',encoding='utf-8',delete=False) as f:
 f.write(js);test_path=f.name
subprocess.run(['node','--check',test_path],check=True)
subprocess.run(['node',test_path],check=True)
count=0
for m in re.finditer(r'<script\b([^>]*)>([\s\S]*?)</script>',html,re.I):
 attrs,body=m.groups()
 if re.search(r'\bsrc\s*=',attrs) or re.search(r'type\s*=\s*["\']text/plain',attrs,re.I) or not body.strip(): continue
 with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8',delete=False) as f:
  f.write(body);path=f.name
 subprocess.run(['node','--check',path],check=True,stdout=subprocess.DEVNULL)
 count+=1
print(f'Menu 18 dictionary regression and {count} inline JS syntax checks: PASS')
