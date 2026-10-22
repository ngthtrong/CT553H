import type { DomainInfo } from '../api/types';
import { STATUS } from '../lib/domain';
import { fmtPsi } from '../lib/format';

const GLYPH = { solid: '●', hatched: '▨', dotted: '◌', empty: '○' } as const;

/** Rule W-1: the domain status is on every result view, in words, before any score. */
export function DomainBanner({ domain }: { domain: DomainInfo }) {
  const s = STATUS[domain.status];
  const measured = domain.psi_wt_measured !== null && domain.psi_wt_measured !== undefined;
  return (
    <section className="banner" aria-labelledby="domain-heading" data-testid="domain-banner" data-status={domain.status}>
      <h2 id="domain-heading" style={{ margin: 0, fontSize: '1.05rem' }}>
        <span aria-hidden="true">{GLYPH[s.pattern]} </span>
        Domain: {s.label}
        {measured && <> — measured tile PSI {fmtPsi(domain.psi_wt_measured)}</>}
      </h2>
      <p style={{ margin: '0.25rem 0 0' }}>{domain.message}</p>
    </section>
  );
}
