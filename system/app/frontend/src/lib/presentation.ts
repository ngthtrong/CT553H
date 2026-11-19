import { useCallback, useEffect, useState } from 'react';

/**
 * Presentation mode for the defence (plan-system 5.4): larger matrix and text, secondary panels hidden, limitation
 * labels and warnings kept (R-1). Toggled by a button or Alt+Shift+P; remembered for the browser session only (a
 * flag, never data).
 */
const KEY = 'df-presentation';
export const PRESENTATION_SHORTCUT = 'Alt+Shift+P';

function read(): boolean {
  try {
    return window.sessionStorage.getItem(KEY) === '1';
  } catch {
    return false;
  }
}

export function usePresentation(): [boolean, () => void] {
  const [on, setOn] = useState(read);
  useEffect(() => {
    const root = document.documentElement;
    if (on) root.setAttribute('data-presentation', 'on');
    else root.removeAttribute('data-presentation');
    try {
      if (on) window.sessionStorage.setItem(KEY, '1');
      else window.sessionStorage.removeItem(KEY);
    } catch {
      // storage blocked: the mode simply does not survive a reload
    }
  }, [on]);
  const toggle = useCallback(() => setOn((v) => !v), []);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.altKey && e.shiftKey && !e.ctrlKey && !e.metaKey && (e.key === 'P' || e.key === 'p' || e.code === 'KeyP')) {
        e.preventDefault();
        toggle();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [toggle]);
  return [on, toggle];
}
