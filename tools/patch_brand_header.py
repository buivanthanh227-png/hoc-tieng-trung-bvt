#!/usr/bin/env python3
"""Inject a responsive three-zone brand banner into the published app shell."""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_brand_header.py <site/index.html>")
target = Path(sys.argv[1])
html = target.read_text(encoding="utf-8")
if "BVT_RESPONSIVE_BRAND_BANNER_V1" in html:
    raise SystemExit("Brand banner patch already applied; refusing duplicate injection.")
if "</body>" not in html:
    raise SystemExit("Cannot find </body> in application HTML.")
overlay = r"""
<style id="bvt-responsive-brand-banner">
.bvt-brand-banner{width:100%;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2.25fr) minmax(0,1fr);align-items:center;gap:clamp(8px,2vw,28px);padding:clamp(8px,1.4vw,18px) clamp(8px,2vw,28px);margin:0 auto;color:#fff;text-align:center;isolation:isolate}
.bvt-brand-side{min-width:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;color:#fff}
.bvt-brand-slogan{display:block;max-width:100%;color:#fff!important;font-size:clamp(10px,.95vw,15px);font-weight:800;letter-spacing:.035em;line-height:1.28;text-align:center;text-wrap:balance;text-shadow:0 1px 4px rgba(0,0,0,.35)}
.bvt-brand-title{min-width:0;margin:0!important;padding:0!important;color:#fff!important;font-size:clamp(25px,4.25vw,58px)!important;font-weight:950!important;letter-spacing:.025em!important;line-height:1.08!important;text-align:center!important;text-wrap:balance;text-shadow:0 3px 10px rgba(0,0,0,.34)}
.topbar{flex-wrap:wrap!important;align-items:center!important}
.topbar .bvt-brand-banner{flex:1 0 100%;order:-100;position:relative;z-index:2}
@media(min-width:1100px){.bvt-brand-banner{max-width:1500px}.bvt-brand-title{font-size:clamp(40px,4vw,62px)!important}.bvt-brand-slogan{font-size:clamp(13px,.95vw,16px)}}
@media(min-width:601px) and (max-width:1099px){.bvt-brand-banner{grid-template-columns:minmax(0,1fr) minmax(0,2fr) minmax(0,1fr);gap:10px;padding:12px 10px}.bvt-brand-title{font-size:clamp(26px,4.4vw,42px)!important}.bvt-brand-slogan{font-size:clamp(10px,1.25vw,13px)}}
@media(max-width:600px){.bvt-brand-banner{grid-template-columns:minmax(0,1fr) minmax(0,1.45fr) minmax(0,1fr);gap:5px;padding:9px 4px}.bvt-brand-side{gap:4px}.bvt-brand-title{font-size:clamp(19px,5.8vw,29px)!important;letter-spacing:0!important;line-height:1.08!important}.bvt-brand-slogan{font-size:clamp(8px,2.45vw,10px);letter-spacing:0;line-height:1.25}}
</style>
<script id="bvt-responsive-brand-banner-script">
(function(){
 function install(){
  if(document.querySelector('.bvt-brand-banner'))return;
  const header=document.querySelector('header.topbar')||document.querySelector('.topbar')||document.querySelector('header');
  if(!header)return;
  const norm=value=>String(value||'').replace(/\s+/g,' ').trim().toLocaleUpperCase('vi');
  function exactElement(phrase){
   const matches=Array.from(header.querySelectorAll('*')).filter(el=>norm(el.textContent)===phrase);
   return matches.sort((a,b)=>a.querySelectorAll('*').length-b.querySelectorAll('*').length)[0]||null;
  }
  [exactElement('HỌC TIẾNG TRUNG'),exactElement('HỌC THÊM MỘT NGÔN NGỮ'),exactElement('SỐNG THÊM MỘT CUỘC ĐỜI')].filter(Boolean).forEach(el=>el.remove());
  const banner=document.createElement('div');banner.className='bvt-brand-banner';banner.setAttribute('aria-label','Học Tiếng Trung BVT');
  const left=document.createElement('div');left.className='bvt-brand-side bvt-brand-left';
  const center=document.createElement('div');center.className='bvt-brand-center';
  const right=document.createElement('div');right.className='bvt-brand-side bvt-brand-right';
  const title=document.createElement('h1');title.className='bvt-brand-title';title.textContent='HỌC TIẾNG TRUNG';
  const leftText=document.createElement('div');leftText.className='bvt-brand-slogan';leftText.textContent='HỌC THÊM MỘT NGÔN NGỮ';
  const rightText=document.createElement('div');rightText.className='bvt-brand-slogan';rightText.textContent='SỐNG THÊM MỘT CUỘC ĐỜI';
  left.append(leftText);center.append(title);right.append(rightText);banner.append(left,center,right);
  header.insertBefore(banner,header.firstChild);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});else install();
})();
</script>
"""
html = html.replace("</body>", overlay + "\n</body>", 1)
target.write_text(html, encoding="utf-8")
