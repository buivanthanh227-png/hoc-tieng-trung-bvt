HOC TIENG TRUNG BVT - PHIEN BAN V42.5.13

PHAT AM TIENG TRUNG VA TIENG VIET
- Da tro lai co che doc bang SpeechSynthesis cua trinh duyet/he dieu hanh nhu ban truoc khi them dich vu TTS Cloudflare.
- Ca tieng Trung va tieng Viet deu doc truc tiep bang giong co san tren thiet bi; ung dung khong goi dich vu TTS truc tuyen, khong dung Puck, Kore, Olivia hay danh sach giong tren Cloudflare.
- Tieng Trung uu tien cac giong zh co san; neu thiet bi co cap giong nam/nu phu hop thi co che cu van luan phien nhu ban goc. Tieng Viet uu tien giong vi-VN neu thiet bi co.
- Neu thiet bi thieu giong tieng Trung hoac tieng Viet, muc CHON GIONG DOC THIET BI se tu hien. Danh sach chi lay cac giong da cai tren thiet bi de nguoi dung tu chon. Neu danh sach khong co giong phu hop, can cai them giong trong cai dat he dieu hanh.
- Neu chon mot giong khac ngon ngu, chat luong phat am co the khong chinh xac; nen chon giong co ngon ngu Trung hoac Viet.

CLOUDFLARE
- Cloudflare Worker chi con phuc vu nhan dien giong noi (ASR), khong phat am (TTS).
- Khong can Deploy lai Worker neu nhan dien giong noi hien tai van hoat dong. Tep asr-cloudflare-worker.js trong goi day la ban ASR-only neu can tham chieu hoac thay Worker.
- Giu nguyen AI binding (AI), TURNSTILE_SECRET_KEY va ALLOWED_ORIGIN neu tiep tuc su dung Worker ASR.
- Cac worker rieng khac (asr-worker.js, asr-voice-worker.js, ocr-worker.js) giu nguyen.

MENU 3 VA CAC MENU LUYEN TAP
- Da sua quy tac CSS de the DICH NHANH an dung khi chuyen sang menu 5, 6, 7 va 8; khong con bi chen len dau khu vuc chuc nang ben phai.
- Giao dien menu 3 tiep tuc duoc thu gon; cac chuc nang dich nhanh, dich doan va dich tep duoc giu nguyen.

CAP NHAT GITHUB PAGES
- Giai nen goi va tai ghi de vao dung thu muc GitHub Pages dang publish.
- Goi PATCH chi gom 3 tep can cap nhat: index.html, manifest.webmanifest, sw.js.
- Goi FULL gom day du 13 tep de luu tru/thay toan bo neu can.
