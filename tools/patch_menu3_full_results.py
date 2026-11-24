#!/usr/bin/env python3
"""Route Menu 3's actual lookup pipeline to the complete, paginated result renderer."""
from pathlib import Path
import sys

MARKER = "BVT_MENU3_FULL_RESULTS_RENDERER_BRIDGE_V1"
if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_menu3_full_results.py <index.html>")
target = Path(sys.argv[1])
html = target.read_text(encoding="utf-8")

start_token = "async function renderHomework3xCandidates(candidates){"
end_token = "function looksLikeVietnamese3x(raw){"
start = html.find(start_token)
end = html.find(end_token, start + len(start_token))
if start < 0 or end < 0:
    raise SystemExit("Cannot locate the original Menu 3 result renderer boundaries.")

bridge = """/* BVT_MENU3_FULL_RESULTS_RENDERER_BRIDGE_V1 */
async function renderHomework3xCandidates(candidates){
 const renderer=window.renderHomework3xCandidatesV421023;
 const host=document.getElementById('homework3x-candidates');
 const status=document.getElementById('homework3x-status');
 if(typeof renderer!=='function'){
  if(host){host.replaceChildren();host.hidden=true;}
  if(status)status.textContent='Bộ hiển thị kết quả Menu 3 chưa tải xong. Vui lòng tải lại trang.';
  return null;
 }
 return await renderer(candidates);
}
"""
existing = html[max(0, start - 80):end]
if MARKER in existing:
    if "window.renderHomework3xCandidatesV421023" not in html[start:end]:
        raise SystemExit("Menu 3 renderer bridge marker exists but is malformed.")
    print("Menu 3 full-result renderer bridge already installed.")
else:
    html = html[:start] + bridge + html[end:]
    target.write_text(html, encoding="utf-8", newline="\n")
    print("Menu 3 lookup now delegates to the full-result renderer.")

# Ensure the live lookup function calls the bridged renderer, not a stale inline renderer.
lookup_start = html.find("async function lookupHomework3x(){")
if lookup_start < 0:
    raise SystemExit("Menu 3 lookup function not found.")
if "renderHomework3xCandidates(" not in html[lookup_start:]:
    raise SystemExit("Menu 3 lookup does not call the candidate renderer.")
