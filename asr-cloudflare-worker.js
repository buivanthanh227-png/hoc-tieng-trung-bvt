/**
 * BVT Cloudflare Workers AI speech-to-text gateway (V42.5).
 * Required Worker configuration:
 *   AI: Workers AI binding named exactly "AI"
 *   TURNSTILE_SECRET_KEY: Cloudflare Turnstile Secret Key (Worker Secret)
 *   ALLOWED_ORIGIN: https://buivanthanh227-png.github.io
 * Model: @cf/openai/whisper-large-v3-turbo
 * The Turnstile Site Key is public and is embedded in index.html.
 */
const MODEL = '@cf/openai/whisper-large-v3-turbo';
const MAX_AUDIO_BYTES = 15 * 1024 * 1024;
const EXPECTED_ACTION = 'bvt_asr';

function json(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
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

async function verifyTurnstile(token, request, env, expectedHostname) {
  if (typeof token !== 'string' || !token || token.length > 2048) {
    return { success: false, reason: 'missing-input-response' };
  }
  const body = new URLSearchParams({
    secret: String(env.TURNSTILE_SECRET_KEY || ''),
    response: token
  });
  const ip = request.headers.get('CF-Connecting-IP');
  if (ip) body.set('remoteip', ip);

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  try {
    const response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
      signal: controller.signal
    });
    if (!response.ok) return { success: false, reason: 'siteverify-http-' + response.status };
    const result = await response.json();
    const valid = !!result.success &&
      result.hostname === expectedHostname &&
      result.action === EXPECTED_ACTION;
    return {
      success: valid,
      reason: valid ? '' : (Array.isArray(result['error-codes']) ? result['error-codes'].join(',') : 'turnstile-validation-failed')
    };
  } catch (error) {
    return { success: false, reason: String(error?.message || 'siteverify-unavailable') };
  } finally {
    clearTimeout(timeout);
  }
}

export default {
  async fetch(request, env) {
    const allowedOrigin = String(env.ALLOWED_ORIGIN || 'https://buivanthanh227-png.github.io')
      .trim()
      .replace(/\/+$/, '');
    const requestOrigin = request.headers.get('Origin') || '';
    let expectedHostname = 'buivanthanh227-png.github.io';
    try { expectedHostname = new URL(allowedOrigin).hostname; } catch (_) {}

    // Direct browser navigation is a read-only health check.
    if (request.method === 'GET' && !requestOrigin) {
      return json({
        ok: true,
        service: 'BVT speech recognition Worker',
        model: MODEL,
        protection: 'Cloudflare Turnstile',
        message: 'Worker is running. Send a Turnstile-verified audio POST request from the BVT learning app.'
      }, 200, allowedOrigin);
    }

    if (requestOrigin !== allowedOrigin) {
      return new Response('Origin not allowed', { status: 403 });
    }
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': allowedOrigin,
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
          'Vary': 'Origin'
        }
      });
    }
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405, allowedOrigin);
    if (!env.AI) return json({ error: 'Worker is missing the AI binding. Add Workers AI binding named AI.' }, 500, allowedOrigin);
    if (!env.TURNSTILE_SECRET_KEY) return json({ error: 'Worker is missing TURNSTILE_SECRET_KEY. Add the Turnstile Secret Key as a Worker Secret.' }, 500, allowedOrigin);

    try {
      const form = await request.formData();
      const audio = form.get('audio');
      if (!audio || typeof audio.arrayBuffer !== 'function') return json({ error: 'Missing audio file.' }, 400, allowedOrigin);
      if (!audio.size || audio.size > MAX_AUDIO_BYTES) return json({ error: 'Audio must be between 1 byte and 15 MB.' }, 413, allowedOrigin);

      const verification = await verifyTurnstile(form.get('cf-turnstile-response'), request, env, expectedHostname);
      if (!verification.success) {
        return json({ error: 'Turnstile verification failed.', details: verification.reason }, 401, allowedOrigin);
      }

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
