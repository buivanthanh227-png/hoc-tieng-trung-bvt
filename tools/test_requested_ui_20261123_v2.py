#!/usr/bin/env python3
"""Regression tests for V2 banner/footer and embedded dictionary integrity."""
from pathlib import Path
import json,sys
if len(sys.argv)!=2: raise SystemExit("Usage: test_requested_ui_20261123_v2.py <site/index.html>")
h=Path(sys.argv[1]).read_text(encoding="utf-8")
required=[
 "BVT_REQUESTED_UI_20261123_V2",
 'id="bvt-banner-footer-layout-v2"',
 'grid-column:1!important;grid-row:2!important',
 'grid-column:3!important;grid-row:2!important',
 'color:#111!important',
 'color:#dc2626!important',
 'max-width:100%!important',
 'text-align:left!important',
 'text-align:right!important',
 'id="bvt-footer-meta-move-v2"',
 "querySelector('.credit-line')",
 "getElementById('bvt-header-clock')",
 'bvt-footer-version-row-v2',
 "window.__menu1DictionaryLoaded=function(count,sourceName)",
 "window.__menu1DictionaryLoadedCount",
 "$('dict-status').hidden=false;",
 'id="embedded-cvdict-data"',
]
for marker in required:
 if marker not in h: raise SystemExit("Missing V2 regression marker: "+marker)
start=h.index('id="embedded-cvdict-data"')
tag_end=h.index(">",start)
end=h.index("</script>",tag_end)
rows=json.loads(h[tag_end+1:end])
if len(rows)<120000: raise SystemExit(f"Embedded dictionary has only {len(rows)} rows")
if len([x for x in rows if isinstance(x,list) and len(x)>=4])<120000:
 raise SystemExit("Embedded dictionary contains malformed rows")
if 'BVT_REQUESTED_UI_20261123_V1' not in h:
 raise SystemExit("V1 baseline UI patch unexpectedly missing")
if h.count('class="brand-flag"')!=2: raise SystemExit("Expected exactly two flag cards")
print(f"V2 regression checks PASS: {len(rows):,} embedded dictionary entries.")
