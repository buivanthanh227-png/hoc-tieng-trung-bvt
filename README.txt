HOC TIENG TRUNG BVT - PHIEN BAN V42.7.6

V42.7.6 - SUA LOGIC NHAN DIEN NGON NGU VA DICH DA NGON NGU
- Bo doan ma trinh duyet tu doan nguon bang tu khoa. Che do TU DONG gui van ban OCR/ASR den Worker de nhan dien bang @cf/meta/llama-3.3-70b-instruct-fp8-fast voi JSON Schema va muc tin cay.
- Neu van ban ngan, da ngon ngu, nhieu ten rieng hoac mo ho, Worker khong tu doan. Ung dung yeu cau nguoi dung chon nguon thu cong de tranh dua sai source_lang vao bo dich.
- Nguon da nhan dien duoc luu theo dung van ban; doi ngon ngu dich khong can nhan dien lai. Sua noi dung hoac doi nguon se xoa ket qua nhan dien cu.
- Dinh tuyen dich: SEA-LION cho cac cap trong 11 ngon ngu Dong Nam A duoc ho tro; Gemma 4 cho nhom ngon ngu pho bien; M2M100 lam du phong va giu do phu danh sach 100 ngon ngu.
- Dung tham so rieng theo schema model: SEA-LION dung max_tokens; Gemma 4 dung max_completion_tokens va tat thinking trong tac vu dich.
- Worker tra ve ngon ngu nguon thuc te, model nhan dien, do tin cay, model dich va duong dinh tuyen.
- Endpoint Whisper ASR goc (/) duoc giu nguyen. OCR Worker khong thay doi.
- Cac giao dien, 13 menu cu, du lieu tu dien va cac sua doi v42.7.5 duoc giu nguyen.

CAP NHAT GITHUB PAGES
- PATCH_GITHUB_3_TEP.zip: giai nen, ghi de index.html, manifest.webmanifest, sw.js vao repository Pages, sau do Commit changes.
- FULL_13_TEP.zip: goi day du 13 tep, bao gom Worker moi.

CLOUDFLARE WORKER - BAT BUOC DEPLOY
- Mo Worker hien tai bvt-asr va thay ma bang tep asr-cloudflare-worker-v42_7_6-language-detection-translation.js.
- Giu nguyen Workers AI binding ten AI, Secret TURNSTILE_SECRET_KEY va ALLOWED_ORIGIN https://buivanthanh227-png.github.io.
- Khong can thay OCR Worker.

LUU Y CHAT LUONG
- Tu dong nhan dien khong nen tu dong ket luan voi doan qua ngan, da ngon ngu, ten rieng hoac van ban OCR bi loi; khi do app yeu cau chon nguon thu cong.
- SEA-LION/Gemma 4 duoc uu tien cho nhom ngon ngu tuong ung; M2M100 giu do phu rong. Chat luong van co the khac nhau theo cap ngon ngu va van ban. Khong co mo hinh dich nao dam bao dung tuyet doi moi truong hop.

SAU KHI CAP NHAT
- May tinh: Ctrl+F5.
- Dien thoai/may tinh bang: dong tab/app roi mo lai. Neu van con giao dien cu, xoa cache website.


V42.8 - THEM MENU 16 LUYEN NGHE PHAT AM PINYIN
- Bo sung menu 16, giu nguyen 15 menu truoc do; them mau rieng xanh duong.
- Su dung dung bang Pinyin trong PDF nguoi dung cung cap: 23 hang phu am dau, 36 cot van mau, 391 am tiet; khong tu tao cac o trong.
- Them nghe mau cho 23 thanh mau va 36 van mau; moi muc co nut loa va nut sao chep. Thanh mau duoc nghe qua am tiet dan co cung thanh mau, khong doc ten chu cai tieng Anh.
- Bang ghep am co bo loc 16.1/16.2/16.3/16.4; bam loa tai moi o de nghe am tiet theo thanh dang chon.
- Muc 16.5 tao bai nghe ngau nhien tu tap 391 am tiet x 4 thanh. Hai nhom dap an doc lap: thanh dieu so may va am tiet Pinyin khong dau; co the chon chi mot nhom hoac ca hai.
- Giong doc dung bo ghi am nguoi that Chen Wang tu hugolpz/audio-cmn (64k/syllabs), ghim theo commit f759a0f18f27690742957619e1248ed91e9b3f2c; khong dung giong doc mac dinh cua thiet bi.
- 1.564 tep ghi am can thiet (co xu ly ten tep dac biet ju4 -> jv4) duoc tai va luu vao Cache Storage cua trinh duyet tren tung thiet bi. Lan dau can Internet; co nut tai tron bo de dung ngoai tuyen sau khi tai du va Service Worker da kich hoat (mo lai trang sau khi deploy de worker nhan quyen kiem soat).
- Ghi cong: hugolpz/audio-cmn; nguoi doc am tiet Chen Wang; nguon tuyen bo giay phep CC BY-SA. Kiem tra README nguon de biet dieu khoan/phiên ban ap dung.
- Giao dien menu 16 co CSS va JavaScript rieng, tu dong co gian tren desktop, tablet va dien thoai. Khong sua logic 15 menu cu.

CAP NHAT GITHUB PAGES
- PATCH_GITHUB_3_TEP.zip: ghi de index.html, manifest.webmanifest, sw.js.
- FULL_14_TEP.zip: goi day du cac tep ung dung, bao gom sw.js cap nhat.
- Sau khi deploy: PC nhan Ctrl+F5; dien thoai dong app/tab roi mo lai.
