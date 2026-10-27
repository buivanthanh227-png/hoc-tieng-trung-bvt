// BVT v36: Whisper chạy cục bộ. Import động để lỗi tải thư viện được trả về giao diện rõ ràng.
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
      env.cacheKey = 'bvt-whisper-tiny-local-v36';
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
    const output = await pipe(audio, { language: 'chinese', task: 'transcribe', return_timestamps: false });
    postForActive('result', session, { text: String(output && output.text || '').trim() });
  } catch (error) {
    postForActive('error', session, { message: String(error && error.message || error || 'Không nhận dạng được âm thanh.') });
  }
});
