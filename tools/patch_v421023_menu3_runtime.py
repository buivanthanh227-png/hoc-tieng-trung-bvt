#!/usr/bin/env python3
"""Load the dedicated V42.10.23 Menu 3 runtime directly in the app document."""
from pathlib import Path
import re
import sys

MARKER = 'id="bvt-v421023-menu3-runtime"'
SCRIPT = '<script id="bvt-v421023-menu3-runtime" src="./menu3-pinyin-fix-v42.10.23.js?v=42.10.23" defer></script>'

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    html = target.read_text(encoding="utf-8")
    if "homework3x-query" not in html or "panel-translate3" not in html:
        raise SystemExit("Independent Menu 3 panel is missing; refusing to patch.")
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
