#!/usr/bin/env python3
"""Apply the V42.10.22 requested UI and Menu 3 fixes to the main HTML source."""
from pathlib import Path
import sys

MARKER = 'id="bvt-v4222-user-layout-fixes"'

def replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return source.replace(old, new, 1)

def insert_once(source: str, anchor: str, value: str, label: str) -> str:
    if value.splitlines()[0] in source:
        return source
    if source.count(anchor) != 1:
        raise SystemExit(f"{label}: insertion anchor is missing or duplicated")
    return source.replace(anchor, value + "\n" + anchor, 1)

def main() -> None:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    html = target.read_text(encoding="utf-8")
    if MARKER in html:
        print("V42.10.22 fixes already present; no change.")
        return
    if '<title>HỌC TIẾNG TRUNG · V42.10.22</title>' not in html:
        raise SystemExit("Source version is not V42.10.22; refusing to patch.")

    old_search = """<div class="dict-advanced-search" id="dict-advanced-search">
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
  </div>"""
    new_search = """<div class="dict-advanced-search" id="dict-advanced-search">
   <label class="dict-search-field dict-search-field-meaning" id="dict-search-field-meaning"><span>1. Tìm bằng nghĩa tiếng Việt</span><input id="dict-search-meaning" class="field" type="search" autocomplete="off" placeholder="Vui lòng nhập"></label>
   <label class="dict-search-field dict-search-field-hanzi" id="dict-search-field-hanzi"><span>2. Tìm bằng chữ Hán</span><input id="dict-search-hanzi" class="field" type="search" autocomplete="off" placeholder="Vui lòng nhập"></label>
   <label class="dict-search-field dict-search-field-pinyin" id="dict-search-field-pinyin"><span>3. Tìm bằng phiên âm Pinyin</span><input id="dict-search-pinyin" class="field" type="search" autocomplete="off" placeholder="Vui lòng nhập"></label>
   <div class="dict-tone-picker" id="dict-tone-picker" role="group" aria-label="Lọc thanh điệu Pinyin">
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
   <p class="dict-search-hint">Có thể dùng từng ô riêng hoặc kết hợp nhiều ô để thu hẹp kết quả.</p>
  </div>"""
    html = replace_once(html, old_search, new_search, "Menu 1 search order")

    # Modal copy status and direct button listeners.
    old_meaning = """'<div class="homework3x-modal-line is-meaning"><b>NGHĨA TIẾNG VIỆT</b><div class="homework3x-modal-value">'+escapeHTML(vi||'Chưa có nghĩa tiếng Việt')+'</div><div class="homework3x-modal-actions"><button type="button" data-homework3x-copy="meaning">Sao chép nghĩa</button><button type="button" data-homework3x-speak="vi">🔊 Đọc nghĩa</button></div></div><div class="homework3x-modal-source">Nguồn: '+escapeHTML(item.sourceLabel||item.source||'')+'</div>'+
 '<div class="homework3x-modal-nav">"""
    new_meaning = """'<div class="homework3x-modal-line is-meaning"><b>NGHĨA TIẾNG VIỆT</b><div class="homework3x-modal-value">'+escapeHTML(vi||'Chưa có nghĩa tiếng Việt')+'</div><div class="homework3x-modal-actions"><button type="button" data-homework3x-copy="meaning">Sao chép nghĩa</button><button type="button" data-homework3x-speak="vi">🔊 Đọc nghĩa</button></div></div><div class="homework3x-modal-source">Nguồn: '+escapeHTML(item.sourceLabel||item.source||'')+'</div><div class="homework3x-copy-status" role="status" aria-live="polite"></div>'+
 '<div class="homework3x-modal-nav">"""
    html = replace_once(html, old_meaning, new_meaning, "Menu 3 modal status")

    old_copy = """ const copy=async value=>{
  try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(value);return true;}}catch(_){}
  const area=document.createElement('textarea');area.value=value;area.setAttribute('readonly','');area.style.cssText='position:fixed;left:-9999px;top:0;opacity:0';document.body.appendChild(area);area.select();let ok=false;try{ok=document.execCommand('copy');}catch(_){}area.remove();return ok;
 };"""
    new_copy = """ const copy=async value=>{
  const text=String(value||'');if(!text)return false;
  try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);return true;}}catch(_){}
  const area=document.createElement('textarea');area.value=text;area.readOnly=true;area.setAttribute('aria-hidden','true');
  area.style.cssText='position:fixed;left:0;top:0;width:1px;height:1px;padding:0;border:0;opacity:.01;pointer-events:none;font-size:16px';
  document.body.appendChild(area);let ok=false;
  try{area.focus({preventScroll:true});area.select();area.setSelectionRange(0,area.value.length);ok=document.execCommand('copy');}catch(_){}
  area.remove();return ok;
 };"""
    html = replace_once(html, old_copy, new_copy, "Menu 3 copy fallback")

    copy_anchor = " const playHanziSentence=()=>bvtSpeakLocale(zh,'zh');"
    copy_handlers = """ const copyStatus=modal.querySelector('.homework3x-copy-status');
 modal.querySelectorAll('[data-homework3x-copy]').forEach(button=>button.addEventListener('click',async()=>{
  const kind=button.dataset.homework3xCopy,value=values[kind]||'';
  if(!value){if(copyStatus)copyStatus.textContent='Không có nội dung để sao chép.';return;}
  button.disabled=true;const ok=await copy(value);button.disabled=false;
  if(copyStatus)copyStatus.textContent=ok
   ?(kind==='hanzi'?'Đã sao chép chữ Hán.':kind==='pinyin'?'Đã sao chép Pinyin.':'Đã sao chép nghĩa tiếng Việt.')
   :'Không thể sao chép tự động trên trình duyệt này. Hãy chọn và sao chép nội dung thủ công.';
 }));
 const playHanziSentence=()=>bvtSpeakLocale(zh,'zh');"""
    html = replace_once(html, copy_anchor, copy_handlers, "Menu 3 copy event listeners")

    # Correct Vietnamese routing and add a translation service fallback.
    start = html.find("function looksLikePinyin3x(raw,local){")
    end = html.find("\nlet homework3xLookupToken=0;", start)
    if start < 0 or end <= start:
        raise SystemExit("Menu 3 Pinyin classifier boundary not found.")
    helpers = r"""function looksLikeVietnamese3x(raw){
 const value=String(raw||'').trim();if(!value)return false;
 const hasDistinctive=[...value.toLowerCase()].some(ch=>'ăâđêôơư'.includes(ch));
 if(hasDistinctive)return true;
 const decomposed=value.normalize('NFD').toLowerCase();
 const plain=[...decomposed].filter(ch=>{const code=ch.codePointAt(0);return code<768||code>879;}).join('').replace(/đ/g,'d');
 const words=plain.match(/[a-z]+/g)||[];
 const common=new Set(['xin','chao','toi','ban','la','nguoi','viet','nam','tieng','trung','hoc','khong','mot','muon','dang','can','rat','nhieu','nhung','va','cua','voi','duoc','hom','nay','mai','qua','cam','on','tai','di','den','cho','em','anh','chi','co','thay','nha','minh','chung','biet','noi','lam','an','uong','gia','dinh','con','thich','yeu','dep','xinh','sao','bao','gio','day','kia']);
 return words.length>=2&&words.filter(word=>common.has(word)).length>=2;
}
async function machineTranslate3x(text,source,target){
 const value=String(text||'').trim();if(!value)throw new Error('Nội dung dịch đang trống.');
 if(value.length>1800)throw new Error('Câu quá dài cho dịch vụ dịch miễn phí; hãy chia thành đoạn ngắn hơn.');
 const errors=[],targetChinese=String(target).toLowerCase().startsWith('zh');
 const validate=result=>{
  const translated=String(result||'').trim();if(!translated)throw new Error('Dịch vụ không trả về nội dung.');
  if(targetChinese&&!/[\u3400-\u9fff]/.test(translated))throw new Error('Dịch vụ không trả về câu chữ Hán.');
  return translated;
 };
 const requestJson=async(url,timeoutMs)=>{
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),timeoutMs);
  try{const response=await fetch(url,{method:'GET',cache:'no-store',headers:{Accept:'application/json'},signal:controller.signal});if(!response.ok)throw new Error('HTTP '+response.status);return await response.json();}
  finally{clearTimeout(timer);}
 };
 const byteLength=typeof TextEncoder!=='undefined'?new TextEncoder().encode(value).length:value.length;
 if(byteLength<=480){
  try{
   const url='https://api.mymemory.translated.net/get?q='+encodeURIComponent(value)+'&langpair='+encodeURIComponent(source+'|'+target);
   const data=await requestJson(url,8500);
   if(data?.responseStatus&&Number(data.responseStatus)!==200)throw new Error(String(data.responseDetails||'MyMemory không chấp nhận yêu cầu.'));
   const result=String(data?.responseData?.translatedText||'').trim().replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');
   return {text:validate(result),provider:'MyMemory'};
  }catch(error){errors.push('MyMemory: '+(error?.message||String(error)));}
 }
 try{
  const url='https://translate.googleapis.com/translate_a/single?client=gtx&sl='+encodeURIComponent(source)+'&tl='+encodeURIComponent(target)+'&dt=t&q='+encodeURIComponent(value);
  const data=await requestJson(url,11000);
  const result=Array.isArray(data?.[0])?data[0].map(part=>Array.isArray(part)?String(part[0]||''):'').join('').trim():'';
  return {text:validate(result),provider:'Google Translate'};
 }catch(error){errors.push('Google: '+(error?.message||String(error)));}
 throw new Error('Không kết nối được dịch vụ dịch. '+errors.join(' · '));
}
function looksLikePinyin3x(raw,local){
 if(/[\u3400-\u9fff]/.test(raw)||local&&norm(raw)===norm(local.vi)||looksLikeVietnamese3x(raw))return false;
 const tokens=String(raw||'').trim().split(/[\s,，、;；]+/).filter(Boolean);
 if(!tokens.length)return false;
 const syllables=getPinyin18SourceIndex().syllables;
 return tokens.every(token=>pinyin18CanSegment(token,syllables));
}"""
    html = html[:start] + helpers + html[end:]
    html = replace_once(html, "const translated=await machineTranslate(query,source,target);",
        "const translation=await machineTranslate3x(query,source,target);const translated=translation.text;",
        "Menu 3 translation function")
    html = replace_once(html,
        "renderHomework3xCard({zh:raw,py:pinyinForChinese(raw),vi:translated,note:'Bản dịch máy online'},'Trung → Việt');",
        "renderHomework3xCard({zh:raw,py:pinyinForChinese(raw),vi:translated,note:'Bản dịch máy online · '+translation.provider},'Trung → Việt');",
        "Menu 3 provider label zh-vi")
    html = replace_once(html,
        "renderHomework3xCard({zh,py:pinyinForChinese(zh,curated?.py||''),vi:raw,note:curated?'Câu mẫu đã kiểm chứng':'Bản dịch máy online'},'Việt → Trung');",
        "renderHomework3xCard({zh,py:pinyinForChinese(zh,curated?.py||''),vi:raw,note:curated?'Câu mẫu đã kiểm chứng':'Bản dịch máy online · '+translation.provider},'Việt → Trung');",
        "Menu 3 provider label vi-zh")

    # Keep clock's existing update targets; group time/icon as a centered row.
    old_clock = """ <div class="bvt-footer-clock-v2" id="bvt-header-clock" aria-label="Giờ và ngày hiện tại">
  <svg class="bvt-clock-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.2" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 6.5v5.8l4 2.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <span id="bvt-clock-time">--:--:--</span>
  <span id="bvt-clock-date" class="bvt-clock-date">ĐANG TẢI NGÀY THÁNG…</span>
 </div>"""
    new_clock = """ <div class="bvt-footer-clock-v2" id="bvt-header-clock" aria-label="Giờ và ngày hiện tại">
  <div class="bvt-footer-clock-main">
   <svg class="bvt-clock-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.2" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 6.5v5.8l4 2.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
   <span id="bvt-clock-time">--:--:--</span>
  </div>
  <span id="bvt-clock-date" class="bvt-clock-date">ĐANG TẢI NGÀY THÁNG…</span>
 </div>"""
    html = replace_once(html, old_clock, new_clock, "Footer clock markup")

    # Append centered-title observer at the end of the document.
    banner_script = """<script id="bvt-v4222-banner-center-runtime">
(function(){
 const brand=document.querySelector('.topbar .brand');
 const left=brand?.querySelector('.brand-flag:first-child'),right=brand?.querySelector('.brand-flag:last-child');
 const title=brand?.querySelector('.brand-copy>h1');if(!brand||!left||!right||!title)return;
 let frame=0;
 function align(){
  frame=0;title.style.setProperty('--bvt-banner-title-shift','0px');
  const a=left.getBoundingClientRect(),b=right.getBoundingClientRect(),t=title.getBoundingClientRect();
  if(!a.width||!b.width||!t.width)return;
  const target=((a.left+a.right)/2+(b.left+b.right)/2)/2,delta=target-(t.left+t.right)/2;
  title.style.setProperty('--bvt-banner-title-shift',Math.abs(delta)<0.25?'0px':delta.toFixed(2)+'px');
 }
 function schedule(){if(frame)cancelAnimationFrame(frame);frame=requestAnimationFrame(align);}
 schedule();window.addEventListener('resize',schedule,{passive:true});
 if('ResizeObserver'in window){const observer=new ResizeObserver(schedule);[brand,left,right,title].forEach(node=>observer.observe(node));}
 if(document.fonts?.ready)document.fonts.ready.then(schedule).catch(()=>{});
 window.addEventListener('load',schedule,{once:true});
})();
</script>"""
    if 'id="bvt-v4222-banner-center-runtime"' not in html:
        html = replace_once(html, "</body>", banner_script+"\n</body>", "Banner centering script")

    target.write_text(html, encoding="utf-8")
    print(f"Patched {target}: Menu 1, Menu 3, banner centering, footer clock; {len(html)} characters.")

if __name__ == "__main__":
    main()
