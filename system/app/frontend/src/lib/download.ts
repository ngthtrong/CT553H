import type { ExportFormat, TileRequest } from '../api/types';
import { isStoredTile } from '../api/types';
import { todayStamp } from './format';

/** File name rule of api-spec §7. The sequence itself is never part of a file name. */
export function exportFileName(modelId: string, req: TileRequest | null, tileLabel: string | null, format: ExportFormat, now = new Date()): string {
  const part = req && isStoredTile(req) ? `${req.uniprot_id}-t${req.tile_index}` : tileLabel ?? 'user-seq';
  return `degron-footprint_${modelId}_${part}_${todayStamp(now)}.${format}`;
}

/** Hand a blob to the browser as a download. Throws if the browser refuses. */
export function saveBlob(blob: Blob, fileName: string): void {
  const url = URL.createObjectURL(blob);
  try {
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    a.remove();
  } finally {
    // Revoke on the next tick so the download has started.
    setTimeout(() => URL.revokeObjectURL(url), 0);
  }
}
