import { defineConfig, devices } from '@playwright/test';

// The e2e suite runs against the Vite dev server with the mock API (VITE_MOCK=1), so it needs no backend.
// Against the real stack, start `make -C ../ dev-api` and `npm run dev`, then run with E2E_REAL=1.
const real = process.env.E2E_REAL === '1';
// E2E_PREVIEW=1 serves the production build (with the CSP of the nginx container) and the mock API.
const preview = process.env.E2E_PREVIEW === '1';
const port = preview ? 4173 : 5173;
// E2E_BASE_URL (with E2E_REAL=1) points the real-backend specs at a running stack, e.g. the Docker web container
// http://127.0.0.1:8080 (make docker-e2e); then no local server is started.
const external = real ? process.env.E2E_BASE_URL : undefined;

export default defineConfig({
  testDir: './e2e',
  // Against the real backend only e2e/real.spec.ts runs: the other specs rely on mock fixtures such as tile 5 of A6NMZ7.
  testMatch: real ? /(real|screenshots)\.spec\.ts/ : /(flows|narrow|design|workspace|matrix|visual)\.spec\.ts/,
  // Against the real backend the default model may be LoRA-D (~40 s per tile on the CPU, plan 2.12): longer budgets there.
  timeout: real ? 900_000 : 60_000,
  expect: { timeout: real ? 180_000 : 5_000 },
  fullyParallel: false,
  workers: 1,
  reporter: [['list']],
  use: {
    baseURL: external ?? `http://localhost:${port}`,
    trace: 'off',
    // The first-visit guide (plan-system 5.1) is marked as seen; e2e/onboarding tests start from an empty storage.
    storageState: { cookies: [], origins: [{ origin: new URL(external ?? `http://localhost:${port}`).origin, localStorage: [{ name: 'df-onboarding-done', value: '1' }] }] },
  },
  webServer: external ? undefined : {
    command: preview ? 'VITE_MOCK=1 npx vite preview' : real ? 'npx vite' : 'VITE_MOCK=1 npx vite',
    url: `http://localhost:${port}`,
    reuseExistingServer: true,
    timeout: 60_000,
  },
  projects: [
    { name: 'chromium-desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } }, testIgnore: /narrow\.spec\.ts/ },
    // WP11.2: the browser × width matrix also runs in Firefox and WebKit (NFR-12)
    { name: 'firefox-matrix', use: { ...devices['Desktop Firefox'] }, testMatch: /matrix\.spec\.ts/ },
    { name: 'webkit-matrix', use: { ...devices['Desktop Safari'] }, testMatch: /matrix\.spec\.ts/ },
    { name: 'chromium-narrow', use: { ...devices['Desktop Chrome'], viewport: { width: 360, height: 800 } }, testMatch: /narrow\.spec\.ts/ },
  ],
});
