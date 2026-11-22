#!/usr/bin/env python3
"""Run the shipped Menu 18 mapper against the actual embedded CVDICT dataset."""
from pathlib import Path
import json
import re
import subprocess
import sys
import tempfile

if len(sys.argv) != 2:
    raise SystemExit("Usage: test_menu18_word_mapping.py <site/index.html>")
html = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(r'<script id="embedded-cvdict-data"[^>]*>(.*?)</script>', html, re.S)
if not match:
    raise SystemExit("Embedded CVDICT dataset not found")
dictionary = json.loads(match.group(1))
if len(dictionary) < 100_000:
    raise SystemExit(f"Unexpectedly small CVDICT dataset: {len(dictionary)} rows")

def extract_const(name):
    start = html.index(f"const {name}={{")
    return html[start:html.index("};", start) + 2]

def extract(start_marker, end_marker):
    start = html.index(start_marker)
    return html[start:html.index(end_marker, start)]

parts = [
    extract_const("PINYIN18_COMMON_CHARACTERS"),
    extract_const("PINYIN18_COMMON_WORDS"),
    extract_const("PINYIN18_SINGLE_TONE_WORDS"),
    extract("function pinyin18ToneFromInput(value){", "function pinyin18Key(value){"),
    extract("function pinyin18Key(value){", "function pinyin18LexiconKey(value){"),
    extract("function pinyin18LexiconKey(value){", "function getPinyin18Lexicon(){"),
    extract("function getPinyin18Lexicon(){", "function pinyin18Traditional(zh){"),
    extract("function pinyin18SyllablePaths(raw,syllables){", "function pinyin18SelectToneDiverse(candidates,raw,limit=16){"),
    extract("function pinyin18ToneSignature(value){", "function pinyinToChineseCandidates(raw){"),
    extract("function pinyinToChineseCandidates(raw){", "\nfunction renderHomework18Card(result,sourceLabel=''){"),
    extract("function looksLikePinyin18(raw,local){", "\nlet homework18LookupToken=0;"),
]
prefix = (
    "const dictionary=" + json.dumps(dictionary, ensure_ascii=False) + ";\n"
    "let pinyin18CompactIndexSource=null,pinyin18CompactIndex=null;\n"
    "function buildSeed(){return [];}\n"
    "function norm(value){return String(value||'').toLowerCase();}\n"
)
checks = r"""
const assert = require('node:assert/strict');
const sample='jintian wo jia you ke ren';
const result=pinyinToChineseCandidates(sample);
const byToken=Object.fromEntries([...new Set(result.map(x=>x.inputToken))].map(token=>[token,result.filter(x=>x.inputToken===token).map(x=>x.toneSignature)]));
console.log('Actual CVDICT additive mapping:',JSON.stringify({groups:result.length,byToken}));
assert.equal(result.length,19,'Expected 19 additive tone groups, not Cartesian combinations');
assert.ok(result.every(item=>item.wordMapping),'Every result must represent one input word and one tone signature');
assert.ok(result.every(item=>item.rawInput===sample),'Original input must be preserved exactly');
assert.ok(result.some(item=>item.inputToken==='jintian'&&item.zh==='今天'&&item.toneSignature==='11'),'jintian must map to 今天 with its dictionary tone pattern');
assert.ok(result.some(item=>item.inputToken==='wo'&&item.zh==='我'&&item.toneSignature==='3'),'wo must map to 我');
assert.ok(result.some(item=>item.inputToken==='jia'&&item.zh==='家'&&item.toneSignature==='1'),'jia must map to 家');
assert.ok(result.some(item=>item.inputToken==='you'&&item.zh==='有'&&item.toneSignature==='3'),'you must map to 有');
assert.ok(result.some(item=>item.inputToken==='ke'&&item.zh==='客'&&item.toneSignature==='4'),'ke must map to 客');
assert.ok(result.some(item=>item.inputToken==='ren'&&item.zh==='人'&&item.toneSignature==='2'),'ren must map to 人');
assert.ok(!result.some(item=>item.zh==='今天我家有客人'),'Must not combine separate input words into a sentence');
const a=pinyinToChineseCandidates('a');
assert.equal(a.length,4,'a must expose exactly the four main tones');
const keyi=pinyinToChineseCandidates('keyi');
assert.ok(keyi.some(item=>item.zh==='可以'&&item.toneSignature==='33'),'keyi must map to 可以 as one dictionary word');
assert.ok(keyi.every(item=>item.inputToken==='keyi'),'keyi must not be split into input tokens');
const marked=pinyinToChineseCandidates('wǒ');
assert.equal(marked.length,1,'Tone-marked input must select one tone group');
assert.equal(marked[0].toneSignature,'3');
const numbered=pinyinToChineseCandidates('wo3');
assert.equal(numbered.length,1,'Numbered tone input must select one tone group');
assert.equal(numbered[0].toneSignature,'3');
const mixed=pinyinToChineseCandidates('jintian xyz wo');
assert.ok(mixed.length>0&&mixed.missingTokens.includes('xyz'),'Unknown words must be reported, not fabricated');
assert.equal(looksLikePinyin18('jintian xyz wo',null),true,'Mixed known/unknown Pinyin must stay on dictionary mapping path');
assert.equal(looksLikePinyin18('xyz unknown',null),false,'Unknown non-Pinyin text must not be classified as Pinyin');
const spaced='  jintian   wo jia you ke ren  ';
const preserved=pinyinToChineseCandidates(spaced);
assert.equal(preserved.rawInput,spaced,'Whitespace in the original input must remain unchanged');
assert.ok(preserved.every(item=>item.rawInput===spaced));
console.log('Menu 18 independent word mapping and dictionary integration tests: PASS');
"""
with tempfile.NamedTemporaryFile("w", suffix=".cjs", encoding="utf-8", delete=False) as handle:
    handle.write(prefix + "\n".join(parts) + checks)
    test_path = handle.name
subprocess.run(["node", test_path], check=True)
print(f"Verified against {len(dictionary):,} embedded CVDICT rows.")
