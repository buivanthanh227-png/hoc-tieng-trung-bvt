#!/usr/bin/env python3
"""Static regression checks for the responsive brand header overlay."""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: test_brand_header.py <site/index.html>")
html = Path(sys.argv[1]).read_text(encoding="utf-8")
required = [
    'id="bvt-responsive-brand-banner"',
    'bvt-brand-banner',
    "HỌC TIẾNG TRUNG",
    "HỌC THÊM MỘT NGÔN NGỮ",
    "SỐNG THÊM MỘT CUỘC ĐỜI",
    "left.append(leftText);center.append(title);right.append(rightText);",
    "@media(min-width:601px) and (max-width:1099px)",
    "@media(max-width:600px)",
    "color:#fff!important",
]
for marker in required:
    if marker not in html:
        raise SystemExit(f"Responsive brand banner marker missing: {marker}")
script_start=html.index('<script id="bvt-responsive-brand-banner-script">')
script_end=html.index('</script>', script_start)
script=html[script_start:script_end]
if "🇻🇳" in script or "🇨🇳" in script or "bvt-brand-flag" in html:
    raise SystemExit("Brand overlay still injects duplicate flag elements.")
print("Responsive brand banner checks passed; original header flags are preserved without duplicate overlay flags.")
