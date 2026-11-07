// V6 'The domain gate in practice' - composition script for the Figma MCP tool `use_figma` (Figma Design file).
// STATUS: written and NOT executed. The Figma MCP call limit of the Starter plan was reached before this call
// (error: "You've reached the Figma MCP tool call limit on the Starter plan"). Re-run after the limit resets.
// Prerequisites already done in file 0dSN14jEOK397MFUyExVGw (https://www.figma.com/design/0dSN14jEOK397MFUyExVGw):
// the four PNGs were uploaded with upload_assets and sit on the page as nodes
//   1:2 = inputs/v6-psi-hist.png, 1:3 = v6-card-in.png, 1:4 = v6-card-unknown.png, 1:5 = v6-card-out.png.
// Pass skillNames "figma-use,figma-generate-design". After it runs, add (second call) the leader arrows:
// vertical vectors from each histogram marker down to the top edge of cards 1 and 3, and outline rectangles
// around the status block of each card (coordinates in inputs/v6-data.json: marker_px_in_hist_png_2x,
// highlight_boxes_in_card_2x; histogram scale = 1424/2944, card scale = 464/2170). Then export the frame at 2x.
const hex = (s) => ({ r: parseInt(s.slice(1, 3), 16) / 255, g: parseInt(s.slice(3, 5), 16) / 255, b: parseInt(s.slice(5, 7), 16) / 255 });
const C = { ink: '#1E1E1E', muted: '#4A5563', line: '#7A8594', panel: '#F5F7FA', panelStroke: '#D5DBE3', blue: '#0072B2',
  green: '#009E73', greenBg: '#D5EFE7', orange: '#E69F00', orangeBg: '#FBEFD0', verm: '#D55E00', vermBg: '#F8E0D0', white: '#FFFFFF' };
const solid = (c) => [{ type: 'SOLID', color: hex(c) }];
await Promise.all(['Regular', 'Medium', 'Semi Bold', 'Bold'].map((s) => figma.loadFontAsync({ family: 'Inter', style: s })));

const ICONS = { // lucide-static@0.468.0 (ISC)
  'circle-check': '<circle cx="12" cy="12" r="10" /><path d="m9 12 2 2 4-4" />',
  'triangle-alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" /><path d="M12 9v4" /><path d="M12 17h.01" />',
  'shield-x': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" /><path d="m14.5 9.5-5 5" /><path d="m9.5 9.5 5 5" />',
  'info': '<circle cx="12" cy="12" r="10" /><path d="M12 16v-4" /><path d="M12 8h.01" />',
  'keyboard': '<path d="M10 8h.01" /><path d="M12 12h.01" /><path d="M14 8h.01" /><path d="M16 12h.01" /><path d="M18 8h.01" /><path d="M6 8h.01" /><path d="M7 16h10" /><path d="M8 12h.01" /><rect width="20" height="16" x="2" y="4" rx="2" />',
};
function icon(name, color, size) {
  const n = figma.createNodeFromSvg(`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICONS[name]}</svg>`);
  n.name = 'icon/' + name; n.resize(size, size); return n;
}
function text(str, size, style, color, opts = {}) {
  const t = figma.createText();
  t.fontName = { family: 'Inter', style }; t.characters = str; t.fontSize = size; t.fills = solid(color);
  if (opts.width) { t.resize(opts.width, 10); t.textAutoResize = 'HEIGHT'; }
  return t;
}
function hbox(gap, pad) { const f = figma.createAutoLayout('HORIZONTAL'); f.itemSpacing = gap; f.paddingLeft = f.paddingRight = pad[0]; f.paddingTop = f.paddingBottom = pad[1]; f.counterAxisAlignItems = 'CENTER'; f.fills = []; return f; }
function badge(n) {
  const f = figma.createAutoLayout('HORIZONTAL'); f.resize(44, 44); f.primaryAxisSizingMode = 'FIXED'; f.counterAxisSizingMode = 'FIXED';
  f.primaryAxisAlignItems = 'CENTER'; f.counterAxisAlignItems = 'CENTER'; f.cornerRadius = 22; f.fills = solid(C.blue); f.name = 'step ' + n;
  f.appendChild(text(String(n), 26, 'Bold', C.white)); return f;
}
function panel(w) {
  const p = figma.createAutoLayout('VERTICAL'); p.resize(w, 100); p.primaryAxisSizingMode = 'AUTO';
  p.paddingLeft = p.paddingRight = p.paddingTop = p.paddingBottom = 24; p.itemSpacing = 12;
  p.fills = solid(C.panel); p.strokes = solid(C.panelStroke); p.strokeWeight = 2; p.cornerRadius = 16; return p;
}
function pill(label, bg, stroke, iconName) {
  const f = hbox(10, [16, 8]); f.cornerRadius = 24; f.fills = solid(bg); f.strokes = solid(stroke); f.strokeWeight = 2;
  if (iconName) f.appendChild(icon(iconName, stroke, 28));
  f.appendChild(text(label, 24, 'Semi Bold', C.ink)); return f;
}

const root = figma.createFrame();
root.name = 'V6 The domain gate in practice'; root.resize(1600, 1700); root.x = 0; root.y = 0; root.fills = solid(C.white); root.clipsContent = true;
root.appendChild((() => { const t = text('The domain gate in practice', 40, 'Bold', C.ink); t.x = 64; t.y = 36; return t; })());
root.appendChild((() => { const t = text('Tier 1 reads the measured tile PSI of the GPS screen; a typed sequence has no stored tile to look up.', 26, 'Regular', C.muted, { width: 1472 }); t.x = 64; t.y = 98; return t; })());

// panel A: histogram
const pA = panel(1472); root.appendChild(pA); pA.x = 64; pA.y = 170; pA.name = 'Panel A histogram';
const hA = hbox(14, [0, 0]); pA.appendChild(hA); hA.appendChild(badge(1)); hA.appendChild(text('Measured tile PSI decides the domain', 30, 'Semi Bold', C.ink));
const note = text('Tile PSI comes from one replicate. On the 235 saturation peptides it reads about 0.88 below the intrinsic PSI(WT) that defines the training domain.', 24, 'Regular', C.muted, { width: 1424 });
pA.appendChild(note); note.layoutSizingHorizontal = 'FILL';
const hist = await figma.getNodeByIdAsync('1:2'); pA.appendChild(hist); hist.name = 'PSI histogram (real data)'; hist.resize(1424, Math.round(1424 * 800 / 2944));

// panel B: three real UI cards
const pB = panel(1472); root.appendChild(pB); pB.x = 64; pB.name = 'Panel B tool response';
const hB = hbox(14, [0, 0]); pB.appendChild(hB); hB.appendChild(badge(2)); hB.appendChild(text('Tool response', 30, 'Semi Bold', C.ink));
const row = figma.createAutoLayout('HORIZONTAL'); row.itemSpacing = 16; row.fills = []; row.name = 'cards'; pB.appendChild(row);
const CW = 464, CH = Math.round(CW * 1570 / 2170);
const specs = [
  { id: '1:3', label: 'measured_in_domain', bg: C.greenBg, st: C.green, ic: 'circle-check', cap: 'A6NMZ7 tile 28, PSI 1.88: scored, flagged as a training peptide', name: 'UI in domain' },
  { id: '1:4', label: 'unknown', bg: C.orangeBg, st: C.orange, ic: 'keyboard', cap: 'Typed 28-mer: scored with a warning, no tile PSI to look up', name: 'UI unknown' },
  { id: '1:5', label: 'measured_out_of_domain', bg: C.vermBg, st: C.verm, ic: 'shield-x', cap: 'A6NMZ7 tile 7, PSI 5.10: refused unless override_domain is set', name: 'UI out of domain' },
];
const imgs = [];
for (const s of specs) {
  const card = figma.createAutoLayout('VERTICAL'); card.itemSpacing = 12; card.fills = []; card.name = 'card ' + s.label; row.appendChild(card);
  card.appendChild(pill(s.label, s.bg, s.st, s.ic));
  const im = await figma.getNodeByIdAsync(s.id); card.appendChild(im); im.name = s.name + ' (real screenshot)';
  im.resize(CW, CH); im.cornerRadius = 8; im.strokes = solid(C.panelStroke); im.strokeWeight = 2; imgs.push(im);
  const cap = text(s.cap, 24, 'Regular', C.muted, { width: CW }); card.appendChild(cap); cap.layoutSizingHorizontal = 'FILL';
}
pB.y = pA.y + pA.height + 28;

// panel C: behaviours + tier-2 note
const pC = panel(1472); root.appendChild(pC); pC.x = 64; pC.name = 'Panel C behaviours';
const hC = hbox(14, [0, 0]); pC.appendChild(hC); hC.appendChild(badge(3)); hC.appendChild(text('Three behaviours', 30, 'Semi Bold', C.ink));
const brow = figma.createAutoLayout('HORIZONTAL'); brow.itemSpacing = 16; brow.fills = []; pC.appendChild(brow);
const beh = [
  { ic: 'circle-check', t: 'Score', d: 'Measured PSI at most 4.0', bg: C.greenBg, st: C.green },
  { ic: 'triangle-alert', t: 'Score with warning', d: 'Unknown, unreliable or predicted domain', bg: C.orangeBg, st: C.orange },
  { ic: 'shield-x', t: 'Refused unless override', d: 'Out of domain: 422, override adds a warning', bg: C.vermBg, st: C.verm },
];
for (const b of beh) {
  const tile = hbox(16, [20, 16]); tile.fills = solid(b.bg); tile.strokes = solid(b.st); tile.strokeWeight = 2; tile.cornerRadius = 16; tile.resize(CW, 100);
  tile.primaryAxisSizingMode = 'FIXED'; tile.counterAxisSizingMode = 'AUTO'; brow.appendChild(tile);
  tile.appendChild(icon(b.ic, b.st, 56));
  const col = figma.createAutoLayout('VERTICAL'); col.itemSpacing = 4; col.fills = []; tile.appendChild(col); col.layoutGrow = 1;
  col.appendChild(text(b.t, 26, 'Semi Bold', C.ink, { width: 320 })); col.appendChild(text(b.d, 24, 'Regular', C.muted, { width: 320 }));
  for (const c of col.children) c.layoutSizingHorizontal = 'FILL';
}
const nrow = hbox(12, [0, 0]); pC.appendChild(nrow); nrow.counterAxisAlignItems = 'MIN';
nrow.appendChild(icon('info', C.muted, 32));
nrow.appendChild(text('Tier 2 gate model (R3) is not yet trained: typed sequences and tiles outside the screen stay unknown. Development OOF benchmark, not external validation.', 24, 'Regular', C.muted, { width: 1380 }));
pC.y = pB.y + pB.height + 28;
root.resize(1600, Math.round(pC.y + pC.height + 48));

return { rootId: root.id, panelA: [pA.y, pA.height], panelB: [pB.y, pB.height], panelC: [pC.y, pC.height], rootH: root.height,
  histBox: hist.absoluteBoundingBox, imgBoxes: imgs.map((i) => i.absoluteBoundingBox) };
