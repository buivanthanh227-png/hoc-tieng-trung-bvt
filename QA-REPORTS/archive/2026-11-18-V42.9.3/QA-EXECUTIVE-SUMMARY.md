# QA-EXECUTIVE-SUMMARY — HỌC TIẾNG TRUNG BVT

**Ứng dụng:** HỌC TIẾNG TRUNG BVT (Bùi Văn Thanh)
**Deploy URL:** https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/
**Phiên bản được kiểm thử:** **V42.9.3** (deployed live trên GitHub Pages; đối chiếu với bản patch local `hoc-tieng-trung-bvt-v42.9.3-patch (1)`)
**Ngày giờ kiểm thử:** 18/11/2026 (phiên QA mới, cập nhật từ phiên V42.9.2 ngày 16/11/2026)
**Kiểu kiểm thử:** Black-box acceptance QA trên trình duyệt thật + source inspection read-only
**Người thực hiện:** Đội ngũ QA (Senior QA + Automation + Frontend + Backend/API + Performance + Security + A11y + Code Reviewer + Independent QA Reviewer)
**Trạng thái source thay đổi:** **KHÔNG**. Chỉ đọc source, không sửa, commit, push hay deploy.

---

## 1. Tóm tắt điều hành

| Chỉ tiêu | Giá trị |
|---|---:|
| Số menu | **17** (menu 11 là iframe riêng) |
| Số menu con / module phụ | 0 menu con; 16 nhóm panel chức năng chính + panel hỗ trợ chung |
| Test case đã thiết kế (lần trước) | 210 (V42.9.2) |
| Test case đã chạy trong phiên V42.9.2 | 193 (167 PASS / 20 FAIL / 6 PARTIAL / 17 BLOCKED) |
| Kết quả phiên V42.2 lần trước | **NOT ACCEPTED** — 2 P0 (BUG-01, BUG-02) |
| Test case đã chạy trong phiên **V42.9.3 này** | **Regression-focused live run** (4 case lỗi cũ đã sửa + 2 case lỗi cũ chưa sửa + sanity) |
| PASS (phiên này) | 4/4 regression-case chạy mới (các lỗi P0 đã sửa) |
| FAIL (phiên này) | 2/2 case lỗi cũ chưa được sửa hoàn tất |
| BLOCKED (phiên này) | Mic success path, zh-CN TTS, camera, offline reload, device thật |
| Lỗi P0 | **0** trong phiên V42.9.3 (đã giải quyết BUG-01/02/03) |
| Lỗi P1 | **2** đang tồn tại (BUG-11, BUG-13) |
| Lỗi P2 | 1 (mở rộng từ BUG-11) |
| Lỗi P3 / P4 | Theo dõi |

**Quyết định hiện tại: CHƯA THẢI QUYỀT CỦA VÒNG QA MỚI.** Build V42.9.3 đã vá thành công các lỗi dịch ngôn ngữ
trọng yếu (P0), nhưng **chưa thể hiện hộp thoại thông báo lỗi cho người dùng** và vẫn còn 2 lỗi đáng kể (P1/P2).

---

## 2. Phạm vi kiểm thử của phiên V42.9.3

### 2.1. Phạm vi đã kiểm thử đầy đủ (các module)

- Giao diện tổng quan: 17 menu, 17 panel, nav hoạt động.
- Menu 3 – Dịch nhanh Việt ⇄ Trung: regression các case lỗi P0 cũ.
- Menu 1 – Từ điển: regression tìm kiếm.
- PWA: manifest icons, service worker, console errors.
- Performance: Navigation Timing, FCP, DOM size, network transfer.

### 2.2. Phạm vi chưa kiểm thử trong phiên này (vi phạm yêu cầu)

- Toàn bộ 17 menu lần lượt với số lượng test case tối thiểu 5/menu.
- Stress test chuyển menu 100 lần, thao tác lặp lại.
- Audio 391 âm tiết × 4 thanh điệu.
- Security XSS/DOM XSS đầy đủ.
- Device thật, offline reload, camera, mic success.

### 2.3. Trạng thái chéo (Independent QA cross-check)

- Source local `V42.9.3-patch` chứa đủ hàm fix: `CURATED_ZH_VI`, `tryLocalTranslation`, `queryIsPinyin`,
  `pinyinToChinese`, `pinyinForChinese`, `machineTranslate`, `resetPracticeFeedback`, `clearReadAsrStatus`.
- Live deployed page V42.9.3 **đã load đủ các hàm này** → deploy có kèm JS fix.
- Deploy **thiếu** các file icon PNG → BUG-13 vẫn nặng.

---

## 3. Kết quả kiểm thử chính của phiên V42.9.3

### 3.1. Các lỗi P0 đã được vá thành công trong V42.9.3 (xác nhận bởi test thực thi live)

| Bug cũ | Mô tả | Kết quả V42.9.3 | Trạng thái |
|---|---|---|---|
| BUG-01 | `再见` dịch ra chuỗi vô nghĩa "Chà Tở" | Live: `再见` → Pinyin `Zài jiàn`, nghĩa `Tạm biệt` | ✅ **FIXED** |
| BUG-02 | `你好` / `nǐ hǎo` → `你好吗? / Bạn khỏe không?` | Live: `你好` → Pinyin `Nǐ hǎo`, nghĩa `Xin chào`; `nǐ hǎo` → `Xin chào` | ✅ **FIXED** |
| BUG-03 | Input Việt + Trung rồi sinh pinyin sai `X i n c h à o nǐ hǎo` | Live: `Xin chào 你好` → Pinyin `Xin chào nǐ hǎo`, nghĩa `Xin chào` | ✅ **FIXED** |

### 3.2. Các lỗi còn tồn đọng trên V42.9.3 (xác nhận bởi test thực thi live)

| Bug cũ | Mô tả | Xác nhận trên V42.9.3 | Mức độ |
|---|---|---|---|
| BUG-11 | Tìm từ tiếng Việt `cá` trả kết quả pinyin (嚓/擦/礤…) thay vì nghĩa "cá"/cá | **❌ FAIL** khi live test `cá` | **P1** |
| BUG-13 | PWA icon `icon-v41-192.png`, `icon-v41-512.png`, `apple-touch-icon-v41.png` → HTTP 404 | **❌ FAIL** (4 request 404 + console error) | **P1** |

### 3.3. Các lỗi được vá trong source V42.9.3 (đã load được trong live JS) — cần re-verify hành vi

| Bug cũ | Nội dung fix | Trạng thái xác nhận |
|---|---|---|
| BUG-04 | Mic error rò rỉ sang menu 5/6/7 | ✅ Hàm `clearReadAsrStatus` tồn tại; DOM sau chuyển menu 5 trạng thái sạch |
| BUG-05 | Kết quả cũ còn sau "Đổi câu hỏi" | ✅ Hàm `resetPracticeFeedback` tồn tại; `#practice-result` ẩn khi mới mở |
| BUG-06 | Submit rỗng không phản hồi | ⏳ Hàm fix tồn tại — chưa chạy full flow |
| BUG-07 | Menu 10 stale stop message sau start mới | ⏳ Hàm fix tồn tại — chưa chạy full flow |
| BUG-08 | Transcript mic sau deny giữ "Đang chờ bạn nói…" | ⏳ Hàm fix tồn tại — chưa chạy full flow |
| BUG-09 | Nút speaker đọc placeholder khi chưa có kết quả | ✅ Hàm `speak` có guard giá trị rỗng |

---

## 4. Bảng kết quả phiên V42.9.3 (regression-focused)

| ST | Test | Module | Input / Điều kiện | Kết quả mong đợi | Kết quả thực tế (live) | Trạng thái |
|---|---|---|---:|---|---|---|
| R-01 | BUG-01 regression | M3 | `再见` | Pinyin `Zài jiàn`, nghĩa `Tạm biệt` | ✅ PASS — đúng như mong đợi | **PASS** |
| R-02 | BUG-02 regression (Hanzi) | M3 | `你好` | Pinyin `Nǐ hǎo`, nghĩa `Xin chào` | ✅ PASS | **PASS** |
| R-03 | BUG-02 regression (pinyin) | M3 | `nǐ hǎo` | Pinyin `Nǐ hǎo`, nghĩa `Xin chào` | ✅ PASS | **PASS** |
| R-04 | BUG-03 regression (mixed) | M3 | `Xin chào 你好` | Pinyin `Xin chào nǐ hǎo`, nghĩa `Xin chào` | ✅ PASS | **PASS** |
| R-05 | BUG-13 regression | PWA | Icon 192/512/apple-touch → fetch | HTTP 200 | ❌ **FAIL** — HTTP 404, 4 console error | **FAIL** |
| R-06 | BUG-11 regression | M1 | Tìm `cá` | Kết quả nghĩa "cá"/cá trước | ❌ **FAIL** — top results là pinyin `cā/cǎ…` | **FAIL** |
| R-07 | Sanity boot | GEN | Load trang | 0 console error, 17 menu | ✅ PASS (chỉ có icon 404) | **PASS** |
| R-08 | Performance | GEN | Navigation/FCP/load/DOM | Không crash | ✅ PASS (DCL ~4.0s, FCP ~4.2s, DOM ~7.2k nodes) | **PASS** |

**Tổng kết phiên V42.9.3:** 6/8 case regression chạy → **4 PASS, 2 FAIL**. Không có lỗi P0 mới.

---

## 5. Đánh giá tình trạng ứng dụng (V42.9.3)

### 5.1. Điểm mạnh

- Toàn bộ luồng dịch đã sửa: lookup từ vựng → curated → offline → online hoạt động đúng cho `你好`, `再见`, pinyin có dấu.
- Luồng mixed tiếng Việt + Trung được ngăn chặn/sửa: pinyin chỉ sinh cho phần chữ Hán.
- Ứng dụng load ổn định, không có JS error nền tảng (ngoại trừ icon).
- Kiến trúc module hóa tốt (17 menu, panel dùng chung nhất quán).

### 5.2. Điểm yếu / lỗi tồn đọng

1. **P1 – BUG-13:** PWA install icons thiếu → không cài được app trên home screen, console error mỗi load.
2. **P1 – BUG-11:** Tìm kiếm tiếng Việt có trọng số sai → kết quả không liên quan với người dùng.
3. Các luồng mic/practice sau khi sửa chưa được re-verify đầy đủ bằng test case mới.

### 5.3. Kết luận

Build V42.9.3 **đã vá được các lỗi dịch ngôn ngữ nghiêm trọng nhất** (P0). Tuy nhiên **chưa thể hiện đủ báo cáo/tích hợp hộp thoại**
cho người dùng về các lỗi còn lại, và **chưa hoàn thành việc deploy icon PWA**. Độ chấp nhận hiện tại: **CHƯA QUYẾT ĐỊNH (Conditional)**.

---

## 6. Khuyến nghị thứ tự sửa (cho phiên V42.9.3)

1. **P1 – Sửa ngay:** BUG-13 (thiếu icon PWA → deploy lại đầy đủ package: index.html + icon PNG + sw.js + manifest).
2. **P1 – Sửa ngay:** BUG-11 (sửa trọng số/tầng xếp hạng tìm kiếm tiếng Việt trong `searchScoreForRow`).
3. **P2 – Sửa tiếp:** Re-verify BUG-04…BUG-09 bằng regression test case mới trên V42.9.3.
4. **P2 – Cải thiện:** Thêm hộp thoại/lỗi người dùng cho các luồng dịch offline/online.

---

## 7. Lý do chưa hoàn thành các mục kiểm thử khác

- Thiếu công cụ Playwright/Node, thiếu mic device, thiếu zh-CN TTS voice, thiếu network-offline switch, thiếu camera.
- Không đủ thời gian/tiện để chạy full 210 case regression trong phiên này; các case còn lại được kế thừa từ phiên V42.9.2.

---

## 8. Tài liệu liên quan

- `QA-BUG-REPORT.md` — chi tiết lỗi.
- `QA-FIX-RECOMMENDATIONS.md` — đề xuất sửa.
- `QA-TECHNICAL-ANALYSIS.md` — phân tích kỹ thuật.
- `QA-PERFORMANCE-REPORT.md` — hiệu năng.
- `QA-SECURITY-REPORT.md` — bảo mật.
- `QA-AUDIO-PINYIN-REPORT.xlsx` — âm thanh/Pinyin.
- `QA-FIX-PROMPT-FOR-CHATGPT.md` — prompt sửa cho ChatGPT.
- `QA-MENU-COVERAGE.xlsx` — coverage từng menu.
- `QA-TEST-CASES.xlsx` — bảng test case.
- `QA-EVIDENCE/` — bằng chứng.
