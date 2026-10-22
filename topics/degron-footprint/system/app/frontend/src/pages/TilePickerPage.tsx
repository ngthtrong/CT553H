import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { ErrorBanner } from '../components/ErrorBanner';
import { ProvenanceFooter } from '../components/ProvenanceFooter';
import { DomainLegend, TileMap, tileDescription } from '../components/TileMap';
import { useDocumentTitle } from '../lib/hooks';
import { STATUS } from '../lib/domain';
import { fmtPsi } from '../lib/format';
import type { TileSummary } from '../api/types';

export function TilePickerPage() {
  const { acc = '' } = useParams();
  const navigate = useNavigate();
  const [selected, setSelected] = useState<number | null>(null);
  const [list, setList] = useState(false);
  useDocumentTitle(`Tiles of ${acc}`);

  const q = useQuery({
    queryKey: ['tiles', acc],
    queryFn: ({ signal }) => api.listTiles(acc, signal),
    retry: false,
    staleTime: 300_000,
  });

  if (q.isPending) return <p aria-live="polite">Loading tiles of {acc}…</p>;
  if (q.isError) {
    return (
      <>
        <h1>Tiles of {acc}</h1>
        <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />
        <p>
          <Link to="/">Back to the input page</Link>
        </p>
      </>
    );
  }

  const { protein, tiles, provenance } = q.data;
  const tile: TileSummary | undefined = tiles.find((t) => t.tile_index === selected);

  return (
    <>
      <h1>
        {protein.gene_symbol ?? protein.uniprot_id} ({protein.uniprot_id})
      </h1>
      <p className="muted">
        {protein.protein_name ? `${protein.protein_name} · ` : ''}
        {protein.length.toLocaleString('en-US')} residues · {protein.n_tiles} tiles
      </p>

      <h2>Tile map</h2>
      <p className="muted">One box per tile, left to right = N to C terminus. Use the arrow keys to move and Space or Enter to choose.</p>
      <div className="row">
        <button type="button" onClick={() => setList((v) => !v)} aria-pressed={list}>
          {list ? 'Show the tile map' : 'Show a list of tiles'}
        </button>
      </div>
      {list ? (
        <div className="table-wrap" tabIndex={0} role="region" aria-label="List of tiles">
          <table className="data">
            <caption className="visually-hidden">Tiles of the protein</caption>
            <thead>
              <tr>
                <th scope="col">Tile</th>
                <th scope="col">Residues</th>
                <th scope="col">Domain status</th>
                <th scope="col" className="num">Tile PSI</th>
                <th scope="col">Choose</th>
              </tr>
            </thead>
            <tbody>
              {tiles.map((t) => (
                <tr key={t.tile_index} aria-current={selected === t.tile_index ? 'true' : undefined}>
                  <td>{t.tile_index}</td>
                  <td>{t.start_pos}–{t.end_pos}</td>
                  <td>{STATUS[t.domain_status].label}{t.scorable ? '' : ' · cannot be scored'}</td>
                  <td className="num">{fmtPsi(t.psi_wt_measured)}</td>
                  <td>
                    <button type="button" disabled={!t.scorable} aria-label={`Choose ${tileDescription(t)}`} onClick={() => setSelected(t.tile_index)}>
                      Choose
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <TileMap tiles={tiles} selected={selected} onSelect={setSelected} />
      )}
      <DomainLegend />

      <section aria-live="polite" className="card" aria-label="Selected tile">
        {tile ? (
          <>
            <h2 style={{ marginTop: 0 }}>
              Selected: tile {tile.tile_index} (residues {tile.start_pos}–{tile.end_pos})
            </h2>
            <p className="seq" translate="no">{tile.sequence}</p>
            <p>
              Status: <strong>{STATUS[tile.domain_status].label}</strong>
              {tile.psi_wt_measured !== null && tile.psi_wt_measured !== undefined && <> (measured tile PSI {fmtPsi(tile.psi_wt_measured)})</>}
            </p>
            {tile.domain_status === 'measured_out_of_domain' && (
              <div className="banner warn" role="note">
                <span className="label">Warning</span>
                This tile is measured to be outside the domain of the model. The next page will ask before scoring it.
              </div>
            )}
          </>
        ) : (
          <p className="muted">No tile selected yet. Tiles that cannot be scored are disabled.</p>
        )}
        <button
          type="button"
          className="primary"
          disabled={!tile}
          onClick={() => tile && navigate(`/result/uniprot/${protein.uniprot_id}/${tile.tile_index}`)}
        >
          Predict this tile
        </button>
      </section>
      <ProvenanceFooter provenance={provenance} />
    </>
  );
}

