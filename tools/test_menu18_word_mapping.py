#!/usr/bin/env python3
"""Verify that retired Menu 18 is absent and Menu 3 owns the sentence mapper."""
from pathlib import Path
import json
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: test_menu18_word_mapping.py <site/index.html>")

html = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(r'<script id="embedded-cvdict-data"[^>]*>(.*?)</script>', html, re.S)
if not match:
    raise SystemExit("Embedded CVDICT dataset not found")
dictionary = json.loads(match.group(1))
if len(dictionary) < 120_000:
    raise SystemExit(f"Unexpectedly small CVDICT dataset: {len(dictionary)}")

retired_markers = (
    'data-tab="translate-experimental"',
    'id="panel-translate-experimental"',
    'THỬ NGHIỆM',
    'id="homework18-query"',
)
for marker in retired_markers:
    if marker in html:
        raise SystemExit("Retired Menu 18 or experimental label remains: " + marker)

menu3_markers = (
    '<section id="panel-translate3"',
    'id="homework3x-query"',
    'async function lookupHomework3x()',
    'async function renderHomework3xCandidates(candidates)',
    'homework3x-candidate',
    'homework3x-modal-backdrop',
    'data-homework3x-speak="zh"',
    'data-homework3x-speak="vi"',
)
for marker in menu3_markers:
    if marker not in html:
        raise SystemExit("Independent Menu 3 component missing: " + marker)

print("Retired Menu 18 absent; Menu 3 keeps independent CVDICT sentence mapping: PASS")
