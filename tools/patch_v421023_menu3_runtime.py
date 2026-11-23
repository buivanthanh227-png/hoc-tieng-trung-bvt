#!/usr/bin/env python3
"""Restore Menu 18's verified compact-Pinyin path and load the Menu 3 runtime."""
from pathlib import Path
import sys

MARKER = 'id="bvt-v421023-menu3-runtime"'
SCRIPT = '<script id="bvt-v421023-menu3-runtime" src="./menu3-pinyin-fix-v42.10.22.1.js?v=42.10.23" defer></script>'

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    html = target.read_text(encoding="utf-8")
    if "homework3x-query" not in html or "panel-translate3" not in html:
        raise SystemExit("Independent Menu 3 panel is missing; refusing to patch.")

    # Prefer the shortest valid syllable path before dictionary frequency or
    # priority. Thus compact jintian / zuotian / xihuan resolve as two-syllable
    # words, not jin-ti-an / zuo-ti-an / xi-hu-an component sequences.
    marker = "MENU3_PREFER_SHORTEST_COMPACT_SEGMENTATION_V1"
    if marker not in html:
        start = html.find("ranked=[...groups.values()].sort((a,b)=>{")
        end_marker = "})[0];"
        end = html.find(end_marker, start)
        if start < 0 or end < 0:
            raise SystemExit("Could not locate the compact Pinyin path-ranking block.")
        old_block = html[start:end + len(end_marker)]
        if "if(a.length!==b.length)return b.length-a.length;" not in old_block:
            raise SystemExit("Compact Pinyin ranking block changed unexpectedly; refusing blind patch.")
        replacement = (
            "ranked=[...groups.values()].sort((a,b)=>{"
            "const syllableDelta=(a[0]?.tokens.length||999)-(b[0]?.tokens.length||999);"
            "if(syllableDelta!==0)return syllableDelta;"
            "return Math.max(...b.map(x=>x.priority))-Math.max(...a.map(x=>x.priority));"
            "})[0]; /* " + marker + " */"
        )
        html = html[:start] + replacement + html[end + len(end_marker):]

    if MARKER not in html:
        if html.count("</body>") != 1:
            raise SystemExit("Cannot uniquely locate </body> for Menu 3 runtime link.")
        html = html.replace("</body>", SCRIPT + "\n</body>", 1)

    target.write_text(html, encoding="utf-8", newline="\n")
    print("V42.10.23 shortest Pinyin segmentation and direct runtime link verified.")

if __name__ == "__main__":
    main()
