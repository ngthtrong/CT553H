// V1 "Technology stack and request flow": use_figma script (Figma Design file wng9Yyt2PtXDQ0l2deaLaq).
// NOT RUN: the Figma MCP Starter-plan tool-call limit was reached before this call. Run it with use_figma when calls are available.
// Prerequisite: the 17 prepared SVG logos were already uploaded to that file; they sit on the page as nodes with the ids used below
// (1:2 react, 1:4 typescript, 1:6 vite, 1:8 nginx, 1:10 fastapi, 1:12 python, 1:14 numpy, 1:16 postgresql, 1:18 sqlite,
//  1:20 docker, 1:22 openapi, 1:24 monitor, 1:28 network, 1:34 server, 1:39 database, 1:43 file-down, 1:48 shield-check).
// Afterwards: upload_assets with nodeIds=[<ph-status>,<ph-heatmap>] for src/viz/inputs/v1/ui-status.png and ui-heatmap-excerpt.png.
const hex = (s) => ({ r: parseInt(s.slice(1, 3), 16) / 255, g: parseInt(s.slice(3, 5), 16) / 255, b: parseInt(s.slice(5, 7), 16) / 255 });
const INK = '#1E1E1E', MUTED = '#4A5563', LINE = '#7A8594', PANEL = '#F5F7FA', PSTROKE = '#D5DBE3', BLUE = '#0072B2';
for (const st of ['Regular', 'Medium', 'Semi Bold', 'Bold']) await figma.loadFontAsync({ family: 'Inter', style: st });
const root = figma.createFrame();
root.name = 'V1 Technology stack and request flow';
root.resize(1600, 1580); root.x = 1000; root.y = 0;
root.fills = [{ type: 'SOLID', color: hex('#FFFFFF') }]; root.clipsContent = true;
function R(x, y, w, h, o = {}) {
  const r = figma.createRectangle(); root.appendChild(r); r.x = x; r.y = y; r.resize(w, h);
  r.fills = o.fill ? [{ type: 'SOLID', color: hex(o.fill) }] : [];
  if (o.stroke) { r.strokes = [{ type: 'SOLID', color: hex(o.stroke) }]; r.strokeWeight = o.sw || 2; if (o.dash) r.dashPattern = o.dash; }
  if (o.r) r.cornerRadius = o.r; if (o.name) r.name = o.name; return r;
}
function T(s, x, y, o = {}) {
  const t = figma.createText(); root.appendChild(t);
  t.fontName = { family: 'Inter', style: o.style || 'Regular' }; t.fontSize = o.size || 24; t.characters = s;
  t.fills = [{ type: 'SOLID', color: hex(o.color || INK) }];
  if (o.w) { t.textAutoResize = 'HEIGHT'; t.resize(o.w, t.height); }
  if (o.align) t.textAlignHorizontal = o.align; t.x = x; t.y = y; return t;
}
async function moveIcon(id, cx, cy, name) {
  const n = await figma.getNodeByIdAsync(id); root.appendChild(n); n.name = name; n.x = cx - n.width / 2; n.y = cy - n.height / 2; return n;
}
async function tile(x, y, id, label, name) {
  R(x, y, 96, 96, { fill: '#FFFFFF', stroke: PSTROKE, r: 18, name: 'tile ' + name });
  await moveIcon(id, x + 48, y + 48, 'logo ' + name);
  T(label, x - 22, y + 102, { w: 140, align: 'CENTER', style: 'Medium' });
}
function arrow(x1, y1, x2, y2, color, sw, name) {
  const pad = 12, minx = Math.min(x1, x2) - pad, miny = Math.min(y1, y2) - pad;
  const w = Math.abs(x2 - x1) + 2 * pad, h = Math.abs(y2 - y1) + 2 * pad;
  const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy), ux = dx / len, uy = dy / len;
  const L = 20, W = 10, bx = x2 - ux * L, by = y2 - uy * L;
  const p = (a, b) => `${(a - minx).toFixed(1)},${(b - miny).toFixed(1)}`;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><line x1="${(x1 - minx).toFixed(1)}" y1="${(y1 - miny).toFixed(1)}" x2="${(bx - minx).toFixed(1)}" y2="${(by - miny).toFixed(1)}" stroke="${color}" stroke-width="${sw}" stroke-linecap="round"/><polygon points="${p(x2, y2)} ${p(bx - uy * W, by + ux * W)} ${p(bx + uy * W, by - ux * W)}" fill="${color}"/></svg>`;
  const n = figma.createNodeFromSvg(svg); root.appendChild(n); n.x = minx; n.y = miny; n.name = name || 'arrow'; return n;
}
function badge(cx, cy, num) {
  const e = figma.createEllipse(); root.appendChild(e); e.resize(44, 44); e.x = cx - 22; e.y = cy - 22;
  e.fills = [{ type: 'SOLID', color: hex(BLUE) }]; e.strokes = [{ type: 'SOLID', color: hex('#FFFFFF') }]; e.strokeWeight = 3; e.name = 'badge ' + num;
  const t = T(String(num), cx - 22, cy - 15, { w: 44, align: 'CENTER', style: 'Semi Bold', color: '#FFFFFF', size: 26 }); t.y = cy - t.height / 2;
}
T('Technology stack and request flow', 48, 34, { size: 40, style: 'Bold' });
T('Degron Footprint web tool, design draft v0.1, development environment of 22 Oct 2026', 48, 90, { color: MUTED, w: 1500 });
R(48, 150, 640, 880, { fill: '#FFFFFF', stroke: LINE, sw: 2, r: 16, name: 'browser window' });
R(49, 151, 638, 56, { fill: PANEL, r: 15, name: 'browser title bar' });
for (let i = 0; i < 3; i++) { const e = figma.createEllipse(); root.appendChild(e); e.resize(16, 16); e.x = 72 + i * 28; e.y = 171; e.fills = [{ type: 'SOLID', color: hex(PSTROKE) }]; e.strokes = [{ type: 'SOLID', color: hex(LINE) }]; e.strokeWeight = 1.5; }
R(160, 163, 504, 32, { fill: '#FFFFFF', stroke: PSTROKE, sw: 1.5, r: 16, name: 'url pill' });
T('Degron Footprint', 178, 164, { size: 24, color: MUTED });
const phStatus = R(72, 226, 592, 175, { fill: '#E8ECF1', name: 'ph-status' });
const phHeat = R(72, 417, 400, 586, { fill: '#E8ECF1', name: 'ph-heatmap' });
T('28 positions by 19 substitutions', 488, 470, { w: 176, color: INK, style: 'Medium' });
T('Darker cell: higher P(ΔPSI ≥ 1.0)', 488, 640, { w: 176, color: MUTED });
T('Real screenshot of the running tool: tile 28 of protein A6NMZ7 (example)', 48, 1044, { w: 640, color: MUTED });
R(48, 1136, 640, 140, { fill: PANEL, stroke: PSTROKE, r: 20, name: 'tests card' });
await moveIcon('1:22', 112, 1206, 'logo openapi');
T('13 endpoints, OpenAPI 3.1 contract', 160, 1146, { w: 520, style: 'Medium' });
T('149 pytest and 131 vitest tests', 160, 1180, { w: 520 });
T('Playwright end-to-end tests', 160, 1214, { w: 520 });
function panel(x, y, w, h, stroke, iconId, title, iconName) {
  R(x, y, w, h, { fill: PANEL, stroke, sw: 3, r: 22, name: 'panel ' + title });
  return moveIcon(iconId, x + 40, y + 40, iconName).then(() => T(title, x + 72, y + 22, { size: 30, style: 'Semi Bold' }));
}
await panel(740, 150, 760, 224, BLUE, '1:24', 'Browser', 'icon monitor');
await tile(764, 214, '1:2', 'React', 'react'); await tile(934, 214, '1:4', 'TypeScript', 'typescript'); await tile(1104, 214, '1:6', 'Vite', 'vite');
T('Vite build, heatmap drawn with d3-scale', 1226, 232, { w: 260, color: MUTED });
await panel(740, 440, 760, 168, '#56B4E9', '1:28', 'Gateway', 'icon network');
await tile(764, 484, '1:8', 'nginx', 'nginx');
T('Serves the static build and proxies /v1 to the API', 904, 508, { w: 580, color: MUTED });
await panel(740, 670, 420, 270, '#009E73', '1:34', 'Service', 'icon server');
await tile(764, 732, '1:10', 'FastAPI', 'fastapi'); await tile(884, 732, '1:12', 'Python', 'python'); await tile(1004, 732, '1:14', 'NumPy', 'numpy');
T('Validate, domain gate, ridge + Platt scoring', 764, 876, { w: 380, color: MUTED });
await panel(1230, 670, 270, 270, '#E69F00', '1:39', 'Data', 'icon database');
await tile(1250, 732, '1:16', 'PostgreSQL', 'postgresql'); await tile(1390, 732, '1:18', 'SQLite', 'sqlite');
T('SQLite for dev and tests', 1250, 876, { w: 230, color: MUTED });
R(722, 414, 796, 640, { stroke: '#2496ED', sw: 3, dash: [12, 8], r: 28, name: 'docker compose outline' });
await moveIcon('1:20', 770, 1010, 'logo docker');
T('Docker Compose: configured, not yet run in this environment', 820, 982, { w: 440, color: MUTED });
arrow(900, 380, 900, 432, BLUE, 4, 'arrow 2 down'); arrow(1060, 432, 1060, 380, BLUE, 4, 'arrow 5 up');
badge(900, 406, 2); T('POST /v1/predict', 922, 392, { size: 24, style: 'Medium', w: 140 });
arrow(900, 614, 900, 664, BLUE, 4, 'arrow down to service'); arrow(1060, 664, 1060, 614, BLUE, 4, 'arrow up from service');
badge(1060, 406, 5); badge(1195, 748, 3);
arrow(1166, 800, 1224, 800, BLUE, 4, 'arrow 3 to data'); arrow(1224, 850, 1166, 850, '#7A8594', 3, 'arrow data back'); badge(1118, 700, 4);
R(740, 1086, 760, 176, { fill: PANEL, stroke: LINE, sw: 3, r: 22, name: 'panel ETL' });
await moveIcon('1:43', 780, 1126, 'icon file-down');
T('ETL: one-shot load into the database', 812, 1108, { size: 30, style: 'Semi Bold', w: 660 });
for (const [s, x, w] of [['UniProt', 764, 150], ['GEO screen', 934, 190], ['ClinVar', 1144, 150]]) { R(x, 1166, w, 52, { fill: '#FFFFFF', stroke: PSTROKE, r: 14, name: 'chip ' + s }); T(s, x, 1178, { w, align: 'CENTER', style: 'Medium' }); }
arrow(1306, 1192, 1366, 1192, LINE, 3, 'arrow ETL'); T('Database', 1380, 1178, { w: 110, style: 'Medium' });
T('Blocked sources enforced: Koren, MetaDegron, Larsen', 764, 1226, { size: 24, color: MUTED, w: 720 });
T('Request flow', 48, 1306, { size: 30, style: 'Semi Bold' });
['Choose a tile in the browser', 'POST /v1/predict through nginx', 'Look up tile and domain status', 'Score 532 substitutions: ridge + Platt', 'Return matrix, warnings, provenance'].forEach((s, i) => {
  const x = 48 + i * 317; R(x, 1352, 292, 128, { fill: '#FFFFFF', stroke: PSTROKE, sw: 2, r: 18, name: 'step ' + (i + 1) });
  badge(x + 38, 1352 + 38, i + 1); T(s, x + 70, 1364, { w: 208, style: 'Medium' });
});
T('Docker and PostgreSQL configuration is written but not yet run in this environment; development and tests use SQLite. Counts from system/README.md section 3.1.', 48, 1500, { w: 1500, color: MUTED });
return { rootId: root.id, phStatus: phStatus.id, phHeat: phHeat.id, children: root.children.length };
