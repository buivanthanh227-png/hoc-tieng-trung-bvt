/**
 * BVT Cloudflare Workers AI speech-to-text and text-to-speech gateway (V42.5.8).
 * Required Worker configuration:
 *   AI: Workers AI binding named exactly "AI"
 *   TURNSTILE_SECRET_KEY: Cloudflare Turnstile Secret Key (Worker Secret)
 *   ALLOWED_ORIGIN: https://buivanthanh227-png.github.io
 * Speech-to-text model: @cf/openai/whisper-large-v3-turbo
 * Speech model: google/gemini-3.8-flash-tts
 * The Turnstile Site Key is public and is embedded in index.html.
 */
const MODEL = '@cf/openai/whisper-large-v3-turbo';
const TTS_MODEL = 'google/gemini-3.8-flash-tts';
const TTS_DEFAULT_VOICES = Object.freeze({ vi: 'Kore', zh: 'Puck' });
const MAX_AUDIO_BYTES = 15 * 1024 * 1024;
const MAX_TTS_AUDIO_BYTES = 20 * 1024 * 1024;
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


async function decodeAudioBytes(value) {
  if (value instanceof Uint8Array) return value;
  if (value instanceof ArrayBuffer) return new Uint8Array(value);
  if (ArrayBuffer.isView(value)) return new Uint8Array(value.buffer, value.byteOffset, value.byteLength);
  if (value && typeof value === 'object') {
    if (value.audio != null) return decodeAudioBytes(value.audio);
    if (value.data != null) return decodeAudioBytes(value.data);
  }
  if (typeof value !== 'string') throw new Error('The TTS model did not return audio data.');
  const source = value.trim();
  if (/^https:\/\//i.test(source)) {
    const audioUrl = new URL(source);
    if (audioUrl.protocol !== 'https:') throw new Error('The TTS audio URL must use HTTPS.');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    try {
      const response = await fetch(audioUrl.href, { signal: controller.signal });
      if (!response.ok) throw new Error('Could not download generated audio (' + response.status + ').');
      const length = Number(response.headers.get('Content-Length') || 0);
      if (length > MAX_TTS_AUDIO_BYTES) throw new Error('Generated audio is too large.');
      const bytes = new Uint8Array(await response.arrayBuffer());
      if (!bytes.byteLength || bytes.byteLength > MAX_TTS_AUDIO_BYTES) throw new Error('Generated audio is empty or too large.');
      return bytes;
    } finally { clearTimeout(timeout); }
  }
  const base64 = source.replace(/^data:audio\/[a-z0-9.+-]+;base64,/i, '').replace(/\s/g, '');
  if (!/^[A-Za-z0-9+/]*={0,2}$/.test(base64) || base64.length % 4 === 1) {
    throw new Error('The TTS model returned an unsupported audio format.');
  }
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

async function handleTts(body, request, env, allowedOrigin, expectedHostname) {
  if (!env.AI) return json({ error: 'Worker is missing the AI binding.' }, 500, allowedOrigin);
  if (!env.TURNSTILE_SECRET_KEY) return json({ error: 'Worker is missing TURNSTILE_SECRET_KEY.' }, 500, allowedOrigin);
  const text = String(body?.text || '').trim();
  if (!text) return json({ error: 'Missing text to speak.' }, 400, allowedOrigin);
  if (text.length > 3000) return json({ error: 'Text is too long. Please keep each reading under 3,000 characters.' }, 413, allowedOrigin);
  const verification = await verifyTurnstile(body?.turnstileToken, request, env, expectedHostname);
  if (!verification.success) return json({ error: 'Speech service verification failed.' }, 401, allowedOrigin);
  const language = String(body?.language || 'vi').toLowerCase() === 'zh' ? 'zh' : 'vi';
  // The app ships only two fixed voices: Puck for Mandarin and Kore for Vietnamese.
  // The worker enforces this pair even if a client sends another voice name.
  const voice = TTS_DEFAULT_VOICES[language];
  try {
    const result = await env.AI.run(TTS_MODEL, { text, voice });
    const audio = await decodeAudioBytes(result?.audio ?? result);
    if (!audio.byteLength) throw new Error('The TTS model returned an empty audio file.');
    return new Response(audio, {
      status: 200,
      headers: {
        'Content-Type': 'audio/wav',
        'Content-Length': String(audio.byteLength),
        'Cache-Control': 'no-store',
        'Access-Control-Allow-Origin': allowedOrigin,
        'Vary': 'Origin'
      }
    });
  } catch (error) {
    return json({ error: String(error?.message || error || 'Speech generation failed.') }, 502, allowedOrigin);
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
        service: 'BVT speech recognition and speech playback Worker',
        model: MODEL,
        tts_model: TTS_MODEL,
        protection: 'Cloudflare Turnstile',
        message: 'Worker is running. Send a verified speech-recognition or speech-generation request from the BVT learning app.'
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
      const contentType = request.headers.get('Content-Type') || '';
      if (contentType.toLowerCase().includes('application/json')) {
        const body = await request.json();
        if (body?.task === 'tts') return await handleTts(body, request, env, allowedOrigin, expectedHostname);
        return json({ error: 'Unknown JSON task.' }, 400, allowedOrigin);
      }
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
