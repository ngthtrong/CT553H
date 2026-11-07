// V4 'Evaluation protocol and main results' - composition script for the Figma MCP tool `use_figma` (Figma Design file).
// Run against file i3WSCDZNccWVUIGDvowiQU (22 Oct 2026, CTU account). Skill names: figma-use,figma-generate-design.
// Prerequisite: the four chart PNGs (src/viz/inputs/ev-*.png, made by evaluation_overview.py) were uploaded with upload_assets
// and carry the image hashes below; the four placeholder frames 3:470..3:473 that upload_assets created are removed at the end.
// All numbers below are read from src/viz/inputs/ev-numbers.json (sources listed there); nothing is recomputed here.
const hex = (s) => ({ r: parseInt(s.slice(1, 3), 16) / 255, g: parseInt(s.slice(3, 5), 16) / 255, b: parseInt(s.slice(5, 7), 16) / 255 });
const C = { ink: '#1E1E1E', muted: '#4A5563', line: '#7A8594', panel: '#F5F7FA', panelStroke: '#D5DBE3', blue: '#0072B2', sky: '#56B4E9',
  green: '#009E73', orange: '#E69F00', pink: '#CC79A7', verm: '#D55E00', white: '#FFFFFF', gray: '#C9D0D9', tan: '#EFE6D2' };
const solid = (c) => [{ type: 'SOLID', color: hex(c) }];
await Promise.all(['Regular', 'Medium', 'Semi Bold', 'Bold'].map((s) => figma.loadFontAsync({ family: 'Inter', style: s })));

const HASH = { lc: '5251ad4da9794ff1eda914280ebd96415fc7a9ab', th: '50c322a6f17f15c6301a9d8533d59a658d97f1b5',
  rel: '48f481a6136bdb56cf05389b1d5c2e5e126f297d', fo: '03e8d04fdd1775c2f16c10465f6ee15813692d48' };

const ICONS = { // lucide-static@0.468.0 (ISC)
  'shield-check': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" /><path d="m9 12 2 2 4-4" />',
  'sigma': '<path d="M18 7V5a1 1 0 0 0-1-1H6.5a.5.5 0 0 0-.4.8l4.5 6a2 2 0 0 1 0 2.4l-4.5 6a.5.5 0 0 0 .4.8H17a1 1 0 0 0 1-1v-2" />',
  'circle-check': '<circle cx="12" cy="12" r="10" /><path d="m9 12 2 2 4-4" />',
  'dna': '<path d="m10 16 1.5 1.5" /><path d="m14 8-1.5-1.5" /><path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993" /><path d="m16.5 10.5 1 1" /><path d="m17 6-2.891-2.891" /><path d="M2 15c6.667-6 13.333 0 20-6" /><path d="m20 9 .891.891" /><path d="M3.109 14.109 4 15" /><path d="m6.5 12.5 1 1" /><path d="m7 18 2.891 2.891" /><path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993" />',
};
function icon(name, color, size) {
  const n = figma.createNodeFromSvg(`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICONS[name]}</svg>`);
  n.name = 'icon/' + name; n.resize(size, size); return n;
}
function text(str, size, style, color, width) {
  const t = figma.createText();
  t.fontName = { family: 'Inter', style }; t.characters = str; t.fontSize = size; t.fills = solid(color);
  if (width) { t.resize(width, 10); t.textAutoResize = 'HEIGHT'; }
  return t;
}
function row(gap, align) { const f = figma.createAutoLayout('HORIZONTAL'); f.itemSpacing = gap; f.counterAxisAlignItems = align || 'CENTER'; f.fills = []; return f; }
function col(gap) { const f = figma.createAutoLayout('VERTICAL'); f.itemSpacing = gap; f.fills = []; return f; }
function badge(n) {
  const f = figma.createAutoLayout('HORIZONTAL'); f.resize(44, 44); f.primaryAxisSizingMode = 'FIXED'; f.counterAxisSizingMode = 'FIXED';
  f.primaryAxisAlignItems = 'CENTER'; f.counterAxisAlignItems = 'CENTER'; f.cornerRadius = 22; f.fills = solid(C.blue); f.name = 'step ' + n;
  f.appendChild(text(String(n), 26, 'Bold', C.white)); return f;
}
function panel(w) {
  const p = figma.createAutoLayout('VERTICAL'); p.resize(w, 100); p.primaryAxisSizingMode = 'AUTO'; p.counterAxisSizingMode = 'FIXED';
  p.paddingLeft = p.paddingRight = p.paddingTop = p.paddingBottom = 24; p.itemSpacing = 16;
  p.fills = solid(C.panel); p.strokes = solid(C.panelStroke); p.strokeWeight = 2; p.cornerRadius = 16; return p;
}
function header(n, label) { const h = row(14); h.appendChild(badge(n)); h.appendChild(text(label, 30, 'Semi Bold', C.ink)); return h; }
function seg(w, fill, label, labelColor, stroke, dashed) {
  const f = figma.createAutoLayout('HORIZONTAL'); f.primaryAxisSizingMode = 'FIXED'; f.counterAxisSizingMode = 'FIXED'; f.resize(w, 44);
  f.primaryAxisAlignItems = 'CENTER'; f.counterAxisAlignItems = 'CENTER'; f.fills = solid(fill);
  if (stroke) { f.strokes = solid(stroke); f.strokeWeight = 2; if (dashed) f.dashPattern = [8, 6]; }
  f.appendChild(text(label, 24, 'Semi Bold', labelColor)); return f;
}
function swatch(fill, stroke, dashed) {
  const r = figma.createRectangle(); r.resize(28, 28); r.cornerRadius = 4; r.fills = solid(fill);
  if (stroke) { r.strokes = solid(stroke); r.strokeWeight = 2; if (dashed) r.dashPattern = [6, 4]; } return r;
}
function img(hash, w, h) {
  const r = figma.createRectangle(); r.resize(w, h); r.fills = [{ type: 'IMAGE', imageHash: hash, scaleMode: 'FILL' }]; return r;
}

const root = figma.createAutoLayout('VERTICAL');
root.name = 'V4 Evaluation protocol and main results';
root.resize(1600, 100); root.primaryAxisSizingMode = 'AUTO'; root.counterAxisSizingMode = 'FIXED';
root.paddingLeft = root.paddingRight = 64; root.paddingTop = 40; root.paddingBottom = 48; root.itemSpacing = 24; root.fills = solid(C.white);
root.x = 7200; root.y = 0;

// ---- title
const tb = col(8);
tb.appendChild(text('Evaluation protocol and main results', 40, 'Bold', C.ink));
tb.appendChild(text('Development OOF benchmark on the 91 base peptides, not external validation', 26, 'Regular', C.muted));
root.appendChild(tb);

// ---- panel 1: protocol (cluster-grouped folds + decision rule)
const p1 = panel(1472); root.appendChild(p1); p1.layoutSizingHorizontal = 'FILL'; p1.name = 'Panel 1 protocol';
p1.appendChild(header(1, 'Cluster-grouped cross-validation, decided in advance'));
const body = row(24, 'MIN'); p1.appendChild(body);

const left = col(10); body.appendChild(left);
const FOLDS = [[C.blue, C.white], [C.sky, C.ink], [C.green, C.ink], [C.orange, C.ink], [C.pink, C.ink]];
const TEST = [17, 17, 18, 19, 18], NBASE = 89, NEXTRA = 83, PX = 800 / (NBASE + NEXTRA); // segment width is proportional to cluster count
FOLDS.forEach(([fc, tc], i) => {
  const r = row(8); left.appendChild(r);
  const lab = text('Fold ' + (i + 1), 24, 'Medium', C.ink, 92); r.appendChild(lab);
  const bar = row(0); r.appendChild(bar); bar.name = 'bar fold ' + (i + 1);
  bar.appendChild(seg(Math.round(TEST[i] * PX), fc, String(TEST[i]), tc));
  bar.appendChild(seg(Math.round((NBASE - TEST[i]) * PX), C.gray, String(NBASE - TEST[i]), C.ink));
  bar.appendChild(seg(Math.round(NEXTRA * PX), C.tan, String(NEXTRA), C.ink, C.line, true));
});
const leg = col(8); left.appendChild(leg);
[[C.blue, null, false, 'Outer-test clusters: base peptides only'], [C.gray, null, false, 'Outer-train clusters: base peptides'],
 [C.tan, C.line, true, 'Outer-train only: 83 extra clusters (PSI of wild type 3.0 to 4.0)']].forEach(([f, s, d, t]) => {
  const r = row(12); r.appendChild(swatch(f, s, d)); r.appendChild(text(t, 24, 'Regular', C.ink)); leg.appendChild(r);
});
left.appendChild(text('Segment width is proportional to the number of clusters; numbers are cluster counts.', 24, 'Regular', C.muted, 900));

const rule = col(14); body.appendChild(rule); rule.name = 'Decision rule';
rule.paddingLeft = 20; rule.paddingRight = 20; rule.paddingTop = 18; rule.paddingBottom = 18;
rule.fills = solid(C.white); rule.strokes = solid(C.panelStroke); rule.strokeWeight = 2; rule.cornerRadius = 12; rule.resize(480, 100);
rule.primaryAxisSizingMode = 'AUTO'; rule.counterAxisSizingMode = 'FIXED';
rule.appendChild(text('Pre-registered rule', 26, 'Semi Bold', C.ink));
[['shield-check', 'The outer-test is always the 91 base peptides'], ['dna', 'Folds are grouped by protein cluster'],
 ['sigma', 'Seeds 17, 29, 43; 5,000 cluster-bootstrap resamples'], ['circle-check', 'Accept a gain only if the paired 95% CI is above 0 and all 3 seeds are positive']].forEach(([ic, t]) => {
  const r = row(12, 'MIN'); r.appendChild(icon(ic, C.blue, 36)); const tx = text(t, 24, 'Regular', C.ink, 380); r.appendChild(tx); rule.appendChild(r);
});

// ---- panel 2: three chart cards
const cards = row(16, 'MIN'); root.appendChild(cards); cards.layoutSizingHorizontal = 'FILL'; cards.name = 'Main results';
function card(title, lines, hash) {
  const c = figma.createAutoLayout('VERTICAL'); c.resize(480, 100); c.primaryAxisSizingMode = 'AUTO'; c.counterAxisSizingMode = 'FIXED'; c.itemSpacing = 0;
  c.fills = solid(C.panel); c.strokes = solid(C.panelStroke); c.strokeWeight = 2; c.cornerRadius = 16; c.clipsContent = true;
  const hd = col(6); hd.paddingLeft = hd.paddingRight = 16; hd.paddingTop = 16; hd.paddingBottom = 12; c.appendChild(hd);
  hd.appendChild(text(title, 28, 'Semi Bold', C.ink));
  hd.appendChild(text(lines, 24, 'Regular', C.muted, 448));
  c.appendChild(img(hash, 480, 350)); return c;
}
cards.appendChild(card('Learning curve', 'With extra data (threshold 4.0): ridge +0.013 [+0.006, +0.019]; gated net +0.014 [+0.006, +0.022]', HASH.lc));
cards.appendChild(card('Threshold sensitivity', 'AUROC gain over threshold 3.0; every CI is above 0. The main value 4.0 was fixed first.', HASH.th));
cards.appendChild(card('Calibration', 'Brier 0.127 raw to 0.093 with Platt; ECE 0.144 to 0.016 on 47,847 test cells', HASH.rel));
cards.children.forEach((c) => { c.layoutAlign = 'STRETCH'; });

// ---- panel 3: negative results
const p3 = panel(1472); root.appendChild(p3); p3.layoutSizingHorizontal = 'FILL'; p3.name = 'Panel 3 negative results';
p3.appendChild(header(2, 'Designs that did not beat their reference'));
p3.appendChild(img(HASH.fo, 1424, 305));
const lg = row(32); p3.appendChild(lg);
const l1 = row(10); const dot = figma.createEllipse(); dot.resize(22, 22); dot.fills = solid(C.verm); l1.appendChild(dot); l1.appendChild(text('CI entirely below 0: worse than the reference', 24, 'Regular', C.ink)); lg.appendChild(l1);
const l2 = row(10); const sq = figma.createRectangle(); sq.resize(22, 22); sq.fills = solid(C.orange); sq.strokes = solid(C.ink); sq.strokeWeight = 2; l2.appendChild(sq); l2.appendChild(text('CI includes 0: no evidence of a gain', 24, 'Regular', C.ink)); lg.appendChild(l2);
p3.appendChild(text('None of the six designs passed the pre-registered rule, so the reported model stays ridge.', 24, 'Semi Bold', C.ink, 1424));

// ---- footer
root.appendChild(text('Macro AUROC per peptide, 91 base peptides (89 clusters, 47,847 cells), three seeds pooled. Sources: research/learning-curve-2026-10-22, g2-saturation, g2-extension, calibration-p6, pretrain-p3 (results.json).', 24, 'Regular', C.muted, 1472));

for (const id of ['3:470', '3:471', '3:472', '3:473']) { const n = await figma.getNodeByIdAsync(id); if (n) n.remove(); }
return { rootId: root.id, w: root.width, h: root.height, cardH: cards.height, p1H: p1.height, p3H: p3.height };
