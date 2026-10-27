// BVT v35: on-device speech-to-text worker. Audio stays in this browser; no inference API/server is called.
import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1';

let transcriber = null;
let transcriberPromise = null;
let activeSession = null;

function postForActive(type, session, payload={}) {
  if (activeSession !== session) return;
  self.postMessage({ type, session, ...payload });
}

async function getTranscriber(session) {
  if (transcriber) return transcriber;
  if (!transcriberPromise) {
    transcriberPromise = (async () => {
      env.allowLocalModels = false;
      env.allowRemoteModels = true;
      env.useBrowserCache = true;
      env.useWasmCache = true;
      env.cacheKey = 'bvt-whisper-tiny-local-v35';
      if (env.backends && env.backends.onnx && env.backends.onnx.wasm) {
        // Single-thread WASM is conservative for iOS Safari and avoids COOP/COEP requirements.
        env.backends.onnx.wasm.numThreads = 1;
      }
      postForActive('status', session, {
        text: 'Đang tải mô hình Whisper tiny miễn phí lần đầu…',
        instruction: 'Lần đầu cần Internet để tải mô hình nhận dạng khoảng vài chục MB. Âm thanh không được gửi đi.'
      });
      const pipe = await pipeline('automatic-speech-recognition', 'onnx-community/whisper-tiny', {
        device: 'wasm',
        dtype: 'q8',
        progress_callback: info => {
          if (activeSession === null) return;
          if (info && info.status === 'progress') {
            const name = String(info.file || 'tệp mô hình').split('/').pop();
            const pct = Number.isFinite(info.progress) ? ` ${Math.round(info.progress)}%` : '';
            self.postMessage({ type: 'progress', session: activeSession,
              text: `Đang tải mô hình nhận dạng: ${name}${pct}`,
              instruction: 'Đang tải mô hình miễn phí về bộ nhớ đệm của trình duyệt. Không đóng trang.' });
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
      instruction: 'Bản ghi được xử lý cục bộ. Có thể mất vài giây tùy cấu hình điện thoại.'
    });
    const audio = message.audio instanceof Float32Array ? message.audio : new Float32Array(message.audio);
    const output = await pipe(audio, { language: 'chinese', task: 'transcribe', return_timestamps: false });
    postForActive('result', session, { text: String(output && output.text || '').trim() });
  } catch (error) {
    postForActive('error', session, { message: String(error && error.message || error || 'Không nhận dạng được âm thanh.') });
  }
});
