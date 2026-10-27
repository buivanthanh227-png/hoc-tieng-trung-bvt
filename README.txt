HOC TIENG TRUNG BVT — v35 GHI AM TAI MAY + NHAN DANG CUC BO

MUC TIEU
- Phan xa noi khong dung SpeechRecognition cua Safari/Chrome nua.
- Nhan am thanh truc tiep tu micro dien thoai bang MediaRecorder.
- Whisper tiny multilingual chay trong trinh duyet qua Web Worker/WASM, giu giao dien phan hoi tot hon khi dang nhan dang.
- Khong gui file ghi am len may chu; khong can Cloudflare Workers AI, API key hay binding moi.

LAN DAU SU DUNG
- Mo app qua HTTPS (GitHub Pages) va cho phep micro.
- Lan dau can Internet de tai Transformers.js va mo hinh Whisper tiny; mo hinh quantized co tong dung luong tai xuong khoang 40–60 MB, tuy cac tep duoc phuc vu. Mang cham co the mat vai phut.
- Trinh duyet se co gang luu mo hinh vao Cache API. He dieu hanh co the xoa cache khi thieu dung luong; neu bi xoa thi se tai lai.
- Sau khi tai xong, am thanh duoc xu ly tren thiet bi. Khong gui ban ghi am len Cloudflare hay Hugging Face Inference API.
- Whisper tiny la mo hinh nho de chay tren dien thoai, ket qua co the nham chu. Neu nhan sai, nguoi dung van co the nhap cau tra loi bang chu Han.

CAP NHAT GITHUB PAGES
1. Giai nen ZIP.
2. Thay index.html, sw.js va them asr-worker.js vao thu muc goc repository. Giu manifest.webmanifest va icon.svg nhu trong goi.
3. Commit thay doi, mo lai GitHub Pages tren iPhone.
4. Cho phep microphone. Vao Phan xa noi, bam Bat dau ghi am, noi 1 cau, cham icon mic lon de dung. Lan dau cho tai mo hinh xong; cac luot sau dung lai mo hinh neu cache con.

GHI CHU KY THUAT QUAN TRONG
- Day khong phai ung dung ghi am Voice Memos nguyen ban cua iOS. Mot trang web khong the mo giao dien Voice Memos de ghi am roi tu dong lay ban ghi/van ban. V35 dung MediaRecorder de thu am tu microphone he thong, sau do nhan dang audio ngay tren thiet bi bang Transformers.js va onnx-community/whisper-tiny q8.
- OCR Worker hien tai khong can doi.
