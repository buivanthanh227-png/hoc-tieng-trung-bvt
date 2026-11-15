const { test, expect, openApplication, discoverMenuItems, clickMenuItem, getPageSnapshot, attachJson } = require('./helpers');

const MAX_MENU_SLOTS = 24;
for (let slot = 0; slot < MAX_MENU_SLOTS; slot += 1) {
  test('Menu ' + String(slot + 1).padStart(2, '0') + ': mở, chuyển trạng thái và mở lại', async ({ page }, testInfo) => {
    await openApplication(page);
    const menus = await discoverMenuItems(page);
    if (slot >= menus.length) test.skip(true, 'Website hiện chỉ phát hiện ' + menus.length + ' menu.');
    const item = menus[slot];
    await clickMenuItem(page, item);
    const first = await getPageSnapshot(page);
    expect(first.textLength, 'Menu không hiển thị nội dung: ' + item.label).toBeGreaterThan(25);

    const menusAgain = await discoverMenuItems(page);
    const current = menusAgain.find(candidate => candidate.label === item.label) || menusAgain[slot];
    if (current) {
      await clickMenuItem(page, current);
      const second = await getPageSnapshot(page);
      expect(second.textLength, 'Nội dung biến mất khi mở lại menu: ' + item.label).toBeGreaterThan(25);
    }
    await attachJson(testInfo, 'menu-' + (slot + 1) + '-snapshot.json', {
      menu: item.label,
      firstState: { textLength: first.textLength, textSample: first.textSample.slice(0, 1200) },
      secondOpen: Boolean(current)
    });
    if (process.env.QA_ATTACH_EVERY_SCREEN === '1') {
      await testInfo.attach('menu-' + (slot + 1) + '.png', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
    }
  });
}