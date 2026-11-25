# QA-FIX-PROMPT-FOR-CHATGPT — HỌC TIẾNG TRUNG BVT

**Nhiệm vụ:** Prompt riêng để ChatGPT hiểu tình trạng ứng dụng và sửa lỗi trực tiếp trên mã nguồn / GitHub ở giai đoạn tiếp theo.

---

## PROMPT CHO CHATGPT (COPY VÀ DÁN)

```
Bạn là kỹ sư phần mềm đang được giao nhiệm vụ sửa lỗi cho ứng dụng web "HỌC TIẾNG TRUNG BVT".

THÔNG TIN ỨNG DỤNG:
- Ứng dụng học tiếng Trung (Vietnamese-first) với đa ngôn ngữ.
- Deploy URL: https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/
- Phiên bản hiện tại đã kiểm thử: V42.9.3 (được deploy lên GitHub Pages).
- Kiến trúc: static SPA (index.html chứa inline CSS/JS) + 1 iframe (menu 11).
- Source local tham khảo: hoc-tieng-trung-bvt-v42.9.3-patch (1) (đã có bản vá local).

NGUYÊN NHÂN GỐC (đã xác minh trong phiên QA 18/11/2026):
1. BUG-01 (P0, FIXED): lookup từ vựng/curated trước khi gọi machineTranslate; thiếu override offline cho từ đơn.
2. BUG-02 (P0, FIXED): tryLocalTranslation dùng near-match includes() ưu tiên câu dài; queryIsPinyin chặn ký tự dấu Latin.
3. BUG-03 (P1, FIXED): pinyinForChinese/pinyinToChinese áp dụng lên toàn chuỗi, cần phân segment Hanzi/Latin.
4. BUG-11 (P1, OPEN): searchScoreForRow xếp hạng sai cho query tiếng Việt ngắn (ví dụ "cá" ra kết quả pinyin).
5. BUG-13 (P1, OPEN): PWA icon (icon-v41-192.png, icon-v41-512.png, apple-touch-icon-v41.png) thiếu → HTTP 404 trên deploy.

HÀNH VI ĐÃ XÁC NHẬN TRÊN MÔ PHÒNG V42.9.3:
- "再见" → Pinyin "Zài jiàn", nghĩa "Tạm biệt" ✅ FIXED.
- "你好" → Pinyin "Nǐ hǎo", nghĩa "Xin chào" ✅ FIXED.
- "nǐ hǎo" → Pinyin "Nǐ hǎo", nghĩa "Xin chào" ✅ FIXED.
- "Xin chào 你好" → Pinyin "Xin chào nǐ hǎo" ✅ FIXED.
- Tìm "cá" → top kết quả là pinyin (cā/cǎ...) ❌ BUG-11 VẪN OPEN.
- Fetch icon → HTTP 404 ❌ BUG-13 VẪN OPEN.

CÔNG VIỆC CẦN LÀM:
1. Bổ sung/thiết kế lại cách sửa cho BUG-13: đảm bảo icon 192/512 PNG và apple-touch-icon tồn tại trong gốc repo deploy; cập nhật manifest + sw.js + bump cache.
2. Sửa ranking tìm kiếm cho BUG-11 trong searchScoreForRow.
3. Re-verify sau khi sửa: các regression case R-01..R-08 (xem QA-TEST-CASES.xlsx), đặc biệt:
   - R-01..R-04: dịch từ đơn/pinyin/mixed phải đúng.
   - R-05: icon PWA phải trả HTTP 200.
   - R-06: tìm "cá" phải có nghĩa "cá" trước.

YÊU CẦU KHÔNG ĐƯỢC THAY ĐỔI NGOÀI PHẠM VI SỬA:
- Không thay đổi dữ liệu từ điển, dữ liệu âm thanh, dữ liệu câu hỏi.
- Không thay đổi cấu trúc thư mục repo.
- Không đổi API bên ngoài (MyMemory, BVT workers, OCR/ASR).
- Không thay đổi phạm vi menu/functionality chưa được xác nhận.
- Không tự ý đổi version quá nhiều; mỗi lần thay đổi SW cache phải bump đúng 1 lần.

BÁO CÁO SAU SỬA:
- Chỉ báo cáo lỗi đã sửa và test case re-run.
- Nếu không chắc lỗi nào còn tái phát, phải re-run toàn bộ regression suite trước khi báo DONE.
```

---

## 8. Yêu cầu không được thay đổi ngoài phạm vi sửa lỗi

- Không thay đổi dữ liệu từ điển, dữ liệu âm thanh, dữ liệu câu hỏi.
- Không thay đổi cấu trúc thư mục repo.
- Không đổi API ngoài (MyMemory, BVT workers, OCR/ASR).
- Không thay đổi phạm vi menu/functionality chưa được xác nhận.
- Không tự ý đổi version quá nhiều; mỗi lần thay đổi SW cache phải bump đúng 1 lần.

---

## 9. Ghi chú cho QA sau khi ChatGPT sửa

- Chạy lại R-01..R-08.
- Chạy lại smoke: boot trang, console errors = 0.
- Nếu BUG-13 được sửa, chạy Lighthouse/PWA install check.
- Nếu BUG-11 được sửa, chạy tìm kiếm `cá`, `ăn`, `nước`, `người`, `你好`.
