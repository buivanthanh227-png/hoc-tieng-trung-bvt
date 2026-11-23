#!/usr/bin/env python3
"""Regression tests for V2 banner/footer and embedded dictionary integrity."""
from pathlib import Path
import json,sys,subprocess,tempfile
if len(sys.argv)!=2: raise SystemExit("Usage: test_requested_ui_20261123_v2.py <site/index.html>")
h=Path(sys.argv[1]).read_text(encoding="utf-8")
required=[
 "BVT_REQUESTED_UI_20261123_V2",
 'id="bvt-banner-footer-layout-v2"',
 'grid-column:1!important;grid-row:2!important',
 '.topbar .brand-copy>h1{',
 'grid-column:2!important;grid-row:1!important',
 '.topbar .brand-copy>.brand-slogan{display:contents!important}',
 'width:auto!important',
 'max-width:48%!important',
 'box-sizing:border-box!important',
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
 "#dict-status:not([hidden]){display:block!important",
 "function mergeRows(rows){const out=Array.isArray(rows)?rows:[];",
 "window.dictionary=dictionary;",

 "out[write++]=raw",
 "parsed=null;setDictionary(rows,'CVDICT Trung–Việt nhúng sẵn')",
 "init().catch(error=>",
 "setDictionary(buildSeed(),'Bộ từ cơ bản dự phòng')",

 "window.__menu1DictionaryLoaded(dictionary.length,'bộ từ cơ bản dự phòng')",
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

# Execute the exact production mergeRows helper and verify it reuses the parsed
# array instead of cloning every 122k row into a second large array.
start=h.index("function mergeRows(rows){")
end=h.index("function makeSearchRecord",start)
merge_js=h[start:end].strip()
runtime_test=r"""
const assert=require('node:assert/strict');
function keyPinyin(s){return String(s||'').toLowerCase();}
function hskFromSeed(){return '';}
function buildSeed(){return [['你','你','nǐ','you','HSK1'],['好','好','hǎo','good','HSK1']];}
"""+merge_js+r"""
const rows=[['你','你','nǐ','you',''],['学','學','xué','study','']];
const same=mergeRows(rows);
assert.strictEqual(same,rows,'mergeRows must reuse the parsed source array');
assert.equal(same.length,3,'duplicate seed should be skipped and missing seed appended');
assert.equal(same.filter(r=>r[0]==='你').length,1,'duplicate row must be removed');
assert.ok(same.some(r=>r[0]==='好'),'missing curated seed must be added');
console.log('Menu 1 in-place dictionary merge runtime test: PASS');
"""
with tempfile.NamedTemporaryFile("w",suffix=".cjs",encoding="utf-8",delete=False) as f:
 f.write(runtime_test); runtime_path=f.name
subprocess.run(["node","--check",runtime_path],check=True)
subprocess.run(["node",runtime_path],check=True)

if h.count('class="brand-flag"')!=2: raise SystemExit("Expected exactly two flag cards")
if '--bvt-slogan-offset:' in h: raise SystemExit("Legacy offset-based slogan positioning remains")
if '.topbar .brand .brand-slogan{\n display:flex!important' in h: raise SystemExit("Slogans must be grid children, not a flex container")
print(f"V2 regression checks PASS: {len(rows):,} embedded dictionary entries.")
