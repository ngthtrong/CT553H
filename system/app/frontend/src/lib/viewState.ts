/**
 * Per-analysis display choices (plan-system 5.2): ranking filter, sort and pinned substitutions. Keyed by an id that is
 * never user input — a saved analysis id or a reference accession + tile index; typed previews are not remembered.
 * Values are ids and display options only, never a sequence (NFR-09, UX-06).
 */
export interface ViewState {
  filter?: { position: number | null; aa: string | null };
  sort?: { key: string; dir: 'asc' | 'desc' };
  pinned?: string[];                      // cell keys like "12:A"
}

const PREFIX = 'df-view:';
const KEY_RE = /^(analysis:[0-9a-f-]{36}|tile:[A-Z0-9]{6,10}:\d{1,5})$/;

export function viewKey(opts: { analysisId?: string; uniprotId?: string | null; tileIndex?: number | null }): string | null {
  if (opts.analysisId) return `analysis:${opts.analysisId}`;
  if (opts.uniprotId && opts.tileIndex) return `tile:${opts.uniprotId}:${opts.tileIndex}`;
  return null;
}

export function loadView(key: string | null): ViewState {
  if (!key || !KEY_RE.test(key)) return {};
  try {
    const raw = window.localStorage.getItem(PREFIX + key);
    const v = raw ? (JSON.parse(raw) as ViewState) : {};
    return {
      filter: v.filter && (v.filter.position === null || Number.isInteger(v.filter.position)) && (v.filter.aa === null || /^[A-Z]$/.test(v.filter.aa ?? '')) ? v.filter : undefined,
      sort: v.sort,
      pinned: Array.isArray(v.pinned) ? v.pinned.filter((k) => /^\d{1,2}:[A-Z]$/.test(k)).slice(0, 532) : undefined,
    };
  } catch {
    return {};
  }
}

export function saveView(key: string | null, patch: ViewState): void {
  if (!key || !KEY_RE.test(key)) return;
  try {
    const cur = loadView(key);
    window.localStorage.setItem(PREFIX + key, JSON.stringify({ ...cur, ...patch }));
  } catch {
    // storage blocked or full: choices are simply not remembered
  }
}
