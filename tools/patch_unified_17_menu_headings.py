#!/usr/bin/env python3
"""Unify right-side headings across the 17 navigation menus."""
from pathlib import Path
import re
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
html = path.read_text(encoding="utf-8")
marker = '<style id="bvt-unified-17-menu-headings-v1">'
if marker in html:
    if html.count(marker) != 1:
        raise SystemExit("Unified menu-heading style marker is duplicated.")
    print("Unified 17-menu heading style already present; no change.")
    raise SystemExit(0)

tabs = re.findall(r'<button\\b[^>]*class="[^"]*\\btab\\b[^"]*"[^>]*data-tab="([^"]+)"', html)
if len(tabs) != 17:
    # Attribute order is not guaranteed; count the canonical tab elements instead.
    tabs = re.findall(r'<button\\b(?=[^>]*class="[^"]*\\btab\\b)(?=[^>]*data-tab="[^"]+")[^>]*>', html)
if len(tabs) != 17:
    raise SystemExit(f"Expected exactly 17 navigation menu buttons; found {len(tabs)}.")

required = [
    "BVT_FUNCTION_COLORS",
    "function bvtSyncFunctionHeading",
    "function switchTab(tab)",
    "data-function-number",
]
missing = [token for token in required if token not in html]
if missing:
    raise SystemExit("Cannot verify existing heading/color architecture: " + ", ".join(missing))

style = """<style id="bvt-unified-17-menu-headings-v1">
/* A single typography rule for all right-side headings.
   switchTab() assigns --red from the selected menu's existing banner palette. */
.panel .section-title[data-function-number] {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", sans-serif !important;
  font-size: clamp(16px, 2.1vw, 18px) !important;
  font-weight: 850 !important;
  line-height: 1.3 !important;
  letter-spacing: 0 !important;
  color: var(--red) !important;
  max-width: 100% !important;
  overflow-wrap: break-word !important;
  word-break: normal !important;
  text-wrap: pretty;
}
.panel.active .section-title[data-function-number] {
  color: var(--red) !important;
}
.panel .section-title[data-function-number] .function-title-icon {
  font: inherit !important;
  line-height: inherit !important;
}
@media (max-width: 600px) {
  .panel .section-title[data-function-number] {
    font-size: 16px !important;
    line-height: 1.3 !important;
  }
}
</style>
"""
if html.count("</head>") != 1:
    raise SystemExit("Cannot uniquely locate the document head closing tag.")
html = html.replace("</head>", style + "\\n</head>", 1)
if html.count(marker) != 1:
    raise SystemExit("Failed to insert exactly one unified heading style.")
if "color: var(--red) !important;" not in html:
    raise SystemExit("Active banner accent color binding was not inserted.")
path.write_text(html, encoding="utf-8")
print("Unified typography inserted; all 17 menu buttons and active banner accent binding verified.")
