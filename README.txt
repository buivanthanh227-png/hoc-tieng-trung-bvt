HOC TIENG TRUNG BVT - PHIEN BAN V42.7

V42.7 - BO SUNG HAI MENU DA NGON NGU
- Menu 14: DICH HINH ANH DA NGON NGU. Chup/tai nhieu anh, OCR tu dong, hien van ban de sua, chon nguon tu dong/thu cong, chon ngon ngu dich va sao chep/phat am ket qua.
- Menu 15: DICH GIONG NOI DA NGON NGU. Ghi am, nhan dien Whisper tren Cloudflare, tu dong/chon ngon ngu nguon, dich sang ngon ngu dich, sua van ban, sao chep/phat am.
- Danh sach ngon ngu ban dau: Viet, Trung, Anh, Nhat, Han, Thai, Phap, Duc, Tay Ban Nha, Y, Bo Dao Nha, Nga, Indonesia, Malay, Hindi va A Rap.
- Hai menu moi dung OCR Space Engine 3, Whisper Large V3 Turbo va Meta M2M100 tren Cloudflare Workers AI.
- Cac menu 1–13 giu nguyen noi dung/chuc nang; chi them hai muc dieu huong va hai man hinh moi. Menu 4 van gui ASR o duong dan goc cua Worker.

QUAN TRONG - CAN CAP NHAT CLOUDFLARE WORKER ASR
1. Mo Cloudflare > Workers & Pages > Worker dang co ten/dia chi bvt-asr.
2. Thay ma Worker bang tep asr-cloudflare-worker.js trong goi v42.7 va Deploy.
3. GIU NGUYEN cac cau hinh hien co: Workers AI binding ten AI, Secret TURNSTILE_SECRET_KEY, bien ALLOWED_ORIGIN = https://buivanthanh227-png.github.io.
4. Worker moi giu nguyen POST tai duong dan goc cho menu 4, them POST /translate cho menu 14 va 15, dong thoi mo rong ngon ngu Whisper cho menu 15.
5. Khong can tao Worker moi. Khong can sua OCR Worker; OCR.Space Engine 3 da mac dinh tu dong nhan dien ngon ngu (language=auto neu khong gui ma cu).

CAP NHAT GITHUB PAGES
- PATCH_GITHUB_3_TEP.zip: giai nen va ghi de index.html, manifest.webmanifest, sw.js.
- FULL_13_TEP.zip: goi day du 13 tep, trong do asr-cloudflare-worker.js da la ban moi.
- Sau khi cap nhat Pages, deploy lai Worker bvt-asr theo huong dan phia tren de chuc nang dich da ngon ngu hoat dong.
- May tinh: Ctrl+F5. Dien thoai/may tinh bang: dong tab/app va mo lai; neu van con ban cu, xoa cache website.

GHI CHU
- Tu dong nhan dien tren van ban dung ky tu/tu khoa de doan nguon; voi doan Latin ngan hoac ngon ngu de nham lan, chon nguon thu cong de co ket qua chac hon.
- OCR mien phi co gioi han dung luong tep va quota cua nha cung cap. Worker OCR hien tai gioi han moi anh 1 MB sau nen.
- Phat am ket qua phu thuoc giong ngon ngu duoc cai tren thiet bi.
