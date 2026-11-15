const { test, expect, openApplication, getPageSnapshot, attachJson } = require('./helpers');

test('PWA: thử tải lại trang chính khi offline', async ({ page, context }, testInfo) => {
  test.skip(process.env.RUN_OFFLINE_TESTS !== '1', 'Chạy riêng bằng RUN_OFFLINE_TESTS=1.');
  test.skip(!testInfo.project.name.startsWith('chromium'), 'Offline PWA chỉ kiểm tra trong Chromium.');
  await openApplication(page);
  const before = await getPageSnapshot(page);
  const swState = await page.evaluate(async () => {
    if (!('serviceWorker' in navigator)) return { supported: false, controller: false, registrations: 0 };
    const registrations = await navigator.serviceWorker.getRegistrations();
    return { supported: true, controller: Boolean(navigator.serviceWorker.controller), registrations: registrations.length };
  });
  await attachJson(testInfo, 'pwa-before-offline.json', { before, swState });
  expect(swState.supported).toBe(true);
  await context.setOffline(true);
  await page.reload({ waitUntil: 'domcontentloaded', timeout: 20000 });
  const after = await getPageSnapshot(page);
  expect(after.textLength, 'Trang không khôi phục được từ cache offline').toBeGreaterThan(30);
  await context.setOffline(false);
});