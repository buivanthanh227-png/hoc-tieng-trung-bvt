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
renderer = r'''let homework18SelectedCandidateIndex=0,homework18CandidateModal=null;
function closeHomework18CandidateModal(){if(homework18CandidateModal){homework18CandidateModal.remove();homework18CandidateModal=null;}}
function openHomework18CandidateModal(item,index,total){
 closeHomework18CandidateModal();const zh=String(item.zh||''),py=formatHomework18PinyinByWord(zh,item.py||pinyinForChinese(zh)),vi=String(item.vi||'').trim();
 const modal=document.createElement('div');modal.className='homework18-modal-backdrop';
 modal.innerHTML='<section class="homework18-modal" role="dialog" aria-modal="true"><div class="homework18-modal-head"><strong>Kết quả '+(index+1)+' / '+total+'</strong><button type="button" class="homework18-modal-close">×</button></div>'+
 '<div class="homework18-modal-line is-hanzi"><b>HÁN TỰ</b><div class="homework18-modal-value">'+escapeHTML(zh)+'</div>'+copyButton(zh,'chữ Hán')+speakButton(zh,'chữ Hán')+'</div>'+
 '<div class="homework18-modal-line is-pinyin"><b>PHIÊN ÂM PINYIN</b><div class="homework18-modal-value">'+escapeHTML(py)+'</div>'+copyButton(py,'Pinyin')+'</div>'+
 '<div class="homework18-modal-line is-meaning"><b>NGHĨA TIẾNG VIỆT</b><div class="homework18-modal-value">'+escapeHTML(vi||'Chưa có nghĩa tiếng Việt')+'</div>'+copyButton(vi,'nghĩa tiếng Việt')+speakButton(vi,'nghĩa tiếng Việt')+'</div>'+
 '<div class="homework18-modal-nav"><button type="button" data-prev '+(index===0?'disabled':'')+'>‹ Trước</button><button type="button" data-next '+(index>=total-1?'disabled':'')+'>Tiếp theo ›</button></div></section>';
 document.body.appendChild(modal);homework18CandidateModal=modal;
 modal.querySelector('.homework18-modal-close').addEventListener('click',closeHomework18CandidateModal);
 modal.addEventListener('click',e=>{if(e.target===modal)closeHomework18CandidateModal();});
 modal.querySelector('[data-prev]').addEventListener('click',()=>{if(index>0)openHomework18CandidateModal(homework18Candidates[index-1],index-1,total);});
 modal.querySelector('[data-next]').addEventListener('click',()=>{if(index<total-1)openHomework18CandidateModal(homework18Candidates[index+1],index+1,total);});
}
async function renderHomework18Candidates(candidates){
 const box=$('homework18-candidates');box.replaceChildren();
 const sourceList=(Array.isArray(candidates)?candidates:[]).filter(item=>typeof homework18ValidVietnameseMeaning!=='function'||homework18ValidVietnameseMeaning(item));
 if(!sourceList.length){box.hidden=true;return null;}
 const requestToken=homework18LookupToken,status=$('homework18-status'),queue=sourceList,resolved=new Array(sourceList.length);let cursor=0,completed=0;
 box.hidden=false;box.innerHTML='<div class="homework18-candidate-heading">Đang kiểm tra nghĩa của các câu hoàn chỉnh…</div>';
 if(status)status.textContent='Đang xác minh nghĩa toàn câu: 0 / '+queue.length+'…';
 const worker=async()=>{while(true){const index=cursor++;if(index>=queue.length)return;const item=queue[index];try{
  if(String(item.vi||'').trim()&&homework18ValidVietnameseMeaning(item))resolved[index]=item;
  else{const vi=await machineTranslate(item.zh,'zh-CN','vi'),enriched={...item,vi,note:'Nghĩa tiếng Việt được dịch từ toàn câu.'};resolved[index]=homework18ValidVietnameseMeaning(enriched)?enriched:null;}
 }catch(_){resolved[index]=null;}completed++;if(requestToken===homework18LookupToken&&status)status.textContent='Đang xác minh nghĩa toàn câu: '+completed+' / '+queue.length+'…';}};
 await Promise.all(Array.from({length:Math.min(4,queue.length)},worker));if(requestToken!==homework18LookupToken)return null;
 const list=resolved.filter(Boolean);if(!list.length){box.hidden=true;box.replaceChildren();if(status)status.textContent='Không xác minh được câu hoàn chỉnh có nghĩa tiếng Việt.';return null;}
 homework18Candidates=list;homework18SelectedCandidateIndex=0;box.hidden=false;
 box.innerHTML='<div class="homework18-candidate-heading">Chọn câu phù hợp với ý bạn · '+list.length+' kết quả</div>'+list.map((item,index)=>'<button type="button" class="homework18-candidate" data-homework18-candidate="'+index+'"><span class="homework18-candidate-number">'+(index+1)+'</span><span class="homework18-candidate-content"><span class="homework18-candidate-zh">'+escapeHTML(item.zh)+'</span><span class="homework18-candidate-py">'+escapeHTML(formatHomework18PinyinByWord(item.zh,item.py||pinyinForChinese(item.zh)))+'</span><span class="homework18-candidate-vi">'+escapeHTML(item.vi||'')+'</span></span></button>').join('');
 box.querySelectorAll('[data-homework18-candidate]').forEach(button=>button.addEventListener('click',()=>{const index=Number(button.dataset.homework18Candidate),item=list[index];if(!item)return;homework18SelectedCandidateIndex=index;box.querySelectorAll('[data-homework18-candidate]').forEach(node=>node.classList.toggle('is-selected',Number(node.dataset.homework18Candidate)===index));openHomework18CandidateModal(item,index,list.length);if(status)status.textContent='Đang xem kết quả '+(index+1)+' / '+list.length+'.';}));
 if(status)status.textContent='Đã xác minh nghĩa tiếng Việt cho '+list.length+' kết quả. Chạm vào một kết quả để xem chi tiết.';return list[0];
}'''
source = source[:start] + renderer + source[end:]

lookup_anchor = "const best=renderHomework18Candidates(candidates);"
lookup_replacement = "const best=await renderHomework18Candidates(candidates);"
if source.count(lookup_anchor) == 1:
    source = source.replace(lookup_anchor, lookup_replacement, 1)
elif source.count(lookup_replacement) != 1:
    raise SystemExit("Menu 18 multicandidate patch: lookup await anchor missing or ambiguous.")


old_css = ".homework18-candidates:not([hidden]){display:block!important;margin:7px 0 9px!important}"
new_css = """.homework18-candidates{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin:4px 0 8px!important;padding:0!important}
.homework18-candidate-vi{font-size:12px;line-height:1.45;color:#21805b;font-weight:650;overflow-wrap:anywhere}
.homework18-modal-backdrop{position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(15,23,42,.62)}
.homework18-modal{width:min(100%,520px);max-height:min(88dvh,760px);overflow:auto;background:#fff;color:#182230;border-radius:18px;padding:16px;box-shadow:0 20px 60px rgba(0,0,0,.28)}
.homework18-modal-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;font-size:16px}
.homework18-modal-close{border:0;border-radius:50%;width:36px;height:36px;font-size:25px;background:#f2f4f7;color:#344054}
.homework18-modal-line{padding:12px 0;border-bottom:1px solid #eaecf0}
.homework18-modal-line b{display:block;font-size:11px;letter-spacing:.06em;margin-bottom:5px}
.homework18-modal-value{font-size:22px;font-weight:800;line-height:1.45;overflow-wrap:anywhere}
.homework18-modal-line.is-hanzi{color:#7b3fa1}.homework18-modal-line.is-pinyin{color:#2563a6}.homework18-modal-line.is-meaning{color:#21805b}
.homework18-modal-nav{display:flex;justify-content:space-between;gap:10px;margin-top:14px}
.homework18-modal-nav button{border:1px solid #d0d5dd;border-radius:9px;padding:9px 14px;background:#f9fafb;font-weight:750}
.homework18-modal-nav button:disabled{opacity:.35}
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
    "Chọn câu hoàn chỉnh phù hợp với ý bạn",
    "async function renderHomework18Candidates(candidates)",
    "await Promise.all(",
    "select(0);",
    "const best=await renderHomework18Candidates(candidates);",
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
