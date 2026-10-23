// Fig 3.7 "From a GPS experiment to a calibrated prediction": composition script for `use_figma` (Figma Design file).
// STATUS (23/10/2026, new Figma account): run into file i3WSCDZNccWVUIGDvowiQU at x=3600. (Earlier note: written and NOT yet executed.) The Figma MCP call limit of the Starter plan was reached
// (error: "You've reached the Figma MCP tool call limit on the Starter plan") before this call could run.
// Empty target file already created: https://www.figma.com/design/NQRHjRziv78u033JVqPfgk  (file key NQRHjRziv78u033JVqPfgk)
//
// To finish when calls are available again:
//   1. run this script with use_figma (fileKey above, skillNames "figma-use,figma-generate-design"); it returns the ids of the
//      four image placeholders (imgBins, imgHeatMeasured, imgHeatPredicted, imgReliability);
//   2. add the scikit-learn logo (simple-icons slug `scikitlearn`, fill #F7931E, 44 px) to the headers of panels 4 and 5
//      with createNodeFromSvg (omitted here because its SVG path is 4.9 kB; fetch it from
//      https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/scikitlearn.svg);
//   3. upload the four PNGs from src/viz/inputs/ (v2-bins.png, v2-heat-measured.png, v2-heat-predicted.png, v2-reliability.png)
//      with upload_assets (count 4, nodeIds = the placeholder ids, scaleMode FILL) and POST the bytes;
//   4. screenshot the frame, check text >= 24 px and no clipping, export at scale 2 to report/assets/diagrams/fig-3-7-method-overview.png.
// Charts: src/viz/method_overview.py (data from src/viz/method_data.py). All numbers on the figure come from
// src/viz/inputs/v2-summary.json and research/calibration-p6-2026-10-22/results.json.

const A = {
  svg: {
    numpy: '<svg width="44" height="44" fill="#013243" role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M10.315 4.876L6.3048 2.8517l-4.401 2.1965 4.1186 2.0683zm1.8381.9277l4.2045 2.1223-4.3622 2.1906-4.125-2.0718zm5.6153-2.9213l4.3193 2.1658-3.863 1.9402-4.2131-2.1252zm-1.859-.9329L12.021 0 8.1742 1.9193l4.0068 2.0208zm-3.0401 16.7443V24l4.7107-2.3507-.0053-5.3085zm4.7037-4.2057l-.0052-5.2528-4.6985 2.3356v5.2546zm5.6553-.9845v5.327l-4.0178 2.0052-.0029-5.3028zm0-1.8626V6.4214l-4.0253 2.001.0034 5.2633zM11.2062 11.571L8.0333 9.9756v6.895s-3.8804-8.2564-4.2399-8.998c-.0463-.0957-.2371-.2007-.2858-.2262C2.8118 7.2812.773 6.2485.773 6.2485V18.43l2.8204 1.5076v-6.3674s3.8392 7.3775 3.878 7.458c.0389.0807.4245.8582.8362 1.1314.5485.363 2.8992 1.7766 2.8992 1.7766z"/></svg>',
    sklearn: "<svg width=\"44\" height=\"44\" fill=\"#F7931E\" role=\"img\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M15.601 5.53c-1.91.035-3.981.91-5.63 2.56-2.93 2.93-2.083 8.53-1.088 9.525.805.804 6.595 1.843 9.526-1.088a9.74 9.74 0 0 0 .584-.643c.043-.292.205-.66.489-1.106a1.848 1.848 0 0 1-.537.176c-.144.265-.37.55-.676.855-.354.335-.607.554-.76.656a.795.795 0 0 1-.437.152c-.35 0-.514-.308-.494-.924-.22.316-.425.549-.612.7a.914.914 0 0 1-.578.224c-.194 0-.36-.09-.496-.273a1.03 1.03 0 0 1-.193-.507 4.016 4.016 0 0 1-.726.583c-.224.132-.47.197-.74.197-.3 0-.543-.096-.727-.288a.978.978 0 0 1-.257-.524v.004c-.3.276-.564.48-.79.611a1.295 1.295 0 0 1-.649.197.693.693 0 0 1-.571-.275c-.145-.183-.218-.43-.218-.739 0-.464.101-1.02.302-1.67.201-.65.445-1.25.733-1.797l.842-.312a.21.21 0 0 1 .06-.013c.063 0 .116.047.157.14.04.095.061.221.061.38 0 .451-.104.888-.312 1.31-.207.422-.532.873-.974 1.352-.018.23-.027.388-.027.474 0 .193.036.345.106.458.071.113.165.169.282.169a.71.71 0 0 0 .382-.13c.132-.084.333-.26.602-.523.028-.418.187-.798.482-1.142.324-.38.685-.569 1.08-.569.206 0 .37.054.494.16a.524.524 0 0 1 .186.417c0 .458-.486.829-1.459 1.114.088.43.32.646.693.646a.807.807 0 0 0 .417-.117c.129-.076.321-.243.575-.497.032-.252.118-.495.259-.728.182-.3.416-.544.701-.73.285-.185.537-.278.756-.278.276 0 .47.127.58.381l.677-.374h.186l-.292.971c-.15.488-.226.823-.226 1.004 0 .19.067.285.202.285.086 0 .181-.045.285-.137.104-.092.25-.232.437-.42v.001c.143-.155.274-.32.392-.494-.19-.084-.285-.21-.285-.375 0-.17.058-.352.174-.545.116-.194.275-.29.479-.29.172 0 .258.088.258.265 0 .139-.05.338-.149.596.367-.04.687-.32.961-.842l.228-.01c1.059-2.438.828-5.075-.83-6.732-1.019-1.02-2.408-1.5-3.895-1.471zm4.725 8.203a8.938 8.938 0 0 1-1.333 2.151 1.09 1.09 0 0 0-.012.147c0 .168.047.309.14.423.092.113.206.17.34.17.296 0 .714-.264 1.254-.787-.001.04-.003.08-.003.121 0 .146.012.368.036.666l.733-.172c0-.2.003-.357.01-.474.01-.157.033-.33.066-.517.02-.11.07-.216.152-.315l.186-.216a5.276 5.276 0 0 1 .378-.397c.062-.055.116-.099.162-.13a.26.26 0 0 1 .123-.046c.055 0 .083.035.083.106 0 .07-.052.236-.156.497-.194.486-.292.848-.292 1.084 0 .175.046.314.136.418a.45.45 0 0 0 .358.155c.365 0 .803-.269 1.313-.808v-.381c-.361.426-.623.64-.784.64-.109 0-.163-.067-.163-.2 0-.1.065-.316.195-.65.19-.486.285-.836.285-1.048a.464.464 0 0 0-.112-.319.36.36 0 0 0-.282-.127c-.165 0-.354.077-.567.233-.213.156-.5.436-.863.84.053-.262.165-.622.335-1.08l-.809.156a6.54 6.54 0 0 0-.399 1.074c-.04.156-.07.316-.092.48a7.447 7.447 0 0 1-.49.45.38.38 0 0 1-.229.08.208.208 0 0 1-.174-.082.352.352 0 0 1-.064-.222c0-.1.019-.214.056-.343.038-.13.12-.373.249-.731l.308-.849zm-17.21-2.927c-.863-.016-1.67.263-2.261.854-1.352 1.352-1.07 3.827.631 5.527 1.7 1.701 4.95 1.21 5.527.632.467-.466 1.07-3.827-.631-5.527-.957-.957-2.158-1.465-3.267-1.486zm12.285.358h.166v.21H15.4zm.427 0h.166v.865l.46-.455h.195l-.364.362.428.684h-.198l-.357-.575-.164.166v.41h-.166zm1.016 0h.166v.21h-.166zm.481.122h.166v.288h.172v.135h-.172v.717c0 .037.006.062.02.075.012.013.037.02.074.02a.23.23 0 0 0 .078-.01v.141a.802.802 0 0 1-.136.014.23.23 0 0 1-.15-.043.15.15 0 0 1-.052-.123v-.79h-.141v-.136h.141zm-3.562.258c.081 0 .15.012.207.038.057.024.1.061.13.11s.045.106.045.173h-.176c-.006-.111-.075-.167-.208-.167a.285.285 0 0 0-.164.041.134.134 0 0 0-.06.117c0 .035.015.065.045.088.03.024.08.044.15.06l.16.039a.47.47 0 0 1 .224.105c.047.046.07.108.07.186a.3.3 0 0 1-.052.175.327.327 0 0 1-.152.116.585.585 0 0 1-.226.041c-.136 0-.24-.03-.309-.088-.069-.059-.105-.149-.109-.269h.176c.004.037.01.065.017.084a.166.166 0 0 0 .034.054c.044.043.112.065.204.065a.31.31 0 0 0 .177-.045.139.139 0 0 0 .067-.119.116.116 0 0 0-.038-.09.287.287 0 0 0-.124-.055l-.156-.038a1.248 1.248 0 0 1-.159-.05.359.359 0 0 1-.098-.061.22.22 0 0 1-.058-.083.32.32 0 0 1-.016-.108c0-.096.036-.174.109-.232a.45.45 0 0 1 .29-.087zm1.035 0a.46.46 0 0 1 .202.043.351.351 0 0 1 .187.212.577.577 0 0 1 .023.126h-.168a.256.256 0 0 0-.078-.168.242.242 0 0 0-.17-.06.248.248 0 0 0-.155.05.306.306 0 0 0-.1.144.662.662 0 0 0-.034.224.58.58 0 0 0 .035.214.299.299 0 0 0 .101.135.261.261 0 0 0 .157.048c.142 0 .227-.084.256-.252h.167a.519.519 0 0 1-.065.22.35.35 0 0 1-.146.138.464.464 0 0 1-.216.048.448.448 0 0 1-.246-.066.441.441 0 0 1-.161-.192.703.703 0 0 1-.057-.293c0-.085.01-.163.032-.233a.522.522 0 0 1 .095-.182.403.403 0 0 1 .15-.117.453.453 0 0 1 .191-.04zm.603.03h.166v1.046H15.4zm1.443 0h.166v1.046h-.166zm-5.05.618c-.08 0-.2.204-.356.611-.155.407-.308.977-.459 1.71.281-.312.509-.662.683-1.05.175-.387.262-.72.262-.999a.455.455 0 0 0-.036-.197c-.025-.05-.056-.075-.093-.075zm4.662 1.797c-.221 0-.431.188-.629.563-.197.376-.296.722-.296 1.038 0 .12.029.216.088.29a.273.273 0 0 0 .223.111c.221 0 .43-.188.625-.565.196-.377.294-.725.294-1.043a.457.457 0 0 0-.083-.29.269.269 0 0 0-.222-.104zm-2.848.007c-.146 0-.285.11-.417.333-.133.222-.2.51-.2.866.566-.159.849-.452.849-.881 0-.212-.077-.318-.232-.318Z\"/></svg>",
    arrow: '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#4A5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
  },
  // real tile composition of the example peptide (A..Y order), computed from its 28-mer
  comp: [0.10714285714285714, 0.03571428571428571, 0.10714285714285714, 0.07142857142857142, 0.10714285714285714, 0.03571428571428571, 0.0, 0.07142857142857142, 0.07142857142857142, 0.10714285714285714, 0.0, 0.0, 0.03571428571428571, 0.03571428571428571, 0.03571428571428571, 0.10714285714285714, 0.0, 0.0, 0.03571428571428571, 0.03571428571428571],
  seq: 'EDASAFPGKRALISFLSWFDYCDQLIKE',
};

const C = { INK: '#1E1E1E', MUTED: '#4A5563', LINE: '#7A8594', PANEL: '#F5F7FA', PSTROKE: '#D5DBE3', BLUE: '#0072B2', BLUEBG: '#E1EFF8',
  SKY: '#56B4E9', ORANGE: '#E69F00', ORANGEBG: '#FBEFD0', VERM: '#D55E00', VERMBG: '#F8E0D0', GREEN: '#009E73', GREENBG: '#D5EFE7',
  PURPLE: '#CC79A7', PURPLEBG: '#F4E4EC', WHITE: '#FFFFFF' };
const rgb = (hex) => { const n = parseInt(hex.slice(1), 16); return { r: ((n >> 16) & 255) / 255, g: ((n >> 8) & 255) / 255, b: (n & 255) / 255 }; };
const solid = (hex) => [{ type: 'SOLID', color: rgb(hex) }];

for (const style of ['Regular', 'Medium', 'Semi Bold', 'Bold']) await figma.loadFontAsync({ family: 'Inter', style });

function txt(parent, s, o = {}) {
  const { size = 26, style = 'Regular', color = C.INK, fill = false, width = null, align = 'LEFT', name = null } = o;
  const t = figma.createText();
  t.fontName = { family: 'Inter', style }; t.characters = s; t.fontSize = size; t.fills = solid(color); t.textAlignHorizontal = align;
  if (name) t.name = name;
  parent.appendChild(t);
  if (width) { t.textAutoResize = 'HEIGHT'; t.resize(width, t.height); }
  if (fill) { t.textAutoResize = 'HEIGHT'; t.layoutSizingHorizontal = 'FILL'; }
  return t;
}
function box(name, o = {}) {
  const { dir = 'VERTICAL', gap = 0, padX = 0, padY = 0, fill = null, stroke = null, radius = 0, w = null, h = null, main = 'MIN', cross = 'MIN' } = o;
  const f = figma.createAutoLayout(dir);
  f.name = name; f.itemSpacing = gap; f.paddingLeft = padX; f.paddingRight = padX; f.paddingTop = padY; f.paddingBottom = padY;
  f.fills = fill ? solid(fill) : [];
  if (stroke) { f.strokes = solid(stroke); f.strokeWeight = 2; }
  f.cornerRadius = radius; f.primaryAxisAlignItems = main; f.counterAxisAlignItems = cross;
  if (w || h) { f.resize(w || f.width, h || f.height); if (w) f.layoutSizingHorizontal = 'FIXED'; if (h) f.layoutSizingVertical = 'FIXED'; }
  return f;
}
function add(parent, child, o = {}) { parent.appendChild(child); if (o.fillW) child.layoutSizingHorizontal = 'FILL'; if (o.fillH) child.layoutSizingVertical = 'FILL'; return child; }
function icon(parent, svg, name) { const n = figma.createNodeFromSvg(svg); n.name = name; parent.appendChild(n); return n; }
function badge(parent, n) {
  const b = box('Step ' + n, { dir: 'HORIZONTAL', fill: C.BLUE, radius: 22, w: 44, h: 44, main: 'CENTER', cross: 'CENTER' });
  parent.appendChild(b); txt(b, String(n), { size: 26, style: 'Semi Bold', color: C.WHITE }); return b;
}
function panel(parent, n, title, width) {
  const p = box('Panel ' + n, { gap: 14, padX: 20, padY: 20, fill: C.PANEL, stroke: C.PSTROKE, radius: 16, w: width });
  p.layoutSizingVertical = 'HUG'; parent.appendChild(p);
  const head = box('Header', { dir: 'HORIZONTAL', gap: 12, cross: 'CENTER' }); add(p, head, { fillW: true });
  badge(head, n); const tt = txt(head, title, { size: 30, style: 'Semi Bold', fill: true });
  return { p, head, tt };
}
function strip(parent, name, n, cw, ch, gap, baseHex, hiIdx, hiHex) {
  const f = figma.createFrame(); f.name = name; f.fills = []; f.clipsContent = false; f.resize(n * cw + (n - 1) * gap, ch); parent.appendChild(f);
  for (let i = 0; i < n; i++) { const r = figma.createRectangle(); r.resize(cw, ch); r.x = i * (cw + gap); r.y = 0; r.cornerRadius = 3; r.fills = solid(i === hiIdx ? hiHex : baseHex); f.appendChild(r); }
  return f;
}
function placeholder(parent, name, w, h) { const r = figma.createRectangle(); r.name = name; r.resize(w, h); r.fills = solid(C.WHITE); parent.appendChild(r); return r; }

const AAS = 'ACDEFGHIKLMNPQRSTVWY';
const SEQ = A.seq; const POS = 15; const MUT = 'P';
const created = {};

// ---------- root ----------
const root = box('V2 Method overview', { gap: 24, padX: 40, padY: 40, fill: C.WHITE, w: 1600 });
root.layoutSizingVertical = 'HUG'; root.x = 3600; root.y = 0;
const titleBlock = box('Title', { gap: 6 }); add(root, titleBlock, { fillW: true });
txt(titleBlock, 'From a GPS experiment to a calibrated prediction', { size: 40, style: 'Bold', fill: true });
txt(titleBlock, 'Example peptide Q5W0V3_FAM160B1_16 (positions 1–28) · data: Zhang et al. 2023 (CC BY 4.0) · same colour scale in 2 and 4', { size: 24, color: C.MUTED, fill: true });
const row1 = box('Row 1', { dir: 'HORIZONTAL', gap: 28 }); add(root, row1, { fillW: true });
const row2 = box('Row 2', { dir: 'HORIZONTAL', gap: 28 }); add(root, row2, { fillW: true });
const PW = 488;

// ---------- panel 1: GPS assay ----------
{
  const { p } = panel(row1, 1, 'GPS assay → PSI', PW);
  const sch = box('Assay schematic', { dir: 'HORIZONTAL', gap: 8, cross: 'CENTER' }); add(p, sch, { fillW: true });
  const colL = box('Reporters', { gap: 8 }); sch.appendChild(colL);
  const g1 = box('GFP-peptide row', { dir: 'HORIZONTAL', gap: 4 }); colL.appendChild(g1);
  const gfp = figma.createRectangle(); gfp.name = 'GFP'; gfp.resize(100, 28); gfp.cornerRadius = 6; gfp.fills = solid(C.GREEN); g1.appendChild(gfp);
  const pep = figma.createRectangle(); pep.name = '28-mer peptide'; pep.resize(44, 28); pep.cornerRadius = 6; pep.fills = solid(C.ORANGE); g1.appendChild(pep);
  txt(colL, 'GFP–peptide', { size: 24, color: C.INK });
  const ds = figma.createRectangle(); ds.name = 'DsRed'; ds.resize(148, 28); ds.cornerRadius = 6; ds.fills = solid(C.PURPLE); colL.appendChild(ds);
  txt(colL, 'DsRed', { size: 24, color: C.INK });
  icon(sch, A.svg.arrow, 'arrow');
  const colR = box('Bins', { gap: 8 }); sch.appendChild(colR);
  const bins = box('Six bins', { dir: 'HORIZONTAL', gap: 4 }); colR.appendChild(bins);
  const ramp = ['#E1EFF8', '#BCD9EC', '#8DBBDC', '#5A9BC9', '#2E7DB7', '#0072B2'];
  ramp.forEach((hex, i) => { const b = box('bin ' + (i + 1), { dir: 'HORIZONTAL', fill: hex, radius: 6, w: 36, h: 36, main: 'CENTER', cross: 'CENTER' }); bins.appendChild(b); txt(b, String(i + 1), { size: 24, style: 'Medium', color: i < 3 ? C.INK : C.WHITE }); });
  txt(colR, '6 bins by GFP/DsRed', { size: 24, color: C.INK });
  created.imgBins = placeholder(p, 'IMG bins (matplotlib)', 440, 350).id;
  txt(p, 'PSI = read-weighted mean bin (1–6)', { size: 24, style: 'Medium', fill: true });
  txt(p, 'ΔPSI = PSI(mutant) − PSI(WT)', { size: 24, style: 'Medium', fill: true });
  txt(p, 'silent = same residue, other codon: the WT reference. Bin shares of one replicate.', { size: 24, color: C.MUTED, fill: true });
}

// ---------- panel 2: measured matrix ----------
{
  const { p } = panel(row1, 2, 'Measured ΔPSI matrix', PW);
  created.imgHeatMeasured = placeholder(p, 'IMG heatmap measured (matplotlib)', 440, 416).id;
  txt(p, 'Rows: position 1–28. Columns: mutant residue. Grey: wild type. Mean of 2 replicates; orange = stabilising.', { size: 24, color: C.MUTED, fill: true });
}

// ---------- panel 3: features ----------
{
  const { p, head } = panel(row1, 3, 'Features: 180 numbers', PW);
  const lg = box('Logo NumPy', { dir: 'HORIZONTAL' }); head.appendChild(lg); icon(lg, A.svg.numpy, 'logo NumPy');
  txt(p, 'Window around F15, mutated to P', { size: 24, color: C.MUTED, fill: true });
  const win = box('Sequence window', { dir: 'HORIZONTAL', gap: 6 }); p.appendChild(win);
  const letters = SEQ.slice(POS - 4, POS + 3);
  [...letters].forEach((ch, i) => {
    const hi = i === 3;
    const c = box('res ' + (POS - 3 + i), { dir: 'HORIZONTAL', fill: hi ? C.VERMBG : C.WHITE, stroke: hi ? C.VERM : C.PSTROKE, radius: 8, w: 56, h: 56, main: 'CENTER', cross: 'CENTER' });
    win.appendChild(c); txt(c, ch, { size: 28, style: hi ? 'Bold' : 'Medium' });
  });
  const wtIdx = AAS.indexOf(SEQ[POS - 1]), mutIdx = AAS.indexOf(MUT);
  const blocks = box('Feature blocks', { gap: 8 }); add(p, blocks, { fillW: true });
  strip(blocks, 'wild-type one-hot', 20, 18, 22, 2, C.BLUEBG, wtIdx, C.SKY);
  txt(blocks, 'wild type F, one-hot · 20', { size: 24, color: C.INK });
  strip(blocks, 'mutant one-hot', 20, 18, 22, 2, C.VERMBG, mutIdx, C.VERM);
  txt(blocks, 'mutant P, one-hot · 20', { size: 24, color: C.INK });
  const comp = figma.createFrame(); comp.name = 'tile composition'; comp.fills = []; comp.clipsContent = false; comp.resize(398, 40); blocks.appendChild(comp);
  A.comp.forEach((v, i) => { const hgt = Math.max(2, Math.round(v / 0.108 * 38)); const r = figma.createRectangle(); r.resize(18, hgt); r.x = i * 20; r.y = 40 - hgt; r.cornerRadius = 2; r.fills = solid(v > 0 ? C.GREEN : C.GREENBG); comp.appendChild(r); });
  txt(blocks, 'tile composition · 20', { size: 24, color: C.INK });
  const ctx = figma.createFrame(); ctx.name = 'context one-hot'; ctx.fills = []; ctx.clipsContent = false; ctx.resize(398, 6 * 14 - 2); blocks.appendChild(ctx);
  const nb = [SEQ[POS - 4], SEQ[POS - 3], SEQ[POS - 2], SEQ[POS], SEQ[POS + 1], SEQ[POS + 2]];
  nb.forEach((ch, r) => { for (let i = 0; i < 20; i++) { const q = figma.createRectangle(); q.resize(18, 12); q.x = i * 20; q.y = r * 14; q.cornerRadius = 2; q.fills = solid(i === AAS.indexOf(ch) ? C.PURPLE : C.PURPLEBG); ctx.appendChild(q); } });
  txt(blocks, 'context ±3, one-hot · 6×20 = 120', { size: 24, color: C.INK });
}

// ---------- panel 4: predicted matrix ----------
{
  const { p, head } = panel(row2, 4, 'Ridge → predicted ΔPSI', PW);
  const lg = box('Logos', { dir: 'HORIZONTAL', gap: 8, cross: 'CENTER' }); head.appendChild(lg);
  created.logosPanel4 = lg.id;
  icon(lg, A.svg.numpy, 'logo NumPy');
  icon(lg, A.svg.sklearn, 'logo scikit-learn');
  created.imgHeatPredicted = placeholder(p, 'IMG heatmap predicted (matplotlib)', 440, 416).id;
  txt(p, 'Out-of-fold ridge score, mean of 3 seeds. This peptide: Spearman 0.44; median over the 91 peptides: 0.43.', { size: 24, color: C.MUTED, fill: true });
}

// ---------- panel 5: calibration ----------
{
  const { p, head } = panel(row2, 5, 'Platt calibration → P(ΔPSI ≥ 1.0)', 1520 - PW - 28);
  created.headerPanel5 = head.id;
  const lg5 = box('Logo scikit-learn', { dir: 'HORIZONTAL' }); head.appendChild(lg5); icon(lg5, A.svg.sklearn, 'logo scikit-learn');
  row2.layoutSizingVertical = 'HUG';
  p.layoutSizingVertical = 'FILL';
  const inner = box('Calibration body', { dir: 'HORIZONTAL', gap: 24, cross: 'CENTER' }); add(p, inner, { fillW: true });
  created.imgReliability = placeholder(inner, 'IMG reliability (matplotlib)', 440, 470).id;
  const card = box('Numbers', { gap: 14 }); add(inner, card, { fillW: true });
  const t1 = box('Brier', { gap: 4, padX: 18, padY: 14, fill: C.WHITE, stroke: C.PSTROKE, radius: 12 }); add(card, t1, { fillW: true });
  txt(t1, 'Brier score (lower is better)', { size: 24, color: C.MUTED, fill: true });
  const r1 = box('Brier values', { dir: 'HORIZONTAL', gap: 10, cross: 'CENTER' }); t1.appendChild(r1);
  txt(r1, '0.127', { size: 44, style: 'Bold', color: C.VERM });
  icon(r1, A.svg.arrow, 'arrow');
  txt(r1, '0.093', { size: 44, style: 'Bold', color: C.BLUE });
  txt(t1, 'raw score → after Platt', { size: 24, color: C.MUTED, fill: true });
  const t2 = box('Enrichment', { gap: 4, padX: 18, padY: 14, fill: C.WHITE, stroke: C.PSTROKE, radius: 12 }); add(card, t2, { fillW: true });
  txt(t2, 'Top 10% of cells per peptide', { size: 24, color: C.MUTED, fill: true });
  txt(t2, '4.0× more hits than random', { size: 34, style: 'Bold', color: C.GREEN, fill: true });
  txt(t2, '95% CI 3.7–4.3', { size: 24, color: C.MUTED, fill: true });
  const t3 = box('Event', { gap: 4, padX: 18, padY: 14, fill: C.WHITE, stroke: C.PSTROKE, radius: 12 }); add(card, t3, { fillW: true });
  txt(t3, 'Event predicted', { size: 24, color: C.MUTED, fill: true });
  txt(t3, 'ΔPSI ≥ 1.0', { size: 34, style: 'Bold', fill: true });
  txt(t3, '13.1% of cells in the test peptides', { size: 24, color: C.MUTED, fill: true });
  const warn = box('Evidence label', { gap: 0, padX: 18, padY: 12, fill: C.ORANGEBG, stroke: C.ORANGE, radius: 12 }); add(card, warn, { fillW: true });
  txt(warn, 'Development out-of-fold results, 91 peptides. Not external validation.', { size: 24, style: 'Medium', fill: true });
}

return { rootId: root.id, w: root.width, h: root.height, ...created };
