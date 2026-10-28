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
