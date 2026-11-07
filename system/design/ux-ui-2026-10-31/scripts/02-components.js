const page=await figma.getNodeByIdAsync(CONFIG.foundation.pages.kit);
await figma.setCurrentPageAsync(page);
const properties={bannerLabel:{},bannerBody:{}};
function component(name,w,h,dir='VERTICAL',bg='surface'){
  if(page.children.some(n=>n.name===name))throw new Error('Component already exists: '+name);
  const c=track(figma.createComponent());c.name=name;c.description='Degron Footprint v0.2. Reusable research-workspace element; native editable layers, bound design tokens.';c.layoutMode=dir;c.resize(w,h);c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';gap(c,8);fill(c,bg);pad(c,16);radius(c,12);return c;
}
function prop(c,node,name){const key=c.addComponentProperty(name,'TEXT',node.characters);node.componentPropertyReferences={characters:key};return key;}
const statC=component('Stat',272,108);
const value=txt('98','Title',240),label=txt('Full windows','BodyStrong',240),detail=txt('28 residues · step 23','Caption',240,'muted');
add(statC,value,label,detail);gap(statC,2);stroke(statC);statC.x=80;statC.y=180;componentMap.Stat=statC;
properties.statValue=prop(statC,value,'Value');properties.statLabel=prop(statC,label,'Label');properties.statDetail=prop(statC,detail,'Detail');
for(const [i,key,title,body,bg,color] of [
  [0,'Domain','Measured in-domain','Tile and source evidence remain attached.','accentSoft','accent'],
  [1,'Evidence','Development OOF benchmark, not external validation','Assay event only. Not a probability of disease.','soft','muted'],
  [2,'Warning','Unknown / borderline / training observation','Interpret the uncertainty before reading the scores.','warning','warningInk'],
  [3,'Danger','Out-of-domain override','An explicit override is recorded in the snapshot and exports.','danger','dangerInk']
]){
  const c=component(key,1152,84,'VERTICAL',bg);gap(c,4);c.x=400;c.y=180+i*120;const l=txt(title,'BodyStrong',1120,color),b=txt(body,'Caption',1120,'ink');add(c,l,b);l.layoutSizingHorizontal='FILL';b.layoutSizingHorizontal='FILL';properties.bannerLabel[key]=prop(c,l,'Label');properties.bannerBody[key]=prop(c,b,'Body');componentMap[key]=c;
}
const nav=component('Sidebar',224,1060,'VERTICAL','sidebar');nav.x=1660;nav.y=180;pad(nav,20);nav.itemSpacing=24;nav.cornerRadius=0;
const brand=row('Brand',184,12);add(brand,icon('dna',28,'accentText'),txt('Degron\nFootprint','BodyStrong',134,'accentText'));
add(nav,brand,txt('RESEARCH WORKSPACE','Label',184,'sidebarText'));
const navlist=al('Primary navigation',184,'VERTICAL',8);
for(const [name,ico] of [['Projects','folder'],['New analysis','flask-conical'],['Model','activity'],['Data & sources','database']]){
  const r=row('Nav/'+name,184,12);pad(r,12);radius(r,8);add(r,icon(ico,20,'sidebarText'),txt(name,'BodyStrong',128,'sidebarText'));add(navlist,r);
}
add(nav,navlist);
const spacer=al('Flexible space',184,'VERTICAL',0);add(nav,spacer);spacer.layoutSizingVertical='FILL';
const foot=al('Workspace information',184,'VERTICAL',12);
add(foot,txt('LOCAL INSTANCE','Label',184,'sidebarText'),txt('Your work stays on\nthis computer.','Body',184,'sidebarText'),txt('m3-ext4.0-platt-v1','MonoSmall',184,'sidebarText'),txt('Development benchmark','Caption',184,'sidebarText'));
add(nav,foot);componentMap.Sidebar=nav;
const seq=component('SequenceStrip',688,94,'VERTICAL','soft');seq.x=80;seq.y=720;add(seq,txt('28 residues · tile positions 1–28','Caption',656,'muted'),txt(CONFIG.fixture.sequence,'Mono',656));componentMap.SequenceStrip=seq;
const progress=component('JobProgress',688,110);progress.x=800;progress.y=720;add(progress,txt('Processing 66 of 98 tiles','BodyStrong',656),txt('62 succeeded · 3 refused · 1 failed · 32 pending/running','Caption',656,'muted'));const trackBar=row('Progress track',656,0,'soft');trackBar.resize(656,8);trackBar.layoutSizingVertical='FIXED';radius(trackBar,8);const segment=track(figma.createRectangle());segment.resize(442,8);fill(segment,'accent');add(trackBar,segment);add(progress,trackBar);componentMap.JobProgress=progress;
const heading=txt('Components / foundations','Title',1100);heading.x=80;heading.y=80;
return {...summary(),properties,componentIds:Object.fromEntries(Object.entries(componentMap).map(([k,v])=>[k,v.id]))};
