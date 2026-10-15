/* Scientific diagrams drawn for this presentation. No existing repo slide is used. */
window.DECK_PARTS = [];
window.V = (() => {
  const ink='#15323f',teal='#2a9d8f',coral='#d1495b',blue='#386fa4',muted='#546e79';
  let serial=0;
  const svg=(label,body,w=700,h=400)=>{
    const id=`arrow-${++serial}`;
    return `<svg class="diagram" viewBox="0 0 ${w} ${h}" role="img" aria-label="${label}"><defs><marker id="${id}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="${muted}"/></marker></defs>${body.replaceAll('url(#arrow)',`url(#${id})`)}</svg>`;
  };
  const text=(x,y,s,cl='label',extra='')=>`<text x="${x}" y="${y}" class="${cl}" ${extra}>${s}</text>`;
  const box=(x,y,w,h,s,color='#fff')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="${color}" stroke="#dce5e9" stroke-width="2"/>${text(x+w/2,y+h/2+7,s,'label','text-anchor="middle"')}`;
  const arrow=(x,y,x2,y2)=>`<path d="M${x} ${y}L${x2} ${y2}" class="arrow flow"/>`;
  function seq(s='MKTAYIMKQRQISFVKSHFSRQDILDLW',hot=[6,7,8],compact=false){return `<div class="sequence-wrap"><div class="sequence ${compact?'compact':''}">${[...s].map((a,i)=>`<span class="residue ${hot.includes(i)?'hot':''}" data-i="${i+1}">${a}</span>`).join('')}</div></div>`;}
  const miniMatrix=()=>`<div class="mini-heatmap" role="img" aria-label="Schematic matrix, no numeric predictions">${'<i></i>'.repeat(180)}</div>`;
  function folding(){
    const s='MKTAYIMKQRQISFVK';
    return svg('Schematic protein chain folds, then residue 7 changes from M to V',
      text(25,40,'Sequence → fold → substitution','sub')+
      [...s].map((a,i)=>{const x=35+i*40,y=130,ang=i*.95,fx=345+95*Math.cos(ang),fy=250+75*Math.sin(ang);return `<g class="fold-bead" style="--dx:${fx-x}px;--dy:${fy-y}px" data-residue="${i+1}"><circle cx="${x}" cy="${y}" r="17" fill="${i===6?coral:teal}" opacity=".9"/>${text(x,y+6,a,'sub',`text-anchor="middle" style="fill:white" data-letter="${i+1}"`)}${text(x,y+40,i+1,'sub','text-anchor="middle"')}</g>`;}).join('')+
      `<g class="fragment" data-fragment-index="0">${text(25,360,'Same chain, a three-dimensional fold.','sub')}</g><g class="fragment" data-fragment-index="1">${text(25,390,'M7V: methionine → valine at residue 7.','label')}</g>`,700,430);
  }
  function balance(){return svg('Protein amount is controlled by synthesis and degradation',
    text(24,50,'SYNTHESIS','sub')+text(510,50,'DEGRADATION','sub')+
    arrow(40,100,225,100)+arrow(460,100,650,100)+
    `<circle class="supply-dot" cx="45" cy="100" r="8" fill="${teal}"/><circle class="drain-dot" cx="470" cy="100" r="8" fill="${coral}"/>`+
    `<path d="M340 160L295 310H385Z" fill="#dce5e9"/><g class="balance-line"><path d="M120 160H560" stroke="${ink}" stroke-width="7"/><path d="M140 160v75M540 160v75" stroke="${ink}" stroke-width="2"/><path d="M75 235Q140 300 205 235Z" fill="${teal}" opacity=".8"/><path d="M475 235Q540 300 605 235Z" fill="${coral}" opacity=".8"/></g>`+
    `<g class="fragment" data-fragment-index="0">${text(140,365,'Faster clearance → less protein in the cell','label')}</g>`,700,400);}
  function ups(){return svg('Three schematic UPS stages: recognition, ubiquitin tagging, proteasomal degradation',
    `<g class="e3-shape"><path d="M60 90h90v95h-30v-40H90v40H60Z" fill="${blue}"/>${text(105,75,'E3','label','text-anchor="middle"')}</g>`+
    `<g class="ups-protein"><path d="M70 245q30-45 60 0t60 0t60 0t60 0" fill="none" stroke="${muted}" stroke-width="11"/><path d="M130 245q30 45 60 0" fill="none" stroke="${coral}" stroke-width="12"/></g>`+
    `<g class="fragment" data-fragment-index="0">${[0,1,2,3].map(i=>`<circle cx="${242+i*29}" cy="${220-i*25}" r="17" fill="#e9c46a"/>`).join('')}${text(300,90,'Ubiquitin chain','sub')}</g>`+
    `<ellipse cx="525" cy="145" rx="69" ry="24" fill="#b6c7ce"/><path d="M456 145v155q69 45 138 0V145" fill="#dce5e9"/><ellipse cx="525" cy="145" rx="43" ry="13" fill="${ink}"/>${text(525,355,'26S proteasome','label','text-anchor="middle"')}`+
    `<g class="fragment" data-fragment-index="1">${[0,1,2].map(i=>`<path d="M610 ${190+i*45}l28 14l27-14" stroke="${teal}" stroke-width="7" fill="none"/>`).join('')}${text(590,110,'Peptides','sub')}</g>`,700,400);}
  function zoom(){return svg('Protein region to 28-residue peptide to important residues',
    `<path d="M70 100q110-100 170 15t-110 80t-10-130t120 100" fill="none" stroke="#b6c7ce" stroke-width="16"/><path d="M165 82l39 30" stroke="${coral}" stroke-width="18"/>`+
    text(63,240,'Protein','label')+arrow(270,135,365,135)+
    `<g class="fragment" data-fragment-index="0">${box(390,76,245,112,'28-residue window','#edf3f8')}${text(390,230,'An autonomous degron','sub')}</g>`+
    `<g class="fragment" data-fragment-index="1">${[0,1,2,3,4,5,6,7].map(i=>`<rect x="${115+i*61}" y="300" width="49" height="49" rx="4" fill="${[2,3,4].includes(i)?coral:'#dce5e9'}"/>`).join('')}${text(210,395,'Which residues control its strength?','label')}</g>`,700,430);}
  function forest(){
    const x=v=>65+(v-.8)*355;
    return svg('Within-protein pathogenic-versus-benign odds ratio: 2.148, confidence interval 2.072 to 2.227',
      text(35,40,'Within-protein association','label')+
      `<path d="M${x(1)} 70V205" stroke="${muted}" stroke-dasharray="6 6"/><path d="M${x(.8)} 205H${x(2.45)}" stroke="${muted}"/>`+
      [1,1.5,2,2.4].map(v=>text(x(v),237,v,'sub','text-anchor="middle"')).join('')+
      `<g class="fragment" data-fragment-index="0"><path d="M${x(2.072)} 135H${x(2.227)}" stroke="${teal}" stroke-width="5"/><circle cx="${x(2.148)}" cy="135" r="10" fill="${teal}"/>${text(210,100,'OR 2.148 [2.072, 2.227]','label')}</g>`+
      text(45,285,'3,114 protein strata · 2.56 M variants','sub')+text(45,320,'Odds ratio; dashed reference = 1','sub'),700,340);
  }
  function gps(){return svg('GPS workflow: peptide reporter, cells, sorting into six bins, sequencing and PSI',
    box(15,80,255,90,'Peptide–GFP reporter','#eaf5f2')+arrow(280,125,345,125)+box(360,80,200,90,'Cell library')+arrow(570,125,640,125)+
    [0,1,2,3,4,5].map((i)=>`<rect x="${660+i*60}" y="${165-i*16}" width="44" height="${35+i*16}" rx="3" fill="${i<3?coral:teal}" opacity="${.4+i*.1}"/>${text(682+i*60,230,i+1,'sub','text-anchor="middle"')}`).join('')+
    text(665,55,'FACS stability bins','label')+arrow(1040,125,1110,125)+box(1125,80,245,90,'Sequence → PSI')+
    text(15,295,'Library synthesis','sub')+text(360,295,'One peptide per cell','sub')+text(660,295,'GFP / stable-control ratio','sub')+text(1125,295,'Weighted bin average','sub'),1400,340);}
  function resolution(){return svg('Question resolution from protein through region to residue',
    ['Protein','Region','Motif','Residue'].map((s,i)=>box(30,20+i*90,190,66,s,i===3?'#fbf0da':'#fff')+(i<3?arrow(125,87+i*90,125,106+i*90):'')).join('')+
    text(260,145,'Degpred · DegronMD','label')+text(260,235,'DEGRONOPEDIA · MetaDegron','label')+text(260,325,'Measured mutation effects?','label'),700,390);}
  function shuffle(){
    const s='ALDLKAVDLK';const perm=[3,7,1,9,5,0,8,2,6,4];
    return svg('Permutation of sequence leaves the internal PAP cnn2w1 score unchanged',
      text(15,35,'PAP internal channel: cnn2w1','label')+
      [...s].map((a,i)=>`<g class="shuffle-cell" style="--shuffle:${(perm[i]-i)*46}px"><rect x="${30+i*46}" y="90" width="39" height="43" rx="4" fill="${i%3===0?coral:teal}"/>${text(49+i*46,119,a,'label','text-anchor="middle" style="fill:white"')}</g>`).join('')+
      arrow(280,165,280,220)+box(130,250,300,75,'Same model score')+text(460,300,'=','big')+
      text(20,385,'Pearson(original, shuffled) = 1.000000','label'),700,420);}
  function benchmark(){
    const y=v=>470-(v-.7)/.26*380;
    let b='';
    [.7,.75,.8,.85,.9,.95].forEach(v=>{b+=`<path d="M65 ${y(v)}H970" stroke="#e0e7ea"/>`+text(15,y(v)+5,v.toFixed(2),'sub');});
    const data=[{x:150,n:'Scanning',vals:[['ΔPAP w1',.7943,muted],['ΔPAP w7',.8357,blue],['M0',.8393,ink],['M3',.8682,teal]],ceiling:.9458},{x:650,n:'Saturation',vals:[['M0',.7071,ink],['M3',.7273,teal],['ΔPAP w1',.7693,coral]],ceiling:.9519}];
    data.forEach((d,k)=>{b+=`<g class="${k?'fragment':''}" data-fragment-index="0">`+text(d.x,530,d.n,'label')+`<path d="M${d.x-20} ${y(d.ceiling)}h290" stroke="${ink}" stroke-dasharray="7 5"/>`+text(d.x-10,y(d.ceiling)-13,`Ceiling ${d.ceiling}`,'sub');
      d.vals.forEach(([n,v,c],i)=>{const x=d.x+i*65;b+=`<circle cx="${x}" cy="${y(v)}" r="8" fill="${c}"/><path d="M${x} ${y(v)}V480" stroke="${c}" opacity=".3"/>`+text(x+12,y(v)+(i%2?5:20),`${n} ${v.toFixed(4)}`,'sub',`style="fill:${c};font-size:16px"`);});b+='</g>';});
    return svg('Cell-level AUROC benchmark, axis starts at 0.70. Scanning gain and saturation shortfall are shown separately.',b,1050,560);
  }
  function workflow(labels){return `<div class="stages">${labels.map((s,i)=>`<div class="stage fragment rise" data-fragment-index="${i}"><div class="stage-no">0${i+1}</div>${s}</div>`).join('')}</div>`;}
  function split(){return svg('Protein clusters remain intact on either side of the train and test split',
    `<rect x="15" y="20" width="290" height="220" rx="12" fill="#eaf5f2"/><rect x="355" y="20" width="290" height="220" rx="12" fill="#edf3f8"/>`+
    [65,165,235,405,505,575].map((x,k)=>[0,1,2,3,4].map((j)=>`<circle cx="${x+Math.cos(j*1.25)*22}" cy="${110+Math.sin(j*1.25)*22+(k%2)*50}" r="9" fill="${k<3?teal:blue}"/>`).join('')).join('')+
    text(85,285,'TRAIN CLUSTERS','sub')+text(425,285,'TEST CLUSTERS','sub')+`<path d="M330 10V240" stroke="${coral}" stroke-dasharray="6 6"/>`+text(25,335,'All homologues and cross-source overlaps travel together.','sub'),700,360);}
  function decomposition(){return `<div class="metric-bars" aria-label="Gain decomposition: neighbourhood composition 0.0232; order 0.0057; absolute-position increment 0.0002 separately"><div style="width:80.28%;background:${teal}">±3 composition · 80%</div><div style="width:19.72%;background:${blue}">Order</div></div><div class="decomposition-labels"><span>+0.0232 neighbourhood composition</span><span>+0.0057 order</span></div><p class="tiny muted" style="margin-top:14px">Absolute position adds +0.0002 on top of context; reported separately.</p>`;}
  return {svg,text,box,arrow,seq,miniMatrix,folding,balance,ups,zoom,forest,gps,resolution,shuffle,benchmark,workflow,split,decomposition};
})();
