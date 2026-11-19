import { useId } from 'react';

export type ScaleMode = 'prob' | 'raw' | 'spread';

/** `spread` (plan-system 1.3) is offered only when every cell carries the seed spread of an ensemble model. */
export function ScaleToggle({ mode, onChange, eventDefinition, hasSpread = false }: { mode: ScaleMode; onChange: (m: ScaleMode) => void; eventDefinition: string; hasSpread?: boolean }) {
  const name = useId();
  return (
    <fieldset className="row" style={{ border: 0, padding: 0, margin: 0 }}>
      <legend className="visually-hidden">Quantity shown in the heatmap</legend>
      <span className="matrix-toolbar__label" aria-hidden="true">View</span>
      <label>
        <input type="radio" name={name} checked={mode === 'prob'} onChange={() => onChange('prob')} /> Probability {eventDefinition}
      </label>
      <label>
        <input type="radio" name={name} checked={mode === 'raw'} onChange={() => onChange('raw')} /> Raw score
      </label>
      {hasSpread && (
        <label>
          <input type="radio" name={name} checked={mode === 'spread'} onChange={() => onChange('spread')} /> Seed spread
        </label>
      )}
    </fieldset>
  );
}
