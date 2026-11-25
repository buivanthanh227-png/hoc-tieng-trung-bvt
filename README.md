# Học Tiếng Trung BVT

Ứng dụng web/PWA tự học tiếng Trung dành cho người Việt, tập hợp công cụ tra cứu, dịch, luyện nghe/nói và thực hành chữ Hán. Giao diện tối ưu cho điện thoại, máy tính bảng và máy tính; không yêu cầu tài khoản. Đây là công cụ hỗ trợ tự học, không thay thế giáo trình, giáo viên hoặc chương trình HSK chính thức.

- **Ứng dụng:** https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/
- **Mã nguồn:** https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt
- **Nền tảng:** GitHub Pages, GitHub Actions và PWA Service Worker
- **Giao diện:** Tiếng Việt; hỗ trợ màn hình di động và máy tính
- Phiên bản phát hành hiện tại: **V42.10.23**.

## Tính năng

Ứng dụng chính có 17 menu, được tổ chức theo nhóm công cụ (không phải lộ trình sư phạm):

1. Từ điển Trung–Việt: tra theo nghĩa, chữ Hán giản thể/phồn thể và Pinyin; dữ liệu CVDICT được tích hợp.
2. Nhận diện chữ Hán từ hình ảnh (OCR).
3. Dịch nhanh Việt ⇄ Trung và tra/ánh xạ Pinyin; hiển thị phương án khi có nhiều cách hiểu.
4–15. Các nhóm công cụ dịch giọng nói, luyện viết và đọc, ghép câu, học từ vựng, luyện số, bộ thủ, thư viện tài liệu và dịch đa ngôn ngữ.
16. Luyện nghe phiên âm tiếng Trung: thanh mẫu, vận mẫu, âm tiết Pinyin và thanh điệu.
17. Thử thách ghi nhớ chữ Hán.

Một trang luyện số độc lập cũng được xuất bản tại `/luyen-so/`. Một số chức năng cần microphone, camera, giọng đọc do thiết bị cung cấp hoặc kết nối Internet. ASR cục bộ tải mô hình khi cần; OCR, dịch và một số dịch vụ khác dùng các endpoint bên ngoài. Khả năng phát âm/nhận diện phụ thuộc trình duyệt, thiết bị, quyền truy cập và kết nối.

## Sử dụng và cài đặt

Mở [ứng dụng trực tuyến](https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/) rồi chọn menu theo nhu cầu. Trên iPhone/iPad, mở bằng Safari và chọn **Chia sẻ → Thêm vào Màn hình chính**. Trên Android, mở bằng Chrome và chọn **Cài đặt ứng dụng** hoặc **Thêm vào màn hình chính**. Hãy cấp quyền camera/microphone cho các chức năng cần chúng.

### Chạy cục bộ

Cần Python 3 để phục vụ tệp qua localhost (Service Worker không chạy qua `file://`):

```bash
git clone https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt.git
cd hoc-tieng-trung-bvt
python3 -m http.server 8000
```

Sau đó mở `http://localhost:8000/`. Không cần cài package Node.js cho bộ regression tests; cần Node.js 22.

## Cấu trúc repository

| Đường dẫn | Chức năng / ghi chú |
|---|---|
| `index.html` | Entry point ứng dụng chính; giao diện, CSS/JavaScript nhúng và dữ liệu từ điển. |
| `menu3-pinyin-fix-v42.10.23.js` | Runtime bổ trợ Menu 3, nạp trực tiếp và qua Service Worker. |
| `luyen-so/index.html` | Ứng dụng luyện số độc lập, được xuất bản tại `/luyen-so/`. |
| `sw.js` | PWA Service Worker: shell offline, cache điều hướng, asset và âm thanh Pinyin. |
| `manifest.webmanifest`, `icon.svg`, `*-v41*.png` | Metadata cài PWA và biểu tượng ứng dụng. |
| `audio/pinyin/` | Kho MP3 Pinyin; tên tệp được tạo động ở runtime và được dùng làm nguồn local/fallback. Giữ `ATTRIBUTION.txt` cùng corpus. |
| `asr-worker.js`, `asr-voice-worker.js` | Worker xử lý nhận diện giọng nói cục bộ; worker thứ hai hiện được đóng gói/cache nhưng không tìm thấy call site trực tiếp trong entry point, nên được giữ để tương thích. |
| `asr-cloudflare-worker.js`, `ocr-worker.js` | Mã nguồn Cloudflare Worker cho dịch vụ ASR/dịch và OCR. |
| `asr-cloudflare-worker-fixed.js` | Bản nguồn tương thích cũ, không được tham chiếu bởi luồng ứng dụng hoặc workflow Pages hiện tại; giữ nguyên vì chưa xác minh được liệu có được triển khai/quản lý thủ công bên ngoài repo hay không. |
| `.github/workflows/` | Workflow xuất bản GitHub Pages, kiểm thử Service Worker/Menu 3, kiểm tra mapping và bổ sung audio Pinyin. |
| `tools/` | Script chuẩn bị build, patch/check HTML và test Python; một số được gọi bởi CI, không xóa chỉ dựa trên tên hoặc việc không có import runtime. `build_site.py` là đường build thủ công riêng, không phải workflow Pages hiện hành. |
| `qa-tests/` | Bộ regression tests Node.js dùng `node:test`. |
| `QA-REPORTS/README.md` | Hướng dẫn chạy và phạm vi kiểm thử hiện tại. |
| `QA-REPORTS/archive/` | Hồ sơ QA cũ theo phiên bản; hồ sơ V42.9.3 và bằng chứng ngày 18/11/2026 được lưu trong `2026-11-18-V42.9.3/`. |
| `docs/REPOSITORY-ABOUT.md` | Mô tả ngắn phục vụ trang thông tin repository. |
| `LICENSES.txt` | Ghi công và thông tin giấy phép dữ liệu. |

## Kiểm thử

Chạy toàn bộ regression tests Node.js:

```bash
node --test qa-tests/*.test.cjs
```

Chạy kiểm tra cú pháp toàn bộ script Python trong `tools/`:

```bash
python3 -m py_compile tools/*.py
```

GitHub Actions chạy các kiểm tra tương ứng khi thay đổi mã nguồn. Các bài test hiện tại là regression/unit tests, không thay thế việc kiểm thử trực tiếp trên trình duyệt, thiết bị, camera, microphone, accessibility hay HTTP security headers.

## Build và triển khai

### Website GitHub Pages

Push lên nhánh `main` hoặc chạy thủ công workflow **Build and deploy Học Tiếng Trung** tại `.github/workflows/deploy-pages.yml`. Workflow áp dụng các bước kiểm tra/patch tương thích, chạy regression tests, chuẩn bị thư mục `site/`, xác minh các tệp bắt buộc và triển khai GitHub Pages. Sau triển khai, workflow kiểm tra `build-info.json` để xác nhận commit đang chạy.

Không chỉnh `site/` như nguồn chính: đây là artifact do workflow tạo. Thay đổi ứng dụng cần được thực hiện trên các tệp nguồn ở gốc repo (và cập nhật kiểm thử/cache nếu thích hợp).

### Cloudflare Workers

GitHub Pages workflow **không triển khai Cloudflare Workers**. Repo không có cấu hình Wrangler hoặc workflow Cloudflare; mã nguồn Worker được quản lý/triển khai riêng trong Cloudflare. Nếu chỉnh Worker, hãy cập nhật đúng Worker tương ứng trong Cloudflare Dashboard hoặc cấu hình triển khai hiện có, kiểm tra bindings/secrets, rồi xác nhận endpoint hoạt động; không đưa secret vào Git.

| Worker | Vai trò | Binding/secret được mã nguồn sử dụng |
|---|---|---|
| `asr-cloudflare-worker.js` | ASR và dịch qua endpoint `bvt-asr…workers.dev` | `AI`, `TURNSTILE_SECRET_KEY`, `ALLOWED_ORIGIN` |
| `ocr-worker.js` | Proxy OCR qua endpoint `bvt-ocr…workers.dev` | `OCR_SPACE_API_KEY` |

`asr-worker.js` và `asr-voice-worker.js` là browser Web Workers, không phải Cloudflare Workers; chúng được phân phối cùng trang và không cần triển khai bằng Cloudflare Worker.

## PWA, cache và dữ liệu

Service Worker precache shell cốt lõi, cache tài nguyên tùy chọn và dùng cache riêng cho âm thanh Pinyin. Sau khi xuất bản, ứng dụng thường tự nhận phiên bản mới khi Service Worker cập nhật. Nếu vẫn thấy nội dung cũ, thử tải lại trang hoặc đóng/mở ứng dụng; chỉ xóa dữ liệu trang web khi cần thiết vì việc đó có thể xóa dữ liệu lưu cục bộ của người dùng. Không cần deploy lại Cloudflare Worker nếu chỉ sửa giao diện/tài liệu hoặc asset Pages.

Ứng dụng không yêu cầu đăng nhập cho các chức năng cốt lõi. Dữ liệu do một tính năng lưu bằng bộ nhớ trình duyệt có thể chỉ tồn tại trên thiết bị/trình duyệt đó. Một số chức năng gửi yêu cầu đến dịch vụ bên ngoài; cân nhắc nội dung đầu vào trước khi sử dụng.

## Dữ liệu và ghi công

Dữ liệu từ điển tích hợp dựa trên [ph0ngp/CVDICT](https://github.com/ph0ngp/CVDICT), theo giấy phép [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Giữ nguyên ghi công và điều kiện chia sẻ tương ứng khi phân phối dữ liệu phái sinh. Xem thêm `LICENSES.txt` và `audio/pinyin/ATTRIBUTION.txt`.

## Nhật ký cập nhật

- **V42.10.23:** phiên bản ứng dụng được khai báo trong `manifest.webmanifest` và đồng bộ trong quy trình Pages.
- **2026-11-25 (repository):** sửa bố cục banner để căn giữa cả tiêu đề, hai câu slogan và hai lá cờ; lưu trữ hồ sơ QA cũ theo phiên bản và cập nhật tài liệu/test hướng dẫn. Các thay đổi tài liệu không làm thay đổi số phiên bản ứng dụng.

## Báo lỗi

Khi báo lỗi, vui lòng ghi thiết bị, hệ điều hành, trình duyệt, menu, các bước tái hiện, nội dung mẫu và kết quả mong đợi/thực tế; nếu có thể, gửi ảnh chụp màn hình hoặc video.
