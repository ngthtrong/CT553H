import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui';

const KEY = 'df-onboarding-done';
const STEPS = [
  { title: 'Create a project', text: 'Projects keep your saved analyses, jobs and imported measurements on this computer.', to: '/projects', link: 'Open Projects' },
  { title: 'Choose a protein', text: 'In New analysis, choose a reviewed human protein or paste one 28-residue sequence.', to: '/', link: 'Open New analysis' },
  { title: 'Score a tile', text: 'Pick a tile: the matrix shows the predicted effect of all 532 substitutions, after the domain status and warnings.', to: null, link: '' },
  { title: 'Save it', text: 'Save the result to your project to reopen it later exactly as it was, compare it, or export it with its provenance.', to: null, link: '' },
];

function done(): boolean {
  try {
    return window.localStorage.getItem(KEY) === '1';
  } catch {
    return true;                                          // storage blocked: do not nag on every page
  }
}

/** First-visit guide in 4 steps (plan-system 5.1); skippable; remembered with one flag in localStorage, never data. */
export function Onboarding() {
  const [hidden, setHidden] = useState(done);
  const [step, setStep] = useState(0);
  if (hidden) return null;
  const finish = () => {
    try { window.localStorage.setItem(KEY, '1'); } catch { /* blocked: shows again next time */ }
    setHidden(true);
  };
  const s = STEPS[step]!;
  return (
    <section className="onboarding panel" aria-labelledby="onb-h" data-testid="onboarding">
      <p className="muted" style={{ margin: 0 }}>Getting started · step {step + 1} of {STEPS.length}</p>
      <h2 id="onb-h" style={{ margin: '0.25rem 0' }}>{s.title}</h2>
      <p style={{ margin: 0 }}>{s.text}{s.to ? <> <Link to={s.to}>{s.link}</Link>.</> : null}</p>
      <div className="row" style={{ marginTop: 'var(--space-2)' }}>
        {step > 0 && <Button onClick={() => setStep(step - 1)}>Back</Button>}
        {step < STEPS.length - 1 ? <Button variant="primary" onClick={() => setStep(step + 1)}>Next</Button> : <Button variant="primary" onClick={finish}>Done</Button>}
        <Button onClick={finish}>Skip the guide</Button>
      </div>
    </section>
  );
}
