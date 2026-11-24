#!/usr/bin/env python3
"""Unify right-side heading typography and bind its accent to each selected menu banner."""
from pathlib import Path
import re
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
html = path.read_text(encoding="utf-8")

tabs = re.findall(r'<button\b[^>]*class="[^"]*\btab\b[^"]*"[^>]*data-tab="([^"]+)"', html)
if len(tabs) != 17:
    tabs = re.findall(r'<button\b(?=[^>]*class="[^"]*\btab\b)(?=[^>]*data-tab="[^"]+")[^>]*>', html)
if len(tabs) != 17:
    raise SystemExit(f"Expected exactly 17 navigation menu buttons; found {len(tabs)}.")
required = ["BVT_FUNCTION_COLORS", "function bvtSyncFunctionHeading", "function switchTab(tab)"]
missing = [token for token in required if token not in html]
if missing:
    raise SystemExit("Cannot verify existing heading/color architecture: " + ", ".join(missing))
heading_tags = re.findall(r'<h[1-6]\b[^>]*class="[^"]*\bsection-title\b[^"]*"[^>]*>', html)
if len(heading_tags) < 17:
    raise SystemExit(f"Expected at least 17 numbered right-side headings; found {len(heading_tags)}.")

style = """<style id="bvt-unified-17-menu-headings-v2">
/* Normalize heading and nested fragments: no menu-specific oversized text. */
body .panel .section-title,
body .panel .section-title * {
  box-sizing: border-box !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", sans-serif !important;
  font-size: 18px !important;
  font-weight: 850 !important;
  line-height: 1.3 !important;
  letter-spacing: 0 !important;
}
body .panel .section-title {
  color: var(--red) !important;
  max-width: 100% !important;
  overflow-wrap: break-word !important;
  word-break: normal !important;
  text-wrap: pretty;
}
body .panel .section-title * { color: inherit !important; }
@media (max-width: 600px) {
  body .panel .section-title,
  body .panel .section-title * {
    font-size: 16px !important;
    line-height: 1.3 !important;
  }
}
</style>"""
style_pattern = re.compile(r'<style id="bvt-unified-17-menu-headings-v[12]">.*?</style>', re.S)
if style_pattern.search(html):
    html, count = style_pattern.subn(style, html)
    if count != 1: raise SystemExit(f"Expected one old heading style; found {count}.")
else:
    if html.count("</head>") != 1: raise SystemExit("Cannot uniquely locate </head>.")
    html = html.replace("</head>", style + "\n</head>", 1)

script = r"""<script id="bvt-unified-17-menu-headings-runtime-v2">
(function(){
  function syncSelectedHeading(){
    const panel=document.querySelector('.panel.active');
    if(!panel)return;
    const heading=panel.querySelector('.section-title');
    if(!heading)return;
    const key=String(panel.id||'').replace(/^panel-/,'');
    let palette=null;
    try{if(typeof BVT_FUNCTION_COLORS!=='undefined')palette=BVT_FUNCTION_COLORS[key]||null;}catch(_){}
    let accent=palette&&(palette.main||palette.alt);
    if(!accent){
      accent=getComputedStyle(panel).getPropertyValue('--red').trim()||
        getComputedStyle(document.documentElement).getPropertyValue('--red').trim();
    }
    const size=matchMedia('(max-width: 600px)').matches?'16px':'18px';
    const styles={'font-family':'-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", sans-serif',
      'font-size':size,'font-weight':'850','line-height':'1.3','letter-spacing':'0'};
    Object.entries(styles).forEach(([k,v])=>heading.style.setProperty(k,v,'important'));
    if(accent)heading.style.setProperty('color',accent,'important');
    heading.querySelectorAll('*').forEach(node=>{
      Object.entries(styles).forEach(([k,v])=>node.style.setProperty(k,v,'important'));
      node.style.setProperty('color','inherit','important');
    });
  }
  function schedule(){requestAnimationFrame(syncSelectedHeading);}
  document.addEventListener('click',event=>{
    if(event.target&&event.target.closest&&event.target.closest('#main-tabs .tab'))schedule();
  },true);
  window.addEventListener('resize',schedule,{passive:true});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule,{once:true});
  else schedule();
})();
</script>"""
script_pattern = re.compile(r'<script id="bvt-unified-17-menu-headings-runtime-v2">.*?</script>', re.S)
if script_pattern.search(html):
    html, count = script_pattern.subn(script, html)
    if count != 1: raise SystemExit(f"Expected one heading runtime; found {count}.")
else:
    if html.count("</body>") != 1: raise SystemExit("Cannot uniquely locate </body>.")
    html = html.replace("</body>", script + "\n</body>", 1)

if html.count('id="bvt-unified-17-menu-headings-v2"') != 1 or html.count('id="bvt-unified-17-menu-headings-runtime-v2"') != 1:
    raise SystemExit("Heading style/runtime validation failed.")
path.write_text(html,encoding="utf-8")
print(f"Unified {len(heading_tags)} headings: 18px desktop, 16px mobile; selected banner accent applied dynamically.")
