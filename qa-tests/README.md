# Bộ QA tự động – HỌC TIẾNG TRUNG BVT

Bộ kiểm thử Playwright độc lập cho website:
https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/

## Phạm vi

- Smoke test: HTTP, tải trang, trang rỗng, ký tự lỗi mã hóa, phát hiện menu và phiên bản.
- Menu matrix: tối đa 24 menu trên 5 cấu hình trình duyệt/thiết bị (tối đa 120 test case).
- Responsive: Desktop Chrome, mobile Chromium, Pixel/Android Chromium, iPhone WebKit và iPad WebKit.
- Input fuzz: Hán tự, tiếng Việt, Pinyin có dấu, văn bản hỗn hợp, chuỗi dài, ký tự đặc biệt và số.
- Stress navigation: mặc định 120 lần chuyển menu theo chuỗi ngẫu nhiên có seed cố định bằng fast-check.
- Accessibility: quét WCAG bằng axe-core, fail với lỗi mức critical, lưu cả serious/moderate vào JSON.
- PWA offline: bài test riêng, tùy chọn.
- Diagnostics: JavaScript page error, console error, request thất bại, HTTP lỗi, trace, screenshot và video khi fail.

## Chạy trên Windows 11

Cài Node.js 20 trở lên. Mở PowerShell tại thư mục qa-tests và chạy:

    npm install
    npx playwright install chromium webkit
    npm test
    npm run report

Chạy từng nhóm:

    npm run test:smoke
    npm run test:layout
    npm run test:stress

Tăng stress lên 200 bước:

    $env:QA_REPEAT_STEPS="200"
    $env:QA_RANDOM_SEED="20261115"
    npm run test:stress

Kiểm tra offline:

    $env:RUN_OFFLINE_TESTS="1"
    npm run test:offline

Đổi website cần kiểm thử:

    $env:BASE_URL="https://example.com/"
    npm test

## GitHub Actions

Workflow ../.github/workflows/qa-playwright.yml cho phép chạy thủ công, tự chạy sau khi workflow deploy hoàn thành thành công và chạy định kỳ hàng tuần. Artifact lưu báo cáo HTML/JSON, ảnh, video và trace trong 21 ngày.

## An toàn dữ liệu

- Mỗi test dùng browser context riêng; không dùng profile Chrome thật của bạn.
- Input fuzz chỉ nhập rồi khôi phục trường, không nhấn Lưu/Xóa/Gửi.
- Không chủ động sửa mã website hoặc dữ liệu người dùng.
- Offline test dùng context cô lập.

## Giới hạn cần hiểu rõ

1. Menu được phát hiện từ nút/link đánh số, trong navigation/sidebar hoặc có nhãn chức năng. Nếu giao diện đổi cấu trúc, cập nhật nhận diện trong tests/helpers.js.
2. Corpus dịch thuật trong data/translation-corpus.json là tập câu chuẩn ban đầu, chưa tự chấm chất lượng bản dịch trên giao diện vì cần nối đúng đầu ra menu dịch. Không được coi test nhập liệu là test độ chính xác dịch thuật.
3. ASR, TTS và OCR phụ thuộc quyền thiết bị, media fixture và dịch vụ bên ngoài. Cần bài test chuyên biệt và thiết bị thật; không đánh PASS khi chưa chạy.
4. Giả lập iPhone/Android không thay thế hoàn toàn thiết bị vật lý.
5. HTTP lỗi bên ngoài được lưu để phân tích, không tự động quy kết mọi lỗi API bên ngoài cho website.
6. Lỗi JavaScript không được xử lý làm bài test thất bại.

## Báo cáo

- playwright-report/index.html: báo cáo tương tác.
- test-results/results.json: kết quả máy đọc được.
- test-results/: screenshot, video, trace và file đính kèm.

Số lượng thao tác thực tế thay đổi theo số menu và số trường nhập liệu website đang hiển thị.