'use strict';
const CACHE_NAME = 'hoc-trung-app-shell-v42-10-22-menu3-pinyin-composition-turnstile-12s';
const PINYIN_AUDIO_CACHE = 'bvt-pinyin-audio-assets-v42-10';
const PINYIN_AUDIO_ORIGIN = 'https://cdn.jsdelivr.net';
const PINYIN_AUDIO_PATH = '/gh/hugolpz/audio-cmn@f759a0f18f27690742957619e1248ed91e9b3f2c/64k/syllabs/';
const LOCAL_PINYIN_AUDIO_ENABLED = true; // Prefer repository-hosted 24k-abr MP3; CDN remains fallback.

// These paths are the documents actually published by deploy-pages.yml.
// Keep the required shell small and deterministic; optional workers/icons may
// fail to cache without falsely reporting the core offline installation as ready.
const REQUIRED_APP_FILES = [
  './index.html',
  './luyen-so/index.html',
  './manifest.webmanifest'
];
const OPTIONAL_APP_FILES = [
  './icon.svg',
  './icon.svg?v=41-gold-logo-stroke-practice-20261028',
  './icon-v41-192.png',
  './icon-v41-192.png?v=41-gold-logo-stroke-practice-20261028',
  './icon-v41-512.png',
  './icon-v41-512.png?v=41-gold-logo-stroke-practice-20261028',
  './apple-touch-icon-v41.png',
  './apple-touch-icon-v41.png?v=41-gold-logo-stroke-practice-20261028',
  './asr-worker.js',
  './asr-voice-worker.js',
  './asr-cloudflare-worker.js',
  './ocr-worker.js'
];
const APP_FILES = REQUIRED_APP_FILES.concat(OPTIONAL_APP_FILES);
const INDEX_URL = new URL('index.html', self.registration.scope).href;

function navigationCacheKey(input) {
  const url = new URL(typeof input === 'string' ? input : input.url);
  // GitHub Pages serves a directory URL from its index.html document. Map
  // /path/ and /path/index.html to the same offline cache entry.
  url.search = '';
  url.hash = '';
  if (url.pathname.endsWith('/')) url.pathname += 'index.html';
  return url.href;
}

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
    return new Response(null, { status: 416, headers: { 'Content-Range': 'bytes */' + total, 'Accept-Ranges': 'bytes' } });
  }
  end = Math.min(end, total - 1);
  const part = blob.slice(start, end + 1, 'audio/mpeg');
  const headers = new Headers(response.headers);
  headers.set('Content-Type', 'audio/mpeg');
  headers.set('Content-Length', String(part.size));
  headers.set('Content-Range', 'bytes ' + start + '-' + end + '/' + total);
  headers.set('Accept-Ranges', 'bytes');
  return new Response(part, { status: 206, statusText: 'Partial Content', headers });
}

async function handlePinyinAudio(request, url) {
  const cache = await caches.open(PINYIN_AUDIO_CACHE);
  const range = request.headers.get('range');
  // Prefer the MP3 bundled in this repository. Keep the original CDN URL
  // as a compatibility key so the app's existing AUDIO_BASE need not change.
  const fileName = url.pathname.slice(PINYIN_AUDIO_PATH.length);
  const localUrl = new URL('audio/pinyin/' + fileName, self.registration.scope);
  if (LOCAL_PINYIN_AUDIO_ENABLED) try {
    let local = await cache.match(localUrl.href);
    if (!local) {
      const localResponse = await fetch(new Request(localUrl.href, { method: 'GET' }));
      if (localResponse.ok && localResponse.type !== 'opaque') {
        local = localResponse.clone();
        cache.put(localUrl.href, localResponse.clone()).catch(() => {});
      }
    }
    if (local) {
      cache.put(url.href, local.clone()).catch(() => {});
      return withAudioRange(local, range);
    }
  } catch (_) {}
  // Fallback to the pinned upstream CDN if a local asset is absent.
  const cached = await cache.match(url.href);
  if (cached) return withAudioRange(cached, range);
  try {
    const networkRequest = new Request(url.href, { method: 'GET', mode: 'cors', credentials: 'omit' });
    const response = await fetch(networkRequest);
    if (response.ok && response.type !== 'opaque') {
      cache.put(url.href, response.clone()).catch(() => {});
      return withAudioRange(response, range);
    }
    return response;
  } catch (_) {
    return cached || Response.error();
  }
}

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    try {
      // Cache.addAll rejects if any required document/manifest is unavailable.
      // On failure, remove the incomplete cache and keep the previously active SW.
      await cache.addAll(REQUIRED_APP_FILES);
    } catch (error) {
      await caches.delete(CACHE_NAME);
      throw error;
    }

    const optionalResults = await Promise.allSettled(
      OPTIONAL_APP_FILES.map(file => cache.add(file))
    );
    optionalResults.forEach((result, index) => {
      if (result.status === 'rejected') {
        console.warn('[SW] Optional asset was not precached: ' + OPTIONAL_APP_FILES[index], result.reason);
      }
    });
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
  const request = event.request;
  const url = new URL(request.url);
  if (request.method === 'GET' && url.origin === PINYIN_AUDIO_ORIGIN && url.pathname.startsWith(PINYIN_AUDIO_PATH) && url.pathname.endsWith('.mp3')) {
    event.respondWith(handlePinyinAudio(request, url));
    return;
  }
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      const cacheKey = navigationCacheKey(request.url);
      try {
      const response = await fetch(new Request(request, { cache: 'no-store' }));
        if (response.ok) {
          const cache = await caches.open(CACHE_NAME);
          cache.put(cacheKey, response.clone()).catch(() => {});
        }
        return response;
      } catch (_) {
        // Serve only the matching document. Never substitute the home page for
        // an unrelated offline URL (for example, the number-practice page).
        return (await caches.match(cacheKey)) || Response.error();
      }
    })());
    return;
  }

  event.respondWith((async () => {
    const cached = await caches.match(request);
    if (cached) return cached;
    const response = await fetch(request);
    if (response.ok && APP_FILES.some(file => new URL(file, self.registration.scope).href === url.href)) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone()).catch(() => {});
    }
    return response;
  })());
});
