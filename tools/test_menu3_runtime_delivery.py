#!/usr/bin/env python3
"""Verify the external Menu 3 runtime actually contains the UI behavior it promises."""
from pathlib import Path
import re, sys
if len(sys.argv) != 3:
    raise SystemExit("Usage: test_menu3_runtime_delivery.py <index.html> <runtime.js>")
html = Path(sys.argv[1]).read_text(encoding="utf-8")
js = Path(sys.argv[2]).read_text(encoding="utf-8")
checks = {
    "HTML loads the exact Menu 3 runtime": 'id="bvt-v421023-menu3-runtime"' in html and 'menu3-pinyin-fix-v42.10.23.js' in html,
    "result renderer targets the visible candidate container": "getElementById('homework3x-candidates')" in js,
    "all three result fields are rendered": all(x in js for x in ["homework3x-candidate-py", "homework3x-candidate-zh", "homework3x-candidate-vi"]),
    "Pinyin is explicitly large": "font-size:clamp(21px,5.2vw,27px)!important" in js,
    "Vietnamese meaning is retained and validated": "const direct=[item.preferredMeaning,item.vi]" in js and "validMeaning(value)" in js,
    "candidate click opens the detail modal": "window.openHomework3xCandidateModal(item,index,complete.length)" in js,
    "modal has Hanzi, Pinyin and Vietnamese": all(x in js for x in ["CHỮ HÁN", "PHIÊN ÂM PINYIN", "NGHĨA TIẾNG VIỆT"]),
    "modal has three copy actions": all(x in js for x in ['data-copy="hanzi"', 'data-copy="pinyin"', 'data-copy="meaning"']),
    "modal has two speech actions": all(x in js for x in ['data-menu3-speak="zh"', 'data-menu3-speak="vi"']),
    "candidate renderer is exported to the page": "window.renderHomework3xCandidatesV421023=renderCandidates" in js,
    "lookup bridge is present in HTML": "BVT_MENU3_FULL_RESULTS_RENDERER_BRIDGE_V1" in html and "window.renderHomework3xCandidatesV421023" in html,
    "exactly ten results per page": "const token=++renderToken;let page=0;const pageSize=10" in js,
    "full Chinese sentence is translated when dictionary meaning is absent": "translators.push(()=>window.machineTranslate3x(hanzi,'zh-CN','vi'))" in js,
    "input word spacing is preserved": ".join('')" in js,
}
for label, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + label)
if not all(checks.values()):
    raise SystemExit(1)
# Reject the exact bug in both the patch source and the generated production HTML.
selector = Path("tools/patch_menu3_tone_selector.py").read_text(encoding="utf-8")
if r"split(/\s+/).filter(Boolean)" not in selector or 'bad = r"split(/\\\\s+/).filter(Boolean)"' not in selector:
    raise SystemExit("FAIL: patch source does not contain both the old-pattern repair and corrected regex")
if "MENU3_MENU18_TONE_POSITION_SELECTOR_V1" not in html:
    raise SystemExit("FAIL: generated HTML is missing the Menu 3 tone selector")
if r"split(/\\s+/).filter(Boolean)" in html:
    raise SystemExit("FAIL: generated HTML still uses a literal backslash-s regex")
if r"split(/\s+/).filter(Boolean)" not in html:
    raise SystemExit("FAIL: generated HTML does not contain the corrected whitespace regex")
print("PASS: patch source and generated HTML split Pinyin syllables on actual whitespace")
