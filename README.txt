HOC TIENG TRUNG BVT - PHIEN BAN V42.7.1

V42.7.1 - TINH CHINH RIENG MENU 14 VA 15
- Lam nhe, giam do dam mau rieng cua menu 14 va 15; mau chu/so tren cac nen mau moi la trang.
- Menu 15 doi bieu tuong tai nghe thanh bieu tuong giao tiep/dich thuat (nguoi noi ⇄ chu).
- Thu gon o tim/chon ngon ngu va nut BAT DAU NOI.
- Them nut phat am, sao chep, xoa noi dung nhan dien cho ca hai menu.
- Sau khi OCR hoac nhan dien giong noi xong, tu dong dich; khi sua van ban hoac doi nguon/dich sang, tu dong dich lai. Van ban nhan dien duoc giu nguyen khi chi doi ngon ngu dich.
- Danh sach dich M2M100 gom 100 ma ngon ngu; menu 15 chi hien nguon nam trong tap Whisper Large v3 Turbo co the chuyen tiep sang M2M100. O tim kiem loc ten ngon ngu/ma ngon ngu.
- Menu 1–13 va cac Worker OCR khong bi sua chuc nang. Endpoint ASR goc van giu nguyen giao thuc cho menu 4; Worker chi mo rong ma ngon ngu chap nhan cho ASR va duong /translate.

CAP NHAT GITHUB PAGES
- PATCH_GITHUB_3_TEP.zip: giai nen, ghi de index.html, manifest.webmanifest, sw.js vao repository Pages, sau do Commit changes.
- FULL_13_TEP.zip: goi day du 13 tep neu can luu tru/thay toan bo ung dung.

CAP NHAT CLOUDFLARE WORKER (BAT BUOC DE CO 100 NGON NGU DICH)
1. Mo Cloudflare > Workers & Pages > Worker dang dung cho bvt-asr.
2. Thay ma Worker bang tep asr-cloudflare-worker-v42_7_1-multilingual.js va Deploy.
3. Giu nguyen Workers AI binding ten AI, Secret TURNSTILE_SECRET_KEY, bien ALLOWED_ORIGIN = https://buivanthanh227-png.github.io.
4. Khong tao Worker moi; endpoint POST / cu van danh cho menu 4. Endpoint POST /translate xu ly menu 14 va 15.
5. Khong can sua OCR Worker.

SAU KHI CAP NHAT
- May tinh: Ctrl+F5.
- Dien thoai/may tinh bang: dong tab/app roi mo lai. Neu van con giao dien cu, xoa cache website.

GHI CHU
- M2M100 ho tro bo ma ngon ngu dich 100 ngon ngu. Whisper khong co cung danh sach, nen nguon menu 15 duoc gioi han theo tap ngon ngu giao nhau ma hai buoc nhan dien va dich cung xu ly duoc.
- Tu dong nhan dien ngon ngu van co the khong chac chan voi cau rat ngan hoac cac ngon ngu dung chung chu cai Latin; khi do hay chon nguon bang tay trong o tim kiem.
- Phat am ket qua phu thuoc voice/TTS duoc cai tren thiet bi.
