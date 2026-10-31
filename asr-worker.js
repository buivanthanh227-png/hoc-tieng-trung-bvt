// BVT v42: Whisper worker dùng cho phản xạ tiếng Trung và dịch giọng nói Việt/Trung. Import động để lỗi tải thư viện được trả về giao diện rõ ràng.
let transformersModulePromise = null;
let transcriber = null;
let transcriberPromise = null;
let activeSession = null;

function postForActive(type, session, payload = {}) {
  if (activeSession !== session) return;
  self.postMessage({ type, session, ...payload });
}

async function loadTransformers() {
  if (!transformersModulePromise) {
    transformersModulePromise = import('https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1')
      .catch(error => {
        transformersModulePromise = null;
        throw new Error('Không tải được thư viện Transformers.js từ CDN. Hãy kiểm tra kết nối Internet hoặc chặn nội dung của trình duyệt. ' + String(error && error.message || error || ''));
      });
  }
  return transformersModulePromise;
}

async function getTranscriber(session) {
  if (transcriber) return transcriber;
  if (!transcriberPromise) {
    transcriberPromise = (async () => {
      const { pipeline, env } = await loadTransformers();
      env.allowLocalModels = false;
      env.allowRemoteModels = true;
      env.useBrowserCache = true;
      env.useWasmCache = true;
      env.cacheKey = 'bvt-whisper-tiny-local-v37';
      try {
        if (env.backends && env.backends.onnx && env.backends.onnx.wasm) {
          env.backends.onnx.wasm.numThreads = 1;
        }
      } catch (_) {}
      postForActive('status', session, {
        text: 'Đang tải mô hình Whisper tiny miễn phí lần đầu…',
        instruction: 'Lần đầu cần Internet để tải mô hình. Âm thanh được xử lý trên điện thoại, không gửi lên API nhận dạng.'
      });
      const pipe = await pipeline('automatic-speech-recognition', 'onnx-community/whisper-tiny', {
        device: 'wasm', dtype: 'q8',
        progress_callback: info => {
          if (activeSession !== session || !info) return;
          if (info.status === 'progress') {
            const name = String(info.file || 'tệp mô hình').split('/').pop();
            const pct = Number.isFinite(info.progress) ? ` ${Math.round(info.progress)}%` : '';
            postForActive('progress', session, {
              text: `Đang tải mô hình nhận dạng: ${name}${pct}`,
              instruction: 'Đang tải mô hình miễn phí vào bộ nhớ đệm. Hãy giữ trang mở.'
            });
          }
        }
      });
      transcriber = pipe;
      return pipe;
    })().catch(error => {
      transcriberPromise = null;
      throw error;
    });
  }
  return transcriberPromise;
}


function countMatches(text, regex) { return (String(text || '').match(regex) || []).length; }
function hasVoiceTargetScript(text) {
  const t = String(text || '');
  return /[\u3400-\u9fff\uf900-\ufaff]/.test(t) || /[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽệềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]/i.test(t);
}
function scoreVoiceText(text, language) {
  const t = String(text || '');
  const han = countMatches(t, /[\u3400-\u9fff\uf900-\ufaff]/g);
  const latin = countMatches(t, /[A-Za-zÀ-ỹ]/g);
  const accents = countMatches(t, /[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽệềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]/gi);
  return language === 'chinese' ? han * 5 - latin * .15 : latin + accents * 3 - han * 5;
}


async function transcribeVietnameseChinese(pipe, audio, session) {
  const run = async options => {
    const output = await pipe(audio, { task: 'transcribe', return_timestamps: false, chunk_length_s: 30, stride_length_s: 5, ...options });
    return String(output && output.text || '').replace(/[\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
  };
  let automatic = '';
  try { automatic = await run({}); } catch (_) {}
  if (activeSession !== session) return '';
  if (automatic && hasVoiceTargetScript(automatic)) return automatic;
  postForActive('status', session, { text: 'Đang kiểm tra riêng tiếng Việt và tiếng Trung…' });
  let vietnamese = '', chinese = '';
  try { vietnamese = await run({ language: 'vietnamese' }); } catch (_) {}
  if (activeSession !== session) return '';
  try { chinese = await run({ language: 'chinese' }); } catch (_) {}
  if (activeSession !== session) return '';
  // Prefer a forced-language hypothesis with the matching writing system.
  if (/[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽệềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]/i.test(vietnamese)) return vietnamese;
  if (/[\u3400-\u9fff\uf900-\ufaff]/.test(chinese)) return chinese;
  const candidates = [
    { text: automatic, score: 0 },
    { text: vietnamese, score: scoreVoiceText(vietnamese, 'vietnamese') },
    { text: chinese, score: scoreVoiceText(chinese, 'chinese') }
  ].filter(item => item.text);
  candidates.sort((a, b) => b.score - a.score || b.text.length - a.text.length);
  return candidates[0]?.text || '';
}

self.addEventListener('message', async event => {
  const message = event.data || {};
  if (message.type === 'cancel') {
    if (activeSession === message.session) activeSession = null;
    return;
  }
  if (message.type !== 'transcribe') return;
  const session = message.session;
  activeSession = session;
  try {
    const pipe = await getTranscriber(session);
    if (activeSession !== session) return;
    postForActive('status', session, {
      text: 'Đang chạy mô hình nhận dạng trên điện thoại…',
      instruction: 'Bản ghi đang được xử lý cục bộ. Có thể mất vài giây tùy cấu hình điện thoại.'
    });
    const audio = message.audio instanceof Float32Array ? message.audio : new Float32Array(message.audio);
    const text = message.language === 'auto'
      ? await transcribeVietnameseChinese(pipe, audio, session)
      : String((await pipe(audio, { language: message.language === 'vietnamese' ? 'vietnamese' : 'chinese', task: 'transcribe', return_timestamps: false }))?.text || '').replace(/[\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
    postForActive('result', session, { text });
  } catch (error) {
    postForActive('error', session, { message: String(error && error.message || error || 'Không nhận dạng được âm thanh.') });
  }
});
