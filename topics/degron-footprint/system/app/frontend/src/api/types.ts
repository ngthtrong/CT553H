import type { components } from './schema';

type S = components['schemas'];

export type PredictionResult = S['PredictionResult'];
export type Cell = S['Cell'];
export type Provenance = S['Provenance'];
export type DomainInfo = S['DomainInfo'];
export type DomainStatus = S['DomainStatus'];
export type Warning = S['Warning'];
export type TileInfo = S['TileInfo'];
export type ProteinSummary = S['ProteinSummary'];
export type TileSummary = S['TileSummary'];
export type TileList = S['TileList'];
export type MeasuredCell = S['MeasuredCell'];
export type MeasuredOverlay = S['MeasuredOverlay'];
export type ClinvarVariant = S['ClinvarVariant'];
export type ClinvarOverlay = S['ClinvarOverlay'];
export type ModelSummary = S['ModelSummary'];
export type ModelCard = S['ModelCard'];
export type DataSource = S['DataSource'];
export type DataSourceRef = S['DataSourceRef'];
export type RunCreated = S['RunCreated'];
export type Health = S['Health'];
export type ExportFormat = S['ExportFormat'];
export type ApiErrorCode = S['Error']['code'];

/** Exactly one of a typed sequence or a stored tile (UniProt accession + 1-based tile index). */
export type TileRequest =
  | { sequence: string; override_domain?: boolean }
  | { uniprot_id: string; tile_index: number; override_domain?: boolean };

export function isStoredTile(r: TileRequest): r is { uniprot_id: string; tile_index: number; override_domain?: boolean } {
  return 'uniprot_id' in r;
}

/** The 20 standard amino acids in the column order of the API (api-spec §1). */
export const AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY';
export const TILE_LENGTH = 28;
export const N_CELLS = 532;
