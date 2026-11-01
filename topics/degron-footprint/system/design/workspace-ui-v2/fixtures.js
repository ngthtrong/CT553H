/* Illustrative fixtures only. This module does not call or approximate the model. */
window.FootprintFixtures = (() => {
  const alphabet = 'ACDEFGHIKLMNPQRSTVWY';
  const sequence = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';
  const model = 'm3-ext4.0-platt-v1';
  function cellsFor(sequence) {
    const cells = [];
    [...sequence].forEach((wt, i) => [...alphabet].forEach((mut, j) => {
      if (wt === mut) return;
      const wave = Math.sin((i + 2) * .76 + j * .43) * .5 + Math.cos(i * .35 - j * .83) * .27;
      const raw = Math.round((wave * 1.65 + (i > 9 && i < 19 ? .3 : -.35)) * 1000) / 1000;
      const probability = Math.round((1 / (1 + Math.exp(-raw * 1.7 - .1))) * 1000) / 1000;
      cells.push({id:`${i+1}-${mut}`, position:i+1, wt, mut, raw, probability});
    }));
    cells.sort((a,b) => b.probability-a.probability || a.position-b.position || a.mut.localeCompare(b.mut));
    cells.forEach((c,i) => { c.rank=i+1; c.top10=i<Math.ceil(cells.length*.1); });
    return cells;
  }
  function result(seq=sequence, reference=true) {
    return {id:null, sequence:seq, reference, label:reference?'COL6A6 · Tile 28':'Custom peptide', accession:reference?'A6NMZ7':null,
      tile:reference?28:null, start:reference?622:null, end:reference?649:null, domain:'unknown',
      gate:'not connected in design preview', model, evidence:'Development OOF benchmark, not external validation',
      fixture:true, generatedBy:'illustrative-ui-fixture-v2', createdAt:'2026-11-01T09:00:00+08:00', cells:cellsFor(seq), shortlist:[]};
  }
  return {alphabet, sequence, model, result,
    probabilityScale:['#fde725','#bddf26','#7ad151','#44bf70','#22a884','#21918c','#2a788e','#355f8d','#414487','#482475','#440154'],
    rawScale:['#7f3b08','#b35806','#e08214','#fdb863','#fee0b6','#f7f7f7','#d8daeb','#b2abd2','#8073ac','#542788','#2d004b'],
    projects:[{id:'p-col6a6',name:'COL6A6 exploration',description:'Residue-level substitutions and experimental follow-up.',date:'01 Nov 2026'},
      {id:'p-pilot',name:'Assay comparison',description:'Compare predictions with project measurements.',date:'31 Oct 2026'},
      {id:'p-empty',name:'Sequence library',description:'A fresh workspace for the next set of questions.',date:'30 Oct 2026'}],
    observations:[{position:14,wt:'P',mut:'W',value:1.12,replicate:'rep-1'}, {position:17,wt:'F',mut:'A',value:.47,replicate:'rep-1'},
      {position:11,wt:'S',mut:'L',value:-.28,replicate:'rep-1'}, {position:19,wt:'K',mut:'R',value:null,replicate:'rep-1',missing:'not measured'}]
  };
})();
