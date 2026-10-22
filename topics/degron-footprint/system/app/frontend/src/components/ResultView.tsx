import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { isStoredTile } from '../api/types';
import type { Cell, PredictionResult, TileRequest } from '../api/types';
import { effectiveWarnings, isOverridden, unshowableReason } from '../lib/domain';
import { useMediaQuery } from '../lib/hooks';
import { DomainBanner } from './DomainBanner';
import { EvidenceLabel } from './EvidenceLabel';
import { ErrorBanner } from './ErrorBanner';
import { ExportMenu } from './ExportMenu';
import { Heatmap, cellKey } from './Heatmap';
import { LayerToggles, type LayerState } from './LayerToggles';
import { MatrixTable } from './MatrixTable';
import { ProvenanceFooter } from './ProvenanceFooter';
import { RankTable, type RankFilter } from './RankTable';
import { ScaleToggle, type ScaleMode } from './ScaleToggle';
import { WarningList } from './WarningList';

const CLINVAR_FALLBACK_ATTRIBUTION = 'ClinVar variants come from NCBI ClinVar.';
const CLINVAR_FALLBACK_DISCLAIMER = 'For research use only; not for diagnosis.';

interface Props {
  result: PredictionResult;
  /** Request that produced the result; null on a shared page. */
  request: TileRequest | null;
  shared?: { runId: string; token: string };
}

/**
 * Everything below the page title of a result, in reading order (ui-design §3.3):
 * domain banner, warnings, evidence label, controls, heatmap, ranking, actions, provenance.
 */
export function ResultView({ result, request, shared }: Props) {
  const reason = unshowableReason(result);
  const narrow = useMediaQuery('(max-width: 767px)');
  const [mode, setMode] = useState<ScaleMode>('prob');
  const [view, setView] = useState<'heatmap' | 'table' | null>(null);
  const [layers, setLayers] = useState<LayerState>({ measured: false, clinvar: false });
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const [filter, setFilter] = useState<RankFilter>({ position: null, aa: null });

  // Overlays exist only for tiles addressed by accession; a stored tile is read from the tile in the result for shared runs.
  const stored = useMemo(() => {
    if (request && isStoredTile(request)) return { acc: request.uniprot_id, n: request.tile_index };
    const t = result.tile;
    return t?.uniprot_id && t.tile_index ? { acc: t.uniprot_id, n: t.tile_index } : null;
  }, [request, result.tile]);

  const measuredQ = useQuery({
    queryKey: ['measured', stored?.acc, stored?.n],
    queryFn: ({ signal }) => api.getMeasured(stored!.acc, stored!.n, signal),
    enabled: layers.measured && stored !== null,
    retry: false,
    staleTime: 300_000,
  });
  const clinvarQ = useQuery({
    queryKey: ['clinvar', stored?.acc, stored?.n],
    queryFn: ({ signal }) => api.getClinvar(stored!.acc, stored!.n, signal),
    enabled: layers.clinvar && stored !== null,
    retry: false,
    staleTime: 300_000,
  });
  const sourcesQ = useQuery({ queryKey: ['sources'], queryFn: ({ signal }) => api.listSources(signal), retry: false, staleTime: 300_000 });

  if (reason) {
    // Rule: never show a score without the domain status and the model version.
    return (
      <div className="banner danger" role="alert" data-testid="unshowable">
        <span className="label">Not shown</span>
        The scores are not shown because the response is incomplete: {reason}
      </div>
    );
  }

  const prov = result.provenance;
  const ev = prov.event_definition;
  const warnings = effectiveWarnings(result);
  const clinvarSource = sourcesQ.data?.items.find((s) => /clinvar/i.test(`${s.source_id} ${s.name}`));
  const clinvarAttribution = clinvarSource?.attribution_text ?? CLINVAR_FALLBACK_ATTRIBUTION;
  const clinvarDisclaimer = clinvarSource?.disclaimer_text ?? clinvarQ.data?.provenance.disclaimers.at(-1) ?? CLINVAR_FALLBACK_DISCLAIMER;

  const measured = layers.measured ? measuredQ.data?.cells : undefined;
  const clinvar = layers.clinvar ? clinvarQ.data?.variants : undefined;
  const unavailableReason = stored === null ? 'they are available only for a tile chosen from a protein, not for a typed sequence.' : null;
  const effectiveView = view ?? (narrow ? 'table' : 'heatmap');
  const nTop = result.cells.filter((c) => c.top10pct_in_tile).length;

  function select(c: Cell) {
    setSelectedKey(cellKey(c.position, c.mut_aa));
  }

  return (
    <>
      {/* Reading order: domain, warnings, evidence, then the controls and the numbers. */}
      <DomainBanner domain={result.domain} />
      <WarningList warnings={warnings} overridden={isOverridden(result)} />
      <EvidenceLabel provenance={prov} />

      <p className="visually-hidden" role="status" aria-live="polite">
        Scored {result.cells.length} substitutions with model {prov.model_id}. {nTop} are in the top 10 percent.
      </p>

      <section aria-labelledby="matrix-heading">
        <h2 id="matrix-heading">Effect matrix</h2>
        <div className="row" style={{ marginBottom: '0.5rem' }}>
          <ScaleToggle mode={mode} onChange={setMode} eventDefinition={ev} />
          <button type="button" aria-pressed={effectiveView === 'table'} onClick={() => setView(effectiveView === 'table' ? 'heatmap' : 'table')}>
            {effectiveView === 'table' ? 'Show the heatmap' : 'Show as a table'}
          </button>
        </div>
        <LayerToggles
          state={layers}
          onChange={setLayers}
          unavailableReason={unavailableReason}
          clinvarAttribution={clinvarAttribution}
          clinvarDisclaimer={clinvarDisclaimer}
        />
        {layers.measured && measuredQ.isError && <ErrorBanner error={measuredQ.error} onRetry={() => void measuredQ.refetch()} />}
        {layers.clinvar && clinvarQ.isError && <ErrorBanner error={clinvarQ.error} onRetry={() => void clinvarQ.refetch()} />}
        {layers.measured && measuredQ.isSuccess && measuredQ.data.cells.length === 0 && <p className="muted">No measured data for this tile.</p>}
        {layers.measured && measuredQ.isSuccess && measuredQ.data.cells.length > 0 && (
          <p className="muted">Measured values are part of the training data of this model; they are not a validation.</p>
        )}
        {layers.clinvar && clinvarQ.isSuccess && clinvarQ.data.variants.length === 0 && <p className="muted">No ClinVar missense variant in this tile.</p>}
        {layers.clinvar && clinvarQ.isSuccess && <p className="muted">ClinVar file dated {clinvarQ.data.clinvar_file_date}.</p>}

        {effectiveView === 'heatmap' ? (
          <Heatmap
            cells={result.cells}
            tile={result.tile}
            mode={mode}
            eventDefinition={ev}
            measured={measured}
            clinvar={clinvar}
            clinvarNote={`${clinvarAttribution} ${clinvarDisclaimer}`}
            selectedKey={selectedKey}
            onSelect={select}
          />
        ) : (
          <MatrixTable cells={result.cells} tile={result.tile} mode={mode} eventDefinition={ev} />
        )}
      </section>

      <RankTable cells={result.cells} eventDefinition={ev} filter={filter} onFilter={setFilter} selectedKey={selectedKey} onSelect={select} />

      <ExportMenu request={request} shared={shared} provenance={prov} />
      <ProvenanceFooter provenance={prov} />
    </>
  );
}
