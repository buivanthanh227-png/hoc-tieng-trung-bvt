HOC TIENG TRUNG BVT - PHIEN BAN V42.6.3

BAN SUA LOI PHAT AM MENU 4, 7 VA 8
- Menu 4: nut doc ket qua tieng Trung phat am ca doan bang mot luot SpeechSynthesis zh-CN, khong tach thanh nhieu utterance de tranh chi doc cau dau tren mot so trinh duyet desktop.
- Menu 7: tu dong phat am chu Han sau khi chon tu vung hoac cau de luyen viet.
- Menu 8: tu dong phat am chu Han sau khi chon tu vung hoac cau de luyen doc.
- Cac luot chon noi dung tu menu 9 chuyen sang menu 7/8 cung tu dong phat am.
- Khong thay doi ten phien ban hien thi: van la V42.6. Khong can Deploy lai Cloudflare Worker.

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


MENU 5 VA 6 - LOC DO DAI TU VA CHONG LAP
- Hai menu Viet -> Trung va Trung -> Viet dung chung bo tu vung lay tu tu dien CVDICT da nhung trong ung dung (122.523 muc), khong con gioi han o 158 tu mau.
- Co the loc theo do dai: 1, 2, 3, 4, 5, 6 chu Han hoac 7 chu tro len. Mac dinh la 1 chu; lua chon gan nhat duoc nho tren thiet bi.
- Bo loc chi dem chu Han; chi dua vao muc co chu Han, Pinyin va nghia tieng Viet hop le, loai cac muc tham chieu/bien the ro rang va gop trung theo chu Han.
- So luong muc phu hop duoc hien ngay ben bo loc. Cac tu mau HSK 1-3 duoc xao tron hoc truoc, sau do moi den phan mo rong tu CVDICT. Do dai chu Han la bo loc do kho theo quy uoc nguoi hoc, khong phai bang xep hang HSK; CVDICT khong gan cap do cho toan bo tu dien.
- Hai menu dung chung hang doi xao tron rieng theo tung do dai. Moi tu chi xuat hien mot lan trong mot chu ky; het chu ky moi xao tron lai va tranh lap ngay tai ranh gioi hai chu ky.
- Thu tu va vi tri hoc duoc luu tren thiet bi; dong/mo lai ung dung hoac chuyen qua lai giua menu 5 va 6 khong lam lai tu dau.
