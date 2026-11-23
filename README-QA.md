# Học Tiếng Trung BVT – kiểm thử hồi quy

## Kiểm thử hiện có

Chạy bằng Node.js 22, không cần cài package bên ngoài:

```bash
node --test qa-tests/sw.test.cjs
```

Bộ test kiểm tra các hành vi của Service Worker:

- Ba tài nguyên cốt lõi (trang chính, trang luyện số và manifest) phải precache thành công.
- Thiếu một tài nguyên cốt lõi phải làm quá trình cài Service Worker thất bại, không để lại cache cài đặt dở dang.
- Lỗi precache tài nguyên tùy chọn phải được ghi cảnh báo nhưng không chặn app shell.
- Khi offline, URL `/luyen-so/` phải trả đúng trang luyện số đã cache.
- URL không có bản cache không được trả nhầm nội dung trang chủ.

GitHub Actions tự chạy bộ test tại `.github/workflows/sw-regression.yml` khi các tệp liên quan thay đổi.

## Giới hạn

Đây là kiểm thử logic Service Worker bằng Node.js, **không phải** kiểm thử trình duyệt đầy đủ. Nó không thay thế việc kiểm tra giao diện Production, camera, microphone, accessibility, Lighthouse, XSS trong browser hoặc HTTP security headers.
