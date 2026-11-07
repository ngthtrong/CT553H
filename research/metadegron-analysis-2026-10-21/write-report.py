"""Render Vietnamese reports from the measured JSON; no third-party data copied."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'data'/'README.md').exists())
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())

def load(n):return json.loads((HERE/n).read_text())
def write(n,t): (HERE/n).write_text(t.strip()+'\n')
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+['| '+' | '.join(str(v).replace('|','/') for v in r)+' |' for r in rows])

def main():
    d=load('dataset-audit.json');o=load('overlap-audit.json');b=load('composition-baseline.json');x=load('safe-x-reproduction.json');c=load('clusters.json');ri=load('repository-inventory.json');mr=load('manual-label-review.json')
    refs='[dataset-audit.json](dataset-audit.json), sinh bởi [audit_dataset.py](audit_dataset.py)'
    current='[current-topic-evidence.json](current-topic-evidence.json); đọc lại JSON thí nghiệm cũ, không huấn luyện lại G2'
    write('README.md',f'''# MetaDegron và degron-footprint — audit 21/10/2026

1. [ĐỌC-MÃ] Nhãn chính là ΔPSI thực nghiệm = PSI(mutant) − PSI(WT); dương nghĩa là reporter bền hơn. [Nguồn pipeline](../residue-task-derisk-2026-10-15/residue_data.py).
2. [ĐỌC-MÃ] Một dự đoán ứng với một phép thay acid amin tại một vị trí; gộp thành bản đồ vị trí × acid amin. [Runner G2](../g2-saturation-2026-10-18/run.py).
3. [ĐO] Bộ quét có 2.624 footprint theo bộ lọc lịch sử; không phải số protein độc lập. {current}.
4. [ĐO] Bão hòa thô có 249 peptide; benchmark G2 còn 91 peptide / 89 cụm / 47.847 ô. {current}.
5. [ĐỌC-MÃ] Chỉ số chính hiện hành: AUROC mức ô, macro theo peptide, ô dương khi ΔPSI ≥ 1. [Protocol](../g2-saturation-2026-10-18/PROTOCOL.md).
6. [ĐỌC-MÃ] G2 dùng 5 outer fold theo cụm protein MMseqs2 id30/cov80; cov50 dùng kiểm độ nhạy. [Runner](../g2-saturation-2026-10-18/run.py).
7. [ĐO] Seed 17/29/43 là seed huấn luyện trên cùng outer partition; bootstrap 5.000 lần theo cụm. {current}.
8. [ĐO] Ridge M3 0,8082; ΔPAP 0,7693; Degformer retrain 0,7500, riêng đối chứng sau chỉ một seed. {current}.
9. [ĐO] CRISPR có 31 screen, 10 E3 được gán; chỉ 1 E3 có ít nhất 5 peptide. {current}.
10. [DIỄN GIẢI] G2 còn mở: lượng nhãn chưa kiểm trực tiếp, tiền huấn luyện mức túi chưa chứng minh, so pretrained Degformer sạch cụm chưa xong; định vị cần GVHD chấp thuận. [Trạng thái hiện hành](../topic-decision.md).

## Kết luận điều hành

- [ĐO] MetaDegron cung cấp 302 dòng curate / 240 accession; 227 dòng HUMAN, tập thuộc tính X chỉ 212 dương tính. {refs}.
- [ĐO] Tái tính MetaDegron-X được AUC **0,9670** bằng đọc cây số an toàn; **8/20** dương tính kiểm tra nằm trong bảng thuộc tính fitting được cung cấp. Đây không phải kết quả GPS. [safe-x-reproduction.json](safe-x-reproduction.json), [safe-predict-x.py](safe-predict-x.py).
- [ĐO] Theo cách sampling/split của script X, **91–111** dòng test mỗi fold có cùng tọa độ với train. Logistic thành phần cov80 khoảng **0,728–0,731**, ngữ cảnh 29 aa **0,737–0,747**; chưa đạt ngưỡng shortcut mạnh đăng ký trước. [composition-baseline.json](composition-baseline.json).
- [ĐO] Giao đúng vùng với bộ quét có footprint: **2 peptide**; bão hòa: **1** (map được 248/249); CRISPR: **0** (map đủ). Số này khác giao cùng protein và khác giao với tile. [overlap-audit.json](overlap-audit.json).
- [DIỄN GIẢI] “21 E3” là lựa chọn motif gắn với classifier dùng chung; dữ liệu không tự tạo ra 21 lớp E3 có nhãn độc lập. Sau lọc HUMAN, vùng trùng và cụm G2, chỉ **2 nhóm motif** còn ≥5 mẫu; lọc bảo thủ mọi protein tham chiếu còn **1**. [overlap-audit.json](overlap-audit.json), [mã/đánh giá](model-and-evaluation.md).
- [ĐỀ XUẤT] Định vị MetaDegron là công cụ bổ sung về motif/E3 và đối chiếu ứng dụng. Ưu tiên đường cong học, prior motif và tiền huấn luyện có kiểm soát; chưa nhập nhãn nhị phân vào thang ΔPSI. [Đề xuất và tiêu chí chốt](recommendations.md).

## Mục lục

- [Nguồn, phiên bản, quyền sử dụng và truy cập](source-inventory.md) · [manifest SHA-256](source-manifest.json) · [cây toàn repo](repository-tree.md).
- [Audit dữ liệu](dataset-audit.md) · [schema mọi bảng](table-schemas.md) · [kiểm nguồn mẫu](manual-label-review.md).
- [Ứng dụng và đầu ra](application-and-outputs.md) · [mô hình/đánh giá](model-and-evaluation.md) · [kiểm từng nhận định cũ](claims-verification.md).
- [So sánh và vị thế](comparison-and-positioning.md) · [khuyến nghị và tối đa năm prompt tiếp theo](recommendations.md).
- [Đăng ký trước](PREREGISTRATION.md) · [kiểm chéo](VALIDATION.md) · [kết quả kiểm](validation.json).

## Việc không làm được và vì sao

[CHƯA XÁC MINH] Chưa chạy MetaDegron-D trên GPS hoặc ma trận đột biến. SeqVec/embedding tải lớn có endpoint trả HTTP 200, **không được gọi là mất trọng số**; bản tải thử dừng ở giới hạn dung lượng của fetcher và không giữ payload. Runtime cũ TensorFlow/Keras/allennlp chưa có trong môi trường Python hiện tại; mã web và cấu hình checkpoint còn bất nhất cửa sổ. Nhánh X chỉ tái chạy được trên bảng đặc trưng đã chuẩn bị; các tài sản tạo đặc trưng cho protein/đột biến GPS chưa đầy đủ. [code-audit.json](code-audit.json), [source-manifest.json](source-manifest.json), [external-evaluation.json](external-evaluation.json).

[CHƯA XÁC MINH] Đã kiểm truy nguồn mẫu theo protocol, nhưng chưa phân xử đầy đủ thí nghiệm sinh học gốc cho mọi dòng; tỉ lệ nhãn degron sai để `null`. Trang bảng review gốc trả trang hạn chế ELTEnet; không coi HTTP 200 là truy cập được dữ liệu. [manual-label-review.json](manual-label-review.json), [source-manifest.json](source-manifest.json).

[ĐỌC-MÃ] Không gửi chuỗi lên server: Terms.php không có, liên kết chính sách bị 403; vì vậy không thực hiện bước phụ thuộc điều khoản chưa rõ. Chỉ tải trang/tài liệu và ảnh ví dụ sẵn có. [source-manifest.json](source-manifest.json).

## Đề xuất chỉnh sửa file hiện có

[ĐỀ XUẤT] Khi bạn duyệt, sửa `lectures/degron-basics/papers/metadegron-2024.md`: hạ cách gọi “đối thủ trực tiếp nhất”; thay nhận định âm ngẫu nhiên bằng sampled protein segments, tách split D/X, bổ sung HUMAN và nhãn nguồn; sửa mô tả “ghép XGBoost với DNN”, cập nhật kết quả tái tính và các giới hạn. Không sửa file đó trong phiên này.

[ĐỀ XUẤT] Đợt đồng bộ sau nên sửa định vị kiến trúc trong tài liệu lịch sử và tránh câu tuyệt đối về ứng dụng/mức residue. Báo cáo này không đổi `topic-decision.md`, slide, hay trạng thái G2. `data/README.md` được cập nhật theo yêu cầu sổ nguồn gốc.
''')
    write('source-inventory.md',f'''# Kiểm kê nguồn

[ĐO] Repo [BioDataStudy/MetaDegron](https://github.com/BioDataStudy/MetaDegron) ghim `{ri['commit']}`, commit ngày `{ri['commit_date']}`. Có {ri['file_count']} file được git theo dõi, tổng {ri['bytes']:,} byte; gồm {ri['extension_file_counts']['.py']} Python, {ri['notebook_count']} notebook và {ri['extension_file_counts']['.php']} PHP, cùng JavaScript/CSS và tài sản web. Cây đầy đủ: [repository-tree.md](repository-tree.md). [repository-inventory.json](repository-inventory.json), [inventory-sources.py](inventory-sources.py).

[ĐO] Có `models/degron_DL.h5`, `degron_DL.json`, `classifier_XGBoost.pickle`, `uniref50_v2/options.json`; không có file LICENSE trong cây ghim. SHA-256 **mọi file tải giữ lại**, gồm từng bảng và trọng số nhỏ, nằm trong [source-manifest.json](source-manifest.json). Không đưa payload nguồn, hình hoặc checkpoint vào phần git theo dõi. [repository-inventory.json](repository-inventory.json).

[ĐỌC-MÃ] README nêu Python 3.7, TensorFlow 1.15, Keras 2.3.1, allennlp 0.9.0, h5py 2.10.0, protobuf 3.20 và thư viện khoa học; có XGBoost trong mã dù hướng dẫn cài không liệt kê đầy đủ. Không có requirements/environment/setup đóng gói. Danh sách import và vị trí mã: [code-audit.json](code-audit.json). Không chạy lệnh cài đặt của repo.

## Các kênh nguồn đã thử

| Nguồn | Trạng thái và nội dung | Quyền sử dụng đã kiểm |
|---|---|---|
| [Bài báo DOI](https://doi.org/10.1093/bib/bbae519) / [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/) | [ĐO] Publisher trực tiếp 403; PMC HTML và Europe PMC XML đọc được toàn văn | [NGUỒN] Bài ghi CC BY 4.0; nguyên văn tuyên bố nằm trong manifest |
| Supplementary của PMC | [ĐO] URL XLSX lẻ trả challenge HTML dù status 200; ZIP supplementaryFiles của Europe PMC có XLSX thật | [NGUỒN] Thuộc tài liệu kèm bài; quyền các nguồn nhập như ELM cần kiểm riêng |
| GitHub | [ĐO] Clone thành công; dữ liệu/thuộc tính, mã train/predict, checkpoint và web code có sẵn | [CHƯA XÁC MINH] Không có LICENSE; metadata GitHub không thay giấy phép |
| [Server HTTP](http://modinfor.com/MetaDegron/) | [ĐO] Home, Prediction, Tutorial và Download đọc được qua HTTP; HTTPS timeout; Download hiện không có link dữ liệu trong nội dung nhận được | [CHƯA XÁC MINH] Chỉ dẫn chính sách UTHealth trả 403; Terms.php 404; không submit |
| Trọng số SeqVec / all_train_embedding.npy | [ĐO] Hai endpoint README chỉ trả HTTP 200; payload quá giới hạn fetcher nên không giữ bản tải | [CHƯA XÁC MINH] Không có SHA đầy đủ cho file không tải xong; không tuyên bố đã audit object NPY đó |
| Zenodo/Figshare | [NGUỒN] Tra các truy vấn ghi ở discovery-searches.json chưa xác định deposit riêng của MetaDegron | [CHƯA XÁC MINH] Không kết luận không tồn tại |
| [ELM downloads](http://elm.eu.org/downloads.html) | [ĐO] Đọc query protein cho mẫu; endpoint không query chỉ có giới hạn mặc định, không phải toàn CSDL | [NGUỒN] Academic License đọc nguyên văn từ PDF; dùng nghiên cứu nội bộ, không tự suy ra quyền tích hợp/phân phối |
| Bảng review 2017 | [ĐO] HTTP 200 nhưng nội dung báo chỉ ELTEnet được truy cập | [CHƯA XÁC MINH] Không lấy được bảng gốc |
| [DegronMD](https://pmc.ncbi.nlm.nih.gov/articles/PMC10701100/) | [ĐO] XML bài đọc được; trang Download 403 | [NGUỒN] Bài CC BY 4.0; [CHƯA XÁC MINH] quyền toàn bộ dữ liệu web và nguồn nhập |

[ĐO] Bằng chứng truy cập, status, ngày, URL cuối, content validation và lỗi chính xác: [source-manifest.json](source-manifest.json); truy vấn tìm kiếm: [discovery-searches.json](discovery-searches.json). Script [fetch-sources.py](fetch-sources.py) chỉ tải byte, không chạy nội dung. Các file HTML challenge được giữ làm bằng chứng lỗi, không đếm là bảng.

## Từ nguồn đến kết quả

[ĐỌC-MÃ] `data/degron_data.txt` ↔ supplementary S2 là danh sách curate; `annotated_degrons_properties.tsv` là tập con có thuộc tính; background ở `data/` và `supporting_file/` là hai pool khác nhau, không tráo cho nhau. S4 có Positive và Simulated; pool âm thực sự được notebook benchmarking đọc lại là `simulated_degron2.csv`. Danh sách schema và số dòng từng file: [dataset-audit.json](dataset-audit.json), [table-schemas.md](table-schemas.md).

[NGUỒN] S2 trỏ review *Degrons in cancer*, ELM, *Tripartite degrons* và bài Nature Cancer; không có bằng chứng MetaDegron trực tiếp thu nhãn từ DEGRONOPEDIA. DEGRONOPEDIA/DegronMD xuất hiện như tài nguyên được thảo luận. [Toàn văn](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/).

[CHƯA XÁC MINH] Không gán giấy phép mã GitHub từ giấy phép bài báo. Việc đọc và ghi số đếm không đồng nghĩa cho phép phân phối lại bảng gốc hay nhúng regex ELM vào ứng dụng công khai. Chưa nhập nguồn mới vào huấn luyện chính.
''')
    schema_rows=[]
    for name,s in d['schemas'].items():
        schema_rows.append([name,s.get('rows','?'),len(s.get('columns',[])),', '.join(str(z) for z in s.get('columns',[]))])
    write('table-schemas.md','# Schema từng bảng\n\n[ĐO] Tự đọc bảng bằng `audit_dataset.py --stage profile`; kiểu từng cột, missing và exact duplicates ở [dataset-audit.json](dataset-audit.json). Không nạp object NPY hoặc notebook. Các cột được ghi để định nghĩa schema, không sao chép dòng dữ liệu.\n\n'+table(['Bảng','Dòng','Cột','Tên cột'],schema_rows))
    e=o['e3_after_filter']['80']; e50=o['e3_after_filter']['50']
    e3_rows=[[k,e['motif_mapped_unique'][k],e['human_unique'][k],e['human_no_g2_clusters_no_regional_overlap'][k],e['human_no_topic_cluster_no_regional_overlap'][k],e50['human_no_topic_cluster_no_regional_overlap'][k]] for k in e['motif_mapped_unique']]
    base_rows=[]
    for view in ['length','core-frequency','core-count-length','context29-frequency']:
        v=[r for r in b['results'] if r['cov']==80 and r['features']==view];cv=v[0]['group_oof']['bootstrap']['ci95']
        base_rows.append([view,' / '.join(f"{r['group_oof']['auroc']:.4f}" for r in v),f'[{cv[0]:.4f}; {cv[1]:.4f}]'])
    overlap_rows=[]
    for name in ['footprint','saturation','crispr','g2']:
        s=o['datasets'][name];overlap_rows.append([name,s['denominator'],s['same_accession_positive_rows'],s['regional_positive_rows'],s['regional_peptides'],f"{s['psi_low_pairs']} / {s['psi_high_pairs']}",s['pairs_with_measured_important_position']])
    for name in ['voutsinos','larsen']:
        s=o['datasets'][name];overlap_rows.append([name,s['denominator'],'xem JSON',s['regional_positive_rows'],s['regional_tiles'],f"score≥0,5: {s['pairs_score_ge_point5']}; thấp: {s['pairs_score_lt_point5']}",'không có ΔPSI residue'])
    write('dataset-audit.md',f'''# Audit dữ liệu MetaDegron

## Cỡ dữ liệu và đơn vị nhãn

[ĐO] Bảng curate có **302 dòng**, **240 accession**, **241 chuỗi protein phân biệt**, **274 chuỗi motif phân biệt**, **302 khóa accession/start/end** và **31 loại motif/class**. Đây không phải 302 protein, không phải số nhãn ΔPSI, và không phải 31 E3. Cột nguồn có 166 ELM_TP, 93 signal, 16 natcancer, 13 natcomm, 9 natcancer,signal và 5 natcomm,natcancer,signal. {refs}.

[ĐO] S2 và file repo khớp toàn bộ accession và chuỗi degron theo thứ tự. S2 có PMID nguồn nhưng thường là bài tổng hợp/resource, không phải PMID thí nghiệm riêng từng dòng. Không có cột kiểu thí nghiệm/PTM requirement có cấu trúc. Phân bố loài từ hậu tố Entry name: **227 HUMAN, 75 khác**; đây là kiểm metadata, chưa xác minh taxonomy hiện tại từng accession. Tiêu đề S2 nói dữ liệu người nên không được dùng tiêu đề thay phép đếm. {refs}.

[ĐO] Chuỗi báo cáo dài **5–18 aa**, trong khi khoảng tọa độ dài **2–18 aa**. Có **243/302** dòng mà chuỗi cắt theo tọa độ khớp chuỗi báo cáo; cả **302/302** khoảng cắt đều nằm trong chuỗi báo cáo. Các motif ngắn có thêm flank trong chuỗi; không coi mọi chênh độ dài là sai tọa độ. Có **80** accession và **77** chuỗi protein khớp chính xác với `proteins-full.fasta`. {refs}.

[ĐỌC-MÃ] Dòng curate là motif/đoạn gắn với protein, tọa độ 1-based inclusive, nguồn và class; không có nhãn thực nghiệm “mỗi phép thay AA”. `DEGRON=Known-INTERNAL` trong bảng thuộc tính là tên loại record, không phải chuỗi. UniProt hỗ trợ join accession nhưng phải kiểm isoform/chuỗi; một accession có nhiều chuỗi trong bản nguồn nên không join chỉ bằng số dòng.

[ĐO] Tập X có **212 dòng dương / 158 protein**, toàn bộ join được về danh sách curate theo accession/start/end. Nguồn âm file `data/simulated_degrons.tsv.gz` có **1.510 dòng / 1.457 accession**, còn **1.428** sau `CONS_SCORE>0` và drop missing; baseline chuỗi dùng **1.421** âm có chuỗi/tọa độ hợp lệ, loại **7** dòng không tái dựng được. Không tự điền chuỗi thiếu. {refs}.

## Âm được dựng ra sao

[ĐỌC-MÃ] `Training_MetaDegron-X.py`: lấy 212 positives, lọc background như trên, sample **5×N có hoàn lại**, `random_state=2024509`, shuffle 42, StratifiedKFold 5 fold với RandomState 527. Đây là script CV X; nó không giữ riêng 10% holdout như script D. [Mã ghim](https://github.com/BioDataStudy/MetaDegron/blob/{ri['commit']}/Training_MetaDegron-X.py), [code-audit.json](code-audit.json).

[ĐO] Tái dựng đúng phép sampling này tạo **212 dương + 1.060 âm**, chỉ **748** hàng âm gốc phân biệt. Mỗi fold có **91–111** dòng test trùng khóa nhãn/accession/start/end với train. Đây là rò rỉ bản sao trong cách chạy script được cung cấp, chưa chứng minh số liệu bài báo được tạo bằng đúng script này. [composition-baseline.json](composition-baseline.json) → `author_x_sampling`; [audit_dataset.py](audit_dataset.py) → `sampling`.

[ĐO] Background là đoạn có accession/tọa độ trên protein thật: tái dựng được chuỗi cho các dòng đủ mapping. Histogram độ dài tọa độ âm đúng bằng 5 lần histogram dương toàn danh sách nhưng **dịch +1 aa**. Không có giao tọa độ chính xác với positive; có 14 protein chung. {refs}.

[CHƯA XÁC MINH] Không tìm được vòng lặp tạo ban đầu từng tọa độ âm trong mã/notebook đã kiểm. `random.seed(2023)` và `N=5` trong code tính thuộc tính không đủ chứng minh thuật toán tạo âm. Vì vậy giả thuyết “peptide ngẫu nhiên” chỉ đúng ở mức sampled background theo tác giả; **không có căn cứ gọi là chuỗi amino acid tổng hợp i.i.d.** hoặc biết chính xác quy tắc loại motif thật. [code-audit.json](code-audit.json).

## Thành phần và độ dài có phân biệt được không?

[ĐO] Logistic L2 C=1, chuẩn hóa trên train, 5 fold theo cụm protein, seed 17/29/43; không oversample âm và không chọn C bằng test. Quần thể tái dựng là bảng X, không phải object-NPY training của D. Bảng dưới là OOF pooled AUROC, CI bootstrap 5.000 cụm ở seed 17; khác metric macro theo peptide của G2. [composition-baseline.json](composition-baseline.json), [PREREGISTRATION.md](PREREGISTRATION.md).

{table(['Biểu diễn','cov80: seed 17 / 29 / 43','CI95 seed17'],base_rows)}

[DIỄN GIẢI] Thành phần có tín hiệu, song chưa đạt tiêu chí ≥0,75 ở cả ba seed; length-only dưới ngưỡng 0,65. Không được kết luận mô hình chỉ học thành phần, hoặc âm “dễ” hoàn toàn giải thích AUC công bố. Cửa sổ ngữ cảnh bằng độ dài vẫn có tín hiệu; phép so với AUC 0,87/0,90 chỉ là đối chiếu mức độ, không kiểm định ghép cặp cùng test. Kết quả cov50 và random 10% nằm trong JSON.

## Đồng dạng nội bộ

[ĐO] Phân cụm trên protein đầy đủ của các dòng dương tính, giữ các phiên bản chuỗi: **183 cụm cov80, 158 cụm cov50**. Dùng motif rất ngắn để gọi protein-homology sẽ không cùng điều kiện với G2. Tập hợp reference + positive + background có **8.333 record** và **5.793 / 4.969 cụm** tương ứng cov80/cov50. [clusters.json](clusters.json).

[ĐO] Khi mở rộng population, runner đọc lại **cả hai TSV cụm cũ** và ràng buộc mọi thành viên của mỗi cụm cũ phải cùng nhóm; không ghi lại TSV cũ hoặc đổi fold G2. Số cụm gốc, SHA và kiểm không tách nhóm được ghi trong [frozen-group-reuse.json](frozen-group-reuse.json). Baseline mới dùng nhóm mở rộng có ràng buộc này; count protein dương tính riêng dùng phép phân cụm riêng để mô tả dư thừa.

[ĐO] Mô phỏng 90/10 random trên danh sách dương, cov80 có **11–20/31** dòng test có họ hàng trong train; số cặp train–test cùng cụm **23–51/8.401**. Cov50 là **14–20/31**, **35–68/8.401**. Báo cả hai mẫu số để tránh tỉ lệ cặp nhỏ che số test bị ảnh hưởng. [overlap-audit.json](overlap-audit.json) → `internal_positive_homology`.

[CHƯA XÁC MINH] Đây là mô phỏng độ nhạy, **không phải split D thực tế**. Mã D dùng permutation seed 202310, split 10% seed 202309, stratification vector không được permutation đồng bộ; chưa tái dựng thứ tự object-NPY nên chưa biết giao thực tế. Bảng curate có cột `cluster` với các giá trị fold-like nhưng không được dùng làm group trong script train đã công bố; nguồn sinh cột đó chưa rõ. [code-audit.json](code-audit.json).

[ĐO] Riêng split X có thể tái dựng population và seed: đã đếm số dòng test chung cụm, số cặp train–test chung cụm và mẫu số mapped ở **từng fold**, cov50/cov80; xem `author_x_sampling.homology_by_cov` trong [composition-baseline.json](composition-baseline.json). Dòng thiếu mapping được loại khỏi mẫu số homology và báo coverage, không tự coi là singleton sạch.

## Chồng lấn với đề tài

[ĐO] Bảng sau phân biệt giao cùng accession và giao **đúng đoạn**: tile phải khớp toàn chuỗi trong protein nguồn, rồi khoảng degron phải giao tọa độ tile. Không tìm motif ngắn tự do trên protein không liên quan. Đã chuẩn hóa tên CRISPR thiếu accession bằng hậu tố tên peptide; không suy luận giao từ số tổng bằng nhau. [overlap-audit.json](overlap-audit.json).

{table(['Bộ','Tổng peptide/tile','Dòng curate cùng accession','Dòng curate giao vùng','Peptide/tile giao vùng','Đồng thuận nhãn theo cặp','Cặp giao vị trí quan trọng'],overlap_rows)}

[ĐO] Coverage chuỗi: footprint **{o['datasets']['footprint']['peptides_with_mapped_sequence']}/2.624**, bão hòa **{o['datasets']['saturation']['peptides_with_mapped_sequence']}/249**, CRISPR **{o['datasets']['crispr']['peptides_with_mapped_sequence']}/31**, G2 **{o['datasets']['g2']['peptides_with_mapped_sequence']}/91**. Peptide chỉ có trong bão hòa dùng snapshot UniProt người đã ghim/17 accession bổ sung và quy tắc tile của pipeline gốc; CRISPR thiếu accession được map GN nếu duy nhất. Một record bão hòa chưa map được, nên phép giao của bộ249 có giới hạn coverage; không coi record đó là không trùng. [overlap-audit.json](overlap-audit.json).

[ĐO] Hai giao footprint nằm ở HIF3A và HIF1A, đều PSI WT thấp và có vị trí đột biến làm bền reporter nằm trong khoảng curate. Giao bão hòa/G2 là cùng ca HIF1A: PSI WT nội tại **2,186493579**, **13/13** vị trí giao có ít nhất một thay thế ΔPSI ≥1. Không gọi đó là 13 ô: mỗi vị trí có nhiều acid amin thay thế. Số chi tiết và accession nằm trong [overlap-audit.json](overlap-audit.json), sinh từ file PSI hai nửa và NPZ G2.

[DIỄN GIẢI] Concordance ở giao nhỏ không đo được độ nhạy/đặc hiệu toàn quần thể và không xác nhận E3 trực tiếp. Voutsinos/Larsen dùng score khác PSI; mốc score 0,5 là ngưỡng thăm dò, không hoán đổi với PSI=3. Larsen có **3 cặp thiếu score**, đã để missing. [overlap-audit.json](overlap-audit.json). Một motif được annotate trong protein nguyên vẹn có thể yếu ở reporter tách rời và ngược lại; đó chưa phải nhãn curate sai.

## “21 E3” có cứu nhiệm vụ E3 không?

[ĐỌC-MÃ] Danh sách dưới lấy từ mapping E3→motif của prediction source, join class của bảng curate; **đếm tương thích motif**, không gán thêm nhãn thực nghiệm phân biệt E3. CBL gom các subtype về class CBL; CUL3 chồng KLHL; SIAH1/2 và NEDD4/ITCH chia sẻ cùng mẫu. Không cộng các cột để làm số degron độc lập.

[ĐO] Mỗi ô số dưới do `e3_after_filter` trong [overlap-audit.json](overlap-audit.json). Cột “G2” bỏ vùng trùng mọi bộ đang audit và protein cùng cụm với các peptide G2. Cột “toàn reference” bảo thủ hơn: bỏ mọi cụm chứa protein trong `proteins-full.fasta`, gồm cả protein không thuộc tập G2. Hai điều kiện này không tương đương.

{table(['E3 lựa chọn','Mẫu motif','HUMAN','Không trùng vùng/cụm G2 cov80','Toàn reference cov80','Toàn reference cov50'],e3_rows)}

[ĐO] Số lựa chọn ≥5 mẫu: trước lọc **13**, HUMAN **12**, bỏ vùng trùng **2**, thêm bỏ cụm G2 **2**, toàn reference **1** ở cả hai coverage. Chỉ **21** dòng curate HUMAN còn lại trong phép lọc toàn reference cov80, **18** ở cov50. [overlap-audit.json](overlap-audit.json).

[DIỄN GIẢI] Số đếm này chưa đủ tái mở nhiệm vụ E3 của luận văn: cần nhãn liên kết E3 riêng từng dòng, đủ **cụm** cho train/test, và negatives có ý nghĩa theo E3. Nhóm APC/C không tự phân biệt được CDC20/Cdh1. Số 21 của web không phải chứng cứ có 21 bộ train sạch.

## Chất lượng nhãn và mức dùng được

[ĐO] Mẫu truy nguồn: **40** dòng ngẫu nhiên seed17; **22/40** có ELM true-positive cùng class/giao tọa độ, **18/40** chưa chốt lineage qua nguồn hiện hành. Wilson cho tỉ lệ chưa chốt **45,0% [30,7%; 60,2%]**. Đây **không phải tỉ lệ sai nhãn**. [manual-label-review.json](manual-label-review.json), [review-labels.py](review-labels.py).

[DIỄN GIẢI] Rủi ro cao: gộp nhãn từ hệ đo khác; suy E3 từ motif; shortcut/duplicate split; quyền dữ liệu chưa rõ. Rủi ro trung bình: flank/isoform và metadata loài. Nhãn binary curate bổ sung vị trí/cơ chế/PTM nhưng thiên về motif kinh điển; ΔPSI lớn hơn về số phép đo nhưng là reporter, có nhiễu và nhiều ô chung protein. Không gán 0/1 curate vào cột ΔPSI hay coi background ngẫu nhiên là thí nghiệm không phân hủy.
''')
    write('manual-label-review.md',f'''# Kiểm truy nguồn mẫu dương tính

[ĐO] Đã chọn ngẫu nhiên {mr['n']} dòng bằng seed17 trước tính điểm, giữ chỉ số mẫu ở [label-sample.json](label-sample.json). Đã đọc từng dòng: protein/tọa độ/chuỗi từ S2, PMID nguồn, và Methods/References của record ELM hiện hành cùng class/giao tọa độ. Bản ghi từng dòng và nhận xét nằm ở đường dẫn `details_path` trong [manual-label-review.json](manual-label-review.json), dưới raw bị gitignore để không phân phối dữ liệu nguồn.

[ĐO] Có **22/40** truy được ELM true-positive; **18/40** chưa chốt lineage, **45,0%**, Wilson 95% **[30,7%;60,2%]**; **11/40** không phải HUMAN theo hậu tố, **27,5% [16,1%;42,8%]**. **4/40** có metadata assay ubiquitination. [manual-label-review.json](manual-label-review.json), [review-labels.py](review-labels.py).

[DIỄN GIẢI] “True-positive” của ELM là bằng chứng cho motif/tương tác mà ELM curate, không tự xác nhận protein nguồn bị phân hủy qua motif trong mọi hệ đo. Motif APC/C TPR có thể thuộc co-activator; BUB1B liên quan phức hợp checkpoint, nên đặc biệt cần thí nghiệm đo degradation, không chỉ cấu trúc/binding.

[CHƯA XÁC MINH] Chưa đọc đủ thí nghiệm gốc của mọi dòng; review 2017 có bảng gốc bị hạn chế ELTEnet, và nguồn S2 phần lớn trỏ bài tổng hợp. Không tìm được record ELM hiện hành không có nghĩa nhãn sai ở snapshot cũ. Do đó **tỉ lệ nhãn degron sinh học sai/mơ hồ chưa định lượng được**, để `null`; không trình bày 18/40 là false-positive rate. Các khoảng Wilson mô tả mẫu metadata, không chữa được thiếu thẩm định sinh học và không điều chỉnh phụ thuộc giữa motif.

[ĐỀ XUẤT] Vòng adjudication tiếp theo cần hai người đọc độc lập PMID thí nghiệm gốc, chốt loại assay (half-life/reporter, mutation rescue, E3 perturbation, binding-only), PTM, loài và isoform. Mỗi nhãn không đủ chứng cứ để ngoài training; không đổi thành âm. Dừng nhập nhãn nếu không có giấy phép và lineage đủ rõ.
''')

if __name__=='__main__':main()
