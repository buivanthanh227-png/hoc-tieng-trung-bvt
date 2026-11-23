/* Menu 3 Pinyin composer fix · V42.10.22.1 */
(function(){
 'use strict';
 if(!document.getElementById('homework3x-query'))return;
 if(typeof getPinyin18SourceIndex!=='function'||typeof pinyin18InputToken!=='function'||
    typeof pinyin18InputInfosMatchSource!=='function'||typeof pinyin18ToneFromInput!=='function')return;
 try{pinyin3xComposerSourceIndex=null;pinyin3xComposerIndex=null;}catch(_){}

 function segmentToken(rawToken,syllables,maxResults,groupIndex){
  const parsed=pinyin18InputToken(rawToken),base=parsed.base;
  if(!base||base.length>24)return [];
  const results=[];
  const walk=(offset,path)=>{
   if(results.length>=maxResults)return;
   if(offset===base.length){results.push(path.slice());return;}
   for(let next=Math.min(base.length,offset+6);next>offset;next--){
    const part=base.slice(offset,next);if(!syllables.has(part))continue;
    const tones=parsed.tones.filter(mark=>mark.numeric?mark.offset===next:mark.offset>=offset&&mark.offset<next).map(mark=>({...mark,offset:mark.offset-offset}));
    path.push({base:part,tones,group:groupIndex});walk(next,path);path.pop();
    if(results.length>=maxResults)return;
   }
  };
  walk(0,[]);return results;
 }

 function buildInputOptions(raw,syllables,maxOptions){
  const source=String(raw||''),matches=[...source.matchAll(/[^\s,，、;；.!?！？]+/g)];
  if(!matches.length)return [];
  let combined=[[]];
  for(let index=0;index<matches.length;index++){
   const choices=segmentToken(matches[index][0],syllables,64,index);
   if(!choices.length)return [];
   const next=[];
   for(const prefix of combined){
    for(const choice of choices){next.push(prefix.concat(choice));if(next.length>=maxOptions)break;}
    if(next.length>=maxOptions)break;
   }
   combined=next;
  }
  const seen=new Set();
  return combined.filter(option=>{
   const key=option.map(item=>item.base+':'+item.tones.map(t=>t.offset+'-'+t.tone).join(',')+'@'+item.group).join('|');
   if(seen.has(key))return false;seen.add(key);return true;
  });
 }

 function getComposerIndex(){
  const sourceIndex=getPinyin18SourceIndex();
  if(pinyin3xComposerSourceIndex===sourceIndex&&pinyin3xComposerIndex)return pinyin3xComposerIndex;
  const seedRows=[...(typeof seed!=='undefined'&&Array.isArray(seed)?seed:[]),...(typeof extraSeed!=='undefined'&&Array.isArray(extraSeed)?extraSeed:[])];
  const seedByKey=new Map();
  for(const row of seedRows){
   const zh=String(row?.[0]||'').trim(),py=String(row?.[2]||'').trim();if(!zh||!py)continue;
   const compact=py.split(/\s+/).map(pinyin18Key).join('');if(compact)seedByKey.set(zh+'|'+compact,{level:String(row?.[4]||''),py});
  }
  const byCompact=new Map(),dedupe=new Map();
  for(const item of sourceIndex.entries){
   const zh=String(item.zh||'').trim(),py=String(item.py||'').trim();
   if(!/^[\u3400-\u9fff\uf900-\ufaff]{1,6}$/.test(zh)||!py)continue;
   if(typeof homework3xValidVietnameseMeaning==='function'&&!homework3xValidVietnameseMeaning(item))continue;
   const tokens=py.split(/\s+/).filter(Boolean),compact=tokens.map(pinyin18Key).join('');
   if(!compact||compact.length>30||tokens.some(token=>!pinyin18Key(token)))continue;
   const chars=[...zh],seedData=seedByKey.get(zh+'|'+compact),seedExact=!!seedData,level=seedData?.level||'';
   const levelBonus=/HSK\s*1|HSK1/i.test(level)?100:/HSK\s*2|HSK2/i.test(level)?75:/HSK\s*3|HSK3/i.test(level)?50:/HSK\s*4|HSK4/i.test(level)?25:0;
   const score=(chars.length>1?180+Math.min(chars.length,6)*28:24)+(seedExact?160+levelBonus:0)+(item.priority===100?12:0);
   const identity=zh+'|'+compact,previous=dedupe.get(identity);
   const entry={...item,zh,py:seedData?.py||py,compact,score,seedExact,chars:chars.length};
   if(!previous||entry.score>previous.score)dedupe.set(identity,entry);
  }
  for(const entry of dedupe.values()){if(!byCompact.has(entry.compact))byCompact.set(entry.compact,[]);byCompact.get(entry.compact).push(entry);}
  for(const entries of byCompact.values()){entries.sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh));if(entries.length>96)entries.length=96;}
  pinyin3xComposerSourceIndex=sourceIndex;pinyin3xComposerIndex={byCompact,entryCount:dedupe.size};return pinyin3xComposerIndex;
 }

 function applyTone(rawSyllable,tone){
  const original=String(rawSyllable||'').trim();if(!original)return original;
  const normalized=original.replace(/u:/gi,'ü').replace(/v/gi,'ü').normalize('NFD'),hasUmlaut=normalized.includes('\u0308');
  let base=normalized.replace(/[\u0300-\u036f]/g,'');if(hasUmlaut)base=base.replace(/u/g,'ü');
  if(!tone||tone===5||tone<1||tone>4)return base;
  let at=base.indexOf('a');if(at<0)at=base.indexOf('e');if(at<0&&base.includes('ou'))at=base.indexOf('o');
  if(at<0)for(let i=base.length-1;i>=0;i--)if('aeiouü'.includes(base[i])){at=i;break;}
  if(at<0)return base;
  const map={a:['ā','á','ǎ','à'],e:['ē','é','ě','è'],i:['ī','í','ǐ','ì'],o:['ō','ó','ǒ','ò'],u:['ū','ú','ǔ','ù'],ü:['ǖ','ǘ','ǚ','ǜ']};
  const marked=map[base[at]]?.[tone-1];if(!marked)return base;
  const output=base.slice(0,at)+marked+base.slice(at+1);
  return /^[A-Z]/.test(original)?output.charAt(0).toUpperCase()+output.slice(1):output;
 }

 function renderPinyinPreservingInput(raw,input,entries){
  const source=String(raw||''),matches=[...source.matchAll(/[^\s,，、;；.!?！？]+/g)];
  if(!matches.length||!input.length)return '';
  const units=[];for(const entry of entries)units.push(...String(entry.py||'').trim().split(/\s+/).filter(Boolean));
  if(units.length!==input.length)return '';
  for(let i=0;i<input.length;i++)if(pinyin18Key(units[i])!==input[i].base)return '';
  const groups=Array.from({length:matches.length},()=>[]);
  for(let i=0;i<input.length;i++){
   const entered=input[i].tones?.[0]?.tone,canonical=pinyin18ToneFromInput(units[i]),tone=entered===undefined?canonical:entered,group=input[i].group;
   if(!Number.isInteger(group)||group<0||group>=groups.length)return '';
   groups[group].push(applyTone(units[i],tone));
  }
  const leading=source.slice(0,matches[0].index),last=matches[matches.length-1];
  const trailing=source.slice(last.index+last[0].length);
  let output=leading+groups[0].join('');
  for(let i=1;i<groups.length;i++)output+=source.slice(matches[i-1].index+matches[i-1][0].length,matches[i].index)+groups[i].join('');
  output+=trailing;
  return output.replace(/^(\s*)([a-zü])/i,(whole,prefix,first)=>prefix+first.toUpperCase());
 }

 function composeSentence(raw){
  const sourceIndex=getPinyin18SourceIndex(),composer=getComposerIndex(),options=buildInputOptions(raw,sourceIndex.syllables,128);
  if(!options.length)return {status:'none'};
  const resultsByHanzi=new Map();
  for(const input of options){
   const states=Array.from({length:input.length+1},()=>[]);states[0]=[{score:0,zh:'',entries:[]}];
   const add=(pos,candidate)=>{
    const bucket=states[pos],prior=bucket.find(item=>item.zh===candidate.zh);
    if(prior){if(candidate.score>prior.score)Object.assign(prior,candidate);}else bucket.push(candidate);
    bucket.sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh));if(bucket.length>32)bucket.length=32;
   };
   for(let start=0;start<input.length;start++){
    if(!states[start].length)continue;
    for(let end=start+1;end<=Math.min(input.length,start+6);end++){
     const span=input.slice(start,end),compact=span.map(item=>item.base).join('');
     for(const entry of composer.byCompact.get(compact)||[]){
      if(!pinyin18InputInfosMatchSource(entry,span))continue;
      for(const path of states[start])add(end,{score:path.score+entry.score-4,zh:path.zh+entry.zh,entries:path.entries.concat(entry)});
     }
    }
   }
   for(const path of states[input.length]){
    const py=renderPinyinPreservingInput(raw,input,path.entries);if(!py)continue;
    const prior=resultsByHanzi.get(path.zh);if(!prior||path.score>prior.score)resultsByHanzi.set(path.zh,{...path,py});
   }
  }
  const results=[...resultsByHanzi.values()].sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh));
  if(!results.length)return {status:'none'};
  const best=results[0].score,top=results.filter(item=>best-item.score<=12).slice(0,6);
  const final=top.map(item=>{
   let zh=item.zh;if(/[?？]$/.test(String(raw||'').trim())||/[吗呢]$/.test(zh))zh=zh.replace(/[。.!?！？]*$/,'')+'？';
   return {zh,py:item.py,score:item.score};
  });
  return final.length===1?{status:'ok',...final[0]}:{status:'ambiguous',options:final};
 }

 window.pinyin3xSegmentInputToken=segmentToken;
 window.pinyin3xBuildInputOptions=(raw,syllables,maxOptions=128)=>buildInputOptions(raw,syllables,maxOptions);
 window.getPinyin3xComposerIndex=getComposerIndex;
 window.composePinyinSentence3x=composeSentence;
 window.formatHomework3xPinyinByWord=function(zh,py){return String(py||'');};
 const intro=document.querySelector('#panel-translate3 .quick-translate-intro');
 if(intro)intro.textContent='Nhập tiếng Việt, chữ Hán hoặc Pinyin. Pinyin được tra cứu nguyên cụm trước; nếu không có mục từ/câu hoàn chỉnh, hệ thống sẽ phân tích âm tiết và ghép câu từ các mục từ có trong từ điển.';
 document.documentElement.dataset.menu3PinyinFix='42.10.22.1';
})();

/* MENU3_PRESERVE_MENU18_TONE_CANDIDATES_V2 */
(function(){
 'use strict';
 if(!document.getElementById('homework3x-query'))return;
 const $=id=>document.getElementById(id);
 const toneMap={a:['ā','á','ǎ','à'],e:['ē','é','ě','è'],i:['ī','í','ǐ','ì'],o:['ō','ó','ǒ','ò'],u:['ū','ú','ǔ','ù'],ü:['ǖ','ǘ','ǚ','ǜ']};
 function tonePinyin(raw,tone){
  const original=String(raw||'');let value=original.replace(/u:/gi,'ü').replace(/v/gi,'ü');
  const nfd=value.normalize('NFD'),hasDiaeresis=nfd.includes('\u0308');
  let base=nfd.replace(/[\u0300-\u036f]/g,'');if(hasDiaeresis)base=base.replace(/u/g,'ü');
  if(!tone||tone===5||tone<1||tone>4)return base;
  let at=base.indexOf('a');if(at<0)at=base.indexOf('e');if(at<0&&base.includes('ou'))at=base.indexOf('o');
  if(at<0)for(let i=base.length-1;i>=0;i--)if('aeiouü'.includes(base[i])){at=i;break;}
  const mark=toneMap[base[at]]?.[tone-1];if(!mark)return base;
  let out=base.slice(0,at)+mark+base.slice(at+1);
  if(/^[A-Z]/.test(original))out=out.charAt(0).toUpperCase()+out.slice(1);
  return out;
 }
 function exactSpacingPinyin(raw,input,entries){
  const source=String(raw||''),matches=[...source.matchAll(/[^\s,，、;；.!?！？]+/g)];
  const syllables=[];for(const entry of entries)syllables.push(...String(entry.py||'').trim().split(/\s+/).filter(Boolean));
  if(!matches.length||syllables.length!==input.length)return '';
  for(let i=0;i<input.length;i++)if(pinyin18Key(syllables[i])!==input[i].base)return '';
  const groups=Array.from({length:matches.length},()=>[]);
  for(let i=0;i<input.length;i++){
   const explicit=input[i].tones?.[0]?.tone;
   const tone=explicit===undefined?pinyin18ToneFromInput(syllables[i]):explicit;
   const group=input[i].group;
   if(!Number.isInteger(group)||!groups[group])return '';
   groups[group].push(tonePinyin(syllables[i],tone));
  }
  const last=matches[matches.length-1];
  let output=source.slice(0,matches[0].index)+groups[0].join('');
  for(let i=1;i<groups.length;i++)output+=source.slice(matches[i-1].index+matches[i-1][0].length,matches[i].index)+groups[i].join('');
  output+=source.slice(last.index+last[0].length);
  return output.replace(/^(\s*)([a-zü])/i,(_,space,ch)=>space+ch.toUpperCase());
 }
 function composeAll(raw){
  const sourceIndex=getPinyin18SourceIndex(),composer=getPinyin3xComposerIndex();
  const options=window.pinyin3xBuildInputOptions?.(raw,sourceIndex.syllables,512)||[];
  if(!options.length)return {status:'none'};
  const results=new Map();
  for(const input of options){
   const states=Array.from({length:input.length+1},()=>[]);
   states[0]=[{score:0,zh:'',entries:[]}];
   const add=(position,candidate)=>{
    const bucket=states[position],prior=bucket.find(item=>item.zh===candidate.zh);
    if(prior){if(candidate.score>prior.score)Object.assign(prior,candidate);}else bucket.push(candidate);
    bucket.sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh));if(bucket.length>96)bucket.length=96;
   };
   for(let start=0;start<input.length;start++){
    if(!states[start].length)continue;
    for(let end=start+1;end<=Math.min(input.length,start+6);end++){
     const span=input.slice(start,end),compact=span.map(item=>item.base).join('');
     for(const entry of composer.byCompact.get(compact)||[]){
      if(!pinyin18InputInfosMatchSource(entry,span))continue;
      for(const path of states[start])add(end,{score:path.score+entry.score-3,zh:path.zh+entry.zh,entries:path.entries.concat(entry)});
     }
    }
   }
   for(const path of states[input.length]){
    const py=exactSpacingPinyin(raw,input,path.entries);if(!py)continue;
    const vi=path.entries.map(entry=>String(entry.vi||'').trim()).filter(Boolean).join(' ');
    const prior=results.get(path.zh);
    if(!prior||path.score>prior.score)results.set(path.zh,{zh:path.zh,py,vi,score:path.score,entries:path.entries,sourceLabel:'Ghép từ các mục từ điển'});
   }
  }
  const sorted=[...results.values()].sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh));
  if(!sorted.length)return {status:'none'};
  const best=sorted[0].score,threshold=Math.max(40,Math.ceil(Math.abs(best)*0.18));
  const optionsOut=sorted.filter(item=>best-item.score<=threshold).slice(0,100);
  return optionsOut.length===1?{status:'ok',...optionsOut[0]}:{status:'ambiguous',options:optionsOut};
 }
 function renderList(candidates){
  const host=$('homework3x-candidates');if(!host)return null;
  const list=(Array.isArray(candidates)?candidates:[]).filter(item=>item&&item.zh&&item.py&&item.vi);
  if(!list.length){host.replaceChildren();host.hidden=true;return null;}
  list.sort((a,b)=>(b.score||b.priority||0)-(a.score||a.priority||0));
  homework3xCandidates=list;homework3xSelectedCandidateIndex=0;host.hidden=false;
  let page=0;const pageSize=10;
  const render=()=>{
   const pageCount=Math.max(1,Math.ceil(list.length/pageSize)),start=page*pageSize,items=list.slice(start,start+pageSize);
   host.replaceChildren();
   const makeNav=()=>{
    const nav=document.createElement('div');nav.className='homework3x-pagination';
    nav.innerHTML='<button type="button" data-page-prev>‹ Trang trước</button><span>Trang '+(page+1)+' / '+pageCount+' · '+list.length+' kết quả</span><button type="button" data-page-next>Trang sau ›</button>';
    nav.querySelector('[data-page-prev]').disabled=page===0;nav.querySelector('[data-page-next]').disabled=page>=pageCount-1;
    nav.querySelector('[data-page-prev]').addEventListener('click',()=>{if(page>0){page--;render();}});
    nav.querySelector('[data-page-next]').addEventListener('click',()=>{if(page<pageCount-1){page++;render();}});
    return nav;
   };
   host.appendChild(makeNav());
   const grid=document.createElement('div');grid.className='homework3x-candidate-grid';
   items.forEach((item,offset)=>{
    const index=start+offset,button=document.createElement('button');button.type='button';button.className='homework3x-candidate';button.dataset.homework3xCandidate=String(index);
    const number=document.createElement('span');number.className='homework3x-candidate-number';number.textContent=String(index+1);
    const content=document.createElement('span');content.className='homework3x-candidate-content';
    const py=document.createElement('span');py.className='homework3x-candidate-py';py.textContent=item.py;
    const zh=document.createElement('span');zh.className='homework3x-candidate-zh';zh.textContent=item.zh;
    const vi=document.createElement('span');vi.className='homework3x-candidate-vi';vi.textContent=item.vi;
    content.append(py,zh,vi);button.append(number,content);
    button.addEventListener('click',()=>{homework3xSelectedCandidateIndex=index;openHomework3xCandidateModal(item,index,list.length);});
    grid.appendChild(button);
   });
   host.appendChild(grid);host.appendChild(makeNav());
  };
  render();
  const status=$('homework3x-status');if(status)status.textContent='Có '+list.length+' phương án Pinyin–chữ Hán–nghĩa tiếng Việt. Hiển thị 10 kết quả mỗi trang; chạm vào thẻ có số thứ tự để mở hộp thoại chi tiết.';
  if(!document.documentElement.dataset.menu3CandidateClickV2){
   document.documentElement.dataset.menu3CandidateClickV2='1';
   document.addEventListener('click',event=>{
    const button=event.target?.closest?.('[data-homework3x-candidate]'),box=$('homework3x-candidates');
    if(!button||!box?.contains(button))return;
    const index=Number(button.dataset.homework3xCandidate),item=homework3xCandidates[index];if(!item)return;
    homework3xSelectedCandidateIndex=index;
    try{return;}
    catch(error){const live=$('homework3x-status');if(live)live.textContent='Không mở được chi tiết kết quả: '+String(error?.message||error);}
   },true);
  }
  return list[0];
 }
 function noResultDialog(raw){
  document.querySelector('.homework3x-spacing-dialog')?.remove();
  const layer=document.createElement('div');layer.className='homework3x-modal-backdrop homework3x-spacing-dialog';
  const panel=document.createElement('section');panel.className='homework3x-modal';panel.setAttribute('role','dialog');panel.setAttribute('aria-modal','true');
  const title=document.createElement('h3');title.textContent='Chưa tìm thấy cách ghép Pinyin';
  const msg=document.createElement('p');msg.textContent='Hệ thống chưa tìm được tổ hợp chữ Hán có nghĩa phù hợp với “'+raw+'”. Vui lòng kiểm tra lại chính tả, dấu thanh hoặc khoảng cách giữa các âm tiết rồi thử lại.';
  const close=document.createElement('button');close.type='button';close.className='homework3x-modal-close';close.textContent='Đóng';
  panel.append(title,msg,close);layer.appendChild(panel);document.body.appendChild(layer);
  close.addEventListener('click',()=>layer.remove());layer.addEventListener('click',event=>{if(event.target===layer)layer.remove();});
 }
 const oldDirect=window.pinyinToChineseCandidates;
 if(typeof oldDirect==='function'){
  window.pinyinToChineseCandidates=function(raw){
   const source=oldDirect(raw)||[],sourceIndex=getPinyin18SourceIndex(),parsed=window.pinyin3xBuildInputOptions?.(raw,sourceIndex.syllables,128)||[];
   return source.map(item=>{
    for(const input of parsed){const py=exactSpacingPinyin(raw,input,[item]);if(py)return {...item,py};}
    return item;
   });
  };
 }
 window.composePinyinSentence3x=composeAll;
 window.renderPinyinCompositionOptions3x=function(options){renderList(options);};
 window.renderHomework3xCandidates=async function(candidates){return renderList(candidates);};
 const oldLookup=window.lookupHomework3x;
 if(typeof oldLookup==='function'){
  window.lookupHomework3x=async function(){
   const raw=String($('homework3x-query')?.value||'');
   await oldLookup.apply(this,arguments);
   const status=String($('homework3x-status')?.textContent||''),host=$('homework3x-candidates');
   if(raw.trim()&&typeof looksLikePinyin3x==='function'&&looksLikePinyin3x(raw,tryLocalTranslation(raw))&&/Chưa tìm được|Không tìm thấy/i.test(status)&&(!host||!host.querySelector('[data-homework3x-candidate]')))noResultDialog(raw);
  };
 }
 if(typeof document.createElement==='function'){
 const style=document.createElement('style');style.id='menu3-tone-candidate-layout-v2';
 style.textContent=[
  '#homework3x-candidates .homework3x-candidate-grid{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:8px!important}',
  '#homework3x-candidates .homework3x-candidate{min-width:0!important;padding:9px 7px!important;display:grid!important;grid-template-columns:auto minmax(0,1fr)!important;align-items:start!important;gap:6px!important}',
  '#homework3x-candidates .homework3x-candidate-number{display:grid!important;place-items:center!important;min-width:23px!important;height:23px!important;border-radius:7px!important;background:#f0f2f5!important;color:#1f2937!important;font-size:12px!important;font-weight:850!important}',
  '#homework3x-candidates .homework3x-candidate-content{display:flex!important;flex-direction:column!important;gap:3px!important;min-width:0!important;width:100%!important}',
  '#homework3x-candidates .homework3x-candidate-py{order:0!important;font-size:clamp(15px,1.65vw,20px)!important;line-height:1.35!important;font-weight:900!important;overflow-wrap:anywhere!important}',
  '#homework3x-candidates .homework3x-candidate-zh{order:1!important;font-size:14px!important;line-height:1.35!important;font-weight:750!important;overflow-wrap:anywhere!important}',
  '#homework3x-candidates .homework3x-candidate-vi{order:2!important;font-size:11px!important;line-height:1.35!important;overflow-wrap:anywhere!important}',
  '.homework3x-modal-line.is-hanzi .homework3x-modal-value,.homework3x-modal-line.is-pinyin .homework3x-modal-value,.homework3x-modal-line.is-meaning .homework3x-modal-value{font-size:22px!important;font-weight:800!important;line-height:1.45!important}',
  '@media(max-width:720px){#homework3x-candidates .homework3x-candidate-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:6px!important}#homework3x-candidates .homework3x-candidate{padding:8px 5px!important}}'
 ].join('\n');
 document.head.appendChild(style);
 }
 document.documentElement.dataset.menu3PinyinFix='42.10.22.1';
 document.documentElement.dataset.menu3ToneCandidates='2';
})();
