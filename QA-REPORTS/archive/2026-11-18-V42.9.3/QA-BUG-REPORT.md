# QA-BUG-REPORT — HỌC TIẾNG TRUNG BVT

**Ứng dụng:** HỌC TIẾNG TRUNG BVT
**Deploy URL:** https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/
**Phiên bản kiểm thử:** **V42.9.3** (18/11/2026)
**Phiên bản trước đó:** V42.9.2 (16/11/2026) — kết quả: NOT ACCEPTED
**Ngày giờ:** 18/11/2026
**Nguyên tắc:** Chỉ ghi nhận lỗi đã thực thi và xác nhận; không tự sửa code.

---

## 1. Tổng quan lỗi trong phiên V42.9.3

| Nhóm | Số lượng | ID |
|---|---:|---|
| Lỗi đã sửa và xác nhận đã FIXED trong V42.9.3 | 3 | BUG-01, BUG-02, BUG-03 |
| Lỗi còn đang mở (đã xác nhận FAIL trên V42.9.3) | 2 | BUG-11, BUG-13 |
| Lỗi đã sửa trong source V42.9.3 (hàm tồn tại trên live) nhưng cần re-verify case mới | 6 | BUG-04…BUG-09 |
| Tổng lỗi mới phát hiện trong phiên V42.9.3 | **2** | — |

**Nhận định:** Phiên V42.9.3 đã giải quyết gói lỗi dịch ngôn ngữ P0 (BUG-01, BUG-02, BUG-03). Hai lỗi P1 còn lại
(BUG-11, BUG-13) chưa được vá và vẫn đang ảnh hưởng đến sản phẩm. Không có lỗi mới P0 xuất hiện trong phiên kiểm thử này.

---

## 2. Chi tiết lỗi

### BUG-13 — PWA manifest icon thiếu / 404 (MỚI CẬN ĐÃ XÁC NHẬN LẦN TRỐNG — CÒN MỚI TRONG V42.9.3)

| Trường | Nội dung |
|---|---|
| Mã lỗi | BUG-13 |
| Tên lỗi | PWA install icons không tồn tại trên GitHub Pages → HTTP 404 |
| Mức độ | **P1 – HIGH** |
| Phiên bản | V42.9.3 (còn FAIL) / V42.9.2 (còn FAIL) |
| Menu / module | PWA (menu chung, ngoài nav) |
| Chức năng liên quan | Cài đặt / Add to Home Screen / Service Worker cache |
| Điều kiện xảy ra | Mở trang, đọc `manifest.webmanifest`, fetch icon |
| Các bước tái hiện | 1. Mở `https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/`<br>2. Đọc `manifest.webmanifest`<br>3. Fetch `icon-v41-192.png`, `icon-v41-512.png`, `apple-touch-icon-v41.png` |
| Kết quả mong đợi | HTTP 200, `image/png` |
| Kết quả thực tế | HTTP **404** (text/html); `icon.svg` → 200. Gây 4 console error + 4 network error |
| Bằng chứng | `QA-EXECUTIVE-SUMMARY.md` §3.2; console log trong phiên V42.9.3 |
| Tên file liên quan | `manifest.webmanifest`, `sw.js`, `index.html` (PWA) |
| Nguyên nhân gốc rễ | Bản vá local V42.9.3 đã thêm file icon vào thư mục patch, nhưng bản **deploy** lên GitHub Pages chưa chứa đủ 3 file PNG; cache SW đã bump nhưng asset list thiếu. |
| Phương án sửa | 1. Thêm `icon-v41-192.png`, `icon-v41-512.png`, `apple-touch-icon-v41.png` vào gốc repo deploy.<br>2. Hoặc đổi manifest về `icon.svg` (type image/svg+xml, sizes any) + thêm icon maskable hợp lệ.<br>3. Cập nhật `sw.js` `APP_FILES` và bump `CACHE_NAME`. |
| Rủi ro khi sửa | Thấp–Trung: ảnh hưởng PWA install cho người dùng; cần re-test cache/SW. |
| Test case sau sửa | TC-015 (PWA icons), smoke cài đặt PWA. |
| Độ chắc chắn | **Cao** — xác nhận bằng fetch + console + source (manifest trỏ đúng path PNG). |

---

### BUG-11 — Tìm kiếm tiếng Việt trả kết quả theo pinyin thay vì nghĩa từ (CÒN MỚI TRONG V42.9.3)

| Trường | Nội dung |
|---|---|
| Mã lỗi | BUG-11 |
| Tên lỗi | Dictionary search `cá` ra top kết quả là pinyin `cā/cǎ…` (嚓, 擦, 礤, 鮆, 鱎, 菜) — thiếu kết quả nghĩa "cá"/cá |
| Mức độ | **P1 – HIGH** (tìm kiếm là entry point chính của app) |
| Phiên bản | V42.9.3 (còn FAIL) / V42.9.2 (còn FAIL) |
| Menu | 1 – TỪ ĐIỂN TIẾNG TRUNG |
| Chức năng | Tìm kiếm từ vựng |
| Điều kiện | Gõ `cá` vào ô tìm kiếm từ điển |
| Các bước tái hiện | 1. Mở menu 1<br>2. Gõ `cá` vào `#dict-search`<br>3. Đọc top kết quả |
| Kết quả mong đợi | Kết quả nghĩa tiếng Việt (`cá` → 鱼/cá) đứng đầu; hoặc ít nhất không bị chiếm top bởi pinyin. |
| Kết quả thực tế | Top 8: 嚓 (cā), 擦 (cā), 礤 (cǎ), 鮆 (jì/cá), 鱎, 菜 (cài) — **鱼 không nằm ở đầu danh sách**. |
| Bằng chứng | Screenshot `QA/screenshots/d01_dict.png`; log TC-027 |
| Tên file liên quan | `index.html` (`searchScoreForRow`) |
| Nguyên nhân gốc rễ | `searchScoreForRow()` ưu tiên equality pinyin, không tách tầng xếp hạng theo nghĩa tiếng Việt; query tiếng Việt ngắn (`cá` → `ca`) gây nhiễu. |
| Phương án sửa | 1. Thêm tầng xếp hạng "nghĩa tiếng Việt trùng/ gần" trên các query chứa dấu tiếng Việt.<br>2. Yêu cầu word-boundary cho query 1–2 ký tự.<br>3. Demote pinyin-match khi query chứa chữ Việt có dấu. |
| Rủi ro khi sửa | Trung – ảnh hưởng picker từ vựng, sentence generator, memory. Cần re-test TC-024–TC-029. |
| Test case sau sửa | TC-027, TC-028, TC-040. |
| Độ chắc chắn | **Cao** — xác nhận bằng live test + source. |

---

### BUG-01 — `再见` dịch ra chuỗi vô nghĩa (ĐÃ SỬA TRONG V42.9.3)

| Trường | Nội dung |
|---|---|
| Mã lỗi | BUG-01 |
| Tên lỗi | Từ điển offline/MyMemory trả nghĩa sai cho từ đơn (`再见` → "Chà Tở") |
| Mức độ | **P0 – CRITICAL** (người học bắt đầu) |
| Phiên bản | V42.9.2: FAIL → V42.9.3: **FIXED** (xác nhận live) |
| Menu | 3 – Dịch nhanh Việt ⇄ Trung |
| Kết quả thực tế (V42.9.2) | Pinyin `Zài jiàn` đúng; nghĩa `Chà Tở` sai. |
| Kết quả thực tế (V42.9.3) | ✅ Pinyin `Zài jiàn`, nghĩa `Tạm biệt`; status `Đã tìm được câu mẫu offline.` |
| Nguyên nhân gốc rễ | `machineTranslate()` gọi MyMemory trước khi có curated/dictionary lookup; thiếu override offline cho từ đơn. |
| Phương án sửa | Dùng curated `CURATED_ZH_VI` + exact dictionary trước; MT chỉ fallback. |
| Trạng thái hiện tại | **FIXED** — cần theo dõi lại sau deploy. |

---

### BUG-02 — `你好` / `nǐ hǎo` trả kết quả câu hỏi sai (ĐÃ SỬA TRONG V42.9.3)

| Trường | Nội dung |
|---|---|
| Mã lỗi | BUG-02 |
| Tên lỗi | Từ vựng `你好` bị map sang câu mẫu gần (`你好吗?`) |
| Mức độ | **P0 – CRITICAL** |
| Phiên bản | V42.9.2: FAIL → V42.9.3: **FIXED** (xác nhận live) |
| Kết quả thực tế (V42.9.2) | `你好` → `你好吗? / Bạn khỏe không?` |
| Kết quả thực tế (V42.9.3) | ✅ `你好` → Pinyin `Nǐ hǎo`, nghĩa `Xin chào`; `nǐ hǎo` → `Xin chào` |
| Nguyên nhân gốc rễ | Near-match `includes()` ưu tiên câu dài; `queryIsPinyin` chặn ký tự dấu Latin. |
| Phương án sửa | Exact-first lookup + rank fuzzy + chuẩn hoá pinyin có dấu. |
| Trạng thái hiện tại | **FIXED** — xác nhận live trên V42.9.3. |

---

### BUG-03 — Input Việt + Trung sinh pinyin garbled (ĐÃ SỬA TRONG V42.9.3)

| Trường | Nội dung |
|---|---|
| Mã lỗi | BUG-03 |
| Tên lỗi | Pinyin cho `Xin chào 你好` thành `X i n c h à o nǐ hǎo` |
| Mức độ | **P1 – HIGH** |
| Phiên bản | V42.9.2: FAIL → V42.9.3: **FIXED** (xác nhận live) |
| Kết quả thực tế (V42.9.3) | ✅ Pinyin `Xin chào nǐ hǎo` |
| Trạng thái hiện tại | **FIXED** — xác nhận live trên V42.9.3. |

---

## 3. Lỗi cùng nhóm đã vá trong source V42.9.3 — trạng thái re-verify

| Bug | Nội dung | Hàm fix trên live | Kết quả re-verify |
|---|---|---|---|
| BUG-04 | Mic error rò rỉ sang menu 5/6/7 | `clearReadAsrStatus` | ✅ Hàm tồn tại; state sau chuyển menu sạch |
| BUG-05 | Kết quả cũ sau "Đổi câu hỏi" | `resetPracticeFeedback` | ✅ Hàm tồn tại; `#practice-result` ẩn |
| BUG-06 | Submit rỗng không phản hồi | (fix trong handler) | ⏳ Chưa chạy full flow |
| BUG-07 | Menu 10 stale stop/start | (fix trong handler) | ⏳ Chưa chạy full flow |
| BUG-08 | Transcript sau mic deny giữ "Đang chờ bạn nói…" | (fix trong handler) | ⏳ Chưa chạy full flow |
| BUG-09 | Speaker đọc placeholder khi chưa có kết quả | `speak` guard | ✅ Guard tồn tại (`if(!value)…return null`) |

**Kết luận nhóm này:** Source fix đã được deploy cùng V42.9.3. Việc hành vi đầy đủ (đặc biệt BUG-06, BUG-07, BUG-08)
cần regression test case mới ở phiên sau.

---

## 4. Lỗi cũ đã có và trạng thái qua các phiên

| Bug | Nội dung | Phiên 16/11 | Phiên 18/11 | Ghi chú |
|---|---|---|---:|---|
| BUG-01 | `再见` → "Chà Tở" | FAIL (P0) | **FIXED** | ✅ Xác nhận live V42.9.3 |
| BUG-02 | `你好` → `你好吗?` | FAIL (P0) | **FIXED** | ✅ Xác nhận live V42.9.3 |
| BUG-03 | Mixed pinyin garbled | FAIL (P1) | **FIXED** | ✅ Xác nhận live V42.9.3 |
| BUG-04 | Mic rò rỉ sang menu 5/6/7 | FAIL (P1) | ⏳ Cần re-verify | Fix có trên live |
| BUG-05 | Stale result sau đổi câu | FAIL (P1) | ⏳ Cần re-verify | Fix có trên live |
| BUG-06 | Submit rỗng | FAIL (P1) | ⏳ Cần re-verify | Fix có trên live |
| BUG-07 | Vocab stop/start stale | FAIL (P1) | ⏳ Cần re-verify | Fix có trên live |
| BUG-08 | Mic deny transcript | FAIL (P1) | ⏳ Cần re-verify | Fix có trên live |
| BUG-09 | Empty speaker | FAIL (P2) | ⏳ Cần re-verify | Fix có trên live |
| BUG-10 | Invalid file silent | FAIL (P2) | ⏳ Chưa re-verify | Không nằm trong fix V42.9.3 |
| BUG-11 | Dict `cá` ranking | FAIL (P1) | **FAIL** | ❌ Không sửa |
| BUG-12 | Sentence gloss `你好` → `Bạn tốt.` | FAIL (P2) | ⏳ Chưa re-verify | Không nằm trong fix V42.9.3 |
| BUG-13 | PWA icons 404 | FAIL (P1) | **FAIL** | ❌ Không sửa (thiếu file trong deploy) |
| BUG-14 | Touch target 17×17 | FAIL (P2) | ⏳ Chưa re-verify | Không nằm trong fix |
| BUG-15 | A11y contrast/label | FAIL (P2) | ⏳ Chưa re-verify | Không nằm trong fix |
| BUG-16 | Menu 15 copy confirmation | FAIL (P2) | ⏳ Chưa re-verify | Không nằm trong fix |
| BUG-17 | Menu 4 empty play enabled | FAIL (P2) | ⏳ Chưa re-verify | Không nằm trong fix |

---

## 5. Lỗi mới phát hiện trong phiên V42.9.3 (nếu có)

| Bug | Nội dung | Mức độ | Trạng thái |
|---|---|---:|---|
| — | Không có lỗi P0 mới. Các lỗi P1/P2 còn lại đã nằm trong phiên V42.9.2. | — | — |

**Ghi chú:** Không tìm thấy lỗi JS runtime mới trong phiên này; console error chỉ gắn với icon 404.

---

## 6. Tổng hợp theo mức độ (phiên V42.9.3)

| Mức độ | Số lỗi | ID |
|---|---:|---|
| P0 CRITICAL | 0 | — |
| P1 HIGH | 2 | BUG-11, BUG-13 |
| P2 MEDIUM | 0 mới (các lỗi P2 cũ đang chờ re-verify) | BUG-10, BUG-12, BUG-14…BUG-17 |
| P3 LOW | 0 | — |
| P4 COSMETIC | 0 | — |

---

## 7. Kết luận tổng thể

- Build V42.9.3 **đã khắc phục được 3 lỗi P0 dịch ngôn ngữ** và xác nhận qua test thực thi live.
- Còn **2 lỗi P1 chưa được khắc phục** trên bản deploy hiện tại: **BUG-13** (PWA icons 404) và **BUG-11** (tìm kiếm tiếng Việt sai thứ bậc).
- Không có lỗi nào mới nghiêm trọng hơn mức P1 trong phiên kiểm thử V42.9.3.
- Độ chấp nhận: **CHƯA QUYẾT ĐỊNH** cho release; cần fix BUG-13 + BUG-11 trước khi re-accept.

---

## 8. Disclaimer

- Mọi kết quả dựa trên bản deploy thực tế đang chạy tại thời điểm kiểm thử.
- Một số luồng (mic, TTS, device thật, offline) không thể kiểm thử được trong môi trường này → ghi rõ BLOCKED.
- Không tự sửa code, không commit/push/deploy trong phiên kiểm thử.
