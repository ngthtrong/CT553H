# Schema từng bảng

[ĐO] Tự đọc bảng bằng `audit_dataset.py --stage profile`; kiểu từng cột, missing và exact duplicates ở [dataset-audit.json](dataset-audit.json). Không nạp object NPY hoặc notebook. Các cột được ghi để định nghĩa schema, không sao chép dòng dữ liệu.

| Bảng | Dòng | Cột | Tên cột |
|---|---|---|---|
| repo/data/annotated_degrons_properties.tsv | 212 | 22 | Entry, Entry_Isoform, DEGRON, START, END, ASA_SCORE, CONS_SCORE, FCONS_SCORE, COIL, HELIX, STRAND, DSS_SCORE, RIG_SCORE, ANCHOR_SCORE, Domain_pfam, nflanking_ub_lysines, ub_lysines, nflanking_lysines, any_lysines, nflanking_ptms, ptms_flanking, Type |
| repo/data/degron_data.txt | 302 | 9 | class, Entry, Entry name, START, END, deg_seq, source, cluster, protein seq |
| repo/data/simulated_degrons.tsv.gz | 1510 | 21 | Entry, Entry_Isoform, DEGRON, START, END, ASA_SCORE, CONS_SCORE, FCONS_SCORE, COIL, HELIX, STRAND, DSS_SCORE, RIG_SCORE, ANCHOR_SCORE, Domain_pfam, nflanking_ub_lysines, ub_lysines, nflanking_lysines, any_lysines, nflanking_ptms, ptms_flanking |
| repo/data/test_properties.tsv | 20 | 16 | Gene_names, Entry, DEGRON, Start, End, solvent_accessibility, conservative_score, coiled_coil, a_helix, disorder, flexibility, anchoring_score, structured_domain, flanking_ub_lysine, flanking_ptms, Hit |
| repo/supporting_file/Degpred_result.csv | 400 | 3 | predicted_probs, true_labels, symbol |
| repo/supporting_file/elm_class_202309.txt | 28 | 6 | Accession, ELMIdentifier, Motif, FunctionalSiteName, Description, Regex |
| repo/supporting_file/simulated_degron2.csv | 733 | 21 | Entry, Entry_Isoform, DEGRON, START, END, ASA_SCORE, CONS_SCORE, FCONS_SCORE, COIL, HELIX, STRAND, DSS_SCORE, RIG_SCORE, ANCHOR_SCORE, Domain_pfam, nflanking_ub_lysines, ub_lysines, nflanking_lysines, any_lysines, nflanking_ptms, ptms_flanking |
| repo/supporting_file/simulated_degrons.tsv.gz | 1510 | 21 | Entry, Entry_Isoform, DEGRON, START, END, ASA_SCORE, CONS_SCORE, FCONS_SCORE, COIL, HELIX, STRAND, DSS_SCORE, RIG_SCORE, ANCHOR_SCORE, Domain_pfam, nflanking_ub_lysines, ub_lysines, nflanking_lysines, any_lysines, nflanking_ptms, ptms_flanking |
| repo/supporting_file/uniprot_seq.tsv | 20377 | 12 | Entry, Reviewed, Entry Name, Protein names, Gene Names, Organism, Length, Gene Names (primary), Sequence, Tissue specificity, Ensembl, Entry_Isoform |
| supplementary/supplementary_table_s1_bbae519.xlsx#Table S1 | 7 | 10 | Name, Release year, Category, Feature input, Algorithm, Type, Availability, Prediction webserver, Other omics, PubMed ID |
| supplementary/supplementary_table_s2_bbae519.xlsx#Table S2 | 302 | 7 | UniProt ID, Entry name, Start, End, Degron instance, PudMed ID, Source protein squence |
| supplementary/supplementary_table_s3_bbae519.xlsx#Table S3 | 1510 | 20 | Entry, Degron, Start, End, ASA_SCORE, CONS_SCORE, FCONS_SCORE, COIL, HELIX, STRAND, Disorder_SCORE, RIG_SCORE, ANCHOR_SCORE, Domain_pfam, nflanking_ub_lysines, ub_lysines, nflanking_lysines, any_lysines, nflanking_ptms, ptms_flanking |
| supplementary/supplementary_table_s4_bbae519.xlsx#Positive | 20 | 23 | Gene name, Entry, Degron type, Start, End, ASA_SCORE, CONS_SCORE, FCONS_SCORE, COIL, HELIX, STRAND, DSS_SCORE, RIG_SCORE, ANCHOR_SCORE, Domain_pfam, nflanking_ub_lysines, ub_lysines, nflanking_lysines, any_lysines, nflanking_ptms, ptms_flanking, Hit, Protein name |
| supplementary/supplementary_table_s4_bbae519.xlsx#Simulated | 1510 | 20 | Entry, Degron type, START, END, ASA_SCORE, CONS_SCORE, FCONS_SCORE, COIL, HELIX, STRAND, DSS_SCORE, RIG_SCORE, ANCHOR_SCORE, Domain_pfam, nflanking_ub_lysines, ub_lysines, nflanking_lysines, any_lysines, nflanking_ptms, ptms_flanking |
| supplementary/supplementary_table_s5_bbae519.xlsx#Average | 15 | 3 | Tools, Metrics, Values |
| supplementary/supplementary_table_s5_bbae519.xlsx#All | 150 | 4 | Tools, Metrics, Values, Times |
