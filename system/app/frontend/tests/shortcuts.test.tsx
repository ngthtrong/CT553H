/** plan-system 5.2 — shortcuts, remembered filters and pins (UX-05, UX-06). */
import { fireEvent, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { REAL_TILE, renderApp } from './utils';

describe('5.2 shortcuts and remembered display choices', () => {
  it('v and t switch the view; nothing fires while typing; shortcuts can be turned off', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('heatmap');
    fireEvent.keyDown(window, { key: 'v' });
    expect(screen.getByRole('radio', { name: 'Raw score' })).toBeChecked();
    fireEvent.keyDown(window, { key: 't' });
    expect(screen.getByTestId('matrix-table')).toBeInTheDocument();
    // typing in a field does not trigger them
    const select = screen.getAllByRole('combobox', { name: /Position/ })[0]!;
    fireEvent.keyDown(select, { key: 't' });
    expect(screen.getByTestId('matrix-table')).toBeInTheDocument();
    // "?" opens the list, where single-key shortcuts are turned off (WCAG 2.1.4)
    fireEvent.keyDown(window, { key: '?' });
    const box = await screen.findByRole('checkbox', { name: /Use single-key shortcuts/ });
    await user.click(box);
    expect(window.localStorage.getItem('df-shortcuts')).toBe('off');
    await user.click(screen.getByRole('button', { name: 'Close' }));
    fireEvent.keyDown(window, { key: 't' });
    expect(screen.getByTestId('matrix-table')).toBeInTheDocument();         // still the table: shortcut off
  });

  it('remembers the filter and the pins of a reference tile; stores ids and options only (UX-06)', async () => {
    const user = userEvent.setup();
    const first = renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('rank-table');
    await user.selectOptions(screen.getAllByRole('combobox', { name: /Substituted amino acid/ })[0]!, 'A');
    const table = screen.getByTestId('rank-table');
    await user.click(within(table).getAllByRole('button', { name: /^Pin / })[0]!);
    expect(screen.getByTestId('pinned-list')).toHaveTextContent('Pinned (1)');
    first.unmount();
    renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('rank-table');
    expect(screen.getAllByRole('combobox', { name: /Substituted amino acid/ })[0]).toHaveValue('A');
    expect(screen.getByTestId('pinned-list')).toHaveTextContent('Pinned (1)');
    const stored = JSON.stringify({ ...window.localStorage });
    expect(stored).toContain('df-view:tile:A6NMZ7:28');
    expect(stored).not.toMatch(/[A-Z]{28}/);                                  // no sequence
  });

  it('a typed sequence is never remembered', async () => {
    const user = userEvent.setup();
    renderApp('/');
    await user.type(screen.getByLabelText(/Tile sequence/), REAL_TILE);
    await user.click(screen.getByRole('button', { name: 'Predict' }));
    await screen.findByTestId('rank-table');
    await user.click(within(screen.getByTestId('rank-table')).getAllByRole('button', { name: /^Pin / })[0]!);
    expect(Object.keys(window.localStorage).filter((k) => k.startsWith('df-view:'))).toEqual([]);
    expect(JSON.stringify({ ...window.localStorage })).not.toContain(REAL_TILE);
  });
});
