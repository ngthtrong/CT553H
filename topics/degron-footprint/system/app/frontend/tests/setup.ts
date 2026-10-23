import '@testing-library/jest-dom/vitest';
import 'vitest-axe/extend-expect';
import * as axeMatchers from 'vitest-axe/matchers';
import { afterAll, afterEach, beforeAll, expect } from 'vitest';
import { cleanup } from '@testing-library/react';
import { resetMock } from '../mock/handler';
import { requestStore } from '../src/state/requestStore';
import { server } from './server';

expect.extend(axeMatchers);

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
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
