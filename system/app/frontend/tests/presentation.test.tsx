/** plan-system 5.4 — presentation mode (UX-10, UI side). */
import { fireEvent, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it } from 'vitest';
import { renderApp } from './utils';

afterEach(() => document.documentElement.removeAttribute('data-presentation'));

describe('5.4 presentation mode', () => {
  it('toggles with Alt+Shift+P and the button, keeps the warnings and only a flag in session storage', async () => {
    renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('heatmap');
    fireEvent.keyDown(window, { key: 'P', altKey: true, shiftKey: true });
    expect(document.documentElement.getAttribute('data-presentation')).toBe('on');
    expect(screen.getByTestId('presentation-bar')).toHaveTextContent('warnings and limitations stay');
    expect(window.sessionStorage.getItem('df-presentation')).toBe('1');
    // the limitation labels are still rendered (R-1)
    expect(screen.getByTestId('domain-banner')).toBeInTheDocument();
    expect(screen.getByTestId('warning-list')).toBeInTheDocument();
    expect(screen.getByTestId('evidence-label')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: /Exit/ }));
    expect(document.documentElement.hasAttribute('data-presentation')).toBe(false);
    expect(window.sessionStorage.getItem('df-presentation')).toBeNull();
    await userEvent.click(screen.getByTestId('presentation-toggle'));
    expect(screen.getByTestId('presentation-toggle')).toHaveAttribute('aria-pressed', 'true');
  });
});
