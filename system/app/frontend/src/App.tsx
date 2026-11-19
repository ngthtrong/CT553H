import { lazy, Suspense } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { AppShell } from './components/AppShell';
import { AboutPage } from './pages/AboutPage';
import { AdminPage } from './pages/AdminPage';
import { AnalysisPage } from './pages/AnalysisPage';
import { DatasetPage, ImportPage } from './pages/ImportPages';
import { JobPage } from './pages/JobPage';
import { ProjectPage } from './pages/ProjectPage';
import { ProjectsPage } from './pages/ProjectsPage';
import { InputPage } from './pages/InputPage';
import { ModelCardPage } from './pages/ModelCardPage';
import { ModelComparisonPage } from './pages/ModelComparisonPage';
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
        <Route path="/new" element={<InputPage />} />
        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/projects/:id" element={<ProjectPage />} />
        <Route path="/analyses/:id" element={<AnalysisPage />} />
        <Route path="/jobs/:id" element={<JobPage />} />
        <Route path="/import" element={<ImportPage />} />
        <Route path="/datasets/:id" element={<DatasetPage />} />
        <Route path="/model-comparisons/:id" element={<ModelComparisonPage />} />
        <Route path="/protein/:acc" element={<TilePickerPage />} />
        <Route path="/result" element={<TypedResultPage />} />
        <Route path="/result/uniprot/:acc/:n" element={<StoredResultPage />} />
        <Route path="/shared/:runId" element={<SharedPage />} />
        <Route path="/model" element={<ModelCardPage />} />
        <Route path="/model/:id" element={<ModelCardPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/admin" element={<AdminPage />} />
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
