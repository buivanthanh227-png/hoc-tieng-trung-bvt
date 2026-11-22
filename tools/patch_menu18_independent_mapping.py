#!/usr/bin/env python3
"""Replace Menu 18 sentence composition with independent dictionary mapping per input token."""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_menu18_independent_mapping.py <site/index.html>")
target = Path(sys.argv[1])
if not target.is_file():
    raise SystemExit(f"Menu 18 target not found: {target}")
source = target.read_text(encoding="utf-8")
original = source

a = source.find("function pinyinToChineseCandidates(raw){")
b = source.find("\nfunction renderHomework18Card(result,sourceLabel=''){", a)
if a < 0 or b < 0:
    raise SystemExit("Menu 18 mapper boundaries not found")

mapper = r'''function pinyinToChineseCandidates(raw){
 // MENU18_INDEPENDENT_TOKEN_MAPPING_V1: map each original input token separately; never compose a sentence.
 const lexicon=getPinyin18Lexicon();
 const inputTokens=String(raw??'').split(/[\s,，、;；]+/).filter(Boolean);
 const results=[],seen=new Set(),unmatched=[];
 const preferredByTone={
  a:{1:['啊','ā','thán từ biểu thị ngạc nhiên hoặc khẳng định'],2:['啊','á','thán từ biểu thị nghi ngờ; hả'],3:['啊','ǎ','thán từ biểu thị ngạc nhiên hoặc nghi ngờ'],4:['啊','à','thán từ biểu thị đồng ý hoặc nhận ra'],5:['啊','a','thán từ kết thúc câu']},
  le:{4:['乐','lè','vui; vui vẻ'],5:['了','le','trợ từ chỉ hành động đã hoàn thành hoặc thay đổi trạng thái']}
 };
 const toneLabel=tone=>tone===5?'thanh nhẹ':'thanh '+tone;
 function inputToneSequence(rawToken,path){
  const nfd=String(rawToken||'').normalize('NFD').toLowerCase();
  const tonesByLetter=[];let letterIndex=0,pendingTone=null;
  for(const ch of nfd){
   if(/[a-z]/.test(ch)){
    if(pendingTone!==null)tonesByLetter[letterIndex]=pendingTone;
    pendingTone=null;letterIndex++;
   }else if(ch==='\u0304')pendingTone=1;
   else if(ch==='\u0301')pendingTone=2;
   else if(ch==='\u030c')pendingTone=3;
   else if(ch==='\u0300')pendingTone=4;
   else if(/[1-5]/.test(ch)&&letterIndex>0)tonesByLetter[letterIndex-1]=Number(ch);
  }
  if(pendingTone!==null&&letterIndex>0)tonesByLetter[letterIndex-1]=pendingTone;
  let offset=0;
  return path.map(syllable=>{
   const end=offset+syllable.length;let tone=null;
   for(let i=offset;i<end;i++)if(tonesByLetter[i]!==undefined){tone=tonesByLetter[i];break;}
   offset=end;return tone;
  });
 }
 function rowToneSequence(py){
  return String(py||'').trim().split(/\s+/).filter(Boolean).map(part=>pinyin18ToneFromInput(part)||5);
 }
 function cleanMeaning(value){return String(value||'').trim().replace(/^[\s·•；;]+/,'');}
 for(let tokenIndex=0;tokenIndex<inputTokens.length;tokenIndex++){
  const inputToken=inputTokens[tokenIndex];
  const cleanToken=inputToken.replace(/[，,。.!?？；;]+$/,'');
  const base=pinyin18Key(cleanToken);
  if(!base){unmatched.push(inputToken);continue;}
  const paths=pinyin18SyllablePaths(cleanToken,pinyin18Syllables);
  const perToken=new Map();
  for(const path of paths){
   const pathKey=path.join(' '),matches=lexicon.get(pathKey)||[];
   if(!matches.length)continue;
   const requestedTones=inputToneSequence(cleanToken,path);
   for(const entry of matches){
    const row=entry.row||[];
    const zh=String(row[0]||'').trim(),py=String(row[2]||'').trim();
    if(!zh||!py||pinyin18LexiconKey(py)!==pathKey)continue;
    const actualTones=rowToneSequence(py);
    if(actualTones.length!==path.length)continue;
    if(requestedTones.some((tone,index)=>tone!==null&&actualTones[index]!==tone))continue;
    // Bare syllables expose the four standard tones; neutral tone remains available for lexical words or explicit tone 5.
    if(path.length===1&&requestedTones[0]===null&&actualTones[0]===5)continue;
    const toneKey=actualTones.join('-');
    let score=0;
    if(entry.preferredWord)score+=100000;
    if(PINYIN18_COMMON_WORDS[pathKey]?.[0]===zh)score+=90000;
    if(path.length===1&&PINYIN18_COMMON_CHARACTERS[path[0]]===zh)score+=80000;
    if(PINYIN18_SINGLE_TONE_WORDS[base]?.[actualTones[0]]?.[0]===zh)score+=110000;
    if(preferredByTone[base]?.[actualTones[0]]?.[0]===zh)score+=120000;
    score-=Math.max(0,Number(entry.rowIndex)||0)*0.001;
    const prior=perToken.get(toneKey);
    if(prior&&prior.score>=score)continue;
    const preferred=PINYIN18_SINGLE_TONE_WORDS[base]?.[actualTones[0]];
    const special=preferredByTone[base]?.[actualTones[0]];
    const vi=cleanMeaning(special?.[2]||preferred?.[2]||entry.preferredMeaning||row[3]);
    perToken.set(toneKey,{
     zh,trad:String(row[1]||pinyin18Traditional(zh)),py,vi,
     source:'Mục '+(tokenIndex+1)+' · '+inputToken+' · '+actualTones.map(toneLabel).join(' / '),
     inputToken,inputIndex:tokenIndex,toneKey,toneLabel:actualTones.map(toneLabel).join(' / '),
     score,note:'Ánh xạ độc lập theo đúng mục nhập; không ghép với các mục khác.'
    });
   }
  }
  if(!perToken.size){unmatched.push(inputToken);continue;}
  for(const item of [...perToken.values()].sort((x,y)=>x.toneKey.localeCompare(y.toneKey,undefined,{numeric:true}))){
   const identity=tokenIndex+'|'+item.zh+'|'+String(item.py||'').toLowerCase();
   if(seen.has(identity))continue;
   seen.add(identity);results.push(item);
  }
 }
 results.unmatchedTokens=unmatched;
 results.inputTokens=inputTokens;
 return results;
}'''
source = source[:a] + mapper + source[b:]

a = source.find("function renderHomework18Candidates(candidates){")
b = source.find("\nfunction looksLikePinyin18(raw,local){", a)
if a < 0 or b < 0:
    raise SystemExit("Menu 18 candidate renderer boundaries not found")
renderer = r'''function renderHomework18Candidates(candidates){
 const box=$('homework18-candidates');
 box.replaceChildren();
 const list=Array.isArray(candidates)?candidates:[];
 if(!list.length){box.hidden=true;return null;}
 homework18SelectedCandidateIndex=0;
 box.hidden=false;
 box.innerHTML='<div class="homework18-candidate-heading">Các kết quả ánh xạ độc lập ('+list.length+' kết quả)</div>'+list.map((item,index)=>
  '<button type="button" class="homework18-candidate'+(index===0?' is-selected':'')+'" data-homework18-candidate="'+index+'" aria-pressed="'+(index===0?'true':'false')+'">'+
  '<span class="homework18-candidate-number">'+(index+1)+'</span><span class="homework18-candidate-content">'+
  '<span class="homework18-candidate-source">'+escapeHTML(item.source||'Từ điển')+'</span>'+
  '<span class="homework18-candidate-zh">'+escapeHTML(item.zh)+'</span>'+
  '<span class="homework18-candidate-py">'+escapeHTML(formatHomework18PinyinByWord(item.zh,item.py||pinyinForChinese(item.zh)))+'</span></span></button>'
 ).join('');
 const select=index=>{
  if(index<0||index>=list.length)return;
  homework18SelectedCandidateIndex=index;
  const item=list[index];
  box.querySelectorAll('[data-homework18-candidate]').forEach(button=>{
   const selected=Number(button.dataset.homework18Candidate)===index;
   button.classList.toggle('is-selected',selected);
   button.setAttribute('aria-pressed',selected?'true':'false');
  });
  renderHomework18Card({...item,py:formatHomework18PinyinByWord(item.zh,item.py||pinyinForChinese(item.zh))},item.source||('Kết quả '+(index+1)));
  const status=$('homework18-status');
  if(status)status.textContent='Đang xem kết quả '+(index+1)+' / '+list.length+' · mục nhập: '+item.inputToken+'.';
 };
 box.querySelectorAll('[data-homework18-candidate]').forEach(button=>button.addEventListener('click',()=>select(Number(button.dataset.homework18Candidate))));
 select(0);
 return list[0];
}'''
source = source[:a] + renderer + source[b:]

old_intro='Nhập tiếng Việt, chữ Hán hoặc Pinyin không dấu. Với Pinyin, hệ thống tự xét nhiều thanh điệu và ghép thành một câu phù hợp nhất.'
new_intro='Nhập tiếng Việt, chữ Hán hoặc Pinyin. Với Pinyin, hệ thống tra từng mục nhập độc lập và hiển thị các thanh điệu có trong từ điển; không tự ghép các mục thành câu.'
if source.count(old_intro)==1: source=source.replace(old_intro,new_intro,1)
elif source.count(new_intro)!=1: raise SystemExit('Menu 18 intro anchor missing or ambiguous')

old_status="""status.textContent=best.vi
   ?'Đã ghép Pinyin. Bạn có thể xem các phương án ghép khác nếu cần.'
   :'Đã ghép được chữ Hán. Đang tra nghĩa tiếng Việt cho phương án đang chọn…';"""
new_status="status.textContent='Đã ánh xạ độc lập '+candidates.length+' kết quả từ '+(candidates.inputTokens||[]).length+' mục nhập.'+(candidates.unmatchedTokens?.length?' Chưa tìm thấy: '+candidates.unmatchedTokens.join(', '):'');"
if source.count(old_status)==1: source=source.replace(old_status,new_status,1)
elif source.count(new_status)!=1: raise SystemExit('Menu 18 status anchor missing or ambiguous')

old_empty='Không ghép được toàn bộ Pinyin từ dữ liệu hiện có. Hãy kiểm tra âm tiết hoặc thử thêm khoảng trắng; không tạo chữ Hán thay thế.'
new_empty='Không tìm thấy mục từ điển phù hợp cho các mục Pinyin đã nhập. Nội dung nhập được giữ nguyên; không tự tạo chữ Hán thay thế.'
if source.count(old_empty)==1: source=source.replace(old_empty,new_empty,1)
elif source.count(new_empty)!=1: raise SystemExit('Menu 18 empty-result message anchor missing or ambiguous')

old_css='.homework18-candidate-heading{grid-column:1/-1;font-size:12px;font-weight:800;color:var(--muted,#667085);padding:2px 0}'
new_css=old_css+'\n.homework18-candidate-source{font-size:10px;font-weight:750;color:var(--muted,#667085);line-height:1.35;overflow-wrap:anywhere}'
if source.count(old_css)==1 and 'homework18-candidate-source{' not in source: source=source.replace(old_css,new_css,1)
elif source.count('homework18-candidate-source{')!=1: raise SystemExit('Menu 18 candidate source CSS anchor missing or ambiguous')

required=['MENU18_INDEPENDENT_TOKEN_MAPPING_V1','results.unmatchedTokens=unmatched','Các kết quả ánh xạ độc lập','homework18-candidate-source','tra từng mục nhập độc lập','Đã ánh xạ độc lập '+ "'+candidates.length"]
missing=[x for x in required if x not in source]
if missing: raise SystemExit('Menu 18 independent mapping verification failed: '+', '.join(missing))
if source!=original: target.write_text(source,encoding='utf-8',newline='\n')
print('Menu 18 independent token mapping patch: PASS')
