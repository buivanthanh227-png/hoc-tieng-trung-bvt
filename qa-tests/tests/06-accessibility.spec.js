const AxeBuilder = require('@axe-core/playwright').default;
const { test, expect, openApplication, discoverMenuItems, clickMenuItem, attachJson } = require('./helpers');

test('Accessibility: rà soát WCAG trên trang chủ và từng menu', async ({ page }, testInfo) => {
  await openApplication(page);
  const menus = (await discoverMenuItems(page)).slice(0, 24);
  const scans = [];
  for (const item of [{ label: 'Trang đầu' }, ...menus]) {
    if (item.label !== 'Trang đầu') await clickMenuItem(page, item);
    const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    scans.push({ menu: item.label, violations: result.violations.map(v => ({ id: v.id, impact: v.impact, description: v.description, nodes: v.nodes.length, help: v.help })) });
  }
  const critical = scans.flatMap(scan => scan.violations.filter(v => v.impact === 'critical').map(v => ({ menu: scan.menu, ...v })));
  const serious = scans.flatMap(scan => scan.violations.filter(v => v.impact === 'serious').map(v => ({ menu: scan.menu, ...v })));
  await attachJson(testInfo, 'accessibility-findings.json', { scans, critical, serious });
  expect(critical, 'Có ' + critical.length + ' lỗi accessibility mức critical').toHaveLength(0);
});