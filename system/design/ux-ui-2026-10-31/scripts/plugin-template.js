/* Native Figma development plugin. No network or MCP tools.
 * DESIGN is embedded by build_package.py from the reviewed editable node spec.
 * Existing work is retained; every import is placed in a newly named section. */
figma.showUI(`<html><style>body{font:14px/1.5 Arial;padding:18px;color:#183b2c}button{background:#096b57;color:white;border:0;border-radius:8px;padding:12px 16px;font-size:14px;cursor:pointer}small{color:#52675b}#status{white-space:pre-wrap;margin-top:12px}</style><h2>Degron Footprint · UX/UI</h2><p>Import the reviewed screens as editable Figma layers. No MCP calls are used.</p><p><small>Design fixtures only. Existing frames are preserved. This import does not implement the application.</small></p><button id="build">Build editable screens</button><div id="status">Ready.</div><script>document.getElementById('build').onclick=()=>{document.getElementById('build').disabled=true;parent.postMessage({pluginMessage:{type:'build'}},'*')};onmessage=e=>{if(e.data.pluginMessage)document.getElementById('status').textContent=e.data.pluginMessage.message};</script></html>`,{width:440,height:360});
let running=false;
figma.ui.onmessage=async msg=>{
 if(msg.type!=='build'||running)return;running=true;
 const run='UX-2026-10-31-'+new Date().toISOString().replace(/[^0-9]/g,'').slice(0,14);
 const created=[],styles={},tokens={},components=new Map(),sceneMap=new Map(),pendingLinks=[],warnings=[];
 const report=s=>figma.ui.postMessage({message:s});
 try{
  report('Loading product fonts…');
  const available=await figma.listAvailableFontsAsync();
  for(const family of ['Roboto','Roboto Mono'])for(const style of ['Regular','Medium']){
   if(!available.some(f=>f.fontName.family===family&&f.fontName.style===style))throw new Error('Required font unavailable: '+family+' '+style);
   await figma.loadFontAsync({family,style});
  }
  function page(name){let p=figma.root.children.find(p=>p.name===name);if(!p){p=figma.createPage();p.name=name;}return p;}
  const coverPage=page('00 · Direction & UX'),screenPage=page('01 · Research workspace'),kitPage=page('02 · Components & states');
  const localCollections=await figma.variables.getLocalVariableCollectionsAsync();
  const localVariables=await figma.variables.getLocalVariablesAsync();
  const rgb=h=>({r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255,a:1});
  for(const [mode,pal]of Object.entries(DESIGN.palette)){
   const name='DF · '+(mode==='light'?'Light':'Dark');let c=localCollections.find(c=>c.name===name);if(!c){c=figma.variables.createVariableCollection(name);c.renameMode(c.modes[0].modeId,'Value');}
   tokens[mode]={};for(const [role,value]of Object.entries(pal)){let v=localVariables.find(v=>v.variableCollectionId===c.id&&v.name==='color/'+role);if(!v){v=figma.variables.createVariable('color/'+role,c,'COLOR');v.setValueForMode(c.modes[0].modeId,rgb(value));v.scopes=['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'];v.setVariableCodeSyntax('WEB','var(--df-'+(mode==='dark'?'dark-':'')+'color-'+role+')');}tokens[mode][role]=v;}
  }
  let geo=localCollections.find(c=>c.name==='DF · Geometry');if(!geo){geo=figma.variables.createVariableCollection('DF · Geometry');geo.renameMode(geo.modes[0].modeId,'Value');}
  const nums={};function numberToken(kind,value){const name=kind+'/'+value;if(nums[name])return nums[name];let v=localVariables.find(v=>v.variableCollectionId===geo.id&&v.name===name);if(!v){v=figma.variables.createVariable(name,geo,'FLOAT');v.setValueForMode(geo.modes[0].modeId,value);v.scopes=[kind==='space'?'GAP':'CORNER_RADIUS'];v.setVariableCodeSyntax('WEB','var(--df-'+kind+'-'+value+')');}return nums[name]=v;}
  const existingStyles=await figma.getLocalTextStylesAsync();
  for(const [name,t]of Object.entries(DESIGN.typography)){let st=existingStyles.find(s=>s.name==='DF/'+name);if(!st){st=figma.createTextStyle();st.name='DF/'+name;st.fontName={family:t[3],style:t[2]>=500?'Medium':'Regular'};st.fontSize=t[0];st.lineHeight={unit:'PIXELS',value:t[1]};}styles[name]=st;}
  function paints(items){return items.map(p=>{let paint={type:'SOLID',color:{r:p.color.r,g:p.color.g,b:p.color.b}};if(p.token&&tokens[p.mode]?.[p.token])paint=figma.variables.setBoundVariableForPaint(paint,'color',tokens[p.mode][p.token]);return paint;});}
  function geometry(n,s){n.resize(Math.max(.01,s.width),Math.max(.01,s.height));if('fills'in n)n.fills=paints(s.fills);if('strokes'in n){n.strokes=paints(s.strokes);n.strokeWeight=s.strokeWeight||1;if(s.dash)n.dashPattern=s.dash;}
   if('cornerRadius'in n&&s.radius){n.cornerRadius=s.radius;if([4,8,12,20,999].includes(s.radius))for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])n.setBoundVariable(k,numberToken('radius',s.radius));}
   if(s.layoutMode!=='NONE'&&'layoutMode'in n){n.layoutMode=s.layoutMode;n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';n.itemSpacing=s.gap||0;if([0,4,8,12,16,24,32,40].includes(s.gap))n.setBoundVariable('itemSpacing',numberToken('space',s.gap));const fields=['paddingTop','paddingRight','paddingBottom','paddingLeft'];fields.forEach((k,i)=>{n[k]=s.padding[i];if([0,4,8,12,16,24,32,40].includes(s.padding[i]))n.setBoundVariable(k,numberToken('space',s.padding[i]));});n.counterAxisAlignItems=s.align==='CENTER'?'CENTER':s.align==='MAX'?'MAX':'MIN';n.primaryAxisAlignItems=s.justify==='CENTER'?'CENTER':'MIN';}
   if('clipsContent'in n)n.clipsContent=!!s.clip;
   if(s.scrollX&&'overflowDirection'in n)n.overflowDirection='HORIZONTAL_SCROLLING';
  }
  function signature(s){return s.type+':'+(s.textStyle||'')+'['+s.children.map(signature).join(',')+']';}
  function at(s,path){for(const i of path)s=s.children[i];return s;}
  function instanceLinks(s,n){if(s.target&&!s.disabled)pendingLinks.push({node:n,target:s.target});if('children'in n)for(let i=0;i<s.children.length;i++){if(n.children[i])instanceLinks(s.children[i],n.children[i]);}}
  let compIndex=0;
  async function render(s,parent,context=null,path=[],bypass=false){
   const isReusable=s.role&&s.type!=='SVG';
   if(isReusable&&!bypass){const key=s.mode+'/'+s.role+'/'+signature(s);let def=components.get(key);
    if(!def){const main=figma.createComponent();created.push(main.id);main.name='DF/'+s.role+' / '+s.mode+' / '+components.size;main.description='Original editable component for '+run+'. Based on the reviewed BA v0.2 design. Fixtures are illustrative.';kitPage.appendChild(main);main.x=2200+(compIndex%4)*1240;main.y=160+Math.floor(compIndex/4)*1240;compIndex++;geometry(main,s);const ctx={main,props:[],count:0};for(let i=0;i<s.children.length;i++)await render(s.children[i],main,ctx,[i]);def={main,props:ctx.props};components.set(key,def);}
    const inst=def.main.createInstance();created.push(inst.id);inst.name=s.name;parent.appendChild(inst);inst.resize(Math.max(.01,s.width),Math.max(.01,s.height));const overrides={};for(const prop of def.props){const source=at(s,prop.path);if(source&&source.text!==null)overrides[prop.key]=source.text;}if(Object.keys(overrides).length)inst.setProperties(overrides);sceneMap.set(s.id,inst);if(!context)instanceLinks(s,inst);return inst;
   }
   let n;
   if(s.type==='SVG'){n=figma.createNodeFromSvg(s.svg);n.resize(Math.max(.01,s.width),Math.max(.01,s.height));}
   else if(s.type==='TEXT'){n=figma.createText();const t=DESIGN.typography[s.textStyle];await n.setTextStyleIdAsync(styles[s.textStyle].id);n.characters=s.text;n.fills=paints(s.fills);n.resize(Math.max(.01,s.width),Math.max(.01,s.height));n.textAutoResize='HEIGHT';}
   else if(s.type==='RECTANGLE'){n=figma.createRectangle();geometry(n,s);}
   else if(s.type==='ELLIPSE'){n=figma.createEllipse();geometry(n,s);}
   else{n=figma.createFrame();geometry(n,s);}
   created.push(n.id);n.name=s.name;parent.appendChild(n);if(parent.type==='PAGE'||parent.layoutMode==='NONE'){n.x=s.x;n.y=s.y;}
   if(context&&n.type==='TEXT'){const name=s.bind||'Text '+(++context.count);const key=context.main.addComponentProperty(name,'TEXT',s.text);n.componentPropertyReferences={characters:key};context.props.push({key,path:[...path]});if(parent.layoutMode&&parent.layoutMode!=='NONE'){n.layoutSizingHorizontal='FILL';}}
   sceneMap.set(s.id,n);if(s.target&&!s.disabled&&!context)pendingLinks.push({node:n,target:s.target});
   if(s.type!=='SVG'&&s.type!=='TEXT')for(let i=0;i<s.children.length;i++)await render(s.children[i],n,context,[...path,i]);return n;
  }
  // Independent placement cursors prevent overlap even for unusually tall states.
  const columns={screen:{x:80,y:160,rowH:0,col:0},cover:{x:80,y:160,rowH:0,col:0}};const frameMap={},imported=[];
  let i=0;
  for(const item of DESIGN.screens){const board=item.id.startsWith('UX'),p=board?coverPage:screenPage,c=columns[board?'cover':'screen'];const n=await render(item.node,p);n.name=run+' / '+item.id+' · '+item.title;n.x=c.x;n.y=c.y;c.rowH=Math.max(c.rowH,n.height);c.col++;if(c.col===3){c.x=80;c.y+=c.rowH+160;c.col=0;c.rowH=0;}else c.x+=1540;frameMap[item.id]=n;imported.push(n);i++;if(i%3===0){report('Built '+i+' / '+DESIGN.screens.length+' screens…');await new Promise(resolve=>setTimeout(resolve,0));}}
  report('Connecting prototype routes…');
  for(const link of pendingLinks){const target=frameMap[link.target];if(!target){warnings.push('Unresolved target '+link.target);continue;}await link.node.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',destinationId:target.id,navigation:'NAVIGATE',transition:null,resetScrollPosition:true}]}]);}
  await figma.setCurrentPageAsync(screenPage);figma.currentPage.selection=[frameMap.DF01];figma.viewport.scrollAndZoomIntoView([frameMap.DF01]);
  try{screenPage.flowStartingPoints=[{nodeId:frameMap.DF01.id,name:run+' / Research workspace'}];}catch(e){warnings.push('Set prototype start manually: DF01');}
  report('Created '+imported.length+' editable frames and '+components.size+' reusable component definitions.\n'+pendingLinks.length+' prototype hotspots processed.\n'+(warnings.length?warnings.join('\n'):'No unresolved prototype targets.')+'\n\nReview in Figma: text wrapping, component overrides, matrix sizing and target links. This native import has not been pre-verified through MCP.');
 }catch(error){report('Import stopped: '+error.message+'\nExisting work is retained. Partial import nodes carry '+run+' where available. Inspect this run before trying again.');running=false;}
};
