import { useId, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import type { ProteinSummary } from '../api/types';
import { useDebounced } from '../lib/hooks';
import { ErrorBanner } from './ErrorBanner';

/** Debounced autocomplete (ARIA 1.2 combobox with a listbox popup). */
export function ProteinSearch({ onSelect }: { onSelect: (p: ProteinSummary) => void }) {
  const id = useId();
  const [text, setText] = useState('');
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(-1);
  const q = useDebounced(text.trim(), 250);
  const enabled = q.length >= 2;

  const res = useQuery({
    queryKey: ['proteins', q],
    queryFn: ({ signal }) => api.searchProteins(q, signal),
    enabled,
    retry: false,
    staleTime: 60_000,
  });
  const items = enabled ? (res.data?.items ?? []) : [];
  const listId = `${id}-list`;

  function choose(p: ProteinSummary) {
    setOpen(false);
    onSelect(p);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setOpen(true);
      setActive((a) => Math.min(items.length - 1, a + 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActive((a) => Math.max(0, a - 1));
    } else if (e.key === 'Enter') {
      const p = items[active];
      if (open && p) {
        e.preventDefault();
        choose(p);
      }
    } else if (e.key === 'Escape') {
      setOpen(false);
      setActive(-1);
    }
  }

  const status = !enabled
    ? text.trim().length > 0
      ? 'Type at least 2 characters.'
      : ''
    : res.isFetching
      ? 'Searching…'
      : res.isError
        ? ''
        : items.length === 0
          ? 'No protein matches this search.'
          : `${items.length} match${items.length === 1 ? '' : 'es'}. Use the arrow keys and Enter to choose.`;

  return (
    <div className="field combo">
      <label htmlFor={id}>Gene symbol or UniProt accession</label>
      <input
        id={id}
        type="text"
        role="combobox"
        aria-expanded={open && items.length > 0}
        aria-controls={listId}
        aria-autocomplete="list"
        aria-activedescendant={open && active >= 0 ? `${id}-opt-${active}` : undefined}
        aria-describedby={`${id}-status`}
        value={text}
        autoComplete="off"
        spellCheck={false}
        placeholder="For example COL6A6 or P60484"
        onChange={(e) => {
          setText(e.target.value);
          setOpen(true);
          setActive(-1);
        }}
        onKeyDown={onKeyDown}
        onBlur={() => setTimeout(() => setOpen(false), 120)}
        onFocus={() => setOpen(true)}
      />
      <div id={`${id}-status`} className="muted" aria-live="polite">
        {status}
      </div>
      <ul id={listId} role="listbox" aria-label="Matching proteins" hidden={!(open && items.length > 0)}>
        {items.map((p, i) => (
          <li
            key={p.uniprot_id}
            id={`${id}-opt-${i}`}
            role="option"
            aria-selected={i === active}
            onMouseDown={(e) => {
              e.preventDefault();
              choose(p);
            }}
          >
            <strong>{p.gene_symbol ?? '—'}</strong> — {p.protein_name ?? 'unnamed protein'} — {p.uniprot_id} — {p.n_tiles} tiles
          </li>
        ))}
      </ul>
      {res.isError && <ErrorBanner error={res.error} onRetry={() => void res.refetch()} />}
    </div>
  );
}
