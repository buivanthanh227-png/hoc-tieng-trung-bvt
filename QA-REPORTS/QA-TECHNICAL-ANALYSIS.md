# QA-TECHNICAL-ANALYSIS — HỌC TIẾNG TRUNG BVT

**Phiên bản:** V42.9.3
**Ngày:** 18/11/2026

---

## 1. Kiến trúc ứng dụng

| Thành phần | Mô tả |
|---|---|
| Kiểu ứng dụng | Static SPA (single-page) + 1 iframe (menu 11) |
| Hosting | GitHub Pages (`buivanthanh227-png.github.io/hoc-tieng-trung-bvt/`) |
| Front-end | `index.html` chứa inline CSS + JS (đoạn lớn), CSS/JS tách qua CDN một số thư viện |
| Workers | ASR, OCR, ASR-cloudflare (JS riêng) |
| Storage | localStorage (prefs), IndexedDB (library), Cache Storage (app shell + audio), Service Worker |
| External | MyMemory, BVT workers, Tesseract.js, HanziWriter, pinyin-pro, audio-cmn (jsDelivr) |

### 1.1. Các module chính (dữ liệu / logic)

| Module | Vai trò |
|---|---|
| `CURATED_ZH_VI` | Bộ từ điển tiếng Việt→Trung được curated cho các từ đơn. |
| `tryLocalTranslation(raw)` | Resolver dịch offline: curated → offline key → sentence deck → near-match. |
| `queryIsPinyin(raw)` | Xác định query là pinyin có dấu hay không. |
| `pinyinToChinese(raw)` / `pinyinForChinese(text)` | Chuyển pinyin ↔ chữ Hán; sinh pinyin từ text. |
| `machineTranslate(text, source, target)` | Dịch qua MyMemory / BVT ML. |
| `resetPracticeFeedback()` | Reset trạng thái feedback sau khi đổi câu hỏi. |
| `clearReadAsrStatus()` | Xóa/reset trạng thái mic. |
| `speak(text, button, onFinished)` | Phát TTS; có guard cho giá trị rỗng. |
| `renderHomeworkCard(...)` | Render kết quả dịch nhanh. |
| `translateLongText(...)` | Dịch đoạn văn. |

---

## 2. Các module liên quan đến lỗi đã sửa

| Bug | Module liên quan | Hàm/đoạn code | Fix đã có trong V42.9.3 |
|---|---|---|---|
| BUG-01 | Dịch từ đơn | `machineTranslate`, `CURATED_ZH_VI`, `lookupHomework` | ✅ curated trước MT |
| BUG-02 | Dịch từ vựng | `tryLocalTranslation`, `queryIsPinyin` | ✅ exact-first + pinyin normalize |
| BUG-03 | Pinyin mixed | `pinyinForChinese` | ✅ segment Hanzi/Latin |
| BUG-04 | Mic | `switchTab`, `clearReadAsrStatus` | ✅ reset khi chuyển tab |
| BUG-05 | Practice | `nextPractice`, `resetPracticeFeedback` | ✅ reset feedback |
| BUG-06 | Submit | `handleSubmit` | ✅ clear/toast/focus |
| BUG-07 | Vocab | `startVocabularyTraining` | ✅ set status |
| BUG-08 | Mic deny | ASR error handler | ✅ reset transcript |
| BUG-09 | Speak | `speak` | ✅ guard `!value` |

---

## 3. Các đoạn code có nguy cơ / rủi ro khi sửa

| Đoạn code | Rủi ro | Hệ quả nếu sửa sai |
|---|---|---|
| `tryLocalTranslation` | Thứ tự ưu tiên (curated → offline → near) | Có thể phá offline translation cho câu dài; regression menu 14/15. |
| `pinyinForChinese` | Hành vi segment | Có thể sinh pinyin sai cho pure-Latin/pure-Hanzi. |
| `resetPracticeFeedback` | Shared panel menus 3/5/6/7/8 | Có thể xóa kết quả hợp lệ. |
| `searchScoreForRow` | Xếp hạng | Có thể đổi thứ tự picker từ vựng. |
| `manifest.webmanifest` + `sw.js` | Cache/SW | Có thể stranded installed client. |

---

## 4. Nguyên nhân gốc rễ (tóm tắt)

| Bug | Nguyên nhân gốc rễ đã xác định |
|---|---|
| BUG-01 | Thiếu curated/offline trước khi gọi MT; MyMemory trả kết quả sai. |
| BUG-02 | Near-match ưu tiên câu con (`你好吗`) trước exact; `queryIsPinyin` chặn ký tự dấu. |
| BUG-03 | `pinyinForChinese` áp dụng lên toàn chuỗi, không phân segment. |
| BUG-11 | `searchScoreForRow` không tách tầng theo nghĩa tiếng Việt. |
| BUG-13 | Thiếu asset trong package deploy; cache/SW không đủ. |

---

## 5. Rủi ro khi sửa (cross-menu impact)

| Fix đang định | Menu ảnh hưởng | Rủi ro |
|---|---|---|
| Translation resolver | M3, M4, M14, M15 | **Cao** — shared. |
| Pinyin segment | M2, M3, M9, M14 | Trung. |
| Practice reset | M3, M5, M6, M7, M8 | **Cao** — shared panel. |
| Dict ranking | M1, M9, M10, M17 | Trung. |
| PWA icon/SW | Toàn app install | Thấp–Trung. |

---

## 6. Điểm cần chú ý để không làm hỏng menu khác

- **Luôn giữ nguyên thứ tự ưu tiên** trong `tryLocalTranslation` khi sửa BUG-11.
- Khi sửa segment pinyin, phải giữ hành vi pure-Hanzi/pure-Latin/punctuation/emoji.
- Khi sửa reset feedback, chỉ reset khi chuyển câu hỏi/new session, không reset sau submit.
- Khi sửa SW cache, phải bump `CACHE_NAME` và cập nhật `APP_FILES`.

---

## 7. Rủi ro toàn cục khi sửa

- Sửa `index.html` (file ~13MB) có thể gây lỗi cú pháp JS nguy hiểm nếu không kiểm tra.
- Thay đổi version trong `index.html` + `manifest.webmanifest` + `sw.js` phải đồng bộ 3 nơi.
- Không tự ý sửa khi chưa có bản vá local và không có re-deploy kế hoạch.
