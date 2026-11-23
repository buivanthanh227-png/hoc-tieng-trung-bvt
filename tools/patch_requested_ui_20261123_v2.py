#!/usr/bin/env python3
"""V2 repair: align slogans to flags, relocate real clock/credit safely, and harden dictionary startup."""
from pathlib import Path
import sys, json

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_requested_ui_20261123_v2.py <site/index.html>")
path = Path(sys.argv[1])
html = path.read_text(encoding="utf-8")
MARK = "BVT_REQUESTED_UI_20261123_V2"
if MARK in html:
    print("Requested UI V2 patch already applied")
    raise SystemExit(0)

css = """<style id="bvt-banner-footer-layout-v2">
/* Surface dictionary loading/error feedback instead of silently leaving the count at “loading”. */
#dict-status:not([hidden]){display:block!important;margin:8px 0!important;padding:9px 11px!important;border-radius:10px!important;font-size:12px!important;line-height:1.45!important;overflow-wrap:anywhere!important}
#dict-status.error:not([hidden]){color:#991b1b!important;background:#fef2f2!important;border:1px solid #fecaca!important}
#dict-status.ok:not([hidden]){color:#166534!important;background:#f0fdf4!important;border:1px solid #bbf7d0!important}

/* One grid owns the header geometry: flags | centered title | flags;
   slogans are independent grid children under their matching flags. */
.topbar .brand{
 display:grid!important;
 grid-template-columns:minmax(0,1fr) minmax(0,auto) minmax(0,1fr)!important;
 grid-template-rows:auto auto!important;
 align-items:center!important;justify-items:stretch!important;
 column-gap:clamp(4px,1.2vw,12px)!important;row-gap:5px!important;
 width:100%!important;max-width:1100px!important;min-width:0!important;
 margin:0 auto!important;box-sizing:border-box!important
}
.topbar .brand>.brand-flag:first-child{
 grid-column:1!important;grid-row:1!important;justify-self:center!important;
 align-self:center!important;width:clamp(34px,5vw,62px)!important;
 height:auto!important;aspect-ratio:3/2!important;box-sizing:border-box!important
}
.topbar .brand>.brand-flag:last-child{
 grid-column:3!important;grid-row:1!important;justify-self:center!important;
 align-self:center!important;width:clamp(34px,5vw,62px)!important;
 height:auto!important;aspect-ratio:3/2!important;box-sizing:border-box!important
}
.topbar .brand>.brand-flag svg{display:block!important;width:100%!important;height:100%!important}
.topbar .brand>.brand-copy{display:contents!important}
.topbar .brand-copy>h1{
 grid-column:2!important;grid-row:1!important;justify-self:center!important;
 align-self:center!important;width:max-content!important;max-width:100%!important;
 min-width:0!important;margin:0!important;padding:0!important;
 color:#fff!important;text-align:center!important;white-space:nowrap!important;
 font-size:clamp(13px,3.6vw,34px)!important;line-height:1.08!important;
 letter-spacing:0!important;font-weight:900!important;overflow:visible!important
}
.topbar .brand-copy>.brand-slogan{display:contents!important}
.topbar .brand-slogan>span:first-child{
 grid-column:1!important;grid-row:2!important;justify-self:stretch!important;
 align-self:start!important;width:100%!important;text-align:left!important
}
.topbar .brand-slogan>span:last-child{
 grid-column:3!important;grid-row:2!important;justify-self:stretch!important;
 align-self:start!important;width:100%!important;text-align:right!important
}
.topbar .brand-slogan>span{
 display:block!important;min-width:0!important;margin:0!important;padding:0!important;
 color:#fff!important;font-size:clamp(7px,1.8vw,11px)!important;
 font-weight:850!important;line-height:1.22!important;letter-spacing:0!important;
 white-space:normal!important;overflow-wrap:anywhere!important;word-break:normal!important
}
#app-footer-meta .bvt-footer-credit-line-v2{
 display:flex!important;justify-content:center!important;align-items:center!important;
 flex-wrap:wrap!important;gap:4px!important;margin:4px 0 10px!important;
 width:100%!important;box-sizing:border-box!important;text-align:center!important;
 font-size:12px!important;font-weight:750!important;color:#111!important
}
#app-footer-meta .bvt-footer-credit-line-v2,
#app-footer-meta .bvt-footer-credit-line-v2 *{color:#111!important}
#app-footer-meta .bvt-footer-version-row-v2{
 display:flex!important;align-items:center!important;justify-content:space-between!important;
 flex-wrap:nowrap!important;gap:8px!important;width:100%!important;max-width:100%!important;
 min-width:0!important;box-sizing:border-box!important;padding:0 8px 0 0!important;
 overflow:visible!important;margin:0 0 8px!important
}
#app-footer-meta .bvt-footer-version-row-v2 .bvt-version-node-v2{
 margin:0!important;min-width:0!important;max-width:52%!important;overflow-wrap:anywhere!important
}
#app-footer-meta #bvt-header-clock{
 display:flex!important;flex:0 1 auto!important;flex-direction:column!important;
 align-items:flex-end!important;justify-content:center!important;gap:2px!important;
 margin:0 0 0 auto!important;padding:2px 8px 2px 4px!important;
 box-sizing:border-box!important;width:auto!important;max-width:48%!important;min-width:0!important;
 text-align:right!important;font-size:11px!important;line-height:1.35!important;
 white-space:normal!important;overflow:visible!important;color:#dc2626!important
}
#app-footer-meta #bvt-header-clock,
#app-footer-meta #bvt-header-clock *{color:#dc2626!important}
#app-footer-meta #bvt-clock-time{font-weight:900!important;font-variant-numeric:tabular-nums}
#app-footer-meta #bvt-clock-date{font-size:10px!important;font-weight:800!important}
.topbar .top-meta #bvt-header-clock{display:none!important}
@media(max-width:520px){
 .topbar .brand{column-gap:4px!important;row-gap:4px!important}
 .topbar .brand-copy>h1{font-size:clamp(12px,3.8vw,18px)!important}
 .topbar .brand-slogan>span{font-size:clamp(6.5px,1.85vw,8.5px)!important;line-height:1.18!important}
 #app-footer-meta .bvt-footer-version-row-v2{gap:4px!important;padding-right:5px!important}
 #app-footer-meta .bvt-footer-version-row-v2 .bvt-version-node-v2{max-width:50%!important}
 #app-footer-meta #bvt-header-clock{max-width:48%!important;font-size:9px!important;padding-right:6px!important}
 #app-footer-meta #bvt-clock-date{font-size:8px!important}
}
@media(max-width:350px){
 .topbar .brand-copy>h1{font-size:11px!important}
 .topbar .brand-slogan>span{font-size:6.2px!important}
}
</style>
"""
if 'id="bvt-banner-footer-layout-v2"' not in html:
    if html.count("</head>") != 1:
        raise SystemExit("Expected one </head> for V2 CSS insertion")
    html = html.replace("</head>", css + "\n</head>", 1)

footer_js = r"""<script id="bvt-footer-meta-move-v2">
(function(){
 function moveFooterMeta(){
  const footer=document.getElementById('app-footer-meta');
  if(!footer||footer.dataset.bvtMetaV2==='1')return;
  const topMeta=document.querySelector('.topbar .top-meta');
  const credit=topMeta&&topMeta.querySelector('.credit-line');
  const clock=document.getElementById('bvt-header-clock');
  const oldBox=document.getElementById('bvt-footer-meta-v1');
  let version=null;
  if(oldBox){
   version=oldBox.querySelector('.bvt-footer-version-row-v1>*');
   const oldCredit=oldBox.querySelector('.bvt-footer-credit-v1');
   if(credit&&oldCredit)credit.appendChild(oldCredit);
   const oldStatus=oldBox.querySelector('#top-status');
   if(oldStatus)oldStatus.remove();
  }
  if(!version)version=[...footer.children].find(el=>/phiên bản/i.test(el.textContent||''));
  if(!version)return;
  const row=document.createElement('div');
  row.className='bvt-footer-version-row-v2';
  version.classList.add('bvt-version-node-v2');
  if(credit){
   credit.classList.add('bvt-footer-credit-line-v2');
   footer.insertBefore(credit,footer.firstChild);
  }
  const insertionPoint=credit?credit.nextSibling:footer.firstChild;
  footer.insertBefore(row,insertionPoint);
  row.appendChild(version);
  if(clock)row.appendChild(clock);
  if(oldBox){
   const oldParent=oldBox.parentElement;
   oldBox.remove();
   if(oldParent&&oldParent!==footer&&!oldParent.children.length&&!oldParent.textContent.trim())oldParent.remove();
  }
  footer.dataset.bvtMetaV2='1';
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',moveFooterMeta,{once:true});
 else moveFooterMeta();
})();
</script>
"""
if 'id="bvt-footer-meta-move-v2"' not in html:
    if html.count("</body>") != 1:
        raise SystemExit("Expected one </body> for V2 footer script insertion")
    html = html.replace("</body>", footer_js + "\n</body>", 1)


# Menu 1: mutate the parsed dataset in place. Avoid allocating a second 122k-row
# array while retaining the parsed JSON, which can exceed mobile Safari memory.
old_merge = "function mergeRows(rows){const out=buildSeed();const seen=new Set(out.map(r=>r[0]+'|'+r[1]+'|'+keyPinyin(r[2])));for(const raw of rows){if(!Array.isArray(raw)||raw.length<4)continue;const row=[String(raw[0]||''),String(raw[1]||raw[0]||''),String(raw[2]||''),String(raw[3]||''),String(raw[4]||hskFromSeed(raw[0])||'')];if(!row[0]||!row[3])continue;const k=row[0]+'|'+row[1]+'|'+keyPinyin(row[2]);if(seen.has(k))continue;seen.add(k);out.push(row);}return out;}"
new_merge = "function mergeRows(rows){const out=Array.isArray(rows)?rows:[];const seen=new Set();let write=0;for(let read=0;read<out.length;read++){const raw=out[read];if(!Array.isArray(raw)||raw.length<4||!raw[0]||!raw[3])continue;raw[0]=String(raw[0]);raw[1]=String(raw[1]||raw[0]);raw[2]=String(raw[2]||'');raw[3]=String(raw[3]);raw[4]=String(raw[4]||hskFromSeed(raw[0])||'');const key=raw[0]+'|'+raw[1]+'|'+keyPinyin(raw[2]);if(seen.has(key))continue;seen.add(key);out[write++]=raw;}out.length=write;for(const raw of buildSeed()){const key=raw[0]+'|'+raw[1]+'|'+keyPinyin(raw[2]);if(!seen.has(key)){seen.add(key);out.push(raw);}}return out;}"
if html.count(old_merge) != 1:
    raise SystemExit(f"Expected one original mergeRows function; found {html.count(old_merge)}")
html = html.replace(old_merge, new_merge, 1)
for old, new, label in [
    ("$('dict-status').textContent=hasEmbedded?", "$('dict-status').hidden=false;$('dict-status').textContent=hasEmbedded?", "show initial dictionary status"),
    ("const rows=mergeRows(parsed);setDictionary(rows,'CVDICT Trung–Việt nhúng sẵn');", "const rows=mergeRows(parsed);parsed=null;setDictionary(rows,'CVDICT Trung–Việt nhúng sẵn');", "release parsed JSON reference"),
    ("catch(e){$('dict-status').className='source-status error';", "catch(e){try{setDictionary(buildSeed(),'Bộ từ cơ bản dự phòng');}catch(fallbackError){}if(typeof window.__menu1DictionaryLoaded==='function')window.__menu1DictionaryLoaded(dictionary.length,'bộ từ cơ bản dự phòng');$('dict-status').className='source-status error';", "reset to searchable seed when embedded loading fails"),
    ("init();", "init().catch(error=>{try{setDictionary(buildSeed(),'Bộ từ cơ bản dự phòng');}catch(fallbackError){}const status=$('dict-status');if(typeof window.__menu1DictionaryLoaded==='function')window.__menu1DictionaryLoaded(dictionary.length,'bộ từ cơ bản dự phòng');status.hidden=false;status.className='source-status error';status.textContent='⚠️ Lỗi khởi tạo từ điển: '+(error&&error.message?error.message:String(error))+'. Đang dùng bộ từ cơ bản dự phòng.';});", "surface unexpected initialization errors")
]:
    if html.count(old) != 1:
        raise SystemExit(f"Expected one insertion point to {label}; found {html.count(old)}")
    html = html.replace(old, new, 1)



# Expose the live dictionary explicitly for the independently injected Menu 1
# search controller; do not rely on cross-script lexical global resolution.
dictionary_marker = "function setDictionary(rows,sourceName){dictionary=rows;"
if html.count(dictionary_marker) != 1:
    raise SystemExit(f"Expected one setDictionary assignment point; found {html.count(dictionary_marker)}")
html = html.replace(dictionary_marker, dictionary_marker + "window.dictionary=dictionary;", 1)

set_marker = "applyFilter();renderCombineChoices();"
if html.count(set_marker) != 1:
    raise SystemExit(f"Expected one setDictionary refresh point; found {html.count(set_marker)}")
html = html.replace(set_marker,
    "applyFilter();if(typeof window.__menu1DictionaryLoaded==='function')window.__menu1DictionaryLoaded(dictionary.length,sourceName);renderCombineChoices();",1)

cache_marker = "if(Array.isArray(cached)&&cached.length>1000){"
if html.count(cache_marker) != 1:
    raise SystemExit(f"Expected one cached dictionary threshold; found {html.count(cache_marker)}")
html = html.replace(cache_marker, "if(Array.isArray(cached)&&cached.length>=(hasEmbedded?120000:1000)){", 1)

error_marker = "$('dict-status').className='source-status error';$('dict-status').textContent='⚠️ Không nạp được dữ liệu từ điển nhúng:"
if html.count(error_marker) != 1:
    raise SystemExit(f"Expected one embedded dictionary error handler; found {html.count(error_marker)}")
html = html.replace(error_marker, "$('dict-status').hidden=false;"+error_marker, 1)

if "MENU1_THREE_FIELD_DICTIONARY_SEARCH_V1" not in html:
    raise SystemExit("Menu 1 three-field search script is missing")
callback = r"""
window.__menu1DictionaryLoaded=function(count,sourceName){
 if(typeof window.applyFilter==='function')window.applyFilter();
 const status=$id('dict-status');
 if(status){
  status.hidden=false;status.className='source-status ok';
  status.textContent='✅ Đã nạp '+Number(count||0).toLocaleString('vi-VN')+' mục từ từ '+String(sourceName||'từ điển tiếng Trung')+'. Bạn có thể tra cứu bằng chữ Hán, Pinyin hoặc nghĩa tiếng Việt.';
 }
 window.__menu1DictionaryLoadedCount=Number(count||0);
};
"""
bind_marker = " function bind(){"
if html.count(bind_marker) != 1:
    raise SystemExit("Menu 1 bind() insertion point missing or ambiguous")
html = html.replace(bind_marker, callback + "\n"+bind_marker, 1)

data_start = html.find('id="embedded-cvdict-data"')
if data_start < 0:
    raise SystemExit("Embedded CVDICT data block is missing")
tag_end = html.find(">", data_start)
data_end = html.find("</script>", tag_end)
if tag_end < 0 or data_end < 0:
    raise SystemExit("Embedded CVDICT data block is malformed")
try:
    rows = json.loads(html[tag_end+1:data_end])
except Exception as exc:
    raise SystemExit("Embedded CVDICT JSON is invalid: "+str(exc))
if not isinstance(rows, list) or len(rows) < 120000:
    raise SystemExit(f"Embedded CVDICT is incomplete: {len(rows) if isinstance(rows,list) else 'not an array'} rows")

html = html.replace("</body>", "<!-- "+MARK+" -->\n</body>", 1)
path.write_text(html, encoding="utf-8", newline="\n")
print(f"PASS: V2 slogan alignment, full author credit/clock relocation, dictionary loader hook; embedded CVDICT rows={len(rows):,}.")
