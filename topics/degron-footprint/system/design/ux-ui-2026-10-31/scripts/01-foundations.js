// Figma Plugin API. Run via use_figma; the caller records the returned ledger.
// Helper pattern adapted from figma-generate-library createVariableCollection.js.
const createdNodeIds = [], variableIds = [], styleIds = [];
const oldPages = figma.root.children;
const cover = oldPages.find(p => p.id === '0:1');
cover.name = '00 · Direction & UX';
function page(name) {
  const existing = figma.root.children.find(p => p.name === name);
  if (existing) return existing;
  const p = figma.createPage(); p.name = name; createdNodeIds.push(p.id); return p;
}
const screens = page('01 · Research workspace');
const kit = page('02 · Components & states');
await figma.setCurrentPageAsync(kit);
await Promise.all([
  ...['Regular','Medium','SemiBold','Bold'].map(style => figma.loadFontAsync({family:'Roboto', style})),
  ...['Regular','Medium'].map(style => figma.loadFontAsync({family:'Roboto Mono', style})),
  figma.loadFontAsync({family:'Inter',style:'Regular'})
]);
const imports = await Promise.all([
  figma.variables.importVariableByKeyAsync('a4865545b526a5b3399a512667f40c9efe0c2fc4'),
  figma.variables.importVariableByKeyAsync('cf92d4e8c6a5a5ed82f024d47d11c21d5162ac3c'),
  figma.variables.importVariableByKeyAsync('395870afebb3397e858358930ffdd69a5ec0f73d'),
  figma.variables.importVariableByKeyAsync('16bc6f84b6e7e20e4234ef79030ee580ec0f4505'),
  figma.variables.importVariableByKeyAsync('15bb1c0f339146e931cf0dc15f89ed57dcbd907e'),
  figma.variables.importVariableByKeyAsync('be3115966ea99eef888c9f25751b54695c7e88d2'),
  figma.variables.importVariableByKeyAsync('9e82491aff6fe809fe71856da5612db502221455'),
  figma.importStyleByKeyAsync('6dc22e0ddb735b3b4fdf3afecd5762a1c9bc42ed')
]);
const [sdsBg,sdsText,sdsBorder,space16,space8,space24,radius8,shadow] = imports;
function rgb(hex) { return {r:parseInt(hex.slice(1,3),16)/255,g:parseInt(hex.slice(3,5),16)/255,b:parseInt(hex.slice(5,7),16)/255,a:1}; }
async function collection(name) {
  const existing=(await figma.variables.getLocalVariableCollectionsAsync()).find(c=>c.name===name);
  if (existing) return existing;
  const c=figma.variables.createVariableCollection(name); c.renameMode(c.modes[0].modeId,'Value'); return c;
}
const light = await collection('DF · Light'), dark = await collection('DF · Dark'), geometry = await collection('DF · Geometry');
const locals=await figma.variables.getLocalVariablesAsync();
function token(coll,name,type,value,scopes) {
  const v=locals.find(v=>v.name===name&&v.variableCollectionId===coll.id)||figma.variables.createVariable(name,coll,type);
  v.scopes=scopes; v.setValueForMode(coll.modes[0].modeId,value);
  v.setVariableCodeSyntax('WEB','var(--df-'+(coll===dark?'dark-':'')+name.replaceAll('/','-')+')'); variableIds.push(v.id); return v;
}
const palettes = {
  light:{bg:'#F5F7F6',surface:null,ink:null,muted:'#566660',line:'#DCE4E0',accent:'#096B57',accentSoft:'#E7F3ED',accentText:'#FFFFFF',sidebar:'#142A24',sidebarText:'#B9CDC5',sidebarActive:'#24493D',warning:'#FFF5DE',warningInk:'#795000',danger:'#FFF0EE',dangerInk:'#A72B24',violet:'#62558B',soft:'#EEF2EF'},
  dark:{bg:'#111B17',surface:'#192720',ink:'#E9F1EC',muted:'#B4C6BA',line:'#3C5146',accent:'#8BDBB7',accentSoft:'#203E30',accentText:'#103526',sidebar:'#101A15',sidebarText:'#B4C6BA',sidebarActive:'#254333',warning:'#3B3015',warningInk:'#FFDD8F',danger:'#40221F',dangerInk:'#FFBCB4',violet:'#C5B7EE',soft:'#213329'}
};
const colorVars={light:{},dark:{}};
for(const [mode,pal] of Object.entries(palettes)) {
  const c=mode==='light'?light:dark;
  for(const [name,hex] of Object.entries(pal)) {
    const isText=['ink','muted','accentText','sidebarText','warningInk','dangerInk'].includes(name);
    const scopes=isText?['TEXT_FILL','SHAPE_FILL']:name==='line'?['STROKE_COLOR','SHAPE_FILL']:['FRAME_FILL','SHAPE_FILL','STROKE_COLOR'];
    const value=hex?rgb(hex):{type:'VARIABLE_ALIAS',id:name==='surface'?sdsBg.id:sdsText.id};
    colorVars[mode][name]=token(c,'color/'+name,'COLOR',value,scopes).id;
  }
}
const geometryVars={};
for(const [name,value] of Object.entries({'space/4':4,'space/12':12,'space/32':32,'space/40':40,'radius/12':12,'radius/20':20,'radius/999':999})) geometryVars[name]=token(geometry,name,'FLOAT',value,[name.startsWith('space')?'GAP':'CORNER_RADIUS']).id;
geometryVars['space/8']=space8.id;geometryVars['space/16']=space16.id;geometryVars['space/24']=space24.id;geometryVars['radius/8']=radius8.id;
const textStyles={};
for(const [name,size,lineHeight,style,family] of [
  ['Display',40,48,'Medium','Roboto'],['Title',28,36,'Medium','Roboto'],['Heading',20,28,'Medium','Roboto'],['Body',14,20,'Regular','Roboto'],['BodyStrong',14,20,'Medium','Roboto'],['Large',16,24,'Regular','Roboto'],['Caption',12,16,'Regular','Roboto'],['Label',12,16,'Medium','Roboto'],['Mono',13,20,'Regular','Roboto Mono'],['MonoSmall',11,16,'Regular','Roboto Mono']
]) {
  const localStyles=await figma.getLocalTextStylesAsync();
  const s=localStyles.find(s=>s.name==='DF/'+name)||figma.createTextStyle();s.name='DF/'+name;s.fontName={family,style};s.fontSize=size;s.lineHeight={unit:'PIXELS',value:lineHeight};textStyles[name]=s.id;styleIds.push(s.id);
}
return {createdNodeIds,mutatedNodeIds:[cover.id],variableIds,styleIds,pages:{cover:cover.id,screens:screens.id,kit:kit.id},colors:colorVars,geometry:geometryVars,textStyles,shadowStyleId:shadow.id,sourceAssets:{sdsBg:sdsBg.id,sdsText:sdsText.id,sdsBorder:sdsBorder.id},themeStrategy:'Starter plan: separate Light and Dark one-mode collections',fonts:['Roboto','Roboto Mono']};
