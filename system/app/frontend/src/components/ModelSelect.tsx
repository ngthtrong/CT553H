import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { ModelSummary } from '../api/types';
import { describeEstimate, effectModels, estimate, fmtPerTile, resolveModel, SLOW_SECONDS, useModels, type Estimate } from '../lib/models';
import { Button, Dialog, Field } from './ui';

/**
 * Model picker (plan-system 1.1). Lists every effect model; one that does not serve is shown but cannot be chosen, with
 * its reason. The empty value means "the service default", so a request without a choice names no model.
 */
export function ModelSelect({ value, onChange, label = 'Model', testId = 'model-select' }: {
  value: string | undefined;
  onChange: (id: string | undefined) => void;
  label?: string;
  testId?: string;
}) {
  const models = useModels();
  const eff = effectModels(models.data?.items);
  const def = eff.find((m) => m.is_default);
  const chosen = resolveModel(models.data?.items, value);
  const notServing = eff.filter((m) => !m.serving);
  const per = estimate(chosen, 1);
  if (models.isError || (models.data && eff.length === 0)) return null;
  return (
    <div className="stack" data-testid={testId}>
      <Field
        label={label}
        hint={
          <>
            {chosen ? <>Scored with <code>{chosen.model_id}</code>{chosen.kind ? ` (${chosen.kind})` : ''}. </> : null}
            {per ? <>Measured about {fmtPerTile(per.secondsPerTile)} per tile on this computer. </> : null}
            {chosen ? <Link to={`/model/${encodeURIComponent(chosen.model_id)}`}>Model card</Link> : null}
          </>
        }
      >
        {({ id, describedBy }) => (
          <select
            id={id}
            className="ui-select"
            aria-describedby={describedBy}
            value={value ?? ''}
            disabled={models.isPending}
            onChange={(e) => onChange(e.target.value === '' || e.target.value === def?.model_id ? undefined : e.target.value)}
          >
            <option value="">{def ? `${def.model_id} (default)` : 'Service default'}</option>
            {eff.filter((m) => m.model_id !== def?.model_id).map((m) => (
              <option key={m.model_id} value={m.model_id} disabled={!m.serving}>
                {m.model_id}{m.serving ? '' : ' — not serving'}
              </option>
            ))}
          </select>
        )}
      </Field>
      {notServing.length > 0 && (
        <ul className="muted model-select__reasons" data-testid="model-not-serving">
          {notServing.map((m) => <li key={m.model_id}><code>{m.model_id}</code> cannot be chosen: {m.not_serving_reason ?? 'not serving'}.</li>)}
        </ul>
      )}
    </div>
  );
}

/**
 * Confirmation before a slow model starts: "≈ N tiles × M s ≈ T". `run(go)` calls `go` at once when the model is fast
 * or not yet measured, otherwise after the user confirms.
 */
export function useSlowModelConfirm(model: ModelSummary | undefined) {
  const [pending, setPending] = useState<{ est: Estimate; go: () => void } | null>(null);
  function run(tiles: number, go: () => void) {
    const est = estimate(model, tiles);
    if (est && est.totalSeconds > SLOW_SECONDS) setPending({ est, go });
    else go();
  }
  const dialog = (
    <Dialog
      open={pending !== null}
      title="This model is slow"
      onClose={() => setPending(null)}
      actions={
        <>
          <Button onClick={() => setPending(null)}>Cancel</Button>
          <Button variant="primary" onClick={() => { const p = pending; setPending(null); p?.go(); }}>Start anyway</Button>
        </>
      }
    >
      {pending && (
        <p data-testid="slow-model-estimate">
          <code>{model?.model_id}</code>: {describeEstimate(pending.est)}. The time is the mean of the last tiles this service
          scored on this computer; it is an estimate, not a guarantee.
        </p>
      )}
    </Dialog>
  );
  return { run, dialog };
}
