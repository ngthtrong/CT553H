import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { App } from './App';
import { applyTheme } from './lib/theme';
import './styles.css';

// Apply the stored or system theme before the first paint of the React tree.
try {
  const stored = window.localStorage.getItem('df-theme');
  applyTheme(stored === 'light' || stored === 'dark' ? stored : 'system');
} catch {
  applyTheme('system');
}

const client = new QueryClient({
  defaultOptions: { queries: { refetchOnWindowFocus: false } },
});

const root = document.getElementById('root');
if (!root) throw new Error('Missing #root element');
createRoot(root).render(
  <StrictMode>
    <QueryClientProvider client={client}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
);
