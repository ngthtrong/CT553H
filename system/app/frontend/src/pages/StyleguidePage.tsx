import { useState } from 'react';
import { Download, FolderPlus, Play, Trash2 } from 'lucide-react';
import {
  Banner,
  Button,
  DataTable,
  Dialog,
  EmptyState,
  Field,
  IconButton,
  LiveRegion,
  ProgressBar,
  Select,
  Skeleton,
  StatusPill,
  Tabs,
  Toast,
  tabPanelProps,
} from '../components/ui';

const TOKENS = ['bg', 'surface', 'subtle', 'soft', 'text', 'muted', 'border', 'line', 'accent', 'accent-soft', 'accent-ink',
  'warn-bg', 'warn-text', 'danger-bg', 'danger-text', 'info-bg', 'info-text', 'focus'];
const ROWS = Array.from({ length: 32 }, (_, i) => ({ id: `item-${i + 1}`, input: `peptide ${i + 1}`, score: ((i * 37) % 23) / 10,
  state: ['succeeded', 'refused', 'failed', 'running', 'pending', 'cancelled'][i % 6]! }));

/** Development-only review page for every primitive in both themes (WP1.8); not routed in production builds. */
export function StyleguidePage() {
  const [tab, setTab] = useState('a');
  const [open, setOpen] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [name, setName] = useState('');
  return (
    <div className="stack">
      <div className="page-head">
        <div>
          <h1>Styleguide</h1>
          <p>Primitives of Degron Workspace. Roboto for text, <span className="mono">Roboto Mono</span> for sequences.</p>
        </div>
      </div>
      <section className="panel" aria-labelledby="sg-tokens">
        <h2 id="sg-tokens">Purpose tokens</h2>
        <div className="swatch-row">
          {TOKENS.map((t) => (
            <div key={t} className="swatch-chip">
              <span style={{ background: `var(--${t})` }} />
              <span className="mono">--{t}</span>
            </div>
          ))}
        </div>
        <p className="seq">DIMFLVDSSGSIGPENFSKMKTFMKNLV</p>
      </section>
      <section className="panel" aria-labelledby="sg-buttons">
        <h2 id="sg-buttons">Buttons</h2>
        <div className="row">
          <Button variant="primary" icon={Play}>Run analysis</Button>
          <Button icon={FolderPlus}>New project</Button>
          <Button variant="ghost" icon={Download}>Export CSV</Button>
          <Button variant="danger" icon={Trash2} onClick={() => setOpen(true)}>Delete…</Button>
          <Button busy>Saving</Button>
          <Button disabled>Disabled</Button>
          <IconButton icon={Download} label="Download manifest" />
        </div>
      </section>
      <section className="panel" aria-labelledby="sg-fields">
        <h2 id="sg-fields">Fields</h2>
        <Field label="Project name" hint="1 to 200 characters." required error={name.length > 200 ? 'Too long.' : null}>
          {({ id, describedBy, invalid }) => (
            <input id={id} className="ui-input" aria-describedby={describedBy} aria-invalid={invalid || undefined} value={name} onChange={(e) => setName(e.target.value)} />
          )}
        </Field>
        <Field label="Field with an error" error="The sequence has 27 residues; 28 are needed.">
          {({ id, describedBy, invalid }) => <input id={id} className="ui-input" aria-describedby={describedBy} aria-invalid={invalid} defaultValue="ACDEFGHIK" />}
        </Field>
        <Select label="Calibrator" options={[{ value: 'platt', label: 'Platt (default)' }, { value: 'iso', label: 'Isotonic' }]} />
      </section>
      <section className="panel" aria-labelledby="sg-status">
        <h2 id="sg-status">Status, banners, progress</h2>
        <div className="row">
          {['pending', 'running', 'completed', 'partial', 'failed', 'cancelled', 'refused', 'staged', 'committed', 'expired'].map((s) => <StatusPill key={s} status={s} />)}
        </div>
        <Banner tone="info" title="Comparison only">Imported observations are never used to retrain the model.</Banner>
        <Banner tone="warn" title="Borderline domain">The gate places this tile between its cuts.</Banner>
        <Banner tone="danger" title="Out of domain">Scores are unsupported for this tile.</Banner>
        <Banner tone="success" title="Saved">The analysis is stored in this project.</Banner>
        <ProgressBar value={37} max={97} label="Tiles scored" />
        <LiveRegion message="37 of 97 tiles scored" />
      </section>
      <section className="panel" aria-labelledby="sg-tabs">
        <h2 id="sg-tabs">Tabs and table</h2>
        <Tabs id="sg-tabs-demo" label="Project sections" active={tab} onChange={setTab} tabs={[{ id: 'a', label: 'History', count: 12 }, { id: 'b', label: 'Jobs', count: 3 }, { id: 'c', label: 'Datasets', count: 1 }]} />
        <div {...tabPanelProps('sg-tabs-demo', tab)}>
        <DataTable
          caption="Job items"
          rows={ROWS}
          rowKey={(r) => r.id}
          pageSize={8}
          columns={[
            { key: 'id', header: 'Item', render: (r) => <span className="mono">{r.id}</span>, sortValue: (r) => r.id },
            { key: 'input', header: 'Input', render: (r) => r.input },
            { key: 'score', header: 'Max ΔPSI', render: (r) => r.score.toFixed(2), sortValue: (r) => r.score, numeric: true },
            { key: 'state', header: 'Status', render: (r) => <StatusPill status={r.state} /> },
          ]}
        />
        </div>
      </section>
      <section className="panel" aria-labelledby="sg-empty">
        <h2 id="sg-empty">Empty and loading</h2>
        <EmptyState title="No analyses yet" action={<Button variant="primary">New analysis</Button>}>Save an analysis to see it here.</EmptyState>
        <Skeleton lines={3} />
        <Button onClick={() => setToast('Project renamed.')}>Show a toast</Button>
      </section>
      <Dialog open={open} title="Delete project?" onClose={() => setOpen(false)} actions={<><Button onClick={() => setOpen(false)}>Cancel</Button><Button variant="danger" onClick={() => setOpen(false)}>Delete</Button></>}>
        <p>This removes 12 analyses, 3 jobs and 1 dataset. Reference data and other projects are not affected.</p>
      </Dialog>
      <Toast message={toast} onDismiss={() => setToast(null)} />
    </div>
  );
}
