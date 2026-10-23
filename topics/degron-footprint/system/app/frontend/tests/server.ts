import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { handle } from '../mock/handler';

export const API = 'http://api.test';

/** Every API call of the interface goes through the same pure handler that backs `npm run dev:mock`. */
export const server = setupServer(
  http.all(`${API}/*`, async ({ request }) => {
    const url = new URL(request.url);
    const headers: Record<string, string> = {};
    request.headers.forEach((v, k) => {
      headers[k.toLowerCase()] = v;
    });
    const out = handle(request.method, url.pathname + url.search, headers, request.method === 'GET' ? '' : await request.text());
    return new HttpResponse(out.body, { status: out.status, headers: out.headers });
  }),
);

export { http, HttpResponse };
