import { useEffect, useId, useRef, useState } from 'react';
import { CircleHelp } from 'lucide-react';
import { GLOSSARY, type GlossaryId } from '../lib/glossary';

/**
 * A glossary term with a "?" button (plan-system 5.1): Enter/Space opens a non-modal popover described by the button
 * (aria-describedby), Escape or a second press closes it and keeps the focus on the button, a click outside closes it.
 */
export function Term({ id, children }: { id: GlossaryId; children?: React.ReactNode }) {
  const g = GLOSSARY[id];
  const [open, setOpen] = useState(false);
  const pid = useId();
  const wrap = useRef<HTMLSpanElement>(null);
  const btn = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (!open) return undefined;
    const onDoc = (e: MouseEvent) => { if (wrap.current && !wrap.current.contains(e.target as Node)) setOpen(false); };
    document.addEventListener('mousedown', onDoc);
    return () => document.removeEventListener('mousedown', onDoc);
  }, [open]);
  return (
    <span className="term" ref={wrap}>
      {children ?? g.term}
      <button
        ref={btn}
        type="button"
        className="term__button"
        aria-label={`What is ${g.term}?`}
        aria-expanded={open}
        aria-controls={pid}
        aria-describedby={open ? pid : undefined}
        onClick={() => setOpen((o) => !o)}
        onKeyDown={(e) => { if (e.key === 'Escape' && open) { e.preventDefault(); e.stopPropagation(); setOpen(false); btn.current?.focus(); } }}
        data-testid={`term-${id}`}
      >
        <CircleHelp size={14} aria-hidden="true" />
      </button>
      <span id={pid} role="note" className="term__popover" hidden={!open}>
        <strong>{g.term}.</strong> {g.text}
      </span>
    </span>
  );
}

/** A row of the terms used on the result page. */
export function GlossaryBar() {
  return (
    <p className="glossary-bar muted" data-testid="glossary-bar">
      Terms:{' '}
      {(['psi', 'dpsi', 'tile', 'domain', 'calibration', 'raw', 'top10'] as GlossaryId[]).map((id, i) => (
        <span key={id}>{i > 0 ? ' · ' : ''}<Term id={id} /></span>
      ))}
    </p>
  );
}
