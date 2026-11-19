/** plan-system 5.1 — glossary popovers and the first-visit guide (UX-03, UX-04). */
import { screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { GLOSSARY } from '../src/lib/glossary';
import { renderApp } from './utils';

describe('UX-03 glossary', () => {
  it('opens and closes with the keyboard, is described by the button, keeps the focus', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/A6NMZ7/28');
    const bar = await screen.findByTestId('glossary-bar');
    const btn = within(bar).getByRole('button', { name: 'What is ΔPSI?' });
    btn.focus();
    await user.keyboard('{Enter}');
    expect(btn).toHaveAttribute('aria-expanded', 'true');
    const pop = document.getElementById(btn.getAttribute('aria-controls')!)!;
    expect(pop).toBeVisible();
    expect(btn).toHaveAttribute('aria-describedby', pop.id);
    expect(pop).toHaveTextContent(GLOSSARY.dpsi.text);
    await user.keyboard('{Escape}');
    expect(btn).toHaveAttribute('aria-expanded', 'false');
    expect(pop).not.toBeVisible();
    expect(document.activeElement).toBe(btn);
    expect(btn).not.toHaveAttribute('aria-describedby');
  });
  it('every term has a text; limitation labels remain on the page', async () => {
    for (const g of Object.values(GLOSSARY)) expect(g.text.length).toBeGreaterThan(40);
    renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('glossary-bar');
    expect(screen.getByTestId('evidence-label')).toBeInTheDocument();
  });
});

describe('UX-04 first-visit guide', () => {
  it('shows on the first visit only, steps with Next/Back, and Skip is remembered with a flag', async () => {
    const user = userEvent.setup();
    window.localStorage.removeItem('df-onboarding-done');
    const first = renderApp('/projects');
    const guide = await screen.findByTestId('onboarding');
    expect(guide).toHaveTextContent('step 1 of 4');
    await user.click(within(guide).getByRole('button', { name: 'Next' }));
    expect(guide).toHaveTextContent('Choose a protein');
    await user.click(within(guide).getByRole('button', { name: 'Back' }));
    expect(guide).toHaveTextContent('Create a project');
    await user.click(within(guide).getByRole('button', { name: 'Skip the guide' }));
    expect(screen.queryByTestId('onboarding')).toBeNull();
    expect(window.localStorage.getItem('df-onboarding-done')).toBe('1');
    first.unmount();
    renderApp('/projects');
    await screen.findByRole('heading', { level: 1 });
    expect(screen.queryByTestId('onboarding')).toBeNull();
  });
});
