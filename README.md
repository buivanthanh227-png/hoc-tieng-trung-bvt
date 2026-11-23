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

Ứng dụng hiện có **17 menu**:

- **Menu 1 – Từ điển tiếng Trung:** tra cứu theo ba trường độc lập hoặc kết hợp: chữ Hán giản thể/phồn thể, Pinyin (có thể lọc một trong năm thanh điệu) và nghĩa tiếng Việt. Danh sách kết quả chỉ xuất hiện sau khi người học nhập nội dung tìm kiếm; dữ liệu CVDICT được nhúng trong ứng dụng.
- **Menu 2 – Nhận diện chữ Hán bằng hình ảnh.**
- **Menu 3 – Dịch nhanh Việt ⇄ Trung / ánh xạ Pinyin:** giữ nguyên chuỗi và khoảng cách người dùng nhập; với Pinyin, tìm các phương án chữ Hán dựa trên dữ liệu từ điển và các thanh điệu phù hợp. Kết quả gồm Pinyin có dấu, chữ Hán và nghĩa tiếng Việt. Có thể mở chi tiết, sao chép và nghe tiếng Trung hoặc nghĩa tiếng Việt. **Không phát âm thanh Pinyin.**
- **Menu 4–15:** các công cụ dịch giọng nói, luyện viết, luyện đọc, ghép câu, học từ vựng, luyện số, bộ thủ, lưu trữ tài liệu và dịch đa ngôn ngữ.
- **Menu 16 – Luyện nghe phiên âm tiếng Trung:** luyện thanh mẫu, vận mẫu, âm tiết Pinyin và thanh điệu.
- **Menu 17 – Thử thách nhớ mặt chữ Hán.**

Các menu được tổ chức theo nhu cầu sử dụng, không phải lộ trình sư phạm hoặc chương trình HSK chính thức. Menu 3 có thể hiển thị Pinyin để người học đọc/đối chiếu; phần nghe chỉ phát tiếng Trung và nghĩa tiếng Việt. Dịch máy và một số dịch vụ ngoài cần kết nối Internet.

## Cách sử dụng

1. Mở [ứng dụng Học Tiếng Trung BVT](https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/).
2. Chọn menu phù hợp. Với Menu 1, nhập chữ Hán, Pinyin hoặc nghĩa tiếng Việt vào ô tìm kiếm tương ứng.
3. Có thể chọn thanh điệu để thu hẹp kết quả Pinyin; kết hợp các trường để lọc chính xác hơn.
4. Với Menu 3, nhập câu tiếng Việt, chữ Hán hoặc Pinyin; giữ nguyên cách phân tách âm tiết mong muốn.
5. Chạm vào phương án kết quả để mở chi tiết, sao chép nội dung hoặc nghe tiếng Trung/nghĩa tiếng Việt.

Thông tin phiên bản, ghi công tác giả và đồng hồ ngày/giờ được bố trí tại chân trang ứng dụng.

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

Phiên bản phát hành hiện tại: **V42.10.20**.

Bản V42.10.20 sửa nguyên nhân cuối cùng làm CVDICT nhúng rơi vào fallback: loader gán trực tiếp `.textContent` vào `#top-status` sau khi bố cục/footer đã loại bỏ phần tử này khỏi DOM, ném lỗi `Cannot set properties of null`. Phiên bản này thêm helper cập nhật top-status an toàn, giữ bọc khởi tạo từ điển khỏi loadPractice và nâng cache Service Worker. Banner căn đúng cạnh slogan theo cạnh lá cờ bằng Grid. Khi báo lỗi, vui lòng nêu thiết bị, hệ điều hành, trình duyệt, menu, các bước tái hiện, nội dung đầu vào mẫu và kết quả mong đợi/thực tế.

## Liên kết

- [Mở ứng dụng](https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/)
- [Repository GitHub](https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt)
- [CVDICT](https://github.com/ph0ngp/CVDICT)
- [GitHub Pages](https://docs.github.com/en/pages)
- [PWA và Service Worker](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
