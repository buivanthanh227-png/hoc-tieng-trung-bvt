# Thông tin repository

## Mô tả ngắn

Học Tiếng Trung BVT là ứng dụng web/PWA tiếng Việt để tự học tiếng Trung: từ điển Trung–Việt, tra cứu và luyện Pinyin, công cụ dịch, ASR/OCR và các bài thực hành chữ Hán. Ứng dụng chính có 17 menu; trang luyện số riêng được xuất bản tại `/luyen-so/`.

## Website và mã nguồn

- Website: https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/
- Repository: https://github.com/buivanthanh227-png/hoc-tieng-trung-bvt
- Phiên bản ứng dụng theo manifest: V42.10.23

## Nền tảng

Website được build/triển khai bằng GitHub Actions lên GitHub Pages. `sw.js` hỗ trợ PWA/offline có giới hạn. Các Cloudflare Workers ASR/dịch và OCR được quản lý/triển khai riêng; workflow Pages không cập nhật Workers.

## GitHub topics đề xuất

`chinese-learning`, `learn-chinese`, `pinyin`, `chinese-dictionary`, `vietnamese`, `language-learning`, `github-pages`, `pwa`

Ứng dụng là công cụ tự học cá nhân, không phải giáo trình, khóa học hoặc chương trình HSK chính thức. Xem README gốc để biết cấu trúc, cách chạy, kiểm thử và hướng dẫn triển khai.
