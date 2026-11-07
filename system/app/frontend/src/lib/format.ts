export function fmtProb(p: number): string {
  return p.toFixed(3);
}

export function fmtScore(s: number): string {
  return s.toFixed(3);
}

export function fmtPsi(v: number | null | undefined): string {
  return v === null || v === undefined ? 'n/a' : v.toFixed(2);
}

export function fmtDateTime(iso: string): string {
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? iso : d.toISOString().replace('T', ' ').replace(/\.\d+Z$/, ' UTC');
}

export function todayStamp(now: Date = new Date()): string {
  return now.toISOString().slice(0, 10);
}
