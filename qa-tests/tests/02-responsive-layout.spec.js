const { test, expect, openApplication, discoverMenuItems, clickMenuItem, getPageSnapshot, attachJson } = require('./helpers');

test('Responsive + font: kiểm tra bố cục của tất cả menu trên viewport hiện tại', async ({ page }, testInfo) => {
  await openApplication(page);
  const menus = (await discoverMenuItems(page)).slice(0, 24);
  expect(menus.length).toBeGreaterThan(0);
  const findings = [];
  for (const item of [{ label: 'Trang đầu' }, ...menus]) {
    if (item.label !== 'Trang đầu') await clickMenuItem(page, item);
    const state = await getPageSnapshot(page);
    const overflow = state.document.scrollWidth - state.document.clientWidth;
    findings.push({ menu: item.label, ...state.document, viewport: state.viewport, horizontalOverflowPx: overflow, replacementCharacterCount: state.replacementCharacterCount, fontAudit: state.fontAudit });\n    if (process.env.QA_CAPTURE_VISUALS === '1') {\n      await testInfo.attach('visual-' + findings.length + '-' + item.label.replace(/[^a-z0-9]/gi, '-') + '.png', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });\n    }
    expect(state.textLength, 'Menu bị rỗng: ' + item.label).toBeGreaterThan(20);
    expect(state.replacementCharacterCount, 'Lỗi mã hóa tại: ' + item.label).toBe(0);
    if (state.viewport.width <= 430) {
      expect(overflow, 'Tràn ngang ' + overflow + 'px ở menu ' + item.label).toBeLessThanOrEqual(8);
    }
  }
  await attachJson(testInfo, 'responsive-layout-findings.json', findings);
});