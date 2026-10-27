// Cloudflare Worker: private proxy for OCR.Space Engine 3.
// Add OCR_SPACE_API_KEY as a Secret in Cloudflare Worker Settings > Variables and Secrets.
// Do not put the API key in index.html or GitHub.
const ALLOWED_ORIGIN = 'https://buivanthanh227-png.github.io';
const corsHeaders = (origin) => ({
  'Access-Control-Allow-Origin': origin === ALLOWED_ORIGIN ? origin : ALLOWED_ORIGIN,
  'Access-Control-Allow-Methods': 'POST, OPTIONS, GET',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
  'Vary': 'Origin'
});
function json(data, status, origin) {
  return new Response(JSON.stringify(data), { status: status || 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...corsHeaders(origin) } });
}
export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const url = new URL(request.url);
    if (request.method === 'OPTIONS') {
      if (origin && origin !== ALLOWED_ORIGIN) return new Response(null, { status: 403 });
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }
    if (request.method === 'GET' && url.pathname === '/') {
      return json({ ok: true, service: 'BVT Online OCR proxy', endpoint: '/ocr', engine: 3 }, 200, origin);
    }
    if (url.pathname !== '/ocr') return json({ ok: false, error: 'Đường dẫn không hợp lệ. Dùng /ocr.' }, 404, origin);
    if (request.method !== 'POST') return json({ ok: false, error: 'Chỉ chấp nhận POST.' }, 405, origin);
    if (origin !== ALLOWED_ORIGIN) return json({ ok: false, error: 'Nguồn yêu cầu không được phép.' }, 403, origin);
    if (!env.OCR_SPACE_API_KEY) return json({ ok: false, error: 'Worker chưa được cấu hình Secret OCR_SPACE_API_KEY.' }, 503, origin);
    let file;
    try {
      const incoming = await request.formData();
      file = incoming.get('file');
    } catch (_) {
      return json({ ok: false, error: 'Không đọc được ảnh tải lên.' }, 400, origin);
    }
    if (!(file instanceof File)) return json({ ok: false, error: 'Không tìm thấy tệp ảnh.' }, 400, origin);
    if (!String(file.type || '').startsWith('image/')) return json({ ok: false, error: 'Tệp gửi lên không phải ảnh.' }, 415, origin);
    if (file.size > 1024 * 1024) return json({ ok: false, error: 'Ảnh vượt giới hạn 1 MB của gói OCR miễn phí; ứng dụng cần nén ảnh trước khi gửi.' }, 413, origin);
    try {
      const body = new FormData();
      body.append('file', file, file.name || 'chinese-vocabulary.jpg');
      body.append('OCREngine', '3');
      body.append('isOverlayRequired', 'false');
      body.append('detectOrientation', 'true');
      body.append('scale', 'true');
      body.append('isTable', 'true');
      const response = await fetch('https://api.ocr.space/parse/image', {
        method: 'POST',
        headers: { 'apikey': env.OCR_SPACE_API_KEY },
        body
      });
      let upstream;
      try { upstream = await response.json(); } catch (_) { throw new Error('Dịch vụ OCR trả về phản hồi không đọc được.'); }
      if (!response.ok) return json({ ok: false, error: 'Dịch vụ OCR trả mã HTTP ' + response.status + '. Thử lại sau.' }, 502, origin);
      if (upstream.IsErroredOnProcessing) {
        const detail = [upstream.ErrorMessage, upstream.ErrorDetails].flat().filter(Boolean).join(' ');
        return json({ ok: false, error: detail || 'OCR.Space không xử lý được ảnh.' }, 422, origin);
      }
      const parsed = Array.isArray(upstream.ParsedResults) ? upstream.ParsedResults : [];
      const text = parsed.map(p => p && p.ParsedText || '').filter(Boolean).join('\n').trim();
      if (!text) return json({ ok: false, error: 'OCR.Space không nhận diện được chữ. Hãy thử ảnh sáng, rõ và chụp gần hơn.' }, 422, origin);
      return json({ ok: true, engine: 3, text, processingTimeMs: Number(upstream.ProcessingTimeInMilliseconds) || null }, 200, origin);
    } catch (err) {
      return json({ ok: false, error: (err && err.message) || 'Không thể kết nối dịch vụ OCR.Space.' }, 502, origin);
    }
  }
};
