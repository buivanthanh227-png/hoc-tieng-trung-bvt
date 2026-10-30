HỌC TIẾNG TRUNG BVT - PHIÊN BẢN V42

V42 bổ sung dịch nhanh bằng giọng nói, nhận diện tự động Việt/Trung bằng Whisper đa ngôn ngữ và thanh danh mục dọc bên trái (thu gọn trên điện thoại). Các chức năng hiện có được giữ nguyên.

HỌC TIẾNG TRUNG — v42

Thay đổi chính:
- Tiêu đề trình duyệt / tên ứng dụng hiển thị là HỌC TIẾNG TRUNG; logo đổi thành 汉语.
- Bỏ mục menu chung “Luyện tập”; các chức năng được đưa thẳng lên thanh menu: Dịch nhanh Việt–Trung, Luyện viết Việt → Trung, Luyện viết Trung → Việt, Luyện viết Hán tự, Luyện đọc chữ Hán.
- Từ điển giữ nguyên. Phần Ghép câu dùng bộ lọc mẫu ngữ pháp, cặp từ tương thích và nghĩa tiếng Việt; kết quả xếp theo tổ hợp 2 từ trước, rồi 3 từ, 4 từ… và tối đa 2.000 câu.
- Trong mỗi mục luyện tập chỉ hiện chức năng tương ứng; bộ nút chọn chế độ bên trong được ẩn để tránh trùng menu.
- V42 chuyển toàn bộ menu sang thanh dọc bên trái; trên điện thoại menu được thu gọn và mở bằng nút “DANH MỤC CHỨC NĂNG”.

Cập nhật GitHub Pages:
1. Giải nén ZIP.
2. Tải LÊN TOÀN BỘ các tệp trong thư mục này vào cùng thư mục gốc đang lưu site (không bỏ sót worker hoặc biểu tượng): index.html, sw.js, asr-worker.js, asr-voice-worker.js, ocr-worker.js, luyen-so-tieng-trung.html, manifest.webmanifest, icon.svg, icon-v41-192.png, icon-v41-512.png, apple-touch-icon-v41.png.
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


CẬP NHẬT BỔ SUNG TRONG GÓI V42 (30-10-2026)
- Tích hợp nguyên giao diện và 7 chế độ của công cụ Luyện Số Tiếng Trung V10 trong tệp luyen-so-tieng-trung.html; mở từ menu LUYỆN SỐ TIẾNG TRUNG.
- Đổi tên menu đầu tiên thành TỪ ĐIỂN TIẾNG TRUNG.
- Đổi tên menu Ghép câu thành GHÉP CÂU LUYỆN PHẢN XẠ.
- Bổ sung luồng thu âm MediaRecorder riêng cho hai chế độ phản xạ đọc câu và đọc hỏi–đáp; dùng lại asr-worker.js tiếng Trung có sẵn để xử lý từng lượt, tránh phụ thuộc vào phiên SpeechRecognition của trình duyệt.
- Cải thiện nhận diện giọng nói của DỊCH NHANH BẰNG GIỌNG NÓI: chuẩn hóa âm thanh 16 kHz, tăng mức âm lượng khi bản ghi nhỏ và thêm lượt thử nhận diện theo từng ngôn ngữ khi tự động phát hiện không có kết quả hữu ích.
- Căn lại hai cột menu/nội dung trên máy tính; giữ menu thu gọn trên điện thoại.
- Service worker đã thêm trang luyện số vào danh sách cache và đổi cache key để cập nhật bản v42 trên GitHub Pages.


CẬP NHẬT TINH CHỈNH V42 (30-10-2026, lần 2):
- Nút DANH MỤC CHỨC NĂNG trên điện thoại được tăng kích thước, độ tương phản và độ đậm để dễ nhìn, dễ bấm.
- Đổi tên menu thành LUYỆN VIẾT HÁN TỰ.
- Hai chế độ LUYỆN VIẾT VIỆT → TRUNG và LUYỆN VIẾT TRUNG → VIỆT chỉ dùng bộ từ vựng sơ cấp đã chọn lọc; bỏ các mục từ dài, mục từ giải thích vòng hoặc không phù hợp cho người mới.
- Bổ sung ba nút riêng: Đổi câu hỏi, Hiện đáp án, Kiểm tra đáp án. Nút Hiện đáp án không yêu cầu nhập câu và không tính vào thống kê đúng/sai.
- Trang LUYỆN SỐ TIẾNG TRUNG được nhúng trực tiếp vào index.html; không còn phụ thuộc đường dẫn luyen-so-tieng-trung.html nên không bị 404 nếu tệp con không được tải lên GitHub.
- DỊCH NHANH BẰNG GIỌNG NÓI dùng lại worker Whisper ổn định của phần phản xạ đọc, có nhận diện tự động và thử riêng tiếng Việt/tiếng Trung; thêm phương án dự phòng chạy trực tiếp trong trang nếu worker không hoạt động hoặc không trả chữ.
- Đổi cache service worker để người dùng nhận mã mới sau khi tải lên GitHub Pages.

CẬP NHẬT GITHUB PAGES:
Giải nén ZIP, mở đúng thư mục hoc-tieng-trung-bvt-v42 bên trong, sau đó tải TẤT CẢ tệp và thư mục trong đó lên cùng thư mục gốc đang chứa index.html trên GitHub. Không tải nguyên thư mục cha lồng thêm một cấp. Dù trang luyện số hiện đã được nhúng vào index.html, vẫn giữ các tệp còn lại như sw.js, asr-worker.js, ocr-worker.js, asr-voice-worker.js, manifest.webmanifest và các biểu tượng trong kho GitHub để ứng dụng đầy đủ chức năng.


CẬP NHẬT TINH CHỈNH V42 (30-10-2026, lần 3):
- Tăng nút DANH MỤC CHỨC NĂNG trên điện thoại lên 88 px chiều cao, chữ 24 px, viền và độ tương phản đậm hơn; máy nhỏ vẫn có cỡ riêng để không tràn màn hình.
- Nhúng nguyên trang Luyện Số Tiếng Trung V10 vào index.html dưới dạng srcdoc; khi mở menu, trang chạy từ nội dung nhúng, không yêu cầu đường dẫn trang con nên không bị 404. Tệp luyen-so-tieng-trung.html vẫn được giữ trong ZIP để tiện lưu trữ/đối chiếu.
- Bộ câu hỏi LUYỆN VIẾT VIỆT → TRUNG và LUYỆN VIẾT TRUNG → VIỆT chỉ lấy từ sơ cấp HSK1–2, ưu tiên nghĩa ngắn, loại mục từ dài/giải thích; có ba nút Đổi câu hỏi, Hiện đáp án, Kiểm tra đáp án.
- DỊCH NHANH BẰNG GIỌNG NÓI sử dụng cùng asr-worker.js đang dùng trong phản xạ đọc. Worker được bổ sung chế độ tự nhận diện và thử riêng tiếng Việt/tiếng Trung; phần phản xạ đọc vẫn gọi worker ở chế độ tiếng Trung như trước.
- Đồng nhất tuỳ chọn micro và MediaRecorder với phần phản xạ đọc; cho phép bản ghi ngắn từ 0,25 giây; đổi cache service worker để trình duyệt tải mã v42 mới.

CẬP NHẬT GITHUB PAGES LẦN 3:
1. Mở thư mục ZIP đã giải nén, chọn tất cả 12 tệp bên trong và tải trực tiếp lên thư mục gốc của repository đang có index.html. Không đưa nguyên thư mục hoc-tieng-trung-bvt-v42 thành thư mục con.
2. Trang Luyện Số đã được nhúng vào index.html, vì vậy menu vẫn mở kể cả khi GitHub Pages không có luyen-so-tieng-trung.html. Tuy nhiên, hãy giữ/tải toàn bộ tệp trong ZIP để các worker, OCR, từ điển và biểu tượng hoạt động đúng.
3. Sau khi GitHub báo cập nhật xong, mở lại website và tải mới hoàn toàn (trên máy tính Ctrl+F5; trên điện thoại đóng tab rồi mở lại). Nếu vẫn thấy bản cũ, xóa dữ liệu/cache riêng của website rồi mở lại.


CẬP NHẬT TINH CHỈNH V42 (30-10-2026, lần 4):
- Tăng nút DANH MỤC CHỨC NĂNG trên điện thoại lên 88 px chiều cao và 24 px cỡ chữ; trên màn hình nhỏ tự điều chỉnh để tránh tràn ngang.
- Đổi cơ chế mở LUYỆN SỐ TIẾNG TRUNG sang nội dung trang V10 nhúng trong index.html. Trang hoạt động trực tiếp trong iframe srcdoc, không yêu cầu tải tệp trang con theo đường dẫn nên tránh lỗi 404.
- Bộ luyện VIỆT → TRUNG và TRUNG → VIỆT giới hạn ở nhóm từ sơ cấp HSK1–2, tối đa 3 chữ Hán, nghĩa ngắn và Pinyin ngắn; chọn nghĩa đầu tiên thay vì chuỗi giải nghĩa dài.
- Thêm bảo đảm Đổi câu hỏi không lặp lại ngay câu vừa hỏi; Hiện đáp án hoạt động khi ô nhập còn trống, không cộng điểm; Kiểm tra đáp án vẫn hoạt động riêng. Ở chiều Trung → Việt, đáp án hiển thị thêm chữ Hán để người học đối chiếu.
- DỊCH NHANH BẰNG GIỌNG NÓI sử dụng cùng tệp asr-worker.js đang vận hành ở phần phản xạ đọc. Worker có thêm nhánh tự nhận diện Việt/Trung, còn phản xạ đọc vẫn giữ chế độ nhận diện tiếng Trung.
- Đồng nhất tuỳ chọn micro với phần phản xạ đọc và cho phép bản ghi ngắn từ 0,25 giây trước khi xử lý.
- Đổi cache service worker để trình duyệt tải mã mới, giữ nguyên nhãn phiên bản ứng dụng v42.

HƯỚNG DẪN CẬP NHẬT GITHUB PAGES: giải nén ZIP, mở thư mục chứa 12 tệp, chọn tất cả và tải trực tiếp vào thư mục gốc repository đang chứa index.html. Không tải thư mục cha thành thư mục con. Sau khi GitHub hoàn tất, đóng tab website rồi mở lại; trên máy tính có thể nhấn Ctrl+F5. Trang luyện số đã nằm ngay trong index.html, nhưng vẫn nên tải đủ tất cả worker, manifest và biểu tượng trong ZIP để ứng dụng đầy đủ.

CẬP NHẬT TINH CHỈNH V42 (lần 5):
- Nút DANH MỤC CHỨC NĂNG trên điện thoại được tăng độ nổi bật: chữ lớn, nút cao và tương phản rõ hơn nhãn menu; tự điều chỉnh trên màn hình rất nhỏ.
- Khắc phục nguyên nhân dễ gây lỗi 404 ở LUYỆN SỐ TIẾNG TRUNG: trang V10 được nhúng trực tiếp vào index.html và mở bằng srcdoc, không phụ thuộc tệp HTML con trên GitHub Pages.
- Đổi tên menu thành LUYỆN VIẾT HÁN TỰ.
- Hai bài luyện Việt → Trung và Trung → Việt chỉ dùng 158 từ sơ cấp HSK1–2, ưu tiên từ ngắn, nghĩa tiếng Việt ngắn; có ba nút Đổi câu hỏi, Hiện đáp án (không cần nhập) và Kiểm tra đáp án.
- Dịch nhanh bằng giọng nói dùng cùng asr-worker.js của phản xạ đọc; worker có chế độ tự nhận diện Việt/Trung, giữ nguyên chế độ tiếng Trung cho phản xạ đọc.
- Đổi cache service worker để tải bản v42 tinh chỉnh mới.

Cập nhật GitHub: giải nén ZIP, mở thư mục hoc-tieng-trung-bvt-v42, chọn toàn bộ tệp bên trong và tải trực tiếp lên thư mục gốc repository (nơi đang có index.html). Để chắc chắn không sót worker, hãy tải đủ cả 12 tệp. Sau đó chờ GitHub Pages hoàn tất, nhấn Ctrl+F5 trên máy tính hoặc đóng tab và mở lại trên điện thoại.


CAP NHAT V42 - 30/10/2026
- Phan xa doc theo va hoi-dap: tu dong phat am lai moi khi chuyen sang cau tiep theo.
- Nut DANH MUC CHUC NANG tren dien thoai duoc thu gon con khoang mot nua kich thuoc truoc do.
- DICH NHANH BANG GIONG NOI: them nut loa cho noi dung nhan dien va ket qua dich; doi chieu nhieu phuong an Whisper (tu dong, tieng Viet, tieng Trung) de chon ket qua phu hop hon.
- DICH NHANH VIET-TRUNG: them khu vuc dan ca doan van ban va tai tep, moi khu vuc co nut dich ra tieng Trung va tieng Viet.
- Tep ho tro: TXT, MD, CSV, DOCX. PDF chua ho tro. Dich van ban can ket noi Internet.
- Menu NHAN DIEN ANH la ten rut gon cua chuc nang nhan dien chu Han tu hinh anh.


CẬP NHẬT GIAO DIỆN TỪ ĐIỂN — 30/10/2026
- Đổi tên mục thành “NHẬN DIỆN CHỮ HÁN BẰNG HÌNH ẢNH”.
- Thu gọn thẻ từ điển: chữ Hán, Pinyin và nghĩa trên hàng đầu; bốn nút nghe, thêm vào ghép câu, xem thứ tự nét và liên kết từ vựng nằm ngang hàng thứ hai.
- Bổ sung điều hướng trang ở cả phía trên và phía dưới danh sách từ.
- Nút “Liên kết từ vựng” hiển thị các mục có chung chữ Hán (đối với từ đơn) và/hoặc nghĩa tiếng Việt liên quan; bấm vào một mục liên quan sẽ đưa mục đó vào ô tra cứu từ điển.


CAP NHAT GIAO DIEN v42 - 30/10/2026 (TOI UU THEO Y KIEN NGUOI DUNG)
- Rà soát ghi chú nhỏ: lược bỏ hướng dẫn lặp lại hoặc không cần thiết; giữ các lưu ý quan trọng về quyền micro, Internet, xử lý âm thanh trên thiết bị, định dạng tệp, lưu dữ liệu, nguồn dữ liệu và giới hạn sử dụng.
- Ghép câu: mỗi thẻ câu hiển thị chữ Hán, Pinyin và nghĩa tiếng Việt trên cùng một hàng; bỏ dòng liệt kê từ đã dùng và ghi chú lọc mẫu.
- Giữ ba thao tác luyện viết, luyện dịch và luyện đọc dưới mỗi câu, đồng thời thu nhỏ nút để giảm chiều cao thẻ.
- Thêm nút mũi tên nổi ở góc dưới bên phải; bấm để cuộn về đầu trang.
- Giữ nguyên mã phiên bản ứng dụng v42; cập nhật tên bộ nhớ đệm Service Worker để thiết bị tải giao diện mới.
