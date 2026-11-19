import { screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { MOCK_SLOW_MODEL_ID } from '../mock/handler';
import { describeEstimate, estimate, fmtDuration } from '../src/lib/models';
import { REAL_TILE, renderApp } from './utils';

/** plan-system 1.1 — model selection on New analysis, the result page and the model card (MSEL-01…03, UI side). */
describe('MSEL model selection', () => {
  it('lists every effect model, keeps a model that does not serve unselectable and says why', async () => {
    renderApp('/');
    const select = await screen.findByLabelText('Model');
    await waitFor(() => expect(within(select).getAllByRole('option')).toHaveLength(3));
    const retired = within(select).getByRole('option', { name: /mock-retired-v0/ });
    expect(retired).toBeDisabled();
    expect(screen.getByTestId('model-not-serving')).toHaveTextContent('mock-retired-v0 cannot be chosen: model status is retired');
    expect(within(select).getByRole('option', { name: /\(default\)/ })).toHaveValue('');
    // gates are not effect models and are not offered
    expect(within(select).queryByRole('option', { name: /gate/ })).toBeNull();
  });

  it('MSEL-02: a chosen model goes into ?model= (id only), asks before a slow model and shows in the provenance', async () => {
    const user = userEvent.setup();
    const { location } = renderApp('/');
    const select = await screen.findByLabelText('Model');
    await waitFor(() => expect(within(select).getByRole('option', { name: MOCK_SLOW_MODEL_ID })).toBeEnabled());
    await user.selectOptions(select, MOCK_SLOW_MODEL_ID);
    expect(location().search).toBe(`?model=${MOCK_SLOW_MODEL_ID}`);
    await user.type(screen.getByLabelText(/Tile sequence/), REAL_TILE);
    await user.click(screen.getByRole('button', { name: 'Predict' }));
    // 38 s per tile > 20 s: the user confirms first
    expect(await screen.findByTestId('slow-model-estimate')).toHaveTextContent('≈ 1 tile × 38.0 s ≈ 38 s');
    expect(location().pathname).toBe('/');
    await user.click(screen.getByRole('button', { name: 'Start anyway' }));
    await screen.findByTestId('heatmap');
    expect(screen.getAllByText(MOCK_SLOW_MODEL_ID).length).toBeGreaterThan(0);
    expect(JSON.stringify(location())).not.toContain(REAL_TILE);
  });

  it('a fast model starts without a confirmation; "Run with another model" scores the same tile again', async () => {
    const user = userEvent.setup();
    const { location } = renderApp('/result/uniprot/A6NMZ7/1');
    await screen.findByTestId('heatmap');
    expect(screen.queryByTestId('slow-model-estimate')).toBeNull();
    const rerun = await screen.findByTestId('rerun-model');
    expect(within(rerun).getByRole('combobox')).toHaveValue(MOCK_SLOW_MODEL_ID);
    await user.click(within(rerun).getByRole('button', { name: 'Run with another model' }));
    await user.click(await screen.findByRole('button', { name: 'Start anyway' }));
    await waitFor(() => expect(location().search).toBe(`?model=${MOCK_SLOW_MODEL_ID}`));
    await waitFor(() => expect(screen.getAllByText(MOCK_SLOW_MODEL_ID).length).toBeGreaterThan(0));
    expect(location().pathname).toBe('/result/uniprot/A6NMZ7/1');
  });

  it('an invalid ?model= value is ignored, not sent', async () => {
    renderApp('/?model=<script>');
    const select = await screen.findByLabelText('Model');
    expect(select).toHaveValue('');
  });

  it('/model/:id shows the card of that model with its serving state', async () => {
    renderApp(`/model/${MOCK_SLOW_MODEL_ID}`);
    expect(await screen.findByRole('heading', { level: 1 })).toHaveTextContent(MOCK_SLOW_MODEL_ID);
    expect(screen.getByText(/· serving/)).toBeInTheDocument();
  });

  it('formats the estimate', () => {
    const m = { model_id: 'x', role: 'effect', status: 'frozen', is_default: false, serving: true, not_serving_reason: null, expected_tile_seconds: 38 } as const;
    expect(describeEstimate(estimate(m, 382)!)).toBe('≈ 382 tiles × 38.0 s ≈ 4.0 h');
    expect(estimate({ ...m, expected_tile_seconds: null }, 10)).toBeNull();
    expect(fmtDuration(600)).toBe('10 min');
  });
});
