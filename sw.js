'use strict';
const CACHE_NAME='hoc-trung-app-shell-v41-no-hsk-recognition-restart-20261028';
const APP_FILES = ['./index.html', './manifest.webmanifest', './icon.svg', './icon.svg?v=41-gold-logo-stroke-practice-20261028', './icon-v41-192.png', './icon-v41-192.png?v=41-gold-logo-stroke-practice-20261028', './icon-v41-512.png', './icon-v41-512.png?v=41-gold-logo-stroke-practice-20261028', './apple-touch-icon-v41.png', './apple-touch-icon-v41.png?v=41-gold-logo-stroke-practice-20261028', './sw.js', './asr-worker.js', './ocr-worker.js'];
const INDEX_URL = new URL('index.html', self.registration.scope).href;
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
