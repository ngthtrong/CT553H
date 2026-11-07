import { render } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { App } from '../src/App';

/** Exposes the router location (path, query, hash and history state) so that tests can prove what is in the address. */
function LocationProbe() {
  const loc = useLocation();
  return <output data-testid="location" hidden>{JSON.stringify({ pathname: loc.pathname, search: loc.search, hash: loc.hash, state: loc.state })}</output>;
}

export function renderApp(route = '/') {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false, refetchOnWindowFocus: false } } });
  const utils = render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[route]}>
        <App />
        <LocationProbe />
      </MemoryRouter>
    </QueryClientProvider>,
  );
  const location = () => JSON.parse(utils.getByTestId('location').textContent ?? '{}') as { pathname: string; search: string; hash: string; state: unknown };
  return { ...utils, client, location };
}

export const REAL_TILE = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';
