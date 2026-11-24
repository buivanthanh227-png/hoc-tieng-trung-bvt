/* Menu 3 recovery · reuse the verified Menu 18 sentence mapper; V42.10.23 */
(function(){
 'use strict';
 const root=document.documentElement;
 if(!root||root.dataset.bvtMenu3VerifiedMapperV421023)return;
 root.dataset.bvtMenu3VerifiedMapperV421023='1';

 /* Immediate press feedback for touch, mouse, keyboard and all 17 menus. */
 const style=document.createElement('style');
 style.id='bvt-global-button-press-v421023';
 style.textContent=[
  'button,input[type=button],input[type=submit],[role=button],[role=tab],.btn,.tab,.menu-button,.tool-button,[data-action]{-webkit-tap-highlight-color:transparent;touch-action:manipulation;transition:transform 110ms ease,filter 110ms ease,box-shadow 110ms ease!important}',
  '.bvt-press-active{transform:translateY(2px) scale(.965)!important;filter:brightness(.86)!important;box-shadow:inset 0 3px 7px rgba(0,0,0,.24)!important}',
  'button:active,input[type=button]:active,input[type=submit]:active,[role=button]:active,[role=tab]:active,.btn:active,.tab:active,.menu-button:active,.tool-button:active{transform:translateY(2px) scale(.965)!important;filter:brightness(.86)!important;box-shadow:inset 0 3px 7px rgba(0,0,0,.24)!important}',
  '#homework3x-candidates .homework3x-candidate-grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:10px!important;align-items:stretch!important}',
  '#homework3x-candidates .homework3x-candidate{display:flex!important;align-items:flex-start!important;gap:10px!important;width:100%!important;min-width:0!important;min-height:150px!important;padding:12px!important;border:1.5px solid #dfe5ec!important;border-radius:15px!important;background:#fff!important;text-align:left!important;white-space:normal!important;box-shadow:0 1px 2px rgba(15,23,42,.04)!important}',
  '#homework3x-candidates .homework3x-candidate-content{display:flex!important;flex:1!important;flex-direction:column!important;gap:7px!important;min-width:0!important}',
  '#homework3x-candidates .homework3x-pagination{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:8px!important;margin:12px 0!important;flex-wrap:nowrap!important}',
  '#homework3x-candidates .homework3x-pagination.single-page{display:none!important}',
  '#homework3x-candidates .homework3x-pagination button{padding:9px 12px!important;border:1px solid #cbd5e1!important;border-radius:10px!important;background:#fff!important;font-weight:750!important;color:#344256!important}',
  '#homework3x-candidates .homework3x-pagination button:disabled{opacity:.4!important}',
  '.homework3x-modal-backdrop button{transition:transform 110ms ease,filter 110ms ease!important}',
  '.homework3x-modal-backdrop button:active{transform:translateY(2px) scale(.965)!important;filter:brightness(.86)!important}',
  '@media(max-width:600px){#homework3x-candidates .homework3x-candidate-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important}#homework3x-candidates .homework3x-candidate{min-height:140px!important;padding:9px!important}#homework3x-candidates .homework3x-candidate-number{flex:0 0 25px!important;width:25px!important;height:25px!important;font-size:13px!important}}',
  '@media(max-width:360px){#homework3x-candidates .homework3x-candidate-grid{grid-template-columns:1fr!important}}',
  '@media(prefers-reduced-motion:reduce){button,input[type=button],input[type=submit],[role=button],[role=tab],.btn,.tab,.menu-button,.tool-button{transition:none!important}}'
 ].join('\n');
 (document.head||root).appendChild(style);

 const selector='button,input[type=button],input[type=submit],[role=button],[role=tab],.btn,.tab,.menu-button,.tool-button,[data-action]';
 const pressed=new Map();
 const findControl=target=>{
  if(!target)return null;
  if(typeof target.closest==='function')return target.closest(selector);
  return null;
 };
 const applyPress=element=>{
  if(!element||element.disabled||element.getAttribute?.('aria-disabled')==='true')return;
  element.classList?.add('bvt-press-active');
 };
 const releasePress=element=>{
  if(!element)return;
  const remove=()=>element.classList?.remove('bvt-press-active');
  if(typeof window!=='undefined'&&typeof window.setTimeout==='function')window.setTimeout(remove,110);
  else remove();
 };
 document.addEventListener('pointerdown',event=>{
  const element=findControl(event.target);if(!element||element.disabled)return;
  applyPress(element);pressed.set(event.pointerId,element);
 },true);
 const releasePointer=event=>{
  const element=pressed.get(event.pointerId)||findControl(event.target);
  pressed.delete(event.pointerId);releasePress(element);
 };
 document.addEventListener('pointerup',releasePointer,true);
 document.addEventListener('pointercancel',releasePointer,true);
 document.addEventListener('keydown',event=>{
  if(event.key!=='Enter'&&event.key!==' ')return;
  const element=findControl(event.target);if(element)applyPress(element);
 },true);
 document.addEventListener('keyup',event=>{
  if(event.key!=='Enter'&&event.key!==' ')return;
  releasePress(findControl(event.target));
 },true);
 document.addEventListener('click',event=>{
  const element=findControl(event.target);
  if(!element||event.detail!==0)return;
  applyPress(element);releasePress(element);
 },true);

 /* Keep the original Menu 18-derived Menu 3 Pinyin mapper untouched.
    It matches complete source readings and applies shortest-path syllable
    segmentation plus one-position tone diversity. No component-word Cartesian
    composition is performed here. */
 const cleanMeaning=value=>String(value||'').split(/[;；]/)[0]
  .replace(/^[\s·•,，、:：-]+/,'').replace(/\s+/g,' ').trim();
 const validMeaning=value=>{
  const v=cleanMeaning(value),low=v.toLocaleLowerCase('vi');
  if(v.length<2||v.length>180)return false;
  if(/(?:chưa có nghĩa|chưa tìm được nghĩa|chưa tra được nghĩa|không có nghĩa|không tìm thấy nghĩa|not found|undefined|null)/i.test(low))return false;
  if(/[\d\u3400-\u9fff\uf900-\ufaff]/.test(v))return false;
  if(/\b(?:phương ngữ miền bắc|phương ngữ miền nam|dạng kết hợp|tên khoa học|danh pháp|tên riêng tiếng)\b/i.test(low))return false;
  return (v.match(/[A-Za-zÀ-ỹĐđ]/g)||[]).length>=2;
 };
 const pinyinKey=value=>typeof window.pinyin18Key==='function'
  ?window.pinyin18Key(value)
  :String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[üÜvV]/g,'u').toLowerCase().replace(/[^a-z]/g,'');
 function pathsForInputToken(rawToken,available){
  const key=pinyinKey(rawToken),memo=new Array(key.length+1);
  if(!key)return [];
  memo[key.length]=[[]];
  for(let start=key.length-1;start>=0;start--){
   const options=[];
   for(let finish=start+1;finish<=Math.min(key.length,start+6);finish++){
    const syllable=key.slice(start,finish),tails=memo[finish];
    if(!available.has(syllable)||!tails)continue;
    for(const tail of tails){options.push([syllable].concat(tail));if(options.length>=24)break;}
    if(options.length>=24)break;
   }
   memo[start]=options;
  }
  const paths=memo[0]||[];
  // A valid standalone syllable remains ambiguous (e.g. xian). For a
  // non-syllable compact token, prefer only the minimum-syllable path.
  if(available.has(key))return paths;
  if(!paths.length)return [];
  const shortest=Math.min(...paths.map(path=>path.length));
  return paths.filter(path=>path.length===shortest);
 }
 function matchesPreferredBoundaries(raw,sourcePinyin){
  const matches=[...String(raw||'').matchAll(/[^\s,，、;；.!?！？]+/g)];
  const tokens=String(sourcePinyin||'').trim().split(/\s+/).filter(Boolean);
  if(!matches.length||!tokens.length||typeof window.getPinyin18SourceIndex!=='function')return false;
  const available=window.getPinyin18SourceIndex()?.syllables;if(!available)return false;
  const actual=tokens.map(pinyinKey);let offset=0;
  for(const match of matches){
   const paths=pathsForInputToken(match[0],available);
   const selected=paths.find(path=>path.length<=actual.length-offset&&path.every((key,index)=>actual[offset+index]===key));
   if(!selected)return false;
   offset+=selected.length;
  }
  return offset===actual.length;
 }
 function menu3SourceLetters(value){
  const toneMarks=new Set(['\u0304','\u0301','\u030c','\u0300']);
  const letters=[];let lastVowel=-1;
  for(const ch of String(value||'').normalize('NFD').toLowerCase()){
   if(ch==='v'){letters.push({base:'u',mark:'',umlaut:true});lastVowel=letters.length-1;continue;}
   if(/[a-z]/.test(ch)){letters.push({base:ch,mark:'',umlaut:false});if('aeiou'.includes(ch))lastVowel=letters.length-1;continue;}
   if(ch==='\u0308'){if(lastVowel>=0&&letters[lastVowel].base==='u')letters[lastVowel].umlaut=true;continue;}
   if(toneMarks.has(ch)){if(lastVowel>=0&&!letters[lastVowel].mark)letters[lastVowel].mark=ch;continue;}
  }
  return letters;
 }
 function menu3FormatWord(rawWord,sourceWord){
  const rawLetters=menu3SourceLetters(rawWord),sourceLetters=menu3SourceLetters(sourceWord);
  if(!rawLetters.length||rawLetters.length!==sourceLetters.length)return rawWord;
  const rawChars=[...String(rawWord).normalize('NFD')].filter(ch=>/[A-Za-z]/.test(ch));
  return rawLetters.map((letter,index)=>{
   const source=sourceLetters[index],upper=/[A-Z]/.test(rawChars[index]||'');
   let output=upper?letter.base.toUpperCase():letter.base;
   if(source.umlaut)output+='\u0308';
   output+=source.mark||'';
   return output;
  }).join('').normalize('NFC');
 }
 function formatByInputSpacing(raw,sourcePinyin){
  const source=String(raw??''),matches=[...source.matchAll(/[^\s,，、;；.!?！？]+/g)];
  let syllables=String(sourcePinyin||'').trim().split(/\s+/).filter(Boolean);
  if(!matches.length)return String(sourcePinyin||'');
  if(typeof window.getPinyin18SourceIndex!=='function')return String(sourcePinyin||'');
  const available=window.getPinyin18SourceIndex()?.syllables;
  if(!available)return String(sourcePinyin||'');
  // If source is compact (one token) but user has multiple tokens, expand it.
  if(syllables.length===1 && matches.length>1){
   const compactKey=pinyinKey(syllables[0]);
   const paths=pathsForInputToken(syllables[0],available);
   const expanded=paths.find(path=>path.join('')===compactKey);
   if(expanded)syllables=expanded.map(base=>base); // use base forms; tones will be applied later if needed
  }
  const keys=syllables.map(pinyinKey),groups=[];let at=0;
  for(const match of matches){
   const paths=pathsForInputToken(match[0],available);
   const selected=paths.find(path=>path.length<=keys.length-at&&path.every((key,index)=>keys[at+index]===key));
   if(!selected)return String(sourcePinyin||'');
   const sourceGroup=syllables.slice(at,at+selected.length);
   groups.push(menu3FormatWord(match[0],sourceGroup.join('')));at+=selected.length;
  }
  if(at!==syllables.length)return String(sourcePinyin||'');
  const first=matches[0],last=matches[matches.length-1];
  let output=source.slice(0,first.index)+groups[0];
  for(let i=1;i<groups.length;i++){
   const previous=matches[i-1],current=matches[i];
   output+=source.slice(previous.index+previous[0].length,current.index)+groups[i];
  }
  output+=source.slice(last.index+last[0].length);
  return output;
 }
 const isPinyinEchoMeaning=(meaning,pinyin)=>{
  const meaningKey=pinyinKey(meaning),pinyinValue=pinyinKey(pinyin);
  return !!meaningKey&&!!pinyinValue&&meaningKey===pinyinValue;
 };
 const translateFullSentence=async item=>{
  if(!item||!String(item.zh||'').trim()||!String(item.py||'').trim())return null;
  const composed=Array.isArray(item.sourceRows)&&item.sourceRows.length>1;
  // Prefer the first genuinely valid Vietnamese gloss; an invalid
  // preferredMeaning must never mask a valid item.vi value.
  const direct=[item.preferredMeaning,item.vi].map(cleanMeaning)
   .find(value=>validMeaning(value)&&!isPinyinEchoMeaning(value,item.py));
  if(!composed&&direct)return {...item,vi:direct};
  const hanzi=String(item.zh).trim();
  const translators=[];
  if(typeof window.machineTranslate3x==='function'){
   translators.push(()=>window.machineTranslate3x(hanzi,'zh-CN','vi'));
  }
  // Keep the legacy translator as a real fallback even when the newer
  // machineTranslate3x function exists but rejects, times out or returns junk.
  if(typeof window.machineTranslate==='function'){
   translators.push(()=>window.machineTranslate(hanzi,'zh-CN','vi'));
  }
  if(!translators.length)return null;
  for(let attempt=0;attempt<3;attempt++){
   for(const translate of translators){
    try{
     const result=await translate();
     const raw=result&&typeof result==='object'
      ?(result.text??result.translation??result.translatedText??'')
      :result;
     const translated=cleanMeaning(raw);
     if(validMeaning(translated)&&!isPinyinEchoMeaning(translated,item.py)){
      return {...item,vi:translated,note:'Nghĩa tiếng Việt được dịch từ toàn câu chữ Hán.'};
     }
    }catch(_){}
   }
   if(attempt<2)await new Promise(r=>setTimeout(r,180));
  }
  return null;
 };
 async function mapLimit(items,limit,worker){
  const output=new Array(items.length);let next=0;
  const runners=Array.from({length:Math.min(limit,items.length)},async()=>{
   while(next<items.length){const index=next++;output[index]=await worker(items[index],index);}
  });
  await Promise.all(runners);return output;
 }
 let renderToken=0;
 let currentCandidates=[];
 function menu3ReadingUsesUmlaut(value){
  const text=String(value||'').normalize('NFD').toLowerCase();
  // Tone-marked ü syllables (nǚ, lǜ, jù, qǔ, xū, yǔ) no longer
  // carry the visible diaeresis after Unicode normalization.
  const toneMarkedUmlaut=/(?:^|[^a-z])[nljqxy]u[\u0304\u0301\u030c\u0300]/.test(text);
  return text.includes('\u0308')||/v/.test(text)||toneMarkedUmlaut;
 }
 function installMenu3UmlautSelector(){
  const original=window.pinyin18SelectToneDiverse;
  if(typeof original!=='function'||original.__menu3UmlautStrict)return;
  const wrapped=function(candidates,raw,limit){
   const inputTokens=String(raw||'').trim().split(/[\s,，、;；]+/).filter(Boolean);
   let pool=Array.isArray(candidates)?candidates:[];
   if(inputTokens.some(menu3ReadingUsesUmlaut)){
    pool=pool.filter(item=>{
     const tokens=String(item?.py||'').trim().split(/\s+/).filter(Boolean);
     return inputTokens.every((token,index)=>!menu3ReadingUsesUmlaut(token)||menu3ReadingUsesUmlaut(tokens[index]));
    });
   }
   if(!pool.length)return [];
   return original.call(this,pool,raw,limit);
  };
  wrapped.__menu3UmlautStrict=true;
  window.pinyin18SelectToneDiverse=wrapped;
 }
 async function renderCandidates(candidates){
  const host=document.getElementById('homework3x-candidates');
  if(!host)return null;
  const status=document.getElementById('homework3x-status');
  const query=String(document.getElementById('homework3x-query')?.value||'');
  installMenu3UmlautSelector();
  const seen=new Set();
  const valid=(Array.isArray(candidates)?candidates:[]).filter(item=>{
   if(!item||!item.zh||!item.py)return false;
   const id=String(item.zh)+'|'+String(item.py);
   if(seen.has(id))return false;seen.add(id);return true;
  });
  // Candidates have already passed Menu 3's semantic sentence gate.
  // Do not run Menu 18's one-position tone selector here: it would discard
  // valid combinations that differ at more than one Pinyin position.
  const source=valid.slice().sort((a,b)=>
   (Number(b.score)||Number(b.priority)||0)-(Number(a.score)||Number(a.priority)||0)||
   String(a.zh).localeCompare(String(b.zh),'zh-CN')
  );
  if(!source.length){host.replaceChildren();host.hidden=true;if(status)status.textContent='Chưa tìm được kết quả Pinyin khớp với mục từ/câu hoàn chỉnh trong từ điển.';return null;}
  const token=++renderToken;let page=0;const pageSize=10;
  if(status)status.textContent='Đang hoàn thiện nghĩa tiếng Việt cho các kết quả…';
  host.hidden=false;host.replaceChildren();
  // Resolve meanings for the entire candidate set before any card is shown.
  const resolved=await mapLimit(source,3,translateFullSentence);
  if(token!==renderToken)return null;
  const complete=resolved.filter(item=>item&&item.zh&&item.py&&validMeaning(item.vi));
  if(!complete.length){
   host.replaceChildren();host.hidden=true;
   if(status)status.textContent='Chưa thể xác minh nghĩa tiếng Việt hợp lệ cho các kết quả tìm được.';
   return null;
  }
  currentCandidates=complete;
  const renderPage=()=>{
   if(token!==renderToken)return;
   const pageCount=Math.max(1,Math.ceil(complete.length/pageSize));
   const start=page*pageSize,items=complete.slice(start,start+pageSize);
   host.replaceChildren();
   const nav=()=>{
    const node=document.createElement('div');node.className='homework3x-pagination'+(pageCount<=1?' single-page':'');
    node.innerHTML='<button type="button" data-page-prev>‹ Trang trước</button><span>Trang '+(page+1)+' / '+pageCount+'</span><button type="button" data-page-next>Trang sau ›</button>';
    node.querySelector('[data-page-prev]').disabled=page===0;
    node.querySelector('[data-page-next]').disabled=page>=pageCount-1;
    node.querySelector('[data-page-prev]').addEventListener('click',()=>{if(page>0){page--;renderPage();}});
    node.querySelector('[data-page-next]').addEventListener('click',()=>{if(page<pageCount-1){page++;renderPage();}});
    return node;
   };
   const grid=document.createElement('div');grid.className='homework3x-candidate-grid';
   items.forEach((item,offset)=>{
    const index=start+offset,button=document.createElement('button');
    button.type='button';button.className='homework3x-candidate';button.dataset.homework3xCandidate=String(index);
    const number=document.createElement('span');number.className='homework3x-candidate-number';number.textContent=String(index+1);
    const content=document.createElement('span');content.className='homework3x-candidate-content';
    const py=document.createElement('span');py.className='homework3x-candidate-py';py.style.cssText='display:block!important;color:#1769c2!important;font-size:clamp(21px,5.2vw,27px)!important;font-weight:900!important;line-height:1.35!important;letter-spacing:.01em!important;overflow-wrap:anywhere!important';py.textContent=formatByInputSpacing(query,item.py);
    const zh=document.createElement('span');zh.className='homework3x-candidate-zh';zh.style.cssText='display:block!important;color:#7b3fa1!important;font-size:19px!important;font-weight:850!important;line-height:1.4!important;overflow-wrap:anywhere!important';zh.textContent=item.zh;
    const vi=document.createElement('span');vi.className='homework3x-candidate-vi';vi.style.cssText='display:block!important;color:#16845b!important;font-size:16px!important;font-weight:750!important;line-height:1.45!important;white-space:normal!important;overflow-wrap:anywhere!important';vi.textContent=item.vi;
    content.append(py,zh,vi);button.append(number,content);
    button.addEventListener('click',event=>{
     event.preventDefault();event.stopPropagation();
     window.homework3xSelectedCandidateIndex=index;
     if(typeof window.openHomework3xCandidateModal==='function'){window.openHomework3xCandidateModal(item,index,complete.length);}
    });
    grid.appendChild(button);
   });
   host.appendChild(nav());
   host.appendChild(grid);
   host.appendChild(nav());
   host.hidden=false;
   if(status)status.textContent='Có '+complete.length+' kết quả hợp lệ. Mỗi kết quả đã có phiên âm, chữ Hán và nghĩa tiếng Việt. Hiển thị tối đa 10 kết quả mỗi trang.';
  };
  renderPage();
  return complete[0]||null;
 }
 window.formatByInputSpacing=formatByInputSpacing;
 window.renderHomework3xCandidatesV421023=renderCandidates;

 /* Menu 3 candidate detail modal: three values, three copy actions, two speech actions. */
 const escapeHtml=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
 const copyText=async value=>{
  const text=String(value||'');if(!text)return false;
  try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);return true;}}catch(_){}
  const area=document.createElement('textarea');area.value=text;area.readOnly=true;
  area.style.cssText='position:fixed;left:0;top:0;width:1px;height:1px;opacity:.01;font-size:16px';
  document.body.appendChild(area);let ok=false;
  try{area.focus({preventScroll:true});area.select();area.setSelectionRange(0,text.length);ok=document.execCommand('copy');}catch(_){}
  area.remove();return ok;
 };
 const speakText=(value,locale)=>{
  const text=String(value||'').trim();if(!text)return;
  if(typeof window.bvtSpeakLocale==='function'){window.bvtSpeakLocale(text,locale);return;}
  if(typeof window.speakMandarinSentence==='function'&&locale==='zh'){window.speakMandarinSentence(text);return;}
  if('speechSynthesis'in window){window.speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(text);utterance.lang=locale==='zh'?'zh-CN':'vi-VN';window.speechSynthesis.speak(utterance);}
 };
 window.openHomework3xCandidateModal=function(item,index,total){
  const existing=document.querySelector('.homework3x-modal-backdrop');
  if(existing)existing.remove();
  const modalVi=cleanMeaning(item?.vi||'');
  const preferredVi=cleanMeaning(item?.preferredMeaning||'');
  const values={
   hanzi:String(item?.zh||'').trim(),
   pinyin:formatByInputSpacing(String(document.getElementById('homework3x-query')?.value||''),String(item?.py||'').trim()),
   // The resolved card meaning is authoritative; never let a stale or
   // invalid preferredMeaning hide the verified Vietnamese result.
   meaning:validMeaning(modalVi)&&!isPinyinEchoMeaning(modalVi,item?.py)
    ?modalVi
    :(validMeaning(preferredVi)&&!isPinyinEchoMeaning(preferredVi,item?.py)?preferredVi:'')
  };
  if(!values.hanzi||!values.pinyin||!values.meaning)return;
  const backdrop=document.createElement('div');
  backdrop.className='homework3x-modal-backdrop';
  backdrop.style.cssText='position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(9,12,17,.62);overscroll-behavior:contain';
  backdrop.innerHTML='<section role="dialog" aria-modal="true" aria-labelledby="homework3x-detail-title" style="width:min(620px,100%);max-height:88dvh;overflow:auto;background:#fff;color:#172033;border-radius:18px;padding:20px;box-shadow:0 20px 60px rgba(0,0,0,.3)">'+
   '<header style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:8px"><h3 id="homework3x-detail-title" style="margin:0;font-size:18px">Kết quả '+(Number(index)+1)+' / '+Number(total||0)+'</h3><button type="button" data-detail-close style="min-width:40px;min-height:40px;border-radius:10px;font-weight:800">✕</button></header>'+
   '<div style="border:1px solid #dbe2ea;border-radius:12px;padding:13px;margin:9px 0"><b style="color:#7b3fa1">CHỮ HÁN</b><div style="font-size:27px;font-weight:800;margin:7px 0;overflow-wrap:anywhere">'+escapeHtml(values.hanzi)+'</div><div><button type="button" data-copy="hanzi">Sao chép chữ Hán</button><button type="button" data-speak="zh">🔊 Phát âm chữ Hán</button></div></div>'+
   '<div style="border:1px solid #dbe2ea;border-radius:12px;padding:13px;margin:9px 0"><b style="color:#2563a6">PHIÊN ÂM PINYIN</b><div style="font-size:22px;font-weight:800;margin:7px 0;overflow-wrap:anywhere">'+escapeHtml(values.pinyin)+'</div><button type="button" data-copy="pinyin">Sao chép Pinyin</button></div>'+
   '<div style="border:1px solid #dbe2ea;border-radius:12px;padding:13px;margin:9px 0"><b style="color:#21805b">NGHĨA TIẾNG VIỆT</b><div style="font-size:19px;font-weight:700;margin:7px 0;overflow-wrap:anywhere">'+escapeHtml(values.meaning||'Chưa có nghĩa tiếng Việt hợp lệ')+'</div><div><button type="button" data-copy="meaning">Sao chép nghĩa</button><button type="button" data-speak="vi">🔊 Phát âm tiếng Việt</button></div></div>'+
   '<p data-copy-status role="status" aria-live="polite" style="min-height:20px;color:#15803d;font-weight:700"></p></section>';
  const prevOverflow=document.body.style.overflow;
  document.body.style.overflow='hidden';
  document.body.appendChild(backdrop);
  const status=backdrop.querySelector('[data-copy-status]');
  const close=()=>{backdrop.remove();document.body.style.overflow=prevOverflow;document.removeEventListener('keydown',onKey);};
  const onKey=e=>{if(e.key==='Escape')close();};
  document.addEventListener('keydown',onKey);
  backdrop.querySelector('[data-detail-close]').addEventListener('click',close);
  backdrop.addEventListener('click',event=>{if(event.target===backdrop)close();});
  backdrop.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
   const kind=button.dataset.copy;button.disabled=true;const ok=await copyText(values[kind]);button.disabled=false;
   if(status)status.textContent=ok?'Đã sao chép thành công.':'Không thể sao chép tự động trên trình duyệt này.';
  }));
  backdrop.querySelectorAll('[data-speak]').forEach(button=>button.addEventListener('click',()=>speakText(button.dataset.speak==='zh'?values.hanzi:values.meaning,button.dataset.speak==='zh'?'zh':'vi')));
 };
 /* Serialize lookup requests; every path, including errors, releases the lock. */
 const lookupButton=document.getElementById('homework3x-lookup');
 const originalLookup=window.lookupHomework3x;
 if(typeof originalLookup==='function'&&!originalLookup.__bvtSerializedV421023){
  let running=false;
  const serialized=async function(){
   if(running)return null;
   running=true;if(lookupButton)lookupButton.disabled=true;
   try{
    const query=String(document.getElementById('homework3x-query')?.value||'').trim();
    const semantic=typeof window.menu3AnalyzeSentence==='function'?window.menu3AnalyzeSentence(query):[];
    if(semantic.length&&typeof window.renderHomework3xCandidatesV421023==='function'){
     const status=document.getElementById('homework3x-status');
     if(status)status.textContent='Đã ghép các phương án từ điển và kiểm tra nghĩa tiếng Việt của toàn câu…';
     return await window.renderHomework3xCandidatesV421023(semantic);
    }
    return await originalLookup.apply(this,arguments);
   }
   catch(error){
    const status=document.getElementById('homework3x-status');
    if(status)status.textContent='Đã xảy ra lỗi khi tra cứu. Bạn có thể thử lại: '+String(error&&error.message||error);
    return null;
   }finally{running=false;if(lookupButton)lookupButton.disabled=false;}
  };
  serialized.__bvtSerializedV421023=true;
  window.lookupHomework3x=serialized;
 }
 const input=document.getElementById('homework3x-query');
 if(input)input.addEventListener('keydown',event=>{
  if(event.key==='Enter'&&window.lookupHomework3x?.__bvtSerializedV421023&&lookupButton?.disabled)event.preventDefault();
 },true);
 root.dataset.menu3PinyinFix='42.10.23';


 /* Vietnamese sentence meaning composition for Menu 3. */
 function menu3Gloss(entry){
  let text=String(entry?.vi||'');
  text=text.split(/[;；]/)[0];
  text=text.replace(/\([^)]*\)/g,' ').replace(/\[[^\]]*\]/g,' ');
  text=text.replace(/^[\s·•,，、:：|\-]+/,'').replace(/[\s·•,，、:：|\-]+$/,'').replace(/\s+/g,' ').trim();
  return text;
 }
 function menu3BadGloss(text){
  return !text||text.length>80||/biến thể|phương ngữ|hình thức kết hợp|tên khoa học|danh pháp|trợ từ|chất liệu/i.test(text)||/[\u3400-\u9fff]/.test(text);
 }
 function menu3BadEntry(entry){
  const raw=String(entry?.vi||'');
  if(/biến thể|phương ngữ|hình thức kết hợp|tên khoa học|danh pháp|trợ từ|dùng trong|chất liệu/i.test(raw))return true;
  if(/^\s*họ\s*\[/i.test(raw))return true;
  return menu3BadGloss(menu3Gloss(entry));
 }
 function menu3FinishSentence(text,ending='.'){
  let sentence=String(text||'').replace(/\s+/g,' ').trim();
  if(!sentence)return '';
  sentence=sentence.charAt(0).toLocaleUpperCase('vi')+sentence.slice(1);
  if(!/[.!?…]$/.test(sentence))sentence+=ending;
  return sentence;
 }
 function menu3IsVerbGloss(gloss){
  const text=String(gloss||'').toLocaleLowerCase('vi').trim();
  if(!text)return false;
  return /^(yêu|thích|nhớ|gặp|quen|giúp|mời|hỏi|nhìn|xem|nghe|gọi|uống|ăn|đi|đến|tới|học|làm|nói|đọc|viết|mua|bán|cho|lấy|đưa|mang|mở|đóng|ngồi|đứng|chạy|bay|hát|nhảy|chơi|trả|lời|cười|khóc|ngủ|thức|dậy|tắm|rửa|mặc|cởi|về|ra|vào|lên|xuống|qua|lại|biết|hiểu|nghĩ|muốn|cần|phải|có thể|sẽ|đã|đang|vừa|mới|còn|chỉ|cũng|rất|không|có|là|ở|tại|từ)$/.test(text);
 }
 function menu3HasVerb(parts){
  return (Array.isArray(parts)?parts:[]).some(part=>menu3IsVerbGloss(part.gloss||part));
 }
 function menu3MeaningFromEntries(entries){
  const parts=(Array.isArray(entries)?entries:[]).map(entry=>{
   const zh=String(entry.zh||''),gloss=menu3Gloss(entry),key=pinyinKey(entry.py);
   return {zh,gloss,entry,le:zh==='了'&&key==='le',question:zh==='吗'&&key==='ma',qing:zh==='请',and:zh==='和'||zh==='合'||zh==='跟'};
  });
  if(!parts.length)return '';
  // 吗 is a sentence-final question particle, not a content word. Keep it
  // as a grammatical signal and exclude its dictionary gloss from Vietnamese.
  const questionAt=parts.findIndex(part=>part.question);
  if(questionAt>=0&&questionAt!==parts.length-1)return '';
  const asked=questionAt===parts.length-1;
  const content=asked?parts.slice(0,-1):parts.slice();
  const completed=content.length>0&&content[content.length-1].le;
  const core=completed?content.slice(0,-1):content;
  if(!core.length||core.some(part=>menu3BadEntry(part.entry)))return '';
  const time=/^(hôm qua|hôm nay|hôm kia|ngày mai|bây giờ|sáng nay|tối nay|tuần trước|tuần sau|năm ngoái)$/i;
  const person=/^(tôi|mình|bạn|anh|chị|em|họ|ông|bà|chúng tôi|chúng ta)$/i;
  const andAt=core.findIndex(part=>part.and);
  if(andAt>=0){
   const left=core.slice(0,andAt),right=core.slice(andAt+1);
   if(!left.length||!right.length||left.concat(right).some(part=>part.and||part.qing))return '';
   const personSide=/^(tôi|mình|bạn|anh|chị|em|họ|ông|bà|chúng tôi|chúng ta|các bạn)$/i;
   const countPeople=parts=>parts.filter(part=>personSide.test(part.gloss)).length;
   const leftPeople=countPeople(left),rightPeople=countPeople(right);
   if((leftPeople>0)!==(rightPeople>0))return '';
   if((leftPeople&&leftPeople!==left.length)||(rightPeople&&rightPeople!==right.length))return '';
   const conj=core[andAt].gloss.toLocaleLowerCase('vi');
   const word=/^(và|với|cùng|cùng với)$/.test(conj)?conj:'và';
   return menu3FinishSentence(left.map(part=>part.gloss.toLocaleLowerCase('vi')).join(' ')+' '+word+' '+right.map(part=>part.gloss.toLocaleLowerCase('vi')).join(' '),asked?'?':'.');
  }
  let index=0;const times=[];
  while(index<core.length&&time.test(core[index].gloss)){times.push(core[index].gloss.toLocaleLowerCase('vi'));index++;}
  let subject='';
  if(index<core.length&&person.test(core[index].gloss)){subject=core[index].gloss.toLocaleLowerCase('vi');index++;}
  const rest=core.slice(index);
  if(rest[0]&&rest[0].qing){
   const after=rest.slice(1);let object='';
   if(after[0]&&person.test(after[0].gloss)){object=after.shift().gloss.toLocaleLowerCase('vi');}
   if(after.some(part=>part.and))return '';
   const action=after.map(part=>part.gloss.toLocaleLowerCase('vi')).filter(Boolean);
   if(!object||!menu3HasVerb(after))return '';
   return menu3FinishSentence([times.join(' '),subject,completed?'đã':'','mời',object,action.join(' ')].filter(Boolean).join(' '),asked?'?':'.');
  }
  if(subject&&rest.length&&!rest.some(part=>part.and||part.qing)){
   const pronoun=/^(tôi|mình|bạn|anh|chị|em|họ|ông|bà|chúng tôi|chúng ta|các bạn)$/i;
   const social=/^(yêu|thích|nhớ|gặp|quen|giúp|mời|hỏi|nhìn|xem|nghe|gọi)$/i;
   if(pronoun.test(rest[rest.length-1].gloss)&&!social.test(rest[0].gloss))return '';
   if(!menu3HasVerb(rest))return '';
   return menu3FinishSentence([times.join(' '),subject,completed?'đã':'',rest.map(part=>part.gloss.toLocaleLowerCase('vi')).join(' '),asked?'không':''].filter(Boolean).join(' '),asked?'?':'.');
  }
  if(core.length===1&&!menu3BadGloss(core[0].gloss))return asked?menu3FinishSentence(core[0].gloss,'?'):core[0].gloss;
  return '';
 }
 function menu3ShortestSyllables(token){
  if(typeof window.getPinyin18SourceIndex!=='function')return [];
  const available=window.getPinyin18SourceIndex()?.syllables;if(!available)return [];
  return pathsForInputToken(token,available);
 }
 function menu3ComposeAnalyses(raw){
  if(typeof window.getPinyin3xComposerIndex!=='function'||typeof window.pinyin18InputInfosMatchSource!=='function')return [];
  const composer=window.getPinyin3xComposerIndex();
  const tokens=String(raw||'').trim().split(/[\s,，、;；]+/).filter(Boolean);
  if(!tokens.length||tokens.length>12)return [];
  let sequences=[[]];
  for(const token of tokens){
   const paths=menu3ShortestSyllables(token);
   if(!paths.length)return [];
   const shortest=Math.min(...paths.map(path=>path.length));
   const chosen=paths.filter(path=>path.length===shortest).slice(0,2);
   const next=[];
   for(const prefix of sequences)for(const path of chosen){
    next.push(prefix.concat(path.map(base=>({base,tones:[]}))));
    if(next.length>=6)break;
   }
   sequences=next;if(!sequences.length)return [];
  }
  const found=[];
  for(const input of sequences){
   const states=Array.from({length:input.length+1},()=>[]);states[0]=[{score:0,zh:'',entries:[]}];
   for(let start=0;start<input.length;start++){
    if(!states[start].length)continue;
    for(let end=start+1;end<=Math.min(input.length,start+6);end++){
     const span=input.slice(start,end),compact=span.map(item=>item.base).join('');
     const entries=composer.byCompact.get(compact)||[];
     for(const entry of entries){
      if(!window.pinyin18InputInfosMatchSource(entry,span))continue;
      for(const path of states[start]){
       const candidate={score:path.score+Number(entry.score||0)+(Number(entry.chars)>1?20:0)-4,zh:path.zh+entry.zh,entries:path.entries.concat(entry)};
       const bucket=states[end],prior=bucket.find(item=>item.zh===candidate.zh);
       if(prior){if(candidate.score>prior.score)Object.assign(prior,candidate);}else bucket.push(candidate);
       bucket.sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh,'zh-CN'));
       if(bucket.length>256)bucket.length=256;
      }
     }
    }
   }
   for(const path of states[input.length]||[])found.push(path);
  }
  found.sort((a,b)=>b.score-a.score);
  const results=[],seen=new Set();
  for(const path of found){
   const vi=menu3MeaningFromEntries(path.entries);if(!vi)continue;
   if(path.entries.some(entry=>Number(entry.score||0)<80&&!(entry.zh==='了'&&pinyinKey(entry.py)==='le')))continue;
   const id=path.zh+'|'+vi;if(seen.has(id))continue;seen.add(id);
   results.push({zh:path.zh,py:path.entries.map(entry=>String(entry.py||'').trim()).filter(Boolean).join(' '),vi,score:path.score});
   if(results.length>=300)break;
  }
  return results;
 }
 function menu3LexicalMeaning(item){
  const direct=cleanMeaning(item?.preferredMeaning||item?.vi||'');
  if(validMeaning(direct)&&!menu3BadGloss(direct))return direct;
  const gloss=menu3Gloss(item);
  return !menu3BadGloss(gloss)&&validMeaning(gloss)?gloss:'';
 }
 function menu3EntryMatchesReading(token,item){
  if(!menu3ReadingUsesUmlaut(token))return true;
  return String(item?.py||'').trim().split(/\s+/).filter(Boolean).some(menu3ReadingUsesUmlaut);
 }
 function menu3AnalyzeSentence(raw){
  const query=String(raw||'').trim();
  if(!query)return [];
  installMenu3UmlautSelector();
  // Primary path: compose dictionary-backed lexical entries across every
  // Pinyin slot, then accept only combinations that pass the Vietnamese
  // sentence-structure validator. This is the semantic final gate.
  const rows=menu3ComposeAnalyses(query);
  const seen=new Set(rows.map(item=>String(item.zh)+'|'+String(item.py)));
  // Add only complete, independently glossed dictionary phrases. Never let
  // isolated component-word glosses bypass the sentence-level semantic gate.
  const findChinese=window['pinyinToChineseCandidates'];
  const exact=typeof findChinese==='function'?findChinese(query):[];
  for(const item of Array.isArray(exact)?exact:[]){
   if(!item||!item.zh||!item.py)continue;
   if(!Array.isArray(item.sourceRows)||item.sourceRows.length!==1)continue;
   const sourceRow=item.sourceRows[0];
   if(!Array.isArray(sourceRow)||String(sourceRow[0]||'')!==String(item.zh))continue;
   const vi=menu3LexicalMeaning(item);
   if(!vi||!validMeaning(vi))continue;
   const id=String(item.zh)+'|'+String(item.py);
   if(seen.has(id))continue;
   seen.add(id);
   rows.push({zh:item.zh,py:item.py,vi,score:Number(item.priority)||Number(item.score)||0});
  }
  rows.sort((a,b)=>(Number(b.score)||0)-(Number(a.score)||0)||String(a.zh).localeCompare(String(b.zh),'zh-CN'));
  return rows.map(item=>({zh:item.zh,py:formatByInputSpacing(query,item.py),vi:item.vi,score:item.score||0,sourcePy:item.py}));
 }
 window.menu3AnalyzeSentence=menu3AnalyzeSentence;
 window.menu3PageItems=function(items,page,pageSize){
  const list=Array.isArray(items)?items:[],size=Math.max(1,Number(pageSize)||10);
  const pageCount=Math.max(1,Math.ceil(list.length/size)||1);
  const current=Math.min(Math.max(0,Number(page)||0),pageCount-1);
  const start=current*size;
  return {page:current,pageCount,total:list.length,items:list.slice(start,start+size),start};
 };

const menu3Heading=typeof document.querySelector==='function'
  ?document.querySelector('#panel-translate3 h2[data-function-number="3"]')
  :null;
 if(menu3Heading)menu3Heading.textContent='DỊCH NHANH VIỆT ⇄ TRUNG'; root.dataset.menu3PinyinMapper='menu18-source-sentence-mapper';
})();