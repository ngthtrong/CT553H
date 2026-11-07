import 'vitest';

// vitest-axe registers the matcher at runtime (tests/setup.ts); this declares it for the type checker under vitest 5.
declare module 'vitest' {
  interface Assertion {
    toHaveNoViolations(): void;
  }
  interface AsymmetricMatchersContaining {
    toHaveNoViolations(): void;
  }
}
