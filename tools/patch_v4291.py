#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

BROKEN = """if(!text){result.textContent='Bản dịch sẽ hiển thị tại đây.';result.dataset.bvtTranslationReady='false';const recordingActive=prefix==='bvt-mv'&&typeof bvtMvRecorder!=='undefined'&&bvtMvRecorder?.state==='recording';if(status)status.textContent=recordingActive?'Đang ghi âm… chạm lại để kết thúc.':'Sẵn sàng.';return;
 const source=$(prefix+'-source')?.value||'auto',target=$(prefix+'-target')?.value||'vi';"""
FIXED = """if(!text){result.textContent='Bản dịch sẽ hiển thị tại đây.';result.dataset.bvtTranslationReady='false';const recordingActive=prefix==='bvt-mv'&&typeof bvtMvRecorder!=='undefined'&&bvtMvRecorder?.state==='recording';if(status)status.textContent=recordingActive?'Đang ghi âm… chạm lại để kết thúc.':'Sẵn sàng.';return;}
 const source=$(prefix+'-source')?.value||'auto',target=$(prefix+'-target')?.value||'vi';"""

html = INDEX.read_text(encoding="utf-8")
if html.count(BROKEN) == 1:
    html = html.replace(BROKEN, FIXED, 1)
    INDEX.write_text(html, encoding="utf-8")
    print("Fixed missing closing brace in bvtMlRunTranslation.")
elif html.count(FIXED) == 1:
    print("The translation branch already has its closing brace.")
else:
    raise SystemExit("Could not match the exact translation branch safely.")

class InlineScripts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.active = False
        self.attrs = {}
        self.parts = []
        self.items = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "script":
            self.active = True
            self.attrs = dict(attrs)
            self.parts = []

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.active:
            kind = (self.attrs.get("type") or "").lower()
            if not self.attrs.get("src") and kind not in (
                "text/plain", "application/json", "application/ld+json", "importmap"
            ):
                self.items.append((self.attrs.get("id") or "inline", "".join(self.parts)))
            self.active = False

parser = InlineScripts()
parser.feed(INDEX.read_text(encoding="utf-8"))
if not parser.items:
    raise SystemExit("No inline JavaScript found to validate.")

with tempfile.TemporaryDirectory() as tmp:
    for number, (name, code) in enumerate(parser.items):
        target = Path(tmp) / f"inline-{number}.js"
        target.write_text(code, encoding="utf-8")
        result = subprocess.run(
            ["node", "--check", str(target)],
            capture_output=True,
            text=True
        )
        if result.returncode:
            print(f"JavaScript syntax error in inline script [{name}]:")
            print(result.stderr)
            raise SystemExit(result.returncode)

print(f"PASS: all {len(parser.items)} inline JavaScript blocks passed node --check.")
