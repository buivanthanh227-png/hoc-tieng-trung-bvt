#!/usr/bin/env python3
"""Align Menu 3 colors with its original cyan palette and bind its lookup action."""
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit('Usage: patch_menu3_ui_fix.py <site/index.html>')
p=Path(sys.argv[1]); html=p.read_text(encoding='utf-8')
marker='MENU3_UI_COLOR_AND_LOOKUP_FIX_V1'
if marker in html: raise SystemExit('Menu 3 UI fix already applied.')
if 'id="panel-translate3"' not in html or 'id="homework3x-lookup"' not in html or 'async function lookupHomework3x()' not in html:
    raise SystemExit('Menu 3 cloned panel or lookup function is missing.')
old='''<style id="menu3-independent-color">\n.app-shell #main-tabs .tab[data-tab="translate3"]{--menu-color:#0891b2}\n#panel-translate3{--red:#0891b2;--red2:#0e7490}\n#panel-translate3 .section-title{color:var(--red)}\n#panel-translate3 .btn:not(.secondary){background:var(--red)}\n</style>'''
new='''<style id="menu3-independent-color">\n/* Match the original Menu 3 cyan across navigation, heading banner and panel. */\n.app-shell #main-tabs .tab[data-tab="translate3"]{--menu-color:#0891b2}\n#panel-translate3{--red:#0891b2;--red2:#0e7490}\n#panel-translate3 .section-title{color:#0891b2}\n#panel-translate3 .btn:not(.secondary){background:#0891b2}\n#panel-translate3 .btn:not(.secondary):hover{background:#0e7490}\n</style>'''
if html.count(old)!=1: raise SystemExit('Cannot uniquely locate Menu 3 color override.')
html=html.replace(old,new,1)
old_color='BVT_FUNCTION_COLORS.translate3=BVT_FUNCTION_COLORS.translate;'
new_color="BVT_FUNCTION_COLORS.translate3={main:'#0891b2',alt:'#0e7490'};"
if html.count(old_color)!=1: raise SystemExit('Cannot uniquely locate Menu 3 function-banner color mapping.')
html=html.replace(old_color,new_color,1)
script=r'''<script id="menu3-independent-lookup-binding">
(function(){
 const bind=()=>{
  const button=$('homework3x-lookup'),input=$('homework3x-query');
  if(button&&!button.dataset.menu3LookupBound){
   button.dataset.menu3LookupBound='1';
   button.addEventListener('click',()=>{lookupHomework3x();});
  }
  if(input&&!input.dataset.menu3EnterBound){
   input.dataset.menu3EnterBound='1';
   input.addEventListener('keydown',event=>{if(event.key==='Enter'){event.preventDefault();lookupHomework3x();}});
  }
 };
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
})();
</script>
'''
if '</body>' not in html: raise SystemExit('Missing body close.')
html=html.replace('</body>',script+'<!-- '+marker+' -->\n</body>',1)
p.write_text(html,encoding='utf-8')
print('Menu 3 palette and lookup button/Enter handlers patched.')
