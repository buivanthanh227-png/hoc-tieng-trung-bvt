#!/usr/bin/env python3
"""Add independent Hanzi, Pinyin+tone, and Vietnamese dictionary filters to Menu 1."""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_menu1_dictionary_search.py <site/index.html>")
target = Path(sys.argv[1])
if not target.is_file():
    raise SystemExit(f"Menu 1 target not found: {target}")
source = target.read_text(encoding="utf-8")
original = source

if "MENU1_THREE_FIELD_DICTIONARY_SEARCH_V1" in source:
    print("Menu 1 three-field dictionary search: already applied")
    raise SystemExit(0)

old = '<label class="sr-only" for="dict-search">Tìm từ vựng</label><input id="dict-search" class="field" type="search" autocomplete="off" placeholder="Vui lòng nhập nội dung bạn muốn...">'
new = r'''<div class="dict-advanced-search" id="dict-advanced-search">
   <label class="dict-search-field"><span>1. Tìm bằng chữ Hán</span><input id="dict-search-hanzi" class="field" type="search" autocomplete="off" placeholder="Nhập chữ Hán giản thể hoặc phồn thể"></label>
   <div class="dict-search-field"><label for="dict-search-pinyin"><span>2. Tìm bằng phiên âm Pinyin</span></label><input id="dict-search-pinyin" class="field" type="search" autocomplete="off" placeholder="Ví dụ: jin, jintian hoặc jīn"></div>
   <div class="dict-tone-picker" role="group" aria-label="Lọc thanh điệu Pinyin">
    <span class="dict-tone-label">Chọn thanh điệu</span>
    <div class="dict-tone-buttons">
     <button type="button" data-dict-tone="1" aria-pressed="false">Thanh 1</button>
     <button type="button" data-dict-tone="2" aria-pressed="false">Thanh 2</button>
     <button type="button" data-dict-tone="3" aria-pressed="false">Thanh 3</button>
     <button type="button" data-dict-tone="4" aria-pressed="false">Thanh 4</button>
     <button type="button" data-dict-tone="5" aria-pressed="false">Khinh thanh</button>
    </div>
    <span class="dict-tone-hint">Chạm lại thanh đang chọn để bỏ lọc. Nếu nhập Pinyin nhiều âm tiết, tất cả âm tiết khớp phải mang thanh đã chọn.</span>
   </div>
   <label class="dict-search-field"><span>3. Tìm bằng nghĩa tiếng Việt</span><input id="dict-search-meaning" class="field" type="search" autocomplete="off" placeholder="Nhập nghĩa tiếng Việt muốn tìm"></label>
   <p class="dict-search-hint">Có thể dùng từng ô riêng hoặc kết hợp nhiều ô để thu hẹp kết quả.</p>
  </div>
  <input id="dict-search" class="dict-legacy-search" type="search" tabindex="-1" aria-hidden="true" autocomplete="off">'''
if source.count(old) != 1:
    raise SystemExit(f"Menu 1 search input anchor expected once; found {source.count(old)}")
source = source.replace(old, new, 1)

css = r'''<style id="menu1-dictionary-search-style">
.dict-advanced-search{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px;margin:12px 0 8px}
.dict-search-field{display:grid;gap:6px;min-width:0;font-size:12px;font-weight:800;color:var(--ink,#182230)}
.dict-search-field .field{width:100%;min-width:0}
.dict-tone-picker{grid-column:1/-1;display:grid;gap:7px;padding:10px;border:1px solid var(--line,#d0d5dd);border-radius:12px;background:var(--surface-soft,#f8fafc)}
.dict-tone-label{font-size:12px;font-weight:800;color:var(--ink,#182230)}
.dict-tone-buttons{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px}
.dict-tone-buttons button{min-width:0;padding:9px 4px;border:1px solid var(--line,#d0d5dd);border-radius:8px;background:#fff;color:var(--ink,#344054);font-size:11px;font-weight:800;cursor:pointer}
.dict-tone-buttons button[aria-pressed="true"]{background:#e8f0ff;border-color:#3975c6;color:#174b91;box-shadow:0 0 0 1px #3975c6}
.dict-tone-hint,.dict-search-hint{font-size:11px;line-height:1.5;color:var(--muted,#667085);margin:0}
.dict-search-hint{grid-column:1/-1}
.dict-legacy-search{display:none!important}
@media(max-width:520px){.dict-advanced-search{grid-template-columns:1fr;gap:9px}.dict-tone-picker{grid-column:1}.dict-tone-buttons{gap:4px}.dict-tone-buttons button{font-size:10px;padding:9px 2px}}
</style>
'''
if source.count("</head>") != 1:
    raise SystemExit("Menu 1 CSS insertion point </head> missing or ambiguous")
source = source.replace("</head>", css + "\n</head>", 1)

js = r'''<script id="menu1-three-field-dictionary-search">
/* MENU1_THREE_FIELD_DICTIONARY_SEARCH_V1 */
(function(){
 const state={tone:null};
 const $id=id=>document.getElementById(id);
 function normalize(value){
  return String(value||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/Đ/g,'d').trim();
 }
 function pinyinParts(value){
  return String(value||'').trim().split(/\s+/).filter(Boolean).map(token=>{
   let raw=token.toLowerCase().replace(/ü/g,'v').replace(/u:/g,'v');
   let tone=null,explicit=false;
   const digit=raw.match(/([1-5])$/);
   if(digit){tone=Number(digit[1]);explicit=true;raw=raw.slice(0,-1);}
   const decomposed=raw.normalize('NFD');
   for(const ch of decomposed){
    if(ch==='\u0304'){tone=1;explicit=true;}
    else if(ch==='\u0301'){tone=2;explicit=true;}
    else if(ch==='\u030c'){tone=3;explicit=true;}
    else if(ch==='\u0300'){tone=4;explicit=true;}
   }
   const base=decomposed.replace(/[\u0300-\u036f]/g,'').replace(/[^a-zv]/g,'').replace(/v/g,'ü');
   return {base,tone,explicit};
  });
 }
 function pinyinScore(candidate,query,selectedTone){
  const parts=pinyinParts(candidate),wanted=pinyinParts(query);
  if(!parts.length||!wanted.length||wanted.some(x=>!x.base))return 0;
  const compact=wanted.map(x=>x.base).join('');
  let matched=null,exact=false;
  if(wanted.length>1){
   for(let start=0;start<=parts.length-wanted.length;start++){
    const segment=parts.slice(start,start+wanted.length);
    if(segment.every((part,i)=>part.base===wanted[i].base)){matched=segment;exact=true;break;}
   }
  }else{
   for(let start=0;start<parts.length;start++){
    let joined='';
    for(let end=start;end<parts.length;end++){
     joined+=parts[end].base;
     if(joined===compact){matched=parts.slice(start,end+1);exact=true;break;}
     if(joined.length>=compact.length)break;
    }
    if(matched)break;
   }
   if(!matched){
    const start=parts.findIndex(part=>part.base.startsWith(compact));
    if(start>=0){matched=[parts[start]];exact=false;}
   }
  }
  if(!matched)return 0;
  const explicitWanted=wanted.filter(x=>x.explicit);
  if(explicitWanted.length){
   if(explicitWanted.length!==matched.length||explicitWanted.some((x,i)=>x.tone!==matched[i].tone))return 0;
  }
  if(selectedTone!==null&&matched.some(part=>(part.tone===null?5:part.tone)!==selectedTone))return 0;
  return exact?500:350;
 }
 function textScore(value,query){
  if(!query)return 1;
  const v=normalize(value),q=normalize(query);
  if(!v||!q)return 0;
  if(v===q)return 500;
  if(v.startsWith(q))return 400;
  return v.includes(q)?250:0;
 }
 function matchRow(row,hanzi,pinyin,meaning,tone){
  const h=hanzi?Math.max(textScore(row[0],hanzi),textScore(row[1],hanzi)):1;
  if(!h)return 0;
  const p=pinyin?pinyinScore(row[2],pinyin,tone):1;
  if(!p)return 0;
  const m=meaning?textScore(row[3],meaning):1;
  if(!m)return 0;
  return (hanzi?h:0)+(pinyin?p:0)+(meaning?m:0);
 }
 window.__menu1DictionarySearchTest={normalize,pinyinParts,pinyinScore,textScore,matchRow};
 window.applyFilter=function(){
  const hanzi=$id('dict-search-hanzi')?.value||'';
  const pinyin=$id('dict-search-pinyin')?.value||'';
  const meaning=$id('dict-search-meaning')?.value||'';
  const hasQuery=!!(hanzi.trim()||pinyin.trim()||meaning.trim());
  const rows=Array.isArray(window.dictionary)?window.dictionary:dictionary;
  const found=[];
  if(!hasQuery){filteredIndices=[];}
  else{
   for(let i=0;i<rows.length;i++){
    const score=matchRow(rows[i],hanzi,pinyin,meaning,pinyin.trim()?state.tone:null);
    if(score>0)found.push({i,score});
   }
   found.sort((a,b)=>Array.from(String(rows[a.i][0]||'')).length-Array.from(String(rows[b.i][0]||'')).length||b.score-a.score||a.i-b.i);
   filteredIndices=found.map(x=>x.i);
  }
  currentPage=1;
  renderDictionary();
  const count=$id('dict-result-count');
  if(count&&pinyin.trim()&&state.tone!==null)count.title='Đã lọc Pinyin theo thanh '+(state.tone===5?'nhẹ':state.tone);
 };
 function bind(){
  const fields=['dict-search-hanzi','dict-search-pinyin','dict-search-meaning'].map($id).filter(Boolean);
  if(fields.length!==3)return;
  let timer=null;
  fields.forEach(input=>input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>window.applyFilter(),100);}));
  document.querySelectorAll('[data-dict-tone]').forEach(button=>button.addEventListener('click',()=>{
   const next=Number(button.dataset.dictTone);
   state.tone=state.tone===next?null:next;
   document.querySelectorAll('[data-dict-tone]').forEach(item=>item.setAttribute('aria-pressed',Number(item.dataset.dictTone)===state.tone?'true':'false'));
   window.applyFilter();
  }));
  window.applyFilter();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
})();
</script>
'''
if source.count("</body>") != 1:
    raise SystemExit("Menu 1 script insertion point </body> missing or ambiguous")
source = source.replace("</body>", js + "\n</body>", 1)

required = [
 "MENU1_THREE_FIELD_DICTIONARY_SEARCH_V1",
 'id="dict-search-hanzi"',
 'id="dict-search-pinyin"',
 'id="dict-search-meaning"',
 'data-dict-tone="1"',
 'data-dict-tone="2"',
 'data-dict-tone="3"',
 'data-dict-tone="4"',
 'data-dict-tone="5"',
 "function pinyinScore(candidate,query,selectedTone)",
 "function matchRow(row,hanzi,pinyin,meaning,tone)",
 "window.applyFilter=function()",
 "renderDictionary();"
]
missing = [item for item in required if item not in source]
if missing:
    raise SystemExit("Menu 1 dictionary search verification failed: " + ", ".join(missing))
if source != original:
    target.write_text(source, encoding="utf-8", newline="\n")
print("Menu 1 three-field dictionary search patch: verified")
print("Hanzi, Pinyin, Vietnamese meaning and five single-select tone filters are independent.")
print("Results rank by ascending Hanzi character count, then exactness and source order.")
