import { useState } from 'react';
import { act, fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'vitest-axe';
import { describe, expect, it, vi } from 'vitest';
import { Heatmap, cellKey } from '../src/components/Heatmap';
import { RankTable, type RankFilter } from '../src/components/RankTable';
import { SequenceInput } from '../src/components/SequenceInput';
import { TileMap } from '../src/components/TileMap';
import { WarningList } from '../src/components/WarningList';
import { handle } from '../mock/handler';
import type { Cell, ClinvarVariant, MeasuredCell, PredictionResult, TileSummary } from '../src/api/types';

const result = JSON.parse(handle('POST', '/v1/predict', {}, JSON.stringify({ uniprot_id: 'A6NMZ7', tile_index: 28 })).body) as PredictionResult;
const EV = result.provenance.event_definition;

function HeatmapHarness(props: Partial<React.ComponentProps<typeof Heatmap>> & { onPick?: (c: Cell) => void }) {
  const [sel, setSel] = useState<string | null>(null);
  return (
    <Heatmap
      cells={result.cells}
      tile={result.tile}
      mode="prob"
      eventDefinition={EV}
      selectedKey={sel}
      onSelect={(c) => {
        setSel(cellKey(c.position, c.mut_aa));
        props.onPick?.(c);
      }}
      {...props}
    />
  );
}

describe('Heatmap (FR-06, ui-design §3.3, §6, §7)', () => {
  it('draws 28 rows, 28 wild-type cells and 532 substitution cells in one SVG', () => {
    render(<HeatmapHarness />);
    const svg = screen.getByTestId('heatmap');
    expect(svg.querySelectorAll('[role="row"]')).toHaveLength(29);
    const cells = svg.querySelectorAll('[role="gridcell"]');
    expect(cells).toHaveLength(28 * 20);
    expect([...cells].filter((c) => c.getAttribute('aria-label')?.includes('wild type'))).toHaveLength(28);
  });

  it('describes a cell with position, amino acids, probability with its event, raw score and rank', () => {
    render(<HeatmapHarness />);
    const first = screen.getByLabelText(/^position 1, D to A, probability P\(DeltaPSI >= 1\.0\) 0\.028, raw score -0\.048, rank \d+ of 532/);
    expect(first).toBeInTheDocument();
  });

  it('has a single tab stop and moves with the arrow keys, Home and End', async () => {
    const user = userEvent.setup();
    render(<HeatmapHarness />);
    const grid = screen.getByRole('grid');
    expect(grid.querySelectorAll('[role="gridcell"][tabindex="0"]')).toHaveLength(1);
    const start = grid.querySelector('[role="gridcell"][tabindex="0"]') as SVGElement;
    start.focus();
    await user.keyboard('{ArrowRight}');
    expect(document.activeElement?.getAttribute('aria-label')).toMatch(/^position 1, D to C/);
    await user.keyboard('{ArrowDown}');
    expect(document.activeElement?.getAttribute('aria-label')).toMatch(/^position 2, I to C/);
    await user.keyboard('{End}');
    expect(document.activeElement?.getAttribute('aria-label')).toMatch(/^position 2, I to Y/);
    await user.keyboard('{Home}');
    expect(document.activeElement?.getAttribute('aria-label')).toMatch(/^position 2, I to A/);
    expect(grid.querySelectorAll('[role="gridcell"][tabindex="0"]')).toHaveLength(1);
  });

  it('selects a cell with Enter and shows its details in the live region', async () => {
    const user = userEvent.setup();
    const onPick = vi.fn();
    render(<HeatmapHarness onPick={onPick} />);
    const cell = screen.getByLabelText(/^position 14, P to W/);
    cell.focus();
    await user.keyboard('{Enter}');
    expect(onPick).toHaveBeenCalledWith(expect.objectContaining({ position: 14, mut_aa: 'W' }));
    expect(screen.getByTestId('cell-details')).toHaveTextContent(/Position 14, P → W\. Probability P\(DeltaPSI >= 1\.0\)/);
  });

  it('does not select a wild-type cell', async () => {
    const user = userEvent.setup();
    const onPick = vi.fn();
    render(<HeatmapHarness onPick={onPick} />);
    screen.getByLabelText('position 1, wild type D, no substitution').focus();
    await user.keyboard('{Enter}');
    expect(onPick).not.toHaveBeenCalled();
  });

  it('switches the legend between probability and raw score and names the event', () => {
    const { rerender } = render(<HeatmapHarness />);
    expect(screen.getByText(/Probability that the substitution raises PSI by at least one bin/)).toHaveTextContent('P(DeltaPSI >= 1.0)');
    rerender(<HeatmapHarness mode="raw" />);
    expect(screen.getByText(/not a probability/)).toBeInTheDocument();
  });

  it('marks measured cells with an outline and ClinVar variants with a shape per class, and repeats the disclaimer in the card', () => {
    const measured: MeasuredCell[] = [{ position: 3, mut_aa: 'W', delta_psi: 1.2, in_training_set: true }];
    const clinvar: ClinvarVariant[] = [
      { variation_id: 1, protein_pos: 624, position: 3, ref_aa: 'M', alt_aa: 'W', clinsig: 'pathogenic', review_status: 'x', last_evaluated: null },
      { variation_id: 2, protein_pos: 628, position: 7, ref_aa: 'D', alt_aa: 'N', clinsig: 'vus', review_status: null, last_evaluated: null },
    ];
    render(<HeatmapHarness measured={measured} clinvar={clinvar} clinvarNote="NOTE-ATTRIBUTION NOTE-DISCLAIMER" />);
    const svg = screen.getByTestId('heatmap');
    expect(svg.querySelectorAll('.measured-ring')).toHaveLength(1);
    expect(svg.querySelectorAll('.glyph')).toHaveLength(2);
    expect(screen.getByRole('list', { name: 'ClinVar marker shapes' })).toHaveTextContent(/pathogenic/);
    act(() => screen.getByLabelText(/^position 3, M to W/).focus());
    const card = screen.getByTestId('cell-details');
    expect(card).toHaveTextContent('Measured ΔPSI: 1.20');
    expect(card).toHaveTextContent('ClinVar 1: M624W, pathogenic');
    expect(card).toHaveTextContent('NOTE-ATTRIBUTION NOTE-DISCLAIMER');
  });

  it('has no axe violations', async () => {
    const { container } = render(<HeatmapHarness />);
    expect(await axe(container, { rules: { 'color-contrast': { enabled: false } } })).toHaveNoViolations();
  });
});

function TableHarness({ cells = result.cells }: { cells?: Cell[] }) {
  const [filter, setFilter] = useState<RankFilter>({ position: null, aa: null });
  const [sel, setSel] = useState<string | null>(null);
  return <RankTable cells={cells} eventDefinition={EV} filter={filter} onFilter={setFilter} selectedKey={sel} onSelect={(c) => setSel(cellKey(c.position, c.mut_aa))} />;
}

describe('RankTable (FR-07, FR-08; E2E-02)', () => {
  it('lists all 532 substitutions ranked, with the top 10 % written as text', () => {
    render(<TableHarness />);
    // Role queries over 532 rows are slow in jsdom; read the DOM directly.
    const rows = [...screen.getByTestId('rank-table').querySelectorAll('tbody tr')];
    const col = (r: Element, i: number) => r.querySelectorAll('td')[i]?.textContent;
    expect(rows).toHaveLength(532);
    expect(col(rows[0]!, 0)).toBe('1');
    expect(rows.filter((r) => col(r, 6) === 'yes')).toHaveLength(54);
    expect(col(rows[53]!, 6)).toBe('yes');
    expect(col(rows[54]!, 6)).toBe('no');
  });

  it('sorts by the probability column and announces the sort', async () => {
    const user = userEvent.setup();
    render(<TableHarness />);
    const header = screen.getByRole('columnheader', { name: /P\(DeltaPSI >= 1\.0\)/ });
    await user.click(within(header).getByRole('button'));
    expect(header).toHaveAttribute('aria-sort', 'descending');
    const first = screen.getByTestId('rank-table').querySelector('tbody tr')!;
    const top = [...result.cells].sort((a, b) => b.p_dpsi_ge_1_calibrated - a.p_dpsi_ge_1_calibrated)[0]!;
    expect(first.querySelectorAll('td')[5]?.textContent).toBe(top.p_dpsi_ge_1_calibrated.toFixed(3));
    await user.click(within(header).getByRole('button'));
    expect(header).toHaveAttribute('aria-sort', 'ascending');
  });

  it('filters by position and substituted amino acid, and says so when nothing matches', async () => {
    const user = userEvent.setup();
    render(<TableHarness />);
    await user.selectOptions(screen.getByLabelText('Position'), '14');
    await user.selectOptions(screen.getByLabelText('Substituted amino acid'), 'W');
    const rows = [...screen.getByTestId('rank-table').querySelectorAll('tbody tr')];
    expect(rows).toHaveLength(1);
    expect(rows[0]!.querySelectorAll('td')[3]?.textContent).toBe('W');
    expect(screen.getByText('Showing 1 of 532')).toBeInTheDocument();
    // Position 14 is P, so substituting P is not a cell: no rows.
    await user.selectOptions(screen.getByLabelText('Substituted amino acid'), 'P');
    expect(screen.getByText('No substitutions match the filters.')).toBeInTheDocument();
  });

  it('selects a row on click and marks it as current', async () => {
    const user = userEvent.setup();
    render(<TableHarness />);
    const row = screen.getByTestId('rank-table').querySelectorAll('tbody tr')[2]!;
    await user.click(row);
    expect(row).toHaveAttribute('aria-current', 'true');
  });

  it('has no axe violations', async () => {
    // A slice keeps axe fast in jsdom; the structure is the same for all 532 rows.
    const { container } = render(<TableHarness cells={result.cells.slice(0, 40)} />);
    expect(await axe(container, { rules: { 'color-contrast': { enabled: false } } })).toHaveNoViolations();
  }, 30_000);
});

describe('SequenceInput (FR-03; E2E-08)', () => {
  function Harness({ initial = '', forceShow = false }: { initial?: string; forceShow?: boolean }) {
    const [v, setV] = useState(initial);
    return <SequenceInput value={v} onChange={setV} forceShow={forceShow} />;
  }

  it('counts characters live', async () => {
    const user = userEvent.setup();
    render(<Harness />);
    await user.type(screen.getByLabelText(/Tile sequence/), 'DIMF');
    expect(screen.getByText('4 / 28 characters')).toBeInTheDocument();
  });

  it('names an offending character at once, marks it, and links the message to the field', async () => {
    const user = userEvent.setup();
    render(<Harness />);
    const input = screen.getByLabelText(/Tile sequence/);
    await user.type(input, 'DIMFLVB');
    expect(screen.getByRole('alert')).toHaveTextContent("Position 7: 'B' is not a standard amino acid.");
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input.getAttribute('aria-describedby')).toContain(screen.getByRole('alert').id);
    expect(screen.getByTestId('sequence-preview').querySelectorAll('mark')).toHaveLength(1);
  });

  it('does not nag about length while typing, but does when too long, after blur, or after a blocked submit', async () => {
    const user = userEvent.setup();
    const { unmount } = render(<Harness />);
    const input = screen.getByLabelText(/Tile sequence/);
    await user.type(input, 'DIMFLV');
    expect(screen.queryByRole('alert')).toBeNull();
    fireEvent.blur(input);
    expect(screen.getByRole('alert')).toHaveTextContent('it has 6');
    unmount();
    render(<Harness initial={'A'.repeat(29)} />);
    expect(screen.getByRole('alert')).toHaveTextContent('it has 29');
    cleanupAlerts();
    render(<Harness initial="DIM" forceShow />);
    expect(screen.getAllByRole('alert').at(-1)).toHaveTextContent('it has 3');
  });
});

function cleanupAlerts() {
  document.body.innerHTML = '';
}

describe('TileMap (FR-16, ui-design §3.2)', () => {
  const tiles: TileSummary[] = [
    { tile_index: 1, start_pos: 1, end_pos: 28, sequence: 'A'.repeat(28), scorable: true, domain_status: 'measured_in_domain', psi_wt_measured: 1.5, reads_measured: 20 },
    { tile_index: 2, start_pos: 24, end_pos: 51, sequence: 'A'.repeat(28), scorable: false, domain_status: 'unknown', psi_wt_measured: null, reads_measured: null },
    { tile_index: 3, start_pos: 47, end_pos: 74, sequence: 'A'.repeat(28), scorable: true, domain_status: 'measured_out_of_domain', psi_wt_measured: 4.8, reads_measured: 30 },
    { tile_index: 4, start_pos: 70, end_pos: 97, sequence: 'A'.repeat(28), scorable: true, domain_status: 'predicted_in_domain', psi_wt_measured: null, reads_measured: null },
  ];

  it('has one tab stop, skips disabled tiles with the arrow keys, and selects with Enter', async () => {
    const user = userEvent.setup();
    const onSelect = vi.fn();
    render(<TileMap tiles={tiles} onSelect={onSelect} />);
    const radios = screen.getAllByRole('radio');
    expect(radios.filter((r) => r.tabIndex === 0)).toHaveLength(1);
    radios[0]!.focus();
    await user.keyboard('{ArrowRight}');
    expect(document.activeElement).toBe(radios[2]);
    await user.keyboard('{Enter}');
    expect(onSelect).toHaveBeenCalledWith(3);
    await user.keyboard('{End}');
    expect(document.activeElement).toBe(radios[3]);
  });

  it('describes every tile in words and disables tiles that cannot be scored', async () => {
    const user = userEvent.setup();
    const onSelect = vi.fn();
    render(<TileMap tiles={tiles} onSelect={onSelect} />);
    expect(screen.getByRole('radio', { name: /tile 3, residues 47–74, outside the domain \(measured\), tile PSI 4\.80/ })).toBeInTheDocument();
    const disabled = screen.getByRole('radio', { name: /tile 2.*cannot be scored/ });
    expect(disabled).toHaveAttribute('aria-disabled', 'true');
    await user.click(disabled);
    expect(onSelect).not.toHaveBeenCalled();
    expect(screen.getByRole('radio', { name: /tile 4.*in domain \(predicted\)/ })).toHaveTextContent('p');
  });

  it('repeats the status in a pattern class, not only in colour', () => {
    render(<TileMap tiles={tiles} onSelect={() => undefined} />);
    const radios = screen.getAllByRole('radio');
    expect(radios.map((r) => ['solid', 'hatched', 'dotted', 'empty'].find((c) => r.classList.contains(c)))).toEqual(['solid', 'empty', 'hatched', 'solid']);
  });
});

describe('WarningList (W-2, W-3, W-7)', () => {
  it('shows an override as a red banner and other warnings as amber, as alerts after a request', () => {
    render(
      <WarningList
        overridden
        warnings={[
          { code: 'OUT_OF_DOMAIN_OVERRIDDEN', message: 'o' },
          { code: 'TRAINING_PEPTIDE', message: 'training' },
          { code: 'DOMAIN_UNKNOWN', message: 'unknown' },
        ]}
      />,
    );
    expect(screen.getByTestId('override-banner')).toHaveTextContent(/Out-of-domain override/);
    expect(screen.getByTestId('override-banner')).toHaveAttribute('role', 'alert');
    const w = screen.getByTestId('warning-list');
    expect(w).toHaveTextContent('training');
    expect(w).toHaveTextContent('unknown');
    expect(w).not.toHaveTextContent('o,');
  });

  it('is a note, not an alert, when it is not announced', () => {
    render(<WarningList overridden={false} announce={false} warnings={[{ code: 'DOMAIN_UNKNOWN', message: 'unknown' }]} />);
    expect(screen.getByTestId('warning-list')).toHaveAttribute('role', 'note');
  });
});
