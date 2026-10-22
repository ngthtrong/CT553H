import { useId } from 'react';

export type ScaleMode = 'prob' | 'raw';

export function ScaleToggle({ mode, onChange, eventDefinition }: { mode: ScaleMode; onChange: (m: ScaleMode) => void; eventDefinition: string }) {
  const name = useId();
  return (
    <fieldset className="row" style={{ border: 0, padding: 0, margin: 0 }}>
      <legend className="visually-hidden">Quantity shown in the heatmap</legend>
      <span aria-hidden="true">View:</span>
      <label>
        <input type="radio" name={name} checked={mode === 'prob'} onChange={() => onChange('prob')} /> Probability {eventDefinition}
      </label>
      <label>
        <input type="radio" name={name} checked={mode === 'raw'} onChange={() => onChange('raw')} /> Raw score
      </label>
    </fieldset>
  );
}
