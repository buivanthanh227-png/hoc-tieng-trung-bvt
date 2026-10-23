# Học Tiếng Trung · BVT — bản dành cho GitHub Pages và điện thoại

Bản này giữ giao diện/logic của ứng dụng được cung cấp, bổ sung kiểm tra dữ liệu từ điển khi xuất bản, tối ưu một số chi tiết cho Safari trên iPhone và dùng Service Worker theo phiên bản cache mới.

## Điểm quan trọng về bộ từ điển

File `index.html` trong kho là **mã nguồn mẫu**, chưa chứa dữ liệu lớn. GitHub Actions sẽ tự tải `CVDICT.u8` từ repo nguồn, xác minh có ít nhất 120.000 dòng mục từ hợp lệ, rồi tạo `site/index.html` với dữ liệu nhúng trực tiếp. Nếu tải dữ liệu thất bại hoặc không đủ số lượng, bước xuất bản sẽ dừng thay vì đưa ra một trang chỉ có từ cơ bản.

Dữ liệu nguồn: [ph0ngp/CVDICT](https://github.com/ph0ngp/CVDICT). CVDICT được phát hành theo giấy phép **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. Phần ghi công và giấy phép cũng được giữ trong giao diện ứng dụng. Bản dịch có thể còn sai sót; vui lòng kiểm tra ngữ cảnh khi học.

## Cách đưa lên GitHub và lấy link mở trên điện thoại

1. Tạo một **repository mới, Public** trên GitHub. Ví dụ đặt tên `hoc-tieng-trung-bvt`.
2. Giải nén gói này và tải **toàn bộ nội dung bên trong** lên thư mục gốc của repository, gồm thư mục `.github/workflows` và `tools` (đừng chỉ tải riêng `index.html`). Dùng nhánh `main`.
3. Vào **Settings → Pages**. Ở mục **Build and deployment**, đặt **Source = GitHub Actions**.
4. Vào tab **Actions**, mở workflow “Build and deploy Học Tiếng Trung”. Chờ workflow hoàn thành màu xanh. Trong bước build, nhật ký sẽ ghi số dòng CVDICT đã xác minh và dung lượng HTML thành phẩm.
5. Mở trang đã xuất bản từ **Settings → Pages → Visit site**. Link thường có dạng `https://TEN-TAI-KHOAN.github.io/TEN-REPOSITORY/`; hãy dùng đúng link GitHub hiển thị, không tự đoán link.
6. iPhone: mở link bằng **Safari** → **Chia sẻ** → **Thêm vào MH chính**. Android: mở bằng **Chrome** → menu ⋮ → **Cài đặt ứng dụng** hoặc **Thêm vào màn hình chính**.

## Kiểm tra dữ liệu đã tích hợp

Khi mở bằng link GitHub Pages sau khi workflow thành công, phần đầu trang phải hiển thị tổng số từ vựng trên 120.000. Thẻ trạng thái từ điển sẽ báo CVDICT nhúng sẵn. Nếu workflow thất bại thì chưa có bản xuất bản mới; vào Actions để xem bước tải/kiểm tra CVDICT.

## Lưu ý khi dùng trên điện thoại

- Lần mở website đầu tiên cần Internet để tải trang HTML lớn có sẵn dữ liệu từ điển.
- Khi trình duyệt cài Service Worker và lưu cache thành công, ứng dụng có thể mở lại phần giao diện/từ điển trong chế độ offline. Dung lượng cache lớn nên không thể bảo đảm mọi trình duyệt/thiết bị đều giữ cache vô thời hạn; dữ liệu IndexedDB cũng được lưu riêng trên từng thiết bị.
- Từ điển và ghép câu dựa trên dữ liệu hiện có. Dịch câu mới qua dịch vụ ngoài, tải thư viện/dữ liệu thứ tự nét, hoặc nhận dạng giọng nói có thể cần Internet/quyền microphone và phụ thuộc hỗ trợ của trình duyệt.
- Để nhận bản từ điển mới nhất, chạy lại workflow (Actions → workflow → Run workflow) hoặc đẩy một commit mới lên `main`. Mỗi lần chạy sẽ tải lại dữ liệu và tạo mã phiên bản mới để tránh dùng nhầm bản cũ trong IndexedDB.

## Cấu trúc quan trọng

- `index.html`: mã nguồn ứng dụng có vị trí chờ để nhúng dữ liệu.
- `tools/build_site.py`: xác minh số mục từ và tạo HTML có CVDICT nhúng.
- `.github/workflows/deploy-pages.yml`: tải dữ liệu, xây dựng và xuất bản GitHub Pages.
- `sw.js`, `manifest.webmanifest`, `icon.svg`: hỗ trợ PWA.

## Nguồn tham khảo

- [CVDICT](https://github.com/ph0ngp/CVDICT)
- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- [Tài liệu GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
