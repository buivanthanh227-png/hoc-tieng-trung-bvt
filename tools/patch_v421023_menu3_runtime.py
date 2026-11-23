#!/usr/bin/env python3
"""Ensure the verified Menu 3 runtime is loaded directly by the app document."""
from pathlib import Path
import sys

MARKER = 'id="bvt-v421023-menu3-runtime"'
SCRIPT = '<script id="bvt-v421023-menu3-runtime" src="./menu3-pinyin-fix-v42.10.22.1.js?v=42.10.23" defer></script>'

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    html = target.read_text(encoding="utf-8")
    if MARKER in html:
        print("V42.10.23 Menu 3 runtime already linked.")
        return
    if html.count("</body>") != 1:
        raise SystemExit("Cannot uniquely locate </body> for Menu 3 runtime link.")
    if "homework3x-query" not in html or "panel-translate3" not in html:
        raise SystemExit("Independent Menu 3 panel is missing; refusing to link runtime.")
    html = html.replace("</body>", SCRIPT + "\n</body>", 1)
    target.write_text(html, encoding="utf-8", newline="\n")
    print("V42.10.23 Menu 3 runtime linked directly in index.html.")

if __name__ == "__main__":
    main()
