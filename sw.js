'use strict';
const CACHE_NAME = 'hoc-trung-app-shell-v42-8-9-diagonal-labels-20261113';
const PINYIN_AUDIO_CACHE = 'bvt-pinyin-audio-assets-v42-8-9';
const PINYIN_AUDIO_ORIGIN = 'https://cdn.jsdelivr.net';
const PINYIN_AUDIO_PATH = '/gh/hugolpz/audio-cmn@f759a0f18f27690742957619e1248ed91e9b3f2c/64k/syllabs/';
const APP_FILES = ['./index.html', './luyen-so-tieng-trung.html', './manifest.webmanifest', './icon.svg', './icon.svg?v=41-gold-logo-stroke-practice-20261028', './icon-v41-192.png', './icon-v41-192.png?v=41-gold-logo-stroke-practice-20261028', './icon-v41-512.png', './icon-v41-512.png?v=41-gold-logo-stroke-practice-20261028', './apple-touch-icon-v41.png', './apple-touch-icon-v41.png?v=41-gold-logo-stroke-practice-20261028', './sw.js', './asr-worker.js', './asr-voice-worker.js', './asr-cloudflare-worker.js', './ocr-worker.js'];
const INDEX_URL = new URL('index.html', self.registration.scope).href;
async function withAudioRange(response, rangeHeader) {
  if (!rangeHeader || response.status !== 200) return response;
  const match = /^bytes=(\d*)-(\d*)$/i.exec(rangeHeader.trim());
  if (!match) return response;
  const blob = await response.clone().blob();
  const total = blob.size;
  let start = match[1] ? Number(match[1]) : 0;
  let end = match[2] ? Number(match[2]) : total - 1;
  if (!match[1] && match[2]) { const suffix = Number(match[2]); start = Math.max(0, total - suffix); end = total - 1; }
  if (!Number.isFinite(start) || !Number.isFinite(end) || start >= total || end < start) {
    return new Response(null, { status: 416, headers: { 'Content-Range': `bytes */${total}`, 'Accept-Ranges': 'bytes' } });
  }
  end = Math.min(end, total - 1);
  const part = blob.slice(start, end + 1, 'audio/mpeg');
  const headers = new Headers(response.headers);
  headers.set('Content-Type', 'audio/mpeg');
  headers.set('Content-Length', String(part.size));
  headers.set('Content-Range', `bytes ${start}-${end}/${total}`);
  headers.set('Accept-Ranges', 'bytes');
  return new Response(part, { status: 206, statusText: 'Partial Content', headers });
}
async function handlePinyinAudio(request, url) {
  const cache = await caches.open(PINYIN_AUDIO_CACHE);
  const cached = await cache.match(url.href);
  if (cached) return withAudioRange(cached, request.headers.get('range'));
  try {
    const networkRequest = new Request(url.href, { method: 'GET', mode: 'cors', credentials: 'omit' });
    const response = await fetch(networkRequest);
    if (response.ok && response.type !== 'opaque') {
      cache.put(url.href, response.clone()).catch(() => {});
      return withAudioRange(response, request.headers.get('range'));
    }
    return response;
  } catch (_) {
    return cached || Response.error();
  }
}
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    for (const file of APP_FILES) { try { await cache.add(file); } catch (_) {} }
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(key => key.startsWith('hoc-trung-app-shell-') && key !== CACHE_NAME).map(key => caches.delete(key)));
    await self.clients.claim();
  })());
});
self.addEventListener('fetch', event => {
  const request = event.request; const url = new URL(request.url);
  if (request.method === 'GET' && url.origin === PINYIN_AUDIO_ORIGIN && url.pathname.startsWith(PINYIN_AUDIO_PATH) && url.pathname.endsWith('.mp3')) {
    event.respondWith(handlePinyinAudio(request, url));
    return;
  }
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;
  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (response.ok) { const cache = await caches.open(CACHE_NAME); cache.put(INDEX_URL, response.clone()).catch(() => {}); }
        return response;
      } catch (_) { return (await caches.match(INDEX_URL)) || Response.error(); }
    })()); return;
  }
  event.respondWith((async () => {
    const cached = await caches.match(request); if (cached) return cached;
    const response = await fetch(request);
    if (response.ok && APP_FILES.some(file => new URL(file, self.registration.scope).href === url.href)) {
      const cache = await caches.open(CACHE_NAME); cache.put(request, response.clone()).catch(() => {});
    }
    return response;
  })());
});
