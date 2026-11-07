import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { SimpleMarkdown, flattenMetrics } from '../src/pages/ModelCardPage';

describe('SimpleMarkdown (model card text from the API)', () => {
  it('renders headings, bold, code, joined paragraphs and lists', () => {
    render(<SimpleMarkdown text={'# Title\n\n**What it predicts.** A `P(x)`\nsecond line.\n\n- one\n- two **b**\n'} />);
    expect(screen.getByRole('heading', { name: 'Title' })).toBeInTheDocument();
    expect(screen.getByText('What it predicts.').tagName).toBe('STRONG');
    expect(screen.getByText('P(x)').tagName).toBe('CODE');
    expect(screen.getByText(/second line\./).closest('p')).toHaveTextContent('What it predicts. A P(x) second line.');
    expect(screen.getAllByRole('listitem')).toHaveLength(2);
  });

  it('never interprets HTML in the text', () => {
    const { container } = render(<SimpleMarkdown text={'<img src=x onerror=alert(1)> <script>alert(2)</script>'} />);
    expect(container.querySelector('img, script')).toBeNull();
    expect(container).toHaveTextContent('<img src=x onerror=alert(1)>');
  });
});

describe('flattenMetrics', () => {
  it('flattens nested objects and keeps numeric arrays on one row', () => {
    expect(flattenMetrics({ a: { b: 1, ci95: [0.1, 0.2] }, c: 'x', d: null })).toEqual([
      { key: 'a.b', value: '1' },
      { key: 'a.ci95', value: '[0.1, 0.2]' },
      { key: 'c', value: 'x' },
    ]);
  });
});
