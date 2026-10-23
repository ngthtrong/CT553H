import { useEffect, useRef, type ReactNode } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { useTheme, type ThemeMode } from '../lib/theme';

function ThemeSwitch() {
  const [mode, setMode] = useTheme();
  return (
    <label className="row" style={{ gap: '0.4rem' }}>
      <span className="muted">Theme</span>
      <select value={mode} onChange={(e) => setMode(e.target.value as ThemeMode)} aria-label="Colour theme">
        <option value="system">System</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
    </label>
  );
}

export function AppShell({ children }: { children: ReactNode }) {
  const { pathname } = useLocation();
  const main = useRef<HTMLElement>(null);
  const first = useRef(true);

  // After a route change, move focus to the main region so keyboard and screen-reader users start at the new page.
  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    main.current?.focus({ preventScroll: false });
  }, [pathname]);

  return (
    <>
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <header className="app-header">
        <div className="inner">
          <Link to="/" className="brand">
            Degron Footprint
          </Link>
          <nav aria-label="Main" className="app-nav">
            <NavLink to="/" end>
              Input
            </NavLink>
            <NavLink to="/model">Model card</NavLink>
            <NavLink to="/about">About &amp; data</NavLink>
          </nav>
          <ThemeSwitch />
        </div>
      </header>
      <main id="main" ref={main} tabIndex={-1}>
        {children}
      </main>
      <footer className="app-footer">
        <div className="inner">
          Research prototype. Scores describe one assay (GPS, Zhang et al. 2023) and are not a probability of disease or a
          diagnosis.
        </div>
      </footer>
    </>
  );
}
