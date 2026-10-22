import { useId, useState, type Ref } from 'react';
import { TILE_LENGTH } from '../api/types';
import { checkSequence } from '../lib/validate';

interface Props {
  value: string;
  onChange: (v: string) => void;
  /** Set after a blocked submit so that the message shows even for a short, untouched value. */
  forceShow?: boolean;
  /** Message returned by the server for this field, if any. */
  serverMessage?: string | null;
  inputRef?: Ref<HTMLInputElement>;
}

/** Live validation of a typed tile (ui-design §3.1). Offending characters are named and marked. */
export function SequenceInput({ value, onChange, forceShow = false, serverMessage = null, inputRef }: Props) {
  const id = useId();
  const [touched, setTouched] = useState(false);
  const check = checkSequence(value);
  const n = check.value.length;

  // Show a character problem at once; show a length problem only when too long, after leaving the field, or after a submit attempt.
  const show =
    value.length > 0 && check.issue !== null && (check.issue.kind === 'character' || n > TILE_LENGTH || touched || forceShow);
  const message = show ? check.issue?.message : null;
  const shown = message ?? serverMessage;

  const describedBy = [`${id}-count`, `${id}-hint`, shown ? `${id}-error` : null].filter(Boolean).join(' ');

  return (
    <div className="field">
      <label htmlFor={id}>Tile sequence (exactly {TILE_LENGTH} amino acids)</label>
      <input
        id={id}
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={() => setTouched(true)}
        autoComplete="off"
        autoCapitalize="characters"
        spellCheck={false}
        translate="no"
        className="seq"
        aria-invalid={shown ? true : undefined}
        aria-describedby={describedBy}
        placeholder="For example DIMFLVDSSGSIGPENFSKMKTFMKNLV"
      />
      <div id={`${id}-count`} className="muted" aria-live="polite">
        {n} / {TILE_LENGTH} characters
      </div>
      {check.badIndices.length > 0 && (
        <div className="seq" aria-hidden="true" data-testid="sequence-preview">
          {check.value.split('').map((ch, i) =>
            check.badIndices.includes(i) ? (
              <mark key={i} style={{ textDecoration: 'underline wavy', background: 'transparent', color: 'var(--danger-text)' }}>
                {ch === ' ' ? '·' : ch}
              </mark>
            ) : (
              <span key={i}>{ch}</span>
            ),
          )}
        </div>
      )}
      <div id={`${id}-hint`} className="muted">
        Letters of the 20 standard amino acids only. Case and surrounding spaces are ignored.
      </div>
      {shown && (
        <div id={`${id}-error`} className="error-text" role="alert">
          {shown}
        </div>
      )}
    </div>
  );
}
