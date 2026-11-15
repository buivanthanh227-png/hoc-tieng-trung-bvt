const { test, expect, openApplication, discoverMenuItems, clickMenuItem, getVisibleTextFields, attachJson } = require('./helpers');

const PAYLOADS = [
  '你好',
  'nǐ hǎo ā á ǎ à ǖ ǘ ǚ ǜ ü',
  'Xin chào, tôi đang học tiếng Trung.',
  '中文和越南语 mixed text 你好 Xin chào',
  'Dữ liệu dài thử nghiệm ' + '学习中文'.repeat(35),
  'Ký tự đặc biệt: \' " < > & / \\ ; : @ # %',
  '0123456789'
];

test('Input fuzz: Hán tự, Pinyin, tiếng Việt, chuỗi dài và ký tự đặc biệt', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop', 'Stress nhập liệu chạy trên Chromium desktop.');
  await openApplication(page);
  const menus = (await discoverMenuItems(page)).slice(0, 24);
  const results = [];
  let probes = 0;

  for (const item of menus) {
    await clickMenuItem(page, item);
    const fields = await getVisibleTextFields(page, 5);
    const menuResult = { menu: item.label, fields: [], payloadCount: 0 };
    for (const field of fields) {
      const locator = page.locator('input:not([type="hidden"]):not([type="file"]):not([type="password"]), textarea').nth(field.index);
      if (!(await locator.isVisible().catch(() => false))) continue;
      const original = await locator.inputValue().catch(() => '');
      const values = field.type === 'number' ? ['0', '1', '999999', '-1'] : PAYLOADS;
      const fieldResult = { label: field.label, type: field.type, tested: [] };
      for (const payload of values) {
        await locator.fill(payload);
        expect(await locator.inputValue(), 'Ô nhập không giữ được giá trị: ' + field.label).toBe(payload);
        fieldResult.tested.push({ length: payload.length, sample: payload.slice(0, 80) });
        menuResult.payloadCount += 1;
        probes += 1;
      }
      await locator.fill(original);
      menuResult.fields.push(fieldResult);
    }
    results.push(menuResult);
  }
  await attachJson(testInfo, 'input-fuzz-results.json', { totalProbes: probes, payloads: PAYLOADS, results });
  expect(probes, 'Không tìm được ô nhập liệu để kiểm thử').toBeGreaterThan(0);
});