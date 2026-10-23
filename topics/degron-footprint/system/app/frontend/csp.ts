/**
 * Content-Security-Policy of the web container (test-plan SEC-03: no unsafe-inline).
 * nginx.conf carries the same string; tests/security-headers.test.ts fails if the two differ.
 * Inline `style` set by React goes through the CSSOM, which `style-src 'self'` allows.
 */
export const CSP = [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self'",
  "img-src 'self' data:",
  "connect-src 'self'",
  "base-uri 'none'",
  "form-action 'self'",
  "frame-ancestors 'none'",
].join('; ');
