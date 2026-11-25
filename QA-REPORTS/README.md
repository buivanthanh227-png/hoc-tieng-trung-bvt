# Kiểm thử hồi quy

## Chạy kiểm thử

Yêu cầu Node.js 22; bộ test dùng `node:test` và module lõi của Node, không cần cài package bên ngoài.

```bash
node --test qa-tests/*.test.cjs
```

Lệnh này chạy toàn bộ suite tại `qa-tests/`, giống workflow `.github/workflows/sw-regression.yml`. Để chỉ chạy kiểm thử Service Worker:

```bash
node --test qa-tests/sw.test.cjs
```

Kiểm tra cú pháp các công cụ Python:

```bash
python3 -m py_compile tools/*.py
```

Tại thời điểm dọn tài liệu (2026-11-25), suite đầy đủ hoàn thành **71 test pass, 0 fail** trên Node.js 22. Kết quả này xác minh các regression test hiện có, không phải kiểm thử đầy đủ trên trình duyệt/thiết bị.

## Phạm vi và giới hạn

Các test kiểm tra logic Service Worker, cấu trúc banner và các hồi quy giao diện/runtime Menu 1/Menu 3 qua HTML/JavaScript. Chúng không thay thế kiểm tra trực tiếp trên Safari iOS, Chrome Android, camera, microphone, giọng đọc, accessibility, Lighthouse hoặc HTTP security headers.

## Hồ sơ lịch sử

Các báo cáo, workbook và ảnh bằng chứng được tạo cho phiên QA ngày 18/11/2026, phiên bản **V42.9.3**, đã chuyển vào [`archive/2026-11-18-V42.9.3/`](archive/2026-11-18-V42.9.3/). Đây là tài liệu lịch sử, không phải mô tả hiện trạng V42.10.23; xem README gốc để biết tính năng và triển khai hiện hành.
