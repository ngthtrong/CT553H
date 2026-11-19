import { useRef, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { PeptideBatchForm, WholeProteinForm } from '../components/BatchInput';
import { ModelSelect, useSlowModelConfirm } from '../components/ModelSelect';
import { ProteinSearch } from '../components/ProteinSearch';
import { SequenceInput } from '../components/SequenceInput';
import { useDocumentTitle } from '../lib/hooks';
import { modelQuery, resolveModel, useModelParam, useModels } from '../lib/models';
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

type Mode = 'single' | 'batch' | 'protein';
const MODES: { id: Mode; label: string; hint: string }[] = [
  { id: 'single', label: 'Single peptide', hint: 'One 28-residue tile; a quick preview, saved only on request.' },
  { id: 'batch', label: 'Peptide batch', hint: 'Up to 100 peptides as a durable job in a project.' },
  { id: 'protein', label: 'Whole protein', hint: 'Every full 28-residue window of one protein, as a job.' },
];

/** Screen 9.3, New analysis (UC-01, UC-08): single tile, peptide batch or whole protein. */
export function InputPage() {
  useDocumentTitle('New analysis');
  const [params, setParams] = useSearchParams();
  const mode: Mode = params.get('mode') === 'batch' ? 'batch' : params.get('mode') === 'protein' ? 'protein' : 'single';
  const project = params.get('project') ?? '';
  const [modelId, setModelId] = useModelParam();
  return (
    <>
      <h1>New analysis</h1>
      <fieldset className="mode-picker">
        <legend className="visually-hidden">Analysis type</legend>
        {MODES.map((m) => (
          <label key={m.id} className={`mode-option${mode === m.id ? ' is-active' : ''}`}>
            <input
              type="radio"
              name="analysis-mode"
              checked={mode === m.id}
              onChange={() => {
                const next = new URLSearchParams(params);
                if (m.id === 'single') next.delete('mode');
                else next.set('mode', m.id);
                setParams(next, { replace: true });
              }}
            />
            <strong>{m.label}</strong>
            <span className="muted mode-option__hint">{m.hint}</span>
          </label>
        ))}
      </fieldset>
      <ModelSelect value={modelId} onChange={setModelId} />
      {mode === 'single' && <SingleInput modelId={modelId} />}
      {mode === 'batch' && <PeptideBatchForm initialProject={project} modelId={modelId} />}
      {mode === 'protein' && <WholeProteinForm initialProject={project} modelId={modelId} />}
    </>
  );
}

function SingleInput({ modelId }: { modelId: string | undefined }) {
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

  const models = useModels();
  const model = resolveModel(models.data?.items, modelId);
  const slow = useSlowModelConfirm(model);

  function submit(e: React.FormEvent) {
    e.preventDefault();
    const check = checkSequence(seq);
    if (check.issue) {
      setBlocked(true);
      inputRef.current?.focus();
      return;
    }
    slow.run(1, () => {
      requestStore.set(modelId ? { sequence: check.value, model_id: modelId } : { sequence: check.value });
      navigate('/result');
    });
  }

  return (
    <>
      <h2>Predict the effect of every substitution in a 28-residue degron tile</h2>
      <p className="muted">
        Assay: GPS (Zhang et al. 2023).{' '}
        {model ? <>Model <code>{model.model_id}</code>. </> : null}
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
              The domain of a typed sequence is predicted from its sequence by the R3 gate, not measured. The model was trained
              only on tiles that behave as degrons (intrinsic wild-type PSI ≤ 4.0).
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
          <ProteinSearch onSelect={(p) => navigate(`/protein/${p.uniprot_id}${modelQuery(modelId)}`)} />
          <p className="muted">Reviewed human proteins. You then choose one of the 28-residue tiles of the protein.</p>
        </section>
      )}
      {slow.dialog}
    </>
  );
}
