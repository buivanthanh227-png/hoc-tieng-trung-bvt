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
