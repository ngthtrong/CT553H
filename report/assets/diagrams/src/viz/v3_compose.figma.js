// V3 (fig-3-8-data-processing): full composition for the Figma MCP tool `use_figma` (Figma Design file).
// File i3WSCDZNccWVUIGDvowiQU. Prerequisite: inputs/v3-psiwt-hist.png uploaded with upload_assets (node 3:53 below).
// Numbers come from inputs/v3-data.json (asserted against the result JSON files by data_processing.py).
// Frame is placed at x=5400, y=0 (V6 at 0, V1 at 1800, V2 at 3600). skillNames: figma-use,figma-generate-design
const HIST_NODE = '3:53';
const hex = (s) => ({ r: parseInt(s.slice(1, 3), 16) / 255, g: parseInt(s.slice(3, 5), 16) / 255, b: parseInt(s.slice(5, 7), 16) / 255 });
const C = { ink: '#1E1E1E', muted: '#4A5563', line: '#7A8594', panel: '#F5F7FA', panelStroke: '#D5DBE3', blue: '#0072B2', blueBg: '#E1EFF8',
  orange: '#E69F00', orangeBg: '#FBEFD0', verm: '#D55E00', green: '#009E73', greenBg: '#D5EFE7', pink: '#CC79A7', gray: '#9AA5B1', grayBg: '#E6EAF0', white: '#FFFFFF' };
const solid = (c) => [{ type: 'SOLID', color: hex(c) }];
await Promise.all(['Regular', 'Medium', 'Semi Bold', 'Bold'].map((s) => figma.loadFontAsync({ family: 'Inter', style: s })));

// ---- icons: lucide-static@0.468.0 (ISC), simple-icons@13.21.0 (CC0) ----
const LU = {
  database: '<ellipse cx="12" cy="5" rx="9" ry="3" /><path d="M3 5V19A9 3 0 0 0 21 19V5" /><path d="M3 12A9 3 0 0 0 21 12" />',
  'file-text': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" /><path d="M14 2v4a2 2 0 0 0 2 2h4" /><path d="M10 9H8" /><path d="M16 13H8" /><path d="M16 17H8" />',
  'arrow-right': '<path d="M5 12h14" /><path d="m12 5 7 7-7 7" />',
  'arrow-down': '<path d="M12 5v14" /><path d="m19 12-7 7-7-7" />',
};
const SI = {
  github: ['#181717', 'M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12'],
  mendeley: ['#9D1620', 'M12.0037 9.1684h.019a2.355 2.355 0 011.5038 4.1655 1.8076 1.8076 0 01-.8561.452 2.348 2.348 0 01-.6487.0923h-.019c-.2246 0-.4421-.033-.6487-.0922a1.8126 1.8126 0 01-.8561-.4521 2.346 2.346 0 01-.8511-1.8106 2.358 2.358 0 012.3569-2.355m-9.9731 9.474c1.2652.1583 2.388-.762 2.5073-2.0573a2.4442 2.4442 0 00-.2136-1.236c-1.7724-3.8889 6.9726-3.978 5.4949-.3078l-.01.016c-.6988 1.1178-.3198 2.5695.841 3.2402.4272.2486.9003.3508 1.3625.3308.4622.02.9354-.0822 1.3624-.3308 1.161-.6717 1.54-2.1224.8412-3.2402l-.01-.016c-1.4778-3.6703 7.2682-3.581 5.4938.3077a2.4462 2.4462 0 00-.2126 1.2361c.1203 1.2953 1.2422 2.2156 2.5083 2.0572a2.345 2.345 0 001.4246-.7368s.5885-.4883.5795-1.7334c-.008-1.0156-.5795-1.578-.5795-1.578a2.2116 2.2116 0 00-1.8145-.6456c-1.6231-.036-1.8637-1.3073-1.4056-3.7033.1685-.4251.2416-.8802.2266-1.3354a3.4166 3.4166 0 00-2.1304-3.2953c-.039-.017-.0782-.03-.1183-.0461a1.5138 1.5138 0 00-.1343-.0461 3.4156 3.4156 0 00-4.004 1.4526c-.8171.8973-1.187 1.4417-2.0272 1.4417-.799 0-1.211-.5444-2.0271-1.4417a3.4126 3.4126 0 00-4.1374-1.4075c-.0401.016-.0792.029-.1193.0461a3.4156 3.4156 0 00-2.1294 3.2953c-.016.4552.0582.9103.2256 1.3354.4581 2.397.2175 3.6672-1.4045 3.7033-.795-.0852-1.3885.2426-1.988.8431-.6016.5995-.5514 2.2056 0 2.9063.4.5103.9423.8632 1.598.9454'],
};
function luIcon(name, color, size) {
  const n = figma.createNodeFromSvg(`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${LU[name]}</svg>`);
  n.name = 'icon/' + name; n.resize(size, size); return n;
}
function siLogo(name, size) {
  const [col, d] = SI[name];
  const n = figma.createNodeFromSvg(`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="${col}" d="${d}"/></svg>`);
  n.name = 'logo/' + name; n.resize(size, size); return n;
}

// ---- layout helpers ----
function text(str, size, style, color) {
  const t = figma.createText();
  t.fontName = { family: 'Inter', style }; t.characters = str; t.fontSize = size; t.fills = solid(color);
  t.textAutoResize = 'HEIGHT'; return t;
}
function fillW(parent, node) { parent.appendChild(node); node.layoutSizingHorizontal = 'FILL'; return node; }
function box(dir, gap, pad) {
  const f = figma.createAutoLayout(dir); f.itemSpacing = gap;
  f.paddingLeft = f.paddingRight = pad[0]; f.paddingTop = f.paddingBottom = pad[1]; f.fills = []; return f;
}
function badge(n) {
  const f = figma.createAutoLayout('HORIZONTAL'); f.resize(44, 44); f.primaryAxisSizingMode = 'FIXED'; f.counterAxisSizingMode = 'FIXED';
  f.primaryAxisAlignItems = 'CENTER'; f.counterAxisAlignItems = 'CENTER'; f.cornerRadius = 22; f.fills = solid(C.blue); f.name = 'step ' + n;
  f.appendChild(text(String(n), 26, 'Bold', C.white)); f.children[0].textAutoResize = 'WIDTH_AND_HEIGHT'; return f;
}
function panel(name) {
  const p = figma.createAutoLayout('VERTICAL'); p.name = name;
  p.paddingLeft = p.paddingRight = p.paddingTop = p.paddingBottom = 24; p.itemSpacing = 14;
  p.fills = solid(C.panel); p.strokes = solid(C.panelStroke); p.strokeWeight = 2; p.cornerRadius = 16; return p;
}
function heading(n, str) {
  const h = box('HORIZONTAL', 14, [0, 0]); h.counterAxisAlignItems = 'CENTER'; h.appendChild(badge(n));
  const t = text(str, 30, 'Semi Bold', C.ink); t.textAutoResize = 'WIDTH_AND_HEIGHT'; h.appendChild(t); return h;
}
function pill(label, bg) {
  const f = box('HORIZONTAL', 0, [14, 6]); f.cornerRadius = 20; f.fills = solid(bg);
  const t = text(label, 24, 'Semi Bold', C.ink); t.textAutoResize = 'WIDTH_AND_HEIGHT'; f.appendChild(t); return f;
}
function sq(color, size, outline) {
  const r = figma.createRectangle(); r.resize(size, size); r.cornerRadius = size > 30 ? 8 : 6; r.fills = solid(color);
  if (outline) { r.strokes = solid(outline); r.strokeWeight = 2; } return r;
}
function legendItem(color, label, outline) {
  const f = box('HORIZONTAL', 12, [0, 0]); f.counterAxisAlignItems = 'CENTER';
  f.appendChild(sq(color, 28, outline)); const t = text(label, 24, 'Regular', C.ink); t.textAutoResize = 'WIDTH_AND_HEIGHT'; f.appendChild(t); return f;
}
function wrapRow(width, gap) {
  const f = figma.createAutoLayout('HORIZONTAL'); f.layoutWrap = 'WRAP'; f.itemSpacing = gap; f.counterAxisSpacing = gap;
  f.fills = []; f.primaryAxisSizingMode = 'FIXED'; f.counterAxisSizingMode = 'AUTO'; f.resize(width, 10); return f;
}
function arrowCell(name, w) {
  const f = figma.createAutoLayout('VERTICAL'); f.resize(w, 40); f.primaryAxisSizingMode = 'AUTO'; f.counterAxisSizingMode = 'FIXED';
  f.primaryAxisAlignItems = 'CENTER'; f.counterAxisAlignItems = 'CENTER'; f.fills = []; f.appendChild(luIcon(name, C.line, 32)); return f;
}
function blend(base, t) { const a = hex(base); return { r: 1 + (a.r - 1) * t, g: 1 + (a.g - 1) * t, b: 1 + (a.b - 1) * t }; }

// ---- root ----
const root = figma.createAutoLayout('VERTICAL');
root.name = 'V3 From raw screens to cluster-grouped training data';
root.resize(1600, 100); root.primaryAxisSizingMode = 'AUTO'; root.counterAxisSizingMode = 'FIXED';
root.paddingLeft = root.paddingRight = 48; root.paddingTop = 40; root.paddingBottom = 44; root.itemSpacing = 20;
root.fills = solid(C.white); root.x = 5400; root.y = 0;
const title = text('From raw screens to cluster-grouped training data', 40, 'Bold', C.ink); fillW(root, title);

// ---- panel 1: sources ----
const p1 = panel('Step 1 sources'); fillW(root, p1); p1.itemSpacing = 14;
p1.appendChild(heading(1, 'Public sources, versions pinned, licences recorded'));
const cards = box('HORIZONTAL', 16, [0, 0]); fillW(p1, cards);
const SRC = [
  ['Zhang 2023', 'Mendeley Data v2, scans and saturation', 'CC BY 4.0', C.greenBg, () => siLogo('mendeley', 40)],
  ['GEO', 'GSE240610, peptide library cross-check', 'Public data', C.grayBg, () => luIcon('database', C.muted, 40)],
  ['UniProt', 'Swiss-Prot 2026_03, human reviewed', 'CC BY 4.0', C.greenBg, () => luIcon('file-text', C.muted, 40)],
  ['Voutsinos 2026', 'GitHub repository at a pinned commit', 'MIT', C.greenBg, () => siLogo('github', 40)],
];
for (const [name, desc, lic, bg, logo] of SRC) {
  const c = figma.createAutoLayout('VERTICAL'); c.name = 'source ' + name; c.itemSpacing = 8;
  c.paddingLeft = c.paddingRight = 16; c.paddingTop = c.paddingBottom = 14; c.fills = solid(C.white); c.strokes = solid(C.panelStroke); c.strokeWeight = 2; c.cornerRadius = 12;
  const top = box('HORIZONTAL', 12, [0, 0]); top.counterAxisAlignItems = 'CENTER'; top.appendChild(logo());
  const nm = text(name, 26, 'Semi Bold', C.ink); nm.textAutoResize = 'WIDTH_AND_HEIGHT'; top.appendChild(nm); c.appendChild(top);
  fillW(c, text(desc, 24, 'Regular', C.muted)); c.appendChild(pill(lic, bg));
  cards.appendChild(c); c.layoutSizingHorizontal = 'FILL';
}
fillW(p1, text('Audited, not imported: Koren 2018, MetaDegron, Larsen 2025', 24, 'Regular', C.muted));

root.appendChild(arrowCell('arrow-down', 1504)).layoutSizingHorizontal = 'FILL';

// ---- row 2: panels 2 and 3 ----
const row2 = box('HORIZONTAL', 0, [0, 0]); fillW(root, row2); row2.counterAxisAlignItems = 'MIN';
const p2 = panel('Step 2 delta PSI'); p2.resize(732, 100); p2.layoutSizingHorizontal = 'FIXED'; p2.primaryAxisSizingMode = 'AUTO'; row2.appendChild(p2); p2.layoutAlign = 'STRETCH';
const mid2 = arrowCell('arrow-right', 40); mid2.layoutAlign = 'CENTER'; mid2.layoutSizingVertical = 'HUG'; row2.appendChild(mid2);
const p3 = panel('Step 3 filter'); p3.resize(732, 100); p3.layoutSizingHorizontal = 'FIXED'; row2.appendChild(p3); p3.layoutAlign = 'STRETCH';

p2.appendChild(heading(2, 'Per-cell ΔPSI from two replicates'));
fillW(p2, text('Example peptide Q99741_CDC6_1, excerpt: 4 of 529 cells', 24, 'Regular', C.muted));
const COLW = [172, 170, 170, 172];
const ROWS = [
  { cells: ['Cell', 'PSI rep. a', 'PSI rep. b', 'ΔPSI'], bg: C.grayBg, style: 'Semi Bold' },
  { cells: ['WT baseline', '2.65', '2.54', '0 (ref.)'], bg: C.blueBg, style: 'Medium' },
  { cells: ['F14A', '5.62', '5.47', '+2.95'], d: 2.95 }, { cells: ['P15D', '5.16', '5.34', '+2.66'], d: 2.66 },
  { cells: ['Q9A', '2.65', '2.83', '+0.15'], d: 0.15 }, { cells: ['K25M', '1.71', '1.78', '−0.85'], d: -0.85 },
];
const table = figma.createAutoLayout('VERTICAL'); table.itemSpacing = 0; table.fills = []; table.name = 'excerpt table';
p2.appendChild(table); table.layoutSizingHorizontal = 'FILL';
for (const r of ROWS) {
  const row = figma.createAutoLayout('HORIZONTAL'); row.itemSpacing = 0; row.fills = []; table.appendChild(row);
  r.cells.forEach((v, i) => {
    const cell = figma.createAutoLayout('HORIZONTAL'); cell.resize(COLW[i], 54); cell.primaryAxisSizingMode = 'FIXED'; cell.counterAxisSizingMode = 'FIXED';
    cell.paddingLeft = cell.paddingRight = 12; cell.counterAxisAlignItems = 'CENTER'; cell.strokes = solid(C.panelStroke); cell.strokeWeight = 1;
    let fill = r.bg || C.white, tc = C.ink, st = r.style || 'Regular';
    if (r.d !== undefined && i === 3) {
      const t = Math.min(Math.abs(r.d) / 3, 1); const base = r.d >= 0 ? C.verm : C.blue;
      cell.fills = [{ type: 'SOLID', color: blend(base, t) }]; st = 'Semi Bold'; if (t > 0.6) tc = C.white; fill = null;
    }
    if (fill) cell.fills = solid(fill);
    const tx = text(v, 26, st, tc); tx.textAutoResize = 'WIDTH_AND_HEIGHT'; cell.appendChild(tx); row.appendChild(cell);
  });
}
const note2 = figma.createAutoLayout('VERTICAL'); note2.itemSpacing = 6; note2.paddingLeft = note2.paddingRight = 16; note2.paddingTop = note2.paddingBottom = 12;
note2.fills = solid(C.blueBg); note2.cornerRadius = 12; p2.appendChild(note2); note2.layoutSizingHorizontal = 'FILL';
fillW(note2, text('WT baseline: median PSI of the synonymous cells of the peptide', 24, 'Regular', C.ink));
fillW(note2, text('ΔPSI: mean over the two replicates of PSI(mutant) − PSI(WT)', 24, 'Regular', C.ink));

p3.appendChild(heading(3, 'Keep degron-like peptides'));
fillW(p3, text('PSI of wild type: 235 of 248 peptides have a baseline', 24, 'Regular', C.muted));
const hist = await figma.getNodeByIdAsync(HIST_NODE);
p3.appendChild(hist); hist.name = 'Histogram PSI(WT), real data'; hist.resize(684, Math.round(684 * 680 / 1480)); hist.layoutSizingHorizontal = 'FILL'; hist.cornerRadius = 8;
const leg3 = box('VERTICAL', 10, [0, 0]); fillW(p3, leg3);
leg3.appendChild(legendItem(C.blue, '≤ 3.0: 91 base peptides (evaluation domain)'));
leg3.appendChild(legendItem(C.orange, '3.0 to 4.0: 85 extra peptides (outer-train only)'));
leg3.appendChild(legendItem(C.gray, '> 4.0: 59 peptides not used'));

root.appendChild(arrowCell('arrow-down', 1504)).layoutSizingHorizontal = 'FILL';

// ---- row 3: panels 4 and 5 ----
const row3 = box('HORIZONTAL', 0, [0, 0]); fillW(root, row3);
const p4 = panel('Step 4 clusters'); p4.resize(900, 100); p4.layoutSizingHorizontal = 'FIXED'; row3.appendChild(p4); p4.layoutAlign = 'STRETCH';
const mid3 = arrowCell('arrow-right', 40); mid3.layoutAlign = 'CENTER'; mid3.layoutSizingVertical = 'HUG'; row3.appendChild(mid3);
const p5 = panel('Step 5 outer folds'); p5.resize(564, 100); p5.layoutSizingHorizontal = 'FIXED'; row3.appendChild(p5); p5.layoutAlign = 'STRETCH';

const FOLD = [C.blue, C.orange, C.green, C.verm, C.pink]; const FN = [17, 17, 18, 19, 18];
p4.appendChild(heading(4, 'Cluster proteins by similarity'));
fillW(p4, text('MMseqs2, 30 % identity, 80 % coverage', 24, 'Regular', C.muted));
fillW(p4, text('89 base clusters (91 peptides), colored by outer test fold', 24, 'Semi Bold', C.ink));
const g1 = wrapRow(852, 8); p4.appendChild(g1); g1.layoutSizingHorizontal = 'FILL'; g1.name = '89 base clusters';
FN.forEach((n, f) => { for (let i = 0; i < n; i++) g1.appendChild(sq(FOLD[f], 28)); });
fillW(p4, text('83 new clusters (85 extra peptides): always outer-train', 24, 'Semi Bold', C.ink));
const g2 = wrapRow(852, 8); p4.appendChild(g2); g2.layoutSizingHorizontal = 'FILL'; g2.name = '83 new clusters';
for (let i = 0; i < 83; i++) g2.appendChild(sq(C.grayBg, 28, C.gray));
const leg4 = wrapRow(852, 8); leg4.itemSpacing = 22; p4.appendChild(leg4); leg4.layoutSizingHorizontal = 'FILL';
FN.forEach((n, f) => leg4.appendChild(legendItem(FOLD[f], `Fold ${f + 1} (${n})`)));

p5.appendChild(heading(5, 'Five outer folds'));
fillW(p5, text('One fold shown (fold 3 held out)', 24, 'Regular', C.muted));
fillW(p5, text('Outer-train', 26, 'Semi Bold', C.ink));
const BAR = 516, TOT = 154;
function bar(segs) {
  const b = figma.createAutoLayout('HORIZONTAL'); b.itemSpacing = 2; b.fills = [];
  for (const [col, n] of segs) { const r = figma.createRectangle(); r.resize(Math.round(BAR * n / TOT) - 2, 44); r.cornerRadius = 6; r.fills = solid(col); b.appendChild(r); }
  return b;
}
p5.appendChild(bar([[C.blue, 17], [C.orange, 17], [C.verm, 19], [C.pink, 18], [C.gray, 83]]));
fillW(p5, text('4 base folds + 83 extra clusters', 24, 'Regular', C.muted));
fillW(p5, text('Outer-test', 26, 'Semi Bold', C.ink));
p5.appendChild(bar([[C.green, 18]]));
fillW(p5, text('Held-out fold: 18 base clusters', 24, 'Regular', C.muted));
const note5 = figma.createAutoLayout('VERTICAL'); note5.paddingLeft = note5.paddingRight = 16; note5.paddingTop = note5.paddingBottom = 12;
note5.fills = solid(C.orangeBg); note5.cornerRadius = 12; p5.appendChild(note5); note5.layoutSizingHorizontal = 'FILL';
fillW(note5, text('Extra peptides sharing a cluster with the test fold leave the training set (fold 1: 531 cells, fold 4: 532 cells)', 24, 'Regular', C.ink));

// ---- evidence ----
const texts = root.findAllWithCriteria({ types: ['TEXT'] });
const minFont = Math.min(...texts.map((t) => t.fontSize));
return { rootId: root.id, w: root.width, h: root.height, minFontSize: minFont, textCount: texts.length, histH: hist.height, p2h: p2.height, p3h: p3.height, p4h: p4.height, p5h: p5.height };
