#!/usr/bin/env python3
"""Publication figures from reviewed JSON; illustrative data are marked explicitly."""
from pathlib import Path
import json
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np

HERE=Path(__file__).resolve().parents[1]
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
OUT=HERE/'assets/figures';OUT.mkdir(parents=True,exist_ok=True)
D=json.loads((HERE/'evidence.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.titleweight':'bold','pdf.fonttype':42,
                     'savefig.bbox':'tight','axes.labelcolor':'#243C46','text.color':'#243C46'})
TEAL='#167D8D';BLUE='#3464A0';GOLD='#C18D26';CORAL='#BA5260';GREY='#78858D'
manifest=[]
def save(name,fig,kind,source):
    fig.savefig(OUT/f'{name}.pdf');fig.savefig(OUT/f'{name}.png',dpi=180)
    plt.close(fig);manifest.append(dict(name=name,kind=kind,source=source))

# A deliberately simple, labelled teaching example, never a measured experiment.
fig,ax=plt.subplots(figsize=(8,3.3));x=np.arange(1,7)
ax.bar(x-.18,[0,50,50,0,0,0],.36,label='WT minh họa: PSI = 2,5',color=BLUE)
ax.bar(x+.18,[0,0,0,50,50,0],.36,label='Mutant minh họa: PSI = 4,5',color=TEAL)
ax.set(xlabel='Bin (GFP/DsRed tăng từ trái sang phải)',ylabel='Count đã chuẩn hóa',xticks=x,
       title='VÍ DỤ TỰ ĐẶT: trung bình có trọng số của sáu bin')
ax.set_ylim(0,68);ax.legend(frameon=False,loc='upper left',fontsize=9);fig.tight_layout();save('psi-worked-example',fig,'illustrative','Teaching-only counts, not study data')

h=D['hif'];aa=h['aa_order'];m=np.array([[r.get(a,np.nan) if r.get(a) is not None else np.nan for r in h['matrix']] for a in aa])
fig,ax=plt.subplots(figsize=(10.6,5));cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#D9DDE0')
im=ax.imshow(m,aspect='auto',cmap=cmap,norm=TwoSlopeNorm(vmin=-1,vcenter=0,vmax=3.2))
ax.set_xticks(range(28),[f'{i+1}\n{a}' for i,a in enumerate(h['sequence'])],fontsize=7)
ax.set_yticks(range(20),list(aa));ax.set(xlabel='Vị trí và amino acid WT trong peptide',ylabel='Amino acid thay vào',
 title='NHÃN ĐO ĐÃ LƯU — HIF1A tile 25 (không phải dự đoán)')
cb=fig.colorbar(im,ax=ax,pad=.025);cb.set_label('ΔPSI (mutant − WT)');fig.tight_layout();save('hif-measured',fig,'measured','NC-18; historical selected example, not independent validation')

fig,ax=plt.subplots(figsize=(8.4,3.4));curve=D['historical']['curve']['ridge'];levels=['25','50','75','100']
ax.plot([25,50,75,100],[curve[k]['macro_auroc_ensemble'] for k in levels],'o-',color=BLUE,lw=2)
ax.axhline(curve['ext']['macro_auroc_ensemble'],color=TEAL,ls='--',label='Train mở ngưỡng ≤4; outer-test giữ nguyên')
ax.set(xlabel='% nhóm train trong miền ban đầu',ylabel='AUROC macro (ensemble)',xticks=[25,50,75,100],
 title='BENCHMARK LỊCH SỬ — 91 peptide outer-test');ax.legend(frameon=False,fontsize=8);ax.grid(axis='y',alpha=.2)
fig.tight_layout();save('historical-learning-curve',fig,'measured','NC-04; stored ensemble metrics')

def forest(name,rows,axis_label,title,source):
 fig,ax=plt.subplots(figsize=(10,3.6))
 for i,(label,delta,ci,style) in enumerate(rows):
  color=TEAL if ci[1]<0 else BLUE if ci[0]>0 else CORAL
  ax.errorbar(delta,i,xerr=[[delta-ci[0]],[ci[1]-delta]],fmt='o',capsize=4,color=color,lw=2)
  ax.text(ax.get_xlim()[1],i,'',fontsize=7)
 ax.axvline(0,color=GREY,ls='--');ax.set_yticks(range(len(rows)),[x[0] for x in rows]);ax.invert_yaxis()
 ax.set(xlabel=axis_label,title=title);ax.grid(axis='x',alpha=.2);fig.tight_layout();save(name,fig,'measured',source)
r=D['historical']['r6_contrasts'];rows=[]
for label,key in [('Ridge ±5 − ±3 (họ m=3)','A_ridge_W5_vs_W3'),('ESM+mCNN − ridge (phép chính)','P_esm35_mcnn_vs_ridge'),('ESM+mCNN − one-hot mCNN (phụ)','S1_esm35_mcnn_vs_oh_mcnn')]:
 v=r[key];rows.append((label,v['delta'],v['ci_adj'],'stored'))
forest('r6-intervals',rows,'Chênh AUROC: dương có lợi cho mô hình đứng trước','R6: điểm ước lượng phải đọc cùng khoảng tin cậy','NC-14; family-adjusted where recorded; secondary descriptive')

recipes=D['fullpsi']['recipes']
chosen=[('W5, train PSI≤4','ordered-w5-B'),('W5, toàn dải','ordered-w5-D'),('W5, cân bằng','ordered-w5-E'),
        ('One-hot CNN','cnn-transfer-scratch-D'),('ESM + pointwise','esm2_35m-pointwise-D'),('ESM + CNN','esm2_35m-cnn-D'),
        ('ESM + mCNN cân bằng','esm2_35m-mcnn-E'),('CNN + scanning pretrain','cnn-transfer-dpsi_rep1-D')]
fig,ax=plt.subplots(figsize=(9,4.4));values=[recipes[k]['ensemble']['all']['mae'] for _,k in chosen]
ax.barh(range(len(chosen)),values,color=[GREY,GREY,GREY,BLUE,TEAL,TEAL,TEAL,BLUE],height=.58)
ax.set_yticks(range(len(chosen)),[x[0] for x in chosen]);ax.invert_yaxis();ax.set_xlim(0,.49)
for i,v in enumerate(values):ax.text(v+.004,i,f'{v:.5f}',va='center',fontsize=9)
ax.set(xlabel='MAE macro theo peptide (PSI; thấp hơn tốt hơn)',title='FULL-PSI — cùng 235 peptide, ensemble ba seed');fig.tight_layout();save('fullpsi-mae',fig,'measured','NC-16; selected recipes, no local data')

c=D['fullpsi']['contrasts'];rows=[]
for label,a,b in [('W5 toàn dải − hạn chế (97,5%)','ordered-w5-D','ordered-w5-B'),('W5 cân bằng − hạn chế (97,5%)','ordered-w5-E','ordered-w5-B'),('ESM CNN − pointwise (95%)','esm2_35m-cnn-D','esm2_35m-pointwise-D'),('Scanning pretrain − scratch (95%)','cnn-transfer-dpsi_rep1-D','cnn-transfer-scratch-D'),('Quality weighting − gốc (95%)','sat-quality-D','sat-only-D')]:
 v=next(v for v in c.values() if v['a']==a and v['b']==b and v['metric']=='mae' and v['stratum'] is None)
 rows.append((label,v['delta'],v['ci_adjusted'] if v['multiplicity']>1 else v['ci95'],'stored'))
forest('fullpsi-intervals',rows,'Chênh MAE: âm có lợi cho mô hình đứng trước','FULL-PSI — hai phép chính điều chỉnh; phần còn lại mô tả','NC-16; 5,000 protein-group bootstrap draws')

fig,ax=plt.subplots(figsize=(8.4,3.8));strata=['le3','gt3_le4','gt4_le5','gt5'];x=np.arange(4)
for i,(key,label,color) in enumerate([('ordered-w5-B','Train PSI≤4',GREY),('ordered-w5-D','Toàn dải',BLUE),('ordered-w5-E','Toàn dải cân bằng',TEAL)]):
 ax.bar(x+(i-1)*.25,[recipes[key]['ensemble']['strata'][s]['mae'] for s in strata],.24,label=label,color=color)
ax.set_xticks(x,['≤3 (91 peptide)','(3;4] (85)','(4;5] (36)','>5 (23)']);ax.set(ylabel='MAE macro',xlabel='PSI(WT) của test',title='Lợi ích không phân bố đều giữa các miền WT-PSI');ax.legend(frameon=False,fontsize=8);fig.tight_layout();save('psi-strata',fig,'measured','NC-16; identical stratum cohorts between arms')

fig,ax=plt.subplots(figsize=(8.4,3.8));lc=D['fullpsi']['learning_curve'];keys=['ordered-w5-D-fraction0.25','ordered-w5-D-fraction0.5','ordered-w5-D-fraction0.75','ordered-w5-D'];x=[25,50,75,100]
ax.plot(x,[lc[k]['mean_seed_mae'] for k in keys],'o-',color=BLUE,label='Trung bình metric từng seed')
ax.plot(x,[lc[k]['ensemble_mae'] for k in keys],'s--',color=TEAL,label='Metric sau ensemble dự đoán')
ax.set(xlabel='% nhóm train của từng thành viên',ylabel='MAE macro',xticks=x,title='V3: ensemble 25% không phải một model chỉ thấy 25% dữ liệu');ax.legend(frameon=False,fontsize=8);ax.grid(axis='y',alpha=.2);fig.tight_layout();save('ensemble-learning-curve',fig,'measured','NC-17; post-hoc; training subset union can exceed nominal fraction')

fig,axs=plt.subplots(1,2,figsize=(10,3.9));cal=D['calibration'];rel=cal['platt']['reliability']
axs[0].plot([0,1],[0,1],'--',color=GREY,label='Lý tưởng y=x');axs[0].plot([r['mean_pred'] for r in rel],[r['obs_rate'] for r in rel],'o-',color=TEAL,label='Platt OOF');axs[0].set(xlabel='Xác suất dự đoán trung bình',ylabel='Tần suất dương quan sát',title='Reliability (miền lịch sử)');axs[0].legend(frameon=False,fontsize=8)
names=['const','raw','platt'];axs[1].bar(['Tần suất nền','Raw clip [0;1]','Platt'],[cal[k]['brier'] for k in names],color=[GREY,CORAL,TEAL]);axs[1].set(ylabel='Brier (thấp hơn tốt hơn)',title='ECE thấp chưa đủ chứng minh kỹ năng');axs[1].tick_params(axis='x',labelsize=8)
fig.tight_layout();save('calibration',fig,'measured','NC-08; historical restricted baseline, not full-PSI calibration')

screen=ROOT/'topics/degron-footprint/system/design/workspace-ui-v2/previews/result-light.png'
if screen.exists():
 shutil.copyfile(screen,OUT/'workspace-fixture.png')
 manifest.append(dict(name='workspace-fixture',kind='synthetic-ui',source=str(screen.relative_to(ROOT))))
(HERE/'figure-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'Generated {len(manifest)} figure assets; each has a data-status label')
