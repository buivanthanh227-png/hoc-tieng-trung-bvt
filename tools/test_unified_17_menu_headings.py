#!/usr/bin/env python3
"""Regression checks for all 17 right-side menu headings."""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: test_unified_17_menu_headings.py <site/index.html>")
html = Path(sys.argv[1]).read_text(encoding="utf-8")
tabs = re.findall(r'<button\\b[^>]*class="[^"]*\\btab\\b[^"]*"[^>]*data-tab="([^"]+)"', html)
if len(tabs) != 17:
    tabs = re.findall(r'<button\\b(?=[^>]*class="[^"]*\\btab\\b)(?=[^>]*data-tab="[^"]+")[^>]*>', html)
if len(tabs) != 17:
    raise SystemExit(f"Expected 17 menu buttons; found {len(tabs)}.")
headings = re.findall(r'<h[1-6]\\b[^>]*class="[^"]*\\bsection-title\\b[^"]*"[^>]*data-function-number="[^"]+"[^>]*>', html)
if len(headings) < 17:
    raise SystemExit(f"Expected at least 17 numbered headings; found {len(headings)}.")
for marker in [
    'id="bvt-unified-17-menu-headings-v2"',
    'font-size: 18px !important',
    'font-size: 16px !important',
    'font-family: -apple-system, BlinkMacSystemFont',
    'id="bvt-unified-17-menu-headings-runtime-v2"',
    'BVT_FUNCTION_COLORS[key]',
    "heading.style.setProperty('color',accent,'important')",
    "node.style.setProperty('color','inherit','important')",
    "event.target.closest('#main-tabs .tab')",
]:
    if marker not in html:
        raise SystemExit("Missing unified heading regression marker: " + marker)
if 'id="bvt-unified-17-menu-headings-v1"' in html:
    raise SystemExit("Old v1 heading override must not remain.")
print(f"Unified 17-menu heading regression PASS: {len(tabs)} menus, {len(headings)} numbered headings.")
