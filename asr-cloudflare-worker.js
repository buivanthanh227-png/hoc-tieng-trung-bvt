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
const TRANSLATION_MODEL = '@cf/meta/m2m100-1.2b';
const TRANSLATION_LANGUAGES = Object.freeze({
  "af":"afrikaans",
  "am":"amharic",
  "ar":"arabic",
  "ast":"asturian",
  "az":"azerbaijani",
  "ba":"bashkir",
  "be":"belarusian",
  "bg":"bulgarian",
  "bn":"bengali",
  "br":"breton",
  "bs":"bosnian",
  "ca":"catalan",
  "ceb":"cebuano",
  "cs":"czech",
  "cy":"welsh",
  "da":"danish",
  "de":"german",
  "el":"greek",
  "en":"english",
  "es":"spanish",
  "et":"estonian",
  "fa":"persian",
  "ff":"fulah",
  "fi":"finnish",
  "fr":"french",
  "fy":"western frisian",
  "ga":"irish",
  "gd":"scottish gaelic",
  "gl":"galician",
  "gu":"gujarati",
  "ha":"hausa",
  "he":"hebrew",
  "hi":"hindi",
  "hr":"croatian",
  "ht":"haitian creole",
  "hu":"hungarian",
  "hy":"armenian",
  "id":"indonesian",
  "ig":"igbo",
  "ilo":"iloko",
  "is":"icelandic",
  "it":"italian",
  "ja":"japanese",
  "jv":"javanese",
  "ka":"georgian",
  "kk":"kazakh",
  "km":"central khmer",
  "kn":"kannada",
  "ko":"korean",
  "lb":"luxembourgish",
  "lg":"ganda",
  "ln":"lingala",
  "lo":"lao",
  "lt":"lithuanian",
  "lv":"latvian",
  "mg":"malagasy",
  "mk":"macedonian",
  "ml":"malayalam",
  "mn":"mongolian",
  "mr":"marathi",
  "ms":"malay",
  "my":"burmese",
  "ne":"nepali",
  "nl":"dutch",
  "no":"norwegian",
  "ns":"northern sotho",
  "oc":"occitan",
  "or":"oriya",
  "pa":"punjabi",
  "pl":"polish",
  "ps":"pashto",
  "pt":"portuguese",
  "ro":"romanian",
  "ru":"russian",
  "sd":"sindhi",
  "si":"sinhala",
  "sk":"slovak",
  "sl":"slovenian",
  "so":"somali",
  "sq":"albanian",
  "sr":"serbian",
  "ss":"swati",
  "su":"sundanese",
  "sv":"swedish",
  "sw":"swahili",
  "ta":"tamil",
  "th":"thai",
  "tl":"tagalog",
  "tn":"tswana",
  "tr":"turkish",
  "uk":"ukrainian",
  "ur":"urdu",
  "uz":"uzbek",
  "vi":"vietnamese",
  "wo":"wolof",
  "xh":"xhosa",
  "yi":"yiddish",
  "yo":"yoruba",
  "zh":"chinese",
  "zu":"zulu"
});
const ASR_LANGUAGES = new Set(["af","am","ar","az","ba","be","bg","bn","br","bs","ca","cs","cy","da","de","el","en","es","et","fa","fi","fr","gl","gu","ha","he","hi","hr","ht","hu","hy","id","is","it","ja","jv","ka","kk","km","kn","ko","lb","ln","lo","lt","lv","mg","mk","ml","mn","mr","ms","my","ne","nl","no","oc","pa","pl","ps","pt","ro","ru","sd","si","sk","sl","so","sq","sr","su","sv","sw","ta","th","tl","tr","uk","ur","uz","vi","yi","yo","zh"]);
const ASR_LANGUAGE_ALIASES = Object.freeze({jv:'jw'});
const MAX_TRANSLATION_CHARS = 5000;

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

async function verifyTurnstile(token, request, env, expectedHostname, expectedAction = EXPECTED_ACTION) {
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
      result.action === expectedAction;
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


function splitTranslationInput(value, maxChars = 850) {
  const chars = Array.from(String(value || ''));
  const chunks = [];
  let rest = chars;
  while (rest.length > maxChars) {
    let cut = maxChars;
    const floor = Math.floor(maxChars * 0.62);
    for (let i = maxChars; i >= floor; i--) {
      if (/\s/.test(rest[i] || '')) { cut = i; break; }
    }
    chunks.push(rest.slice(0, cut).join('').trim());
    rest = rest.slice(cut);
    while (rest.length && /\s/.test(rest[0])) rest.shift();
  }
  if (rest.length) chunks.push(rest.join('').trim());
  return chunks.filter(Boolean);
}
async function handleMultilingualTranslation(form, env, request, expectedHostname, allowedOrigin) {
  const text = String(form.get('text') || '').trim();
  const source = String(form.get('source_lang') || '').trim().toLowerCase();
  const target = String(form.get('target_lang') || '').trim().toLowerCase();
  if (!text) return json({ error: 'Chưa có văn bản để dịch.' }, 400, allowedOrigin);
  if (text.length > MAX_TRANSLATION_CHARS) return json({ error: 'Nội dung vượt giới hạn 5.000 ký tự mỗi lượt.' }, 413, allowedOrigin);
  if (!TRANSLATION_LANGUAGES[source] || !TRANSLATION_LANGUAGES[target]) return json({ error: 'Ngôn ngữ nguồn hoặc đích chưa được hỗ trợ.' }, 400, allowedOrigin);
  const verification = await verifyTurnstile(form.get('cf-turnstile-response'), request, env, expectedHostname, EXPECTED_ACTION);
  if (!verification.success) return json({ error: 'Xác minh bảo mật thất bại. Hãy thử lại.', details: verification.reason }, 401, allowedOrigin);
  if (source === target) return json({ translated_text: text, source_lang: source, target_lang: target, model: TRANSLATION_MODEL }, 200, allowedOrigin);
  try {
    const chunks = splitTranslationInput(text);
    const translated = [];
    for (const chunk of chunks) {
      const result = await env.AI.run(TRANSLATION_MODEL, {
        text: chunk,
        source_lang: TRANSLATION_LANGUAGES[source],
        target_lang: TRANSLATION_LANGUAGES[target]
      });
      const output = String(result?.translated_text || '').trim();
      if (!output) throw new Error('Mô hình dịch không trả về văn bản.');
      translated.push(output);
    }
    return json({ translated_text: translated.join(' '), source_lang: source, target_lang: target, model: TRANSLATION_MODEL }, 200, allowedOrigin);
  } catch (error) {
    return json({ error: String(error?.message || error || 'Không thể dịch văn bản lúc này.') }, 502, allowedOrigin);
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
      const url = new URL(request.url);
      const form = await request.formData();
      if (url.pathname === '/translate') {
        return await handleMultilingualTranslation(form, env, request, expectedHostname, allowedOrigin);
      }
      if (url.pathname !== '/' && url.pathname !== '') return json({ error: 'Đường dẫn không hợp lệ.' }, 404, allowedOrigin);
      const audio = form.get('audio');
      if (!audio || typeof audio.arrayBuffer !== 'function') return json({ error: 'Missing audio file.' }, 400, allowedOrigin);
      if (!audio.size || audio.size > MAX_AUDIO_BYTES) return json({ error: 'Audio must be between 1 byte and 15 MB.' }, 413, allowedOrigin);

      const verification = await verifyTurnstile(form.get('cf-turnstile-response'), request, env, expectedHostname);
      if (!verification.success) {
        return json({ error: 'Turnstile verification failed.', details: verification.reason }, 401, allowedOrigin);
      }

      const requestedLanguage = String(form.get('language') || 'auto').toLowerCase();
      const language = ASR_LANGUAGES.has(requestedLanguage) ? requestedLanguage : 'auto';
      const whisperLanguage = ASR_LANGUAGE_ALIASES[language] || language;
      const bytes = new Uint8Array(await audio.arrayBuffer());
      const params = {
        audio: toBase64(bytes),
        task: 'transcribe',
        vad_filter: true,
        ...(language === 'auto' ? {} : { language: whisperLanguage }),
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
