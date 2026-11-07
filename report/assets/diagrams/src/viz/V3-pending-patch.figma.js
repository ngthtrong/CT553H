// V3 (fig-3-8-data-processing): LAST EDIT NOT YET APPLIED, Figma MCP tool-call limit of the Starter plan was reached.
// Run with use_figma on file DU3N3ikRcLELYZcPK0SYxI (frame 1:2), then export the frame at scale 2
// (get_screenshot nodeId 1:2 maxDimension 3200, or download_assets defaultScale 2) over fig-3-8-data-processing.png.
// Effects: single-line captions in step 5, baseline note merged into the step 3 subtitle, equal panel heights per row.
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
const main = await figma.getNodeByIdAsync('1:2');
const find = (from) => { const t = main.findAll(n => n.type === 'TEXT' && n.characters === from)[0]; if (!t) throw new Error('text not found: ' + from); return t; };
find('4 base folds plus all 83 extra clusters: 154 clusters').characters = '4 base folds + 83 extra clusters';
find('Base peptides of the held-out fold only: 18 clusters').characters = 'Held-out fold: 18 base clusters';
find('PSI of wild type, 235 peptides with a baseline').characters = 'PSI of wild type: 235 of 248 peptides have a baseline';
find('13 of 248 peptides lack a WT baseline').remove();
const out = [];
for (const row of main.findAll(n => n.type === 'FRAME' && (n.name === 'Row 2' || n.name === 'Row 3'))) {
  const panels = row.children.filter(c => c.name.startsWith('Step'));
  const hMax = Math.max(...panels.map(p => p.height));
  for (const p of panels) { p.layoutSizingVertical = 'FIXED'; p.resize(p.width, hMax); }
  out.push({ row: row.name, hMax });
}
return { out, mainH: main.height };
