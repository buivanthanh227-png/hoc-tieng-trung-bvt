# FIX_REPORT — HỌC TIẾNG TRUNG BVT

**Build gốc:** V42.9.2  
**Build sau sửa:** V42.9.3 (local patch, chưa deploy)  
**Ngày:** 16 November 2026  
**Nguồn gốc:** https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt  
**Deployed URL (chưa cập nhật):** https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/  
**QA gốc:** NOT ACCEPTED (P0 translation + shared-state defects)

---

## 1. Tóm tắt

Đã sửa **các lỗi P0 và phần lớn P1** trên bản sao local của mã nguồn, dựa trên nguyên nhân gốc trong `05_BUG_REPORT.md` và `06_REGRESSION_REPORT.md`.

| Hạng mục | Giá trị |
|---|---|
| Lỗi P0 đã sửa | BUG-01, BUG-02 |
| Lỗi High/P1 đã sửa | BUG-03, BUG-04, BUG-05, BUG-06, BUG-07, BUG-08 |
| Lỗi PWA | BUG-13 (assets có trong repo; cache SW đã bump; cần deploy lại) |
| Chưa sửa trong lần này | BUG-09…BUG-12, BUG-14…BUG-17 (P2 / polish) |
| File đã đổi | `index.html`, `sw.js`, `manifest.webmanifest` (+ icon PNG đã tải về local) |
| Bản sao lưu | `index.html.backup-v42.9.2-original` |
| Commit / push / deploy | **Không** (theo yêu cầu) |

**Mục tiêu QA:** đưa app từ NOT ACCEPTED về trạng thái có thể nghiệm thu có điều kiện sau khi deploy và re-test các case P0/P1.

---

## 2. Danh sách lỗi đã sửa

### BUG-01 — `再见` → "Chà Tở" (High / P0)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân** | `machineTranslate()` gọi MyMemory trực tiếp; không có override offline cho từ đơn; dictionary không được ưu tiên trước MT. |
| **Sửa** | Thêm `CURATED_ZH_VI` với `再见 → Tạm biệt` và các từ thông dụng khác. Trong `lookupHomework`, nếu input thuần Hán và có trong curated/dictionary thì **không gọi** MyMemory. |
| **File** | `index.html` (`CURATED_ZH_VI`, nhánh `hasChinese` trong `lookupHomework`) |
| **Kỳ vọng sau sửa** | `再见` → Pinyin `Zài jiàn`, nghĩa `Tạm biệt`. |

### BUG-02 — `你好` / `nǐ hǎo` → `你好吗？` / "Bạn khỏe không?" (High / P0)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân (1)** | `tryLocalTranslation()` dùng near-match `includes()`: `你好` là substring của `你好吗` → trả về câu hỏi. |
| **Nguyên nhân (2)** | `queryIsPinyin()` **từ chối** chuỗi có dấu thanh Latin (`[\u00C0-\u024F…]`), nên `nǐ hǎo` không đi path pinyin. |
| **Sửa** | (a) `CURATED_ZH_VI['你好']='Xin chào'`; (b) `tryLocalTranslation` ưu tiên exact curated → offline key → exact sentence → exact dictionary → near-match **chỉ khi score ≥ 40** (bỏ substring thuần cho query ngắn); (c) `queryIsPinyin` strip dấu NFD rồi lookup. |
| **File** | `index.html` |
| **Kỳ vọng** | `你好` và `nǐ hǎo` → `Xin chào` (không thêm `吗`). `你好吗` vẫn có thể map đúng sang "Bạn khỏe không?" qua curated/offline. |

### BUG-03 — Mixed VI+ZH pinyin: `X i n c h à o nǐ hǎo` (High / P1)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân** | `pinyinForChinese()` đưa **cả chuỗi** vào `pinyin-pro`, Latin bị tách syllable. |
| **Sửa** | Segment theo run Hán / không-Hán; chỉ chạy pinyin trên run Hán; giữ nguyên text Latin/Việt. |
| **File** | `index.html` — `pinyinForChinese` |
| **Kỳ vọng** | `Xin chào 你好` → pinyin chứa `Xin chào` + `nǐ hǎo` (không tách từng chữ cái Latin). |

### BUG-04 — Mic error menu 8 rò sang menu 5/6/7 (Medium / P1)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân** | `#read-asr-status` dùng chung trong `#panel-practice`; không reset khi đổi tab/mode. |
| **Sửa** | Thêm `clearReadAsrStatus()`; gọi khi đổi `[data-mode]` và trong `switchTab` (khi tab ≠ `read`). |
| **File** | `index.html` |
| **Kỳ vọng** | Deny mic ở menu 8 → chuyển 5/6/7: không còn dòng "Không mở được micro…". |

### BUG-05 — Stale result sau "Đổi câu hỏi" (menus 5/6) (Medium / P1)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân** | `nextPractice()` / change-question không clear `#practice-result`. |
| **Sửa** | `resetPracticeFeedback()`: ẩn/clear result, clear input, reset `practiceChecked` + nút submit. Gọi đầu `nextPractice()`. |
| **File** | `index.html` |
| **Kỳ vọng** | Sau "Đổi câu hỏi", vùng điểm cũ biến mất. |

### BUG-06 — Empty submit không feedback / giữ stale (Medium / P1)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân** | Early return khi rỗng; result cũ vẫn hiện. |
| **Sửa** | Khi empty: clear `#practice-result`, toast, focus input. |
| **File** | `index.html` — `handleSubmit` |
| **Kỳ vọng** | Click chấm với ô trống → toast + không còn điểm cũ. |

### BUG-07 — Menu 10: "Đã dừng…" còn sau khi start lại (Medium / P1)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân** | `startVocabularyTraining()` không clear `#vocab-training-source-status`. |
| **Sửa** | Set `Đang luyện tập…` khi start. |
| **File** | `index.html` |
| **Kỳ vọng** | Stop → Start: không còn dòng "Đã dừng lượt luyện…". |

### BUG-08 — Menu 4: transcript kẹt "Đang chờ bạn nói…" sau deny (Medium / P1)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân** | Error callback chỉ update status, không reset transcript. |
| **Sửa** | Trong catch mic deny của voice-translate: set transcript = `Chưa có nội dung.` |
| **File** | `index.html` |
| **Kỳ vọng** | Deny mic → transcript không còn "Đang chờ bạn nói…". |

### BUG-13 — PWA icons 404 (Medium / P1)

| Trường | Nội dung |
|---|---|
| **Nguyên nhân** | Manifest/SW trỏ PNG; trên Pages lúc QA trả 404 (PNG **có** trong repo root). |
| **Sửa** | Tải `icon-v41-192.png`, `icon-v41-512.png`, `apple-touch-icon-v41.png` về local patch; bump `CACHE_NAME` → `hoc-trung-app-shell-v42-9-3-p0-fix-20261116`; version manifest/title → V42.9.3. |
| **Lưu ý** | Cần **deploy** full tree (index + icons + sw + manifest) để hết 404 trên Pages. |

---

## 3. File đã thay đổi

| File | Thay đổi |
|---|---|
| `index.html` | Curated ZH→VI; `tryLocalTranslation` exact-first; `queryIsPinyin` diacritics; `pinyinForChinese` segment; practice/ASR/vocab state reset; version V42.9.3 |
| `sw.js` | `CACHE_NAME` bump v42-9-3-p0-fix |
| `manifest.webmanifest` | name version V42.9.3 |
| `icon-v41-192.png` / `512` / `apple-touch-icon-v41.png` | Có sẵn từ repo (đảm bảo có trong package deploy) |
| `index.html.backup-v42.9.2-original` | Bản gốc trước patch |

**Không đổi:** dictionary data, OCR/ASR workers, menu 11 iframe logic, recorded pinyin audio pipeline.

---

## 4. Thay đổi kỹ thuật (tóm tắt)

1. **Translation resolver (menus 3/4/14/15 dùng chung path homework/local):**  
   `CURATED → offline VI-key → exact sentence → exact dict headword → ranked near (≥40) → machineTranslate`.  
   Tránh substring `你好` ⊂ `你好吗`.

2. **Pinyin input:** strip tone marks trước `lookupPinyinToken`.

3. **Pinyin output mixed script:** chỉ convert run Hán.

4. **Shared practice panel:** một helper `resetPracticeFeedback` + `clearReadAsrStatus` trên tab/mode change.

5. **Vocab / voice denial:** clear status/transcript tương ứng.

6. **PWA:** cache version mới để client nhận shell + icons sau deploy.

---

## 5. Test case cần chạy lại sau deploy

### Bắt buộc (P0/P1)

| ID | Case | Kỳ vọng sau fix |
|---|---|---|
| TC-052 | `你好` translate | Xin chào (không `吗`) |
| TC-053 | `nǐ hǎo` translate | Xin chào |
| TC-054 | `再见` translate | Tạm biệt |
| TC-050 | `Cảm ơn` offline | 谢谢 (không regression) |
| TC-051 | `Xin chào` online/offline | 你好 |
| TC-057 | `Xin chào 你好` | Pinyin không bị `X i n…` |
| TC-197 | Mic deny menu 8 → 5/6/7 | Không còn status mic error |
| TC-077 / TC-086 | Đổi câu hỏi | Result cũ biến mất |
| TC-078 / TC-087 | Empty submit | Toast + clear stale |
| TC-117 | Vocab stop → start | Không còn "Đã dừng…" khi đang chạy |
| TC-066 | Voice mic deny | Transcript ≠ "Đang chờ bạn nói…" |
| TC-015 | Manifest icons | HTTP 200 cho PNG (sau deploy) |
| TC-208 / TC-209 / TC-210 | Smoke dictionary / offline 谢谢 / menu 16 audio | PASS |

### Golden set đề xuất (20+ cặp)

`你好`, `nǐ hǎo`, `你好吗`, `再见`, `谢谢`, `Cảm ơn`, `Xin chào`, `早上好`, `晚安`, `对不起`, `没关系`, `不客气`, long VI paragraph, long ZH paragraph, emoji, empty input.

### Regression panel

Menus 3, 5, 6, 7, 8 (shared practice) + menu 10 start/stop + menu 4 deny.

---

## 6. Kết quả kiểm thử trong môi trường này

Môi trường agent **không** mở được browser interactive với app đã patch trên GitHub Pages (chưa deploy).  
Do đó:

| Hạng mục | Trạng thái |
|---|---|
| Phân tích nguyên nhân từ source deployed/repo | **Done** |
| Patch local deterministic | **Done** |
| Re-run TC trong browser sau deploy | **Pending** (cần owner deploy + QA re-test) |
| PASS/FAIL runtime sau fix | **Chưa xác nhận trên URL live** |

Sau khi bạn deploy package local (`app-src/`) lên GitHub Pages, chạy lại bảng mục 5 và cập nhật cột kết quả.

---

## 7. Lỗi còn tồn tại (chưa sửa lần này)

| ID | Mô tả | Priority | Ghi chú |
|---|---|---|---|
| BUG-09 | Menu 14 speaker đọc placeholder | P2 | Disable speak khi empty |
| BUG-10 | File text invalid silent ignore (2/14) | P2 | Message format giống menu 13 |
| BUG-11 | Search "cá" ưu tiên pinyin `ca` | P1 | Ranking meaning vs pinyin |
| BUG-12 | Combine gloss `你好` → "Bạn tốt." | P2 | Whole-word dict gloss |
| BUG-14 | Touch target 17×17 | P2 | min 44px hit area |
| BUG-15 | Contrast + label-name mismatch | P2 | Lighthouse a11y |
| BUG-16 | Menu 15 copy không toast | P2 | Reuse toast pattern |
| BUG-17 | Menu 4 empty play enabled | P2 | Disable khi empty |

Môi trường BLOCKED từ QA gốc (mic success, zh-CN TTS, real device, offline reload, camera) **vẫn BLOCKED** — không phải regression từ patch.

---

## 8. Rủi ro hồi quy

| Vùng | Rủi ro | Giảm thiểu |
|---|---|---|
| Translation resolver (3/4/14/15) | **Cao** — đổi thứ tự match | Golden set 20–30 cặp offline+online; giữ `Cảm ơn`/`Xin chào` |
| Shared practice (3/5/6/7/8) | **Trung** — reset quá sớm | Re-test correct/wrong/show-answer/change-question |
| Pinyin mixed | **Trung** | Pure Hanzi, pure Latin, emoji, punctuation |
| PWA cache bump | **Trung (install)** | Sau deploy: hard refresh, kiểm tra cache name mới, icon 200 |
| Dictionary ranking | Không đụng | BUG-11 còn mở |

**Không** đụng pipeline phát âm recorded (menu 16), SW audio range, dictionary size, OCR worker.

---

## 9. Hướng dẫn deploy (khi được yêu cầu)

1. Copy các file trong `app-src/` (ít nhất: `index.html`, `sw.js`, `manifest.webmanifest`, 3 file icon PNG) vào repo GitHub Pages.  
2. Commit message gợi ý: `fix(v42.9.3): P0 translation exact-match + shared practice state reset`.  
3. Sau deploy: hard refresh / unregister SW cũ nếu cần; xác nhận title `V42.9.3` và cache `…v42-9-3-p0-fix…`.  
4. Chạy bảng TC mục 5.  
5. Nếu P0/P1 PASS → có thể chuyển acceptance sang **CONDITIONAL ACCEPTANCE** theo `08_FINAL_ACCEPTANCE_REPORT.md`.

---

## 10. Kết luận

- **P0 (你好 / nǐ hǎo / 再见) đã được sửa tại tầng resolver đúng nguyên nhân** (exact curated + bỏ near-match substring + pinyin diacritic), không hard-code chỉ 2 case.  
- **Cụm shared-state** (mic leak, stale practice result, empty submit, vocab stop, voice transcript) đã có reset path thống nhất.  
- **PWA icons** sẵn trong package; cần deploy để hết 404.  
- **Chưa commit/push/deploy.** Bản gốc được giữ tại `index.html.backup-v42.9.2-original`.  
- Để đạt nghiệm thu: deploy → re-test TC P0/P1 + golden set → cập nhật acceptance.

**Vị trí package local:** `/home/workdir/artifacts/app-src/`  
**Báo cáo này:** `/home/workdir/artifacts/fix-output/FIX_REPORT.md`
