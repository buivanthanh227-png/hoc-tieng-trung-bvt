#!/usr/bin/env python3
"""Static regression checks for the requested 2026-11-23 UI update."""
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit("Usage: test_requested_ui_20261123.py <site/index.html>")
h=Path(sys.argv[1]).read_text(encoding="utf-8")
required=[
 "BVT_REQUESTED_UI_20261123_V1",
 'id="panel-translate3"',
 'id="bvt-menu3-modal-equal-font"',
 '.homework3x-modal-line.is-pinyin .homework3x-modal-value',
 'font-size:22px!important',
 'id="bvt-banner-footer-layout-v1"',
 'white-space:nowrap!important',
 'font-size:clamp(19px,5.4vw,42px)!important',
 'id="bvt-footer-meta-move-v1"',
 'id="bvt-menu1-colored-actions-v1"',
 'data-dict-tone="1"',
 'data-dict-tone="5"',
]
for marker in required:
 if marker not in h: raise SystemExit("Missing requested UI marker: "+marker)
for marker in ['id="panel-translate-experimental"','data-tab="translate-experimental"']:
 if marker in h: raise SystemExit("Retired Menu 18 UI remains: "+marker)
if h.count('class="brand-flag"')!=2: raise SystemExit("Banner must retain exactly two flags.")
print("Requested UI static regression checks: PASS")
