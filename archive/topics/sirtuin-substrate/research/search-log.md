# Nhật ký tìm kiếm — 08/10/2026

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

Phạm vi: bài toán cơ chất deacetyl hóa sirtuin, không phải nhận diện enzyme sirtuin hay vị trí NAD+ trên enzyme. Ngôn ngữ truy vấn chủ yếu tiếng Anh. Tìm qua web search, trang publisher, PubMed/PMC/Europe PMC, PRIDE/ProteomeXchange, GitHub chính thức và Synapse. Đây là khảo sát định hướng có truy vết, **không phải systematic review đã đăng ký protocol**; chưa có truy vấn Scopus/Web of Science đầy đủ hoặc sàng lọc hai người độc lập.

## Các nhóm truy vấn đã dùng

| Nhóm | Chuỗi truy vấn tiêu biểu | Kết quả ảnh hưởng quyết định |
|---|---|---|
| Tiền lệ trực tiếp | `sirtuin substrate prediction machine learning isoform`; `SIRT3 Substrate Specificity Determined by Peptide Arrays and Machine Learning`; `Identifying Human SIRT1 Substrates Integrating Heterogeneous Information` | Smith 2011; Zhai 2017; Ridgeway 2025; Deep-PLA |
| PLM và nhiều nhãn | `"sirtuin" "protein language" substrate prediction`; `"SIRT3" "substrate" "PLM" prediction`; `"sirtuin" "multi-label" prediction substrate` | Chưa tìm thấy công trình đúng toàn bộ đích bảy nhãn + assay/cellular + protein/homology split; không kết luận không tồn tại |
| Conformal | `"sirtuin" "conformal"`; `"conformal prediction" "sirtuin"`; `"conformal" "post-translational" prediction` | Không tìm được cơ sở để hứa coverage cho endpoint tế bào này; loại kết quả “conformal geometric algebra” vì khác khái niệm |
| Đối thủ được nêu | `Deep-PLA bbz107`; `NAD_MCNN 70085`; `NAD_MCNN 40183480`; `SirtSAGE Structural Gated Graph Attention Framework Unified Classification Evolutionary Mapping` | Deep-PLA có SIRT1/2/3/6/7; NAD_MCNN khác đích; SirtSAGE chưa đọc được publisher full text |
| PTM hiện hành | `DeepPTMPred 2026`; `CLASPP 1014616 post translational 2026`; PLM acetylation AIPred | Đối chiếu paper chính thức: PLM/đa tác vụ/cấu trúc không mới tự thân |
| Dữ liệu cellular | Tên/DOI Rauh, Ridgeway, Weinert, Zhang, Hebert, Rardin; `PXD021357`, `PXD023479`, `PXD019763`, `PXD012796` | Truy nguồn SD14 về Zhang/Synapse; phân biệt sham–UUO, interactome và KO acetylome |
| Giả định uncertainty/XAI | Conformal under covariate shift; beyond exchangeability; two-layer hierarchical conformal; Sanity Checks for Saliency Maps | Cần phân biệt endpoint shift, protein clusters, marginal/joint/conditional coverage và fidelity |

## Mức đọc và nguồn chính

- **Toàn văn + phụ lục/bảng:** [Rauh](https://doi.org/10.1038/ncomms3327); [Ridgeway](https://doi.org/10.1038/s42004-025-01717-6); [Weinert](https://doi.org/10.15252/embj.201591271); [Zhang](https://doi.org/10.1038/s41598-022-06793-5); [Deep-PLA](https://doi.org/10.1093/bib/bbz107). Không đọc từng raw spectrum; không tái chạy MS processing.
- **Toàn văn, chưa audit bảng thí nghiệm:** [Smith 2011](https://doi.org/10.1021/cb100218d), PDF từ [trang tác giả](https://burrsettles.com/pub/smith.acs11.pdf); [Zhai 2017](https://doi.org/10.1038/s41598-017-04847-7), PMC/Europe PMC; [Rardin 2013](https://doi.org/10.1073/pnas.1302961110), PMC HTML. Rardin supplementary XLSX chưa truy cập được.
- **Metadata/abstract và dữ liệu dẫn xuất:** [Hebert](https://pubmed.ncbi.nlm.nih.gov/23201123/) và ratios nhập trong Weinert EV1. Không gọi là đã đọc toàn văn Hebert: Europe PMC fullTextXML trả 500; PMC web challenge.
- **Abstract/tên bài, chưa toàn văn:** [NAD_MCNN](https://doi.org/10.1111/cbdd.70085), PMID40183480; [SirtSAGE](https://doi.org/10.1142/S2737416527400011). Publisher không truy xuất được. Bài đăng LinkedIn tác giả giúp tìm DOI SirtSAGE, **không dùng thay bài gốc để xác nhận chi tiết kỹ thuật**.
- **Toàn văn web ở mức task/architecture, không audit benchmark:** [AIPred](https://doi.org/10.1186/s12915-025-02418-1), [DeepPTMPred](https://doi.org/10.1093/bib/bbag321), [CLASPP](https://doi.org/10.1371/journal.pcbi.1014616). CLASPP xuất bản 14/08/2026, nằm trước ngày khảo sát.
- **Nguồn phương pháp gốc:** [Angelopoulos–Bates](https://arxiv.org/abs/2107.07511); [Tibshirani và cộng sự](https://arxiv.org/abs/1904.06019); [Barber và cộng sự](https://doi.org/10.1214/23-AOS2276); [Dunn và cộng sự](https://robinmdunn.github.io/publication/conformal/); [Adebayo và cộng sự](https://papers.nips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html). Báo cáo đề xuất áp dụng, chưa chứng minh theorem mới.

## Giới hạn và việc phải bổ sung

Chưa vét tất cả preprint, công trình mới không được index hoặc bài paywall; chưa citation-chain đầy đủ từ ASEB/DeepSIRT; chưa full-text SirtSAGE/NAD_MCNN. Cần cập nhật khảo sát khi chốt đề cương, kiểm task/endpoint trước khi xếp một tên bài vào baseline. Các kết luận “đã có tiền lệ” có bằng chứng trực tiếp; kết luận “chưa thấy đúng tổ hợp” chỉ có giá trị trong phạm vi truy vấn này.
