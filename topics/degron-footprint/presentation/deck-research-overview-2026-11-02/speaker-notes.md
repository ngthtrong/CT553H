# Ghi chú người trình bày

## 1. Hiệu ứng đột biến degron ở mức residue

Buổi giới thiệu đề tài và trao đổi tiến độ; không phải bảo vệ hoàn tất. Hình mở đầu dùng ma trận nhãn đo HIF1A. Mục tiêu: người nghe hiểu bài toán, thấy bằng chứng và góp ý hướng tiếp theo.

Nguồn: slide-figures-2026-10-15/example-matrix.json

## 2. Degron tham gia quá trình phân hủy protein

Sơ đồ là nguyên lý đơn giản hóa UPS. GIF Fam188a của Nikolakhs, CC BY-SA 3.0, chỉ minh họa một protein gấp cuộn, không phải HIF1A/degron đã đo. Hoạt tính của đoạn peptide tách rời có thể khác trong protein nguyên vẹn.

Nguồn: 

## 3. Một phép thay tạo một ô trong bản đồ hiệu ứng

WT là trình tự tham chiếu. Ma trận hiển thị 28 vị trí và 20 amino acid; ô WT→WT được mask, có 532 phép thay thật khi đủ dữ liệu. Đây là sơ đồ đầu ra, không phải dự đoán mô hình.

Nguồn: model-selection-pipeline-2026-10-24/README.md

## 4. GPS chuyển tín hiệu reporter thành nhãn ΔPSI

Histogram là minh họa cách đo, không phải số liệu thực nghiệm. PSI của Zhang dùng sáu bin, thang 1–6; thấp là reporter kém bền. Không tự suy dấu ΔPSI thành cơ chế E3 hay khả năng gây bệnh.

Nguồn: full-data-audit/psi-build.json

## 5. Ví dụ HIF1A cho thấy hiệu ứng tập trung theo vị trí

Peptide Q16665_HIF1A_25, vị trí protein 553–580. WT nội tại PSI2.1865; 186 ô ΔPSI≥1. Ví dụ được chọn theo ≥500 ô, nhiều ô dương nhất, hòa lấy ID nhỏ nhất. Đối chiếu motif HIF1A/VHL là y văn, không phải phát hiện cơ chế mới. Ô WT và ô thiếu đều được mask.

Nguồn: slide-figures-2026-10-15/example-matrix.json

## 6. Giá trị sử dụng là ưu tiên đột biến để kiểm chứng

Không coi xếp hạng dự đoán là thay thế thực nghiệm. ClinVar là annotation và động lực nghiên cứu; liên hệ bệnh ở mức residue chưa thiết lập. Các ô trong hình chỉ mô tả lựa chọn, không phải điểm mô hình.

Nguồn: variant-coverage-2026-10-15/README.md

## 7. Công trình liên quan trả lời các câu hỏi khác nhau

Không nhận ma trận hoặc web là tính mới độc quyền. Khác endpoint thì không so trực tiếp AUROC. MetaDegron có một classifier dùng chung với lựa chọn motif/E3; không phải mọi menu là một lớp E3 học độc lập.

Nguồn: metadegron-analysis-2026-10-21/comparison-and-positioning.md

## 8. Ba mục tiêu nối nghiên cứu với công cụ

Không đặt dự đoán E3 hay chẩn đoán biến thể gây bệnh làm nhiệm vụ chính. Không có phép đo sinh học mới. Công cụ phục vụ hình thành giả thuyết và lựa chọn thí nghiệm.

Nguồn: model-selection-pipeline-2026-10-24/README.md

## 9. Các câu hỏi đang dẫn dắt hướng nghiên cứu

Sơ đồ là quan hệ nghiên cứu, không là lịch chạy. Các kết quả được tổ chức theo câu hỏi, không theo mã phiên hay thứ tự thời gian.

Nguồn: kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md

## 10. Nguồn dữ liệu được dùng đúng vai trò

Core v3 chỉ chứa Zhang và UniProt, không chứa ClinVar/Koren/Larsen/MetaDegron hoặc weights. Larsen/MaveDB là nguồn khảo sát với endpoint khác. Phân biệt nguồn đã tải, đã audit và đã dùng fit.

Nguồn: kaggle-roadmap-2026-10-31/DATASET.md, full-data-audit/README.md

## 11. Hai thiết kế đột biến có độ phủ bổ sung

Scanning có phép thay là hàm của WT: hướng R/A/S, tổng20 cặp có hướng trong380 cặp không đồng nghĩa. Hình biểu thị thiết kế lý tưởng, không khẳng định mọi ô đều qua QC.

Nguồn: scan-sat-merge-2026-10-23/README.md

## 12. Mốc WT phải phù hợp với từng thí nghiệm

Saturation không có mut0; dùng trung vị ô đồng nghĩa từng nửa. Scanning dùng mut0 đúng replicate. Không lấy BAG6 WT làm mốc saturation. PSI dựng lại261865 giá trị khớp tác giả trong5e-7 khi mô phỏng điều kiện tái lập.

Nguồn: full-data-audit/psi-build.json, full-data-audit/saturation-matrix.json

## 13. Độ lặp lại của nhãn đặt giới hạn cho cách đọc kết quả

0.8335 là Pearson giữa hai nửa trên cohort saturation theo audit. Không so noise_share của tổng phương sai với noise_share của phần dư như cùng đại lượng. Replicate là mốc độ tin cậy của phép đo, không phải trần tuyệt đối cho mọi estimator.

Nguồn: full-data-audit/saturation-matrix.json, full-data-audit/replicate-audit.json

## 14. Chia theo nhóm protein để kiểm khả năng tổng quát hóa

Hai thiết kế có population, eligibility và preprocessing khác, không nối AUROC thành một đường tiến bộ. V3 dùng5outer folds và3seed inner-validation; các transform chỉ fit trong train, epoch chọn rồi khởi tạo lại refit. Nhóm có homology heuristic, không chứng minh độc lập sinh học tuyệt đối.

Nguồn: kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md

## 15. Sai số, xếp hạng và ngân sách thí nghiệm là các mục tiêu riêng

V3 MAE có235 peptide; event dương Δ≥1 có184peptide đủ điều kiện, âm Δ≤−1 có110. Mỗi lớp phải có≥3ô. Bootstrap5000 theo nhóm, không theo122412ô. AUROC không là accuracy; AP cần đọc với tần suất event.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 16. Ngữ cảnh cục bộ bổ sung thông tin ngoài phép thay

M0 pair+composition0.8393; unordered0.8625; ordered±3 0.8682. Ordered−M0 +.0289 CI[.0264,.0313]. Trung bình AUROC các seed trong nguồn này, không gán là ensemble v3. Mô hình tuyến tính composition hằng trong peptide không tự đổi thứ hạng giữa vị trí có cùng phép thay.

Nguồn: residue-task-derisk-2026-10-15/model.json

## 17. Học toàn dải PSI giảm sai số hồi quy của Ridge

Cùng235peptide test,221nhóm. Hai contrast Q1 dùng CI97.5% Bonferroni. Arm hẹp vẫn dùng validation toàn dải. Không đưa PSI(WT) vào feature hoặc dùng nó clip dự đoán.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 18. Lợi ích toàn dải tập trung ở miền PSI cao

Các strata có91/85/36/23peptide. Ridge full ở miền≤3 không thấy giảm quáguardrail. Cân bằng có cận CI AUROC hơi vượt−.01. >5 không có eventdươngΔ≥1 nên AUROC dươngnull đúng. Khi soCNN toàn dải/chỉ≤4, miền≤3 MAE tăng.00870 CI[.00329,.01411], không suy guardrailRidge sangCNN.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, kaggle-roadmap-2026-10-31/output-analysis-details.json

## 19. ESM bổ sung tín hiệu cho baseline ngữ cảnh

W5+ESM−W5 AUROC+.012548 CI95[.006216,.019670]. Nested selection MAE.397525 vsW5.407803, AUROC improvementCIphủ0. Không lấy fixedrecipe tốt nhất thay cho nested procedure. Bảng nhiều cỡ ESM trên thiết kế khác để phụ lục.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 20. CNN cải thiện thêm sau representation ESM

ESMCNN−pointwise MAE CI95[−.010173,−.000899], AUROC+.011289CI[.003434,.019133]. Head parameter36833vs57185 nên chưa cô lập sức chứa. CI khácQ1 là mô tả, chưa điều chỉnh toàn khảo sát.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 21. Nhiều cửa sổ chưa chứng minh vượt một cửa sổ

mCNNE MAE.383846vsCNND.384354, chênh−.000508CI95[−.003157,+.002223]. CùngD mCNN−CNN +.000639CIphủ0. B/D/E là lựa chọn phân bốtrain nội bộ, màn chiếu dùng tên đầy đủ. CNN chỉPSI≤4 đánggiữ nếuưu tiênmiềnthấp; toàn dải so nó chưađảm bảoguardrail.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, kaggle-roadmap-2026-10-31/output-analysis-details.json

## 22. Học tốt nhãn tile chưa bảo đảm chuyển sang mutation effect

Cùngthiếtkế ext4 trên91peptide. Nguồn212616tile; encoderpretrainPearson.864 nhưng downstreampre−rand−.0077CI[−.0163,+.0006]. Nhánhpre−ridge−.011CIâm. Không so thẳng với số v3 hoặc quy thành pretraining pLM vô ích.

Nguồn: pretrain-p3-2026-10-22/results.json

## 23. Scanning pretrain có lợi cả ngoài các kiểu thay đã thấy

Transfer onehotCNN, không làESM+scanning. Cohort20 có6433ô;360 có115979ô,cùng235peptide221nhóm. Mean12−rep1CIphủ0. Quality−satonly +.004010. Scan_T không thamgiafit; kếtquả ởsaturationOOF khônglàtransferT.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, kaggle-roadmap-2026-10-31/output-analysis-details.json

## 24. Đối chiếu Degformer cần kiểm cả chồng mẫu và ngân sách nhãn

Checkpoint.9248có88.12%ôtrùng. Retrainsạch.806775, Ridgeext.820822, delta−.014CI[−.0283,+.0010]=>khôngphânbiệtđược. Retrainkiếntrúcchỉ47knhãn.749978làthiếtkếriêng. Không coi chênhcheckpoint/retrain là causal leakage-only effect vì các điều kiện thay đổi.

Nguồn: r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json

## 25. Xếp hạng giúp tập trung ngân sách vào đột biến đáng thử

Precision macro trong184peptideeligibleplus. Top10CNN49.04%vsRidge44.29%. AP+.50947,rate+.124697 trêncùngcohort. AP−.213667,rate−.027336trên110peptide;precisiontop5−16.77%. Không dùngtopkzero-scorephụthuộctiebreaklàmrandom.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 26. Độ ổn định và chi phí cùng tham gia lựa chọn mô hình

Tổngtaskseconds9.3265h,77.52%stage11frozen; chưa gồmLoRAdở. Chỉseed17frozenB/D. 35taskcomplete,1runningtrongsnapshotkhôngchứngminhremotecònsống. Frozenstage11chạybackbonemỗibatch; cache làhướngtốiưucầnparity, không cóbenchmarktăngtốc. Nguồn chốt ởsnapshotKaggle, khônggộpjoblocalđangchuẩnbị.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, kaggle-roadmap-2026-10-31/output-analysis-details.json

## 27. Hiệu chuẩn nối điểm hồi quy với xác suất sự kiện

RidgeM3ext4PlattBrier.0925vsconst.1139,BSS.188. ScoreΔPSIclippedkhôngtựlàprobability. Reliabilitythiênthấpdo fitpoolkhácmiềntest; khônggọicalibrationhoànhảo. Protocolv3crossfitcalibrationkhácchitiếtP6, khôngmangnguyêncalibratorsangCNN.

Nguồn: calibration-p6-2026-10-22/results.json

## 28. Miền áp dụng cần được đánh giá cùng với dự đoán

CổngR3khảosátchomiềntrainPSI≤4. PSIpeptidomescreenlệchWTintrinsic~.9,khôngdùngrawthreshold4trực tiếp. ÁpquaR3khoảng26%in9%border65%out. FullPSIkhôngtựchocổngđộcậymớivàkhôngchứngminhphục vụmọiprotein. Tíchhợpgateappcònmở.

Nguồn: r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json

## 29. Công cụ đưa ma trận và danh sách ưu tiên vào cùng một luồng

Ảnhchụpprototypeworkspaceuiv2hiệnhành. Tấtcảscore/probabilitydemo làsyntheticfixture; khônglàmodeloutput. BaselineReact/FastAPIđãcómãriêng; prototypekhôngnghiệmthubatchprojectsimports. Chỉdùngảnhthiếtkếđểminhhọaluồng.

Nguồn: ../system/design/workspace-ui-v2/README.md

## 30. Một ứng dụng local giữ kết quả cùng nguồn gốc

StackđãchốtReactTypeScriptFastAPIlocal. SQLiteđãdùngchobaseline; PostgreSQLvàdurableworkspacelàphạmvicầntriểnkhaikiểm. KhôngcóyêucầupublishVPS. Sơđồkiếntrúcđịnhhướng, khônglàxácnhậnmọimoduleđãhoànthành.

Nguồn: ../system/README.md

## 31. Phần mềm có nền tảng để tiếp tục mở rộng

Baselinebackend149pytest/frontend131vitestlàbằngchứnglịchsửghiởsystemREADME,chưachạylạitrongphiêndựngslide. Scopev0.2đãthiếtkếchưatriểnkhaixong; R3gatechưaloadđúngtrongapp. Tránhtrìnhtấtcảplannedendpointlàđãcó.

Nguồn: ../system/README.md

## 32. Những gì đã thực hiện tạo nền tảng cho hướng nghiên cứu

KhôngtựđóngG2/G3hoặctuyênbốhoàntấtluậnvăn. Đónggópđangxâydựnggồmbenchmark/phươngpháp/đánhgiá/phầnmềm,khôngbắtbuộckiếntrúcmới. Các kết quả âm có vai trò thu hẹp hướng nghiên cứu.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, model-selection-pipeline-2026-10-24/README.md

## 33. Ưu tiên tiếp theo là khóa lựa chọn và kiểm chứng khả năng chuyển giao

FinalpromotiontựđộnghiệnchỉW5; CNNcầnmodel-specificrefitexport. Khóarecipe/calibrationtrướckhiđọcT. Nguồnscanningđãthăm dòtronglịchsử,khônggọiđộclậphoàntoàn. KhôngcầnchờLoRAđểhoànthiệnbenchmarklõi.

Nguồn: kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md

## 34. Trao đổi về hướng nghiên cứu và bước tiếp theo

Mời giảng viên góp ý mục tiêu và hướng ưu tiên. Đây là buổi giới thiệu/tiến độ, không phải nghiệm thu toàn bộ đề tài. Có thể mở overview hoặc phụ lục để trao đổi chi tiết.

Nguồn: 

## 35. Cách đọc các thuật ngữ trong bài toán

Residue: amino acid tại một vị trí. WT: trình tự tham chiếu. OOF: dự đoán ngoài fold.

Nguồn: model-selection-pipeline-2026-10-24/README.md

## 36. Chi tiết tạo nhãn và kiểm chất lượng

Đồng nghĩa dùng làm WT nội tại; ô thiếu được mask; điều kiện đo được giữ riêng.

Nguồn: full-data-audit/psi-build.json, full-data-audit/saturation-matrix.json

## 37. Độ tin cậy phụ thuộc mức phân tích

SốpsiAgreement0.9239trongREADMEfullauditlàmốcsoWTkhôngphảiđúngrep1rep2; dùngđúngtrườngΔPSI. Khônggọi75.9%phầndưnhiễuvà16.7%tổngphươngsailàcùngmẫusố.

Nguồn: full-data-audit/replicate-audit.json, full-data-audit/saturation-matrix.json

## 38. Mô hình composition không phân biệt mọi vị trí

Bấtbiếnápdụngchocompositionthuầntúy; khônggánchotoànPAPcókênhCterminal. M0thực tếcó40chiềupair+20composition. Oracleđọctestkhôngphảitestperformance.

Nguồn: composition-context-audit.md, residue-task-derisk-2026-10-15/model.json

## 39. Learning curve cần tách model đơn và ensemble

Độ nhạy phân cụm là phép kiểm riêng; không đếm phân hoạch trùng nhau như bằng chứng mới.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis-details.json, recluster-sensitivity-2026-10-22/results.json

## 40. Các thiết kế tương tác chưa vượt baseline ổn định

Đây là những thiết kế đã thử, không phải phủ định mọi tương tác phi tuyến.

Nguồn: g2-saturation-2026-10-18/results.json, g2-extension-2026-10-18/e2-candidates.json

## 41. Lọc trùng mức ô chưa loại được chồng mức peptide

Cần đánh giá theo peptide/nhóm protein được giữ riêng.

Nguồn: g2-saturation-2026-10-18/results.json, r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json

## 42. Khảo sát cỡ ESM thuộc các thiết kế riêng

SốlấytừR6D,bổsungchoM3ext4. Cáccheckpointkháctrongregistrykhôngđồngnghĩađãđánhgiá. V3fullWchỉESM235M. 35Mpreflightforwardshape2x28x480vàfinite/repeatpass.

Nguồn: r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json

## 43. Đọc nhiều tiêu chí trên cùng các ứng viên

Các điểm là ensemble dự đoán ba seed; vẫn là phân tích development.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 44. Scanning transfer: tách các kiểu thay thế để kiểm chuyển giao

Mỗi peptidechỉtínhôtrongcohort. AUROCdươngeligible114và184nênkhôngsotrực tiếpmacrogiữahai cohort. HaiCIởhìnhlàhậukiểmmôtảkhôngđiềuchỉnhđa kiểmđịnh.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis-details.json

## 45. ClinVar hỗ trợ động lực ở mức vùng, chưa xác nhận mức residue

ORmh2.14783CI[2.07193,2.22651],3114tầng. Khôngliênhệnhânquả. Sat_exactAUC.6738CI[.489,.831]n51chưađạt; scan_posAUC.5166CIphủ.5. NguồnClinicalkhôngdùngchọnmodel.

Nguồn: variant-coverage-2026-10-15/enrichment.json, variant-coverage-2026-10-15/README.md

## 46. Nhãn E3 chưa đủ cho nhiệm vụ có điều kiện E3

Chỉ một nhóm có ít nhất năm peptide; không dùng số E3 trong menu thay cho số lớp có thể học.

Nguồn: e3-labels-audit/README.md

## 47. Nguồn ngoài cần được đánh giá theo endpoint và khả năng sử dụng

Korenchưađánhgiámôhình,vaitròcandidatetestnhỏvàquyềnsửdụngnộibộ. MaveDBexposureexploratorycònGCKassay/dimerconfound,cầnchạylạitrướckếtluậnmạnh. SaProttrue3Di chưaoutput; weightskhôngthaymappingstructure.

Nguồn: koren-s4-audit-2026-10-22/results.json, larsen-nuclear-and-risks-2026-10-15/README.md, architecture-check/README.md

## 48. Calibration và domain gate trả lời hai câu hỏi khác nhau

Cả hai cần được kiểm lại khi đổi model hoặc thay phạm vi dữ liệu.

Nguồn: calibration-p6-2026-10-22/results.json, r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json

## 49. Tính tái lập nối dữ liệu, model và kết quả phục vụ

Integrity2986files3065290891bytes83OOF47recipes; reproducedanalysisexact. Những con sốtestapp149backend131frontendlàhistoricalbaselinekhôngchạylạitrongtaskslides. SnapshotKaggleupdated2026-11-01T11:18:07Z,khônggộplocalruntimekhác.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, ../system/README.md

## 50. Tài liệu và bằng chứng có thể tra cứu theo chủ đề

Khônggắnfootnotelênmọislidetheoyêucầu. Toànbộnguồnđượctậptrungtạiphụlục,notevàJSON. Websiteđượcdùngkhảosátdesigntrướckhidựng,khôngbổsungclaimhiệunăngmodel.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

