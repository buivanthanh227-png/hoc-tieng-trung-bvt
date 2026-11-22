#!/usr/bin/env python3
"""Patch Menu 18 to map each user-entered Pinyin word independently."""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_menu18_word_mapping.py <site/index.html>")
target = Path(sys.argv[1])
if not target.is_file():
    raise SystemExit(f"Menu 18 patch target not found: {target}")
source = target.read_text(encoding="utf-8")
original = source

def replace_once(old: str, new: str, label: str) -> None:
    global source
    count = source.count(old)
    if count == 0 and source.count(new) == 1:
        return
    if count != 1:
        raise SystemExit(f"Menu 18 word-mapping patch aborted: expected one {label}; found {count}")
    source = source.replace(old, new, 1)

def replace_function(start_marker: str, end_marker: str, replacement: str, label: str) -> None:
    global source
    start = source.find(start_marker)
    if start < 0:
        raise SystemExit(f"Menu 18 word-mapping patch aborted: missing {label} start")
    end = source.find(end_marker, start + len(start_marker))
    if end < 0:
        raise SystemExit(f"Menu 18 word-mapping patch aborted: missing {label} end")
    if source[start:end] == replacement:
        return
    if source.find(start_marker, start + 1) >= 0:
        raise SystemExit(f"Menu 18 word-mapping patch aborted: duplicate {label} start")
    source = source[:start] + replacement + source[end:]

compact_index_code = r"""let pinyin18CompactIndexSource=null,pinyin18CompactIndex=null;
function pinyin18ToneSignature(value){
 return String(value||'').trim().split(/\s+/).filter(Boolean).map(token=>pinyin18ToneFromInput(token)||5).join('');
}
function pinyin18InputToneConstraints(rawToken,pronunciation){
 const syllables=String(pronunciation||'').trim().split(/\s+/).filter(Boolean);
 const raw=String(rawToken||'');
 const expected=[],baseLength=pinyin18Key(raw).length;
 if(!syllables.length||baseLength!==syllables.reduce((sum,item)=>sum+pinyin18Key(item).length,0))return null;
 let offset=0,hasTone=false;
 for(const syllable of syllables){
  const length=pinyin18Key(syllable).length;
  let chunk=raw.slice(offset,offset+length);offset+=length;
  if(/[1-5]/.test(raw[offset]||'')){chunk+=raw[offset];offset++;}
  const tone=pinyin18ToneFromInput(chunk);
  expected.push(tone);
  if(tone!==null)hasTone=true;
 }
 return hasTone?expected:null;
}
function getPinyin18CompactIndex(){
 const lexicon=getPinyin18Lexicon();
 if(pinyin18CompactIndexSource===lexicon&&pinyin18CompactIndex)return pinyin18CompactIndex;
 const index=new Map();
 for(const matches of lexicon.values())for(const item of matches){
  const key=pinyin18Key(item.row?.[2]);
  if(!key)continue;
  if(!index.has(key))index.set(key,[]);
  const list=index.get(key),signature=pinyin18ToneSignature(item.row[2]);
  const identity=String(item.row[0]||'')+'|'+signature;
  if(!list.some(existing=>existing.identity===identity))list.push({...item,identity,toneSignature:signature});
 }
 pinyin18CompactIndexSource=lexicon;pinyin18CompactIndex=index;
 return index;
}"""
if "function getPinyin18CompactIndex(){" not in source:
    anchor = "function pinyinToChineseCandidates(raw){"
    pos = source.find(anchor)
    if pos < 0:
        raise SystemExit("Menu 18 candidate function not found")
    source = source[:pos] + compact_index_code + "\n" + source[pos:]

new_candidates = r"""function pinyinToChineseCandidates(raw){
 const originalInput=String(raw??'');
 const inputTokens=originalInput.trim().split(/[\s,，、;；]+/).filter(Boolean);
 if(!inputTokens.length)return [];
 const compactIndex=getPinyin18CompactIndex(),results=[],missingTokens=[];
 const cleanMeaning=value=>String(value||'').split(/[;；]/)[0].replace(/^[\s·,，;:：-]+/,'').trim();
 for(let wordIndex=0;wordIndex<inputTokens.length;wordIndex++){
  const inputToken=inputTokens[wordIndex],key=pinyin18Key(inputToken);
  if(!key){missingTokens.push(inputToken);continue;}
  const matches=compactIndex.get(key)||[];
  const groups=new Map();
  for(const item of matches){
   const row=item.row,signature=item.toneSignature||pinyin18ToneSignature(row[2]);
   if(!signature||signature.includes('5'))continue;
   const constraints=pinyin18InputToneConstraints(inputToken,row[2]);
   if(constraints){
    const rowTones=String(row[2]||'').trim().split(/\s+/).filter(Boolean).map(token=>pinyin18ToneFromInput(token)||5);
    if(!constraints.every((tone,index)=>tone===null||rowTones[index]===tone))continue;
   }
   if(!groups.has(signature))groups.set(signature,new Map());
   const byHanzi=groups.get(signature),hanzi=String(row[0]||'');
   if(!hanzi)continue;
   const prior=byHanzi.get(hanzi);
   const gloss=cleanMeaning(row[3]);
   const score=(item.preferredWord?1000:0)+(gloss.length>=2?20:0)+(/[À-ỹĐđ]/.test(gloss)?10:0)-Math.log(Number(item.rowIndex||0)+1)*.001;
   if(!prior||score>prior.score)byHanzi.set(hanzi,{item,score});
  }
  if(!groups.size){missingTokens.push(inputToken);continue;}
  const preferredCharacter=PINYIN18_COMMON_CHARACTERS[key]||'';
  const preferredPhrase=Object.entries(PINYIN18_COMMON_WORDS).find(([phrase])=>pinyin18Key(phrase)===key)?.[1]?.[0]||'';
  for(const [signature,byHanzi] of [...groups.entries()].sort((a,b)=>a[0].localeCompare(b[0]))){
   const rows=[...byHanzi.values()].map(value=>value.item).sort((a,b)=>{
    const aPreferred=String(a.row[0])===preferredCharacter||String(a.row[0])===preferredPhrase;
    const bPreferred=String(b.row[0])===preferredCharacter||String(b.row[0])===preferredPhrase;
    if(aPreferred!==bPreferred)return aPreferred?-1:1;
    if(Boolean(a.preferredWord)!==Boolean(b.preferredWord))return a.preferredWord?-1:1;
    return (Number(a.rowIndex)||0)-(Number(b.rowIndex)||0);
   });
   if(!rows.length)continue;
   const primary=rows[0],row=primary.row;
   const details=rows.map(item=>{
    const value=item.row,meaning=cleanMeaning(value[3]);
    return String(value[0]||'')+' ('+String(value[2]||'')+')'+(meaning?' — '+meaning:'');
   });
   const note='Ánh xạ độc lập từ đầu vào “'+inputToken+'” · thanh '+signature.split('').join('-')+'. Có '+rows.length+' mục từ điển cùng nhóm thanh điệu.'+(details.length?' Các mục: '+details.join('；'):'');
   results.push({
    zh:String(row[0]||''),trad:String(row[1]||row[0]||''),py:String(row[2]||'').replace(/\s+/g,''),
    vi:cleanMeaning(row[3]),source:'Từ '+(wordIndex+1)+' · '+inputToken+' · thanh '+signature.split('').join('-'),
    note,wordMapping:true,inputToken,wordIndex,toneSignature:signature,variantCount:rows.length,rawInput:originalInput
   });
  }
 }
 results.missingTokens=missingTokens;
 results.rawInput=originalInput;
 return results;
}"""
replace_function("function pinyinToChineseCandidates(raw){", "\nfunction renderHomework18Card(result,sourceLabel=''){", new_candidates, "Pinyin-to-Chinese mapper")

new_renderer = r"""function renderHomework18Candidates(candidates){
 homework18SelectedIndex=0;
 const box=$('homework18-candidates');
 homework18Candidates=(Array.isArray(candidates)?candidates:[]).filter(item=>item?.wordMapping?Boolean(item.zh):homework18ValidVietnameseMeaning(item));
 if(!homework18Candidates.length){
  box.hidden=true;box.replaceChildren();
  const status=$('homework18-status');
  if(status)status.textContent='Chưa tìm được ánh xạ Pinyin hợp lệ trong từ điển.';
  return null;
 }
 box.hidden=false;
 box.innerHTML='<div class="homework18-candidate-tabs-label">Ánh xạ độc lập theo từng từ · không ghép tổ hợp</div><div class="homework18-candidate-tabs-list">'+
  homework18Candidates.map((item,index)=>'<button type="button" class="homework18-candidate-tab" data-homework18-result="'+index+'" aria-pressed="'+(index===0?'true':'false')+'">Từ '+(Number(item.wordIndex)+1)+' ('+escapeHTML(String(item.inputToken||''))+') · thanh '+escapeHTML(String(item.toneSignature||'').split('').join('-'))+'</button>').join('')+'</div>';
 const choose=index=>{
  const item=homework18Candidates[index];if(!item)return;
  homework18SelectedIndex=index;
  box.querySelectorAll('[data-homework18-result]').forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.homework18Result)===index)));
  const label='Từ '+(Number(item.wordIndex)+1)+' · '+String(item.inputToken||'')+' · thanh '+String(item.toneSignature||'').split('').join('-');
  renderHomework18Card({...item,py:String(item.py||'').replace(/\s+/g,'')},label);
  const status=$('homework18-status');
  if(status){
   const missing=Array.isArray(candidates.missingTokens)?candidates.missingTokens:[];
   status.textContent='Đã ánh xạ '+new Set(homework18Candidates.map(value=>value.wordIndex)).size+'/'+String(candidates.rawInput||'').trim().split(/[\s,，、;；]+/).filter(Boolean).length+' từ; có '+homework18Candidates.length+' nhóm thanh điệu độc lập. '+(missing.length?'Không tìm thấy trong từ điển: '+missing.join(', ')+'.':'Không tạo tổ hợp giữa các từ.');
  }
 };
 box.querySelectorAll('[data-homework18-result]').forEach(button=>button.addEventListener('click',()=>choose(Number(button.dataset.homework18Result))));
 choose(0);
 return homework18Candidates[0];
}"""
replace_function("function renderHomework18Candidates(candidates){", "\nfunction looksLikePinyin18(raw,local){", new_renderer, "word-level result renderer")

replace_once(
    "const token=++homework18LookupToken,raw=$('homework18-query').value.trim(),box=$('homework18-results'),status=$('homework18-status');",
    "const token=++homework18LookupToken,raw=$('homework18-query').value,query=raw.trim(),box=$('homework18-results'),status=$('homework18-status');",
    "preserve raw input in lookup handler"
)
replace_once("const local=tryLocalTranslation(raw),hasChinese=", "const local=tryLocalTranslation(query),hasChinese=", "trim only for local translation")
replace_once("if(!raw){status.textContent='Nhập câu tiếng Việt, chữ Hán hoặc Pinyin để dịch.';", "if(!query){status.textContent='Nhập câu tiếng Việt, chữ Hán hoặc Pinyin để dịch.';", "empty input check")
replace_once("machineTranslate(raw,source,target)", "machineTranslate(query,source,target)", "trim machine translation query")
replace_once("OFFLINE_SENTENCE_TRANSLATIONS[norm(raw)]", "OFFLINE_SENTENCE_TRANSLATIONS[norm(query)]", "trim offline translation lookup")

old_lookup_status = """  status.textContent=best.vi
   ?'Đã ghép Pinyin. Bạn có thể xem các phương án ghép khác nếu cần.'
   :'Đã ghép được chữ Hán. Đang tra nghĩa tiếng Việt cho phương án đang chọn…';"""
mapping_status_branch = """  if(best.wordMapping){
   const mappedWords=new Set(candidates.map(item=>item.wordIndex)).size;
   const totalWords=String(candidates.rawInput||raw).trim().split(/[\\s,，、;；]+/).filter(Boolean).length;
   const missing=Array.isArray(candidates.missingTokens)?candidates.missingTokens:[];
   status.textContent='Đã ánh xạ '+mappedWords+'/'+totalWords+' từ thành '+candidates.length+' nhóm thanh điệu độc lập. '+(missing.length?'Không tìm thấy: '+missing.join(', ')+'.':'Không tạo tổ hợp giữa các từ.');
   return;
  }"""
if mapping_status_branch in source:
    source=source.replace(mapping_status_branch+'\n'+mapping_status_branch,mapping_status_branch,1)
elif old_lookup_status in source:
    source=source.replace(old_lookup_status,mapping_status_branch+'\n'+old_lookup_status,1)
else:
    raise SystemExit("Menu 18 word-mapping patch aborted: lookup status anchor missing")

new_pinyin_detector = r"""function looksLikePinyin18(raw,local){
 if(/[\u3400-\u9fff]/.test(raw)||local&&norm(raw)===norm(local.vi)||/[ăâđêôơư]/i.test(raw))return false;
 getPinyin18Lexicon();
 const tokens=String(raw||'').trim().split(/[\s,，、;；]+/).filter(Boolean);
 if(!tokens.length||!tokens.every(token=>/^[A-Za-züÜvV:1-5]+$/.test(token)))return false;
 const compactIndex=getPinyin18CompactIndex();
 return tokens.some(token=>compactIndex.has(pinyin18Key(token)));
}"""
replace_function("function looksLikePinyin18(raw,local){", "\nlet homework18LookupToken=0;", new_pinyin_detector, "Pinyin input detector")

old_no_candidates = """  if(!candidates.length){status.textContent='Không ghép được toàn bộ Pinyin từ dữ liệu hiện có. Hãy kiểm tra âm tiết hoặc thử thêm khoảng trắng; không tạo chữ Hán thay thế.';box.innerHTML='<div class=\"empty\">Không tìm thấy kết quả ghép Pinyin hợp lệ.</div>';return;}"""
new_no_candidates = """  if(!candidates.length){const missing=Array.isArray(candidates.missingTokens)?candidates.missingTokens:[];status.textContent='Không tìm thấy mục từ điển cho '+(missing.length?missing.join(', '):'nội dung đã nhập')+'. Không tạo chữ Hán thay thế.';box.innerHTML='<div class=\"empty\">Không tìm thấy ánh xạ Pinyin hợp lệ trong từ điển.</div>';return;}"""
if old_no_candidates in source:
    source=source.replace(old_no_candidates,new_no_candidates,1)
elif new_no_candidates not in source:
    raise SystemExit("Menu 18 empty-result message anchor missing")

old_validator = """function homework18ValidVietnameseMeaning(item){
 const meaning=String(item?.preferredMeaning||item?.vi||'').trim();
 const hanzi=String(item?.zh||'');"""
new_validator = """function homework18ValidVietnameseMeaning(item){
 if(item?.wordMapping)return Boolean(String(item?.zh||'').trim());
 const meaning=String(item?.preferredMeaning||item?.vi||'').trim();
 const hanzi=String(item?.zh||'');"""
if old_validator in source:
    source=source.replace(old_validator,new_validator,1)
elif new_validator not in source:
    raise SystemExit("Menu 18 candidate validator anchor missing")

required = [
    "function getPinyin18CompactIndex()",
    "function pinyin18InputToneConstraints(rawToken,pronunciation)",
    "function pinyinToChineseCandidates(raw){",
    "results.missingTokens=missingTokens",
    "wordMapping:true",
    "Ánh xạ độc lập theo từng từ · không ghép tổ hợp",
]
missing=[needle for needle in required if needle not in source]
if missing:
    raise SystemExit("Menu 18 word-mapping verification failed: "+", ".join(missing))
if "state.rows.concat(item.row)" in source:
    raise SystemExit("Menu 18 retired Cartesian beam path remains active")

if source!=original:
    target.write_text(source,encoding='utf-8',newline='\n')
print("Menu 18 independent word-mapping patch: verified")
print("Input preserved; dictionary rows grouped by tone signature; result count is additive, not Cartesian.")
