import { useEffect, useMemo, useState } from 'react';
import { setShortcutsEnabled, shortcutsEnabled, useShortcuts } from '../lib/shortcuts';
import { Button, Dialog } from './ui';

const LIST: [string, string][] = [
  ['?', 'Show this list'],
  ['/', 'Go to the search or filter field of the page'],
  ['v', 'Next view of the matrix (probability, raw score, seed spread)'],
  ['t', 'Switch between the heatmap and the table view'],
  ['Arrow keys, Home, End', 'Move inside the matrix; Enter selects a cell, Escape leaves it'],
  ['Alt+Shift+P', 'Presentation mode on/off'],
];

/** "?" opens the list of keyboard shortcuts (plan-system 5.2), where single-key shortcuts can be turned off. */
export function ShortcutHelp() {
  const [open, setOpen] = useState(false);
  const [on, setOn] = useState(shortcutsEnabled);
  useEffect(() => {
    const sync = () => setOn(shortcutsEnabled());
    window.addEventListener('df-shortcuts-changed', sync);
    return () => window.removeEventListener('df-shortcuts-changed', sync);
  }, []);
  const map = useMemo(() => ({
    '?': () => setOpen(true),
    '/': () => document.querySelector<HTMLElement>('main [role="combobox"], main input[type="search"], main [data-shortcut-search]')?.focus(),
  }), []);
  useShortcuts(map);
  return (
    <>
      <button type="button" className="ui-button" onClick={() => setOpen(true)} aria-keyshortcuts="?" data-testid="shortcut-help-button">Keyboard shortcuts</button>
      <Dialog open={open} title="Keyboard shortcuts" onClose={() => setOpen(false)} actions={<Button onClick={() => setOpen(false)}>Close</Button>}>
        <label className="row">
          <input type="checkbox" checked={on} onChange={(e) => { setShortcutsEnabled(e.target.checked); setOn(e.target.checked); }} />
          Use single-key shortcuts (turn off if they get in the way of your screen reader or dictation)
        </label>
        <table className="data" data-testid="shortcut-list">
          <caption className="visually-hidden">Keyboard shortcuts</caption>
          <thead><tr><th scope="col">Key</th><th scope="col">Action</th></tr></thead>
          <tbody>{LIST.map(([k, v]) => <tr key={k}><td><kbd>{k}</kbd></td><td>{v}</td></tr>)}</tbody>
        </table>
        <p className="muted">Single-key shortcuts do nothing while you type in a field.</p>
      </Dialog>
    </>
  );
}
