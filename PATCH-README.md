# Bản vá Menu 3 – V42.10.22

Đây là **gói vá chồng lên repository hiện có**, không phải bản sao toàn bộ repository.

## Tệp trong gói

- `index.html` – sửa logic Pinyin mới; deadline Turnstile Menu 3 12 giây; timeout Worker 45 giây; cooldown 60 giây sau lỗi xác thực; hiển thị trạng thái chuyển fallback; giữ nguyên xác thực Worker, hộp thoại, Copy và phát âm.
- `sw.js` – đổi cache key để trình duyệt cài bản sửa thay vì tiếp tục dùng cache V42.10.22 cũ.
- `README.md` – cập nhật mô tả hành vi Pinyin và cơ chế fallback.
- `qa-tests/menu1-menu3-ui-regression.test.cjs` – cập nhật regression test cho chữ ký hàm và hành vi mới.
- `qa-tests/menu3-pinyin-composition-turnstile.test.cjs` – bổ sung test Pinyin, Turnstile timeout, token muộn, không POST khi thiếu token và cooldown fallback.

## Cách áp dụng

1. Giải nén ZIP vào đúng thư mục gốc repository `hoc-tieng-trung-bvt`.
2. Chọn ghi đè các tệp cùng tên và giữ nguyên mọi thư mục/tệp khác trong repository.
3. Kiểm tra `git diff --check` và chạy `node --test qa-tests/*.test.cjs`.
4. Chỉ sau khi kiểm tra xong mới đưa các thay đổi lên nhánh `main` theo quy trình GitHub Pages hiện tại.

**Không xóa repository cũ để thay bằng nội dung ZIP này.** Gói chỉ chứa các tệp cần thay thế/thêm mới; các thư mục `.github/`, `tools/`, `audio/`, `luyen-so/`, `QA-REPORTS/` và những tệp khác phải được giữ nguyên.

## Giới hạn kiểm thử

Các test mới mô phỏng callback Turnstile hợp lệ và lỗi timeout, không tạo được Turnstile token thật. Chúng xác nhận luồng ứng dụng không gửi POST khi không có token, nhưng không chứng minh Cloudflare cấp token trên thiết bị thật hay Workers AI đã dịch thành công trong production. Cần kiểm tra bằng Chrome thông thường sau khi triển khai.
