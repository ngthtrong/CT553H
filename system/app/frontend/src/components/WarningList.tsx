import type { Warning } from '../api/types';

interface Props {
  warnings: Warning[];
  /** True when the tile is outside the domain and the user chose to score it (rule W-3). */
  overridden: boolean;
  /** Announce as an alert when the block appears after a request (ui-design §6). */
  announce?: boolean;
}

/** Rules W-2, W-3 and W-7. Not dismissible: it is rendered again on every view. */
export function WarningList({ warnings, overridden, announce = true }: Props) {
  const role = announce ? 'alert' : 'note';
  const rest = warnings.filter((w) => w.code !== 'OUT_OF_DOMAIN_OVERRIDDEN');
  return (
    <>
      {overridden && (
        <div className="banner danger" role={role} data-testid="override-banner">
          <span className="label">Override</span>
          Out-of-domain override: this tile is measured to be outside the domain of the model, and you chose to score it. The
          numbers below are not meaningful for this tile. This warning is part of every export.
        </div>
      )}
      {rest.length > 0 && (
        <div className="banner warn" role={role} data-testid="warning-list">
          <span className="label">Warning</span>
          {rest.length === 1 ? (
            rest[0]?.message
          ) : (
            <ul>
              {rest.map((w) => (
                <li key={w.code}>{w.message}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </>
  );
}
