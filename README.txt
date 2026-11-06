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


CẬP NHẬT V42 — 30/10/2026
- Bổ sung nút Sao chép và Đọc kết quả cho phần dịch cả đoạn văn bản và phần dịch tệp đính kèm.
- Giọng đọc tự chọn tiếng Trung hoặc tiếng Việt theo ngôn ngữ đích của bản dịch.


BIG UPDATE V42.1 – LUYỆN TẬP TỪ VỰNG (31/10/2026)
- Thêm menu LUYỆN TẬP TỪ VỰNG. Nguồn từ vựng gồm: người dùng tự chọn từ điển, từ đã nhận diện/tách từ bằng chức năng quét ảnh, và các từ đã chọn trong menu Ghép câu luyện phản xạ. Có thể gộp nhiều nguồn; ứng dụng tự loại từ trùng theo chữ Hán.
- Bốn chế độ: AI đọc tiếng Việt – người học trả lời tiếng Trung; AI đọc tiếng Trung – người học trả lời tiếng Việt; hiện nghĩa tiếng Việt – trả lời tiếng Trung; hiện chữ Hán – trả lời tiếng Việt.
- Người học có thể nhập câu trả lời hoặc dùng micro (khi trình duyệt hỗ trợ). Có thể cài thời gian tự hiện đáp án và thời gian tự chuyển sang từ tiếp theo. Khi hiện đáp án, ứng dụng luôn phát âm theo ngôn ngữ đáp án.
- Mỗi lượt xáo trộn ngẫu nhiên danh sách và mỗi từ chỉ xuất hiện một lần; hết danh sách sẽ dừng, không tự lặp từ. Bấm BẮT ĐẦU LUYỆN TẬP để tạo lượt mới và xáo trộn lại.
- Micro cần quyền truy cập và khả năng nhận diện giọng nói của trình duyệt; giọng đọc dùng Speech Synthesis có sẵn trên thiết bị.


BIG UPDATE V42.2 – SỬA THU ÂM VÀ PHẢN HỒI LUYỆN TỪ VỰNG (31/10/2026)
- Biểu tượng menu Luyện tập từ vựng dùng hình quyển sách, phù hợp nội dung ôn từ.
- Sửa micro luyện từ vựng: sử dụng MediaRecorder và bộ nhận diện Whisper chạy trên thiết bị; mỗi lần thu âm tạo phiên nhận diện riêng, có thể ghi âm nhiều lượt liên tiếp.
- Nhận diện đúng ngôn ngữ trả lời: tiếng Trung khi cần trả lời chữ Hán, tiếng Việt khi cần trả lời nghĩa tiếng Việt.
- Hiển thị rõ CHÍNH XÁC / CHƯA CHÍNH XÁC khi người học nhập hoặc thu âm có kết quả. Khi không có câu trả lời, ứng dụng tiếp tục bộ đếm và tự hiện đáp án theo thời gian cài đặt.
- Cả bốn chế độ đều phát âm câu hỏi và phát âm đáp án theo ngôn ngữ tương ứng.
- Cần cấp quyền micro và mở ứng dụng bằng HTTPS. Lần đầu sử dụng nhận diện cần Internet để tải mô hình; các lần sau có thể dùng lại mô hình đã lưu trong bộ nhớ đệm trình duyệt.


BIG UPDATE V42.3 – GỘP LUYỆN TẬP TỪ VỰNG THÀNH 2 HƯỚNG (31/10/2026)
- Thay biểu tượng menu Luyện tập từ vựng bằng ký hiệu thẻ từ có chữ 词, phân biệt với biểu tượng quyển sách của Từ điển.
- Gộp bốn lựa chọn cũ thành hai hướng luyện tập: (1) AI hiển thị và phát âm nghĩa tiếng Việt, người học trả lời tiếng Trung; (2) AI hiển thị và phát âm chữ Hán tiếng Trung, người học trả lời tiếng Việt.
- Mỗi câu hỏi được hiển thị trên màn hình và phát âm; khi hiện đáp án, đáp án cũng được phát âm theo ngôn ngữ đích. Giữ nguyên nhập bàn phím, thu âm, chấm CHÍNH XÁC/CHƯA CHÍNH XÁC, bộ hẹn giờ và quy tắc xáo trộn không lặp từ.
- Giữ nguyên ba nguồn nạp từ vựng: tự chọn từ điển, từ đã nhận diện từ ảnh và từ đã chọn ở Ghép câu luyện phản xạ.
- Đổi cache Service Worker sang mã V42.3 để tải giao diện mới.


V42.4: menu 214 bo thu Kangxi (so thu tu, pinyin, nghia goi y, so net, loc va hoat anh Hanzi Writer); nut sao chep rieng cho Hanzi/Pinyin/nghia Viet o cac khu vuc tu vung va cau; mau nhan dien rieng theo chuc nang.


V42.4: menu 214 bo thu Kangxi (so thu tu, pinyin, nghia goi y, so net, loc va hoat anh Hanzi Writer); nut sao chep rieng cho Hanzi/Pinyin/nghia Viet o cac khu vuc tu vung va cau; mau nhan dien rieng theo chuc nang.


CAP NHAT GIAO DIEN V42.4 (05/11/2026): Sua tuong phan nut hien dap an va cac nut che do; bo cac nut sao chep trong danh sach tu lien ket; dua nut sao chep nghia tieng Viet ve dau dong nghia trong tu dien; can giua tieu de tren thanh do o may tinh; danh so 1-12 va to mau 12 muc menu theo mau chuc nang.


V42.4 – cập nhật biểu tượng cờ, tra bộ thủ theo từng chữ và căn chỉnh nút sao chép (05/11/2026):
- Logo chữ Hán cũ được thay bằng quốc kỳ Việt Nam và Trung Quốc trong khung nền trắng; màu cờ được giữ nguyên.
- Bộ thủ trong từng chữ Hán được tra bằng trường radical của dữ liệu Make Me a Hanzi (khoảng hơn 9.000 ký tự), tải khi người dùng mở chức năng lần đầu và lưu bộ tra cứu trên thiết bị. Nếu không có bản ghi, ứng dụng báo chưa có dữ liệu thay vì gán bộ thủ theo suy đoán.
- Nguồn dữ liệu cấu trúc chữ: https://github.com/skishore/makemeahanzi (dictionary.txt; giấy phép của dữ liệu từ điển theo LGPL-3.0-or-later; vui lòng xem tệp giấy phép gốc tại kho dự án).
- Bộ thủ 金 là bộ số 167, dạng chuẩn có 8 nét; dạng giản thể đứng bên trái 钅 có 5 nét. Bộ lọc 5 nét cũng hiển thị biến thể này.
- Các biểu tượng trong danh sách bộ thủ là hình gợi nhớ trực quan, không phải bản vẽ khảo cổ về nguồn gốc chữ.


TINH CHỈNH TRA BỘ THỦ V42.4 (05/11/2026):
- Bổ sung từ khóa tiếng Việt 'kim' và các dạng 金 / 釒 / 钅 vào tra cứu bộ thủ; khi lọc 5 nét, biến thể giản thể 钅 cũng xuất hiện dưới bộ chuẩn #167 金. 金 chuẩn có 8 nét, 钅 có 5 nét.
- Bổ sung biểu tượng gợi nhớ trực quan cho thêm nhiều bộ thủ. Với các bộ trừu tượng/hiếm, ký tự bộ thủ và hoạt ảnh thứ tự nét vẫn là hình tham chiếu chính; biểu tượng không phải hình minh họa nguồn gốc chữ.
- Dữ liệu phân loại theo từng ký tự lấy từ Make Me a Hanzi dictionary.txt, trường radical; dữ liệu này bao phủ hơn 9.000 ký tự thông dụng. dictionary.txt được phân phối theo LGPL-3.0-or-later theo tệp COPYING của dự án gốc.


TINH CHỈNH GIAO DIỆN V42.4.3 (05/11/2026):
- Bỏ nút Bộ thủ riêng cạnh Liên kết từ vựng trong từng thẻ từ điển. Phân tích bộ thủ vẫn được hiển thị trong cửa sổ xem thứ tự nét của chữ Hán.
- Khi mở bộ thủ từ phần phân tích trong cửa sổ thứ tự nét, có nút quay lại đúng chữ Hán và đúng từ đang tra cứu.
- Đánh số 1–12 ngay trên tiêu đề khu vực chức năng; các chế độ luyện Việt→Trung, Trung→Việt, Luyện viết Hán tự và Luyện đọc lần lượt thể hiện số 5–8.
- Thu gọn nút menu trên điện thoại, giảm khoảng cách và kích thước nhãn để 12 mục có thể hiện đầy đủ khi mở danh mục; giới hạn chiều cao menu theo phần màn hình còn lại.


TINH CHINH THU TU NET VA HINH GOI NHO BO THU V42.4 (05/11/2026):
- Hoat anh chu mau trong cua so thu tu net tu dien va phan luyen viet tu dong lap lai sau moi vong, nghi 3 giay; phan hoat anh 214 bo thu cung tu dong lap lai sau 3 giay.
- Nut Chay lai/Xem lai giu nguyen nhan, bam vao se dat lai chu hien tai va phat lai tu net dau tien.
- Thay emoji phu thuoc font bang 214 hinh goi nho SVG vector, cung mau net va nen, hien thi dong bo tren may tinh va dien thoai. Hinh la meo ghi nho truc quan, khong phai minh hoa tu nguyen.
- Service Worker doi ma cache de trinh duyet nhan ban cap nhat.


CAP NHAT V42.4 – AM THANH, KHO TAI LIEU VA MINH HOA 214 BO THU (05/11/2026):
- Menu 4: co nut sao chep rieng noi dung nhan dien; cap nhat Whisper Base da ngon ngu cho nhan dien tieng Viet/Trung.
- Menu 5 va 6: nut loa phat am noi dung cau hoi, dap an tieng Trung va nghia tieng Viet.
- Menu 8: ghi am bang MediaRecorder va nhan dien tieng Trung bang Whisper Base, khong phu thuoc SpeechRecognition tich hop cua trinh duyet. Lan dau can Internet tai mo hinh, sau do duoc cache tren trinh duyet.
- Menu 13 TAI LIEU CUA BAN: luu anh va van ban bang IndexedDB tren trinh duyet; ho tro xem, tim kiem, tai xuong, xoa, xuat/nhap ban sao luu JSON de chuyen thiet bi. Khong dong bo dam may tu dong.
- Danh sach 214 bo thu: bo sung nghia goi y tieng Viet va 214 minh hoa SVG rieng theo tung so bo thu; hinh la cong cu ghi nho su pham, khong phai hinh giai thich nguon goc tu nguyen cua moi chu.
- Luu y: nhan dien giong noi phu thuoc chat luong micro, tieng on va giong doc; TTS phu thuoc giong doc co tren thiet bi.


CAP NHAT V42.4 - SUA HOAT ANH BO THU (05/11/2026)
- Bo sung lai ham tai hoat anh thu tu net bo thu (ban truoc con loi goi ham nhung thieu dinh nghia).
- Khi chon mot bo thu, mo hop thoai noi (modal) hien thi hinh goi nho, y nghia, so net va hoat anh; khong can cuon xuong cuoi danh sach.
- Hoat anh tu lap sau moi luot, nghi 3 giay; nut Xem lai thu tu net dat trong modal va chay lai tu net dau tien.
- Nut quay lai chu dang tra van duoc hien trong modal khi mo tu cua so thu tu net cua tu dien.


CAP NHAT V42.4 - SUA HOAT ANH BO THU (05/11/2026)
- Bo sung lai ham tai hoat anh thu tu net bo thu (ban truoc con loi goi ham nhung thieu dinh nghia).
- Khi chon mot bo thu, mo hop thoai noi (modal) hien thi hinh goi nho, y nghia, so net va hoat anh; khong can cuon xuong cuoi danh sach.
- Hoat anh tu lap sau moi luot, nghi 3 giay; nut Xem lai thu tu net dat trong modal va chay lai tu net dau tien.
- Nut quay lai chu dang tra van duoc hien trong modal khi mo tu cua so thu tu net cua tu dien.


CAP NHAT V42.4 - SUA HOAT ANH BO THU (05/11/2026)
- Bo sung lai ham tai hoat anh thu tu net bo thu (ban truoc con loi goi ham nhung thieu dinh nghia).
- Khi chon mot bo thu, mo hop thoai noi (modal) hien thi hinh goi nho, y nghia, so net va hoat anh; khong can cuon xuong cuoi danh sach.
- Hoat anh tu lap sau moi luot, nghi 3 giay; nut Xem lai thu tu net dat trong modal va chay lai tu net dau tien.
- Nut quay lai chu dang tra van duoc hien trong modal khi mo tu cua so thu tu net cua tu dien.


V42.4.6 - 13 MENU COLORS + RADICAL / IDS COMPONENT ANALYSIS
- 13 menu colors are now distinct and use white labels with high contrast.
- Character analysis combines the official radical field with Make Me a Hanzi IDS decomposition and semantic/phonetic components.
- Silver 银 / 銀 should show the primary metal radical 金 (#167) plus 艮 (#138) as a phonetic component.
- Results are precomputed and cached per character when the Make Me a Hanzi dictionary map is loaded.
- The cache key was bumped to v2 to avoid stale radical-only entries.
- Service worker cache version updated.

V42.4.6 - DISTINCT 13-COLOR IDENTITY + CHARACTER COMPONENT ANALYSIS
- Replaced menu colors with 13 distinct color identities; all have readable white-text contrast. The selected function content uses the corresponding accent color as well.
- Character-to-radical analysis now cross-checks the Make Me a Hanzi fields: radical, IDS decomposition, semantic component, phonetic component, and hint.
- IDS decomposition leaves are compared with the 214 Kangxi radical list and known positional variants. The official primary radical is presented separately from additional visible components that happen to match a Kangxi radical.
- Example: 银 = primary 金 (#167; written as 钅) + phonetic component 艮 (#138). 銀 gives the same component result using 釒. 行 = primary 行 (#144) + recognized component 彳 (#60).
- On first analysis, the browser downloads the Make Me a Hanzi character metadata (about 9,000 common characters), builds the character result index, and caches the source map in local storage. Internet is required for the first download; the local fallback includes the 银/銀/行 examples.
- Cache key and service-worker shell version were bumped so old radical-only cache entries cannot hide the new decomposition data.

============================================================
V42.5 – TURNSTILE, CLOUDFLARE ASR MAC DINH, FALLBACK CUC BO
============================================================
- Menu 4, 8 va 9 uu tien Whisper Large V3 Turbo qua Worker bvt-asr.
- Neu Cloudflare/Turnstile khong tai duoc, xac minh that bai, Worker loi hoac het thoi gian, app tu chuyen sang nhan dien cuc bo tren thiet bi.
- Khong con muc cau hinh URL/ma truy cap thu cong. Endpoint va Turnstile Site Key cong khai duoc dat san trong index.html.
- Menu 8 an nut loa canh cau hoi; nut Nghe mau rieng van duoc giu.
- Giam dong huong dan lap lai trong menu 4 va menu 8; chi hien thong bao trang thai khi thao tac.
- Worker dung Turnstile Siteverify de xac minh moi yeu cau nhan dien. Secret Key chi nam trong Cloudflare Worker, khong nam trong GitHub Pages.
- Worker gioi han moi tep am thanh toi da 15 MB.

BAT BUOC CAP NHAT WORKER TRUOC KHI DANG APP V42.5
-------------------------------------------------
1. Mo Cloudflare Dashboard > Workers & Pages > bvt-asr > Edit code.
2. Thay toan bo ma cu bang tep asr-cloudflare-worker.js trong goi V42.5, sau do Save and Deploy.
3. Giu Workers AI binding ten chinh xac la AI.
4. Trong Settings > Variables and Secrets, them Secret ten TURNSTILE_SECRET_KEY va dan Secret Key cua widget Turnstile (khong phai Site Key).
5. Giu variable ALLOWED_ORIGIN = https://buivanthanh227-png.github.io.
6. Xoa Secret ASR_SHARED_SECRET cu neu con; ban V42.5 khong su dung Bearer password nua.
7. Deploy lai Worker. Mo dia chi workers.dev de kiem tra JSON health co protection: Cloudflare Turnstile.
8. Sau do moi tai len GitHub Pages toan bo tep trong goi V42.5.

TURNSTILE DA DUOC NHUNG SAN TRONG APP
-------------------------------------
- Site Key cong khai da duoc dat san trong index.html: 0x4AAAAAAF0xjE9j2xA4Ndkm.
- Hostname duoc phep: buivanthanh227-png.github.io.
- Action duoc kiem tra tren Worker: bvt_asr.
- Nguoi hoc khong can nhap URL, Site Key hoac mat khau. Turnstile chay tu dong khi can nhan dien; trong truong hop Cloudflare yeu cau tuong tac, nguoi hoc co the thay buoc xac minh nho.
- Site Key la khoa cong khai. Tuyet doi khong dua Turnstile Secret Key vao index.html, README cong khai hoac GitHub.
- Token Turnstile duoc tao moi cho tung lan gui am thanh va duoc xac minh phia Worker qua Siteverify. Token co thoi han 5 phut va chi su dung duoc mot lan.

KHI CO LOI
-----------
- Thieu TURNSTILE_SECRET_KEY: Worker tra ve HTTP 500; them Secret tren Worker va Deploy lai.
- Token khong hop le/het han/da su dung: Worker tra ve HTTP 401; app tu chuyen sang nhan dien cuc bo.
- Sai hostname hoac action: Worker tu choi yeu cau; kiem tra widget Turnstile dang cho phep buivanthanh227-png.github.io va action bvt_asr.
- Thieu AI binding: them Workers AI binding ten AI.
- Worker/Turnstile khong truy cap duoc: app tu chuyen sang Whisper Base cuc bo neu trinh duyet tai duoc model.

CAP NHAT GITHUB PAGES
---------------------
1. Giai nen ZIP.
2. Chon tat ca tep trong goi va tai truc tiep vao thu muc goc repository dang chua index.html; khong tao them thu muc long.
3. Doi GitHub Pages cap nhat xong. Tren may tinh nhan Ctrl+F5; tren dien thoai dong tab va mo lai.
4. Worker Cloudflare la tep rieng, phai Deploy theo huong dan phia tren; tai tep Worker len GitHub khong lam Worker tu cap nhat.

GHI CHU QUYEN RIENG TU VA CHI PHI
---------------------------------
- Am thanh duoc gui toi Cloudflare de nhan dang khi dich vu san sang. Neu Cloudflare/Turnstile loi, app thu nhan dang cuc bo tren thiet bi.
- Turnstile giam yeu cau tu dong va khong cong khai khoa bi mat; no khong thay the hoan toan gioi han tan suat. Nen theo doi Workers AI usage va cau hinh rate limiting neu luong nguoi dung tang.
- Workers AI Free cap 10.000 Neurons/ngay theo chinh sach tai khoan; muc tieu thu cu the co the thay doi. Kiem tra bang gia Cloudflare hien hanh truoc khi dua vao su dung cong khai quy mo lon.


CAP NHAT V42.5.1 – BANG MAU 13 MENU VA DONG BO NHAN DIEN
--------------------------------------------------------
1. Doi 13 mau menu theo bang mau pastel nguoi dung cung cap:
   1 Soft Teal #4DB6AC; 2 Warm Amber #FFB74D; 3 Lavender Purple #BA68C8;
   4 Sky Blue #64B5F6; 5 Coral Peach #FF8A65; 6 Mint Green #81C784;
   7 Rose Pink #F06292; 8 Slate Blue #7986CB; 9 Lime Chartreuse #D4E157;
   10 Warm Sienna #A1887F; 11 Cyan Breeze #4DD0E1;
   12 Orchid Violet #9575CD; 13 Cool Grey #90A4AE.
   Banner, menu dang chon va vung chuc nang ben phai dung cung mau theo menu.
   Chu mau toi tren nen pastel de dam bao de doc.
2. Menu 8, 9 va 10 thong nhat luong MediaRecorder -> Cloudflare Whisper Large V3 Turbo ->
   Whisper Base cuc bo neu Cloudflare that bai. Menu 9 dung nut ghi am noi dong, khong mo
   hop thoai micro do cu. Menu 10 uu tien Cloudflare truoc khi fallback cuc bo.
3. Sua phat am ket qua dich menu 4: ca doan dich duoc dua vao mot SpeechSynthesisUtterance
   de tranh chi doc cau dau trong doan nhieu cau.
4. Lam moi ma cache Service Worker. Worker Cloudflare khong thay doi; khong can Deploy lai
   Worker neu dang dung dung ban Turnstile cua V42.5. Chi can cap nhat 13 tep GitHub Pages.
5. Da kiem tra cu phap JS, manifest, ID HTML, bang mau va tinh toan ven ZIP.


CAP NHAT V42.5.2 – LOA DAP AN, TEN NUT NET VE VA CAN GIUA MENU
----------------------------------------------------------------
1. Menu 5 va 6: khi hien dap an mau hoac kiem tra dap an, them nut loa cho dap an,
   chu Han va nghia tieng Viet. O chieu Trung -> Viet, lay chu Han tu cau/tu dang luyen
   de phat am rieng, khong chi phat am phan nghia tieng Viet.
2. Thong nhat nhan nut xem lai net thanh “Chay lai tu dau thu tu net” tren cac khu vuc
   luyen viet, tu dien va bo thu.
3. Menu 10: bo chu 词 khoi tieu de ben phai “LUYEN TAP TU VUNG”; giu bieu tuong o menu trai.
4. Menu 3: bieu tuong 文 ⇄ A nam ngang.
5. Ca 13 menu trai co chieu cao dong nhat theo tung breakpoint, so thu tu nam ben trai,
   nhom bieu tuong + ten nam giua chieu ngang, tang co chu va can giua ten menu.
6. Doi ma cache Service Worker. Worker Cloudflare khong thay doi.


V42.5.3 – FIX BỐ CỤC MENU DESKTOP/TABLET (2026-11-06)
- Mở rộng cột điều hướng trên desktop/tablet (258–300px tùy chiều rộng màn hình).
- Tên menu được phép xuống dòng tự nhiên, từng hàng tự tăng chiều cao; không còn cố định chiều cao 56px gây chồng chữ.
- Giữ nguyên bố cục menu dạng thu gọn của điện thoại (<=700px).
- Cập nhật Service Worker cache để trình duyệt nhận bản mới.


CẬP NHẬT V42.5.4 (06-11-2026)
- Sửa bố cục menu 4 trên desktop/tablet: thẻ chức năng căn theo lề trái của cột nội dung, không còn bị thu hẹp rồi căn giữa làm cụm điều khiển lệch xa thanh menu.
- Đồng bộ menu 8 và menu 9 với menu 4: dùng cùng MediaRecorder và cấu hình micro, gửi cùng yêu cầu Whisper Large V3 Turbo với language=auto để mô hình tự nhận diện, không ép riêng zh/initial_prompt.
- Bỏ tự dừng 25 giây ở menu 8 và 20 giây ở menu 9; người dùng chủ động dừng như menu 4, tránh cắt mất câu nói.
- Phân biệt rõ kết quả nhận diện qua Cloudflare và kết quả dự phòng Whisper Base cục bộ để người dùng biết nguồn của kết quả.
- Service Worker đổi cache key để trình duyệt tải V42.5.4.

Cập nhật: giải nén và tải ghi đè toàn bộ 13 tệp vào thư mục gốc GitHub Pages. Không cần Deploy lại Cloudflare Worker vì mã Worker và cấu hình Turnstile không thay đổi.
