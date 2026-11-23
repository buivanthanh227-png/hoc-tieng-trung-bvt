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
 function matchesPreferredBoundaries(raw,sourcePinyin){
  const matches=[...String(raw||'').matchAll(/[^\s,，、;；.!?！？]+/g)];
  const tokens=String(sourcePinyin||'').trim().split(/\s+/).filter(Boolean);
  if(!matches.length||!tokens.length||typeof window.getPinyin18SourceIndex!=='function'||typeof window.pinyin18SyllablePaths!=='function')return false;
  const available=window.getPinyin18SourceIndex()?.syllables;if(!available)return false;
  const expected=[];
  for(const match of matches){
   const paths=window.pinyin18SyllablePaths(match[0],available);
   const shortest=paths?.[0];
   if(!shortest?.length)return false;
   expected.push(...shortest);
  }
  return expected.length===tokens.length&&expected.every((key,index)=>pinyinKey(key)===pinyinKey(tokens[index]));
 }
 function formatByInputSpacing(raw,sourcePinyin){
  const source=String(raw||''),matches=[...source.matchAll(/[^\s,，、;；.!?！？]+/g)];
  const syllables=String(sourcePinyin||'').trim().split(/\s+/).filter(Boolean);
  if(!matches.length||!syllables.length)return String(sourcePinyin||'');
  if(typeof window.getPinyin18SourceIndex!=='function'||typeof window.pinyin18SyllablePaths!=='function')return String(sourcePinyin||'');
  const index=window.getPinyin18SourceIndex(),available=index?.syllables;
  if(!available)return String(sourcePinyin||'');
  const keys=syllables.map(pinyinKey),groups=[];let at=0;
  for(const match of matches){
   const paths=window.pinyin18SyllablePaths(match[0],available);
   const selected=paths?.[0];
   if(!selected||!selected.every((key,i)=>keys[at+i]===key))return String(sourcePinyin||'');
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
  const source=(Array.isArray(candidates)?candidates:[]).filter(item=>{
   if(!item||!item.zh||!item.py)return false;
   const id=String(item.zh)+'|'+String(item.py);
   if(seen.has(id))return false;seen.add(id);return true;
  }).filter(item=>matchesPreferredBoundaries(query,item.py)).sort((a,b)=>(Number(b.priority)||Number(b.score)||0)-(Number(a.priority)||Number(a.score)||0)).slice(0,30);
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