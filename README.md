# Học Tiếng Trung BVT

**Công cụ tự học tiếng Trung dành cho người Việt – từ điển, luyện nghe, đọc, viết và thực hành Pinyin.**

Ứng dụng web/PWA cá nhân, ưu tiên thao tác nhanh trên điện thoại, máy tính bảng và máy tính. Không yêu cầu tạo tài khoản. Nội dung và công cụ được phát triển theo nhu cầu học tập thực tế; đây là công cụ hỗ trợ tự học, không tuyên bố thay thế giáo trình, giáo viên hoặc một chương trình HSK chính thức.

- **Ứng dụng trực tiếp:** https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/
- **Mã nguồn:** https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt
- **Nền tảng xuất bản:** GitHub Pages + GitHub Actions
- **Kiểu ứng dụng:** Web app có hỗ trợ Progressive Web App (PWA) và cache ngoại tuyến có giới hạn
- **Ngôn ngữ giao diện:** Tiếng Việt

## Giới thiệu

Học Tiếng Trung BVT tập hợp nhiều công cụ trong một giao diện để người học có thể tra cứu, nghe phát âm, luyện phản xạ và thực hành với từ vựng/câu tiếng Trung. Trọng tâm là giúp người học nhìn rõ Pinyin có dấu thanh, nghe mẫu âm và tự kiểm tra cách ghép câu từ dữ liệu từ điển hiện có.

Ứng dụng được xây dựng như một dự án học tập cá nhân có sự hỗ trợ của AI. Các chức năng được mở rộng theo quá trình sử dụng và phản hồi; không nên hiểu thứ tự menu là một lộ trình sư phạm hay cam kết chuẩn đầu ra.

## Các nhóm chức năng

Giao diện hiện có 18 menu/chức năng. Một số khu vực chính:

- **Tra cứu từ điển Trung–Việt:** tra theo chữ Hán, Pinyin/thanh điệu và nghĩa tiếng Việt; xem các mục từ và thông tin liên quan trong dữ liệu tích hợp.
- **Dịch và xử lý văn bản:** các công cụ hỗ trợ dịch, nhập nội dung và xử lý văn bản đa ngôn ngữ; một số tác vụ có thể cần Internet.
- **Luyện tập:** các hoạt động nghe, đọc, viết, ghi nhớ từ vựng và thực hành theo những công cụ được cung cấp trong từng menu.
- **Bộ thủ và tra cứu chữ:** hỗ trợ tìm hiểu thành phần chữ Hán và thông tin liên quan.
- **Menu 16 – Luyện nghe phiên âm tiếng Trung:** luyện thanh mẫu, vận mẫu, âm tiết Pinyin và thanh điệu; có các chế độ nghe/luyện tập theo cấu hình của ứng dụng.
- **Menu 18 – Ánh xạ Pinyin sang câu chữ Hán:** nhập Pinyin, tìm các kết quả từ dữ liệu từ điển và hiển thị các phương án thanh điệu. Kết quả được trình bày theo thứ tự Pinyin, chữ Hán và nghĩa tiếng Việt để dễ so sánh; người học có thể mở chi tiết, sao chép và nghe từng phần.

Tên, phạm vi và cách hoạt động của từng menu được xác định bởi phiên bản ứng dụng đang triển khai. Không phải mọi chức năng đều hoạt động ngoại tuyến; các dịch vụ ngoài, dịch máy, nhận dạng giọng nói hoặc tải tài nguyên có thể yêu cầu kết nối mạng và quyền truy cập của trình duyệt.

## Cách sử dụng

1. Mở [ứng dụng Học Tiếng Trung BVT](https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/).
2. Chọn menu phù hợp với nhu cầu tra cứu hoặc luyện tập.
3. Với Menu 18, nhập Pinyin theo cách phân tách từ mong muốn, thực hiện tìm/ghép kết quả, sau đó xem Pinyin có dấu thanh trước khi chọn phương án.
4. Dùng nút nghe và sao chép trong kết quả chi tiết. Âm thanh phụ thuộc dữ liệu âm thanh tích hợp, kết nối mạng và khả năng phát âm của trình duyệt/thiết bị.
5. Có thể thêm ứng dụng vào màn hình chính để mở nhanh như một ứng dụng.

### Cài trên thiết bị

- **iPhone/iPad:** mở bằng Safari → Chia sẻ → Thêm vào Màn hình chính.
- **Android:** mở bằng Chrome → menu trình duyệt → Cài đặt ứng dụng hoặc Thêm vào màn hình chính.
- **Máy tính:** mở bằng trình duyệt hiện đại như Chrome, Edge, Firefox hoặc Safari; có thể cài ứng dụng nếu trình duyệt hỗ trợ.

## Tương thích thiết bị và quyền riêng tư

Giao diện được thiết kế đáp ứng cho điện thoại, máy tính bảng và máy tính. Tuy nhiên, kích thước màn hình, hệ điều hành, trình duyệt, bộ nhớ và chính sách âm thanh có thể tạo ra khác biệt.

Ứng dụng không yêu cầu đăng nhập để sử dụng các chức năng cốt lõi. Dữ liệu học tập lưu cục bộ (nếu chức năng tương ứng sử dụng bộ nhớ trình duyệt) có thể chỉ tồn tại trên thiết bị/trình duyệt đó. Xóa dữ liệu trang web hoặc trình duyệt có thể làm mất dữ liệu cục bộ. Các chức năng kết nối dịch vụ bên ngoài chịu chính sách riêng của nhà cung cấp dịch vụ đó.

## Dữ liệu từ điển và ghi công

Dữ liệu từ điển tích hợp được ghi công theo dự án [ph0ngp/CVDICT](https://github.com/ph0ngp/CVDICT), phát hành theo giấy phép **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

- Giấy phép: https://creativecommons.org/licenses/by-sa/4.0/
- Giữ nguyên ghi công và các điều kiện chia sẻ tương ứng khi phân phối dữ liệu phái sinh.
- Nghĩa tiếng Việt và thông tin từ điển có thể chưa bao quát mọi ngữ cảnh; hãy đối chiếu ví dụ và cách dùng thực tế khi học.

## Cấu trúc repository

| Đường dẫn | Vai trò |
|---|---|
| `index.html` | Ứng dụng chính và dữ liệu từ điển nhúng được xuất bản |
| `manifest.webmanifest` | Tên, biểu tượng và cấu hình cài đặt PWA |
| `sw.js` | Service Worker, cache app shell và xử lý tài nguyên âm thanh |
| `audio/pinyin/` | Tài nguyên âm thanh Pinyin được lưu trong repository (nếu có) |
| `luyen-so/index.html` | Ứng dụng luyện số tiếng Trung |
| `tools/` | Các script vá giao diện/logic trên artifact và kiểm thử hồi quy |
| `.github/workflows/deploy-pages.yml` | Quy trình build, kiểm tra và xuất bản GitHub Pages |
| `README-QA.md`, `qa-tests/`, `QA-REPORTS/` | Tài liệu và kiểm thử chất lượng |

## Quy trình build và deploy

Mỗi lần cập nhật trên nhánh `main`, GitHub Actions thực hiện các bước chính:

1. Checkout commit nguồn.
2. Tạo thư mục `site/` và sao chép các tệp được xuất bản.
3. Chạy các script overlay cần thiết trên bản artifact, bao gồm kiểm thử Menu 18, Menu 1 và phần nhận diện thương hiệu đầu trang.
4. Chạy kiểm tra cú pháp và regression tests.
5. Đóng gói và xuất bản GitHub Pages.
6. Kiểm tra `build-info.json` để xác nhận Production phục vụ đúng commit đã build.

**Lưu ý quan trọng về từ điển:** dữ liệu CVDICT hiện được nhúng trong `index.html`. Workflow deploy không tự tải bản CVDICT mới và không tự thay dữ liệu từ điển. Khi thay đổi dữ liệu, phải cập nhật payload đã nhúng và chạy bộ kiểm thử từ điển trước khi xuất bản. `tools/build_site.py` thuộc quy trình template cũ, không phải bước build đang hoạt động của workflow hiện tại.

### Chạy kiểm thử cục bộ

Yêu cầu Python 3 và Node.js 22 cho các bộ kiểm thử tương ứng. Một số kiểm thử Python chạy trực tiếp trên artifact HTML đã tạo:

```bash
python3 -m py_compile tools/*.py
node --test qa-tests/*.test.cjs
```

Để kiểm thử đúng các overlay đang deploy, chạy workflow GitHub Actions hoặc thực hiện theo đúng thứ tự các lệnh trong `.github/workflows/deploy-pages.yml`. Kiểm thử tĩnh không thay thế việc kiểm tra thao tác thực tế trên Safari iOS, Chrome Android, máy tính bảng và máy tính.

## Phiên bản và thay đổi

Phiên bản hiển thị trong manifest và giao diện được cập nhật theo mỗi đợt phát hành. Xem lịch sử commit và GitHub Actions để biết chính xác nội dung đã triển khai. Phiên bản đang được chuẩn bị trong thay đổi này: **V42.10.9**.

## Báo lỗi và đóng góp

Khi báo lỗi, vui lòng cung cấp:
- Thiết bị, hệ điều hành và trình duyệt.
- Menu/chức năng và các bước tái hiện.
- Nội dung đầu vào mẫu (không gửi dữ liệu riêng tư).
- Kết quả mong đợi và kết quả thực tế.
- Ảnh chụp màn hình hoặc thông báo lỗi nếu có.

## Liên kết

- [Mở ứng dụng](https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/)
- [Repository GitHub](https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt)
- [CVDICT](https://github.com/ph0ngp/CVDICT)
- [GitHub Pages](https://docs.github.com/en/pages)
- [PWA và Service Worker](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
