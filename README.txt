HỌC TIẾNG TRUNG — v41

Thay đổi chính:
- Tiêu đề trình duyệt / tên ứng dụng hiển thị là HỌC TIẾNG TRUNG; logo đổi thành 汉语.
- Bỏ mục menu chung “Luyện tập”; các chức năng được đưa thẳng lên thanh menu: Dịch nhanh Việt–Trung, Luyện viết Việt → Trung, Luyện viết Trung → Việt, Luyện viết chữ Hán, Luyện đọc chữ Hán.
- Từ điển giữ nguyên. Phần Ghép câu dùng bộ lọc mẫu ngữ pháp, cặp từ tương thích và nghĩa tiếng Việt; kết quả xếp theo tổ hợp 2 từ trước, rồi 3 từ, 4 từ… và tối đa 2.000 câu.
- Trong mỗi mục luyện tập chỉ hiện chức năng tương ứng; bộ nút chọn chế độ bên trong được ẩn để tránh trùng menu.
- Thanh menu có thể cuộn ngang trên màn hình điện thoại để nhìn thấy đủ 7 mục.

Cập nhật GitHub Pages:
1. Giải nén ZIP.
2. Tải lên các tệp trong thư mục này vào cùng thư mục gốc đang lưu site: index.html, sw.js, asr-worker.js, ocr-worker.js, manifest.webmanifest, icon.svg, icon-v41-192.png, icon-v41-512.png, apple-touch-icon-v41.png.
3. Sau khi cập nhật, tải lại trang. Nếu thiết bị còn lưu bản cũ do service worker, đóng tab và mở lại hoặc xóa dữ liệu trang web rồi mở lại.

Lưu ý:
- Mục “Luyện viết Trung → Việt” là chế độ có sẵn trong v40: ứng dụng đưa câu Trung, người học nhập nghĩa tiếng Việt. Tên menu phản ánh đúng hướng làm bài hiện tại.
- Đã kiểm tra cú pháp JavaScript và service worker; chưa kiểm thử trực tiếp trên từng thiết bị iPhone/Android.

Bản cập nhật lần này giữ nhãn phiên bản v41. Bộ ghép câu là bộ kiểm tra theo quy tắc/ngữ liệu cài sẵn, không phải bộ phân tích ngữ nghĩa bằng AI trực tuyến; vẫn có thể cần rà soát các câu với từ đa nghĩa.


Bản cập nhật tinh chỉnh v41 (28-10-2026):
- Làm mới favicon/logo 汉语 và buộc trình duyệt tải icon có phiên bản mới.
- Từ điển hiển thị 10 từ mỗi trang.
- Gỡ các dòng hướng dẫn dài về giọng đọc và nguồn dữ liệu khỏi phần tra từ để giao diện gọn hơn.
- Phản xạ đọc ưu tiên Web Speech API của trình duyệt (zh-CN), tạo phiên SpeechRecognition mới cho từng câu, hủy phiên cũ khi chuyển câu, gom kết quả cuối và có watchdog khi dừng để giảm lỗi treo giữa các lượt. Tính năng này tùy trình duyệt và có thể cần Internet; không sử dụng Whisper tiny làm đường chính vì kết quả nhận dạng tiếng Trung kém hơn trong thử nghiệm người dùng báo cáo.
- Nhãn phiên bản hiển thị vẫn là v41; tên cache service worker được đổi để cập nhật bản mới.


Tinh chỉnh giao diện (vẫn giữ nhãn v41): đã bỏ các đoạn giải thích dài dưới Ghép câu, OCR và Phản xạ; phần trạng thái ban đầu để trống và chỉ hiện thông báo khi thao tác cần phản hồi. Phần chọn ảnh chỉ hiện số ảnh đã chọn. Cache service worker được đổi tên để trình duyệt lấy nội dung mới.


Tinh chỉnh giao diện và luyện viết (giữ nguyên nhãn v41):
- Tăng cỡ chữ slogan, mở rộng khoảng cách giữa hai dòng nhưng vẫn nhỏ hơn tiêu đề chính.
- Đổi chữ 汉语 trên logo sang vàng tươi; cập nhật SVG, PNG, Apple touch icon và cache token.
- Khôi phục ô thứ tự nét mẫu trong mục Luyện viết chữ Hán. Bên cạnh là vùng viết theo thứ tự nét của Hanzi Writer; khi hoàn tất hiển thị điểm và số lần viết sai nét.
- Ẩn ô vẽ tự do không chấm điểm trong chế độ luyện viết chữ Hán để thao tác khớp với chức năng xem nét mẫu ở Từ điển.


Cập nhật v41 (29-10-2026):
- Tách “NHẬN DIỆN CHỮ HÁN BẰNG HÌNH ẢNH” thành menu riêng ngay sau Từ điển và trước Dịch nhanh Việt–Trung. Chụp/tải nhiều ảnh, OCR, chọn/tích từ và thêm vào Ghép câu vẫn dùng chung danh sách từ đã chọn.
- Trong Ghép câu chỉ còn công cụ ghép câu và luyện phản xạ; vùng OCR không còn nằm trong menu này.
- Trên máy tính, giới hạn vùng vẽ Hanzi Writer trong Luyện viết chữ Hán về kích thước tương ứng với vùng luyện viết trong Từ điển, để tọa độ nét khớp với vị trí chuột. CSS sửa chỉ áp dụng desktop; bố cục trên điện thoại giữ nguyên.
- Đổi tên cache service worker để thiết bị lấy bản HTML mới.
