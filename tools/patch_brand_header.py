#!/usr/bin/env python3
"""Build a compact three-column header and move the dictionary word count."""
from pathlib import Path
import re,sys

if len(sys.argv)!=2: raise SystemExit('Usage: patch_brand_header.py <site/index.html>')
p=Path(sys.argv[1]); html=p.read_text(encoding='utf-8')
if 'BVT_FLAGS_AND_SPLIT_SLOGANS_V3' in html: raise SystemExit('Brand header v3 already applied.')
if html.count('class="brand-flag"')!=2 or html.count('class="brand-slogan"')!=1:
    raise SystemExit('Expected exactly two original flags and one original two-line slogan block.')

count=re.search(r'<span class="count-pill" id="count-pill">.*?</span>',html,re.S)
if not count: raise SystemExit('Cannot locate dictionary word-count badge.')
count_html=count.group(0)
html=html[:count.start()]+html[count.end():]
label='<span class="tab-label">TỪ ĐIỂN TIẾNG TRUNG</span>'
if html.count(label)!=1: raise SystemExit('Cannot uniquely locate Dictionary navigation label.')
html=html.replace(label,label+count_html,1)

style="""<style id="bvt-responsive-brand-banner">
/* Three-column banner: Vietnam flag | centered title | China flag.
   Each slogan sits below its corresponding flag, left/right aligned. */
.topbar .toprow{display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:center!important;gap:7px!important;width:100%;}
.topbar .brand{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1.8fr) minmax(0,1fr)!important;grid-template-rows:auto auto!important;align-items:center!important;justify-items:stretch!important;gap:5px 10px!important;width:100%!important;max-width:1100px!important;min-width:0!important;margin:0 auto!important;flex:none!important;}
.topbar .brand>.brand-flag:first-child{grid-column:1!important;grid-row:1!important;justify-self:center!important;align-self:center!important;width:clamp(38px,5vw,62px)!important;height:auto!important;aspect-ratio:3/2!important;padding:3px!important;overflow:hidden!important;}
.topbar .brand>.brand-flag:last-child{grid-column:3!important;grid-row:1!important;justify-self:center!important;align-self:center!important;width:clamp(38px,5vw,62px)!important;height:auto!important;aspect-ratio:3/2!important;padding:3px!important;overflow:hidden!important;}
.topbar .brand>.brand-flag svg{display:block!important;width:100%!important;height:100%!important;max-height:none!important;}
.topbar .brand>.brand-copy{display:contents!important;}
.topbar .brand-copy>h1{grid-column:2!important;grid-row:1!important;align-self:center!important;justify-self:center!important;width:100%!important;max-width:100%!important;margin:0!important;padding:0!important;color:#fff!important;font-size:clamp(14px,4.3vw,34px)!important;font-weight:900!important;line-height:1.08!important;letter-spacing:0!important;text-align:center!important;white-space:nowrap!important;overflow:visible!important;}
.topbar .brand-copy>.brand-slogan{display:contents!important;}
.topbar .brand-slogan>span:first-child{grid-column:1!important;grid-row:2!important;justify-self:stretch!important;align-self:start!important;text-align:left!important;}
.topbar .brand-slogan>span:last-child{grid-column:3!important;grid-row:2!important;justify-self:stretch!important;align-self:start!important;text-align:right!important;}
.topbar .brand-slogan>span{display:block!important;width:100%!important;min-width:0!important;margin:0!important;padding:0!important;color:#fff!important;font-size:clamp(7.4px,2.05vw,11px)!important;font-weight:850!important;letter-spacing:0!important;line-height:1.22!important;white-space:normal!important;overflow-wrap:anywhere!important;text-wrap:pretty!important;}
.topbar .brand h1,.topbar .brand-slogan,.topbar .brand-slogan span{color:#fff!important;}
.topbar .brand-copy>#top-status{display:none!important;}
.topbar .top-meta{display:flex!important;flex-wrap:wrap!important;align-items:center!important;justify-content:center!important;gap:8px 14px!important;width:100%!important;min-width:0!important;}
.topbar .count-pill{font-size:10px!important;padding:3px 7px!important;white-space:nowrap!important;flex:0 0 auto!important;margin-left:auto!important;}
#main-tabs .tab[data-tab="dict"] .tab-main{display:flex!important;align-items:center!important;gap:7px!important;width:100%!important;min-width:0!important;}
#main-tabs .tab[data-tab="dict"] .tab-label{flex:1 1 auto!important;min-width:0!important;}
#main-tabs .tab[data-tab="dict"] .count-pill{margin-left:auto!important;font-size:10px!important;line-height:1.25!important;padding:3px 6px!important;white-space:nowrap!important;border-radius:999px!important;}
@media(max-width:600px){
 .topbar .toprow{gap:5px!important;}
 .topbar .brand{grid-template-columns:minmax(0,1fr) minmax(0,1.65fr) minmax(0,1fr)!important;gap:4px 5px!important;}
 .topbar .brand>.brand-flag:first-child,.topbar .brand>.brand-flag:last-child{width:clamp(34px,10vw,46px)!important;padding:2px!important;border-radius:5px!important;}
 .topbar .brand-copy>h1{font-size:clamp(14px,4.3vw,19px)!important;letter-spacing:0!important;}
 .topbar .brand-slogan>span{font-size:clamp(7.2px,2.05vw,8.8px)!important;line-height:1.2!important;}
 .topbar .top-meta{gap:5px 8px!important;}
 #main-tabs .tab[data-tab="dict"] .tab-main{gap:4px!important;}
 #main-tabs .tab[data-tab="dict"] .count-pill{font-size:8px!important;padding:2px 4px!important;}
}
@media(max-width:350px){
 .topbar .brand-copy>h1{font-size:13px!important;}
 .topbar .brand-slogan>span{font-size:7px!important;}
}
</style>
"""
if '</head>' not in html: raise SystemExit('Missing head close.')
html=html.replace('</head>',style+'\n</head>',1)
html=html.replace('</body>','<script id="bvt-dictionary-count-placement">(function(){const count=document.getElementById("count-pill");const tab=document.querySelector("#main-tabs .tab[data-tab=\\"dict\\"] .tab-main");if(count&&tab&&!tab.contains(count))tab.appendChild(count);})();</script>\n<!-- BVT_FLAGS_AND_SPLIT_SLOGANS_V3 -->\n</body>',1)
p.write_text(html,encoding='utf-8')
print('Header v3: centered title between flags; split slogans below each flag; white text; count moved beside dictionary label.')
