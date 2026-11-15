const fc = require('fast-check');
const { test, expect, openApplication, discoverMenuItems, clickMenuItem, getPageSnapshot, attachJson } = require('./helpers');

test('Stress navigation: 120 lượt chuyển menu ngẫu nhiên có seed', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop', 'Stress navigation tập trung trên Chromium desktop.');
  await openApplication(page);
  const menus = await discoverMenuItems(page);
  expect(menus.length).toBeGreaterThan(1);
  const seed = Number(process.env.QA_RANDOM_SEED || 20261115);
  const stepCount = Number(process.env.QA_REPEAT_STEPS || 120);
  const trace = [];
  const arbitrary = fc.array(fc.integer({ min: 0, max: menus.length - 1 }), { minLength: stepCount, maxLength: stepCount });
  await fc.assert(
    fc.asyncProperty(arbitrary, async sequence => {
      for (let step = 0; step < sequence.length; step += 1) {
        const current = await discoverMenuItems(page);
        const item = current[sequence[step] % current.length];
        await clickMenuItem(page, item);
        const snapshot = await getPageSnapshot(page);
        expect(snapshot.textLength, 'Trang trắng ở bước ' + (step + 1) + ', menu ' + item.label).toBeGreaterThan(20);
        trace.push({ step: step + 1, menu: item.label, textLength: snapshot.textLength });
      }
    }),
    { seed, numRuns: 1, endOnFailure: true, verbose: true }
  );
  await attachJson(testInfo, 'repeat-navigation-trace.json', { seed, stepCount, completedSteps: trace.length, trace });
  expect(trace.length).toBe(stepCount);
});