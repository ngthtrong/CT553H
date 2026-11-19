import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import type { ModelSummary } from '../api/types';

/** Same pattern as the contract's model id; anything else in `?model=` is ignored (only an id, never user data). */
const MODEL_ID = /^[a-z0-9][a-z0-9.-]{1,63}$/;

/** Above this estimate the user confirms before a slow model starts (plan-system 1.1). */
export const SLOW_SECONDS = 20;

export function useModels() {
  return useQuery({ queryKey: ['models'], queryFn: ({ signal }) => api.listModels(signal), retry: false, staleTime: 30_000 });
}

export function effectModels(items: ModelSummary[] | undefined): ModelSummary[] {
  return (items ?? []).filter((m) => m.role === 'effect');
}

/** The model chosen in `?model=` (an id only), or undefined for the service default. */
export function useModelParam(): [string | undefined, (id: string | undefined) => void] {
  const [params, setParams] = useSearchParams();
  const raw = params.get('model');
  const value = raw !== null && MODEL_ID.test(raw) ? raw : undefined;
  const set = (id: string | undefined) => {
    const next = new URLSearchParams(params);
    if (id) next.set('model', id);
    else next.delete('model');
    setParams(next, { replace: true });
  };
  return [value, set];
}

/** `?model=<id>` suffix for links that carry the choice to the next screen. */
export function modelQuery(id: string | undefined, prefix: '?' | '&' = '?'): string {
  return id ? `${prefix}model=${encodeURIComponent(id)}` : '';
}

/** The model a request will use: the chosen one, else the service default. */
export function resolveModel(items: ModelSummary[] | undefined, chosen: string | undefined): ModelSummary | undefined {
  const eff = effectModels(items);
  return chosen ? eff.find((m) => m.model_id === chosen) : eff.find((m) => m.is_default);
}

export interface Estimate {
  tiles: number;
  secondsPerTile: number;
  totalSeconds: number;
}

/** "≈ N tiles × M s ≈ T" when the model has a measured time; null before the first measurement. */
export function estimate(model: ModelSummary | undefined, tiles: number): Estimate | null {
  const s = model?.expected_tile_seconds;
  if (s === null || s === undefined || tiles <= 0) return null;
  return { tiles, secondsPerTile: s, totalSeconds: s * tiles };
}

export function fmtDuration(seconds: number): string {
  if (seconds < 90) return `${Math.max(1, Math.round(seconds))} s`;
  if (seconds < 5400) return `${Math.round(seconds / 60)} min`;
  return `${(seconds / 3600).toFixed(1)} h`;
}

export function fmtPerTile(seconds: number): string {
  return seconds < 1 ? `${(seconds * 1000).toFixed(0)} ms` : `${seconds.toFixed(1)} s`;
}

export function describeEstimate(e: Estimate): string {
  const per = fmtPerTile(e.secondsPerTile);
  return `≈ ${e.tiles} tile${e.tiles === 1 ? '' : 's'} × ${per} ≈ ${fmtDuration(e.totalSeconds)}`;
}
