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
    "Vietnamese meaning is retained and validated": "item.preferredMeaning||item.vi||''" in js and "validMeaning(vi)" in js,
    "candidate click opens the detail modal": "window.openHomework3xCandidateModal(item,index,source.length)" in js,
    "modal has Hanzi, Pinyin and Vietnamese": all(x in js for x in ["CHỮ HÁN", "PHIÊN ÂM PINYIN", "NGHĨA TIẾNG VIỆT"]),
    "modal has three copy actions": all(x in js for x in ['data-copy="hanzi"', 'data-copy="pinyin"', 'data-copy="meaning"']),
    "modal has two speech actions": all(x in js for x in ['data-speak="zh"', 'data-speak="vi"']),
    "candidate renderer is exported to the page": "window.renderHomework3xCandidates=renderCandidates" in js,
}
for label, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + label)
if not all(checks.values()):
    raise SystemExit(1)
# Reject the exact bug: a regex matching a literal backslash-s instead of whitespace.
selector = Path("tools/patch_menu3_tone_selector.py").read_text(encoding="utf-8")
if r"split(/\\s+/)" in selector:
    raise SystemExit("FAIL: selector still uses an escaped literal backslash-s regex")
if r"split(/\s+/)" not in selector:
    raise SystemExit("FAIL: selector whitespace tokenization expression is missing")
print("PASS: selector splits Pinyin syllables on actual whitespace")
