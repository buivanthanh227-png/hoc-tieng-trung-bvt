#!/usr/bin/env python3
"""Regression tests for Menu 3's complete, paginated Pinyin mapping UI."""
from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit("Usage: test_menu3_full_results.py <index.html> <runtime.js>")
html = Path(sys.argv[1]).read_text(encoding="utf-8")
js = Path(sys.argv[2]).read_text(encoding="utf-8")

checks = {
    "the original lookup renderer delegates to the V42.10.23 runtime":
        "BVT_MENU3_FULL_RESULTS_RENDERER_BRIDGE_V1" in html
        and "window.renderHomework3xCandidatesV421023" in html,
    "the lookup flow still calls the renderer":
        "renderHomework3xCandidates(candidates)" in html,
    "ten results are shown per page":
        "const token=++renderToken;let page=0;const pageSize=10" in js,
    "previous and next page controls exist":
        "data-page-prev" in js and "data-page-next" in js,
    "each card shows Pinyin, Hanzi and Vietnamese meaning":
        all(x in js for x in ["homework3x-candidate-py", "homework3x-candidate-zh", "homework3x-candidate-vi"]),
    "Pinyin remains visually prominent":
        "font-size:clamp(21px,5.2vw,27px)!important" in js,
    "Pinyin grouping preserves user token boundaries and formats tones from source syllables":
        "const sourceGroup=syllables.slice(at,at+selected.length)" in js
        and "groups.push(menu3FormatWord(match[0],sourceGroup.join('')))" in js,
    "original separators and punctuation are copied from the user's input":
        "source.slice(previous.index+previous[0].length,current.index)" in js
        and "source.slice(last.index+last[0].length)" in js,
    "the user's original letter case is not changed":
        "return output;" in js and "ch.toUpperCase()" not in js,
    "missing Vietnamese glosses are translated from the complete Hanzi sentence":
        "window.machineTranslate3x(String(item.zh),'zh-CN','vi')" in js,
    "meaning quality gate rejects dictionary metadata, not full sentence meanings":
        "validMeaning(translated)" in js and "phương ngữ miền bắc" in js,
    "touching a result opens the detail modal":
        "window.openHomework3xCandidateModal(item,index,complete.length)" in js,
    "detail modal provides three copy controls and two speech controls":
        all(x in js for x in ['data-copy="hanzi"', 'data-copy="pinyin"', 'data-copy="meaning"', 'data-speak="zh"', 'data-speak="vi"']),
    "old instruction to tap merely to translate is absent":
        "Chọn để dịch nghĩa" not in js,
}
failed = False
for label, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + label)
    failed |= not ok
if failed:
    raise SystemExit(1)
print("Menu 3 full-result UI regression: PASS")
