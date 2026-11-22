# Học Tiếng Trung · BVT — bản dành cho GitHub Pages và điện thoại

Bản này giữ giao diện/logic của ứng dụng học tiếng Trung, tối ưu cho trình duyệt máy tính và điện thoại, đồng thời dùng Service Worker để hỗ trợ PWA/offline.

## Trạng thái dữ liệu và quy trình xuất bản hiện hành

Cập nhật ngày **21/11/2026**:

- `index.html` hiện đã chứa dữ liệu từ điển nhúng (khối `embedded-cvdict-data`); kích thước tệp trong repository khoảng **13,3 MB**.
- Workflow `.github/workflows/deploy-pages.yml` hiện sao chép `index.html` đã commit vào thư mục xuất bản, cùng manifest, icon, worker, audio và ứng dụng luyện số. Workflow **không tự tải CVDICT.u8 và không chạy `tools/build_site.py`**.
- `tools/build_site.py` thuộc quy trình template cũ, yêu cầu placeholder `EMBEDDED_CVDICT_DATA_SLOT`. Placeholder này không còn trong `index.html` hiện tại, nên không được xem là bước build đang hoạt động.
- Sau khi deploy, workflow kiểm tra `build-info.json` để xác nhận Production đang phục vụ đúng Git commit. Kiểm tra SHA này xác nhận mã nguồn được xuất bản, **không thay thế kiểm tra chất lượng hoặc số lượng mục từ điển**.

Vì vậy, thay đổi dữ liệu từ điển phải được tích hợp và kiểm tra vào `index.html` trước khi commit. Không nên giả định rằng chạy lại workflow sẽ tự tải bản CVDICT mới nhất.

Dữ liệu từ điển được ghi công theo nguồn [ph0ngp/CVDICT](https://github.com/ph0ngp/CVDICT), giấy phép **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. Phần ghi công và giấy phép cần được giữ trong ứng dụng. Bản dịch có thể còn sai sót; vui lòng kiểm tra ngữ cảnh khi học.

## Cách đưa lên GitHub và lấy link mở trên điện thoại

1. Tạo một **repository mới, Public** trên GitHub. Ví dụ đặt tên `hoc-tieng-trung-bvt`.
2. Giải nén gói này và tải **toàn bộ nội dung bên trong** lên thư mục gốc của repository, gồm thư mục `.github/workflows` và `tools` (đừng chỉ tải riêng `index.html`). Dùng nhánh `main`.
3. Vào **Settings → Pages**. Ở mục **Build and deployment**, đặt **Source = GitHub Actions**.
4. Vào tab **Actions**, mở workflow “Build and deploy Học Tiếng Trung”. Chờ workflow hoàn thành màu xanh. Workflow tạo `build-info.json` và xác minh SHA trên Production khớp với commit vừa xuất bản.
5. Mở trang đã xuất bản từ **Settings → Pages → Visit site**. Link thường có dạng `https://TEN-TAI-KHOAN.github.io/TEN-REPOSITORY/`; hãy dùng đúng link GitHub hiển thị, không tự đoán link.
6. iPhone: mở link bằng **Safari** → **Chia sẻ** → **Thêm vào MH chính**. Android: mở bằng **Chrome** → menu ⋮ → **Cài đặt ứng dụng** hoặc **Thêm vào màn hình chính**.

## Kiểm tra dữ liệu đã tích hợp

Khi cần xác nhận bản Production, đối chiếu trường `git_sha` trong `build-info.json` với commit SHA trên GitHub. Việc này chỉ xác nhận đúng artifact; số lượng, nội dung và chất lượng từ điển vẫn cần bộ kiểm thử từ điển riêng. Nếu workflow thất bại thì chưa có bản xuất bản mới; vào Actions để xem bước build/deploy bị lỗi.

## Lưu ý khi dùng trên điện thoại

- Lần mở website đầu tiên cần Internet để tải trang HTML lớn có sẵn dữ liệu từ điển.
- Khi trình duyệt cài Service Worker và lưu cache thành công, ứng dụng có thể mở lại phần giao diện/từ điển trong chế độ offline. Dung lượng cache lớn nên không thể bảo đảm mọi trình duyệt/thiết bị đều giữ cache vô thời hạn; dữ liệu IndexedDB cũng được lưu riêng trên từng thiết bị.
- Từ điển và ghép câu dựa trên dữ liệu hiện có. Dịch câu mới qua dịch vụ ngoài, tải thư viện/dữ liệu thứ tự nét, hoặc nhận dạng giọng nói có thể cần Internet/quyền microphone và phụ thuộc hỗ trợ của trình duyệt.
- Chạy lại workflow (Actions → workflow → Run workflow) sẽ xuất bản các tệp hiện có trong commit; nó không tự tải dữ liệu CVDICT mới. Khi cập nhật từ điển, cần cập nhật payload trong `index.html` và chạy regression test từ điển trước khi xuất bản.

## Cấu trúc quan trọng

- `index.html`: ứng dụng cùng dữ liệu từ điển nhúng đang được xuất bản.
- `tools/build_site.py`: helper của kiến trúc template cũ; hiện không được workflow deploy gọi.
- `.github/workflows/deploy-pages.yml`: đóng gói các tệp đã commit, xuất bản GitHub Pages và xác minh SHA Production.
- `sw.js`, `manifest.webmanifest`, `icon.svg`: hỗ trợ PWA/offline.
- `qa-tests/sw.test.cjs`: regression test cho precache và điều hướng offline.

## Nguồn tham khảo

- [CVDICT](https://github.com/ph0ngp/CVDICT)
- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- [Tài liệu GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)


## Menu 18 — xếp hạng ngữ cảnh và từ/cụm từ đã xác minh (22/11/2026)

- `tools/patch_menu18_ranking.py` được gọi trong workflow Pages để vá riêng artifact `site/index.html` trước khi xuất bản; không sửa hoặc thay thế khối dữ liệu từ điển nhúng trong `index.html`.
- Ưu tiên các từ ghép đã xác minh, bao gồm `客人`, `天气`, `现在`, `三个人` và `中文`.
- Bổ sung nghĩa tiếng Việt offline cho các mục từ ưu tiên thường gặp như `明天` và `什么`.
- Tăng trọng số từ ghép đúng ngữ cảnh khi ghép cả câu; giữ nguyên các menu và giao diện Copy/Loa khác.
- Cache Service Worker được đổi tên để trình duyệt tải lại artifact sau khi deploy.
- Bản V42.9.5 mở rộng cụm từ thông dụng theo ngữ cảnh, chọn thanh điệu cho âm tiết đơn có số/dấu thanh và nâng giới hạn chuỗi Pinyin.

## Menu 18 — sửa khả năng ghép Pinyin dài (22/11/2026)
- Bổ sung câu mẫu `jintian wo jia you ke ren` → `今天我家有客人`.
- Bổ sung dự phòng các âm tiết đơn phổ biến khi từ điển chính thiếu mục từ.
- Cho phép hiển thị kết quả ghép theo từng âm tiết thay vì loại bỏ mọi chuỗi chỉ gồm chữ đơn.
- Menu 3 và dữ liệu/chức năng của các menu khác không bị chỉnh sửa trong bản vá này.

## Menu 18 — chọn nhiều phương án thanh điệu (V42.9.8)

- Menu 18 tiếp tục dùng từ điển và luồng dịch nhanh theo cách tiếp cận của Menu 3; Menu 3 không bị thay đổi.
- Với Pinyin không dấu, giữ phương án câu khớp chính xác ở vị trí ưu tiên nhưng vẫn tìm thêm các cách ghép hợp lệ từ những thanh điệu có trong từ điển.
- Hiển thị danh sách phương án để người học chọn; khi chọn một câu ghép từ nhiều mục từ, nghĩa tiếng Việt được dịch theo toàn câu.
- Giữ nguyên chuỗi người dùng nhập; chuẩn hóa chỉ dùng nội bộ để tra cứu, không ghi đè hoặc tự thêm/bớt khoảng trắng trong ô nhập.
- Workflow kiểm tra bản vá chạy lặp, cú pháp Python/JavaScript và các kiểm thử hồi quy thanh điệu trước khi xuất bản.


## Menu 18 — ánh xạ độc lập từng mục Pinyin (V42.9.9)

- Giữ nguyên chuỗi người dùng nhập; chỉ tách nội bộ theo các dấu phân cách đã có, không sửa ô nhập.
- Mỗi mục nhập được tra riêng trong CVDICT. Mỗi thanh điệu có trong từ điển tạo tối đa một kết quả cho mục đó; tổng số kết quả là tổng các lựa chọn của từng mục, không phải tích tổ hợp ghép thành câu.
- Không ghép các mục nhập thành câu, không thay âm tiết, không tự tạo chữ Hán cho mục không có dữ liệu.
- Với âm tiết đơn không dấu, hiển thị các thanh 1–4; thanh nhẹ chỉ xuất hiện khi người học nhập rõ thanh 5. Từ nhiều âm tiết vẫn giữ cách đọc thanh nhẹ nếu đó là cách đọc từ điển.
- Bộ kiểm thử dùng trực tiếp 122.523 dòng CVDICT nhúng, gồm ví dụ `a ba` → 8 lựa chọn (4 + 4), `ni jin le ma`, Pinyin có dấu, từ viết liền `jintian`, và đầu vào không có trong từ điển.
- Menu 3 và các menu khác không bị sửa.
