const fc = require('fast-check');
const { test, expect, openApplication, discoverMenuItems, clickMenuItem, getPageSnapshot, attachJson } = require('./helpers');

test('Stress navigation: bao phủ mọi cặp menu + lượt chuyển ngẫu nhiên', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop', 'Stress navigation tập trung trên Chromium desktop để kiểm soát tải.');
  await openApplication(page);
  const menus = await discoverMenuItems(page);
  expect(menus.length).toBeGreaterThan(1);
  const seed = Number(process.env.QA_RANDOM_SEED || 20261115);
  const randomSteps = Number(process.env.QA_REPEAT_STEPS || 120);
  const trace = [];
  let pairCount = 0;
  try {
    // Test every directed origin -> destination pair. N menus = N*N transitions.
    for (const origin of menus) {
      for (const destination of menus) {
        const origins = await discoverMenuItems(page);
        const originNow = origins.find(item => item.label === origin.label);
        expect(originNow, 'Không tìm thấy menu nguồn: ' + origin.label).toBeTruthy();
        await clickMenuItem(page, originNow);
        const destinations = await discoverMenuItems(page);
        const destinationNow = destinations.find(item => item.label === destination.label);
        expect(destinationNow, 'Không tìm thấy menu đích: ' + destination.label).toBeTruthy();
        await clickMenuItem(page, destinationNow);
        const snapshot = await getPageSnapshot(page);
        expect(snapshot.textLength, 'Trang trắng khi chuyển ' + origin.label + ' -> ' + destination.label).toBeGreaterThan(20);
        trace.push({ kind: 'pairwise', from: origin.label, to: destination.label, textLength: snapshot.textLength });
        pairCount += 1;
      }
    }
    const arbitrary = fc.array(fc.integer({ min: 0, max: menus.length - 1 }), { minLength: randomSteps, maxLength: randomSteps });
    await fc.assert(fc.asyncProperty(arbitrary, async sequence => {
      for (let step = 0; step < sequence.length; step += 1) {
        const current = await discoverMenuItems(page);
        const item = current[sequence[step] % current.length];
        await clickMenuItem(page, item);
        const snapshot = await getPageSnapshot(page);
        expect(snapshot.textLength, 'Trang trắng ở bước ngẫu nhiên ' + (step + 1) + ': ' + item.label).toBeGreaterThan(20);
        trace.push({ kind: 'random', step: step + 1, menu: item.label, textLength: snapshot.textLength });
      }
    }), { seed, numRuns: 1, endOnFailure: true, verbose: true });
  } catch (error) {
    await attachJson(testInfo, 'repeat-navigation-failure-trace.json', { seed, pairCount, completedSteps: trace.length, trace, error: String(error) });
    throw error;
  }
  await attachJson(testInfo, 'repeat-navigation-trace.json', { seed, pairCount, randomSteps, completedSteps: trace.length, trace });
  expect(pairCount).toBe(menus.length * menus.length);
  expect(trace.length).toBe(pairCount + randomSteps);
});