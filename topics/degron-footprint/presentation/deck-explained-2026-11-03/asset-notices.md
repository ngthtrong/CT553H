# Nguồn hình ảnh và tài sản

## Video proteasome

- Tác giả: **Andreas Martin, HHMI**; nguồn [NIGMS Image Gallery, ID 3764](https://www.nigms.nih.gov/image-gallery/3764).
- Video: https://www.nigms.nih.gov/sites/nigms/files/image-and-video-gallery/AllDegProcesses.mp4
- Giấy phép thư viện: **CC BY-NC-SA 3.0**, theo [trang Image and Video Gallery](https://www.nigms.nih.gov/image-gallery), kiểm ngày 03/11/2026.
- `assets/proteasome.mp4` giữ nguyên; `assets/proteasome-poster.jpg` là khung hình trích tại giây 6. Video và poster giữ điều kiện giấy phép của nguồn.
- Đây là mô phỏng cơ chế, không phải quan sát của thí nghiệm Zhang hoặc kết quả nghiên cứu trong repo.

## Graphical abstract Zhang 2023

- Zhang et al., *Elucidation of E3 ubiquitin ligase specificity through proteome-wide internal degron mapping*, Molecular Cell 83, DOI [10.1016/j.molcel.2023.08.022](https://doi.org/10.1016/j.molcel.2023.08.022).
- Nguồn: [PDF từ Timms Lab](https://www.timmslab.com/media/papers/2023_Mol_Cell_Elucidation_of_E3_ubiquitin_ligase_specificity_through_proteome-wide_internal_degron_mapping_naf6vNE.pdf).
- **CC BY 4.0** được khai báo rõ trên trang PDF 2 (trang bài báo 3377), đã đọc trực tiếp ngày 03/11/2026. Hash PDF nằm trong `media-sources.json`.
- `assets/zhang-graphical-abstract.png`: cắt graphical abstract từ trang PDF 1, raster hóa, giữ nguyên nội dung hình. Chú thích và nguồn được đặt ngoài hình.
- Ghi chú giấy phép lịch sử trong `resources/papers/analyzed-papers/zhang-2023.md` khác bản PDF đã kiểm; không sửa ghi chú đó trong công việc này. Quyết định dùng hình dựa trên tuyên bố giấy phép trong bản PDF cụ thể.
- Bài có erratum Figure 2A, DOI 10.1016/j.molcel.2023.10.021; deck không sao chép Figure 2A.

## GIF protein

- Nikolakhs: [I-TASSER predicted protein fold of Fam188a](https://commons.wikimedia.org/wiki/File:I-TASSER_predicted_protein_fold_of_Fam188a.gif), **CC BY-SA 3.0**.
- GIF và poster dùng lại từ deck ngày 02/11; giữ attribution và giấy phép. Chỉ minh họa protein gấp cuộn, không phải HIF1A hay degron đang được đo.

## Tài sản dùng lại và sơ đồ mới

- Các SVG `training-range`, `strata`, `mcnn-ci`, `transfer`, `hif-measured` và screenshot `workspace-prototype.png` dùng lại từ `../deck-research-overview-2026-11-02/`. Nguồn khoa học được đối chiếu qua `evidence.json`, mỗi slide có nguồn và giới hạn trong `slide-sources.json`.
- Screenshot là prototype với fixture tổng hợp, không phải inference hoặc chức năng đã nghiệm thu.
- Một số helper SVG và CSS theme được dùng lại. Sơ đồ còn lại dựng bằng SVG/HTML từ mô tả và code trong repo, gắn nhãn minh họa khi không là dữ liệu đo.
- Font **Be Vietnam Pro**, SIL OFL; xem `vendor/font-license.txt`.
- **Chart.js 4.4.1**, MIT; xem `vendor/chart-license.md`.

Hash media ở `media-sources.json`; hash các tài sản cuối và nguồn số liệu ở `evidence.json`.
