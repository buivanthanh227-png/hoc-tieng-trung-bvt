HOC TIENG TRUNG BVT - PHIEN BAN V42.9

V42.9 - CAI THIEN MENU 16 VA ON TAP SAU LUYEN NGHE

- So menu 16 nam tren o dem xam nhat giong 15 menu con lai; huy hieu duoc ep mau ca khi menu dang chon.
- Bieu tuong loa trong dong huong dan 16.1 chi la hinh minh hoa, khong phat am thanh khi bam.
- 16.1 doi nhan 4 nut thanh thanh dieu so 1, 2, 3, 4; them nut loa mau va loi nhac bam vao o de nghe am thanh.
- Cac truong nhap thoi gian o menu Luyen so (menu 11), menu 10, 16.2 va 16.3 co nut mui ten tang/giam ngay trong o nhap.
- Hai truong SO CAU MOI LUOT o 16.2 va 16.3 cung co nut mui ten tang/giam, tu gioi han 1-500 cau.
- 16.2 va 16.3: phat lai am thanh khong dat lai dong ho; dong ho tiep tuc dem theo moc ban dau.
- Them tam dung/tiep tuc va huy bo luyen tap cho ca hai bai 16.2 va 16.3. Thoi gian tam dung duoc loai khoi thoi gian hoan thanh.
- Tang kich thuoc va do tuong phan thong tin dap an; tang thoi gian mac dinh truoc khi chuyen cau tiep theo len 5 giay.
- Ket thuc bai, hien tong ket tung cau: dap an nguoi hoc chon va dap an dung cua ung dung; moi cau co nut nghe lai am thanh cau hoi.
- Giu nguyen du lieu tu dien, ASR/OCR, bang Pinyin 23 x 36 / 391 am tiet va bo ghi am audio-cmn.

CAP NHAT GITHUB PAGES
- PATCH_GITHUB_4_TEP.zip: giai nen va ghi de index.html, luyen-so-tieng-trung.html, manifest.webmanifest, sw.js vao thu muc goc repository, sau do Commit changes.
- FULL_14_TEP.zip: goi day du 14 tep ung dung.
- Sau khi deploy: PC nhan Ctrl+F5; dien thoai/may tinh bang dong tab/app roi mo lai de Service Worker cap nhat.

V42.9 - Bo sung o phat am toan hang/toan cot trong bang Pinyin 16.1; thu gon bon thanh cuon.


CAP NHAT v42.9 - MENU 16.1
- Bo nhan chu Han "声母 / 韵母" khoi goc bang.
- Gop hai cot dau va hai hang tieu de thanh mot o cheo: VẬN MẪU / THANH MẪU.
- Cot thanh mau co do rong 39px, bang moi cot van mau.
- Khi cuon ngang, cot nut loa va cot thanh mau duoc giu co dinh.
- Khi cuon doc, hang nut doc van mau va hang ten van mau duoc giu co dinh.
- Dong bo phien ban ung dung, manifest va Service Worker cache v42.9.


V42.9 - Dieu chinh vi tri hai nhan tren o goc cheo bang Pinyin 16.1; dua VẬN MẪU va THANH MẪU vao tron ven hai nua tam giac, khong de duong cheo de len chu.

V42.9 FIX - Chinh lai dung huong o cheo: VẬN MẪU nam tron trong nua tam giac tren-trai; THANH MẪU nam tron trong nua tam giac doi dien phia duoi-phai. Duong cheo di tu goc tren-phai xuong goc duoi-trai, khong cat qua chu.
- Tu dong do do rong tung cot van mau theo am tiet dai nhat trong cot va ca bon thanh dieu; cac cot ngan giu toi thieu 39px, cot uang duoc mo rong de chua tron cac am tiet zhuāng, chuāng, shuāng.
- Giu nguyen so phien ban v42.9; chi thay ma cache noi bo cua Service Worker de trinh duyet tai lai index.html da sua.


V42.9 - MENU 17: THU THACH NHO MAT CHU HAN (DIEU CHINH GIAO DIEN VA LOGIC).
- Bo dong chu gioi thieu tieng Anh; danh so hai phan 17.1 va 17.2.
- Mau menu trai va panel phai dong bo cung he hong; ba muc Do/Kho/Rat kho dung ba sac hong tu nhat den dam.
- Doi ten nguon menu 10 thanh BO TU VUNG (MENU 10).
- O tim tu hien danh sach goi y truc tiep khi nguoi dung nhap, khong can bam nut Tim tu.
- Mac dinh 5 tu, 5 giay quan sat, 5 luot va 5 giay xem dap an; cac o so co mui ten tang/giam.
- Bo lua chon dap an; chi giu nhap chu Han va thu am. Them nut Bo qua cau nay de khong bi ket o mot cau.
- Them dong ho xem dap an; het thoi gian se tu dong chuyen cau tiep theo.
- Tang kich thuoc chu dap an va chu trong bang tong ket; thu hep khoang cach cac chu tren bang thu thach.
- Service Worker doi ma cache de trinh duyet tai ban index.html moi; giu so phien ban v42.9.


MENU 17 – BẢN TINH CHỈNH TIẾP THEO (GIỮ PHIÊN BẢN ỨNG DỤNG v42.9)
- Đã bỏ hai dòng mô tả dưới tiêu đề, biểu tượng chữ 记忆 và nút lấy từ riêng từ điển menu 1. Ô tìm kiếm trong menu 17 vẫn tra trực tiếp từ điển và hiện gợi ý khi nhập.
- Bảng chữ hiển thị theo vị trí rải ngẫu nhiên trong vùng chơi; thuật toán đo kích thước từng chữ và tránh chồng lấn, tự mở rộng vùng chơi khi cần.
- Ở mức KHÓ và RẤT KHÓ, chữ thay đổi cả màu, font và vị trí; bổ sung các lựa chọn font chữ giản thể như SimHei, FangSong, DengXian và Noto Sans SC bên cạnh các font hiện có.
- Giảm cỡ chữ trên bảng; ô nhập chữ Hán có cùng chiều rộng với nút thu âm; nút BỎ QUA CÂU NÀY và KẾT THÚC SỚM được tăng kích thước, tô màu nổi bật.
- Ba chỉ số lượt chơi, trạng thái ẩn chữ và điểm đúng được tăng cỡ đồng đều.


BẢN TINH CHỈNH MENU 17 (SPATIAL V3)
- Tên menu 17 ở thanh bên trái hiển thị màu đen giống các tên menu khác.
- Hai trường THỜI GIAN QUAN SÁT và THỜI GIAN XEM ĐÁP ÁN có nút ▲/▼ tăng giảm số giây theo cùng kiểu điều khiển ở menu 16.2/16.3.
- Giữ nguyên số phiên bản công khai v42.9; đổi cache service worker để trình duyệt nhận bản cập nhật.


BẢN TINH CHỈNH MENU 17 (SPATIAL V4)
- Bổ sung cụm nút tăng/giảm ▲ / ▼ cho ô SỐ TỪ XUẤT HIỆN (2–30) và SỐ LƯỢT CHƠI (1–50), cùng kiểu điều khiển với menu 16.2/16.3.
- Nút tăng/giảm thay đổi mỗi lần 1 đơn vị, tự tuân thủ giới hạn min/max và phát sự kiện input/change để đồng bộ logic hiện có.
- Giữ nguyên phiên bản ứng dụng v42.9; cập nhật tên cache để trình duyệt tải lại bản mới.


BẢN TINH CHỈNH MENU 17 (FONT RANDOM V5)
- Ở chế độ KHÓ và RẤT KHÓ, từng chữ trên bảng được chọn font ngẫu nhiên độc lập trong bộ font CJK mở rộng.
- Khi một chữ biến mất, tất cả chữ còn lại đều được chọn lại font khác với font ngay trước đó, đồng thời đổi màu và được bố trí lại vị trí ngẫu nhiên, không chỉ đổi màu.
- RẤT KHÓ bổ sung biến thiên độ đậm, kiểu nghiêng và khoảng cách ký tự để tăng khác biệt thị giác.
- Chế độ DỄ giữ nguyên font và màu đen. Giữ nguyên số phiên bản ứng dụng v42.9; cập nhật cache service worker sang V5.


V42.9.1 – QA FIX (15/11/2026)

Bản nền: HOC_TIENG_TRUNG_BVT_v42_9_FULL_MENU17_FONT_RANDOM_V5.zip. Giữ nguyên toàn bộ cấu trúc ứng dụng, dữ liệu từ điển nhúng, menu 1–17 và cải tiến Menu 17 Random V5.

Đã xử lý 16 phát hiện trong báo cáo bang-chung-qa.zip:
- BVT-01: xử lý CSV theo cột dữ liệu, giữ tiêu đề và dữ liệu đích đã có; không đưa dòng tiêu đề vào dịch như văn bản thường.
- BVT-02: hoàn tất chấm thứ tự nét ở Menu 7 được ghi vào thống kê luyện tập dùng chung.
- BVT-03: câu trả lời hỏi–đáp đổi ngôi người nói/người nghe (你 ↔ 我).
- BVT-04: kết quả tìm chữ ở Menu 7 có bố cục riêng cho Hán tự, Pinyin, nghĩa và nút thao tác; nội dung dài được xuống dòng trên màn hình hẹp.
- BVT-05: bổ sung nhận diện cặp nghĩa tương đương đã kiểm thử chè ↔ trà khi chấm Menu 6.
- BVT-06: Menu 17 sắp xếp lại vị trí các chữ đang hiển thị khi đổi kích thước màn hình; không khởi động lại lượt hoặc đồng hồ.
- BVT-07: mục từ 鱼/魚 được bổ sung nghĩa thông dụng “cá”, đồng thời giữ nghĩa họ Yu nếu có.
- BVT-08: lỗi nhập JSON hỏng hiển thị thông báo tiếng Việt dễ hiểu; không đưa lỗi parser tiếng Anh ra giao diện.
- BVT-09: chỉ dùng câu mẫu offline khi toàn bộ Pinyin khớp; “ni hao” không bị mở rộng thành “ni hao ma”.
- BVT-10: không sao chép placeholder hoặc trạng thái đang dịch như thể đó là bản dịch thật.
- BVT-11: bộ đếm ảnh Menu 14 cập nhật sau thao tác xóa từng ảnh.
- BVT-12: hai ô thời gian Menu 10 tự chuẩn hóa giá trị theo giới hạn đang dùng (hiện đáp án 1–120 giây; chuyển từ 0–60 giây).
- BVT-13: truy vấn emoji/không có ký tự tìm kiếm hợp lệ trong Menu 12 trả 0 kết quả, không trả toàn bộ bộ thủ.
- BVT-14: truy vấn emoji/không có ký tự tìm kiếm hợp lệ trong từ điển trả 0 kết quả, không hiển thị toàn bộ từ điển.
- BVT-15: đổi ngôn ngữ nguồn khi Menu 15 đang ghi âm không làm trạng thái chuyển sai thành “Sẵn sàng”.
- BVT-16: kết quả OCR “No text detected” được coi là không có văn bản; không đưa thông báo kỹ thuật sang bước dịch.

Kiểm tra kỹ thuật đã thực hiện trong gói này:
- Kiểm tra cú pháp tất cả script JavaScript nội tuyến bằng Node.js.
- Kiểm tra JSON của manifest.webmanifest.
- Kiểm tra cấu trúc và CRC của các gói ZIP sau khi đóng gói.
- Đã đối chiếu mã nguồn với 16 finding ID trong báo cáo QA.

Giới hạn xác minh:
- Môi trường trình duyệt tự động trong phiên này chặn điều hướng local/localhost nên không hoàn tất được kiểm thử tương tác trình duyệt sau sửa.
- Chưa kiểm thử trực tiếp trên Safari iOS, Chrome Android hoặc Windows thật.
- Báo cáo QA ban đầu cũng ghi rõ giọng đọc, micro, Service Worker/offline và một số request Cloudflare chưa được xác minh đầy đủ; bản sửa này không tuyên bố các phần đó đã PASS.
- Các lỗi mã nguồn/UI trong BVT-01 đến BVT-16 đã được chỉnh theo finding; cần chạy lại bộ QA trên môi trường triển khai để xác nhận đóng lỗi.

Phiên bản công khai: v42.9.1. Service Worker cache đổi sang hoc-trung-app-shell-v42-9-1-qa-fix-20261115 để buộc tải lại bản mới. Chưa tự triển khai lên GitHub Pages.


V42.9.2 - MOMENTIC QA FIX (2026-11-16)
- Sua 13 loi duoc ghi nhan trong bao cao Momentic: nhan dien tieng Viet co dau trong menu 3; nghia ca cho 鱼; chan sao chep placeholder menu 14/15; tim Pinyin co so thanh dieu; responsive ket qua menu 9; trang thai bat dau lai menu 10; ban dich CSV 再见; kiem tra bien so menu 11; giu emoji khi dich doan; khoi phuc cau hoi quiz khi quay lai; xoa bo tu menu 17; va xu ly anh OCR khong co chu.
- Tang cache version Service Worker va cap nhat nhan ung dung v42.9.2.
- Kiem tra da thuc hien: cau truc ZIP, JSON manifest, ma hoa Pinyin embed, cu phap JavaScript. Chua co browser E2E tren thiet bi that trong moi truong dong goi.
