import type { Connect, Plugin } from 'vite';
import { handle } from './handler';

/** Serves the mock API from the Vite dev and preview servers (`npm run dev:mock`), so no backend is needed. */
export function mockApiPlugin(): Plugin {
  const middleware: Connect.NextHandleFunction = (req, res, next) => {
    const url = req.url ?? '';
    if (!url.startsWith('/v1/') && !url.startsWith('/healthz')) return next();
    const chunks: Buffer[] = [];
    req.on('data', (c: Buffer) => chunks.push(c));
    req.on('end', () => {
      const headers: Record<string, string | undefined> = {};
      for (const [k, v] of Object.entries(req.headers)) headers[k.toLowerCase()] = Array.isArray(v) ? v.join(',') : v;
      const out = handle(req.method ?? 'GET', url, headers, Buffer.concat(chunks).toString('utf8'));
      res.statusCode = out.status;
      for (const [k, v] of Object.entries(out.headers)) res.setHeader(k, v);
      res.end(out.body);
    });
  };
  return {
    name: 'degron-footprint-mock-api',
    configureServer(server) {
      server.middlewares.use(middleware);
    },
    configurePreviewServer(server) {
      server.middlewares.use(middleware);
    },
  };
}
