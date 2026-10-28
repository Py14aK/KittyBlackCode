import { defineConfig, devices } from '@playwright/test';
import { existsSync, readFileSync } from 'node:fs';

// Minimal .env loader (no dotenv dependency: fewer packages to carry into a closed network)
if (existsSync('.env')) for (const line of readFileSync('.env', 'utf8').split(/\r?\n/)) {
  const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*([^#]*?)\s*(#.*)?$/);
  if (m && process.env[m[1]] === undefined) process.env[m[1]] = m[2];
}
const mock = process.env.T24_TARGET === 'mock';
const port = Number(process.env.MOCK_PORT ?? 4824);
if (mock) process.env.T24_BASE_URL = `http://localhost:${port}/`;

export default defineConfig({
  testDir: 'tests',
  timeout: 90_000,                 // T24 screens are slow; per-action waits stay auto
  expect: { timeout: 15_000 },
  workers: 1,                      // one T24 session at a time: shared records, locks, COB
  fullyParallel: false,
  retries: 0,                      // a flaky T24 test is a finding, not something to hide
  reporter: [
    ['list'],
    ['html', { outputFolder: 'reports/html', open: 'never' }],
    ['./src/util/xray-reporter.ts'],
  ],
  use: {
    baseURL: process.env.T24_BASE_URL,
    ignoreHTTPSErrors: true,       // internal CA / self-signed on SYT
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    video: 'off',
    actionTimeout: 20_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'edge', use: { ...devices['Desktop Edge'], channel: 'msedge' } },
  ],
  webServer: mock
    ? { command: `node mock/server.mjs ${port}`, url: `http://localhost:${port}/`, reuseExistingServer: true }
    : undefined,
});
