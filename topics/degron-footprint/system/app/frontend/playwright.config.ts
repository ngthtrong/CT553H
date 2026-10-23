import { defineConfig, devices } from '@playwright/test';

// The e2e suite runs against the Vite dev server with the mock API (VITE_MOCK=1), so it needs no backend.
// Against the real stack, start `make -C ../ dev-api` and `npm run dev`, then run with E2E_REAL=1.
const real = process.env.E2E_REAL === '1';
// E2E_PREVIEW=1 serves the production build (with the CSP of the nginx container) and the mock API.
const preview = process.env.E2E_PREVIEW === '1';
const port = preview ? 4173 : 5173;

export default defineConfig({
  testDir: './e2e',
  // Against the real backend only e2e/real.spec.ts runs: the other specs rely on mock fixtures such as tile 5 of A6NMZ7.
  testMatch: real ? /real\.spec\.ts/ : /(flows|narrow)\.spec\.ts/,
  timeout: 60_000,
  fullyParallel: false,
  workers: 1,
  reporter: [['list']],
  use: { baseURL: `http://localhost:${port}`, trace: 'off' },
  webServer: {
    command: preview ? 'VITE_MOCK=1 npx vite preview' : real ? 'npx vite' : 'VITE_MOCK=1 npx vite',
    url: `http://localhost:${port}`,
    reuseExistingServer: true,
    timeout: 60_000,
  },
  projects: [
    { name: 'chromium-desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } }, testIgnore: /narrow\.spec\.ts/ },
    { name: 'chromium-narrow', use: { ...devices['Desktop Chrome'], viewport: { width: 360, height: 800 } }, testMatch: /narrow\.spec\.ts/ },
  ],
});
