import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CSP } from '../csp';

const nginx = readFileSync(resolve(process.cwd(), 'nginx.conf'), 'utf8');
const dockerfile = readFileSync(resolve(process.cwd(), 'Dockerfile'), 'utf8');

describe('SEC-03 security headers of the web container', () => {
  it('nginx serves the same CSP as csp.ts, on the page and as a default', () => {
    const found = [...nginx.matchAll(/add_header Content-Security-Policy "([^"]+)"/g)].map((m) => m[1]);
    expect(found.length).toBeGreaterThanOrEqual(2);
    for (const v of found) expect(v).toBe(CSP);
  });

  it('the policy has no unsafe-inline and no unsafe-eval and no remote origin', () => {
    expect(CSP).not.toMatch(/unsafe-inline|unsafe-eval|https?:|\*/);
  });

  it('every location that sets a header repeats the nosniff and referrer headers (add_header does not inherit)', () => {
    for (const loc of ['/v1/', '/assets/', '/']) {
      const start = nginx.indexOf(`location ${loc} {`);
      expect(start, loc).toBeGreaterThan(-1);
      const block = nginx.slice(start, nginx.indexOf('\n    }', start));
      expect(block, loc).toContain('X-Content-Type-Options');
    }
  });

  it('the request log has neither the query string nor the client address', () => {
    const fmt = /log_format df '([^']+)'/.exec(nginx)?.[1] ?? '';
    expect(fmt).toContain('$uri');
    expect(fmt).not.toMatch(/\$request\b|\$request_uri|\$args|\$query_string|\$remote_addr|\$http_x_forwarded_for/);
  });

  it('proxies /v1 and /healthz to the api service and bounds the body size', () => {
    expect(nginx).toMatch(/location \/v1\/ \{[^}]*proxy_pass http:\/\/api:8000/s);
    expect(nginx).toMatch(/location = \/healthz \{[^}]*proxy_pass http:\/\/api:8000/s);
    expect(nginx).toMatch(/client_max_body_size 8k;/);
  });

  it('the Dockerfile runs as the unprivileged nginx image and does not copy node_modules or tests', () => {
    expect(dockerfile).toContain('nginxinc/nginx-unprivileged');
    expect(dockerfile).not.toMatch(/COPY .*(tests|node_modules)/);
  });
});
