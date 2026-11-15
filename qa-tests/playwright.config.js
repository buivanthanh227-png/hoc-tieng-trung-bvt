const { defineConfig, devices } = require('@playwright/test');

const BASE_URL = process.env.BASE_URL || 'https://buivanthanh227-png.github.io/hoc-tieng-trung-bvt/';
const OUTPUT_DIR = process.env.QA_OUTPUT_DIR || 'test-results';

module.exports = defineConfig({
  testDir: './tests',
  outputDir: OUTPUT_DIR,
  timeout: 60_000,
  expect: { timeout: 8_000 },
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 3 : undefined,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: OUTPUT_DIR + '/results.json' }]
  ],
  use: {
    baseURL: BASE_URL,
    actionTimeout: 10_000,
    navigationTimeout: 30_000,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    serviceWorkers: 'allow'
  },
  projects: [
    { name: 'chromium-desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1366, height: 768 } } },
    { name: 'chromium-small-mobile', use: { ...devices['iPhone SE'], browserName: 'chromium', viewport: { width: 360, height: 800 }, isMobile: true, hasTouch: true } },
    { name: 'chromium-android', use: { ...devices['Pixel 7'], browserName: 'chromium' } },
    { name: 'webkit-iphone', use: { ...devices['iPhone 13'], browserName: 'webkit' } },
    { name: 'webkit-ipad', use: { ...devices['iPad (gen 7)'], browserName: 'webkit' } }
  ]
});