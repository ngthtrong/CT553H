import { screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { MOCK_SLOW_MODEL_ID } from '../mock/handler';
import { contrastRatio, SPREAD_HIGH, SPREAD_LOW, spreadColor } from '../src/lib/colors';
import { SPREAD_LABEL } from '../src/lib/spread';
import { renderApp } from './utils';

const before = (a: Element, b: Element) => Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);

/** plan-system 1.3 — seed spread view (UNC-02, UNC-04 on the UI side). */
describe('UNC seed spread view', () => {
  it('UNC-02: a model without seeds offers no Seed spread view', async () => {
    renderApp('/result/uniprot/A6NMZ7/1');
    await screen.findByTestId('heatmap');
    expect(screen.getByRole('radio', { name: /Raw score/ })).toBeInTheDocument();
    expect(screen.queryByRole('radio', { name: 'Seed spread' })).toBeNull();
  });

  it('an ensemble offers it; the limitation label precedes the numbers; the inspector shows the seed range', async () => {
    const user = userEvent.setup();
    renderApp(`/result/uniprot/A6NMZ7/1?model=${MOCK_SLOW_MODEL_ID}`);
    await screen.findByTestId('heatmap');
    await user.click(screen.getByRole('radio', { name: 'Seed spread' }));
    const desc = screen.getByTestId('scale-description');
    expect(desc).toHaveTextContent(SPREAD_LABEL);
    expect(desc).toHaveTextContent('not a confidence interval and not a prediction error');
    expect(before(desc, screen.getByTestId('heatmap'))).toBe(true);
    expect(screen.getByTestId('colorbar')).toHaveAttribute('aria-label', expect.stringMatching(/seed spread from 0/));
    expect(screen.getByTestId('footprint-track')).toHaveTextContent(/mean seed spread/i);
    // inspector: focus the first substitution cell
    const cells = within(screen.getByTestId('heatmap')).getAllByRole('gridcell');
    const sub = cells.find((c) => !/no substitution/.test(c.getAttribute('aria-label') ?? ''))!;
    expect(sub.getAttribute('aria-label')).toMatch(/seed spread \(not a confidence interval\) SD [0-9.]+, seeds from -?[0-9.]+ to -?[0-9.]+/);
    sub.focus();
    const detail = await screen.findByTestId('seed-spread-detail');
    expect(detail).toHaveTextContent(SPREAD_LABEL);
    expect(detail.textContent!.indexOf(SPREAD_LABEL)).toBeLessThan(detail.textContent!.indexOf('Seeds range from'));
    // table view of the same quantity
    await user.click(screen.getByRole('button', { name: 'Show as a table' }));
    expect(screen.getByTestId('matrix-table').querySelector('caption')).toHaveTextContent('Seed spread');
  });

  it('a saved snapshot without the fields (before 18 Nov) still opens, without the view', async () => {
    renderApp('/result/uniprot/A6NMZ7/1');
    await waitFor(() => expect(screen.getByTestId('heatmap')).toBeInTheDocument());
    expect(screen.queryByTestId('seed-spread-detail')).toBeNull();
  });

  it('the spread scale is monotone from light grey to dark blue with enough contrast between its ends', () => {
    expect(spreadColor(0, 1)).toBe('rgb(238, 241, 245)');
    expect(spreadColor(1, 1)).toBe('rgb(29, 53, 87)');
    expect(spreadColor(5, 1)).toBe(spreadColor(1, 1));            // clamped
    expect(contrastRatio(SPREAD_LOW, SPREAD_HIGH)).toBeGreaterThanOrEqual(4.5);
    expect(contrastRatio(SPREAD_HIGH, '#ffffff')).toBeGreaterThanOrEqual(3);
  });
});
