# QA-FIX-RECOMMENDATIONS — HỌC TIẾNG TRUNG BVT

**Phiên bản:** V42.9.3
**Ngày:** 18/11/2026
**Nguồn:** QA-BUG-REPORT.md, FIX_REPORT.md (local), QA-TECHNICAL-ANALYSIS.md

---

## 1. Nguyên tắc ưu tiên

1. **Không sửa nhiều lỗi cùng lúc** nếu không cần — mỗi fix phải tách biệt để dễ regression.
2. **Ưu tiên các fix đã có sẵn trong source V42.9.3** (đã load được live) để giảm rủi ro.
3. **Mỗi fix phải kèm test case re-run** từ QA-TEST-CASES.xlsx.

---

## 2. Danh sách đề xuất sửa

### 2.1. Cần sửa ngay (P1 / release-blocking)

#### FIX-01 — BUG-13: Bổ sung icon PWA vào bản deploy

| Hạng mục | Nội dung |
|---|---|
| Bug | BUG-13 |
| Mức ưu tiên | **P1 – cần sửa ngay** |
| File cần sửa | `manifest.webmanifest`, `sw.js`, thêm file `icon-v41-192.png`, `icon-v41-512.png`, `apple-touch-icon-v41.png` |
| Logic sửa | - Thêm 3 file icon vào gốc repo / gốc deploy.<br>- Giữ `icon.svg` làm fallback.<br>- Cập nhật `CACHE_NAME` trong `sw.js` (ví dụ `hoc-trung-app-shell-v43-...`). |
| Ước tính | Rất nhỏ |
| Rủi ro sửa | Thấp–Trung (PWA install); cần re-test SW cache. |
| Test sau sửa | TC-015, smoke cài PWA. |

#### FIX-02 — BUG-11: Sửa trọng số tìm kiếm tiếng Việt

| Hạng mục | Nội dung |
|---|---|
| Bug | BUG-11 |
| Mức ưu tiên | **P1 – nên sửa trước release** |
| File cần sửa | `index.html` (`searchScoreForRow`, bộ lọc tìm kiếm) |
| Logic sửa | - Thêm tầng xếp hạng nghĩa tiếng Việt cho query chứa chữ Việt có dấu.<br>- Yêu cầu boundary cho query ngắn.<br>- Demote pinyin-match khi query là tiếng Việt. |
| Ước tính | Trung |
| Rủi ro sửa | Trung (ảnh hưởng picker, dictionary, sentence generator). |
| Test sau sửa | TC-024, TC-025, TC-027, TC-028, TC-040. |

### 2.2. Nên sửa tiếp (P2)

#### FIX-03 — Re-verify và hoàn thiện BUG-04…BUG-09 (đã có code fix trên V42.9.3)

| Bug | Nội dung | Trạng thái | Hành động |
|---|---|---|---|
| BUG-04 | Mic error rò rỉ sang menu 5/6/7 | Fix có (`clearReadAsrStatus`) | Re-run TC-197 + chuyển menu. |
| BUG-05 | Stale result sau "Đổi câu hỏi" | Fix có (`resetPracticeFeedback`) | Re-run TC-077/086. |
| BUG-06 | Submit rỗng không phản hồi | Fix có | Re-run TC-078/087. |
| BUG-07 | Menu 10 stale stop/start | Fix có | Re-run TC-117. |
| BUG-08 | Transcript mic sau deny | Fix có | Re-run TC-066. |
| BUG-09 | Speaker đọc placeholder | Fix có (`speak` guard) | Re-run TC-068/161. |
| BUG-10 | Invalid file silent | Fix chưa có | Tính sau. |
| BUG-12 | Sentence gloss `你好` → `Bạn tốt.` | Fix chưa có | Tính sau. |

#### FIX-04 — Thêm hộp thoại / trạng thái người dùng cho các lỗi dịch

| Hạng mục | Nội dung |
|---|---|
| Mức ưu tiên | P2 |
| Mô tả | Khi dịch offline/online fallback, nếu kết quả không hợp lý cần thông báo rõ cho người dùng. |

### 2.3. Có thể sửa sau (P3/P4)

| Bug | Nội dung | Lý do defer |
|---|---|---|
| BUG-14 | Touch target 17×17 px | Polished, chưa ảnh hưởng chức năng. |
| BUG-15 | A11y contrast/label | Cần Lighthouse re-run sau khi sửa. |
| BUG-16 | Menu 15 copy confirmation | UX polish. |
| BUG-17 | Menu 4 empty play enabled | UX polish. |
| Performance | Document ~13MB, DCL ~4s | Cần tối ưu sau khi fix hết lỗi. |

---

## 3. Thứ tự khuyến nghị theo độ ưu tiên

| STT | Việc cần làm | Mức ưu tiên | Độ rủi ro | Thứ tự |
|---:|---|---:|---:|---:|
| 1 | FIX-01: deploy đầy đủ icon PWA (BUG-13) | P1 | Thấp–Trung | **1** |
| 2 | FIX-02: sửa ranking tìm kiếm tiếng Việt (BUG-11) | P1 | Trung | **2** |
| 3 | Re-verify BUG-04…BUG-09 bằng regression test case mới | P2 | Thấp–Trung | **3** |
| 4 | Thêm hộp thoại lỗi dịch (P2) | P2 | Thấp | **4** |
| 5 | Fix BUG-10, BUG-12 (P2) | P2 | Thấp | **5** |
| 6 | Fix BUG-14…BUG-17 (P2/P3) | P3 | Thấp | **6** |
| 7 | Tối ưu performance (DCL/FCP) | P4 | Cao (regression) | **7** |

---

## 4. Yêu cầu không được thay đổi ngoài phạm vi sửa lỗi

- Không thay đổi dữ liệu từ điển, dữ liệu âm thanh, dữ liệu câu hỏi.
- Không thay đổi cấu trúc thư mục repo.
- Không thay đổi API ngoài (MyMemory, BVT workers, OCR/ASR).
- Không thay đổi phạm vi menu/functionality chưa được xác nhận.
- Không thay đổi PWA cache version quá thường xuyên (phải bump đúng 1 lần mỗi lần thay đổi SW).
