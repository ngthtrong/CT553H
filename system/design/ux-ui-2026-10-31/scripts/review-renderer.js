function cssColor(p){if(!p)return'transparent';const c=p.color;return'rgb('+[c.r,c.g,c.b].map(x=>Math.round(x*255)).join(',')+')';}
function dom(n){
const e=document.createElement('div');e.className='vnode '+(n.type==='TEXT'?'vtext':'');e.dataset.node=n.id;e.dataset.name=n.name;e.dataset.type=n.type;n.el=e;
e.style.width=n.width+'px';e.style.flexShrink='0';e.style.boxSizing='border-box';e.style.position='relative';
if(n.type==='TEXT'){
 const t=typography[n.textStyle];Object.assign(e.style,{fontFamily:'"'+t[3]+'",sans-serif',fontSize:t[0]+'px',lineHeight:t[1]+'px',fontWeight:t[2],whiteSpace:'pre-wrap',overflowWrap:'break-word',color:cssColor(n.fills[0]),textAlign:(n.textAlignHorizontal||'LEFT').toLowerCase()});e.textContent=n.characters;
}else if(n.type==='SVG'){
 e.innerHTML=n.svg;e.style.height=n._height+'px';const svg=e.querySelector('svg');if(svg){svg.setAttribute('width','100%');svg.setAttribute('height','100%');svg.style.display='block';}
}else{
 if(n.layoutMode!=='NONE'){e.style.display='flex';e.style.flexDirection=n.layoutMode==='HORIZONTAL'?'row':'column';e.style.gap=n.itemSpacing+'px';e.style.alignItems=n.counterAxisAlignItems==='CENTER'?'center':n.counterAxisAlignItems==='MAX'?'flex-end':'flex-start';e.style.justifyContent=n.primaryAxisAlignItems==='CENTER'?'center':'flex-start';}
 if(n.layoutSizingVertical!=='HUG')e.style.height=n._height+'px';
 e.style.padding=[n.paddingTop,n.paddingRight,n.paddingBottom,n.paddingLeft].map(x=>x+'px').join(' ');
 e.style.background=cssColor(n.fills[0]);if(n.strokes.length){if(n.dashPattern)e.style.border=(n.strokeWeight||1)+'px dashed '+cssColor(n.strokes[0]);else e.style.boxShadow='inset 0 0 0 '+(n.strokeWeight||1)+'px '+cssColor(n.strokes[0]);}e.style.borderRadius=(n.cornerRadius||0)+'px';
 if(n.type==='ELLIPSE')e.style.borderRadius='50%';
 for(const c of n.children)e.appendChild(dom(c));
}
if(n.flex)e.style.flex='1 1 auto';
if(n.isScreen){e.classList.add('artboard');e.style.height='auto';e.style.minHeight=n._height+'px';e.style.alignItems='stretch';}
if(n.isSidebar){e.style.height='auto';e.style.alignSelf='stretch';}
if(n.clip){e.style.overflowX=n.scrollX?'auto':'hidden';e.style.overflowY='hidden';}
if(n.name==='Accessible table')e.setAttribute('role','table');
if(n.name==='Table header'||n.name.startsWith('Table row '))e.setAttribute('role','row');
if(n.name.startsWith('Column/'))e.setAttribute('role',n.parent?.name==='Table header'?'columnheader':'cell');
if(n.type==='TEXT'&&['Title','Display','Heading'].includes(n.textStyle)){e.setAttribute('role','heading');e.setAttribute('aria-level',n.textStyle==='Heading'?'2':'1');}
if(n.scrollX){for(const label of e.querySelectorAll('[data-name^="Position "] > .vtext:first-child,[data-name="Amino acid columns"] > .vtext:first-child')){label.style.position='sticky';label.style.left='0';label.style.zIndex='2';label.style.background=palette[n.mode].bg;}}
if(n.target&&!n.disabled){e.classList.add('hotspot');e.setAttribute('role','button');e.setAttribute('aria-label',n.name.replace('Action/',''));e.tabIndex=0;e.addEventListener('click',ev=>{ev.stopPropagation();show(n.target);});e.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();show(n.target);}});}
if(n.disabled){e.setAttribute('aria-disabled','true');e.style.opacity='.65';}
if(n.cell){e.title=n.name;e.setAttribute('role','gridcell');e.setAttribute('aria-label',n.name);e.tabIndex=-1;e.addEventListener('focus',()=>{e.style.outline='3px solid #096B57';document.getElementById('cell-status').textContent=n.name;});e.addEventListener('blur',()=>{e.style.outline='';});}
if(n.name.startsWith('Heatmap')){e.setAttribute('role','grid');e.setAttribute('aria-label','28 positions by 20 mutant amino acids');const cs=e.querySelectorAll('[role=gridcell]');if(cs.length)cs[0].tabIndex=0;e.addEventListener('keydown',ev=>{const a=[...e.querySelectorAll('[role=gridcell]')],i=a.indexOf(document.activeElement),d={ArrowRight:1,ArrowLeft:-1,ArrowDown:20,ArrowUp:-20}[ev.key];if(d&&i>=0){ev.preventDefault();a[i].tabIndex=-1;const j=Math.max(0,Math.min(a.length-1,i+d));a[j].tabIndex=0;a[j].focus();}});}
return e;
}
let currentId='DF01';
const registry=Object.fromEntries(screensCreated.map(s=>[s.id,s]));
function resizeCanvas(){const host=document.getElementById('canvas'),r=host.firstElementChild;if(!r)return;const available=document.getElementById('stage').clientWidth-32,scale=Math.min(1,available/r.offsetWidth);r.style.transformOrigin='top left';r.style.transform='scale('+scale+')';host.style.width=r.offsetWidth*scale+'px';host.style.height=r.offsetHeight*scale+'px';document.getElementById('zoom').textContent=Math.round(scale*100)+'%';}
function show(id,update=true){const s=registry[id];if(!s)return;currentId=id;const root=allNodes.get(s.root),host=document.getElementById('canvas');host.replaceChildren(dom(root));document.getElementById('screen-select').value=id;document.getElementById('screen-name').textContent=id+' · '+s.title;if(update)location.hash=id;requestAnimationFrame(resizeCanvas);window.scrollTo({top:0});}
function spec(n,parentRect=null){const r=n.el.getBoundingClientRect(),parent=parentRect||r;return{id:n.id,name:n.name,type:n.type,role:n.role||null,bind:n.bind||null,mode:n.mode,target:n.target||null,disabled:!!n.disabled,x:Math.round((r.x-parent.x)*100)/100,y:Math.round((r.y-parent.y)*100)/100,width:Math.round(r.width*100)/100,height:Math.round(r.height*100)/100,layoutMode:n.layoutMode,padding:[n.paddingTop,n.paddingRight,n.paddingBottom,n.paddingLeft],gap:n.itemSpacing,align:n.counterAxisAlignItems||'MIN',justify:n.primaryAxisAlignItems||'MIN',radius:n.cornerRadius||0,fills:n.fills,strokes:n.strokes,strokeWeight:n.strokeWeight||1,dash:n.dashPattern||null,text:n.characters??null,textStyle:n.textStyle||null,svg:n.svg||null,clip:!!n.clip,scrollX:!!n.scrollX,children:n.children.map(c=>spec(c,r))};}
async function exportSpecs(){
 await document.fonts.ready;const stage=document.getElementById('measure');const out=[];
 for(const s of screensCreated){const root=allNodes.get(s.root);stage.replaceChildren(dom(root));await new Promise(resolve=>requestAnimationFrame(resolve));out.push({...s,node:spec(root)});}
 stage.replaceChildren();show(currentId,false);
 return{format:'degron-footprint-editable-design-v1',date:'2026-10-31',status:'Design proposal. Not runtime acceptance or scientific validation.',fixture:'ILLUSTRATIVE DESIGN VALUES; NOT MODEL OUTPUT',liveFigmaStatus:'Foundations/components only. MCP quota blocked screen creation.',palette,typography,screens:out};
}
window.exportDesign=exportSpecs;
function init(){const select=document.getElementById('screen-select');for(const [name,prefix]of [['Desktop screens','DF'],['States and dialogs','ST'],['Responsive','M'],['Direction and UX','UX']]){const g=document.createElement('optgroup');g.label=name;for(const s of screensCreated.filter(s=>s.id.startsWith(prefix))){const o=document.createElement('option');o.value=s.id;o.textContent=s.id+' · '+s.title;g.appendChild(o);}select.appendChild(g);}select.addEventListener('change',()=>show(select.value));for(const b of document.querySelectorAll('[data-go]'))b.addEventListener('click',()=>show(b.dataset.go));window.addEventListener('resize',resizeCanvas);window.addEventListener('hashchange',()=>show(location.hash.slice(1),false));show(registry[location.hash.slice(1)]?location.hash.slice(1):'DF01',false);document.fonts.ready.then(resizeCanvas);window.reviewReady=true;}
init();
