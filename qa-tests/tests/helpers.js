const { test: base, expect } = require('@playwright/test');

const CLICKABLE_SELECTOR = 'button, a[href], [role="button"], [role="tab"], [tabindex="0"]';
const MENU_TEXT_HINT = /từ điển|luyện|dịch|ghép|nhận diện|bộ thủ|tài liệu|pinyin|thanh mẫu|vận mẫu|hán tự|tiếng trung|phản xạ/i;

function normalizeText(value) {
  return String(value || '').replace(/\\s+/g, ' ').trim();
}

async function openApplication(page) {
  const response = await page.goto('/', { waitUntil: 'domcontentloaded' });
  await page.locator('body').waitFor({ state: 'visible' });
  await page.waitForTimeout(900);
  await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
  return response;
}

async function discoverMenuItems(page) {
  const raw = await page.locator(CLICKABLE_SELECTOR).evaluateAll((elements) => elements.map((el, index) => {
    const text = (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const label = (el.getAttribute('aria-label') || el.getAttribute('title') || text).trim();
    const scope = el.closest('nav, aside, [role="navigation"], [class*="sidebar" i], [class*="menu" i], [id*="menu" i]');
    const disabled = el.disabled || el.getAttribute('aria-disabled') === 'true';
    return { index, label, disabled, inNavigationScope: Boolean(scope), tag: el.tagName.toLowerCase() };
  }));
  const usable = raw.filter(item => item.label && !item.disabled && item.label.length <= 110);
  const numbered = usable.filter(item => /^\\d{1,2}(?:\\s|[.)\\-:]|$)/.test(normalizeText(item.label)));
  let candidates = numbered.length ? numbered : usable.filter(item => item.inNavigationScope || MENU_TEXT_HINT.test(item.label));
  const seen = new Set();
  candidates = candidates.filter(item => {
    const key = normalizeText(item.label).toLocaleLowerCase('vi');
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  candidates.sort((a, b) => {
    const an = Number((normalizeText(a.label).match(/^(\\d{1,2})/) || [])[1] || 999);
    const bn = Number((normalizeText(b.label).match(/^(\\d{1,2})/) || [])[1] || 999);
    return an - bn || a.index - b.index;
  });
  return candidates;
}

async function clickMenuItem(page, item) {
  const target = page.locator(CLICKABLE_SELECTOR).nth(item.index);
  await expect(target).toBeVisible({ timeout: 5000 });
  await target.click({ timeout: 7000 });
  await page.waitForTimeout(250);
}

async function getPageSnapshot(page) {
  return page.evaluate(() => {
    const bodyText = document.body?.innerText || '';
    const root = document.documentElement;
    const body = document.body;
    return {
      title: document.title || '',
      textLength: bodyText.trim().length,
      textSample: bodyText.slice(0, 4000),
      viewport: { width: innerWidth, height: innerHeight },
      document: {
        clientWidth: root?.clientWidth || 0,
        scrollWidth: Math.max(root?.scrollWidth || 0, body?.scrollWidth || 0),
        clientHeight: root?.clientHeight || 0,
        scrollHeight: Math.max(root?.scrollHeight || 0, body?.scrollHeight || 0)
      },
      replacementCharacterCount: (bodyText.match(/\\uFFFD/g) || []).length
    };
  });
}

async function getVisibleTextFields(page, maxFields = 8) {
  const all = await page.locator('input:not([type="hidden"]):not([type="file"]):not([type="password"]), textarea').evaluateAll(elements => elements.map((el, index) => {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    const visible = rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
    return {
      index,
      type: (el.getAttribute('type') || 'text').toLowerCase(),
      label: el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.name || el.id || ('field-' + index),
      visible
    };
  }));
  return all.filter(item => item.visible && ['text', 'search', 'number', 'tel', 'email', 'url'].includes(item.type)).slice(0, maxFields);
}

async function attachJson(testInfo, name, value) {
  await testInfo.attach(name, { body: Buffer.from(JSON.stringify(value, null, 2), 'utf8'), contentType: 'application/json' });
}

const test = base.extend({
  diagnostics: [async ({ page }, use, testInfo) => {
    const data = { pageErrors: [], consoleErrors: [], failedRequests: [], badResponses: [] };
    page.on('pageerror', error => data.pageErrors.push({ message: error.message, stack: error.stack || '' }));
    page.on('console', message => { if (message.type() === 'error') data.consoleErrors.push(message.text()); });
    page.on('requestfailed', request => data.failedRequests.push({ url: request.url(), error: request.failure()?.errorText || 'request failed' }));
    page.on('response', response => { if (response.status() >= 400) data.badResponses.push({ status: response.status(), url: response.url() }); });
    await use(data);
    await page.waitForTimeout(150);
    await attachJson(testInfo, 'browser-diagnostics.json', data);
    if (data.pageErrors.length) {
      throw new Error('Phát hiện ' + data.pageErrors.length + ' lỗi JavaScript: ' + data.pageErrors.slice(0, 5).map(x => x.message).join(' | '));
    }
  }, { auto: true }]
});

module.exports = { test, expect, CLICKABLE_SELECTOR, normalizeText, openApplication, discoverMenuItems, clickMenuItem, getPageSnapshot, getVisibleTextFields, attachJson };