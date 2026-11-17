import { lazy, Suspense } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { AppShell } from './components/AppShell';
import { AboutPage } from './pages/AboutPage';
import { InputPage } from './pages/InputPage';
import { ModelCardPage } from './pages/ModelCardPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { StoredResultPage, TypedResultPage } from './pages/ResultPage';
import { SharedPage } from './pages/SharedPage';
import { TilePickerPage } from './pages/TilePickerPage';

// Development-only review page (WP1.8); the import is dropped from production builds.
const StyleguidePage = import.meta.env.DEV ? lazy(() => import('./pages/StyleguidePage').then((m) => ({ default: m.StyleguidePage }))) : null;

export function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<InputPage />} />
        <Route path="/protein/:acc" element={<TilePickerPage />} />
        <Route path="/result" element={<TypedResultPage />} />
        <Route path="/result/uniprot/:acc/:n" element={<StoredResultPage />} />
        <Route path="/shared/:runId" element={<SharedPage />} />
        <Route path="/model" element={<ModelCardPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/sources" element={<AboutPage />} />
        {StyleguidePage && (
          <Route path="/__styleguide" element={<Suspense fallback={null}><StyleguidePage /></Suspense>} />
        )}
        <Route path="/index.html" element={<Navigate to="/" replace />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AppShell>
  );
}
