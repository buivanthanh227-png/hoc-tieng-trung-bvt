/**
 * BVT Cloudflare Workers AI speech-to-text gateway.
 * Required Worker bindings/settings:
 *   AI: Workers AI binding named exactly "AI"
 *   ASR_SHARED_SECRET: secret string (set with `wrangler secret put ASR_SHARED_SECRET`)
 *   ALLOWED_ORIGIN: https://buivanthanh227-png.github.io
 * Model: @cf/openai/whisper-large-v3-turbo
 */
const MODEL = '@cf/openai/whisper-large-v3-turbo';
const MAX_AUDIO_BYTES = 15 * 1024 * 1024;

function json(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Authorization, Content-Type',
      'Vary': 'Origin'
    }
  });
}
function toBase64(bytes) {
  let binary = '';
  const chunkSize = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += chunkSize) {
    const chunk = bytes.subarray(offset, Math.min(offset + chunkSize, bytes.length));
    binary += String.fromCharCode(...chunk);
  }
  return btoa(binary);
}

export default {
  async fetch(request, env) {
    // Normalize the configured origin so an accidental trailing slash or
    // surrounding whitespace does not cause a false CORS rejection.
    const allowedOrigin = String(env.ALLOWED_ORIGIN || 'https://buivanthanh227-png.github.io')
      .trim()
      .replace(/\/+$/, '');
    const requestOrigin = request.headers.get('Origin') || '';

    // A direct visit to the workers.dev URL from the address bar is a health
    // check. Such top-level navigations normally have no Origin header, so
    // answer them without weakening the CORS allowlist for cross-site calls.
    if (request.method === 'GET' && !requestOrigin) {
      return json({
        ok: true,
        service: 'BVT speech recognition Worker',
        model: MODEL,
        message: 'Worker is running. Send an audio POST request from the BVT learning app.'
      }, 200, allowedOrigin);
    }

    // Browser requests from another website must match the configured origin.
    if (requestOrigin !== allowedOrigin) {
      return new Response('Origin not allowed', { status: 403 });
    }
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': allowedOrigin,
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Authorization, Content-Type',
          'Access-Control-Max-Age': '86400',
          'Vary': 'Origin'
        }
      });
    }
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405, allowedOrigin);
    if (!env.AI || !env.ASR_SHARED_SECRET) return json({ error: 'Worker is missing AI binding or ASR_SHARED_SECRET.' }, 500, allowedOrigin);
    const authorization = request.headers.get('Authorization') || '';
    if (authorization !== `Bearer ${env.ASR_SHARED_SECRET}`) return json({ error: 'Unauthorized' }, 401, allowedOrigin);

    try {
      const form = await request.formData();
      const audio = form.get('audio');
      if (!audio || typeof audio.arrayBuffer !== 'function') return json({ error: 'Missing audio file.' }, 400, allowedOrigin);
      if (!audio.size || audio.size > MAX_AUDIO_BYTES) return json({ error: 'Audio must be between 1 byte and 15 MB.' }, 413, allowedOrigin);
      const requestedLanguage = String(form.get('language') || 'auto').toLowerCase();
      const language = requestedLanguage === 'vi' ? 'vi' : requestedLanguage === 'zh' ? 'zh' : 'auto';
      const bytes = new Uint8Array(await audio.arrayBuffer());
      const params = {
        audio: toBase64(bytes),
        task: 'transcribe',
        vad_filter: true,
        ...(language === 'auto' ? {} : { language }),
        ...(language === 'vi' ? { initial_prompt: 'Tiếng Việt. Giữ dấu tiếng Việt, tên riêng và dấu câu.' } : {}),
        ...(language === 'zh' ? { initial_prompt: '普通话，简体中文。请准确识别汉字、声调和标点。' } : {})
      };
      const result = await env.AI.run(MODEL, params);
      const text = String(result?.text || '').trim();
      return json({ text, model: MODEL }, 200, allowedOrigin);
    } catch (error) {
      return json({ error: String(error?.message || error || 'Speech recognition failed.') }, 502, allowedOrigin);
    }
  }
};
