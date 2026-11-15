const { test, expect, openApplication, getPageSnapshot, discoverMenuItems, attachJson } = require('./helpers');

test('Smoke: trang chính tải thành công và khám phá menu', async ({ page }, testInfo) => {
  const response = await openApplication(page);
  expect(response).not.toBeNull();
  expect(response.status()).toBe(200);
  const snapshot = await getPageSnapshot(page);
  expect(snapshot.textLength, 'Trang không được trắng hoặc rỗng').toBeGreaterThan(40);
  expect(snapshot.replacementCharacterCount, 'Có ký tự Unicode thay thế do lỗi mã hóa').toBe(0);
  const menus = await discoverMenuItems(page);
  await attachJson(testInfo, 'application-discovery.json', {
    url: page.url(),
    title: snapshot.title,
    versionText: (snapshot.textSample.match(/v\s?\d+(?:\.\d+)+/i) || [])[0] || 'Không đọc được',
    discoveredMenuCount: menus.length,
    menus: menus.map((item, index) => ({ order: index + 1, label: item.label, tag: item.tag }))
  });
  expect(menus.length, 'Không phát hiện được menu điều hướng').toBeGreaterThan(0);
});