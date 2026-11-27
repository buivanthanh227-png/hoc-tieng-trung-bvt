#!/usr/bin/env python3
"""Load the dedicated V42.10.23 Menu 3 runtime directly in the app document."""
from pathlib import Path
import re
import sys

MARKER = 'id="bvt-v421023-menu3-runtime"'
SCRIPT = '<script id="bvt-v421023-menu3-runtime" src="./menu3-pinyin-fix-v42.10.23.js?v=42.10.23-racefix-20261127" defer></script>'

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    html = target.read_text(encoding="utf-8")
    if "homework3x-query" not in html or "panel-translate3" not in html:
        raise SystemExit("Independent Menu 3 panel is missing; refusing to patch.")
    # Keep Menu 3's own panel heading separate from the Menu 16 and 17 titles.
    panel_start = html.find('<section id="panel-translate3"')
    panel_end = html.find('<section id="panel-practice"', panel_start + 1)
    if panel_start < 0 or panel_end < 0:
        raise SystemExit("Could not uniquely locate the Menu 3 panel boundaries.")
    panel = html[panel_start:panel_end]
    heading_pattern = re.compile(
        r'(<h2\b[^>]*data-function-number="3"[^>]*>)(.*?)(</h2>)',
        flags=re.I | re.S,
    )
    heading_matches = list(heading_pattern.finditer(panel))
    allowed_titles = {
        "DỊCH NHANH VIỆT ⇄ TRUNG",
        "DỊCH NHANH VIỆT ⇄ TRUNG, LUYỆN NGHE PHIÊN ÂM TIẾNG TRUNG và THỬ THÁCH NHỚ MẶT CHỮ HÁN",
    }
    if len(heading_matches) != 1 or heading_matches[0].group(2).strip() not in allowed_titles:
        raise SystemExit("Menu 3 heading is unexpected; refusing to overwrite it.")
    panel, heading_count = heading_pattern.subn(
        lambda match: match.group(1) + "DỊCH NHANH VIỆT ⇄ TRUNG" + match.group(3),
        panel,
        count=1,
    )
    if heading_count != 1:
        raise SystemExit("Could not uniquely normalize the Menu 3 heading.")
    html = html[:panel_start] + panel + html[panel_end:]
    if MARKER in html:
        html, count = re.subn(
            r'<script\b(?=[^>]*\bid="bvt-v421023-menu3-runtime")[^>]*></script>',
            SCRIPT,
            html,
            count=1,
            flags=re.I
        )
        if count != 1:
            raise SystemExit("Could not uniquely update the existing Menu 3 runtime script tag.")
    else:
        if html.count("</body>") != 1:
            raise SystemExit("Cannot uniquely locate </body> for Menu 3 runtime link.")
        html = html.replace("</body>", SCRIPT + "\n</body>", 1)
    target.write_text(html, encoding="utf-8", newline="\n")
    print("V42.10.23 Menu 3 runtime linked directly in index.html.")

if __name__ == "__main__":
    main()
