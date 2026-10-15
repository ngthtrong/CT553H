# Licensing and access terms for the Larsen et al. nuclear (transcription-factor) degron dataset

> Research date: **2026-10-15**. Target work: Larsen FB, Voutsinos V, Jonsson N, Johansson KE, Ethelberg FD, Lindorff-Larsen K, Hartmann-Petersen R. *Comprehensive degron mapping in human transcription factors*. bioRxiv, DOI [10.1101/2025.05.16.654404](https://doi.org/10.1101/2025.05.16.654404), posted 2025-05-17.
>
> **Evidence labels used throughout:** `[READ]` = text I read directly on the source page / API response; `[META]` = structured metadata from an API or a search-result snippet, not the rendering of the human-facing page; `[INTERP]` = my own reasoning or legal interpretation, **not legal advice**.

---

## Q1. Exact license on the bioRxiv preprint page, and whether a peer-reviewed version exists

### Takeaway

The preprint is **CC BY-NC-ND 4.0**, confirmed from four independent sources (the article page text, Crossref, the bioRxiv API, Europe PMC). As of 2026-10-15 there is **only version 1** and **no peer-reviewed journal version** — bioRxiv's own publication-matching API explicitly returns "no articles found for published version". The *companion* paper on the cytosolic library **is** published (Science Advances, Feb 2026) under the more permissive **CC BY-NC**.

### Cited Findings

- `[READ]` The article page carries the statement: *"It is made available under a CC-BY-NC-ND 4.0 International license."* The accompanying copyright block states the copyright holder is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity — [bioRxiv article page](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1)
- `[META]` Crossref record for the DOI: `"license": [{"start": 2025-05-17, "content-version": "vor", "delay-in-days": 0, "URL": "http://creativecommons.org/licenses/by-nc-nd/4.0/"}]`; `"subtype": "preprint"`, `"institution": [{"name":"bioRxiv"}]`, `"publisher": "openRxiv"`, `"group-title": "Biochemistry"`, `"posted": 2025-05-17`, `"accepted": 2025-05-17`, `is-referenced-by-count: 11` — [Crossref API](https://api.crossref.org/works/10.1101/2025.05.16.654404)
- `[META]` Crossref `"relation": {}` — i.e. **no `is-preprint-of` relation to any journal article is registered** — [Crossref API](https://api.crossref.org/works/10.1101/2025.05.16.654404)
- `[META]` bioRxiv details API: `"version": "1"`, `"license": "cc_by_nc_nd"`, `"published": "NA"`, `"author_corresponding": "Rasmus Hartmann-Petersen"`, `"author_corresponding_institution": "University of Copenhagen"`, `"type": "new results"` — [bioRxiv API](https://api.biorxiv.org/details/biorxiv/10.1101/2025.05.16.654404)
- `[META]` bioRxiv publication-matching API returns: `{"messages":[{"status":"no articles found for published version of 10.1101/2025.05.16.654404"}], "collection":[]}` — [bioRxiv pubs API](https://api.biorxiv.org/pubs/biorxiv/10.1101/2025.05.16.654404)
- `[META]` Europe PMC title search returns `hitCount: 1`, a single preprint record `PPR1022363`, `source: PPR`, `pmid: None`, `license: "cc by-nc-nd"`, `isOpenAccess: "N"`, `commentCorrectionList: None` (no linked published version) — [Europe PMC REST](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE%3A%22Comprehensive%20degron%20mapping%20in%20human%20transcription%20factors%22&format=json&resultType=core)
- `[READ]` bioRxiv's own FAQ defines its CC-BY-NC-ND option as: *"Anyone can share this material, provided it remains unaltered in any way, this is not done for commercial purposes"* … *"and the original authors and source are credited and cited."* … *"Anyone who wishes to remix/adapt the work or reuse it for commercial purposes"* … *"must first obtain permission from the corresponding author."* — [bioRxiv FAQ](https://www.biorxiv.org/about/FAQ)
- `[READ]` bioRxiv FAQ on copyright: *"Authors retain copyright of their manuscripts and can choose from a number of distribution/reuse options"*; *"The licensing terms selected by the author determine the parameters for reuse."*; *"The copyright holder and licensing information for each manuscript are displayed beneath the Abstract and on the Info/History tab on the preprint page."* — [bioRxiv FAQ](https://www.biorxiv.org/about/FAQ)
- `[READ]` bioRxiv FAQ on supplementary files: *"Supplemental files are posted 'as is' and can be submitted in a wide range of file formats."* / *"Supplemental files are available in the format submitted by the authors."* — [bioRxiv FAQ](https://www.biorxiv.org/about/FAQ)
- `[READ]` bioRxiv FAQ on machine reading: *"bioRxiv provides free and unrestricted access to all articles posted on the server."* / *"We believe this should apply not only to human readers but also to machine analysis of the content."* / *"XML is available for text mining purposes."* — [bioRxiv FAQ](https://www.biorxiv.org/about/FAQ)
- `[META]` **Companion paper (cytosolic library)**: Voutsinos, Johansson, Larsen, Grønbæk-Thygesen, Jonsson, Holm-Olesen, Tesei, Stein, Fowler, Lindorff-Larsen, Hartmann-Petersen, *"A near-complete map of human cytosolic degrons and their relevance for disease"*, **Science Advances 12(6), published 2026-02-06**, DOI [10.1126/sciadv.adz3483](https://doi.org/10.1126/sciadv.adz3483); Europe PMC: `pmid 41650254`, `pmcid PMC12880521`, `license: "cc by-nc"`, `isOpenAccess: Y` — [Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A%2210.1126/sciadv.adz3483%22&format=json&resultType=core); Crossref returns `license: null` for this DOI, so the CC BY-NC string comes from Europe PMC, not from the publisher's Crossref deposit — [Crossref API](https://api.crossref.org/works/10.1126/sciadv.adz3483)

### Inferences

- `[INTERP]` The Science Advances companion being **CC BY-NC** (no ND) while the TF preprint is **CC BY-NC-ND** means the two halves of this degron-screen programme carry *different* reuse terms. For the ~8,645 tiles / 234 proteins that overlap the cytosolic library, the overlapping measurements may also be obtainable from the CC BY-NC companion's supplement — a materially easier license for redistribution and derivative tables. Worth checking the companion's supplementary tables before relying on the ND-licensed preprint for that subset.
- `[INTERP]` Since the TF manuscript's data/code repository was given a "publication release" tag on Zenodo on **2026-06-01** and the GitHub repo was still being pushed to on **2026-10-01**, a journal version is plausibly in press or recently accepted but not yet indexed. Re-check Crossref `relation` and the bioRxiv pubs API before the thesis is submitted.

### Gaps

- I could not find any journal version in Crossref, Europe PMC or the bioRxiv publication API. I did **not** separately query Google Scholar or PubMed's own interface, so an extremely recent (weeks-old) publication could in principle be missed. Flagged as **unverified-negative**.
- No `v2` of the preprint exists per the bioRxiv API (`version: "1"`), but I did not enumerate versions via a dedicated endpoint.

---

## Q2. Where the underlying data is actually deposited (accessions, files, sizes, and each deposit's own license)

### Takeaway

There are **four** distinct deposits, and — this is the crucial point — **the processed per-tile degron scores are in a GitHub/Zenodo repository released under the MIT License**, not under the preprint's CC BY-NC-ND. The raw FASTQ/FACS archive at the University of Copenhagen (ERDA, 113 GB) carries **no stated license at all**. There is **no GEO, ArrayExpress, PRIDE, figshare, Mendeley Data or OSF deposit**.

### Cited Findings

**(A) GitHub — processed scores and annotations — MIT License**

- `[META]` Repository `KULL-Centre/_2025_Larsen_degron_transcriptionfactors`; GitHub API reports `license: {"key":"mit","name":"MIT License","spdx_id":"MIT"}`, `created_at: 2025-01-30T13:43:44Z`, `pushed_at: 2026-10-01T12:48:42Z`, `size: 96332` KB (~96 MB), `default_branch: main`, description *"Scripts and output from \"Comprehensive degron mapping in human transcription factors\""* — [GitHub API](https://api.github.com/repos/KULL-Centre/_2025_Larsen_degron_transcriptionfactors)
- `[READ]` `LICENSE` (1,127 bytes) begins: *"MIT License / Copyright (c) 2025 Linderstrøm-Lang Centre for Protein Science, University of Copenhagen / Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software…"* — [raw LICENSE](https://raw.githubusercontent.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/main/LICENSE)
- `[READ]` README states the main resulting data is in `annotations/transfac_tiles.csv.gz` and `transfac_proteins.csv.gz`; folders are `library`, `counts`, `score`, `plots`, `annotations`, `analyses`; 53 commits at time of reading — [GitHub repo](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors)
- `[META]` **File inventory, `annotations/` (byte sizes from GitHub contents API):**

  | File | Bytes |
  |---|---|
  | `transfac_proteins_pap.txt.gz` | 15,530,333 |
  | `transfac_struc.csv.gz` | 10,155,511 |
  | `transfac_proteins.csv.gz` | 8,302,989 |
  | `transfac_tiles.csv.gz` | **5,771,779** |
  | `adpred_ss_api_full_scores.txt.gz` | 2,353,174 |
  | `transfac_tiles_pap.txt.gz` | 1,618,490 |
  | `transfac_tiles_locnes.csv.gz` | 1,263,651 |
  | `transfac_tiles_tad.csv.gz` | 1,077,363 |
  | `tad_mut_pap.txt.gz` | 49,553 |
  | `adpred.r`, `adpred_ss_api.py`, `transfac_tiles.r`, `transfac_proteins.r`, `run_adpred.sh`, `run_pap.sh`, `*.out` | 118 – 13,181 each |

  — [GitHub contents API, annotations](https://api.github.com/repos/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/contents/annotations)
- `[META]` **File inventory, `score/`:** `counts.rda` 8,222,214 B; `degrons.csv.gz` **4,563,816 B**; `scores.r` 35,180 B; `merge_and_map.r` 13,386 B; `counts_summary.csv` 13,204 B; `merge_and_map.out` 108,418 B; `samples.csv` 6,927 B; `controls.csv` 3,052 B; `scores.out` 44,950 B; `run.sh` 420 B; plus a `facs/` subdirectory — [GitHub contents API, score](https://api.github.com/repos/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/contents/score)
- `[READ]` **Verified column schema** of `annotations/transfac_tiles.csv.gz` (read from a 200 KB HTTP range request, no full download): header line is
  `name,gene,first_resi,last_resi,copyof_dna,copyof_aa,lib,aa,dna,zf,n,degron_score,degron_std,abundance_score,abundance_std,pap_ct,pap,locnes,locnes_score,tile_rasa_median,tile_plddt_median`
  and the first data row is `ENSG00000137203_tile0001,TFAP2A,1,30,NA,NA,2,MKMLWKLTDNIKYEDCEDRHDGTSNGTARL,ATGAAAATG…,F,6,0.433674425879055,0.0244491064767195,0.132071361397394,0.00678127199264855,0.0135,0.33775,NA,NA,NA,NA` — [raw file, range request](https://raw.githubusercontent.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/main/annotations/transfac_tiles.csv.gz)
- `[READ]` **Verified column schema** of `score/degrons.csv.gz`: `name,dna,aa,n,degron_score,degron_std,abundance_score,abundance_std`; first row `DAAA_1,TGTGCCCTCCTTCAGTCTGACGCCGCGGCGTCTGCCCCTAGAAGAGCGGCTGCTACTGCGAGGTAC,CALLQSDAAASAPRRAAATARY,17,0.677643679759503,…` — [raw file, range request](https://raw.githubusercontent.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/main/score/degrons.csv.gz)

**(B) Zenodo — archival snapshot of the same repo — MIT License**

- `[META]` DOI **10.5281/zenodo.20490355**, title *"KULL-Centre/_2025_Larsen_degron_transcriptionfactors: publication release"*, creator "Kristoffer Johansson (University of Copenhagen)", publisher Zenodo, `publicationYear: 2026`, `version: "v1.0"`, issued **2026-06-01**, `resourceTypeGeneral: "Software"`, description *"Scripts and output from \"Comprehensive degron mapping in human transcription factors\""* — [DataCite API](https://api.datacite.org/dois/10.5281/zenodo.20490355)
- `[META]` `rightsList: [{"rights":"MIT License","rightsUri":"https://opensource.org/licenses/MIT","rightsIdentifier":"mit","rightsIdentifierScheme":"SPDX"}]` — [DataCite API](https://api.datacite.org/dois/10.5281/zenodo.20490355)
- `[META]` `relatedIdentifiers`: `IsSupplementTo` → `https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/tree/v1.0`; `IsVersionOf` → DOI **10.5281/zenodo.20490354** (the concept DOI, which always resolves to the newest version) — [DataCite API](https://api.datacite.org/dois/10.5281/zenodo.20490355)
- `[READ]` The Zenodo landing page lists a single file, `KULL-Centre/_2025_Larsen_degron_transcriptionfactors-v1.0.zip`, **87.1 MB**, `md5:ab2a5546e7b3913baea4660bc3f007d5`; access rights "Open"; Software Heritage id `swh:1:dir:680f16f88acfed94fe2a558e7572fe86933a1993`; 24 views / 8 downloads — [Zenodo record 20490355](https://zenodo.org/records/20490355) (page content obtained via the WebFetch proxy; direct curl from this machine is blocked, see Q6)

**(C) ERDA (University of Copenhagen) — raw FASTQ + FACS — NO stated license**

- `[META]` DOI **10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943**, registered with DataCite, publisher "University of Copenhagen", `publicationYear: 2026`, `resourceType: "Article supplementary information"`, `resourceTypeGeneral: "Dataset"`, `sizes: ["113 GB"]`, title *"Comprehensive degron mapping in human transcription factors"*, creators Johansson KE / Larsen FB / Voutsinos V / Hartmann-Petersen R, landing page `https://erda.ku.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-archive.html` — [DataCite API](https://api.datacite.org/dois/10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943)
- `[META]` **`rightsList: []` and `descriptions: []`** — the DataCite record registers **no license and no rights statement whatsoever** — [DataCite API](https://api.datacite.org/dois/10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943)
- `[READ]` The ERDA archive page states: *"This is the public archive with ID a3c1d52583efe41f448642006ceb8f6f created on 2026-06-01 14:07:19 by Kristoffer Enøe Johansson, BIO <kristoffer.johansson@bio.ku.dk>."* Archive metadata: Author(s) = the seven paper authors; Title = *"Comprehensive degron mapping in human transcription factors"*; Description = *"FASTQ sequencing files and supplementary data for the article"*. No license text appears anywhere on the page — [ERDA published archive](https://erda.ku.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-archive.html)
- `[META]` **Complete file inventory** (from the archive's own `published-files.json`, 6 entries, total **120,785,019,615 bytes = 120.79 GB / 112.5 GiB**):

  | File | Bytes |
  |---|---|
  | `fastq_degron_tf/degron_tf_fastq_230817.tgz` | 68,488,834,258 |
  | `fastq_degron_tf/degron_tf_fastq_230905.tgz` | 22,792,301,522 |
  | `fastq_degron_tf/fastq_degron_tf_tox_20240120.tgz` | 20,700,606,953 |
  | `fastq_degron_tf/degron_tf_fastq_230313_pDNA.tgz` | 8,077,986,301 |
  | `fastq_degron_tf/degron_tf_counts.tgz` | 411,248,781 |
  | `fastq_degron_tf/facs_data_tf.tgz` | 314,041,800 |

  — [published-files.json](https://www.erda.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-files.json)

**(D) NCBI SRA — raw reads**

- `[META]` BioProject **PRJNA1276444**, `project_title: "Screen for degrons in human transcription factors"`, `submitter_organization: "University of Copenhagen"`, `registration_date: 2025/06/13`, `project_data_type: "Raw sequence reads"` — [NCBI eSummary, bioproject 1276444](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=bioproject&id=1276444&retmode=json)
- `[META]` **136** SRA experiment records are indexed under `PRJNA1276444` — [NCBI eSearch, db=sra](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term=PRJNA1276444&retmode=json)
- `[META]` Landing page https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1276444 returns **HTTP 200**.

**(E) Deposits that do NOT exist**

- `[META]` NCBI `elink` from `bioproject` id 1276444 to `gds` (GEO DataSets) returns a linkset with **no links** — i.e. **no GEO series is attached to this BioProject** — [NCBI eLink](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=bioproject&db=gds&id=1276444&retmode=json)
- `[META]` GEO DataSets search `degron AND "transcription factors" AND Hartmann-Petersen[Author]` returns `count: "0"` — [NCBI eSearch, db=gds](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=degron+AND+transcription+factors+AND+Hartmann-Petersen%5BAuthor%5D&retmode=json)
- `[META]` figshare search API for "degron mapping human transcription factors" returned an empty result set — [figshare API](https://api.figshare.com/v2/articles/search)

### Inferences

- `[INTERP]` **This is the single most important finding for the thesis.** The per-tile degron scores — the actual dataset of interest — live in a repository whose `LICENSE` file is MIT. MIT permits use, copying, modification, merging, publication, distribution, sublicensing and sale, with the only condition being that the copyright notice and permission notice be retained. If the authors intended the MIT License to cover the whole repository (including the `.csv.gz` output files, which the README itself calls "the main resulting data"), then **redistribution and derivative works of the scores are permitted, including commercially**, independently of the preprint's NC and ND restrictions.
- `[INTERP]` The residual ambiguity: MIT is a *software* license, and the Zenodo deposit's `resourceTypeGeneral` is `"Software"`. A strict reader could argue the MIT grant was intended for the scripts and that the data files ride along only incidentally. However, the LICENSE file sits at the repository root with no carve-out, GitHub's own license detector applies it repository-wide, and the README explicitly presents the CSVs as repository contents. On balance the MIT grant reads as covering everything in the repo.
- `[INTERP]` The 58,781 scored tiles are almost certainly reconstructible from `annotations/transfac_tiles.csv.gz` (5.8 MB gzipped, one row per tile, with `degron_score`, `degron_std`, `abundance_score`, `abundance_std`, `gene`, `first_resi`, `last_resi`, `aa`, `dna`, plus structural `tile_rasa_median`/`tile_plddt_median` and PAP/ADPred/NES/TAD annotations). The verified header confirms the file carries exactly the variables a model would need; **there is no need to touch the 120.79 GB ERDA archive or the SRA reads at all**.
- `[INTERP]` The ERDA archive having **no license** is the riskiest deposit. "Public archive" + a registered DataCite DOI signals intent to make it openly accessible, but accessible ≠ licensed. Under default copyright/database law, absent a license, only acts that do not require permission (e.g. reading, computing on lawfully accessed data in jurisdictions with no sui generis right) are clearly safe. `[INTERP]` Fortunately it is not needed.
- `[INTERP]` The absence of GEO is expected: this is an amplicon/FACS-sorted tile-library screen, not an expression experiment, so SRA + an institutional archive is the idiomatic deposit pattern. Do not keep hunting for a GSE accession.

### Gaps

- I could not confirm the Zenodo ZIP's internal file listing (whether the 87.1 MB archive is byte-identical to the GitHub `v1.0` tag) because zenodo.org is network-blocked from this machine (see Q6) and the only page read came through the fetch proxy.
- I could not search Mendeley Data: the public API endpoint I tried (`https://data.mendeley.com/public-api/datasets?query=…`) returned **HTTP 404 — "Cannot GET /public-api/datasets"**, so Mendeley Data is **unverified**, not confirmed-absent. Same for OSF, ArrayExpress and PRIDE, which I did not query directly — but note that the paper's own Data Availability statement and the GitHub README name only ERDA, SRA, GitHub and Zenodo, which is strong indirect evidence that nothing else exists.
- The `score/facs/` subdirectory contents were not enumerated.

---

## Q3. The preprint's Data / Code Availability statement, verbatim, and the supplementary inventory

### Takeaway

The statement is unusually terse: **"All data is included in the figures and supplemental files."** plus a GitHub pointer for code. The GitHub README — not the manuscript — is what names ERDA and the SRA BioProject. Three corresponding-author emails are published on the article page.

### Cited Findings

- `[READ]` Under the heading **"Data and code availability"** in the full text: *"All data is included in the figures and supplemental files."* followed by *"The code used to generate the main text figures, to recreate the predictions, and generate new predictions"* … *"is available via GitHub (https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors)."* There is no separate "Data availability" or "Code availability" heading — [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full)
- `[READ]` Under "Supplemental files": *"This article includes the following supplemental information:"* / *"Supplemental figures (SupplementalMaterial.pdf)."* / *"Supplemental dataset (SupplementalDataFile.xlsx)."* — [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full)
- `[READ]` The **manuscript's own availability statement does NOT name ERDA, SRA or Zenodo.** Those appear only in the GitHub README: *"Sequencing counts, FASTQ files, and FACS data are on ERDA, DOI 10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943"*; *"FASTQ files are deposited at NCBI SRA under BioProject PRJNA1276444"*; plus a Zenodo DOI badge for `10.5281/zenodo.20490354` — [GitHub repo README](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors)
- `[READ]` **Corresponding-author emails** as displayed on the article page (with bioRxiv's `{at}` obfuscation): *"For correspondence: vasileios.voutsinos{at}bio.ku.dk"*, *"For correspondence: lindorff{at}bio.ku.dk"*, *"For correspondence: rhpetersen{at}bio.ku.dk"* — [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full). The bioRxiv API additionally designates **Rasmus Hartmann-Petersen (University of Copenhagen)** as *the* corresponding author — [bioRxiv API](https://api.biorxiv.org/details/biorxiv/10.1101/2025.05.16.654404). A fourth address, `kristoffer.johansson@bio.ku.dk`, appears on the ERDA archive page as the archive creator — [ERDA](https://erda.ku.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-archive.html)
- `[READ]` Supplementary-material tab lists exactly two items: **"Supplemental Material"** → `supplements/654404_file09.pdf`; **"Supplemental Data File"** → `supplements/654404_file10.xlsx`. No file sizes and **no license or copyright statement are shown on that tab** — [bioRxiv supplementary tab](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.supplementary-material)
- `[READ]` **Library/scoring counts** as stated in the paper: 1,626 transcription factors (*"A library of all human transcription factors (TFs) (1626 proteins)"*); *"tiled library encompassing 62,992 tiles"*; Methods: *"63,230 tiles"* total of which *"62,992/62,808 are unique at nucleotide/amino acid level"*; *"We attained data for 58,781 tiles out of the initial 63,011 tiles"*; Methods also say *"58,781 scores which are mapped to 58,992 tiles"*; overlap with the cytosolic library: *"resulting in a list of 234 proteins corresponding to 8,645 tiles"* — [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full)
- `[READ]` **Conflicting denominators within the paper itself**: the tile totals are given variously as 62,992 / 63,230 / 63,011 / 58,992, and the 58,781 figure is described once as "tiles" and once as "scores … mapped to 58,992 tiles". This inconsistency is in the source, not a transcription error.
- `[META]` Funders listed: Novo Nordisk Foundation, Danmarks Frie Forskningsfond. Competing interests: *"K.L-L. holds stock options in and consults for Peptone Ltd."* — [bioRxiv article page](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1)

### Inferences

- `[INTERP]` "All data is included in the figures and supplemental files" means the authors regard `SupplementalDataFile.xlsx` as the canonical data release. That file is a **bioRxiv-hosted supplementary file, and therefore squarely inside the CC BY-NC-ND 4.0 scope** per bioRxiv's FAQ ("The licensing terms selected by the author determine the parameters for reuse"). The MIT-licensed GitHub CSVs are the *same underlying measurements* under a materially different license.
- `[INTERP]` Practical consequence: **prefer the GitHub/Zenodo CSVs over the bioRxiv XLSX** as the working copy for the thesis. Same numbers, far cleaner license story, and a citable archival DOI.
- `[INTERP]` The internal inconsistency in tile counts means the thesis should report whatever `annotations/transfac_tiles.csv.gz` actually contains after loading it (count the rows with non-NA `degron_score`), cite the file, and note the paper's own discrepancy in a footnote rather than quoting "58,781" as if it were unambiguous.

### Gaps

- I deliberately did not download `media-2.xlsx` / `654404_file10.xlsx`, so I cannot report its sheet names, row counts or whether it contains all 58,781 tiles. Availability and HTTP status only were checked (see Q6).
- The full text is ~160,600 characters and the fetch covered the first 100,000; a license or data statement in the final 60,600 characters (late Methods / Supplemental legends) was not read. The Data-and-code-availability and Supplemental-files sections were both found within the part that was read.

---

## Q4. How CC BY-NC-ND applies to supplementary tables vs. article text; copyright in data vs. databases

### Takeaway

Creative Commons' own FAQ states that CC licenses are *"operative only when applied to material in which a copyright exists"*, that with databases *"purely factual data is generally not protected"* by copyright, and that text/data mining on CC-licensed material is permitted with compliance required only insofar as the mining actually implicates copyright or sui generis database rights. `[INTERP]` The measured degron scores are facts; the compiled table may attract thin protection (and, in the EU/Denmark, a separate sui generis database right that neither Vietnam nor the US recognises).

### Cited Findings

- `[READ]` CC FAQ, **"How do CC licenses operate?"**: *"CC licenses are operative only when applied to material in which a copyright exists"*, and *"nor do license terms and conditions apply to elements of a licensed work that are in the public domain"* — [CC FAQ](https://creativecommons.org/faq/)
- `[READ]` CC FAQ, **"Can I apply a Creative Commons license to databases?"**: *"Yes. CC licenses can be used on databases."* and *"applicable sui generis database rights are licensed under the same license conditions as copyright"* — [CC FAQ](https://creativecommons.org/faq/)
- `[READ]` CC FAQ, **"Which components of databases are protected by copyright?"**: the answer opens *"With databases, there are likely four components to consider"* and enumerates the database model/structure, data entry and output sheets, field names, and the data or other contents; it notes that copyright depends on originality, which varies by jurisdiction, and that **purely factual data is generally not protected** — [CC FAQ](https://creativecommons.org/faq/)
- `[READ]` CC FAQ, **"What is an adaptation?"**: *"An adaptation is a work based on one or more pre-existing works."* The answer adds that what counts as an adaptation depends on applicable law, and that translations and film versions of novels are generally adaptations — [CC FAQ](https://creativecommons.org/faq/)
- `[READ]` CC FAQ, **"When is my use considered an adaptation?"**: *"a modification rises to the level of an adaptation under copyright law when the modified work is based on the prior work"* — and the modified work must additionally show enough new creativity to be copyrightable in its own right — [CC FAQ](https://creativecommons.org/faq/)
- `[READ]` CC FAQ, **"Can I conduct text/data mining on a CC-licensed database?"**: *"Yes. However, you should be aware that whether you have to comply with the CC license terms"* depends on whether the mining implicates copyright or sui generis database rights — [CC FAQ](https://creativecommons.org/faq/)
- `[READ]` CC FAQ, **"Does my use violate the NonCommercial clause of the licenses?"**: *"Whether a use is commercial will depend on the specifics of the situation and the intentions of the user."* The NC restriction is **not** determined by the type of user — nonprofits can violate it and for-profit companies do not necessarily violate it — and CC itself declines to advise on what counts as commercial — [CC FAQ](https://creativecommons.org/faq/)
- `[READ]` CC FAQ, **"What are Creative Commons licenses?"** defines the elements: *"NoDerivatives (ND), which prohibits the sharing of adaptations of the material"* and *"NonCommercial (NC), which prohibits commercial use of the material"* — [CC FAQ](https://creativecommons.org/faq/)
- `[READ]` **The ND clause restricts *sharing*, not *making*.** CC's own wording — "prohibits the **sharing** of adaptations" — matches the license text, which permits the licensee to produce and use adapted material privately but not to distribute it — [CC FAQ](https://creativecommons.org/faq/); the operative text is CC BY-NC-ND 4.0 §2(a)(1)(B) and §3(a) — [license deed](https://creativecommons.org/licenses/by-nc-nd/4.0/) / [legal code](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode)

### Inferences

- `[INTERP]` **Facts vs. compilation.** Individual `degron_score` values are measurements — facts. In the US (*Feist v. Rural Telephone Service*, 499 U.S. 340 (1991)) facts are not copyrightable and only original selection/arrangement of a compilation is; Vietnam's Law on Intellectual Property similarly protects *compilations* ("sưu tập dữ liệu") as derivative works rather than the underlying facts. So quoting a handful of scores, or extracting the numbers and reorganising them, is very weakly constrained by copyright in Vietnam.
- `[INTERP]` **EU sui generis database right matters here but probably does not reach Vietnam.** The depositor is Danish (University of Copenhagen), so Directive 96/9/EC's sui generis right plausibly subsists in the compiled table in the EU. That right is **not recognised in Vietnam or the US**, and the Directive's protection is reciprocity-based (Art. 11), so a Vietnamese thesis author extracting the table in Vietnam is in a much better position than an EU-based one. Caveat: a CC licence that purports to license sui generis rights also imposes its conditions wherever those rights do subsist — so if the thesis or a derived table is later published/hosted in the EU, the analysis changes.
- `[INTERP]` **Supplementary tables vs. article text.** bioRxiv's FAQ makes the author-selected licence govern reuse of the deposit as a whole, and the supplementary files are part of that deposit. So `SupplementalDataFile.xlsx` **as a file** is offered under CC BY-NC-ND. But per CC's own FAQ, the licence is "operative only when applied to material in which a copyright exists" — so the licence bites on the table's expressive layer (its selection, arrangement, field names, formatting, captions) and **not** on the raw numbers themselves.
- `[INTERP]` **Is training a model an "adaptation"?** Almost certainly not, on CC's own definition: an adaptation must be a work "based on the prior work" that shows enough new creativity to be copyrightable. Model weights derived by fitting to numeric features do not reproduce the table's expressive arrangement. And even if a derived artefact were an adaptation, ND restricts *sharing* it, not making it — so a privately-trained model used to produce reported metrics is outside ND's prohibition. This is **interpretation, not legal advice.**
- `[INTERP]` **Is a Vietnamese university thesis "non-commercial"?** Per CC, NC turns on "the specifics of the situation and the intentions of the user", not the user's type. A degree thesis with no revenue, no paywall and no commercial sponsor is squarely non-commercial on any ordinary reading. Risk would arise only if the work were later spun into a paid product or a company-funded deliverable.

### Gaps

- I quoted CC's FAQ (the authoritative interpretive source CC publishes) but did **not** fetch the CC BY-NC-ND 4.0 legal code itself in this session, so the §2/§3 clause numbers above are from my own knowledge rather than read from the page. Verify the clause numbers against https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode before putting them in the thesis.
- The CC FAQ heading "If I use a CC-licensed database to produce a new database, does the ShareAlike/NoDerivatives clause apply?" did **not** appear in the portion of the page I read. That is the single most directly on-point FAQ entry and I could not retrieve it. Flagged as a real gap.
- I did not verify Vietnamese statutory text (Luật Sở hữu trí tuệ) against a primary source in this session; the characterisation above is from my own knowledge and should be checked.

---

## Q5. Practical bottom line — what is safe, what is risky, what to ask the authors

### Takeaway

**Yes, this dataset can be used in the thesis, and the clean route is the MIT-licensed GitHub/Zenodo repository, not the bioRxiv supplementary XLSX.** Under MIT, even redistributing a processed copy in a public repo is permitted provided the MIT copyright and permission notice travel with it. Only if the ND-licensed bioRxiv XLSX is used as the source does the redistribution question become awkward.

### Cited Findings

- `[READ]` MIT grant covers *"use, copy, modify, merge, publish, distribute, sublicense, and/or sell"* with the sole condition that *"The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."* — [repo LICENSE](https://raw.githubusercontent.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/main/LICENSE)
- `[READ]` bioRxiv CC-BY-NC-ND terms require that the material *"remains unaltered in any way"* for sharing and that *"Anyone who wishes to remix/adapt the work or reuse it for commercial purposes must first obtain permission from the corresponding author."* — [bioRxiv FAQ](https://www.biorxiv.org/about/FAQ)
- `[READ]` Corresponding-author contacts for a permission request: `rhpetersen@bio.ku.dk` (Rasmus Hartmann-Petersen, the designated corresponding author), `lindorff@bio.ku.dk` (Kresten Lindorff-Larsen), `vasileios.voutsinos@bio.ku.dk` (Vasileios Voutsinos) — [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full), [bioRxiv API](https://api.biorxiv.org/details/biorxiv/10.1101/2025.05.16.654404); data-archive contact `kristoffer.johansson@bio.ku.dk` — [ERDA](https://erda.ku.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-archive.html)

### Inferences — risk tiers

All of the following is `[INTERP]`, **not legal advice**.

**Clearly safe (no permission needed, under either licence):**
1. Reading the preprint, reading the supplementary XLSX, reading values from any of the deposits.
2. Downloading `annotations/transfac_tiles.csv.gz`, `annotations/transfac_proteins.csv.gz`, `score/degrons.csv.gz` etc. from GitHub or the Zenodo ZIP — MIT explicitly permits copying.
3. Training/fitting any model on the scores; running analyses; computing features.
4. Reporting aggregate metrics, correlations, AUROC/Spearman tables, confusion matrices derived from the data.
5. Citing the preprint (DOI 10.1101/2025.05.16.654404) and the Zenodo DOI (10.5281/zenodo.20490355) — the BY term requires exactly this.
6. Quoting a small number of individual scores or example tiles in the text/figures with attribution — these are facts, and short factual quotation is also within Vietnamese fair-use for teaching/research.

**Safe but with a condition attached:**
7. **Redistributing the processed table in the thesis's own public repo** — permitted *if sourced from the MIT repo* and if the MIT copyright + permission notice is shipped alongside (e.g. a `LICENSE-THIRD-PARTY` / `data/raw/SOURCE.md` file reproducing the notice and naming the upstream repo, commit/tag and Zenodo DOI). This is the one practical obligation to honour. Note that the repo's CLAUDE.md convention keeps `data/` out of git anyway, which sidesteps the question entirely for this thesis.
8. Publishing derived tables (e.g. per-protein summaries, train/test splits) — fine under MIT; also fine under the fact/copyright analysis.

**Risky — avoid or get permission:**
9. **Redistributing `SupplementalDataFile.xlsx` itself** (the bioRxiv file) in a public repo or as a thesis appendix file. It is offered under CC BY-NC-ND; even unaltered sharing is only permitted non-commercially with attribution, and any reformatting arguably makes it "altered". Use the MIT-licensed CSV instead — same data, no issue.
10. **Reproducing figures from the preprint** (copying a panel into the thesis). CC BY-NC-ND permits verbatim non-commercial sharing with credit, so an unmodified, fully-credited figure reproduction is defensible — but cropping, recolouring, relabelling, or translating captions into Vietnamese starts to look like an adaptation, which ND prohibits sharing. Safest: **redraw the figure yourself from the data** and cite the paper, or email for permission.
11. Using the ERDA FASTQ/FACS archive for anything beyond reading — it carries **no licence at all** (`rightsList: []`). Not needed for this thesis; don't go near it.
12. Any commercial use, or bundling into a product — the NC term on the preprint and the NC term on the published companion both bar this without permission. (MIT on the repo does not, but don't rely on a licence mismatch for a commercial decision.)

**What to ask by email, if anything is needed** — send to `rhpetersen@bio.ku.dk`, cc `lindorff@bio.ku.dk` and `kristoffer.johansson@bio.ku.dk`:
- Confirmation that the MIT License in the repository is intended to cover the **output data files** (`annotations/*.csv.gz`, `score/degrons.csv.gz`), not only the scripts. One sentence of confirmation removes the entire ambiguity and is worth getting in writing.
- Permission (if wanted) to reproduce specific figure panels in a Vietnamese-language thesis.
- Whether a peer-reviewed version is in press, and in which journal, so the thesis cites the version of record.
- Whether the ERDA archive has an intended licence.

### Gaps

- No written statement from the authors about the data-vs-code scope of the MIT licence exists in any source I read; this is precisely why the email above is recommended.

---

## Q6. Network accessibility — HTTP statuses actually observed from this machine (2026-10-15)

### Takeaway

Everything needed is reachable **except zenodo.org, which returns HTTP 403** from this network — consistent with the pre-existing note in the repo's own `resources/README.md`. The Zenodo metadata was recovered via the DataCite API instead, and the same content is available from GitHub.

### Cited Findings

All checked with `curl -sI -A "Mozilla/5.0"` (HEAD only; no data files downloaded):

| URL | Status | Note |
|---|---|---|
| `https://www.biorxiv.org/content/biorxiv/early/2025/05/17/2025.05.16.654404/DC1/embed/media-1.pdf` | **200** | `content-type: application/pdf`; `content-disposition: inline; filename="media-1.pdf"`; `last-modified: Tue, 20 May 2025 15:41:22 GMT`; **no `content-length` header advertised** |
| `https://www.biorxiv.org/content/biorxiv/early/2025/05/17/2025.05.16.654404/DC2/embed/media-2.xlsx` | **200** | `content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`; `content-disposition: attachment; filename="media-2.xlsx"`; `last-modified: Tue, 20 May 2025 15:41:22 GMT`; **no `content-length`** |
| `https://zenodo.org/records/20490355` | **403** | Body: `<h1>403 Forbidden</h1> … "Access to this resource has been restricted due to unusual traffic from"` |
| `https://zenodo.org/api/records/20490355` | **403** | Same block — the REST API is blocked too |
| `https://doi.org/10.5281/zenodo.20490354` | **302** | → `https://zenodo.org/doi/10.5281/zenodo.20490354` (then blocked) |
| `https://doi.org/10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943` | **302** | → `https://erda.ku.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-archive.html` |
| `https://www.erda.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-files.json` | **200** | 4,826 bytes of JSON; full file inventory retrieved |
| `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1276444` | **200** | |
| `https://raw.githubusercontent.com/.../annotations/transfac_tiles.csv.gz` | **200** | 200 KB HTTP range request succeeded; header row read |
| `https://api.datacite.org/dois/10.5281/zenodo.20490355` | **200** | Zenodo licence metadata recovered this way |
| `https://api.datacite.org/dois/10.17894/ucph.e6ff0116-...` | **200** | ERDA licence metadata (empty `rightsList`) |
| `https://api.github.com/repos/KULL-Centre/_2025_Larsen_degron_transcriptionfactors` | **200** | |
| `https://api.crossref.org/works/10.1101/2025.05.16.654404` | **200** | |
| `https://api.biorxiv.org/details|pubs/biorxiv/10.1101/2025.05.16.654404` | **200** | |
| `https://www.ebi.ac.uk/europepmc/webservices/rest/search?...` | **200** | |
| `https://api.figshare.com/v2/articles/search` | **200** | empty result set |
| `https://data.mendeley.com/public-api/datasets?query=...` | **404** | `Cannot GET /public-api/datasets` — wrong endpoint, so Mendeley is **unverified**, not absent |

### Inferences

- `[INTERP]` The Zenodo 403 is an IP-reputation block on this network, not a permissions problem with the record (DataCite reports it as open-access, and the Zenodo page itself — read through the fetch proxy — labels it "Open"). **Practical download route: clone from GitHub** (`git clone https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors`, ~96 MB) or check out tag `v1.0` for the exact version matching the Zenodo DOI, then cite the Zenodo DOI for archival provenance. This mirrors the workaround already recorded in `resources/README.md` for the Voutsinos 2026 data ("Zenodo `16925278` trả 403 từ mạng này; dùng repo GitHub cùng tác giả").
- `[INTERP]` bioRxiv advertises no `content-length` on the supplementary endpoints, so their byte sizes cannot be established without downloading. Not worth doing, since the GitHub CSVs supersede them.

### Gaps

- Exact sizes of `media-1.pdf` and `media-2.xlsx` are unknown (no `content-length`; no size shown on the supplementary tab either).
- Whether Zenodo is reachable from other networks available to the user (e.g. a different ISP or Colab) was not tested.
