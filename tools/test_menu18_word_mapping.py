#!/usr/bin/env python3
"""Validate Menu 18 sentence-level mapping and whole-sentence Vietnamese output."""
from pathlib import Path
import json,re,subprocess,sys,tempfile
if len(sys.argv)!=2:raise SystemExit("Usage: test_menu18_word_mapping.py <site/index.html>")
html=Path(sys.argv[1]).read_text(encoding="utf-8")
match=re.search(r'<script id="embedded-cvdict-data"[^>]*>(.*?)</script>',html,re.S)
if not match:raise SystemExit("Embedded CVDICT dataset not found")
dictionary=json.loads(match.group(1))
if len(dictionary)<100_000:raise SystemExit(f"Unexpectedly small CVDICT dataset: {len(dictionary)} rows")
for retired in ("function getPinyin18CompactIndex()","wordMapping:true","Ánh xạ độc lập theo từng từ · không ghép tổ hợp"):
    if retired in html:raise SystemExit("Retired word-by-word mapper/UI remains: "+retired)
start=html.index("function renderHomework18Candidates(candidates){")
end=html.index("function looksLikePinyin18(raw,local){",start)
renderer=html[start:end]
for marker in ("pinyin18SelectToneDiverse(","machineTranslate(item.zh,'zh-CN','vi')","formatHomework18PinyinByWord(item.zh,item.py)"):
    if marker not in renderer:raise SystemExit("Whole-sentence renderer missing: "+marker)
if "const token=++homework18LookupToken,raw=$('homework18-query').value,query=raw.trim()" not in html:
    raise SystemExit("Original input is not preserved separately from trimmed query")
def extract(start,end):
    a=html.index(start);b=html.index(end,a);return html[a:b]
parts=[
 extract("const PINYIN18_COMMON_WORDS={","\n};")+"\n};",
 extract("function pinyin18Key(value){","function pinyin18LexiconKey"),
 extract("function pinyin18DisplayKey(value){","function renderHomework18Candidates")
]
js=r"""
const assert=require('node:assert/strict');
function preferred(raw){
 const key=pinyin18Key(raw);
 const found=Object.entries(PINYIN18_COMMON_WORDS).find(([phrase])=>pinyin18Key(phrase)===key);
 return found?found[1]:null;
}
const sample=preferred('jintian wo jia you ke ren');
assert.ok(sample,'whole-sentence regression candidate exists');
assert.equal(sample[0],'今天我家有客人');
assert.equal(sample[1],'jīn tiān wǒ jiā yǒu kè rén');
assert.equal(sample[2],'Hôm nay nhà tôi có khách.');
assert.equal(formatHomework18PinyinByWord(sample[0],sample[1]),'jīntiān wǒ jiā yǒu kèrén');
assert.equal(preferred('keyi')[0],'可以');
assert.equal(formatHomework18PinyinByWord('可以','kě yǐ'),'kěyǐ');
assert.equal(preferred('jintian')[0],'今天');
assert.equal(formatHomework18PinyinByWord('今天','jīn tiān'),'jīntiān');
console.log('Menu 18 whole-sentence candidate, exact Pinyin, tone marks and Vietnamese gloss tests: PASS');
"""
with tempfile.NamedTemporaryFile("w",suffix=".cjs",encoding="utf-8",delete=False) as f:
    f.write("\n".join(parts)+"\n"+js);test_path=f.name
subprocess.run(["node",test_path],check=True)
print(f"Verified sentence-level Menu 18 behavior against {len(dictionary):,} embedded CVDICT rows.")
