import { useCallback, useEffect, useState } from 'react';

export type ThemeMode = 'system' | 'light' | 'dark';
const KEY = 'df-theme';

function readStored(): ThemeMode {
  try {
    const v = window.localStorage.getItem(KEY);
    return v === 'light' || v === 'dark' ? v : 'system';
  } catch {
    return 'system';
  }
}

function systemPrefersDark(): boolean {
  return typeof window.matchMedia === 'function' && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

export function applyTheme(mode: ThemeMode): void {
  const effective = mode === 'system' ? (systemPrefersDark() ? 'dark' : 'light') : mode;
  document.documentElement.setAttribute('data-theme', effective);
}

/** Theme follows the system preference with a manual override (ui-design §5). Only the choice is stored. */
export function useTheme(): [ThemeMode, (m: ThemeMode) => void] {
  const [mode, setModeState] = useState<ThemeMode>(readStored);

  useEffect(() => {
    applyTheme(mode);
    if (mode !== 'system' || typeof window.matchMedia !== 'function') return undefined;
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const onChange = () => applyTheme('system');
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, [mode]);

  const setMode = useCallback((m: ThemeMode) => {
    setModeState(m);
    try {
      if (m === 'system') window.localStorage.removeItem(KEY);
      else window.localStorage.setItem(KEY, m);
    } catch {
      // Storage may be blocked; the choice then lasts for this page view only.
    }
  }, []);

  return [mode, setMode];
}
