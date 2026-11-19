import { ApiError, type ClientErrorCode } from './errors';
import type {
  AdminStatus,
  AgreementSeries,
  ClinvarOverlay,
  Comparison,
  ComparisonPage,
  ComparisonRequest,
  Dataset,
  DatasetPage,
  ImportMetadata,
  Job,
  JobFootprint,
  JobItemPage,
  ModelComparison,
  ModelComparisonPage,
  Suggestions,
  JobPage,
  JobRequest,
  Project,
  ProjectPage,
  SavedAnalysis,
  SavedAnalysisPage,
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
  let dependencies: Record<string, number> | null = null;
  try {
    const body: unknown = await res.json();
    if (body && typeof body === 'object' && 'code' in body && 'message' in body) {
      const b = body as { code: ClientErrorCode; message: string; field?: string | null; dependencies?: Record<string, number> };
      code = b.code;
      message = b.message;
      field = b.field ?? null;
      dependencies = b.dependencies ?? null;
    }
  } catch {
    // A proxy error page (for example nginx 502) is not JSON; the generic message above stands.
  }
  return new ApiError({ status: res.status, code, message, field, retryAfter, requestId, dependencies });
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

function jsonBody(method: string, body: unknown): RequestInit {
  return { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) };
}

const id = (v: string) => encodeURIComponent(v);
const pageQuery = (offset = 0, limit = 50) => `offset=${offset}&limit=${limit}`;

/** Workspace operations (projects, analyses, jobs, datasets, comparisons). Ids only in URLs, never sequences. */
export const workspace = {
  listProjects: (offset = 0, limit = 50, signal?: AbortSignal) => json<ProjectPage>(`/v1/projects?${pageQuery(offset, limit)}`, { signal }),
  createProject: (name: string, description = '') => json<Project>('/v1/projects', post({ name, description })),
  getProject: (pid: string, signal?: AbortSignal) => json<Project>(`/v1/projects/${id(pid)}`, { signal }),
  renameProject: (pid: string, body: { name?: string; description?: string }) => json<Project>(`/v1/projects/${id(pid)}`, jsonBody('PATCH', body)),
  /** Without confirm the server answers 409 with the dependency counts and deletes nothing. */
  deleteProject: async (pid: string, confirm: boolean) => {
    await send(`/v1/projects/${id(pid)}?confirm=${confirm}`, { method: 'DELETE' });
  },

  listAnalyses: (pid: string, offset = 0, limit = 50, signal?: AbortSignal) =>
    json<SavedAnalysisPage>(`/v1/projects/${id(pid)}/analyses?${pageQuery(offset, limit)}`, { signal }),
  saveAnalysis: (pid: string, request: TileRequest, parentAnalysisId?: string) =>
    json<SavedAnalysis>(`/v1/projects/${id(pid)}/analyses`, post(parentAnalysisId ? { request, parent_analysis_id: parentAnalysisId } : { request })),
  getAnalysis: (aid: string, signal?: AbortSignal) => json<SavedAnalysis>(`/v1/analyses/${id(aid)}`, { signal }),
  deleteAnalysis: async (aid: string, confirm: boolean) => {
    await send(`/v1/analyses/${id(aid)}?confirm=${confirm}`, { method: 'DELETE' });
  },
  /** plan-system 3.5: address of the self-contained HTML report (an id only); opened in a new tab, printed to PDF. */
  reportUrl: (aid: string) => `${BASE}/v1/analyses/${id(aid)}/report?format=html`,
  exportAnalysis: async (aid: string, format: ExportFormat, comparisonId?: string): Promise<Blob> =>
    (await send(`/v1/analyses/${id(aid)}/export?format=${format}${comparisonId ? `&comparison_id=${id(comparisonId)}` : ''}`)).blob(),

  listJobs: (pid: string, offset = 0, limit = 50, signal?: AbortSignal) => json<JobPage>(`/v1/projects/${id(pid)}/jobs?${pageQuery(offset, limit)}`, { signal }),
  submitJob: (pid: string, body: JobRequest) => json<Job>(`/v1/projects/${id(pid)}/jobs`, post(body)),
  getJob: (jid: string, signal?: AbortSignal) => json<Job>(`/v1/jobs/${id(jid)}`, { signal }),
  listJobItems: (jid: string, offset = 0, limit = 50, signal?: AbortSignal) => json<JobItemPage>(`/v1/jobs/${id(jid)}/items?${pageQuery(offset, limit)}`, { signal }),
  getJobFootprint: (jid: string, signal?: AbortSignal, inputId?: string) =>
    json<JobFootprint>(`/v1/jobs/${id(jid)}/footprint${inputId ? `?input_id=${encodeURIComponent(inputId)}` : ''}`, { signal }),
  cancelJob: (jid: string) => json<Job>(`/v1/jobs/${id(jid)}/cancel`, { method: 'POST' }),
  exportJob: async (jid: string, format: ExportFormat): Promise<Blob> => (await send(`/v1/jobs/${id(jid)}/export?format=${format}`)).blob(),

  listDatasets: (pid: string, offset = 0, limit = 50, signal?: AbortSignal) =>
    json<DatasetPage>(`/v1/projects/${id(pid)}/datasets?${pageQuery(offset, limit)}`, { signal }),
  previewImport: (pid: string, file: File, metadata: ImportMetadata) => {
    const form = new FormData();
    form.append('metadata', JSON.stringify(metadata));
    form.append('file', file);
    return json<Dataset>(`/v1/projects/${id(pid)}/datasets`, { method: 'POST', body: form });
  },
  getDataset: (did: string, signal?: AbortSignal) => json<Dataset>(`/v1/datasets/${id(did)}`, { signal }),
  commitDataset: (did: string, acknowledgeWarnings: boolean) =>
    json<Dataset>(`/v1/datasets/${id(did)}`, post({ action: 'commit', acknowledge_warnings: acknowledgeWarnings })),
  deleteDataset: async (did: string, confirm: boolean) => {
    await send(`/v1/datasets/${id(did)}?confirm=${confirm}`, { method: 'DELETE' });
  },

  /** plan-system 2.2: two saved analyses of one tile, usually two models; save=true stores it in the project. */
  compareAnalyses: (analysisA: string, analysisB: string, save = false) =>
    json<ModelComparison>('/v1/analyses/compare', post({ analysis_a: analysisA, analysis_b: analysisB, save })),
  getModelComparison: (cid: string, signal?: AbortSignal) => json<ModelComparison>(`/v1/model-comparisons/${id(cid)}`, { signal }),
  listModelComparisons: (pid: string, analysisId?: string, signal?: AbortSignal) =>
    json<ModelComparisonPage>(`/v1/projects/${id(pid)}/model-comparisons?limit=200${analysisId ? `&analysis_id=${id(analysisId)}` : ''}`, { signal }),
  exportModelComparison: async (cid: string, format: ExportFormat): Promise<Blob> =>
    (await send(`/v1/model-comparisons/${id(cid)}/export?format=${format}`)).blob(),
  /** plan-system 2.6: candidates to verify, optionally against another analysis of the same tile. */
  getSuggestions: (aid: string, compareWith?: string, signal?: AbortSignal) =>
    json<Suggestions>(`/v1/analyses/${id(aid)}/suggestions?limit=30${compareWith ? `&compare_with=${id(compareWith)}` : ''}`, { signal }),
  exportSuggestions: async (aid: string, compareWith?: string): Promise<Blob> =>
    (await send(`/v1/analyses/${id(aid)}/suggestions?limit=30&format=csv${compareWith ? `&compare_with=${id(compareWith)}` : ''}`)).blob(),
  /** plan-system 4.4: agreement with imported measurements over time (warnings only). */
  getAgreement: (pid: string, signal?: AbortSignal) => json<AgreementSeries>(`/v1/projects/${id(pid)}/agreement`, { signal }),
  listComparisons: (aid: string, signal?: AbortSignal) => json<ComparisonPage>(`/v1/analyses/${id(aid)}/comparisons?limit=200`, { signal }),
  compare: (aid: string, body: ComparisonRequest) => json<Comparison>(`/v1/analyses/${id(aid)}/comparisons`, post(body)),
  getComparison: (cid: string, signal?: AbortSignal) => json<Comparison>(`/v1/comparisons/${id(cid)}`, { signal }),
};

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

  /** plan-system 4.2: local admin status (counts and states only) and the registry reload. */
  adminStatus: (signal?: AbortSignal) => json<AdminStatus>('/v1/admin/status', { signal }),
  reloadRegistry: () => json<AdminStatus>('/v1/admin/registry/reload', { method: 'POST' }),

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
