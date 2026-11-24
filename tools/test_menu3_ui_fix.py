#!/usr/bin/env python3
"""Regression checks for Menu 3 palette and user-triggered lookup."""
from pathlib import Path
import re,sys
if len(sys.argv)!=2: raise SystemExit('Usage: test_menu3_ui_fix.py <site/index.html>')
h=Path(sys.argv[1]).read_text(encoding='utf-8')
required=[
 'MENU3_UI_COLOR_AND_LOOKUP_FIX_V1',
 '.tab[data-tab="translate3"]{--menu-color:#0891b2}',
 '#panel-translate3{--red:#0891b2;--red2:#0e7490}',
 "BVT_FUNCTION_COLORS.translate3={main:'#0891b2',alt:'#0e7490'};",
 'id="menu3-independent-lookup-binding"',
 "button.addEventListener('click',()=>{lookupHomework3x();});",
 "input.addEventListener('keydown',event=>{if(event.key==='Enter')",
 "button.dataset.menu3LookupBound='1'",
 "input.dataset.menu3EnterBound='1'",
 'async function lookupHomework3x()',
 '.homework3x-modal-backdrop .homework3x-modal-line .homework3x-modal-value',
 'font-size:22px!important;font-weight:800!important;line-height:1.45!important;',
 'bvt-v42121-final-layout',
 'repeat(4,minmax(0,1fr))',
 'homework3x-candidate-grid',
 'width:clamp(50px,7vw,78px)!important',
 'window.renderHomework3xCandidatesV421023',
 'function getPinyin18SourceIndex()',
 'function pinyin18CanSegment(value,syllables)',
]
for x in required:
 if x not in h: raise SystemExit('Menu 3 UI fix marker missing: '+x)
matcher_start=h.index('function pinyinToChineseCandidates(raw){')
matcher_end=h.index('async function machineTranslate(',matcher_start)
matcher=h[matcher_start:matcher_end]
if 'index.bySyllables.get(rawTokens.map(pinyin18Key).join(\' \'))' not in matcher:
 raise SystemExit('Menu 3 Pinyin lookup must match complete source syllable sequences.')
if 'index.byCompact.get(inputKey)' not in matcher:
 raise SystemExit('Menu 3 compact Pinyin lookup must match complete source readings.')
if 'machineTranslate' in matcher or re.search(r'beam|Math\.min\s*\(\s*128|\.slice\s*\(\s*0\s*,\s*128',matcher,re.I):
 raise SystemExit('Menu 3 Pinyin matcher must not compose translations or truncate matches with a beam cap.')
color_block=h[h.index('<style id="menu3-independent-color">'):h.index('</style>',h.index('<style id="menu3-independent-color">'))]
if '#BA68C8' in color_block or '#864B90' in color_block: raise SystemExit('Purple Menu 18 color override remains in Menu 3.')
if h.count("button.addEventListener('click',()=>{lookupHomework3x();});")!=1: raise SystemExit('Menu 3 lookup click handler missing or duplicated.')
print('Menu 3 palette consistency and click/Enter lookup bindings: PASS')
