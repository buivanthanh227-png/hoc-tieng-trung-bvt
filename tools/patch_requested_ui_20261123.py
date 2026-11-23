#!/usr/bin/env python3
"""Apply the requested Menu 3, Menu 18, banner and Menu 1 refinements."""
from pathlib import Path
import re,sys

if len(sys.argv)!=2: raise SystemExit("Usage: patch_requested_ui_20261123.py <site/index.html>")
p=Path(sys.argv[1]); h=p.read_text(encoding="utf-8")
MARK="BVT_REQUESTED_UI_20261123_V1"
if MARK in h: raise SystemExit("Requested UI patch already applied.")

# Menu 3: make Hanzi, Pinyin and Vietnamese modal values exactly the same size.
if 'id="panel-translate3"' not in h: raise SystemExit("Independent Menu 3 panel missing.")
modal_css="""<style id="bvt-menu3-modal-equal-font">
#panel-translate3 .homework3x-modal-line .homework3x-modal-value,
#panel-translate3 .homework3x-modal-line.is-hanzi .homework3x-modal-value,
#panel-translate3 .homework3x-modal-line.is-pinyin .homework3x-modal-value,
#panel-translate3 .homework3x-modal-line.is-meaning .homework3x-modal-value{
 font-size:22px!important;font-weight:800!important;line-height:1.45!important;
}
</style>
"""
if 'id="bvt-menu3-modal-equal-font"' not in h:
    h=h.replace("</head>",modal_css+"\n</head>",1)

# Remove Menu 18 navigation button and panel after Menu 3 has been cloned from it.
nav_start=h.find('<nav id="main-tabs"')
nav_end=h.find('</nav>',nav_start)
if nav_start<0 or nav_end<0: raise SystemExit("Main navigation not found.")
nav=h[nav_start:nav_end+6]
buttons=list(re.finditer(r'<button\b[\s\S]*?</button>',nav))
remove_buttons=[]
for m in buttons:
    b=m.group(0)
    if ('data-tab="translate-experimental"' in b or
        'DỊCH NHANH VIỆT ⇄ TRUNG (THỬ NGHIỆM)' in b or
        ('data-function-number="18"' in b and 'data-tab=' in b)):
        remove_buttons.append(m)
if len(remove_buttons)!=1:
    raise SystemExit(f"Expected one Menu 18 nav button; found {len(remove_buttons)}")
b=remove_buttons[0]
nav=nav[:b.start()]+nav[b.end():]
h=h[:nav_start]+nav+h[nav_end+6:]

panel_start=h.find('<section id="panel-translate-experimental"')
if panel_start<0: raise SystemExit("Menu 18 panel start missing.")
panel_end=h.find('\n<section id="',panel_start+1)
if panel_end<0: raise SystemExit("Menu 18 panel end missing.")
h=h[:panel_start]+h[panel_end+1:]

# Remove the Menu 18-only cloned-source renderer block; Menu 3 has its own namespaced copy.
logic_start=h.find("function renderHomework18Card(result,sourceLabel=''){")
logic_end=h.find("async function machineTranslate(text,source,target){",logic_start)
if logic_start>=0 and logic_end>logic_start:
    h=h[:logic_start]+h[logic_end:]
# Remove Menu 18-only visual style block.
style_start=h.find('<style id="menu18-experimental-styles">')
if style_start>=0:
    style_end=h.find('</style>',style_start)
    if style_end<0: raise SystemExit("Menu 18 style block is malformed.")
    h=h[:style_start]+h[style_end+8:]

# Banner: title larger; both slogans remain on one line each on all screen sizes.
banner_css="""<style id="bvt-banner-footer-layout-v1">
.topbar .brand-copy>h1{font-size:clamp(19px,5.4vw,42px)!important;line-height:1.04!important;letter-spacing:-.015em!important}
.topbar .brand-slogan>span{white-space:nowrap!important;overflow:hidden!important;text-overflow:clip!important;overflow-wrap:normal!important;word-break:keep-all!important;text-wrap:nowrap!important}
.topbar .brand-slogan>span:first-child{text-align:left!important}
.topbar .brand-slogan>span:last-child{text-align:right!important}
@media(max-width:600px){
 .topbar .brand-copy>h1{font-size:clamp(16px,5.2vw,24px)!important}
 .topbar .brand-slogan>span{font-size:clamp(6.4px,1.8vw,8.2px)!important;letter-spacing:-.025em!important}
}
@media(max-width:350px){.topbar .brand-copy>h1{font-size:15px!important}.topbar .brand-slogan>span{font-size:6px!important}}
#bvt-footer-meta-v1{display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:4px!important;width:100%!important;margin:12px auto 4px!important;padding:8px 12px!important;box-sizing:border-box!important}
#bvt-footer-meta-v1 .bvt-footer-credit-v1{display:block!important;text-align:center!important;width:100%!important;font-size:12px!important;font-weight:700!important}
#bvt-footer-meta-v1 .bvt-footer-version-row-v1{display:flex!important;align-items:center!important;justify-content:flex-end!important;gap:12px!important;width:100%!important}
#bvt-footer-meta-v1 .bvt-footer-version-row-v1>*{margin:0!important}
#bvt-footer-meta-v1 .bvt-footer-status-v1{display:block!important;text-align:right!important;margin-left:0!important;font-size:11px!important;white-space:nowrap!important}
.topbar #top-status{display:none!important}
</style>
"""
if 'id="bvt-banner-footer-layout-v1"' not in h:
    h=h.replace("</head>",banner_css+"\n</head>",1)

# Move the existing status (clock/day/date) and existing author credit to the footer,
# immediately before the application-version line; no duplicate clock is created.
footer_js=r"""<script id="bvt-footer-meta-move-v1">
(function(){
 function moveMeta(){
  const body=document.body;if(!body||document.getElementById('bvt-footer-meta-v1'))return;
  const versionLeaf=[...body.querySelectorAll('*')].find(el=>el.children.length===0&&!['SCRIPT','STYLE'].includes(el.tagName)&&/V?42\.\d+\.\d+|phiên bản ứng dụng/i.test(el.textContent||''));
  if(!versionLeaf)return;
  const parent=versionLeaf.parentElement||body;
  const box=document.createElement('div');box.id='bvt-footer-meta-v1';
  const credit=[...body.querySelectorAll('*')].find(el=>el.children.length===0&&/Bùi Văn Thành|Bui Van Thanh|©\s*2026|thiết kế và phát triển/i.test(el.textContent||''));
  if(credit){credit.classList.add('bvt-footer-credit-v1');box.appendChild(credit);}
  const status=document.getElementById('top-status');
  const row=document.createElement('div');row.className='bvt-footer-version-row-v1';
  if(status){status.classList.add('bvt-footer-status-v1');status.style.display='block';}
  parent.insertBefore(box,versionLeaf);
  row.appendChild(versionLeaf);
  if(status)row.appendChild(status);
  box.appendChild(row);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',moveMeta,{once:true});else moveMeta();
})();
</script>
"""
if 'id="bvt-footer-meta-move-v1"' not in h:
    h=h.replace("</body>",footer_js+"\n</body>",1)

# Ensure the retired menu is no longer exposed as a panel/navigation item.
if 'id="panel-translate-experimental"' in h or 'data-tab="translate-experimental"' in h:
    raise SystemExit("Menu 18 navigation or panel remains after removal.")
if 'id="panel-translate3"' not in h: raise SystemExit("Menu 3 panel was damaged during Menu 18 removal.")

# Menu 1: color the tone controls (the existing search fields remain independent).
menu1_css="""<style id="bvt-menu1-colored-actions-v1">
#dict-advanced-search .dict-tone-buttons button{color:#fff!important;border:1px solid transparent!important;font-weight:850!important;box-shadow:0 2px 5px rgba(16,24,40,.13)!important}
#dict-advanced-search .dict-tone-buttons button[data-dict-tone="1"]{background:#2563eb!important}
#dict-advanced-search .dict-tone-buttons button[data-dict-tone="2"]{background:#0f9d72!important}
#dict-advanced-search .dict-tone-buttons button[data-dict-tone="3"]{background:#d97706!important}
#dict-advanced-search .dict-tone-buttons button[data-dict-tone="4"]{background:#dc2626!important}
#dict-advanced-search .dict-tone-buttons button[data-dict-tone="5"]{background:#64748b!important}
#dict-advanced-search .dict-tone-buttons button[aria-pressed="true"]{outline:3px solid rgba(15,23,42,.22)!important;outline-offset:1px!important;filter:brightness(.82)!important}
</style>
"""
if 'id="dict-advanced-search"' in h and 'id="bvt-menu1-colored-actions-v1"' not in h:
    h=h.replace("</head>",menu1_css+"\n</head>",1)

h=h.replace("</body>","<!-- "+MARK+" -->\n</body>",1)
p.write_text(h,encoding="utf-8",newline="\n")
print("PASS: Menu 3 modal font equalized; Menu 18 navigation/panel removed; banner slogans/title adjusted; footer status moved; Menu 1 tone buttons colored.")
