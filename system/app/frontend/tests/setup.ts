import '@testing-library/jest-dom/vitest';
import 'vitest-axe/extend-expect';
import * as axeMatchers from 'vitest-axe/matchers';
import { afterAll, afterEach, beforeAll, beforeEach, expect } from 'vitest';
import { cleanup } from '@testing-library/react';
import { resetMock } from '../mock/handler';
import { requestStore } from '../src/state/requestStore';
import { server } from './server';

expect.extend(axeMatchers);

// jsdom has no modal dialog behaviour; open/close by the attribute so dialog content is reachable in tests. The real
// focus trap and Escape handling are checked in Playwright (e2e).
if (typeof HTMLDialogElement !== 'undefined' && typeof HTMLDialogElement.prototype.showModal !== 'function') {
  HTMLDialogElement.prototype.showModal = function showModal(this: HTMLDialogElement) { this.setAttribute('open', ''); };
  HTMLDialogElement.prototype.close = function close(this: HTMLDialogElement) {
    if (!this.hasAttribute('open')) return;
    this.removeAttribute('open');
    this.dispatchEvent(new Event('close'));
  };
}

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
// The first-visit guide (plan-system 5.1) is tested on its own; elsewhere it is marked as seen.
beforeEach(() => window.localStorage.setItem('df-onboarding-done', '1'));
afterEach(() => {
  cleanup();
  server.resetHandlers();
  resetMock();
  requestStore.clear();
  document.documentElement.removeAttribute('data-theme');
  window.sessionStorage.clear();
  window.localStorage.clear();
});
afterAll(() => server.close());
