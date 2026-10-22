import { ApiError, type ClientErrorCode } from './errors';
import type {
  ClinvarOverlay,
  DataSource,
  ExportFormat,
  Health,
  MeasuredOverlay,
  ModelCard,
  ModelSummary,
  PredictionResult,
  ProteinSummary,
  RunCreated,
  TileList,
  TileRequest,
} from './types';

// Empty in production and in the dev proxy (same origin). Tests point it at the MSW server.
const BASE: string = import.meta.env.VITE_API_BASE ?? '';

async function toApiError(res: Response): Promise<ApiError> {
  const requestId = res.headers.get('X-Request-Id');
  const ra = res.headers.get('Retry-After');
  const retryAfter = ra !== null && /^\d+$/.test(ra) ? Number(ra) : null;
  let code: ClientErrorCode = res.status === 503 ? 'SERVICE_UNAVAILABLE' : 'BAD_RESPONSE';
  let message = `The service answered with HTTP ${res.status}.`;
  let field: string | null = null;
  try {
    const body: unknown = await res.json();
    if (body && typeof body === 'object' && 'code' in body && 'message' in body) {
      const b = body as { code: ClientErrorCode; message: string; field?: string | null };
      code = b.code;
      message = b.message;
      field = b.field ?? null;
    }
  } catch {
    // A proxy error page (for example nginx 502) is not JSON; the generic message above stands.
  }
  return new ApiError({ status: res.status, code, message, field, retryAfter, requestId });
}

async function send(path: string, init: RequestInit = {}): Promise<Response> {
  let res: Response;
  try {
    res = await fetch(BASE + path, init);
  } catch (e) {
    if (e instanceof DOMException && e.name === 'AbortError') {
      throw new ApiError({ status: 0, code: 'ABORTED', message: 'The request was cancelled.' });
    }
    throw new ApiError({ status: 0, code: 'NETWORK', message: 'The service could not be reached.' });
  }
  if (!res.ok) throw await toApiError(res);
  return res;
}

async function json<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await send(path, init);
  try {
    return (await res.json()) as T;
  } catch {
    throw new ApiError({ status: res.status, code: 'BAD_RESPONSE', message: 'The service sent an unreadable answer.' });
  }
}

function post(body: unknown, signal?: AbortSignal): RequestInit {
  return { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal };
}

export const api = {
  predict: (req: TileRequest, signal?: AbortSignal) => json<PredictionResult>('/v1/predict', post(req, signal)),

  searchProteins: (query: string, signal?: AbortSignal) =>
    json<{ items: ProteinSummary[] }>(`/v1/proteins?query=${encodeURIComponent(query)}&limit=10`, { signal }),

  listTiles: (acc: string, signal?: AbortSignal) =>
    json<TileList>(`/v1/proteins/${encodeURIComponent(acc)}/tiles`, { signal }),

  getMeasured: (acc: string, n: number, signal?: AbortSignal) =>
    json<MeasuredOverlay>(`/v1/proteins/${encodeURIComponent(acc)}/tiles/${n}/measured`, { signal }),

  getClinvar: (acc: string, n: number, signal?: AbortSignal) =>
    json<ClinvarOverlay>(`/v1/proteins/${encodeURIComponent(acc)}/tiles/${n}/clinvar`, { signal }),

  listModels: (signal?: AbortSignal) => json<{ items: ModelSummary[] }>('/v1/models', { signal }),

  getModel: (id: string, signal?: AbortSignal) => json<ModelCard>(`/v1/models/${encodeURIComponent(id)}`, { signal }),

  listSources: (signal?: AbortSignal) => json<{ items: DataSource[] }>('/v1/sources', { signal }),

  createRun: (req: TileRequest, ttlDays: number, signal?: AbortSignal) =>
    json<RunCreated>('/v1/runs', post({ ...req, ttl_days: ttlDays }, signal)),

  getRun: (runId: string, token: string, signal?: AbortSignal) =>
    json<PredictionResult>(`/v1/runs/${encodeURIComponent(runId)}`, {
      headers: { 'X-Share-Token': token },
      signal,
    }),

  health: (signal?: AbortSignal) => json<Health>('/healthz', { signal }),

  /** Stateless export; nothing is stored on the server (POST /v1/export). */
  exportStateless: async (req: TileRequest, format: ExportFormat): Promise<Blob> =>
    (await send('/v1/export', post({ ...req, format }))).blob(),

  exportRun: async (runId: string, token: string, format: ExportFormat): Promise<Blob> =>
    (
      await send(`/v1/runs/${encodeURIComponent(runId)}/export?format=${format}`, {
        headers: { 'X-Share-Token': token },
      })
    ).blob(),
};
