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
    # For compact Pinyin, choose the shortest valid syllable path before
    # comparing dictionary frequency/priority. This blocks jin-ti-an and
    # xi-hu-an when jin-tian / xi-huan are complete two-syllable words.
    marker = "MENU3_PREFER_SHORTEST_COMPACT_SEGMENTATION_V1"
    if marker not in html:
        import re
        pattern = re.compile(
            r"ranked=\\[\\.\\.\\.groups\\.values\\(\\)\\]\\.sort\\(\\(a,b\\)=>\\{"
            r"\\s*if\\(a\\.length!==b\\.length\\)return b\\.length-a\\.length;"
            r"\\s*return Math\\.max\\(\\.\\.\\.b\\.map\\(x=>x\\.priority\\)\\)-"
            r"Math\\.max\\(\\.\\.\\.a\\.map\\(x=>x\\.priority\\)\\);"
            r"\\s*\\}\\)\\[0\\];"
        )
        replacement = (
            "ranked=[...groups.values()].sort((a,b)=>{"
            "const syllableDelta=(a[0]?.tokens.length||999)-(b[0]?.tokens.length||999);"
            "if(syllableDelta!==0)return syllableDelta;"
            "return Math.max(...b.map(x=>x.priority))-Math.max(...a.map(x=>x.priority));"
            "})[0]; /* " + marker + " */"
        )
        html, count = pattern.subn(replacement, html, count=1)
        if count != 1:
            raise SystemExit("Could not uniquely patch compact Pinyin segmentation ranking.")
    html = html.replace("</body>", SCRIPT + "\n</body>", 1)
    target.write_text(html, encoding="utf-8", newline="\n")
    print("V42.10.23 shortest Pinyin segmentation and runtime link applied.")

if __name__ == "__main__":
    main()
