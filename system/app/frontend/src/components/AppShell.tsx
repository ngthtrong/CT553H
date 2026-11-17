import { useEffect, useRef, useState, type ReactNode } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { BookOpenText, Database, FlaskConical, FolderKanban, Menu, X } from 'lucide-react';
import { useTheme, type ThemeMode } from '../lib/theme';

function ThemeSwitch() {
  const [mode, setMode] = useTheme();
  return (
    <label className="row" style={{ gap: '0.4rem' }}>
      <span>Theme</span>
      <select value={mode} onChange={(e) => setMode(e.target.value as ThemeMode)} aria-label="Colour theme">
        <option value="system">System</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
    </label>
  );
}

/** Sidebar navigation of ui-design §12.1: no account menu, the workspace is local. */
const NAV = [
  { to: '/projects', label: 'Projects', icon: FolderKanban, end: false },
  { to: '/', label: 'New analysis', icon: FlaskConical, end: true },
  { to: '/model', label: 'Model & evidence', icon: BookOpenText, end: false },
  { to: '/sources', label: 'Data & sources', icon: Database, end: false },
];

export function AppShell({ children }: { children: ReactNode }) {
  const { pathname } = useLocation();
  const main = useRef<HTMLElement>(null);
  const first = useRef(true);
  const [menuOpen, setMenuOpen] = useState(false);

  // After a route change, move focus to the main region so keyboard and screen-reader users start at the new page.
  useEffect(() => {
    setMenuOpen(false);
    if (first.current) {
      first.current = false;
      return;
    }
    main.current?.focus({ preventScroll: false });
  }, [pathname]);

  return (
    <div className="shell">
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <aside id="app-sidebar" className={`shell__sidebar${menuOpen ? ' is-open' : ''}`} aria-label="Workspace">
        <Link to="/projects" className="shell__brand">
          <span>
            Degron Footprint
            <small>Local workspace</small>
          </span>
        </Link>
        <nav aria-label="Main" className="shell__nav">
          {NAV.map(({ to, label, icon: Icon, end }) => (
            <NavLink key={to} to={to} end={end}>
              <Icon size={20} aria-hidden="true" />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="shell__foot">
          <ThemeSwitch />
          <span>Runs on this computer; nothing is sent elsewhere.</span>
        </div>
      </aside>
      <div className="shell__main">
        <header className="shell__topbar">
          <Link to="/projects" className="shell__brand">
            Degron Footprint
          </Link>
          <button
            type="button"
            className="ui-icon-button"
            aria-expanded={menuOpen}
            aria-controls="app-sidebar"
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            onClick={() => setMenuOpen((o) => !o)}
          >
            {menuOpen ? <X size={22} aria-hidden="true" /> : <Menu size={22} aria-hidden="true" />}
          </button>
        </header>
        <main id="main" ref={main} tabIndex={-1} className="shell__content">
          {children}
        </main>
        <footer className="shell__footer">
          Research prototype. Scores describe one assay (GPS, Zhang et al. 2023) and are not a probability of disease or a
          diagnosis.
        </footer>
      </div>
    </div>
  );
}
