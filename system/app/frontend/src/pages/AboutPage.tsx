import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { ErrorBanner } from '../components/ErrorBanner';
import { useDocumentTitle } from '../lib/hooks';

export function AboutPage() {
  useDocumentTitle('About and data');
  const q = useQuery({ queryKey: ['sources'], queryFn: ({ signal }) => api.listSources(signal), retry: false, staleTime: 300_000 });
  return (
    <>
      <h1>About and data sources</h1>
      <h2>What this tool is not</h2>
      <p>
        This is a research prototype. It predicts the effect of single amino-acid substitutions on the stability index of one assay
        (GPS, Zhang et al. 2023). It gives no diagnosis, no risk of disease and no statement on what causes a disease. A
        probability shown here is the probability of the assay event stated next to it.
      </p>
      <h2>Privacy</h2>
      <p>
        A typed sequence is used to compute the prediction and is not written to the address, to the browser storage or to the
        server logs. The server stores a sequence only if you create a share link, and then for the number of days you chose
        (at most 30). The interface sends your input to no other service.
      </p>
      <h2>Data sources and licences</h2>
      {q.isPending && <p role="status" aria-live="polite">Loading the sources…</p>}
      {q.isError && <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />}
      {q.isSuccess && (
        <div className="table-wrap" tabIndex={0} role="region" aria-label="Data sources, scrollable">
          <table className="data" data-testid="sources-table">
            <caption className="visually-hidden">Data sources, versions, licences and required attribution</caption>
            <thead>
              <tr>
                <th scope="col">Source</th><th scope="col">Version</th><th scope="col">Licence</th>
                <th scope="col">Attribution</th><th scope="col">Notice</th>
              </tr>
            </thead>
            <tbody>
              {q.data.items.map((s) => (
                <tr key={s.source_id}>
                  <th scope="row">{s.url ? <a href={s.url} rel="noreferrer noopener">{s.name}</a> : s.name}</th>
                  <td>{s.version}</td>
                  <td>{s.license_name}</td>
                  <td>{s.attribution_text}</td>
                  <td>{s.disclaimer_text ?? ''}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <h2>How to cite</h2>
      <p>
        Cite the data sources above and the thesis that describes this tool. Cite the model by the identifier on the result page
        (model id and weights SHA-256), because results can differ between model versions.
      </p>
    </>
  );
}
