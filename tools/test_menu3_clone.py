#!/usr/bin/env python3
"""Regression checks for the independent Menu 3 clone."""
from pathlib import Path
import re,sys
if len(sys.argv)!=2: raise SystemExit("Usage: test_menu3_clone.py <site/index.html>")
html=Path(sys.argv[1]).read_text(encoding="utf-8")
required=[
 "MENU3_INDEPENDENT_COPY_OF_MENU18_V1",
 '<button class="tab" data-tab="translate3"',
 '<section id="panel-translate3"',
 'data-function-number="3"',
 'DỊCH NHANH VIỆT ⇄ TRUNG',
 'id="homework3x-query"',
 'id="homework3x-lookup"',
 'id="homework3x-status"',
 'id="homework3x-candidates"',
 'id="homework3x-results"',
 'function renderHomework3xCard(',
 'async function renderHomework3xCandidates(candidates)',
 'async function lookupHomework3x()',
 'BVT_MENU3_FULL_RESULTS_RENDERER_BRIDGE_V1',
 'data-homework3x-speak="zh"',
 'data-homework3x-speak="vi"',
 'function looksLikePinyin3x(',
 'runLongTranslation3x',
 'runFileTranslation3x',
 'id="long-translate-3x-input"',
 'id="translate-file-3x-input"',
 'id="panel-practice"',
 'homework3x-output-row',
 'homework3x-modal-backdrop',
 'homework3x-modal-line',
 'homework3x-candidate-tab',
 'homework3x-candidate',
]
for marker in required:
 if marker not in html: raise SystemExit("Independent Menu 3 marker missing: "+marker)
nav=html[html.index('<nav id="main-tabs"'):html.index('</nav>',html.index('<nav id="main-tabs"'))]
if nav.index('data-tab="translate3"') > nav.index('data-tab="voice-translate"'):
 raise SystemExit("New Menu 3 is not in the third position.")
if 'THỬ NGHIỆM' in nav or '(THỬ NGHIỆM)' in html:
 raise SystemExit("Experimental label remains in the navigation/panel.")
if 'data-homework18-speak="py"' in html or 'const playPinyinWords=async()=>{' in html:
 raise SystemExit("Pinyin playback must be absent from both Menu 3 and Menu 18.")
logic_start=html.index('<script id="menu3-independent-lookup-logic">')
logic_end=html.index('</script>',logic_start)
logic=html[logic_start:logic_end]
if 'data-homework18-' in logic or re.search(r"\$\('homework18-",logic) or re.search(r"\bhomework18[A-Za-z0-9_]+",logic):
 raise SystemExit("New Menu 3 lookup logic shares Menu 18 IDs or state.")
if "homework3xLookupToken" not in logic or "homework3xCandidates" not in logic:
 raise SystemExit("New Menu 3 lookup state is not independently namespaced.")
# All HTML IDs must be unique after cloning.
ids=re.findall(r'\bid="([^"]+)"',html)
duplicates=sorted({x for x in ids if ids.count(x)>1})
if duplicates: raise SystemExit("Duplicate HTML IDs after cloning: "+", ".join(duplicates[:20]))
print("Independent Menu 3 clone, navigation order, separate IDs/state and no Pinyin playback: PASS")
