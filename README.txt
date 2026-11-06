HOC TIENG TRUNG BVT - PHIEN BAN V42.5.11

PHAT AM TIENG TRUNG
- Giong mac dinh duy nhat cua ung dung la Google zh-CN, lay tu danh sach SpeechSynthesis do trinh duyet/he dieu hanh cung cap.
- Neu thiet bi khong cung cap Google zh-CN, ung dung KHONG tu dong doi sang Puck hay mot giong Trung mac dinh khac. Nguoi dung co the cai Google zh-CN hoac tu chon mot giong khac trong danh sach giong da cai tren thiet bi.

PHAT AM TIENG VIET
- Mac dinh su dung mot giong truc tuyen co dinh Olivia qua Cloudflare Workers AI (Inworld TTS-2), ngon ngu vi-VN.
- Yeu cau Internet, Worker bvt-asr da duoc Deploy va co Workers AI binding AI.
- Nguoi dung van co the tu chon mot giong tieng Viet co san tren thiet bi. Cac giong nay duoc doc dong tu trinh duyet, khong nhung vao ma nguon.

CAP NHAT GITHUB PAGES
Tai len dung thu muc dang publish: index.html, manifest.webmanifest, sw.js.

CAP NHAT CLOUDFLARE WORKER
Dan ma trong tep asr-cloudflare-worker.js vao Worker hien tai bvt-asr va Deploy. Giu nguyen AI binding (AI), TURNSTILE_SECRET_KEY va ALLOWED_ORIGIN. Khong tai Worker len GitHub Pages.
Cac worker rieng khac (asr-worker.js, asr-voice-worker.js, ocr-worker.js) giu nguyen neu dang su dung.

MENU 3
Giao dien menu 3 da duoc thu gon; cac ID va chuc nang dich nhanh, dich doan va dich tep duoc giu nguyen.
