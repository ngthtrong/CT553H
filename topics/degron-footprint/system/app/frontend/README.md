# Frontend of the Degron Footprint prototype

React 19 + TypeScript + Vite single-page application. It realises `system/ui-design.md` against `system/openapi.yaml` and `system/api-spec.md`. Status on 22 Oct 2026: all pages built; unit, browser and real-backend tests pass as listed in §4.

## 1. Run

Node is pinned in `.nvmrc` (v24.22.1). The machine that built this had no Node; it used the official tarball from nodejs.org, checked against `SHASUMS256.txt` (SHA-256 `6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6`), unpacked to `~/.local/node-v24.22.1-linux-x64` (no sudo), with its `bin` on `PATH`. The SHA-256 list comes from the same origin as the tarball, so it detects a corrupt download but is not a signature check. Every package is pinned to an exact version and `package-lock.json` is committed.

```bash
cd topics/degron-footprint/system/app/frontend
npm ci                      # install exactly the locked versions
npm run dev:mock            # http://localhost:5173 with the mock API (no backend)
npm run dev                 # http://localhost:5173, /v1 and /healthz proxied to http://127.0.0.1:8000
npm run build               # type check + production build in dist/
```

Against the real backend: `make -C topics/degron-footprint/system/app dev-api` in one terminal, `npm run dev` in another. The browser sees one origin, so the dev proxy needs no CORS (the backend also allows `http://localhost:5173`). `API_TARGET=http://host:port npm run dev` points the proxy elsewhere.

**The mock is not the model.** `mock/handler.ts` implements the contract (validation order, domain gate, error codes, exports, share runs) with synthetic numbers. Its model id is `mock-m3-ext4.0-platt-v1`, its evidence label ends with "MOCK FIXTURE: synthetic numbers, not model output", and its model card says so, so a mock screen cannot be mistaken for a real one. Only the first three cells of tile 28 of A6NMZ7 repeat documented values.

## 2. Decisions

| Topic | Decision | Why |
|---|---|---|
| Heatmap | **Custom SVG rendered by React, with `d3-scale` and `d3-scale-chromatic` for the colour scales; no Plotly** | ui-design §7 asks for one SVG, an ARIA grid with a single tab stop and arrow keys, hatched wild-type cells and a different marker per ClinVar class. Plotly gives none of that accessibility out of the box and adds megabytes. The whole app builds to 380 kB (123 kB gzip). |
| Ranking table | Own component (sort, filter, `aria-sort`), **not virtualised** | 532 rows render in one pass and keep native table semantics. Deviation from ui-design §3.3 ("virtualised"); revisit only if NF-06 is missed on the reference host. |
| Types | `src/api/schema.d.ts` generated from `../../openapi.yaml` by `openapi-typescript`; `npm run check:api` fails if it is stale | The contract cannot drift silently (ui-design §8). |
| Server state | TanStack Query; a typed sequence uses `gcTime: 0` | It must not outlive the page (ui-design §9). |
| Typed sequence | Held in a module variable (`state/requestStore.ts`); never in the address, history state, `localStorage` or `sessionStorage` | ui-design §3.1. A reload forgets it by design (the page says so). |
| Share token | Only in the URL fragment (`/shared/:id#t=…`), sent in `X-Share-Token` | api-spec §9. |
| Theme | `data-theme` set from the stored choice or the system preference; only the choice (`light`/`dark`) is stored | ui-design §5. |
| Warnings | Server warnings are shown; if the server omits the one its own domain status requires, the client adds it. A response without domain status, model id, evidence label or event definition is **not shown** ("Not shown" alert) | ui-design principle 1. |
| Empty input | The Predict button is disabled while the field is empty, with the reason written beside it | ui-design §3.1. E2E-08 "empty" is checked as a disabled button plus that hint. |

## 3. What is where

```
src/api/        client.ts (fetch wrapper, error mapping), errors.ts, types.ts, schema.d.ts (generated)
src/lib/        validate.ts (typed-tile rules), colors.ts, domain.ts (status text, warning fallback, "never show without…"),
                download.ts, theme.ts, hooks.ts, format.ts
src/components/ AppShell, SequenceInput, ProteinSearch, TileMap (+DomainLegend), DomainBanner, WarningList, EvidenceLabel,
                Heatmap (+ClinvarLegend), MatrixTable, ScaleToggle, LayerToggles, ClinvarNotice, RankTable, ExportMenu,
                ProvenanceFooter, RefusalNotice, ErrorBanner, ResultView
src/pages/      InputPage, TilePickerPage, ResultPage (stored and typed), SharedPage, ModelCardPage, AboutPage, NotFoundPage
mock/           handler.ts (pure mock of the API), vitePlugin.ts (dev and preview server middleware)
tests/          vitest: unit, component, flows against the mock through MSW, axe, contrast, security headers
e2e/            Playwright: flows.spec.ts and narrow.spec.ts (mock), real.spec.ts (real backend)
csp.ts, nginx.conf, Dockerfile   web container
```

Routes: `/`, `/protein/:acc`, `/result` (typed, in memory), `/result/uniprot/:acc/:n`, `/shared/:runId#t=TOKEN`, `/model`, `/about`.

## 4. Tests and checks (22 Oct 2026; WSL2, Node 24.22.1, Chromium 156)

| Check | Command | Result |
|---|---|---|
| Types | `npx tsc --noEmit` | no errors |
| Lint (typescript-eslint, react-hooks, jsx-a11y) | `npx eslint .` | no errors |
| Contract drift | `npm run check:api` | up to date |
| Unit, component, flows, a11y (jsdom) | `npx vitest run` | **9 files, 131 tests passed** |
| Production build | `npx vite build` | 380.0 kB JS (123.4 kB gzip), 8.3 kB CSS |
| Browser, mock API | `npx playwright test` (once: `npx playwright install chromium`) | 11 desktop tests and 1 at 360 px passed |
| Browser, production build under the CSP | `npx vite build && E2E_PREVIEW=1 npx playwright test -g "E2E-0\|E2E-1\|A11Y-02\|NF-06"` | 9 passed, no CSP violation |
| Browser, **real backend** | `make -C ../ dev-api`, then `E2E_REAL=1 npx playwright test --project=chromium-desktop` | 10 passed |
| Dependencies | `npm audit --audit-level=high` | 0 vulnerabilities |

Coverage of `test-plan.md`: E2E-01, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12; A11Y-01 (axe with colour contrast in Chromium, light and dark, on Input, Tile picker, Result with both layers, Result with unreliable and out-of-domain tiles, Model card, About; jsdom axe without the contrast rule on more states); A11Y-02 (keyboard only); A11Y-04 (token contrast, `tests/contrast.test.ts`); SEC-03 (headers); SEC-05 (`npm audit`).

**Not done:**
* **A11Y-03.** Nobody looked at the interface through a colour-vision simulator. The design carries every status in a pattern, shape or word, and the tests check that those are present, not that they are legible.
* **E2E-02** (sort and filter) runs only in jsdom; **E2E-11 expiry** only in jsdom against the mock.
* Only Chromium ran; Firefox, Safari and Edge did not.
* **NF-06 is not measured.** `e2e/flows.spec.ts` prints the time from clicking Predict to the painted heatmap on the **mock** (about 90 to 340 ms over five runs here) and only guards against a gross regression. The measurement of record (20 runs, reference host, real API) remains to do.

## 5. Web container

`Dockerfile` (multi-stage: `node:24.22.1-alpine` builds; `nginxinc/nginx-unprivileged:1.27-alpine` serves on **port 8080**) and `nginx.conf`. For `docker-compose.yml`:

* service **`web`**, `build: ./frontend`, publishes `8080`;
* it proxies `/v1/` and `/healthz` to the service **`api`** on port **8000**, so name the API service `api`;
* the CSP in `nginx.conf` equals `csp.ts` (a test checks it). It forbids inline scripts and styles; React sets styles through the DOM, which the policy allows, and Chromium under the same policy (`E2E_PREVIEW=1`) reports no violation;
* the access log has neither the query string nor the client address (api-spec §9); `client_max_body_size` is 8k.

**Not tested:** Docker is not installed on this machine, so the image was never built and `nginx.conf` never went through `nginx -t`. What ran is each step by hand (`npm ci`, `vite build`) and the headers through `vite preview`. The image tags are not pinned to digests. DEP-01 will be the first real test.

## 6. Gaps and notes for the backend and the documents

* **Model card "Sources not used" (closed 22 Oct 2026).** The list now comes from the API (`ModelCard.not_used_sources`); the page renders it in its own section and the card Markdown no longer carries it. Tested in `tests/flows.test.tsx` (mock) and `e2e/real.spec.ts` (real backend).
* The overlay endpoints answer `404 TILE_OUT_OF_RANGE` for a tile that does not exist, as the mock does; `openapi.yaml` now documents this (404 for the overlays, 422 for `predict`/`export`/`runs`). The real backend does the same.
* Export errors appear as an inline `role="alert"` message beside the buttons; there is no separate toast.
* The dark theme and the 360 px layout were checked with automatic rules and one narrow test, not by a person.
