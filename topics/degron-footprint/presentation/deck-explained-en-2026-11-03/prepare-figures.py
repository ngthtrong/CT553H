"""Render English labels from exactly the same saved research values."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap,TwoSlopeNorm

HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'data/README.md').exists())
BASE=TOPIC/'research/kaggle-roadmap-2026-10-31'
analysis=json.loads((BASE/'output-analysis.json').read_text())
details=json.loads((BASE/'output-analysis-details.json').read_text())
hif=json.loads((TOPIC/'research/slide-figures-2026-10-15/example-matrix.json').read_text())
for p in (HERE/'vendor').glob('*.ttf'):font_manager.fontManager.addfont(p)
plt.rcParams.update({'font.family':['Be Vietnam Pro','DejaVu Sans'],'font.size':16,'axes.spines.top':False,
    'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#D6DFD3',
    'text.color':'#193A2B','axes.labelcolor':'#617267','xtick.color':'#617267','ytick.color':'#193A2B',
    'savefig.transparent':True,'svg.fonttype':'none','svg.hashsalt':'degron-explained-en-2026-11-03'})
GREEN='#18974C';DARK='#0A5032';CORAL='#C76242';BLUE='#477CA7';MUTED='#A9B7A8'
provenance={}
def metric(recipe,key='mae'):return analysis['recipes'][recipe]['ensemble']['all'][key]
def save(fig,name,values):
    p=HERE/'assets'/f'{name}.svg'
    fig.savefig(p,bbox_inches='tight',pad_inches=.16,metadata={'Date':None});plt.close(fig)
    p.write_text('\n'.join(x.rstrip() for x in p.read_text().splitlines())+'\n')
    provenance[name]={'values':values,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def bars(name,labels,values,colors,xlabel,xmax):
    fig,ax=plt.subplots(figsize=(11,4.6))
    ax.barh(range(len(values)),values,height=.48,color=colors)
    ax.set_yticks(range(len(values)),labels);ax.invert_yaxis();ax.tick_params(axis='y',length=0,pad=12)
    ax.set_xlabel(xlabel,loc='right',labelpad=12);ax.set_xlim(0,xmax)
    ax.xaxis.grid(True,color='#E3E8DF');ax.set_axisbelow(True)
    for i,v in enumerate(values):ax.text(v+xmax*.018,i,f'{v:.4f}',va='center',weight='semibold',fontsize=17)
    fig.tight_layout();save(fig,name,values)

keys=['ordered-w5-'+s for s in 'ABCDE']
bars('training-range',['WT PSI ≤ 3','WT PSI ≤ 4','WT PSI ≤ 5','Full PSI range','Full range, balanced'],
     [metric(k) for k in keys],[MUTED,BLUE,MUTED,GREEN,DARK],'MAE (PSI) · lower is better',.56)

fig,ax=plt.subplots(figsize=(10,4.6));strata={}
for arm,label,col in [('B','WT PSI ≤ 4',BLUE),('D','Full range',GREEN),('E','Balanced',CORAL)]:
    vals=[analysis['recipes']['ordered-w5-'+arm]['ensemble']['strata'][s]['mae'] for s in ['le3','gt3_le4','gt4_le5','gt5']]
    strata[arm]=vals;ax.plot(range(4),vals,'o-',color=col,lw=3,ms=8,label=label)
ax.set_xticks(range(4),['PSI ≤ 3','3 < PSI ≤ 4','4 < PSI ≤ 5','PSI > 5']);ax.set_ylabel('MAE (PSI)')
ax.set_ylim(.27,.55);ax.yaxis.grid(True,color='#E3E8DF');ax.legend(frameon=False,fontsize=13,loc='upper center',ncol=3)
fig.tight_layout();save(fig,'strata',strata)

contrast=details['contrasts']['esm2_35m-mcnn-E minus esm2_35m-cnn-D; mae']
delta=contrast['delta'];lo,hi=contrast['ci95']
fig,ax=plt.subplots(figsize=(10,3.4))
ax.errorbar(delta,0,xerr=[[delta-lo],[hi-delta]],fmt='o',color=CORAL,capsize=6,markersize=10,lw=3)
ax.axvline(0,color=MUTED,lw=1.4,ls='--');ax.set_yticks([0],['Balanced mCNN\nminus full-range CNN'])
ax.tick_params(axis='y',length=0,pad=12);ax.set_xlabel('Difference in MAE · descriptive 95% CI',labelpad=10)
ax.xaxis.grid(True,color='#E3E8DF');fig.tight_layout();save(fig,'mcnn-ci',{'delta':delta,'ci95':[lo,hi]})

keys=['cnn-transfer-scratch-D','cnn-transfer-dpsi_rep1-D','cnn-transfer-dpsi_rep12_mean-D']
bars('transfer',['CNN from scratch','Scanning pretrain, rep. 1','Scanning pretrain, mean reps.'],[metric(k) for k in keys],
     [MUTED,GREEN,BLUE],'MAE (PSI) · matched one-hot CNN architecture',.46)

aa=hif['aa_order']
matrix=np.array([[row.get(a,np.nan) if row.get(a) is not None else np.nan for row in hif['matrix']] for a in aa])
fig,ax=plt.subplots(figsize=(13,5.3))
cmap=LinearSegmentedColormap.from_list('psi',['#477CA7','#F2F4EE','#E9976B','#AE432E'])
im=ax.imshow(matrix,aspect='auto',cmap=cmap,norm=TwoSlopeNorm(vmin=-.6,vcenter=0,vmax=3.2),interpolation='nearest')
ax.set_xticks(range(28),list(hif['sequence']),fontsize=14);ax.xaxis.tick_top();ax.set_yticks(range(20),list(aa),fontsize=14)
ax.tick_params(length=0);ax.set_xlabel('Position in the HIF1A peptide',labelpad=12)
ax.set_xticks(np.arange(-.5,28,1),minor=True);ax.set_yticks(np.arange(-.5,20,1),minor=True);ax.grid(which='minor',color='#F6F7F2',linewidth=1)
ax.add_patch(plt.Rectangle((8.5,-.5),5,20,fill=False,edgecolor=DARK,lw=2.5))
cb=fig.colorbar(im,ax=ax,fraction=.028,pad=.03);cb.set_label('Measured ΔPSI',fontsize=13);cb.ax.tick_params(labelsize=11)
fig.tight_layout();save(fig,'hif-measured',{'source':'research/slide-figures-2026-10-15/example-matrix.json','valid_cells':int(np.isfinite(matrix).sum())})
(HERE/'figure-data.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Rendered five English research figures from unchanged saved values.')
