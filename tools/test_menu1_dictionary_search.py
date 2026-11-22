#!/usr/bin/env python3
"""Regression tests for Menu 1's independent three-field dictionary filters."""
from pathlib import Path
import subprocess,sys,tempfile

if len(sys.argv)!=2:
    raise SystemExit("Usage: test_menu1_dictionary_search.py <site/index.html>")
html=Path(sys.argv[1]).read_text(encoding="utf-8")
markers=[
 "MENU1_THREE_FIELD_DICTIONARY_SEARCH_V1",
 'id="dict-search-hanzi"',
 'id="dict-search-pinyin"',
 'id="dict-search-meaning"',
 'data-dict-tone="1"','data-dict-tone="2"','data-dict-tone="3"','data-dict-tone="4"','data-dict-tone="5"',
 "window.applyFilter=function()",
 "function pinyinScore(candidate,query,selectedTone)",
 "function matchRow(row,hanzi,pinyin,meaning,tone)"
]
for marker in markers:
    if marker not in html:
        raise SystemExit("Menu 1 dictionary search component missing: "+marker)
if html.count('id="dict-search-hanzi"')!=1 or html.count('id="dict-search-pinyin"')!=1 or html.count('id="dict-search-meaning"')!=1:
    raise SystemExit("Menu 1 must have exactly one input for each independent search field")
if html.count('data-dict-tone="')<5:
    raise SystemExit("Menu 1 must expose all five tone filters")
if "found.sort((a,b)=>Array.from(String(rows[a.i][0]||'')).length-Array.from(String(rows[b.i][0]||'')).length||b.score-a.score||a.i-b.i);" not in html:
    raise SystemExit("Menu 1 results must be ranked by ascending Hán tự character count before relevance score")

def extract_fn(name):
    start=html.index("function "+name+"(")
    brace=html.index("{",start); depth=0; quote=None; escaped=False
    for i in range(brace,len(html)):
        ch=html[i]
        if quote:
            if escaped: escaped=False
            elif ch=="\\": escaped=True
            elif ch==quote: quote=None
        else:
            if ch in ("'",'"'): quote=ch
            elif ch=="{": depth+=1
            elif ch=="}":
                depth-=1
                if depth==0:return html[start:i+1]
    raise SystemExit("Could not extract Menu 1 helper "+name)

js="\n".join(extract_fn(name) for name in ("normalize","pinyinParts","pinyinScore","textScore","matchRow"))
js+=r"""
const assert=require('node:assert/strict');
assert.equal(pinyinParts('jīn tiān').length,2,'Pinyin syllable boundaries are read from the dictionary');
assert.ok(pinyinScore('jìn','jin',4)>0,'jin + tone 4 returns jìn');
assert.equal(pinyinScore('jīn','jin',4),0,'tone 4 excludes jīn (tone 1)');
assert.equal(pinyinScore('jǐn','jin',4),0,'tone 4 excludes jǐn (tone 3)');
assert.ok(pinyinScore('jìn','jin',null)>0,'without a tone selected, all tone variants remain searchable');
assert.ok(pinyinScore('jīn tiān','jintian',null)>0,'compact input can match a multi-syllable dictionary word');
assert.ok(pinyinScore('ge','ge',5)>0,'an unmarked syllable is treated as neutral tone 5');
const tone4=['进','進','jìn','vào; tiến vào'];
const tone1=['今','今','jīn','nay; hôm nay'];
const tone3=['紧','緊','jǐn','chặt; khẩn cấp'];
assert.ok(matchRow(tone4,'','jin','',4)>0,'Pinyin field + tone filter returns the correct row');
assert.equal(matchRow(tone1,'','jin','',4),0,'Pinyin tone filter excludes tone 1');
assert.equal(matchRow(tone3,'','jin','',4),0,'Pinyin tone filter excludes tone 3');
assert.ok(matchRow(tone4,'进','','',null)>0,'Hanzi-only search works independently');
assert.ok(matchRow(tone4,'','','tiến vào',null)>0,'Vietnamese meaning-only search works independently');
assert.ok(matchRow(tone4,'进','jin','tiến vào',4)>0,'all three fields can be combined');
assert.equal(matchRow(tone4,'近','jin','tiến vào',4),0,'combined fields use AND semantics');
console.log('Menu 1 independent Hanzi/Pinyin/Vietnamese and five-tone filter tests: PASS');
"""
with tempfile.NamedTemporaryFile("w",suffix=".cjs",encoding="utf-8",delete=False) as f:
    f.write(js); path=f.name
subprocess.run(["node","--check",path],check=True)
subprocess.run(["node",path],check=True)
print("Menu 1 UI and Pinyin tone-filter regression tests: PASS")
