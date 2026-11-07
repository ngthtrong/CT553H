import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'vitest-axe';
import { describe, expect, it } from 'vitest';
import { REAL_TILE, renderApp } from './utils';

// jsdom has no layout or computed styles, so colour contrast is not testable here. It is covered by
// tests/contrast.test.ts (design tokens) and by axe in the browser (e2e/a11y.spec.ts).
const OPTIONS = { rules: { 'color-contrast': { enabled: false } } };

describe('A11Y-01 axe on every page (jsdom, structure and ARIA rules)', () => {
  it('Input, both tabs', async () => {
    const user = userEvent.setup();
    const { container } = renderApp('/');
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
    await user.click(screen.getByRole('tab', { name: 'Choose a protein' }));
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
  });

  it('Input with a validation error', async () => {
    const user = userEvent.setup();
    const { container } = renderApp('/');
    await user.type(screen.getByLabelText(/Tile sequence/), 'DIMFLVB');
    await screen.findByRole('alert');
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
  });

  it('Tile picker, map and list views', async () => {
    const user = userEvent.setup();
    const { container } = renderApp('/protein/A6NMZ7');
    await screen.findByRole('heading', { name: 'COL6A6 (A6NMZ7)' });
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
    await user.click(screen.getByRole('button', { name: 'Show a list of tiles' }));
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
  });

  it('Result for a typed sequence, with the layers disabled', async () => {
    const user = userEvent.setup();
    const { container } = renderApp('/');
    await user.type(screen.getByLabelText(/Tile sequence/), REAL_TILE);
    await user.click(screen.getByRole('button', { name: 'Predict' }));
    await screen.findByTestId('heatmap');
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
  }, 60_000);

  it('Result for a stored tile with both layers on, and the table view', async () => {
    const user = userEvent.setup();
    const { container } = renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('heatmap');
    await user.click(screen.getByRole('checkbox', { name: 'Measured ΔPSI' }));
    await user.click(screen.getByRole('checkbox', { name: 'ClinVar variants' }));
    await screen.findByRole('list', { name: 'ClinVar marker shapes' });
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
    await user.click(screen.getByRole('button', { name: 'Show as a table' }));
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
  }, 60_000);

  it('Refusal page and the page after the override', async () => {
    const user = userEvent.setup();
    const { container } = renderApp('/result/uniprot/A6NMZ7/5');
    await screen.findByTestId('refusal');
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
    await user.click(screen.getByRole('button', { name: 'Score anyway' }));
    await screen.findByTestId('override-banner');
    expect(await axe(container, OPTIONS)).toHaveNoViolations();
  }, 60_000);

  it('Model card, About, share error and not-found pages', async () => {
    for (const route of ['/model', '/about', '/shared/00000000-0000-4000-8000-000000000410#t=AAAAAAAAAAAAAAAAAAAAAAAA', '/nowhere']) {
      const { container, unmount } = renderApp(route);
      await screen.findByRole('heading', { level: 1 });
      expect(await axe(container, OPTIONS), route).toHaveNoViolations();
      unmount();
    }
  }, 60_000);
});
