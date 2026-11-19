import { useEffect } from 'react';

/**
 * Single-key shortcuts (plan-system 5.2). Ignored while typing in a field and with Ctrl/Alt/Meta, and can be turned off
 * (WCAG 2.1.4 Character Key Shortcuts) — the choice is one flag in localStorage. Screen readers in browse mode keep their
 * own single-key navigation; these shortcuts act only when the page receives the key.
 */
const KEY = 'df-shortcuts';

export function shortcutsEnabled(): boolean {
  try {
    return window.localStorage.getItem(KEY) !== 'off';
  } catch {
    return true;
  }
}

export function setShortcutsEnabled(on: boolean): void {
  try {
    if (on) window.localStorage.removeItem(KEY);
    else window.localStorage.setItem(KEY, 'off');
  } catch {
    // storage blocked: the choice lasts for this page only
  }
  window.dispatchEvent(new Event('df-shortcuts-changed'));
}

function typing(target: EventTarget | null): boolean {
  const el = target as HTMLElement | null;
  if (!el) return false;
  const tag = el.tagName;
  return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || el.isContentEditable || Boolean(el.closest?.('dialog[open]'));
}

/** Registers handlers for keys like 'v', 't', '/', '?' while the component is mounted. */
export function useShortcuts(map: Record<string, () => void>): void {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.altKey || e.metaKey || e.defaultPrevented || !shortcutsEnabled() || typing(e.target)) return;
      const fn = map[e.key];
      if (fn) {
        e.preventDefault();
        fn();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [map]);
}
