// Fails when src/api/schema.d.ts is out of date with ../../openapi.yaml (contract drift check).
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const dir = mkdtempSync(join(tmpdir(), 'api-types-'));
const out = join(dir, 'schema.d.ts');
try {
  execFileSync('npx', ['openapi-typescript', '../../openapi.yaml', '-o', out], { stdio: 'ignore' });
  const fresh = readFileSync(out, 'utf8');
  const committed = readFileSync('src/api/schema.d.ts', 'utf8');
  if (fresh !== committed) {
    console.error('src/api/schema.d.ts differs from openapi.yaml. Run: npm run gen:api');
    process.exit(1);
  }
  console.log('API types are up to date with openapi.yaml.');
} finally {
  rmSync(dir, { recursive: true, force: true });
}
