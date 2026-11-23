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
renderer = r'''function formatHomework18PinyinByInput(raw,py){
 const inputTokens=String(raw||'').trim().split(/[\s,，、;；]+/).filter(Boolean),syllables=pinyin18Syllables instanceof Set?pinyin18Syllables:new Set(),output=[],tones=String(py||'').trim().split(/\s+/).filter(Boolean);let at=0;
 for(const inputToken of inputTokens){const key=pinyin18Key(inputToken);if(!key)continue;
  if(syllables.has(key)){if(tones[at])output.push(tones[at]);at++;continue;}
  let combined='',end=at,matched=false;
  while(end<tones.length){combined+=tones[end];end++;if(pinyin18Key(combined)===key){output.push(tones.slice(at,end).join(''));at=end;matched=true;break;}if(combined.length>key.length+2)break;}
  if(!matched&&at<tones.length){output.push(tones[at]);at++;}
 }
 if(at<tones.length)output.push(...tones.slice(at));
 return output.join(' ');
}
let homework18SelectedCandidateIndex=0,homework18CandidateModal=null;
function closeHomework18CandidateModal(){if(homework18CandidateModal){homework18CandidateModal.remove();homework18CandidateModal=null;}}
function openHomework18CandidateModal(item,index,total){
 closeHomework18CandidateModal();const zh=String(item.zh||''),py=formatHomework18PinyinByInput(String($('homework18-query')?.value||''),item.py||pinyinForChinese(zh)),vi=String(item.vi||'').trim();
 const modal=document.createElement('div');modal.className='homework18-modal-backdrop';modal.style.cssText='position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(15,23,42,.62)';
 modal.innerHTML='<section class="homework18-modal" role="dialog" aria-modal="true"><div class="homework18-modal-head"><strong>Kết quả '+(index+1)+' / '+total+'</strong><button type="button" class="homework18-modal-close">×</button></div>'+
 '<div class="homework18-modal-line is-hanzi"><b>HÁN TỰ</b><div class="homework18-modal-value">'+escapeHTML(zh)+'</div><div class="homework18-modal-actions"><button type="button" data-homework18-copy="hanzi">Sao chép chữ Hán</button><button type="button" data-homework18-speak="zh">🔊 Phát âm</button></div></div>'+
 '<div class="homework18-modal-line is-pinyin"><b>PHIÊN ÂM PINYIN</b><div class="homework18-modal-value">'+escapeHTML(py)+'</div><div class="homework18-modal-actions"><button type="button" data-homework18-copy="pinyin">Sao chép Pinyin</button><button type="button" data-homework18-speak="py">🔊 Nghe Pinyin</button></div></div>'+
 '<div class="homework18-modal-line is-meaning"><b>NGHĨA TIẾNG VIỆT</b><div class="homework18-modal-value">'+escapeHTML(vi||'Chưa có nghĩa tiếng Việt')+'</div><div class="homework18-modal-actions"><button type="button" data-homework18-copy="meaning">Sao chép nghĩa</button><button type="button" data-homework18-speak="vi">🔊 Đọc nghĩa</button></div></div>'+
 '<div class="homework18-modal-nav"><button type="button" data-prev '+(index===0?'disabled':'')+'>‹ Trước</button><button type="button" data-next '+(index>=total-1?'disabled':'')+'>Tiếp theo ›</button></div></section>';
 document.body.appendChild(modal);homework18CandidateModal=modal;modal.querySelector('[role=dialog]').style.cssText='width:min(100%,520px);max-height:min(88dvh,760px);overflow:auto;background:#fff;color:#182230;border-radius:18px;padding:16px;box-shadow:0 20px 60px rgba(0,0,0,.28)';
 const values={hanzi:zh,pinyin:py,meaning:vi};
 const copy=async value=>{
  try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(value);return true;}}catch(_){}
  const area=document.createElement('textarea');area.value=value;area.setAttribute('readonly','');area.style.cssText='position:fixed;left:-9999px;top:0;opacity:0';document.body.appendChild(area);area.select();let ok=false;try{ok=document.execCommand('copy');}catch(_){}area.remove();return ok;
 };
 const speakMandarinSentence=(text,rate=0.92)=>{
  if(!('speechSynthesis' in window)||typeof SpeechSynthesisUtterance==='undefined')return false;
  window.speechSynthesis.cancel();
  const utterance=new SpeechSynthesisUtterance(String(text||'').trim());
  utterance.lang='zh-CN';utterance.rate=rate;utterance.pitch=1;
  const voices=window.speechSynthesis.getVoices?.()||[];
  const voice=voices.find(v=>/^zh-CN$/i.test(v.lang))||voices.find(v=>/^zh/i.test(v.lang));
  if(voice)utterance.voice=voice;
  window.speechSynthesis.speak(utterance);return true;
 };
 const playHanziSentence=()=>speakMandarinSentence(zh,0.92);
 // Recorded Pinyin syllable audio grouped by the user's original word boundaries.
 const playPinyinWords=async()=>{
  const raw=String($('homework18-query')?.value||'').trim();
  const tokens=raw.split(/[\s,，、;；]+/).filter(Boolean);
  const syllables=String(item.py||'').trim().split(/\s+/).filter(Boolean);
  const known=pinyin18Syllables instanceof Set?pinyin18Syllables:new Set();
  const groups=[];let cursor=0;
  for(const token of tokens){
   const key=pinyin18Key(token);if(!key)continue;
   if(known.has(key)){if(syllables[cursor])groups.push([syllables[cursor++]]);continue;}
   let joined='',group=[];
   while(cursor<syllables.length){
    const next=syllables[cursor++];group.push(next);joined+=pinyin18Key(next);
    if(joined===key)break;
    if(joined.length>key.length+2)break;
   }
   if(group.length)groups.push(group);
  }
  if(cursor<syllables.length)groups.push(syllables.slice(cursor));
  const queue=groups.flatMap((group,gi)=>group.map((syllable,si)=>({syllable,wordEnd:si===group.length-1&&gi<groups.length-1})));
  if(!queue.length)return;
  if('speechSynthesis' in window)window.speechSynthesis.cancel();
  for(const part of queue){
   const base=pinyin18Key(part.syllable).replace(/ü|u:/g,'v');
   const tone=typeof pinyin18ToneFromInput==='function'?pinyin18ToneFromInput(part.syllable):null;
   const url='https://cdn.jsdelivr.net/gh/hugolpz/audio-cmn@f759a0f18f27690742957619e1248ed91e9b3f2c/64k/syllabs/cmn-'+base+(tone||5)+'.mp3';
   try{await new Promise((resolve,reject)=>{const audio=new Audio(url);audio.preload='auto';audio.playbackRate=1.08;audio.onended=resolve;audio.onerror=reject;audio.play().catch(reject);});}
   catch(_){speakMandarinSentence(zh,0.92);return;}
   await new Promise(resolve=>setTimeout(resolve,part.wordEnd?145:28));
  }
 };
 modal.querySelectorAll('[data-homework18-copy]').forEach(button=>button.addEventListener('click',async()=>{const key=button.dataset.homework18Copy,ok=await copy(values[key]||'');button.textContent=ok?'Đã sao chép ✓':'Không sao chép được';}));
 modal.querySelectorAll('[data-homework18-speak]').forEach(button=>button.addEventListener('click',()=>{const kind=button.dataset.homework18Speak;if(kind==='zh'){playHanziSentence();return;}if(kind==='py'){playPinyinWords();return;}if('speechSynthesis' in window){window.speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(vi);utterance.lang='vi-VN';window.speechSynthesis.speak(utterance);}}));
 modal.querySelector('.homework18-modal-close').addEventListener('click',closeHomework18CandidateModal);
 modal.addEventListener('click',e=>{if(e.target===modal)closeHomework18CandidateModal();});
 modal.querySelector('[data-prev]').addEventListener('click',()=>{if(index>0)openHomework18CandidateModal(homework18Candidates[index-1],index-1,total);});
 modal.querySelector('[data-next]').addEventListener('click',()=>{if(index<total-1)openHomework18CandidateModal(homework18Candidates[index+1],index+1,total);});
}
const homework18QueryInput=$('homework18-query');if(homework18QueryInput&&!homework18QueryInput.dataset.noResultClearBound){homework18QueryInput.dataset.noResultClearBound='1';homework18QueryInput.addEventListener('input',()=>{const status=$('homework18-status'),box=$('homework18-candidates');if(status&&status.textContent.includes('Không tìm thấy kết quả khớp chính xác'))status.textContent='';if(box&&box.textContent.includes('Không tìm thấy kết quả khớp chính xác')){box.replaceChildren();box.hidden=true;}});}
async function renderHomework18Candidates(candidates){
 const box=$('homework18-candidates');box.replaceChildren();
 const rawInput=String($('homework18-query')?.value||'').trim(),rawCandidates=Array.isArray(candidates)?candidates:[];
 if(!rawCandidates.length){box.hidden=true;box.replaceChildren();const noResultStatus=$('homework18-status');if(noResultStatus)noResultStatus.textContent='Không tìm thấy kết quả khớp chính xác với nội dung và khoảng cách bạn đã nhập: “'+rawInput+'”. Hệ thống không tự thêm, bớt hoặc nối các âm tiết (ví dụ “ke ren” không được đổi thành “keren”). Vui lòng kiểm tra từ điển và khoảng cách giữa các âm tiết rồi nhập lại.';return null;}
 const sourceList=rawCandidates.filter(item=>typeof homework18ValidVietnameseMeaning!=='function'||homework18ValidVietnameseMeaning(item));
 if(!sourceList.length){box.hidden=false;box.textContent='Có phương án chữ Hán nhưng chưa xác minh được nghĩa tiếng Việt. Vui lòng thử lại sau.';return null;}
 const requestToken=homework18LookupToken,status=$('homework18-status'),queue=sourceList,resolved=new Array(sourceList.length);let cursor=0,completed=0;
 box.hidden=false;box.innerHTML='<div class="homework18-candidate-heading">Đang kiểm tra nghĩa của các câu hoàn chỉnh…</div>';
 if(status)status.textContent='Đang xác minh nghĩa toàn câu: 0 / '+queue.length+'…';
 const worker=async()=>{while(true){const index=cursor++;if(index>=queue.length)return;const item=queue[index];try{
  if(String(item.vi||'').trim()&&homework18ValidVietnameseMeaning(item))resolved[index]=item;
  else{const vi=await machineTranslate(item.zh,'zh-CN','vi'),enriched={...item,vi,note:'Nghĩa tiếng Việt được dịch từ toàn câu.'};resolved[index]=homework18ValidVietnameseMeaning(enriched)?enriched:null;}
 }catch(_){resolved[index]=null;}completed++;if(requestToken===homework18LookupToken&&status)status.textContent='Đang xác minh nghĩa toàn câu: '+completed+' / '+queue.length+'…';}};
 await Promise.all(Array.from({length:Math.min(4,queue.length)},worker));if(requestToken!==homework18LookupToken)return null;
 const list=resolved.filter(Boolean);if(!list.length){box.hidden=true;box.replaceChildren();if(status)status.textContent='Không xác minh được câu hoàn chỉnh có nghĩa tiếng Việt.';return null;}
 homework18Candidates=list;homework18SelectedCandidateIndex=0;let homework18CandidatePage=0;const homework18PageSize=10;box.hidden=false;
 const renderHomework18Page=()=>{
  const pageCount=Math.max(1,Math.ceil(list.length/homework18PageSize)),start=homework18CandidatePage*homework18PageSize,end=Math.min(start+homework18PageSize,list.length);
  const nav=position=>'<div class="homework18-pagination" data-pagination="'+position+'"><button type="button" data-page-prev '+(homework18CandidatePage===0?'disabled':'')+'>‹ Trang trước</button><span>Trang '+(homework18CandidatePage+1)+' / '+pageCount+'</span><button type="button" data-page-next '+(homework18CandidatePage>=pageCount-1?'disabled':'')+'>Trang sau ›</button></div>';
  box.innerHTML=nav('top')+'<div class="homework18-candidate-heading">Chọn câu phù hợp · '+list.length+' kết quả · Hiển thị '+(start+1)+'–'+end+'</div>'+list.slice(start,end).map((item,offset)=>{const index=start+offset;return '<button type="button" class="homework18-candidate" data-homework18-candidate="'+index+'"><span class="homework18-candidate-number">'+(index+1)+'</span><span class="homework18-candidate-content"><span class="homework18-candidate-py">'+escapeHTML(formatHomework18PinyinByInput(String($('homework18-query')?.value||''),item.py||pinyinForChinese(item.zh)))+'</span><span class="homework18-candidate-zh">'+escapeHTML(item.zh)+'</span><span class="homework18-candidate-vi">'+escapeHTML(item.vi||'')+'</span></span></button>';}).join('')+nav('bottom');
  box.querySelectorAll('[data-page-prev]').forEach(button=>button.addEventListener('click',()=>{if(homework18CandidatePage>0){homework18CandidatePage--;renderHomework18Page();}}));
  box.querySelectorAll('[data-page-next]').forEach(button=>button.addEventListener('click',()=>{if(homework18CandidatePage<pageCount-1){homework18CandidatePage++;renderHomework18Page();}}));
  if(!document.documentElement.dataset.homework18ModalClickBound){document.documentElement.dataset.homework18ModalClickBound='1';document.addEventListener('click',event=>{const button=event.target?.closest?.('[data-homework18-candidate]'),current=Array.isArray(homework18Candidates)?homework18Candidates:[],host=$('homework18-candidates');if(!button||!host?.contains(button))return;const index=Number(button.dataset.homework18Candidate),item=current[index];if(!item)return;homework18SelectedCandidateIndex=index;host.querySelectorAll('[data-homework18-candidate]').forEach(node=>node.classList.toggle('is-selected',Number(node.dataset.homework18Candidate)===index));try{openHomework18CandidateModal(item,index,current.length);const liveStatus=$('homework18-status');if(liveStatus)liveStatus.textContent='Đang xem kết quả '+(index+1)+' / '+current.length+'.';}catch(error){console.error('Menu 18 modal error',error);const liveStatus=$('homework18-status');if(liveStatus)liveStatus.textContent='Không mở được hộp chi tiết: '+(error?.message||String(error));}},true);}
 };
 renderHomework18Page();
 if(status)status.textContent='Đã xác minh nghĩa tiếng Việt cho '+list.length+' kết quả. Mỗi trang hiển thị tối đa 10 kết quả. Chạm vào một kết quả để xem chi tiết.';return list[0];
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
.homework18-candidate-py{order:0;color:#1769c2!important;font-size:18px!important;font-weight:850!important;line-height:1.5!important;letter-spacing:.01em;overflow-wrap:anywhere}.homework18-candidate-zh{order:1;color:#7b3fa1!important;font-size:16px!important;font-weight:750!important;line-height:1.4!important}.homework18-candidate-vi{order:2;font-size:12px;line-height:1.45;color:#21805b!important;font-weight:650;overflow-wrap:anywhere}
.homework18-modal-backdrop{position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(15,23,42,.62)}
.homework18-modal{width:min(100%,520px);max-height:min(88dvh,760px);overflow:auto;background:#fff;color:#182230;border-radius:18px;padding:16px;box-shadow:0 20px 60px rgba(0,0,0,.28)}
.homework18-modal-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;font-size:16px}
.homework18-modal-close{border:0;border-radius:50%;width:36px;height:36px;font-size:25px;background:#f2f4f7;color:#344054}
.homework18-modal-line{padding:12px 0;border-bottom:1px solid #eaecf0}
.homework18-modal-line b{display:block;font-size:11px;letter-spacing:.06em;margin-bottom:5px}
.homework18-modal-value{font-size:22px;font-weight:800;line-height:1.45;overflow-wrap:anywhere}
.homework18-modal-line.is-hanzi{color:#7b3fa1}.homework18-modal-line.is-pinyin{color:#1769c2}.homework18-modal-line.is-pinyin .homework18-modal-value{font-size:29px;font-weight:900;line-height:1.5}.homework18-modal-line.is-meaning{color:#21805b}
.homework18-modal-actions{display:flex;flex-wrap:wrap;gap:7px;margin-top:9px}.homework18-modal-actions button{border:1px solid #cbd5e1;border-radius:8px;padding:7px 10px;background:#f8fafc;color:#243247;font-size:12px;font-weight:750;cursor:pointer}
.homework18-modal-nav{display:flex;justify-content:space-between;gap:10px;margin-top:14px}
.homework18-modal-nav button{border:1px solid #d0d5dd;border-radius:9px;padding:9px 14px;background:#f9fafb;font-weight:750}
.homework18-modal-nav button:disabled{opacity:.35}
.homework18-candidate-heading{grid-column:1/-1;font-size:12px;font-weight:800;color:var(--muted,#667085);padding:2px 0}
.homework18-pagination{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;gap:8px;padding:6px 0}
.homework18-pagination span{font-size:12px;font-weight:750;color:var(--muted,#667085);white-space:nowrap}
.homework18-pagination button{border:1px solid #d0d5dd;border-radius:8px;padding:7px 10px;background:#fff;color:#344054;font-size:12px;font-weight:750}
.homework18-pagination button:disabled{opacity:.35;cursor:not-allowed}
.homework18-candidate{display:flex;align-items:flex-start;gap:8px;min-width:0;text-align:left;padding:9px;border:1px solid var(--line,#d0d5dd);border-radius:9px;background:#fff;color:var(--ink,#182230);cursor:pointer}
.homework18-candidate.is-selected{border-color:#864B90;background:#faf5ff;box-shadow:0 0 0 1px #864B90}
.homework18-candidate-number{display:grid;place-items:center;flex:0 0 21px;height:21px;border-radius:6px;background:#f2f4f7;font-size:11px;font-weight:800}
.homework18-candidate-content{display:grid;gap:3px;min-width:0}
.homework18-candidate-zh{font-size:19px;font-weight:850;line-height:1.35;overflow-wrap:anywhere}
.homework18-candidate-py{font-size:11px;line-height:1.4;color:var(--muted,#667085);overflow-wrap:anywhere}
@media(max-width:430px){.homework18-candidates{grid-template-columns:1fr}.homework18-candidate{padding:8px}.homework18-candidate-py{font-size:19px!important}.homework18-candidate-zh{font-size:16px!important}}"""
if source.count(old_css) == 1:
    source = source.replace(old_css, new_css, 1)
elif source.count(new_css) != 1:
    raise SystemExit("Menu 18 multicandidate patch: expected exactly one candidate-list CSS anchor.")

required = [
    "MENU18_MULTICANDIDATE_SENTENCE_SEARCH",
    "let homework18SelectedCandidateIndex=0,homework18CandidateModal=null;",
    "data-homework18-candidate",
    "Chọn câu phù hợp ·",
    "async function renderHomework18Candidates(candidates)",
    "await Promise.all(",
    "openHomework18CandidateModal(item,index,current.length)",
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
