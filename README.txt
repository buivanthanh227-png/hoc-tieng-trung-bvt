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
