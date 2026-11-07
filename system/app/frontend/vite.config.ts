import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { mockApiPlugin } from './mock/vitePlugin';
import { CSP } from './csp';

// VITE_MOCK=1 serves the API from mock/handler.ts (no backend needed).
// Otherwise /v1 and /healthz are proxied to the FastAPI service, so the browser only talks to one origin.
const useMock = process.env.VITE_MOCK === '1';
const apiTarget = process.env.API_TARGET ?? 'http://127.0.0.1:8000';

export default defineConfig({
  plugins: [react(), ...(useMock ? [mockApiPlugin()] : [])],
  server: {
    port: 5173,
    strictPort: true,
    proxy: useMock
      ? undefined
      : {
          '/v1': { target: apiTarget, changeOrigin: false },
          '/healthz': { target: apiTarget, changeOrigin: false },
        },
  },
  // `vite preview` serves the production build with the same policy as the nginx container.
  preview: { port: 4173, strictPort: true, headers: { 'Content-Security-Policy': CSP, 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer' } },
  build: { sourcemap: false, target: 'es2022' },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    include: ['tests/**/*.test.{ts,tsx}'],
    env: { VITE_API_BASE: 'http://api.test' },
    css: false,
    // A result page renders 560 SVG cells and 532 table rows; jsdom needs more than the default 5 s for the longest flows.
    testTimeout: 20_000,
  },
});
