#!/usr/bin/env python3
"""Expose all dictionary-backed tone candidates in Menu 18.

Menu 3 remains untouched. This overlay changes only the experimental Menu 18
artifact: exact phrase matches are retained as a preferred candidate, but no
longer suppress sentence-level dictionary alternatives.
"""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_menu18_multicandidate.py <site/index.html>")
target = Path(sys.argv[1])
if not target.is_file():
    raise SystemExit(f"Menu 18 target not found: {target}")
source = target.read_text(encoding="utf-8")
original = source

old_guard = "if(!hasExactPhraseSource||shouldGenerateAlternates){"
if source.count(old_guard) == 1:
    source = source.replace(old_guard, "{", 1)
elif source.count(old_guard) != 0:
    raise SystemExit("Menu 18 multicandidate patch: ambiguous sentence-search guard.")
elif "MENU18_MULTICANDIDATE_SENTENCE_SEARCH" not in source:
    raise SystemExit("Menu 18 multicandidate patch: sentence-search guard not found.")
marker_line = "const hasExactPhraseSource=[...found.values()].some(item=>item.priority>=5000);"
if "MENU18_MULTICANDIDATE_SENTENCE_SEARCH" not in source:
    if source.count(marker_line) != 1:
        raise SystemExit("Menu 18 multicandidate patch: exact phrase marker is ambiguous.")
    source = source.replace(
        marker_line,
        marker_line + " // MENU18_MULTICANDIDATE_SENTENCE_SEARCH: exact phrases rank first; dictionary alternatives are still explored.",
        1
    )

# Keep candidate-internal syllable boundaries explicit for tone validation.
# The display formatter compacts known lexical words (e.g. jīntiān) afterwards.
compact_sentence_py = "py:'jīntiān wǒ jiā yǒu kèrén'"
expanded_sentence_py = "py:'jīn tiān wǒ jiā yǒu kè rén'"
if source.count(compact_sentence_py) == 1:
    source = source.replace(compact_sentence_py, expanded_sentence_py, 1)
elif source.count(expanded_sentence_py) != 1:
    raise SystemExit("Menu 18 multicandidate patch: verified sentence Pinyin boundary not found uniquely.")

start = source.find("function renderHomework18Candidates(candidates){")
end = source.find("\nfunction looksLikePinyin18(raw,local){", start)
if start < 0 or end < 0:
    raise SystemExit("Menu 18 multicandidate patch: renderer boundaries not found.")
renderer = r'''let homework18SelectedCandidateIndex=0;
function renderHomework18Candidates(candidates){
 const box=$('homework18-candidates');
 box.replaceChildren();
 const list=(Array.isArray(candidates)?candidates:[]).filter(item=>typeof homework18ValidVietnameseMeaning!=='function'||homework18ValidVietnameseMeaning(item));
 if(!list.length){box.hidden=true;return null;}
 homework18SelectedCandidateIndex=0;
 box.hidden=false;
 box.innerHTML='<div class="homework18-candidate-heading">Chọn phương án phù hợp với ý bạn ('+list.length+' kết quả)</div>'+
  list.map((item,index)=>'<button type="button" class="homework18-candidate'+(index===0?' is-selected':'')+'" data-homework18-candidate="'+index+'" aria-pressed="'+(index===0?'true':'false')+'"><span class="homework18-candidate-number">'+(index+1)+'</span><span class="homework18-candidate-content"><span class="homework18-candidate-zh">'+escapeHTML(item.zh)+'</span><span class="homework18-candidate-py">'+escapeHTML(formatHomework18PinyinByWord(item.zh,item.py||pinyinForChinese(item.zh)))+'</span></span></button>').join('');
 const select=(index)=>{
  if(index<0||index>=list.length)return;
  homework18SelectedCandidateIndex=index;
  const token=++homework18LookupToken,item=list[index];
  box.querySelectorAll('[data-homework18-candidate]').forEach(button=>{
   const selected=Number(button.dataset.homework18Candidate)===index;
   button.classList.toggle('is-selected',selected);
   button.setAttribute('aria-pressed',selected?'true':'false');
  });
  const label='Phương án '+(index+1)+' / '+list.length+' · '+String(item.source||'Từ điển');
  const needsWholeSentenceMeaning=Boolean(item.note&&/ghép từ điển|cụm từ/i.test(item.note));
  renderHomework18Card({...item,vi:needsWholeSentenceMeaning?'Đang tra nghĩa tiếng Việt cho toàn câu…':item.vi},label);
  if(needsWholeSentenceMeaning){
   const status=$('homework18-status');
   if(status)status.textContent='Đang dịch nghĩa toàn câu của phương án '+(index+1)+'…';
   machineTranslate(item.zh,'zh-CN','vi').then(vi=>{
    if(token!==homework18LookupToken||homework18SelectedCandidateIndex!==index)return;
    renderHomework18Card({...item,vi,note:'Nghĩa tiếng Việt được dịch từ toàn câu.'},label);
    if(status)status.textContent='Đã dịch nghĩa toàn câu cho phương án '+(index+1)+'.';
   }).catch(()=>{
    if(token!==homework18LookupToken||homework18SelectedCandidateIndex!==index)return;
    renderHomework18Card({...item,vi:item.vi||'Chưa tra được nghĩa tiếng Việt cho toàn câu.'},label);
    if(status)status.textContent='Không kết nối được dịch vụ dịch nghĩa; đang giữ nghĩa tham khảo từ điển.';
   });
  }else{
   const status=$('homework18-status');
   if(status)status.textContent='Đang xem phương án '+(index+1)+' / '+list.length+'.';
  }
 };
 box.querySelectorAll('[data-homework18-candidate]').forEach(button=>button.addEventListener('click',()=>select(Number(button.dataset.homework18Candidate))));
 return list[0];
}'''
source = source[:start] + renderer + source[end:]

old_css = ".homework18-candidates{display:none!important}"
new_css = """.homework18-candidates{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin:4px 0 8px!important;padding:0!important}
.homework18-candidate-heading{grid-column:1/-1;font-size:12px;font-weight:800;color:var(--muted,#667085);padding:2px 0}
.homework18-candidate{display:flex;align-items:flex-start;gap:8px;min-width:0;text-align:left;padding:9px;border:1px solid var(--line,#d0d5dd);border-radius:9px;background:#fff;color:var(--ink,#182230);cursor:pointer}
.homework18-candidate.is-selected{border-color:#864B90;background:#faf5ff;box-shadow:0 0 0 1px #864B90}
.homework18-candidate-number{display:grid;place-items:center;flex:0 0 21px;height:21px;border-radius:6px;background:#f2f4f7;font-size:11px;font-weight:800}
.homework18-candidate-content{display:grid;gap:3px;min-width:0}
.homework18-candidate-zh{font-size:19px;font-weight:850;line-height:1.35;overflow-wrap:anywhere}
.homework18-candidate-py{font-size:11px;line-height:1.4;color:var(--muted,#667085);overflow-wrap:anywhere}
@media(max-width:430px){.homework18-candidates{grid-template-columns:1fr}.homework18-candidate{padding:8px}.homework18-candidate-zh{font-size:18px}}"""
if source.count(old_css) == 1:
    source = source.replace(old_css, new_css, 1)
elif source.count(new_css) != 1:
    raise SystemExit("Menu 18 multicandidate patch: expected exactly one candidate-list CSS anchor.")

required = [
    "MENU18_MULTICANDIDATE_SENTENCE_SEARCH",
    "let homework18SelectedCandidateIndex=0;",
    "data-homework18-candidate",
    "Chọn phương án phù hợp với ý bạn",
    "machineTranslate(item.zh,'zh-CN','vi')",
    ".homework18-candidates{display:grid!important"
]
missing = [x for x in required if x not in source]
if missing:
    raise SystemExit("Menu 18 multicandidate verification failed: " + ", ".join(missing))
if source != original:
    target.write_text(source, encoding="utf-8", newline="\n")
print("Menu 18 multicandidate patch: verified")
print("Exact phrase is retained as the top-ranked result; sentence-level dictionary alternatives remain enabled.")
print("Candidate selector is visible and selected alternatives translate the complete Chinese sentence.")
