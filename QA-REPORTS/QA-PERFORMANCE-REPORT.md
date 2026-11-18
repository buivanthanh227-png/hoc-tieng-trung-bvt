# QA-PERFORMANCE-REPORT — HỌC TIẾNG TRUNG BVT

**Phiên bản:** V42.9.3
**Ngày:** 18/11/2026
**Môi trường:** Windows, Chromium (in-app), 1 logical CPU, ~16 GB RAM, network bình thường

---

## 1. Kết quả thu thập (phiên V42.9.3)

| Chỉ tiêu | Kết quả | Ghi chú |
|---|---:|---|
| Navigation Timing – DOMContentLoaded | **~4.01 s** | `domContentLoadedEventEnd = 4014 ms` |
| Navigation Timing – Load | **~4.02 s** | `loadEventEnd = 4017 ms` |
| First Contentful Paint (FCP) | **~4.18 s** | `first-contentful-paint = 4180 ms` |
| Largest Contentful Paint (LCP) | chưa đo được đầy đủ | Lighthouse performance category không trả được trong phiên này |
| Cumulative Layout Shift (CLS) | chưa đo được | Chưa chạy Lighthouse performance |
| Số node DOM | **~7.24k** | `document.getElementsByTagName('*').length = 7241` |
| Transfer size (compressed) | **~4.43 MB** | `transferSize = 4431975` |
| Tài liệu HTML | ~13 MB (theo phiên trước) | Rủi ro tải ban đầu |
| Số nút phát âm Pinyin (hiển thị) | 393 cell/sequence | Menu 16 |

---

## 2. Phân tích

- Thời gian load **khá ổn** trên mạng nội bộ/GitHub Pages: DCL < 4.5s.
- FCP ~4.2s cho thấy nội dung chính chưa render sớm do tài liệu inline nặng.
- Transfer size ~4.4MB cho một SPA học ngoại ngữ là **medium–high**; cần Lighthouse để xác định bottleneck.
- DOM ~7.2k nodes cho một trang duy nhất là acceptable nhưng cần kiểm tra với các panel mở rộng.

---

## 3. Stress test

| Thử thử | Kết quả |
|---|---|
| Chuyển menu lần đầu | ổn, 0 console error |
| Đọc nhanh 391 âm tiết | chưa hoàn thành do giới hạn observation (BLOCKED/LIM) |
| Tương tác nhiều menu | chưa đủ case trong phiên này |

---

## 4. Kết luận

- Không có hiện tượng treo, lag đáng kể trong các thao tác cơ bản.
- Rủi ro chính: **tài liệu ~13MB + FCP ~4.2s** → nên tối ưu ở phiên sửa lỗi.
- Không đo được Lighthouse performance đầy đủ trong phiên này.

---

## 5. Khuyến nghị

- Chạy Lighthouse performance + TBT/CLS sau khi vá BUG-13/BUG-11.
- Ưu tiên giảm kích thước tài liệu trước khi thêm tính năng mới.
