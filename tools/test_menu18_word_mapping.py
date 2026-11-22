#!/usr/bin/env python3
"""Regression checks for whole-sentence, tone-diverse Menu 18 and its result actions."""
from pathlib import Path
import json,re,subprocess,sys,tempfile
if len(sys.argv)!=2: raise SystemExit("Usage: test_menu18_word_mapping.py <site/index.html>")
html=Path(sys.argv[1]).read_text(encoding="utf-8")
match=re.search(r'<script id="embedded-cvdict-data"[^>]*>(.*?)</script>',html,re.S)
if not match: raise SystemExit("Embedded CVDICT dataset not found")
dictionary=json.loads(match.group(1))
if len(dictionary)<100_000: raise SystemExit(f"Unexpectedly small CVDICT dataset: {len(dictionary)} rows")
for retired in ("MENU18_INDEPENDENT_TOKEN_MAPPING_V1","Các kết quả ánh xạ độc lập","tra từng mục nhập độc lập","function getPinyin18CompactIndex()","wordMapping:true"):
    if retired in html: raise SystemExit("Retired word-by-word Menu 18 behavior remains: "+retired)
for marker in ("MENU18_MULTICANDIDATE_SENTENCE_SEARCH","function pinyin18SelectToneDiverse(candidates,raw,limit=16){","function pinyinToChineseCandidates(raw){"):
    if marker not in html: raise SystemExit("Whole-sentence tone-search component missing: "+marker)
start=html.index("function renderHomework18Candidates(candidates){")
end=html.index("function looksLikePinyin18(raw,local){",start)
renderer=html[start:end]
for marker in ("renderHomework18Card(","machineTranslate(item.zh,'zh-CN','vi')","formatHomework18PinyinByWord(item.zh,item.py)"):
    if marker not in renderer: raise SystemExit("Whole-sentence result selector missing: "+marker)
card_start=html.index("function renderHomework18Card(result,sourceLabel=''){")
card_end=html.index("\nlet homework18Candidates=[];",card_start)
card=html[card_start:card_end]
for marker in ("copyButton(zh,'chữ Hán')+speakButton(zh,'chữ Hán')","copyButton(py,'Pinyin')","copyButton(vi,'nghĩa tiếng Việt')+speakButton(vi,'nghĩa tiếng Việt')"):
    if marker not in card: raise SystemExit("Menu 18 copy/speaker action missing: "+marker)
if "const token=++homework18LookupToken,raw=$('homework18-query').value,query=raw.trim()" not in html:
    raise SystemExit("Original input is not preserved separately from trimmed query")
def extract(start,end):
    a=html.index(start);b=html.index(end,a);return html[a:b]
parts=[
    extract("const PINYIN18_COMMON_WORDS={","\n};")+"\n};",
    extract("function pinyin18ToneFromInput(value){","let pinyin18IndexSource="),
    extract("function pinyin18Key(value){","function pinyin18LexiconKey"),
    extract("function pinyin18SelectToneDiverse(candidates,raw,limit=16){","function pinyinToChineseCandidates(raw){")
]
js=r"""
const assert=require('node:assert/strict');
const pinyin18Syllables=new Set(['ni','jin','le','ma']);
const sentenceCandidates=[
 {zh:'你进了吗',py:'nǐ jìn le ma',priority:100,vi:'Bạn vào chưa?'},
 {zh:'你今了吗',py:'nǐ jīn le ma',priority:90,vi:''},
 {zh:'你仅了吗',py:'nǐ jǐn le ma',priority:80,vi:''},
 {zh:'你尽了吗',py:'nǐ jín le ma',priority:70,vi:''}
];
const selected=pinyin18SelectToneDiverse(sentenceCandidates,'ni jin le ma',16);
assert.ok(selected.length>=2,'tone-diverse whole-sentence alternatives are retained');
assert.ok(selected.every(item=>[...item.zh].length>1),'every result is a whole Chinese phrase, never an isolated character');
assert.ok(selected.every(item=>item.py.trim().split(/\s+/).length===4),'each result preserves all four input syllables');
assert.ok(new Set(selected.map(item=>pinyin18ToneFromInput(item.py.split(/\s+/)[1]))).size>=2,'alternative tone readings at the second syllable are retained');
const exact=pinyin18SelectToneDiverse([{zh:'你进了吗',py:'nǐ jìn le ma',priority:100}],'nǐ jìn le ma',16);
assert.equal(exact.length,1,'explicit tone marks constrain the full-sentence search');
console.log('Menu 18 whole-sentence tone-diversity selector tests: PASS');
"""
with tempfile.NamedTemporaryFile("w",suffix=".cjs",encoding="utf-8",delete=False) as f:
    f.write("\n".join(parts)+"\n"+js)
    test_path=f.name
subprocess.run(["node",test_path],check=True)
print(f"Verified sentence-level rendering, copy/speaker controls, and tone selector against {len(dictionary):,} embedded CVDICT rows.")
