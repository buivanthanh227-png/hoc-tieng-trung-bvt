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
 function formatByInputSpacing(raw,sourcePinyin){
  const source=String(raw||''),matches=[...source.matchAll(/[^\s,，、;；.!?！？]+/g)];
  const syllables=String(sourcePinyin||'').trim().split(/\s+/).filter(Boolean);
  if(!matches.length||!syllables.length)return String(sourcePinyin||'');
  if(typeof window.getPinyin18SourceIndex!=='function')return String(sourcePinyin||'');
  const available=window.getPinyin18SourceIndex()?.syllables;
  if(!available)return String(sourcePinyin||'');
  const keys=syllables.map(pinyinKey),groups=[];let at=0;
  for(const match of matches){
   const paths=pathsForInputToken(match[0],available);
   const selected=paths.find(path=>path.length<=keys.length-at&&path.every((key,index)=>keys[at+index]===key));
   if(!selected)return String(sourcePinyin||'');
   groups.push(syllables.slice(at,at+selected.length).join(''));at+=selected.length;
  }
  if(at!==syllables.length)return String(sourcePinyin||'');
  const first=matches[0],last=matches[matches.length-1];
  let output=source.slice(0,first.index)+groups[0];
  for(let i=1;i<groups.length;i++){
   const previous=matches[i-1],current=matches[i];
   output+=source.slice(previous.index+previous[0].length,current.index)+groups[i];
  }
  output+=source.slice(last.index+last[0].length);
  return output.replace(/^(\s*)([a-zü])/i,(_,space,ch)=>space+ch.toUpperCase());
 }
 const translateFullSentence=async item=>{
  let vi=cleanMeaning(item.preferredMeaning||item.vi||'');
  if(validMeaning(vi))return {...item,vi};
  if(typeof window.machineTranslate!=='function')return null;
  try{
   const translated=cleanMeaning(await window.machineTranslate(String(item.zh),'zh-CN','vi'));
   return validMeaning(translated)?{...item,vi:translated,note:'Nghĩa tiếng Việt được dịch từ toàn câu chữ Hán.'}:null;
  }catch(_){return null;}
 };
 async function mapLimit(items,limit,worker){
  const output=new Array(items.length);let next=0;
  const runners=Array.from({length:Math.min(limit,items.length)},async()=>{
   while(next<items.length){const index=next++;output[index]=await worker(items[index],index);}
  });
  await Promise.all(runners);return output.filter(Boolean);
 }
 let renderToken=0;
 let currentCandidates=[];
 async function renderCandidates(candidates){
  const host=document.getElementById('homework3x-candidates');
  if(!host)return null;
  const status=document.getElementById('homework3x-status');
  const query=String(document.getElementById('homework3x-query')?.value||'');
  const seen=new Set();
  const valid=(Array.isArray(candidates)?candidates:[]).filter(item=>{
   if(!item||!item.zh||!item.py)return false;
   const id=String(item.zh)+'|'+String(item.py);
   if(seen.has(id))return false;seen.add(id);return true;
  });
  // Reuse the exact Menu 18 tone-position selector. It validates every
  // syllable and tone, selects compact-token boundaries, and only varies
  // one syllable's tone at a time (never a Cartesian product).
  const source=typeof window.pinyin18SelectToneDiverse==='function'
   ?window.pinyin18SelectToneDiverse(valid,query,30)
   :valid.filter(item=>matchesPreferredBoundaries(query,item.py))
     .sort((a,b)=>(Number(b.priority)||Number(b.score)||0)-(Number(a.priority)||Number(a.score)||0)).slice(0,30);
  if(!source.length){host.replaceChildren();host.hidden=true;if(status)status.textContent='Chưa tìm được kết quả Pinyin khớp với mục từ/câu hoàn chỉnh trong từ điển.';return null;}
  const token=++renderToken;let page=0;const pageSize=10;
  currentCandidates=source;
  host.hidden=false;
  const renderPage=async()=>{
   if(token!==renderToken)return;
   const pageCount=Math.max(1,Math.ceil(source.length/pageSize));
   const start=page*pageSize,rawItems=source.slice(start,start+pageSize);
   host.replaceChildren();
   if(status)status.textContent='Đang kiểm tra nghĩa tiếng Việt của tối đa 10 câu hoàn chỉnh…';
   const items=await mapLimit(rawItems,3,translateFullSentence);
   if(token!==renderToken)return;
   const nav=()=>{
    const node=document.createElement('div');node.className='homework3x-pagination';
    node.innerHTML='<button type="button" data-page-prev>‹ Trang trước</button><span>Trang '+(page+1)+' / '+pageCount+' · '+source.length+' kết quả</span><button type="button" data-page-next>Trang sau ›</button>';
    node.querySelector('[data-page-prev]').disabled=page===0;
    node.querySelector('[data-page-next]').disabled=page>=pageCount-1;
    node.querySelector('[data-page-prev]').addEventListener('click',()=>{if(page>0){page--;renderPage();}});
    node.querySelector('[data-page-next]').addEventListener('click',()=>{if(page<pageCount-1){page++;renderPage();}});
    return node;
   };
   host.appendChild(nav());
   const grid=document.createElement('div');grid.className='homework3x-candidate-grid';
   items.forEach((item,offset)=>{
    const index=start+offset,button=document.createElement('button');
    button.type='button';button.className='homework3x-candidate';button.dataset.homework3xCandidate=String(index);
    const number=document.createElement('span');number.className='homework3x-candidate-number';number.textContent=String(index+1);
    const content=document.createElement('span');content.className='homework3x-candidate-content';
    const py=document.createElement('span');py.className='homework3x-candidate-py';py.textContent=formatByInputSpacing(query,item.py);
    const zh=document.createElement('span');zh.className='homework3x-candidate-zh';zh.textContent=item.zh;
    const vi=document.createElement('span');vi.className='homework3x-candidate-vi';vi.textContent=item.vi;
    content.append(py,zh,vi);button.append(number,content);
    button.addEventListener('click',()=>{window.homework3xSelectedCandidateIndex=index;if(typeof window.openHomework3xCandidateModal==='function')window.openHomework3xCandidateModal(item,index,source.length);});
    grid.appendChild(button);
    source[index]=item;
   });
   if(!items.length){
    host.hidden=true;host.replaceChildren();
    if(status)status.textContent='Không tìm thấy nghĩa tiếng Việt hợp lý cho các phương án ở trang này. Đã loại bỏ kết quả không đạt yêu cầu.';
    return;
   }
   host.appendChild(grid);host.appendChild(nav());
   if(status)status.textContent='Có '+source.length+' phương án từ bộ ánh xạ Pinyin theo từ/câu hoàn chỉnh. Hiển thị 10 kết quả mỗi trang.';
  };
  await renderPage();return source[0]||null;
 }
 window.renderHomework3xCandidates=renderCandidates;

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
  if(!item)return;
  document.getElementById('homework3x-candidate-detail')?.remove();
  const py=formatByInputSpacing(String(document.getElementById('homework3x-query')?.value||''),item.py);
  const values={hanzi:String(item.zh||''),pinyin:py,meaning:String(item.vi||'')};
  const backdrop=document.createElement('div');backdrop.id='homework3x-candidate-detail';
  backdrop.className='homework3x-modal-backdrop';
  backdrop.style.cssText='position:fixed;inset:0;z-index:100000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(15,23,42,.62);';
  backdrop.innerHTML='<section role="dialog" aria-modal="true" aria-labelledby="homework3x-detail-title" style="width:min(620px,100%);max-height:88dvh;overflow:auto;background:#fff;color:#172033;border-radius:18px;padding:20px;box-shadow:0 20px 60px rgba(0,0,0,.3)">'+
   '<header style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px"><b id="homework3x-detail-title" style="font-size:18px">KẾT QUẢ '+(Number(index)+1)+' / '+Number(total)+'</b><button type="button" data-detail-close aria-label="Đóng" style="font-size:25px;border:0;background:#eef2f7;border-radius:10px;padding:4px 12px">×</button></header>'+
   '<div style="border:1px solid #dbe2ea;border-radius:12px;padding:13px;margin:9px 0"><b style="color:#7b3fa1">CHỮ HÁN</b><div style="font-size:27px;font-weight:800;margin:7px 0;overflow-wrap:anywhere">'+escapeHtml(values.hanzi)+'</div><div><button type="button" data-copy="hanzi">Sao chép chữ Hán</button><button type="button" data-speak="zh">🔊 Phát âm chữ Hán</button></div></div>'+
   '<div style="border:1px solid #dbe2ea;border-radius:12px;padding:13px;margin:9px 0"><b style="color:#2563a6">PHIÊN ÂM PINYIN</b><div style="font-size:22px;font-weight:800;margin:7px 0;overflow-wrap:anywhere">'+escapeHtml(values.pinyin)+'</div><button type="button" data-copy="pinyin">Sao chép Pinyin</button></div>'+
   '<div style="border:1px solid #dbe2ea;border-radius:12px;padding:13px;margin:9px 0"><b style="color:#21805b">NGHĨA TIẾNG VIỆT</b><div style="font-size:19px;font-weight:700;margin:7px 0;overflow-wrap:anywhere">'+escapeHtml(values.meaning||'Chưa có nghĩa tiếng Việt hợp lệ')+'</div><div><button type="button" data-copy="meaning">Sao chép nghĩa</button><button type="button" data-speak="vi">🔊 Phát âm tiếng Việt</button></div></div>'+
   '<p data-copy-status role="status" aria-live="polite" style="min-height:20px;color:#15803d;font-weight:700"></p></section>';
  document.body.appendChild(backdrop);
  const status=backdrop.querySelector('[data-copy-status]');
  backdrop.querySelector('[data-detail-close]').addEventListener('click',()=>backdrop.remove());
  backdrop.addEventListener('click',event=>{if(event.target===backdrop)backdrop.remove();});
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
   try{return await originalLookup.apply(this,arguments);}
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
 root.dataset.menu3PinyinMapper='menu18-source-sentence-mapper';
})();