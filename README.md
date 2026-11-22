# Học Tiếng Trung BVT

**Công cụ tự học tiếng Trung dành cho người Việt – từ điển, luyện nghe, đọc, viết và thực hành Pinyin.**

Ứng dụng web/PWA cá nhân, ưu tiên thao tác nhanh trên điện thoại, máy tính bảng và máy tính. Không yêu cầu tạo tài khoản. Nội dung và công cụ được phát triển theo nhu cầu học tập thực tế; đây là công cụ hỗ trợ tự học, không thay thế giáo trình, giáo viên hoặc chương trình HSK chính thức.

- **Ứng dụng:** https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/
- **Mã nguồn:** https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt
- **Nền tảng:** GitHub Pages + GitHub Actions
- **Giao diện:** Tiếng Việt; hỗ trợ điện thoại, máy tính bảng và máy tính

## Giới thiệu

Học Tiếng Trung BVT tập hợp các công cụ tra cứu, nghe phát âm, luyện phản xạ và thực hành với từ vựng/câu tiếng Trung. Ứng dụng được xây dựng như một dự án học tập cá nhân có sự hỗ trợ của AI. Các chức năng được mở rộng theo quá trình sử dụng và phản hồi; thứ tự menu không phải lộ trình sư phạm hay cam kết chuẩn đầu ra.

## Các nhóm chức năng

Ứng dụng hiện có 18 mục trong danh mục:

- **Menu 1 – Từ điển tiếng Trung:** tra cứu chữ Hán, Pinyin/thanh điệu và nghĩa tiếng Việt.
- **Menu 2 – Nhận diện chữ Hán bằng hình ảnh.**
- **Menu 3 – Dịch nhanh Việt ⇄ Trung / ánh xạ Pinyin:** nhập nội dung theo đúng chuỗi và khoảng cách người dùng cung cấp; khi đầu vào là Pinyin, hệ thống tìm các phương án câu chữ Hán dựa trên dữ liệu từ điển và các thanh điệu phù hợp. Kết quả gồm Pinyin có dấu, chữ Hán và nghĩa tiếng Việt. Có thể mở chi tiết, sao chép và nghe tiếng Trung hoặc nghĩa tiếng Việt. **Không có chức năng phát âm thanh Pinyin.**
- **Menu 4–15:** các công cụ dịch giọng nói, luyện viết, luyện đọc, ghép câu, học từ vựng, luyện số, bộ thủ, lưu trữ tài liệu và dịch đa ngôn ngữ.
- **Menu 16 – Luyện nghe phiên âm tiếng Trung:** luyện thanh mẫu, vận mẫu, âm tiết Pinyin và thanh điệu.
- **Menu 17 – Thử thách nhớ mặt chữ Hán.**
- **Menu 18 – Bản dự phòng của công cụ Menu 3:** được giữ tạm thời để đối chiếu và kiểm tra trong giai đoạn chuyển đổi. Menu 3 và Menu 18 dùng vùng giao diện, mã định danh và trạng thái riêng. Sau khi Menu 3 được xác nhận ổn định, Menu 18 mới được xem xét gỡ bỏ.

Menu 3 và Menu 18 có thể hiển thị Pinyin để người học đọc/đối chiếu. Phần nghe chỉ phát tiếng Trung và nghĩa tiếng Việt; không phát Pinyin. Không phải mọi chức năng đều hoạt động ngoại tuyến; dịch máy và một số dịch vụ ngoài cần kết nối Internet.

## Cách sử dụng

1. Mở [ứng dụng Học Tiếng Trung BVT](https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/).
2. Chọn Menu 3 để nhập câu tiếng Việt, chữ Hán hoặc Pinyin.
3. Với Pinyin, giữ nguyên cách phân tách âm tiết mong muốn; xem các phương án chữ Hán, Pinyin có dấu và nghĩa tiếng Việt.
4. Chạm vào một phương án để mở chi tiết, sao chép nội dung hoặc nghe tiếng Trung/nghĩa tiếng Việt.
5. Menu 18 hiện được giữ làm bản dự phòng để so sánh trong thời gian kiểm thử.

### Cài trên thiết bị

- **iPhone/iPad:** mở bằng Safari → Chia sẻ → Thêm vào Màn hình chính.
- **Android:** mở bằng Chrome → menu trình duyệt → Cài đặt ứng dụng hoặc Thêm vào màn hình chính.
- **Máy tính:** mở bằng trình duyệt hiện đại như Chrome, Edge, Firefox hoặc Safari.

## Tương thích và quyền riêng tư

Giao diện được thiết kế đáp ứng cho điện thoại, máy tính bảng và máy tính. Kích thước màn hình, hệ điều hành, trình duyệt, bộ nhớ và chính sách âm thanh có thể tạo ra khác biệt. Ứng dụng không yêu cầu đăng nhập cho các chức năng cốt lõi. Dữ liệu lưu cục bộ (nếu chức năng tương ứng sử dụng bộ nhớ trình duyệt) có thể chỉ tồn tại trên thiết bị/trình duyệt đó. Xóa dữ liệu trang web có thể làm mất dữ liệu cục bộ.

## Dữ liệu từ điển và ghi công

Dữ liệu từ điển tích hợp được ghi công theo dự án [ph0ngp/CVDICT](https://github.com/ph0ngp/CVDICT), phát hành theo giấy phép **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

- Giấy phép: https://creativecommons.org/licenses/by-sa/4.0/
- Giữ nguyên ghi công và điều kiện chia sẻ tương ứng khi phân phối dữ liệu phái sinh.
- Nghĩa tiếng Việt có thể chưa bao quát mọi ngữ cảnh; hãy đối chiếu cách dùng thực tế khi học.

## Cấu trúc repository

| Đường dẫn | Vai trò |
|---|---|
| `index.html` | Ứng dụng chính và dữ liệu từ điển nhúng |
| `manifest.webmanifest` | Tên, biểu tượng và cấu hình PWA |
| `sw.js` | Service Worker và cache ngoại tuyến có giới hạn |
| `audio/pinyin/` | Tài nguyên âm thanh Pinyin dùng ở các khu vực phù hợp |
| `luyen-so/index.html` | Ứng dụng luyện số tiếng Trung |
| `tools/` | Script vá artifact và kiểm thử hồi quy |
| `.github/workflows/deploy-pages.yml` | Build, kiểm tra và xuất bản GitHub Pages |
| `README-QA.md`, `qa-tests/`, `QA-REPORTS/` | Tài liệu và kiểm thử chất lượng |

## Build và deploy

Khi cập nhật nhánh `main`, GitHub Actions sao chép ứng dụng vào thư mục `site/`, chạy các patch và regression tests, đóng gói rồi xuất bản GitHub Pages. Workflow xác minh Production đang phục vụ đúng commit vừa build. Dữ liệu CVDICT được nhúng trong `index.html`; workflow không tự tải bản từ điển mới.

Kiểm thử cục bộ cơ bản:

```bash
python3 -m py_compile tools/*.py
node --test qa-tests/*.test.cjs
```

Kiểm thử tĩnh không thay thế việc kiểm tra thao tác thực tế trên Safari iOS, Chrome Android, máy tính bảng và máy tính.

## Phiên bản và báo lỗi

Phiên bản phát hành được quản lý trong manifest và giao diện. Khi báo lỗi, vui lòng nêu thiết bị, hệ điều hành, trình duyệt, menu, các bước tái hiện, nội dung đầu vào mẫu và kết quả mong đợi/thực tế.

## Liên kết

- [Mở ứng dụng](https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/)
- [Repository GitHub](https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt)
- [CVDICT](https://github.com/ph0ngp/CVDICT)
- [GitHub Pages](https://docs.github.com/en/pages)
- [PWA và Service Worker](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
