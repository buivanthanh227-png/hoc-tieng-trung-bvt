#!/usr/bin/env python3
"""Regression checks for the three-column banner and dictionary count placement."""
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit('Usage: test_brand_header.py <site/index.html>')
h=Path(sys.argv[1]).read_text(encoding='utf-8')
required=[
 'id="bvt-responsive-brand-banner"',
 'BVT_FLAGS_AND_SPLIT_SLOGANS_V3',
 '.topbar .brand{display:grid!important',
 '.topbar .brand-copy>h1{grid-column:2!important;grid-row:1!important',
 '.topbar .brand-slogan>span:first-child{grid-column:1!important;grid-row:2!important',
 '.topbar .brand-slogan>span:last-child{grid-column:3!important;grid-row:2!important',
 'color:#fff!important',
 '#panel-dict .section-title .count-pill',
 'id="bvt-dictionary-count-placement"',
 'Tổng số từ vựng: đang nạp…',
 'HỌC THÊM MỘT NGÔN NGỮ',
 'SỐNG THÊM MỘT CUỘC ĐỜI',
 '@media(max-width:600px)',
]
for x in required:
 if x not in h: raise SystemExit('Brand header marker missing: '+x)
if h.count('class="brand-flag"')!=2: raise SystemExit('Expected exactly two original flags.')
if h.count('class="brand-slogan"')!=1: raise SystemExit('Expected one original slogan container.')
if h.count('id="count-pill"')!=1: raise SystemExit('Expected exactly one live dictionary word count.')
heading_start=h.index('<h2 class="section-title" data-function-number="1" style="margin:0">Tra cứu từ vựng')
heading_end=h.index('</h2>',heading_start)
if not (heading_start < h.index('id="count-pill"') < heading_end):
 raise SystemExit('Word count badge is not beside the Menu 1 panel heading.')
if h.index('id="count-pill"') < h.index('<nav id="main-tabs"'):
 raise SystemExit('Word count badge remains in the left navigation/category area.')
if '\\\\n@media' in h or '\\\\n</head>' in h: raise SystemExit('Literal escaped newline corrupted the responsive CSS.')
if 'bvt-brand-banner' in h or 'bvt-brand-flag' in h: raise SystemExit('Duplicate/legacy banner overlay remains.')
print('Centered white title, flags on both sides, left/right slogans below, responsive sizing and dictionary count placement: PASS')
