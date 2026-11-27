'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const SOURCE = fs.readFileSync(path.join(__dirname, '..', 'sw.js'), 'utf8');
const SCOPE = 'https://pages.example.test/hoc-tieng-trung-bvt/';
const WORKER_URL = new URL('sw.js', SCOPE).href;
const CACHE_NAME = 'hoc-trung-app-shell-v42-10-27-menu3-race-fix-20261127';

function createHarness(options = {}) {
  const entries = new Map();
  const listeners = new Map();
  const warnings = [];
  const failedAssets = new Set(options.failedAssets || []);
  let offline = Boolean(options.offline);

  const toUrl = input => typeof input === 'string'
    ? new URL(input, WORKER_URL).href
    : input.url;

  const networkFetch = async input => {
    const url = toUrl(input);
    if (offline) throw new TypeError('Network unavailable');
    if (failedAssets.has(url)) return new Response('Not Found', { status: 404 });
    const body = url.includes('/luyen-so/')
      ? 'LUYEN_SO_DOCUMENT'
      : (options.homeHtml || 'HOME_DOCUMENT');
    return new Response(body, {
      status: 200,
      headers: { 'Content-Type': 'text/html; charset=utf-8' }
    });
  };

  const cache = {
    async addAll(files) {
      const staged = [];
      for (const file of files) {
        const url = new URL(file, WORKER_URL).href;
        const response = await networkFetch(new Request(url));
        if (!response.ok) throw new TypeError('Required asset failed: ' + url);
        staged.push([url, response.clone()]);
      }
      for (const [url, response] of staged) entries.set(url, response);
    },
    async add(file) {
      const url = new URL(file, WORKER_URL).href;
      const response = await networkFetch(new Request(url));
      if (!response.ok) throw new TypeError('Optional asset failed: ' + url);
      entries.set(url, response.clone());
    },
    async put(request, response) {
      entries.set(toUrl(request), response.clone());
    },
    async match(request) {
      const response = entries.get(toUrl(request));
      return response ? response.clone() : undefined;
    }
  };

  const caches = {
    async open() { return cache; },
    async match(request) { return cache.match(request); },
    async keys() { return [CACHE_NAME]; },
    async delete() { entries.clear(); return true; }
  };

  const self = {
    registration: { scope: SCOPE },
    location: { origin: new URL(SCOPE).origin },
    clients: { async claim() {} },
    addEventListener(type, handler) { listeners.set(type, handler); },
    async skipWaiting() {}
  };

  const sandbox = {
    self,
    caches,
    fetch: networkFetch,
    URL,
    Request,
    Response,
    Headers,
    Blob,
    Promise,
    Number,
    Math,
    RegExp,
    String,
    Error,
    TypeError,
    console: { warn: (...args) => warnings.push(args.join(' ')) }
  };
  vm.runInNewContext(SOURCE, sandbox, { filename: 'sw.js' });

  return {
    entries,
    warnings,
    setOffline(value) { offline = Boolean(value); },
    async install() {
      let pending;
      listeners.get('install')({ waitUntil(value) { pending = value; } });
      return pending;
    },
    async navigate(url) {
      let pending;
      const request = {
        method: 'GET',
        mode: 'navigate',
        url,
        headers: new Headers()
      };
      listeners.get('fetch')({
        request,
        respondWith(value) { pending = value; }
      });
      return pending;
    }
  };
}

test('required offline documents are precached and optional worker failures are reported', async () => {
  const failedWorker = new URL('asr-worker.js', SCOPE).href;
  const harness = createHarness({ failedAssets: [failedWorker] });

  await harness.install();

  assert.ok(harness.entries.has(new URL('index.html', SCOPE).href));
  assert.ok(harness.entries.has(new URL('luyen-so/index.html', SCOPE).href));
  assert.ok(harness.entries.has(new URL('manifest.webmanifest', SCOPE).href));
  assert.ok(harness.warnings.some(message => message.includes('asr-worker.js')));
});

test('failure to cache a required document aborts installation and clears its incomplete cache', async () => {
  const missingPage = new URL('luyen-so/index.html', SCOPE).href;
  const harness = createHarness({ failedAssets: [missingPage] });

  await assert.rejects(harness.install(), /Required asset failed/);
  assert.equal(harness.entries.size, 0);
});

test('offline navigation serves the matching document and never substitutes home for an unknown path', async () => {
  const harness = createHarness();
  await harness.install();
  harness.setOffline(true);

  const numberPractice = await harness.navigate(new URL('luyen-so/', SCOPE).href);
  assert.equal(numberPractice.status, 200);
  assert.equal(await numberPractice.text(), 'LUYEN_SO_DOCUMENT');

  const home = await harness.navigate(SCOPE);
  assert.equal(home.status, 200);
  assert.equal(await home.text(), 'HOME_DOCUMENT');

  const unknown = await harness.navigate(new URL('not-published/', SCOPE).href);
  assert.equal(unknown.status, 0);
});


test('Service Worker keeps Menu 3 runtime injection independent and cache-busted', () => {
  assert.match(SOURCE, /const patchUrl = new URL\('menu3-pinyin-fix-v42\.10\.23\.js\?v=42\.10\.23-racefix-20261127'/);
  assert.match(SOURCE, /const scriptTag = '<script id="bvt-v421023-menu3-runtime" src="'/);
  assert.match(SOURCE, /if \(!updated\.includes\('bvt-fix-right-menu-heading-typography-colors-v2'\)\)/);
  assert.match(SOURCE, /if \(!updated\.includes\('bvt-v421023-menu3-runtime'\) && !updated\.includes\(patchUrl\)\)/);
});

test('Service Worker cache namespace is bumped for the Menu 3 race-condition fix', () => {
  assert.match(SOURCE, /hoc-trung-app-shell-v42-10-27-menu3-race-fix-20261127/);
  assert.doesNotMatch(SOURCE, /hoc-trung-app-shell-v42-10-26-menu3-speech-fix-20261124/);
});
