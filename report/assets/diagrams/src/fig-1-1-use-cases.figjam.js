// UML use case diagram of the Degron Footprint tool, drawn in FigJam with the Figma MCP tool `use_figma`.
// Mermaid (generate_diagram) has no use case diagram type, so this one is built from FigJam primitives:
//   actor = ellipse head + vector body + text, use case = ELLIPSE shape, system boundary = section + outlined rectangle,
//   association = solid connector, <<include>>/<<extend>> = dashed connector with an open arrowhead.
// Final state after three runs (draw, fix attachment points, polish). Run with use_figma on a FigJam board;
// X0/Y0 pick a free area. Connector endpoints use POSITION IN PIXELS inside the node (not 0-1 ratios).
const h = (r, g, b) => ({ r: r / 255, g: g / 255, b: b / 255 });
const DARK = h(0x1e, 0x1e, 0x1e);
const BLUE = { fill: h(0xc2, 0xe5, 0xff), stroke: h(0x3d, 0xad, 0xff), text: DARK };
const GRAY = { fill: h(0xd9, 0xd9, 0xd9), stroke: h(0xb3, 0xb3, 0xb3), text: DARK };
const X0 = 20700, Y0 = -100;

const probe = figma.createShapeWithText(); await figma.loadFontAsync(probe.text.fontName); probe.remove();
const TEXT_FONT = { family: 'Inter', style: 'Medium' }; await figma.loadFontAsync(TEXT_FONT);

const section = figma.createSection();
section.name = 'Degron Footprint tool';
section.x = X0 + 260; section.y = Y0; section.resize(1440, 1000);
section.fills = [{ type: 'SOLID', color: h(255, 255, 255) }];

function useCase(label, x, y, w, hh, p) {
  const s = figma.createShapeWithText(); s.shapeType = 'ELLIPSE'; section.appendChild(s);
  s.text.characters = label; s.resize(w, hh); s.x = x; s.y = y;
  s.fills = [{ type: 'SOLID', color: p.fill }]; s.strokes = [{ type: 'SOLID', color: p.stroke }];
  s.text.fills = [{ type: 'SOLID', color: p.text }];
  return s;
}
const uc04 = useCase('UC-04 Select tile from a protein', 60, 80, 380, 140, BLUE);
const uc02 = useCase('UC-02 Rank substitutions', 60, 290, 380, 140, BLUE);
const uc03 = useCase('UC-03 Export with provenance', 60, 545, 380, 140, BLUE);
const uc07 = useCase('UC-07 View model card', 60, 790, 380, 140, BLUE);
const uc05 = useCase('UC-05 Compare with measured data', 600, 90, 380, 140, BLUE);
const uc01 = useCase('UC-01 Predict effect matrix', 600, 400, 380, 140, BLUE);
const uc06 = useCase('UC-06 View ClinVar variants', 600, 710, 380, 140, BLUE);
const validate = useCase('Validate input', 1160, 410, 240, 120, GRAY);

const title = figma.createText(); section.appendChild(title);
title.fontName = TEXT_FONT; title.characters = 'Degron Footprint tool'; title.fontSize = 28; title.x = 40; title.y = 24;
const rect = figma.createRectangle(); section.appendChild(rect);   // visible UML system boundary
rect.name = 'System boundary'; rect.x = 10; rect.y = 10; rect.resize(section.width - 20, section.height - 20);
rect.fills = []; rect.strokes = [{ type: 'SOLID', color: DARK }]; rect.strokeWeight = 3;

const AX = X0 + 40, AY = Y0 + 400;                                   // actor: stick figure
const head = figma.createEllipse(); head.resize(46, 46); head.x = AX + 37; head.y = AY;
head.fills = [{ type: 'SOLID', color: h(255, 255, 255) }]; head.strokes = [{ type: 'SOLID', color: DARK }]; head.strokeWeight = 3;
const body = figma.createVector();
body.vectorPaths = [{ windingRule: 'NONE', data: 'M 60 46 L 60 124 M 20 74 L 100 74 M 60 124 L 22 196 M 60 124 L 98 196' }];
body.fills = []; body.strokes = [{ type: 'SOLID', color: DARK }]; body.strokeWeight = 3; body.strokeCap = 'ROUND';
body.x = AX + 20; body.y = AY + 46;
const label = figma.createText(); label.fontName = TEXT_FONT; label.characters = 'User\n(researcher or student)';
label.fontSize = 19; label.textAlignHorizontal = 'CENTER'; label.textAutoResize = 'HEIGHT'; label.resize(340, 60);
label.x = AX - 110; label.y = AY + 214; label.fills = [{ type: 'SOLID', color: DARK }];
figma.group([head, body, label], figma.currentPage).name = 'Actor: User';

function edge(node, deg) {                                           // point on an ellipse boundary, pixels
  const a = node.width / 2, b = node.height / 2, t = deg * Math.PI / 180;
  return { endpointNodeId: node.id, position: { x: a + a * Math.cos(t), y: b - b * Math.sin(t) } };
}
function link(start, end, { dashed, arrow, text }) {
  const c = figma.createConnector(); c.connectorStart = start; c.connectorEnd = end; c.connectorLineType = 'STRAIGHT';
  c.connectorStartStrokeCap = 'NONE'; c.connectorEndStrokeCap = arrow ? 'ARROW_LINES' : 'NONE';
  c.strokes = [{ type: 'SOLID', color: DARK }]; c.strokeWeight = 2; c.dashPattern = dashed ? [10, 6] : [];
  if (text) { c.text.fontName = TEXT_FONT; c.text.characters = text; }
}
const ax = X0 + 40 + 110, ay = Y0 + 400 + 110;
for (const u of [uc04, uc02, uc03, uc01, uc07]) link({ position: { x: ax, y: ay } }, edge(u, 180), { dashed: false, arrow: false });
link(edge(uc02, 315), edge(uc01, 135), { dashed: true, arrow: true, text: '«include»' });
link(edge(uc03, 45), edge(uc01, 225), { dashed: true, arrow: true, text: '«include»' });
link(edge(uc01, 0), edge(validate, 180), { dashed: true, arrow: true, text: '«include»' });
link(edge(uc05, 270), edge(uc01, 90), { dashed: true, arrow: true, text: '«extend»' });
link(edge(uc06, 90), edge(uc01, 270), { dashed: true, arrow: true, text: '«extend»' });
