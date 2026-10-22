import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { ProteinSearch } from '../components/ProteinSearch';
import { SequenceInput } from '../components/SequenceInput';
import { useDocumentTitle } from '../lib/hooks';
import { checkSequence } from '../lib/validate';
import { requestStore } from '../state/requestStore';

type Tab = 'paste' | 'protein';
const TAB_KEY = 'df-input-tab';

function lastTab(): Tab {
  try {
    return window.sessionStorage.getItem(TAB_KEY) === 'protein' ? 'protein' : 'paste';
  } catch {
    return 'paste';
  }
}

export function InputPage() {
  useDocumentTitle('Input');
  const navigate = useNavigate();
  const [tab, setTabState] = useState<Tab>(lastTab);
  const [seq, setSeq] = useState('');
  const [blocked, setBlocked] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Only the name of the tab is remembered for the session, never the sequence (ui-design §3.1).
  function setTab(t: Tab) {
    setTabState(t);
    try {
      window.sessionStorage.setItem(TAB_KEY, t);
    } catch {
      // Storage may be blocked; the tab then resets on reload.
    }
  }

  const models = useQuery({ queryKey: ['models'], queryFn: ({ signal }) => api.listModels(signal), retry: false, staleTime: 300_000 });
  const defaultModel = models.data?.items.find((m) => m.is_default && m.role === 'effect');

  function submit(e: React.FormEvent) {
    e.preventDefault();
    const check = checkSequence(seq);
    if (check.issue) {
      setBlocked(true);
      inputRef.current?.focus();
      return;
    }
    requestStore.set({ sequence: check.value });
    navigate('/result');
  }

  return (
    <>
      <h1>Predict the effect of every substitution in a 28-residue degron tile</h1>
      <p className="muted">
        Assay: GPS (Zhang et al. 2023).{' '}
        {defaultModel ? <>Model <code>{defaultModel.model_id}</code>. </> : null}
        Development benchmark, not an external validation.
      </p>

      <div className="tabs" role="tablist" aria-label="How to choose a tile">
        <button type="button" role="tab" id="tab-paste" aria-selected={tab === 'paste'} aria-controls="panel-paste" onClick={() => setTab('paste')}>
          Paste a sequence
        </button>
        <button type="button" role="tab" id="tab-protein" aria-selected={tab === 'protein'} aria-controls="panel-protein" onClick={() => setTab('protein')}>
          Choose a protein
        </button>
      </div>

      {tab === 'paste' ? (
        <section role="tabpanel" id="panel-paste" aria-labelledby="tab-paste" className="card">
          <form onSubmit={submit} noValidate>
            <SequenceInput value={seq} onChange={(v) => { setSeq(v); setBlocked(false); }} forceShow={blocked} inputRef={inputRef} />
            <div className="banner warn" role="note">
              <span className="label">Warning</span>
              The domain of a typed sequence is unknown. The model was trained only on tiles that behave as degrons (wild-type
              PSI ≤ 4.0) and cannot check yours.
            </div>
            <p className="muted">
              Your sequence is sent only to get the prediction and is kept in this page&apos;s memory. It is not stored in the
              address, in the browser storage or on the server, unless you ask for a share link.
            </p>
            <button type="submit" className="primary" disabled={seq.trim().length === 0}>
              Predict
            </button>
            {seq.trim().length === 0 && <span className="muted"> Enter a sequence of exactly 28 amino acids.</span>}
          </form>
        </section>
      ) : (
        <section role="tabpanel" id="panel-protein" aria-labelledby="tab-protein" className="card">
          <ProteinSearch onSelect={(p) => navigate(`/protein/${p.uniprot_id}`)} />
          <p className="muted">Reviewed human proteins. You then choose one of the 28-residue tiles of the protein.</p>
        </section>
      )}
    </>
  );
}
