await figma.setCurrentPageAsync(await figma.getNodeByIdAsync(CONFIG.foundation.pages.screens));
// DF01 — Projects
{
const s=shell('DF01','Projects','Continue a saved project or start a transient peptide preview.',{index:0});
const hero=card('Research introduction',1152);const r=row('Introduction with abstract 3D accent',1104,24);const copy=al('Introduction copy',680,'VERTICAL',16);
add(copy,tag('RESIDUE-LEVEL EXPLORATION','brand'),txt('From sequence to the\nnext experiment.','Display',680),txt('Explore substitution effects, compare measurements and keep the evidence attached to every decision.','Large',640,'muted'));
const acts=row('Introduction actions',680,12);add(acts,btn('New analysis','primary','DF03'),btn('Create project','secondary','ST09'));add(copy,acts);
const image=al('Abstract illustration',400,'VERTICAL',4);add(image,art(400,228),txt('Abstract illustration · not a protein structure','Caption',400,'muted'));add(r,copy,image);add(hero,r);add(s.content,hero);
const stats=row('Workspace summary',1152,16);add(stats,stat('3','Projects','Stored on this computer',373),stat('12','Saved analyses','Immutable run snapshots',373),stat('2','Experimental datasets','Comparison only',374));add(s.content,stats);
const c=card('Your projects');add(c,sectionTitle('Your projects','Example workspace contents · reopen a project to see its frozen history.'),table(['Project','Updated','Analyses','Jobs','Datasets','Open'],[
['COL6A6 pilot','31 Oct 2026','5','1','1',btn('Open','secondary','DF02')],['Sequence exploration','30 Oct 2026','4','0','0',btn('Open','subtle','DF02')],['Assay comparison','29 Oct 2026','3','1','1',btn('Open','subtle','DF02')]
],1104,[300,176,136,104,136,252]));add(s.content,c);finish(s);
}
// DF02 — Workspace/history
{
const s=shell('DF02','COL6A6 pilot','Local project · saved work is retained until you delete it.',{index:1,breadcrumb:'Projects / COL6A6 pilot'});
add(s.content,actionRow(btn('New analysis','primary','DF03'),btn('Import observations','secondary','DF12'),btn('Rename project','subtle','ST10'),btn('Delete project','subtle','ST03')),
tabs(['Analysis history','Jobs','Experimental datasets'],'Analysis history',1152,{'Jobs':'DF08','Experimental datasets':'DF14'}));
const stats=row('Project totals',1152,16);add(stats,stat('5','Saved analyses','Open the original snapshot',373),stat('1','Batch job','Partial · review tile outcomes',373),stat('1','Committed dataset','GPS pilot · revision 1',374));add(s.content,stats);
add(s.content,banner('Reopen a snapshot; rerun as a new entry','Saved model, domain and source versions stay attached. Run again creates a new analysis.','info'));
const c=card('Analysis history');add(c,sectionTitle('Analysis history','Newest first · example data'),table(['Input / context','Run / model','Saved','State','Action'],[
['COL6A6 · tile 28\n622–649','run-028 · m3-ext4.0','31 Oct · 15:42',tag('Training peptide','warning'),btn('Open snapshot','secondary','DF10')],
['COL6A6 · tile 29\n645–672','run-029 · m3-ext4.0','31 Oct · 15:41',tag('Domain unknown','warning'),btn('Open snapshot','subtle','DF10')],
['Custom peptide\nNo verified mapping','run-027 · m3-ext4.0','30 Oct · 11:24',tag('Saved','success'),btn('Open snapshot','subtle','DF10')]
],1104,[264,240,168,216,216]));add(c,txt('Showing 1–3 of 5 analyses. Every row opens a frozen result.','Caption',1104,'muted'));add(s.content,c);finish(s);
}
// DF03 — transient single peptide
{
const s=shell('DF03','New analysis','Choose the input unit. The effect model scores one 28-residue tile at a time.',{index:2,active:'New analysis'});
add(s.content,tabs(['Single peptide','Peptide batch','Whole protein'],'Single peptide',1152,{'Peptide batch':'DF05','Whole protein':'DF06'}));
const r=row('Input and guidance',1152,24);r.counterAxisAlignItems='MIN';const left=card('Single peptide input',744),right=card('Analysis guide',384);
add(left,sectionTitle('Paste a peptide','Exactly 28 standard amino acids; case and outer whitespace are normalised.',696),sequence(CONFIG.fixture.sequence,696));
const count=row('Sequence validation',696,16);add(count,tag('28 / 28 residues','success'),txt('All letters are valid','Caption',270,'muted'));add(left,count,txt('This is a transient preview. Save to a project later to keep it.','Body',696,'muted'),banner('Domain unknown · custom sequence','No canonical protein is inferred from pasted text. ClinVar needs a verified accession and release.','warning',696));
const acts=row('Predict actions',696,12);add(acts,btn('Predict 532 substitutions','primary','DF18'),btn('Choose a protein','secondary','DF04'));add(left,acts);
add(right,tag('FROZEN MODEL','brand'),txt('What will you see?','Heading',336),txt('1. Domain and evidence\n2. A 28 × 20 effect matrix\n3. Within-tile ranking\n4. Export and provenance','Large',336),rule(336),txt('P(ΔPSI ≥ 1.0)','Mono',336),txt('The event is a stability-index increase of at least one assay bin, which weakens the degron signal in this assay.','Body',336,'muted'),txt('m3-ext4.0-platt-v1','MonoSmall',336,'muted'));
add(r,left,right);add(s.content,r);finish(s);
}
// DF04 — protein search and tile selection
{
const s=shell('DF04','Protein explorer','Choose a loaded human reference protein, then inspect its tile context.',{index:3,active:'New analysis',height:1420});
const search=card('Protein search');add(search,field('Gene or UniProt accession','COL6A6 — Collagen alpha-6(VI) chain — A6NMZ7',1104,'Loaded human reference · UniProt 2026_03'));
const st=row('Protein facts',1104,16);add(st,stat('2,263','Protein residues','Canonical reference sequence',357),stat('98','Full tiles','28 residues · step 23',357),stat('4','Uncovered residues','Terminal interval 2260–2263',358));add(search,st);add(s.content,search);
const c=card('Tile map');add(c,sectionTitle('Choose a tile','Pattern and text repeat the domain status. The list below offers the same selection.'));
const tiles=al('98 full reference windows',1104,'VERTICAL',8);
for(let j=0;j<7;j++){const rr=row('Tile map row '+(j+1),1104,8);for(let k=1;k<=14;k++){const n=j*14+k;const selected=n===28;const tile=al('Tile '+n+' · residues '+((n-1)*23+1)+'–'+((n-1)*23+28),71,'VERTICAL',2,selected?'accentSoft':'soft');tile.resize(71,44);tile.layoutSizingVertical='FIXED';tile.paddingTop=6;tile.paddingLeft=8;radius(tile,8);if(selected)stroke(tile,'accent');const mark=selected?'● IN':n%7===0?'? UNK':n%5===0?'· BDR':n%3===0?'╱ OUT':'● IN';add(tile,txt(String(n).padStart(2,'0')+'  '+mark,'MonoSmall',59,selected?'accent':'muted'));add(rr,tile);}add(tiles,rr);}add(c,tiles,txt('● In-domain   ╱ Out-of-domain   · Borderline   ? Unknown   Dotted outline: unreliable','Caption',1104,'muted'),rule(1104),sectionTitle('Selected: tile 28 · residues 622–649'),sequence(),banner('Measured in-domain · design target gate','Measured evidence is interpreted by the frozen gate; the assay estimator remains identified.','success',1104));
const ac=row('Tile actions',1104,12);add(ac,btn('Predict tile 28','primary','DF09'),btn('Analyse whole protein','secondary','DF06'));add(c,ac);add(s.content,c);finish(s);
}
// DF05 — batch validation preview
{
const s=shell('DF05','Peptide batch','Review stable input IDs and validation before submitting a durable local job.',{index:4,active:'New analysis'});
add(s.content,tabs(['Single peptide','Peptide batch','Whole protein'],'Peptide batch',1152,{'Single peptide':'DF03','Whole protein':'DF06'}));
const c=card('Batch input');const fields=row('Project and batch identity',1104,24);add(fields,field('Project','COL6A6 pilot',540),field('Input format','Multi-record FASTA',540));add(c,fields);
const fasta=al('Pasted FASTA',1104,'VERTICAL',8,'soft');pad(fasta,16);radius(fasta,8);add(fasta,txt('>sample-001\nDIMFLVDSSGSIGPENFSKMKTFMKNLV\n>sample-002\nAIMFLVDSSGSIGPENFSKMKTFMKNLV\n>sample-003\nCIMFLVDSSGSIGPENFSKMKTFMKNLV','Mono',1072));add(c,fasta,btn('Validate inputs','secondary','DF05'));add(s.content,c);
const preview=card('Batch preview');add(preview,sectionTitle('Validation preview','Example: 3 peptide records · inputs are not yet saved'),table(['Input ID','Length','Syntax','Domain','Outcome'],[
['sample-001','28',tag('Valid','success'),'Predicted in-domain','Score with gate warning'],['sample-002','28',tag('Valid','success'),'Unknown','Score with warning'],['sample-003','28',tag('Valid','success'),'Predicted out-of-domain','Refused by default']
],1104,[200,120,176,280,328]),txt('Configured limit shown here is illustrative: 100 peptides / 1 MiB. Final defaults require local measurement.','Caption',1104,'muted'),banner('Submitting saves this job locally','Inputs, completed results and pinned model/source versions persist in COL6A6 pilot until deletion.','info',1104));add(preview,check('I understand this job will be stored in this local project.',true,1056));add(s.content,preview,actionRow(btn('Submit batch','primary','DF07'),btn('Back to input','secondary','DF03')));finish(s);
}
// DF06 — whole protein preview / coverage
{
const s=shell('DF06','Whole-protein preview','Inspect coverage before applying the same tile model across a protein.',{index:5,active:'New analysis'});
add(s.content,tabs(['Single peptide','Peptide batch','Whole protein'],'Whole protein',1152,{'Single peptide':'DF03','Peptide batch':'DF05'}));
const c=card('Protein submission');const fr=row('Protein job fields',1104,24);add(fr,field('Project','COL6A6 pilot',540),field('Input','A6NMZ7 · reference UniProt 2026_03',540));add(c,fr,txt('Alternatively upload one protein FASTA record. Custom FASTA has no inferred canonical mapping.','Body',1104,'muted'));
const st=row('Coverage summary',1104,16);add(st,stat('98','Full windows','28 residues · step 23',357),stat('1–2259','Covered interval','Distinct overlapping tile contexts',357),stat('2260–2263','Uncovered interval','4 terminal residues; no padding',358));add(c,st,sectionTitle('Coverage manifest','Design example from the 2,263-residue reference length.'));
const cov=row('Full coverage with terminal gap',1104,4);for(let i=0;i<28;i++){const segment=track(figma.createRectangle());segment.resize(i===27?20:36,32);fill(segment,i===27?'warning':'accentSoft');add(cov,segment);}add(c,cov,txt('1                                                                     2259    2260–2263 not covered','MonoSmall',1104,'muted'),table(['Window','Protein coordinates','Context rule'],[['Tile 1','1–28','Full window'],['Tile 28','622–649','Overlap retained'],['Tile 98','2232–2259','Final full window']],1104,[200,304,600]));add(s.content,c,banner('Tile effects do not establish a whole-protein effect','Each tile keeps its own domain, rank and source context. Out-of-domain windows are refused by default.','warning'),check('Save the protein input and job results in COL6A6 pilot.',true,1152),actionRow(btn('Submit 98-tile job','primary','DF07'),btn('Choose one tile','secondary','DF04')));finish(s);
}
function job(id,partial,index){
const s=shell(id,partial?'Job results · partial':'Processing protein tiles','COL6A6 pilot / job-098 · A6NMZ7 · frozen model and reference versions.',{index,height:1200,breadcrumb:'Projects / COL6A6 pilot / Jobs / job-098'});
add(s.content,tag(partial?'PARTIAL · 98 / 98 TERMINAL':'RUNNING · 66 / 98 TERMINAL',partial?'warning':'brand'));
const stats=row('Job outcome counts',1152,16);const counts=partial?[['91','Succeeded'],['5','Refused'],['2','Failed'],['0','Pending / running']]:[['62','Succeeded'],['3','Refused'],['1','Failed'],['32','Pending / running']];for(const [v,l]of counts)add(stats,stat(v,l,'Example job counts',276));add(s.content,stats);
const bar=card('Job progress');add(bar,sectionTitle(partial?'Processing ended with mixed outcomes':'Processing 66 terminal items out of 98',partial?'Completed analyses are preserved; refused and failed items remain in the manifest.':'Progress uses terminal item counts. You may leave this page and reopen the same job.'));
const trackBar=row('98-item progress',1104,0,'soft');trackBar.resize(1104,12);trackBar.layoutSizingVertical='FIXED';radius(trackBar,8);const seg=track(figma.createRectangle());seg.resize(partial?1104:744,12);fill(seg,partial?'warningInk':'accent');add(trackBar,seg);add(bar,trackBar);add(s.content,bar,banner(partial?'Partial is not completed':'Restart recovery uses the same job ID',partial?'91 scored + 5 refused + 2 failed = 98 items. Export all outcomes, including rows without scores.':'Unfinished work resumes after restart; completed snapshots are not duplicated. Cancellation preserves completed results.','info'));
const t=card('Per-tile outcomes');add(t,sectionTitle('Per-tile outcomes','Showing 1–5 of 98 items · paginated, 20 per page'),table(['Tile / coordinates','Outcome','Detail','Action'],[
['28 · 622–649',tag('Succeeded','success'),'532 substitutions',btn('Open tile','secondary','DF09')],['29 · 645–672',tag('Succeeded','success'),'Domain unknown warning',btn('Open tile','subtle','DF09')],['30 · 668–695',tag('Refused','warning'),'Out-of-domain; no scores',btn('Inspect','subtle','ST04')],['31 · 691–718',tag('Failed','danger'),'Non-standard residue; no scores',btn('Inspect','subtle','ST05')],['32 · 714–741',tag(partial?'Succeeded':'Running',partial?'success':'brand'),partial?'532 substitutions':'Scoring this tile…',btn(partial?'Open tile':'Details','subtle',partial?'DF09':'DF07')]
],1104,[260,200,384,260]));add(t,txt('Page 1 of 5 · all 98 items are included in export, not only this page.','Caption',1104,'muted'));add(s.content,t,actionRow(btn(partial?'Export all outcomes':'View terminal results','primary',partial?'ST02':'DF08'),btn(partial?'Back to project':'Cancel job','secondary',partial?'DF02':'ST06')));finish(s);
}
job('DF07',false,6);job('DF08',true,7);
// DF09 — full editable 28x20 result, key research view
{
const s=shell('DF09','Substitution effects','A6NMZ7 · tile 28 · residues 622–649 · 532 substitutions · model m3-ext4.0-platt-v1.',{index:8,active:'New analysis',height:1680,breadcrumb:'New analysis / Reference tile / Results'});
resultNotices(s.content);add(s.content,tabs(['Matrix','Ranking','Compare','Annotations'],'Matrix',1152,{'Ranking':'DF10','Compare':'DF15','Annotations':'DF11'}));
const controls=row('Result controls',1152,16);add(controls,tag('P(ΔPSI ≥ 1.0)','brand'),btn('Raw ΔPSI score','secondary','ST08'),btn('Table view','secondary','DF10'),btn('Model card','subtle','DF16'));add(s.content,controls);
const data=row('Matrix and selected substitutions',1152,24);data.counterAxisAlignItems='MIN';const hm=card('Effect matrix',696);add(hm,sectionTitle('Effect matrix','Rows: position + WT · columns: mutant amino acid.',648),matrix(),legend());const rank=card('Selected substitution and shortlist',432);const best=cells[0];
add(rank,tag('RANK 1 OF 532','brand'),txt(best.wt+best.position+best.mut,'Title',384),txt('Tile position '+best.position+' · protein position '+best.protein_position,'Body',384,'muted'),txt('P(ΔPSI ≥ 1.0) = '+best.prob.toFixed(3),'Mono',384),txt('Raw predicted ΔPSI = +'+best.raw.toFixed(3),'Mono',384),tag('Top 10% in this tile','success'),btn('Add to shortlist','primary','DF10'),rule(384),txt('Top substitutions','Heading',384),table(['#','Change','P(ΔPSI ≥ 1)','Raw ΔPSI'],cells.slice(0,7).map(c=>[String(c.rank),c.wt+c.position+c.mut,c.prob.toFixed(3),(c.raw>=0?'+':'')+c.raw.toFixed(3)]),384,[48,80,144,112]),btn('View all 532 rows','secondary','DF10'),txt('Illustrative design values; not model output.','Caption',384,'muted'));
add(data,hm,rank);add(s.content,data,actionRow(btn('Export CSV / JSON','primary','ST02'),btn('Save to project','secondary','ST01')));finish(s);
}
// Read-back evidence is returned with this write, avoiding a separate inventory call.
const result=summary();
const counts={},fontFamilies=new Set(),imageNodes=[];
for(const s of screensCreated){const root=await figma.getNodeByIdAsync(s.root);for(const n of root.findAll(()=>true)){counts[n.type]=(counts[n.type]||0)+1;if(n.type==='TEXT')fontFamilies.add(n.fontName.family);if('fills' in n&&Array.isArray(n.fills)&&n.fills.some(f=>f.type==='IMAGE'))imageNodes.push({id:n.id,name:n.name});}}
return {...result,validation:{nodeTypes:counts,fontFamilies:[...fontFamilies],expectedFonts:['Roboto','Roboto Mono'],imageNodes,heatmap:{rows:28,columns:20,scoredCells:cells.length,wildTypeCells:28},fixture:'Illustrative design values; not model output'}};
