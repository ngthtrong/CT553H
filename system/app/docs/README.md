# Screenshots

Generated from the real application with the real reference data on 17 Nov 2026 (`frontend/e2e/screenshots.spec.ts`,
run against an API on a copy of `.data/dev.db`; the working database is not changed). Regenerate with an API on port
8000 and `SCREENSHOTS=1 E2E_REAL=1 npx playwright test e2e/screenshots.spec.ts --project=chromium-desktop`.

- `screenshots/light/*.png`, `screenshots/dark/*.png` — 14 screens each, 1440×900.

**Caution for figures:** the comparison screens (`08-comparison`) use an *illustrative* dataset derived from the
prediction itself (named "(illustration)"), so its MAE, residuals and Spearman ρ = 1 are not measurements and must not be
reported as results.
