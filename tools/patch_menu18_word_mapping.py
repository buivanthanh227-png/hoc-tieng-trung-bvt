#!/usr/bin/env python3
"""Keep Menu 18 sentence-level Pinyin mapping and preserve the exact input."""
from pathlib import Path
import sys
if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_menu18_word_mapping.py <site/index.html>")
target=Path(sys.argv[1])
if not target.is_file():
    raise SystemExit(f"Menu 18 patch target not found: {target}")
source=target.read_text(encoding="utf-8")
original=source
def replace_once(old,new,label):
    global source
    if source.count(new)==1:return
    count=source.count(old)
    if count!=1:raise SystemExit(f"Menu 18 sentence patch aborted: expected one {label}; found {count}")
    source=source.replace(old,new,1)
replace_once(
 "const token=++homework18LookupToken,raw=$('homework18-query').value.trim(),box=$('homework18-results'),status=$('homework18-status');",
 "const token=++homework18LookupToken,raw=$('homework18-query').value,query=raw.trim(),box=$('homework18-results'),status=$('homework18-status');",
 "raw input preservation")
replace_once("const local=tryLocalTranslation(raw),hasChinese=","const local=tryLocalTranslation(query),hasChinese=","trimmed local translation query")
replace_once("if(!raw){status.textContent='Nhập câu tiếng Việt, chữ Hán hoặc Pinyin để dịch.';","if(!query){status.textContent='Nhập câu tiếng Việt, chữ Hán hoặc Pinyin để dịch.';","empty input validation")
replace_once("machineTranslate(raw,source,target)","machineTranslate(query,source,target)","trimmed machine translation query")
replace_once("OFFLINE_SENTENCE_TRANSLATIONS[norm(raw)]","OFFLINE_SENTENCE_TRANSLATIONS[norm(query)]","trimmed offline translation lookup")
if "function getPinyin18CompactIndex()" in source or "wordMapping:true" in source:
    raise SystemExit("Menu 18 sentence patch aborted: retired word-by-word mapper is still present.")
renderer_start=source.find("function renderHomework18Candidates(candidates){")
renderer_end=source.find("\nfunction looksLikePinyin18(raw,local){",renderer_start)
if renderer_start<0 or renderer_end<0:raise SystemExit("Menu 18 sentence renderer boundaries not found.")
renderer=source[renderer_start:renderer_end]
for marker in ["pinyin18SelectToneDiverse(","machineTranslate(item.zh,'zh-CN','vi')","formatHomework18PinyinByWord(item.zh,item.py)"]:
    if marker not in renderer:raise SystemExit("Whole-sentence renderer missing: "+marker)
mapper_start=source.find("function pinyinToChineseCandidates(raw){")
mapper_end=source.find("\nfunction renderHomework18Card(result,sourceLabel=''){",mapper_start)
if mapper_start<0 or mapper_end<0:raise SystemExit("Menu 18 sentence candidate mapper not found.")
mapper=source[mapper_start:mapper_end]
if "wordMapping:true" in mapper or "results.missingTokens=missingTokens" in mapper:
    raise SystemExit("Menu 18 sentence mapper still emits isolated word records.")
for marker in ["function pinyin18SyllablePaths(raw,syllables){","function pinyin18SelectToneDiverse(candidates,raw,limit=16){","Nghĩa tiếng Việt sẽ được tra cho toàn câu sau khi chọn phương án."]:
    if marker not in source:raise SystemExit("Menu 18 sentence component missing: "+marker)
if source!=original:target.write_text(source,encoding="utf-8",newline="\n")
print("Menu 18 sentence-level mapping: verified")
print("Whole-sentence candidates retained; exact input preserved; Vietnamese meaning is translated from the full Chinese sentence.")
