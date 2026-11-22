#!/usr/bin/env python3
"""Regression checks for original flags and slogans in a balanced brand header."""
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit('Usage: test_brand_header.py <site/index.html>')
h=Path(sys.argv[1]).read_text(encoding='utf-8')
required=[
 'id="bvt-responsive-brand-banner"',
 'BVT_FLAGS_ABOVE_TWO_SLOGANS_V2',
 '.topbar .brand{display:grid!important',
 '.topbar .brand>.brand-flag',
 '.topbar .brand-copy>h1',
 '.topbar .brand-copy>.brand-slogan{grid-column:1/-1;grid-row:2',
 'HỌC THÊM MỘT NGÔN NGỮ',
 'SỐNG THÊM MỘT CUỘC ĐỜI',
]
for x in required:
 if x not in h: raise SystemExit('Brand header marker missing: '+x)
if h.count('class="brand-flag"')!=2: raise SystemExit('Expected exactly the two original flag elements.')
if h.count('class="brand-slogan"')!=1: raise SystemExit('Expected exactly one original two-line slogan element.')
if 'bvt-brand-banner' in h or 'bvt-brand-flag' in h: raise SystemExit('Legacy duplicate banner/flag overlay remains.')
print('Original two flags retained; two slogans positioned beneath them; no duplicate banner: PASS')
