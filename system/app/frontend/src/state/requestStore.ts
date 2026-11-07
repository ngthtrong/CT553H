import type { TileRequest } from '../api/types';

/**
 * In-memory holder of a typed-sequence request.
 *
 * Privacy rule (ui-design §3.1): a typed sequence is never put in the URL, localStorage,
 * sessionStorage or history state. It lives in this module variable only, so a page reload
 * forgets it by design.
 */
let current: TileRequest | null = null;

export const requestStore = {
  set(req: TileRequest): void {
    current = req;
  },
  get(): TileRequest | null {
    return current;
  },
  clear(): void {
    current = null;
  },
};
