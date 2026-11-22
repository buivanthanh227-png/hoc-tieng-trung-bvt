#!/usr/bin/env python3
"""Place the two original slogans beneath the two original flags in a balanced header."""
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit('Usage: patch_brand_header.py <site/index.html>')
p=Path(sys.argv[1]); html=p.read_text(encoding='utf-8')
if 'BVT_FLAGS_ABOVE_TWO_SLOGANS_V2' in html: raise SystemExit('Brand header v2 already applied.')
if 'class="topbar"' not in html or 'class="brand-flag"' not in html or 'class="brand-slogan"' not in html:
    raise SystemExit('Cannot locate original brand, flag and slogan elements.')
style=r'''<style id="bvt-responsive-brand-banner">
/* Keep the original two flags and title; put both slogan lines below the flags. */
.topbar .toprow{display:flex;align-items:center;justify-content:space-between;gap:clamp(10px,2vw,26px);width:100%;}
.topbar .brand{display:grid!important;grid-template-columns:minmax(56px,1fr) minmax(0,2.2fr) minmax(56px,1fr);grid-template-rows:auto auto;align-items:center;justify-items:center;column-gap:clamp(8px,2vw,24px);row-gap:clamp(5px,1vw,10px);width:min(100%,1000px);min-width:0;margin-inline:auto;}
.topbar .brand>.brand-flag{grid-row:1;justify-self:center;align-self:center;width:clamp(48px,7vw,86px);height:auto;aspect-ratio:3/2;display:grid;place-items:center;overflow:hidden;border-radius:7px;box-shadow:0 2px 8px rgba(0,0,0,.18);}
.topbar .brand>.brand-flag svg{display:block;width:100%;height:100%;}
.topbar .brand>.brand-copy{display:contents;}
.topbar .brand-copy>h1{grid-column:2;grid-row:1;align-self:center;justify-self:center;margin:0!important;max-width:100%;font-size:clamp(22px,4vw,48px)!important;line-height:1.08!important;text-align:center!important;white-space:normal!important;text-wrap:balance;}
.topbar .brand-copy>.brand-slogan{grid-column:1/-1;grid-row:2;display:grid!important;grid-template-columns:1fr;gap:3px;width:100%;margin:0!important;padding:0!important;text-align:center!important;line-height:1.25!important;}
.topbar .brand-slogan>span{display:block!important;width:100%;font-size:clamp(10px,1.35vw,15px)!important;font-weight:800;letter-spacing:.035em;text-align:center!important;text-wrap:balance;}
.topbar .brand-copy>#top-status{display:none!important;}
@media(max-width:600px){.topbar .toprow{gap:5px}.topbar .brand{grid-template-columns:minmax(42px,.8fr) minmax(0,2fr) minmax(42px,.8fr);column-gap:5px;row-gap:5px;width:100%}.topbar .brand>.brand-flag{width:clamp(40px,12vw,58px);border-radius:5px}.topbar .brand-copy>h1{font-size:clamp(18px,5.2vw,27px)!important;letter-spacing:0!important}.topbar .brand-copy>.brand-slogan{gap:2px}.topbar .brand-slogan>span{font-size:clamp(8px,2.45vw,11px)!important;letter-spacing:0;line-height:1.2!important}}
@media(min-width:601px) and (max-width:900px){.topbar .brand{grid-template-columns:minmax(48px,1fr) minmax(0,2fr) minmax(48px,1fr);column-gap:9px}.topbar .brand-copy>h1{font-size:clamp(25px,4.3vw,38px)!important}}
</style>
'''
html=html.replace('</head>',style+'\n</head>',1)
html=html.replace('</body>','<!-- BVT_FLAGS_ABOVE_TWO_SLOGANS_V2 -->\n</body>',1)
p.write_text(html,encoding='utf-8')
print('Brand header aligned: original flags remain; both slogan lines are placed beneath them.')
