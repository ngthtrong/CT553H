import type { ApiError } from '../api/errors';

/** The refused-out-of-domain page of ui-design §3.4. */
export function RefusalNotice({ error, onOverride, onBack }: { error: ApiError; onOverride: () => void; onBack: () => void }) {
  return (
    <section className="card" aria-labelledby="refusal-heading" data-testid="refusal">
      <h2 id="refusal-heading" style={{ marginTop: 0 }}>This tile is outside the domain of the model</h2>
      <div className="banner warn" role="alert">
        <span className="label">Not scored</span>
        {error.message}
      </div>
      <p>
        The model was trained only on tiles that behave as degrons, so a score for such a tile would not be meaningful.
      </p>
      <div className="row">
        <button type="button" className="primary" onClick={onBack}>
          Choose another tile
        </button>
        <button type="button" onClick={onOverride}>
          Score anyway
        </button>
      </div>
    </section>
  );
}
