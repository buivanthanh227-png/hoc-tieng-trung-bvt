#!/usr/bin/env python3
"""Exercise the actual CVDICT-backed whole-sentence Menu 18 mapper."""
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
for marker in ("MENU18_MULTICANDIDATE_SENTENCE_SEARCH","function pinyin18SelectToneDiverse(candidates,raw,limit=16){","function pinyinToChineseCandidates(raw){","state.rows.concat([item.row])","if(ranked.length)add(ranked[0]);"):
    if marker not in html: raise SystemExit("Whole-sentence mapper component missing: "+marker)
if "state.rows.concat(item.row)" in html:
    raise SystemExit("Dictionary rows are flattened; sentence Pinyin cannot be preserved.")
start=html.index("async function renderHomework18Candidates(candidates){")
end=html.index("\nfunction looksLikePinyin18(raw,local){",start)
renderer=html[start:end]
for marker in ("async function renderHomework18Candidates(candidates)","await Promise.all(","select(0);","homework18ValidVietnameseMeaning(enriched)","formatHomework18PinyinByWord(item.zh,item.py||pinyinForChinese(item.zh))"):
    if marker not in renderer: raise SystemExit("Whole-sentence meaning/result UI missing: "+marker)
if "const best=await renderHomework18Candidates(candidates);" not in html:
    raise SystemExit("Menu 18 lookup does not await whole-sentence verification")
card_start=html.index("function renderHomework18Card(result,sourceLabel=''){")
card_end=html.index("\nlet homework18Candidates=[];",card_start)
card=html[card_start:card_end]
for marker in ("copyButton(zh,'chữ Hán')+speakButton(zh,'chữ Hán')","copyButton(py,'Pinyin')","copyButton(vi,'nghĩa tiếng Việt')+speakButton(vi,'nghĩa tiếng Việt')"):
    if marker not in card: raise SystemExit("Menu 18 copy/speaker action missing: "+marker)
if "const token=++homework18LookupToken,raw=$('homework18-query').value,query=raw.trim()" not in html:
    raise SystemExit("Original input is not preserved separately from trimmed query")

def extract_const(name):
    start=html.index("const "+name+"=")
    pos=html.index("=",start)+1
    while html[pos].isspace(): pos+=1
    opening=html[pos]
    closing="]" if opening=="[" else "}"
    depth=0; quote=None; escaped=False
    for i in range(pos,len(html)):
        ch=html[i]
        if quote:
            if escaped: escaped=False
            elif ch=="\\": escaped=True
            elif ch==quote: quote=None
        else:
            if ch in ("'",'"',"`"): quote=ch
            elif ch==opening: depth+=1
            elif ch==closing:
                depth-=1
                if depth==0:
                    end=i+1
                    while html[end].isspace(): end+=1
                    if html[end]!=";": raise SystemExit("Could not isolate JS constant "+name)
                    return html[start:end+1]
    raise SystemExit("Could not extract JS constant "+name)

def extract_fn(name):
    start=html.index("function "+name+"(")
    brace=html.index("{",start); depth=0; quote=None; escaped=False
    line_comment=False; block_comment=False
    for i in range(brace,len(html)):
        ch=html[i]; nxt=html[i+1] if i+1<len(html) else ""
        if line_comment:
            if ch=="\n": line_comment=False
        elif block_comment:
            if ch=="*" and nxt=="/": block_comment=False
        elif quote:
            if escaped: escaped=False
            elif ch=="\\": escaped=True
            elif ch==quote: quote=None
        else:
            if ch=="/" and nxt=="/": line_comment=True
            elif ch=="/" and nxt=="*": block_comment=True
            elif ch in ("'",'"',"`"): quote=ch
            elif ch=="{": depth+=1
            elif ch=="}":
                depth-=1
                if depth==0:return html[start:i+1]
    raise SystemExit("Could not extract JS function "+name)

constants=["MENU18_VERIFIED_SENTENCES","PINYIN18_COMMON_CHARACTERS","PINYIN18_COMMON_CHARACTERS_EXTENDED","PINYIN18_COMMON_WORDS","PINYIN18_SINGLE_TONE_WORDS"]
functions=["pinyin18ToneFromInput","pinyin18Key","pinyin18LexiconKey","getPinyin18Lexicon","pinyin18Traditional","pinyin18SyllablePaths","pinyin18SelectToneDiverse","pinyinToChineseCandidates"]
js='''const dictionary=JSON.parse('''+json.dumps(match.group(1),ensure_ascii=False)+''');
let pinyin18IndexSource=null,pinyin18Lexicon=null,pinyin18SeedRows=null,pinyin18Syllables=null;
const sentenceDeck=[];const OFFLINE_SENTENCE_TRANSLATIONS={};const CURATED_ZH_VI={};
function buildSeed(){return [];}function pinyinForChinese(){return '';}
'''
js+="\n".join(extract_const(name) for name in constants)
js+="\nObject.assign(PINYIN18_COMMON_CHARACTERS,PINYIN18_COMMON_CHARACTERS_EXTENDED);\n"
js+="\n".join(extract_fn(name) for name in functions)
js+=r"""
const assert=require('node:assert/strict');
const results=pinyinToChineseCandidates('ni jin le ma');
assert.ok(results.length>1,'the full sentence returns more than one tone candidate');
assert.equal(results[0].zh,'你进了吗','the verified full-sentence interpretation is ranked first');
assert.equal(results[0].py,'nǐ jìn le ma','the selected sentence keeps the correct dictionary Pinyin and tones');
assert.equal(results[0].vi,'Bạn vào được chưa?','the complete sentence has a Vietnamese meaning');
assert.ok(results.every(item=>[...item.zh].length>1),'all candidates are complete Chinese phrases, not isolated characters');
assert.ok(results.every(item=>pinyin18Key(item.py)===pinyin18Key('ni jin le ma')),'candidate Pinyin matches the entire original input');
const jinTones=results.map(item=>item.py.split(/\\s+/).find(token=>pinyin18Key(token)==='jin')).filter(Boolean).map(pinyin18ToneFromInput);
assert.ok(new Set(jinTones).size>1,'different tone readings at jin are actually explored');
const marked=pinyinToChineseCandidates('nǐ jìn le ma');
assert.ok(marked.length>0&&marked.every(item=>pinyin18ToneFromInput(item.py.split(/\\s+/).find(token=>pinyin18Key(token)==='ni'))===3&&pinyin18ToneFromInput(item.py.split(/\\s+/).find(token=>pinyin18Key(token)==='jin'))===4),'explicit tone marks constrain the whole-sentence search');
console.log('Actual CVDICT Menu 18 whole-sentence mapping and tone-diversity tests: PASS');
"""
with tempfile.NamedTemporaryFile("w",suffix=".cjs",encoding="utf-8",delete=False) as f:
    f.write(js); test_path=f.name
subprocess.run(["node","--check",test_path],check=True)
subprocess.run(["node",test_path],check=True)
print(f"Verified actual full-sentence mapping against {len(dictionary):,} embedded CVDICT rows, including copy/speaker UI markers.")
