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
  | { sequence: string; override_domain?: boolean; model_id?: string }
  | { uniprot_id: string; tile_index: number; override_domain?: boolean; model_id?: string };

export function isStoredTile(r: TileRequest): r is { uniprot_id: string; tile_index: number; override_domain?: boolean; model_id?: string } {
  return 'uniprot_id' in r;
}

/** The 20 standard amino acids in the column order of the API (api-spec §1). */
export const AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY';
export const TILE_LENGTH = 28;
export const N_CELLS = 532;

// ---- workspace (v0.2) ----------------------------------------------------------------------------------------------
export type Project = S['Project'];
export type ProjectPage = S['ProjectPage'];
export type SavedAnalysis = S['SavedAnalysis'];
export type SavedAnalysisSummary = S['SavedAnalysisSummary'];
export type SavedAnalysisPage = S['SavedAnalysisPage'];
export type Job = S['Job'];
export type JobPage = S['JobPage'];
export type JobItem = S['JobItem'];
export type JobItemPage = S['JobItemPage'];
export type JobRequest = S['JobRequest'];
export type JobFootprint = S['JobFootprint'];
export type ModelComparison = S['ModelComparison'];
export type Suggestions = S['Suggestions'];
export type AdminStatus = S['AdminStatus'];
export type AgreementSeries = S['AgreementSeries'];
export type ModelComparisonCell = S['ModelComparisonCell'];
export type ModelComparisonPage = S['ModelComparisonPage'];
export type BatchPeptide = S['BatchPeptide'];
export type Dataset = S['Dataset'];
export type DatasetPage = S['DatasetPage'];
export type ImportMetadata = S['ImportMetadata'];
export type ValidationIssue = S['ValidationIssue'];
export type Comparison = S['Comparison'];
export type ComparisonPage = S['ComparisonPage'];
export type ComparisonRequest = S['ComparisonRequest'];
export type AnnotationState = S['AnnotationState'];
