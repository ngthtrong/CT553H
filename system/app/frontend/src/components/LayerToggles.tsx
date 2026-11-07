import { ClinvarNotice } from './ClinvarNotice';

export interface LayerState {
  measured: boolean;
  clinvar: boolean;
}

interface Props {
  state: LayerState;
  onChange: (s: LayerState) => void;
  /** Reason the layers cannot be offered, or null when they can. A disabled control explains itself (ui-design §3.3). */
  unavailableReason: string | null;
  clinvarAttribution: string;
  clinvarDisclaimer: string;
}

export function LayerToggles({ state, onChange, unavailableReason, clinvarAttribution, clinvarDisclaimer }: Props) {
  const off = unavailableReason !== null;
  return (
    <fieldset style={{ border: 0, padding: 0, margin: 0 }}>
      <legend className="visually-hidden">Overlay layers</legend>
      <div className="row">
        <span aria-hidden="true">Layers:</span>
        <label>
          <input
            type="checkbox"
            checked={state.measured}
            disabled={off}
            onChange={(e) => onChange({ ...state, measured: e.target.checked })}
          />{' '}
          Measured ΔPSI
        </label>
        <label>
          <input
            type="checkbox"
            checked={state.clinvar}
            disabled={off}
            onChange={(e) => onChange({ ...state, clinvar: e.target.checked })}
          />{' '}
          ClinVar variants
        </label>
      </div>
      {off && <p className="muted" style={{ margin: '0.25rem 0' }}>Layers are unavailable: {unavailableReason}</p>}
      <ClinvarNotice attribution={clinvarAttribution} disclaimer={clinvarDisclaimer} />
    </fieldset>
  );
}
