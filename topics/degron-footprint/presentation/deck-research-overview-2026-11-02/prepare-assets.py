"""Create standalone research figures and a hashed evidence bundle; no training/test-T access."""
from pathlib import Path
import hashlib
import json
import shutil
import urllib.request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())
R = TOPIC/'research'
ASSETS = HERE/'assets'
ASSETS.mkdir(exist_ok=True)
VENDOR = HERE/'vendor'
VENDOR.mkdir(exist_ok=True)
source_hashes = {}
downloads = []

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def read(name):
    p = R/name
    source_hashes[name] = digest(p)
    return json.loads(p.read_text(encoding='utf8'))

def download(url, name):
    p = VENDOR/name
    if not p.exists():
        with urllib.request.urlopen(url, timeout=60) as response:
            p.write_bytes(response.read())
    downloads.append(dict(path='vendor/'+name, url=url, sha256=digest(p)))

for weight in ['Regular', 'SemiBold']:
    download(f'https://raw.githubusercontent.com/google/fonts/main/ofl/bevietnampro/BeVietnamPro-{weight}.ttf', f'be-vietnam-pro-{weight.lower()}.ttf')
download('https://raw.githubusercontent.com/google/fonts/main/ofl/bevietnampro/OFL.txt','font-license.txt')
download('https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js','chart.umd.js')
download('https://cdn.jsdelivr.net/npm/chart.js@4.4.1/LICENSE.md','chart-license.md')
old = TOPIC/'presentation/deck-2026-10-16/assets'
for name in ['fam188a.gif', 'fam188a-poster.png']:
    shutil.copy2(old/name, ASSETS/name)
    downloads.append(dict(path='assets/'+name, source=str((old/name).relative_to(TOPIC)), sha256=digest(ASSETS/name),
        attribution='Nikolakhs, I-TASSER predicted protein fold of Fam188a, Wikimedia Commons, CC BY-SA 3.0',
        url='https://commons.wikimedia.org/wiki/File:I-TASSER_predicted_protein_fold_of_Fam188a.gif'))

for p in VENDOR.glob('*.ttf'):
    font_manager.fontManager.addfont(p)
plt.rcParams.update({'font.family':['Be Vietnam Pro','DejaVu Sans'],'font.size':16,'axes.spines.top':False,
    'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#D6DFD3',
    'text.color':'#193A2B','axes.labelcolor':'#617267','xtick.color':'#617267',
    'ytick.color':'#193A2B','savefig.transparent':True,'svg.fonttype':'path',
    'axes.titleweight':'semibold','axes.grid':False})
GREEN='#18974C'; DARK='#0A5032'; CORAL='#C76242'; BLUE='#477CA7'; MUTED='#A9B7A8'
files=[]

def save(fig, name):
    p=ASSETS/(name+'.svg');fig.savefig(p, bbox_inches='tight', pad_inches=.16);plt.close(fig)
    files.append(p.name)

def bars(name, labels, values, xlabel, colors=None, max_x=None, fmt='.3f'):
    fig,ax=plt.subplots(figsize=(11,4.6))
    y=np.arange(len(labels));cols=colors or [GREEN]*len(labels)
    ax.barh(y,values,color=cols,height=.48)
    ax.set_yticks(y,labels);ax.invert_yaxis();ax.tick_params(axis='y',length=0,pad=12)
    ax.set_xlabel(xlabel,loc='right',labelpad=12)
    ax.set_xlim(0,max_x or max(values)*1.20)
    ax.xaxis.grid(True,color='#E3E8DF');ax.set_axisbelow(True)
    for i,v in enumerate(values):ax.text(v+ax.get_xlim()[1]*.018,i,format(v,fmt).replace('.',','),va='center',weight='semibold',fontsize=17)
    fig.tight_layout();save(fig,name)

def forest(name,labels,deltas,cis,xlabel):
    fig,ax=plt.subplots(figsize=(10,3.4 if len(labels)<4 else 4.7))
    for i,(v,ci) in enumerate(zip(deltas,cis)):
        color=GREEN if ci[1]<0 else BLUE if ci[0]>0 else CORAL
        ax.errorbar(v,i,xerr=[[v-ci[0]],[ci[1]-v]],fmt='o',color=color,capsize=6,markersize=10,lw=3)
    ax.axvline(0,color=MUTED,lw=1.4,ls='--');ax.set_yticks(range(len(labels)),labels)
    ax.invert_yaxis();ax.tick_params(axis='y',length=0,pad=12);ax.set_xlabel(xlabel,labelpad=10)
    ax.xaxis.grid(True,color='#E3E8DF');fig.tight_layout();save(fig,name)

analysis=read('kaggle-roadmap-2026-10-31/output-analysis.json')
details=read('kaggle-roadmap-2026-10-31/output-analysis-details.json')
model=read('residue-task-derisk-2026-10-15/model.json')
g2=read('g2-saturation-2026-10-18/results.json')
deg=read('r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json')
cal=read('calibration-p6-2026-10-22/results.json')
hif=read('slide-figures-2026-10-15/example-matrix.json')
replicate=read('full-data-audit/replicate-audit.json')
satquality=read('full-data-audit/saturation-matrix.json')
clinical=read('variant-coverage-2026-10-15/enrichment.json')
pre=read('pretrain-p3-2026-10-22/results.json')
curve=read('learning-curve-2026-10-22/results.json')
recluster=read('recluster-sensitivity-2026-10-22/results.json')
extra=read('r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json')
gate=read('r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json')

def metric(recipe,key='mae'):
    return analysis['recipes'][recipe]['ensemble']['all'][key]

context=model['scanning']['macro_auroc']
bars('context',['Phép thay + thành phần peptide','Thêm thành phần lân cận','Thêm thứ tự trong lân cận'],
    [context[k]['mean'] for k in ['M0_composition_only','M2_plus_window_composition','M3_plus_ordered_context']],
    'AUROC trong peptide · cao hơn tốt hơn',[MUTED,BLUE,GREEN],1)
arms=['ordered-w5-'+x for x in 'ABCDE']
bars('training-range',['Chỉ PSI ≤ 3','Chỉ PSI ≤ 4','Chỉ PSI ≤ 5','Toàn dải PSI','Toàn dải, cân bằng'],
    [metric(k) for k in arms],'MAE (PSI) · thấp hơn tốt hơn',[MUTED,BLUE,MUTED,GREEN,DARK],.56)
q1=[analysis['contrasts'][f'ordered-w5-{x} minus ordered-w5-B; mae'] for x in 'DE']
forest('training-ci',['Toàn dải so với chỉ PSI ≤ 4','Cân bằng so với chỉ PSI ≤ 4'],
    [x['delta'] for x in q1],[x['ci_adjusted'] for x in q1],'Chênh lệch MAE · CI 97,5% đã điều chỉnh')
fig,ax=plt.subplots(figsize=(10,4.6))
for arm,label,color in [('B','Chỉ PSI ≤ 4',BLUE),('D','Toàn dải',GREEN),('E','Toàn dải, cân bằng',CORAL)]:
    values=[analysis['recipes']['ordered-w5-'+arm]['ensemble']['strata'][s]['mae'] for s in ['le3','gt3_le4','gt4_le5','gt5']]
    ax.plot(range(4),values,'o-',color=color,lw=3,ms=8,label=label)
ax.set_xticks(range(4),['PSI ≤ 3','3 < PSI ≤ 4','4 < PSI ≤ 5','PSI > 5']);ax.set_ylabel('MAE (PSI)')
ax.set_ylim(.27,.55);ax.yaxis.grid(True,color='#E3E8DF');ax.legend(frameon=False,fontsize=13,loc='upper center',ncol=3)
fig.tight_layout();save(fig,'strata')

labels=['Ridge ngữ cảnh','Ridge + ESM','Chọn bằng validation']
keys=['ordered-w5-D','esm2_35m-context-D','nested-family-selection']
bars('esm-linear',labels,[metric(k,'auroc_plus') for k in keys], 'AUROC dương · toàn dải PSI',[MUTED,GREEN,BLUE],1)
bars('heads',['One-hot + CNN','ESM + pointwise','ESM + CNN','ESM + nhiều cửa sổ'],
    [metric(k) for k in ['onehot-cnn-D','esm2_35m-pointwise-D','esm2_35m-cnn-D','esm2_35m-mcnn-D']],
    'MAE (PSI) · cùng train toàn dải',[MUTED,BLUE,GREEN,DARK],.47,fmt='.4f')
c=analysis['contrasts']['esm2_35m-cnn-D minus esm2_35m-pointwise-D; mae']
forest('cnn-ci',['CNN so với pointwise'],[c['delta']],[c['ci95']],'Chênh lệch MAE · CI 95% mô tả')
c=details['contrasts']['esm2_35m-mcnn-E minus esm2_35m-cnn-D; mae']
forest('mcnn-ci',['Nhiều cửa sổ, cân bằng\nso với CNN, toàn dải'],[c['delta']],[c['ci95']],'Chênh lệch MAE · CI 95% mô tả')
bars('transfer',['CNN học trực tiếp','CNN khởi tạo từ scanning','CNN từ trung bình replicate'],
    [metric(k) for k in ['cnn-transfer-scratch-D','cnn-transfer-dpsi_rep1-D','cnn-transfer-dpsi_rep12_mean-D']],
    'MAE (PSI) · cùng kiến trúc one-hot',[MUTED,GREEN,BLUE],.46,fmt='.4f')
cc=[details['contrasts']['cnn-transfer-dpsi_rep1-D minus cnn-transfer-scratch-D; mae; '+s] for s in ['scan20','other360']]
forest('transfer-pairs',['20 kiểu thay có trong scanning','360 kiểu thay còn lại'],[v['delta'] for v in cc],[v['ci95'] for v in cc],
    'Chênh lệch MAE so với học trực tiếp · CI 95% mô tả')
refs=deg['references_macro_auroc']
bars('degformer',['Ridge cùng miền đánh giá','Degformer sạch cụm','ΔPAP'],
    [refs['ridge_ext4.0'],deg['macro_auroc_ensemble'],refs['DeltaPAP']],
    'AUROC · đánh giá trên 91 peptide',[GREEN,BLUE,MUTED],1)
fig,ax=plt.subplots(figsize=(9,4.5));xx=np.arange(3);w=.32
for j,(key,label,color) in enumerate([('ordered-w5-D','Ridge ngữ cảnh',MUTED),('esm2_35m-cnn-D','ESM + CNN',GREEN)]):
    vals=[metric(key,'precision_plus_'+s+'_eligible_macro')*100 for s in ['0.05','0.1','0.2']]
    ax.bar(xx+(j-.5)*w,vals,w,color=color,label=label)
    for x,v in zip(xx+(j-.5)*w,vals):ax.text(x,v+1.5,f'{v:.1f}%'.replace('.',','),ha='center',fontsize=15)
ax.set_xticks(xx,['Top 5%','Top 10%','Top 20%']);ax.set_ylabel('Precision dương (%)');ax.set_ylim(0,75)
ax.legend(frameon=False,loc='upper right',fontsize=13);ax.yaxis.grid(True,color='#E3E8DF');ax.set_axisbelow(True)
fig.tight_layout();save(fig,'utility')
fig,ax=plt.subplots(figsize=(9,4.3))
for key,label,color in [('ordered-w5-D','Ridge',MUTED),('esm2_35m-cnn-D','ESM + CNN',GREEN)]:
    vals=details['fold_mae'][key];ax.plot(range(1,6),list(vals.values()),'o-',label=label,lw=3,color=color,ms=9)
ax.set_xticks(range(1,6));ax.set_xlabel('Nhóm kiểm tra ngoài');ax.set_ylabel('MAE (PSI)');ax.set_ylim(.34,.45)
ax.legend(frameon=False);ax.yaxis.grid(True,color='#E3E8DF');fig.tight_layout();save(fig,'folds')
fig,ax=plt.subplots(figsize=(6.5,4.5))
ax.plot([0,.65],[0,.65],ls='--',color=MUTED,lw=1.5)
rr=cal['metrics']['platt']['reliability'];ax.plot([v['mean_pred'] for v in rr],[v['obs_rate'] for v in rr],'o-',color=GREEN,lw=3,ms=7)
ax.set_xlim(0,.65);ax.set_ylim(0,.65);ax.set_xlabel('Xác suất dự đoán');ax.set_ylabel('Tần suất quan sát');ax.grid(color='#E3E8DF')
fig.tight_layout();save(fig,'calibration')

aa=hif['aa_order'];matrix=np.array([[row.get(a,np.nan) if row.get(a) is not None else np.nan for row in hif['matrix']] for a in aa])
fig,ax=plt.subplots(figsize=(13,5.3));cmap=LinearSegmentedColormap.from_list('psi',['#477CA7','#F2F4EE','#E9976B','#AE432E'])
im=ax.imshow(matrix,aspect='auto',cmap=cmap,norm=TwoSlopeNorm(vmin=-.6,vcenter=0,vmax=3.2),interpolation='nearest')
ax.set_xticks(range(28),list(hif['sequence']),fontsize=14);ax.xaxis.tick_top();ax.set_yticks(range(20),list(aa),fontsize=14)
ax.tick_params(length=0);ax.set_xlabel('Vị trí trong peptide HIF1A',labelpad=12)
ax.set_xticks(np.arange(-.5,28,1),minor=True);ax.set_yticks(np.arange(-.5,20,1),minor=True);ax.grid(which='minor',color='#F6F7F2',linewidth=1)
ax.add_patch(plt.Rectangle((8.5,-.5),5,20,fill=False,edgecolor=DARK,lw=2.5))
cb=fig.colorbar(im,ax=ax,fraction=.028,pad=.03);cb.set_label('ΔPSI đo được',fontsize=13);cb.ax.tick_params(labelsize=11)
fig.tight_layout();save(fig,'hif-measured')

seeds=analysis['recipes']['esm2_35m-cnn-D']['seed_mae']
bars('seed-ensemble',['Khởi tạo 17','Khởi tạo 29','Khởi tạo 43','Trung bình dự đoán'],
    list(seeds.values())+[metric('esm2_35m-cnn-D')],'MAE (PSI)',[MUTED,MUTED,MUTED,GREEN],.46,fmt='.4f')
bars('brier',['Tần suất nền','Ridge + hiệu chuẩn'],[cal['metrics']['const']['brier'],cal['metrics']['platt']['brier']],
    'Brier · thấp hơn tốt hơn',[MUTED,GREEN],.15,fmt='.4f')
fig,ax=plt.subplots(figsize=(9,4.3))
curves=details['learning_curve'];values=[curves[k]['mean_seed_mae'] for k in curves]
ax.plot([25,50,75,100],values,'o-',color=GREEN,lw=3,ms=9);ax.set_xticks([25,50,75,100]);ax.set_xlabel('% nhóm train của một lượt fit');ax.set_ylabel('MAE trung bình các seed')
ax.yaxis.grid(True,color='#E3E8DF');fig.tight_layout();save(fig,'learning-curve')

fig,ax=plt.subplots(figsize=(11,4.6));labels=['Ridge ngữ cảnh','ESM + pointwise','ESM + CNN','ESM + nhiều cửa sổ','Scanning → CNN']
ks=['ordered-w5-D','esm2_35m-pointwise-D','esm2_35m-cnn-D','esm2_35m-mcnn-E','cnn-transfer-dpsi_rep1-D']
for k,label,c in zip(ks,labels,[MUTED,BLUE,GREEN,DARK,CORAL]):
    x=metric(k);y=metric(k,'auroc_plus');ax.scatter(x,y,s=160,color=c);ax.annotate(label,(x,y),xytext=(8,8),textcoords='offset points',fontsize=13)
ax.set_xlabel('MAE (PSI) · thấp hơn tốt hơn');ax.set_ylabel('AUROC dương · cao hơn tốt hơn');ax.set_xlim(.376,.43);ax.set_ylim(.819,.865);ax.grid(color='#E3E8DF')
fig.tight_layout();save(fig,'tradeoff')

human_names={
 'ordered-w5-D':'Ridge · toàn dải','ordered-w5-B':'Ridge · chỉ PSI ≤ 4','ordered-w5-E':'Ridge · cân bằng',
 'esm2_35m-cnn-D':'ESM + CNN · toàn dải','esm2_35m-cnn-B':'ESM + CNN · chỉ PSI ≤ 4',
 'esm2_35m-mcnn-E':'ESM + nhiều cửa sổ · cân bằng','esm2_35m-pointwise-D':'ESM + pointwise · toàn dải',
 'onehot-cnn-D':'One-hot + CNN · toàn dải','cnn-transfer-dpsi_rep1-D':'Scanning → CNN · toàn dải',
 'esm2_35m-context-D':'Ridge + ESM · toàn dải','nested-family-selection':'Chọn bằng validation'}
explorer=[dict(name=human_names[k],mae=metric(k),auroc=metric(k,'auroc_plus'),ap=metric(k,'auprc_plus')) for k in human_names]
(HERE/'data.js').write_text('window.DECK_DATA='+json.dumps(dict(explorer=explorer,hif=hif),ensure_ascii=False)+';\n',encoding='utf8')
evidence=dict(source_hashes=source_hashes,assets=downloads,figures=files,
    dataset_identity=analysis['data_identity'],source_manifest_sha256=analysis['source_manifest_sha256'],
    scientific_status='development; no automatic model promotion or gate closure',
    main_population=dict(peptides=235,protein_groups=221,cells=122412),
    chart_explorer=explorer,
    definitions=dict(mae='peptide macro, PSI units',plus='measured delta PSI >= 1',minus='measured delta PSI <= -1',
       ci='Q1 two contrasts: adjusted 97.5%; other added comparisons descriptive 95% protein-group bootstrap',
       plotting='standalone SVG figures generated with Matplotlib; no external test predictions computed'),
    generation_script_sha256=digest(Path(__file__)))
(HERE/'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'asset-notices.md').write_text('# Asset notices\n\nFonts: Be Vietnam Pro, SIL OFL; see vendor/font-license.txt.\n\nChart.js 4.4.1, MIT; see vendor/chart-license.md.\n\nProtein GIF and its existing poster: Nikolakhs, I-TASSER predicted protein fold of Fam188a, Wikimedia Commons, CC BY-SA 3.0. https://commons.wikimedia.org/wiki/File:I-TASSER_predicted_protein_fold_of_Fam188a.gif . Unmodified illustration of a protein fold, not HIF1A or a measured degron structure. The GIF remains under its original license.\n\nAll process diagrams are original schematic SVG/CSS. Research figures are generated from the local evidence sources listed in evidence.json.\n',encoding='utf8')
print(f'Prepared {len(files)} research figures; {len(source_hashes)} hashed result sources.')
