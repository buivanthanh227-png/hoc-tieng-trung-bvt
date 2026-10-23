#!/usr/bin/env python3
"""Build the GitHub Pages site by embedding the upstream CVDICT source in HTML."""
from __future__ import annotations
import hashlib
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site"
SLOT = "<!-- EMBEDDED_CVDICT_DATA_SLOT -->"
ENTRY_RE = re.compile(r"^\S+\s+\S+\s+\[[^\]]+\]\s+/(.+)/\s*(?:#.*)?$")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/build_site.py /path/to/CVDICT.u8", file=sys.stderr)
        return 2
    data_path = Path(sys.argv[1])
    if not data_path.is_file():
        print(f"Không tìm thấy dữ liệu từ điển: {data_path}", file=sys.stderr)
        return 2
    data = data_path.read_text(encoding="utf-8-sig")
    entries = sum(1 for line in data.splitlines() if ENTRY_RE.match(line))
    if entries < 120_000:
        print(f"TỪ CHỐI XUẤT BẢN: chỉ xác nhận được {entries:,} dòng từ hợp lệ; cần ít nhất 120.000.", file=sys.stderr)
        return 1
    if re.search(r"</\s*script", data, flags=re.IGNORECASE):
        print("TỪ CHỐI XUẤT BẢN: dữ liệu chứa chuỗi có thể đóng thẻ script HTML.", file=sys.stderr)
        return 1

    template_path = ROOT / "index.html"
    html = template_path.read_text(encoding="utf-8")
    if html.count(SLOT) != 1:
        print("Không tìm thấy đúng một vị trí nhúng dữ liệu trong index.html.", file=sys.stderr)
        return 1

    digest = hashlib.sha256(data.encode("utf-8")).hexdigest()[:20]
    embedded = (
        f'<script id="embedded-cvdict-data" type="text/plain" data-version="{digest}">\n'
        + data
        + '\n</script>'
    )
    built_html = html.replace(SLOT, embedded, 1)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "index.html").write_text(built_html, encoding="utf-8")
    for name in ("manifest.webmanifest", "icon.svg", "sw.js"):
        src = ROOT / name
        if not src.is_file():
            print(f"Thiếu tệp PWA bắt buộc: {name}", file=sys.stderr)
            return 1
        shutil.copy2(src, OUT / name)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Đã xác nhận {entries:,} dòng CVDICT hợp lệ.")
    print(f"Phiên bản dữ liệu SHA-256: {digest}")
    print(f"Đã tạo {OUT / 'index.html'} ({(OUT / 'index.html').stat().st_size / 1024 / 1024:.2f} MiB).")
    print("Từ điển được nhúng trực tiếp trong index.html được xuất bản; không cần tải CVDICT từ nguồn ngoài khi mở ứng dụng.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
