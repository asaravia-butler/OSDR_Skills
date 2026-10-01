# OSDR Biodata API — Field Reference

Contents: 1 Field paths · 2 Aliases and variants · 3 Live vocabularies
(organism, technology, measurement, project identifier, spaceflight, sex,
file data type) · 4 Factor-value and characteristic sub-fields · 5 File fields

Field names are ISA-Tab paths in dot notation. URL-encode spaces as `%20`.
Names are case-insensitive on input and are returned lower-cased.
Values matched with `=/regex/` are case-insensitive; `=exact` must equal the
whole stored value.

## 1. Field paths

| Concept | Field path (URL-encoded) | Notes |
|---|---|---|
| Dataset accession | `id.accession` | `OSD-###`; always returned |
| Assay name | `id.assay%20name` | returned on assays/samples |
| Sample name | `id.sample%20name` | returned on samples/metadata; requesting it on `/assays/` expands rows to samples |
| Source name (animal/plant/culture ID within a study) | `study.source%20name` | subject ID = project identifier + source name |
| Organism | `study.characteristics.organism` | amplicon/microbiome studies store `Microbiota` here — see host organism |
| Host organism (microbiome / 16S / ITS) | `study.characteristics.host%20organism` | plus `host%20strain`, `host%20sex`; vocabulary in §3 |
| Tissue / material | `study.characteristics.material%20type` | primary tissue field for animal studies; also `study.characteristics.organism%20part` (populated in ~112 datasets, mostly Arabidopsis/plant and microbiome, a few mouse), `study.factor%20value.tissue`, `study.factor%20value.organism%20part` |
| Sex | `study.characteristics.sex` | fallback `study.factor%20value.sex` |
| Strain | `study.characteristics.strain` | fallback `study.factor%20value.strain` |
| Genotype | `study.characteristics.genotype` | fallback `study.factor%20value.genotype` |
| Age | `study.characteristics.age` | see §2 variants |
| Cell line / cell type | `study.characteristics.cell%20line`, `study.characteristics.cell%20type` | |
| All characteristics | `study.characteristics` | bare prefix → every characteristic column |
| Spaceflight factor | `study.factor%20value.spaceflight` | values in §3 |
| Radiation factors | `study.factor%20value.ionizing%20radiation`, `study.factor%20value.absorbed%20radiation%20dose` | |
| Ground-analog factors | `study.factor%20value.hindlimb%20unloading`, `study.factor%20value.microgravity%20simulation`, `study.factor%20value.altered%20gravity` | |
| Any factor by name | `study.factor%20value.<name>` | |
| All factors | `study.factor%20value` | bare prefix → every factor column |
| Study protocol parameters | `study.parameter%20value` | e.g. preservation, dissection |
| Assay parameters | `assay.parameter%20value` | e.g. library layout, instrument |
| Technology type | `investigation.study%20assays.study%20assay%20technology%20type` | values in §3 |
| Measurement type | `investigation.study%20assays.study%20assay%20measurement%20type` | values in §3; `=/behavior/` is the handle for behavioural data |
| Technology platform | `investigation.study%20assays.study%20assay%20technology%20platform` | e.g. Illumina NovaSeq; useful output column |
| Project / mission / ground-study identifier | `investigation.study.comment.Project%20Identifier` | values in §3 |
| Study title | `investigation.study.study%20title` | regex on words works as a crude keyword search |
| Study DOI | `investigation.study.comment.doi` | citation; populated for ~94% of studies |
| Flight vs ground | `investigation.study.comment.project%20type` | values are inconsistently cased (`Spaceflight Study`, `Spaceflight study`, `Spaceflight`, `Ground Study`, `Ground study`, `High Altitude Study`, `Parabolic Study`) — always regex `/spaceflight/`, `/ground/`, `/altitude/` |
| Launch / mission name | `investigation.study.comment.mission%20name` | e.g. `SpaceX-4`, `SpaceX-16`; cross-check for missions — a few datasets (OSD-100) have a null project identifier |
| Mission dates | `investigation.study.comment.mission%20start`, `…mission%20end` | MM/DD/YYYY |
| Space agency | `investigation.study.comment.space%20program` | NASA, JAXA, ESA, DLR |
| All study comments | `investigation.study.comment` | bare prefix → every comment column |
| File name | `file.filename` | `file.file%20name` is an accepted alias |
| File subcategory | `file.subcategory` | vocabulary in §3 |
| File data type | `file.data%20type` | controlled values in §3 |
| File category | `file.category` | `GeneLab Processed <assay> Files`; vocabulary and caveat in §3 |
| Download URL (relative) | `file.remote_url` | prefix `https://osdr.nasa.gov` |

## 2. Aliases and variants (try in this order)

| Concept | Try first | Then |
|---|---|---|
| age | `study.characteristics.age` | `study.characteristics.age%20at%20launch`, `…age%20at%20experiment%20start`, `…age%20at%20irradiation`, `…age%20at%20assay`, `study.factor%20value.age` |
| tissue | `study.characteristics.material%20type` | `study.characteristics.organism%20part`, `study.factor%20value.tissue`, `study.factor%20value.organism%20part`, `study.factor%20value.material%20type` |
| sex | `study.characteristics.sex` | `study.factor%20value.sex` |
| strain | `study.characteristics.strain` | `study.factor%20value.strain`, `study.characteristics.strain%20or%20line`, `study.characteristics.ecotype` (plants) |
| treatment / dose | `study.factor%20value.treatment` | `study.factor%20value.dose`, `study.factor%20value.absorbed%20radiation%20dose`, `study.characteristics.treatment` |
| duration / time | `study.factor%20value.time` | `study.factor%20value.duration`, `study.characteristics.duration`, `study.factor%20value.time%20of%20sample%20collection%20after%20treatment` |
| mission | `investigation.study.comment.Project%20Identifier` | `investigation.study.comment.mission%20name`, `study.characteristics.launch%20mission`, `study.characteristics.mission`, `study.factor%20value.space%20mission` |
| host (microbiome) | `study.characteristics.host%20organism` | `study.characteristics.host%20strain`, `…host%20sex` |

Fastest way to learn a study's real names: bare prefixes on one accession.
`…/v2/query/assays/?id.accession=OSD-104&study.characteristics&study.factor%20value&format=json.records`

## 3. Live vocabularies (counts = datasets or assays at time of capture)

### Organism (`study.characteristics.organism`, top values, dataset counts)
Mus musculus 246 · Homo sapiens 114 · Arabidopsis thaliana 62 · Microbiota 47 ·
Rattus norvegicus 36 · Drosophila melanogaster 17 · Caenorhabditis elegans 14 ·
Bacillus subtilis 7 · Saccharomyces cerevisiae 6 · Escherichia coli 6 ·
Lactuca sativa 6 · Staphylococcus aureus 5 · Pseudomonas aeruginosa 4 ·
Danio rerio 4 · Raphanus sativus 4 · (182 distinct in total; many microbes)
Regex tips: `/musculus/` mouse, `/rattus/` rat, `/sapiens/` human,
`/arabidopsis/` plant model, `/musculus|rattus/` rodents.

### Host organism (`study.characteristics.host%20organism`, amplicon assay rows)
Homo sapiens 124 · Not Applicable 36 · Lactuca sativa 33 · Brassica rapa 11 ·
Capsicum annuum 11 · Mus musculus 8 · Solanum lycopersicum 8 · Raphanus
sativus 6 · Pisum sativum 6 · Triticum aestivum 4 · Rattus norvegicus 1.
Plant hosts: `/lactuca|brassica|capsicum|solanum|raphanus|pisum|triticum/`.

### Technology type (`…technology%20type`, assay counts)
RNA Sequencing (RNA-Seq) 236 · DNA microarray 157 · mass spectrometry 56 ·
nucleotide sequencing 41 · Western Blot 36 · single-cell RNA sequencing 31 (+4
with different capitalisation) · 16S 29 · Whole-Genome Shotgun Sequencing 24 ·
miRNA Sequencing 18 · Whole Genome Bisulfite Sequencing 14 ·
Micro-Computed Tomography 12 · spatial transcriptomics 11 · Microscopy 10 ·
real time PCR 10 · ITS 7 · Immunohistochemistry 6 · Reduced-Representation
Bisulfite Sequencing 5 · Whole Transcriptome Bisulfite Sequencing 5 ·
Immunostaining 5 · Dual-Energy X-Ray Absorptiometry 5 · single-cell ATAC-seq 4 ·
Ribo-seq 4 · Flow Cytometry 4 · Tonometry 2 · (91 distinct)
Regex tips: `/rna-seq/` matches only `RNA Sequencing (RNA-Seq)` (bulk, 236);
`/rna%20sequencing|rna-seq/` also matches single-cell (35), miRNA (18) and
long-read RNA sequencing — say which you used; `/microarray/`;
`/bisulfite/` all methylation; `/16S|ITS/` amplicon; `/shotgun|metagenomic/`;
`/mass%20spectrometry/` proteomics/metabolomics; `/single-cell/`.

### Measurement type (`…measurement%20type`)
transcription profiling 465 · protein expression profiling 41 · Amplicon
Sequencing 37 · genome sequencing 37 · protein quantification 36 · Metagenomic
sequencing 31 · DNA methylation profiling 30 · Behavior 28 · Molecular Cellular
Imaging 23 · Bone Microstructure 19 · metabolite profiling 15 · Immunoassay 7 ·
RNA methylation profiling 5 · Chromatin Accessibility 4 · (54 distinct)
Behaviour: `=/behavior/` → 28 assays / 12 datasets. Technology types under it:
Gait, Elevated Plus Maze, Novel Object Recognition, Open Field, RAWM, Three
Chamber Social Isolation, Balance, Forced Swim Test, Anhedonia, Psychomotor
Vigilance Test, Video Recording, Locomotory Behavior, Behavioral Segmentation,
Pose Estimation. Do not put `activity` in a behaviour regex (matches enzyme assays).

### Project identifier (`investigation.study.comment.Project%20Identifier`)
Spaceflight missions: `RR-1` 21, `RR-3` 7, `RR-4`, `RR-5`, `RR-6` 7, `RR-7`,
`RR-8`, `RRRM-1 (RR-8)` 30, `RR-9` 13, `RR-10` 8, `RR-17` 9, `RR-18` 5,
`RR-23` 12, `Bion-M1` 5, `Inspiration4 Crew` 10, `ISS-MO` 10, `Microbial
Tracking-1A/1B/2`, `MHU-1/2/3/8` (JAXA), `MVP-Fly-01`, `BRIC-16/17/23`,
`APEX-04`, `APEX03-2`, `VEG-04A/B`, `VEG-05`, `CERISE`, `FIT`, `Space Biofilms`,
`CubeLab_HSAPIENS_SpaceX-19`, `STS-###`.
Ground studies use category tokens (comma-joined when several):
`Simulated_Microgravity` 43, `Simulated_Environmental_Factors` 24,
`Hindlimb_Unloading` 20, `Gamma_Irradiation`, `Low_LET_Irradiation`,
`High_LET_Irradiation`, `Heavy_Ion_HZE_Irradiation`, `Proton_Irradiation`,
`X-Ray_Irradiation`, `High_Dose_Irradiation`, `Low_Dose_Irradiation`,
`Simplified_Galactic_Cosmic_Ray_Simulation_Irradiation`,
`Solar_Particle_Event_Simulation_Irradiation`, `Multiple_Radiation_Types`,
`Simulated_Hypergravity`, `GROUND-2`. (213 distinct values)
Value forms to expect: `RR-1`, `RR-1, RR-3` (comma-joined, multi-mission),
`RR-1_BSP`, `RRRM-1 (RR-8)`, `Inspiration4 Crew`, `MVP-Fly-01`, `FFL-01` /
`FFL01` / `FFL-02` / `FFL03` (inconsistent hyphenation), `CubeLab_HSAPIENS_SpaceX-19`.
**Aliases (RRRM = Rodent Research Reference Mission):** `RRRM-1 (RR-8)` is the
RR-8 payload (30 datasets stored that way, 2 stored as plain `RR-8`); `RR-17`
is RRRM-2 (stored as `RR-17`). Count each pair as one mission.
Regex tips: one mission `/RR-1([^\d]|$)/` (else RR-1 also matches RR-10…RR-18);
any Rodent Research `/^RR-?\d|^RRRM/` (unanchored `/RR/` matches
"I**rr**adiation" and adds ~50 ground studies; `^` works server-side);
`/Irradiation/` any radiation ground study; `/Hindlimb_Unloading/`; `/Inspiration/`;
`/FFL-?0\d/`. For mission questions filter on this field, never on organism
(Inspiration4: 10 datasets by project, 7 by `organism=/sapiens/`).

### Spaceflight factor (`study.factor%20value.spaceflight`)
`Space Flight` 454 · `Ground Control` 368 · `Vivarium Control` 76 ·
`Basal Control` 41 · `Not Applicable` 24 · `pre-flight`/`post-flight`/
`in-flight` (human & some rodent) · `Cohort Control #1/#2` · `Baseline Control`.
Regex tips: `/space%20flight|in-flight/` flown samples; `/control/` any control.

### Sex
`study.characteristics.sex`: Female 159 datasets, Male 116 (+ lower-case
variants), Not Applicable 19. `study.factor%20value.sex`: Male 49, Female 46.
Always use `/female/` `/male/` regex (case-insensitive); note `/male/` also
matches `Female` — use `/^male/` for males only. QC/pool samples carry
`Not Applicable`.

### Material type quirks
Blood is inconsistently named: `Whole Blood`, `Whole blood`, `Peripheral
Blood`, `blood plasma`, `Plasma`, `Blood`, `RBC pellet; Whole Blood` — use
`/blood|plasma/`. `/liver/` also matches `Left lobe of liver` (fine).
Proteomics studies often carry `Not Applicable`. In-vitro human work is
`Cells` / `Cells, Cultured`.

### Curation anomalies
Sanity-check organism against the study title: e.g. OSD-832/833/834 (WAG/Rij
rats) are tagged *Homo sapiens*.

### File category and subcategory (`file.category`, `file.subcategory`)
`file.category` = `GeneLab Processed <assay> Files` for pipeline outputs
(`…RNA-Seq Files`, `…long read RNA-Seq Files`, `…Whole Genome Sequencing`,
`…scRNAseq Files`, `…snRNAseq Files`, `…snATACseq Data Files`,
`…Metagenomics Files`, `…Spatial Transcriptomics Data Files`,
`…Chromatin Immunocleavage Sequencing ` (trailing space — use regex)).
**Caveat:** raw MultiQC reports are curated under these categories with
`file.subcategory = Merged Sequence Data`; exclude that subcategory when the
question is "has GeneLab-processed *data*". `!=` on metadata endpoints is
unverified — filter client-side.
`file.subcategory` values seen: `Differential gene expression analysis`,
`Normalized Counts Data`, `Raw Counts Tables`, `Normalized Data`,
`Differential Abundance`, `Differential Methylation Analysis Data`,
`Methylation Call Data`, `Raw sequence data`, `Trimmed Sequence Data`,
`Merged Sequence Data`, `Filtered Sequence Data`, `FastQC Outputs`,
`Read-based Processing`, `Assembly-based Processing`, `Processing Info`, `README`.
Neither field is present in `/v2/dataset/OSD-###/files/` (only `URL`, `REST_URL`).

### File data type (`file.data%20type`, controlled vocabulary)
raw reads · trimmed reads · alignment · raw/trimmed fastqc report/data ·
raw/trimmed multiqc report/data · unnormalized counts · normalized counts ·
differential expression table · differential expression contrasts · sample
table · pca · visualization table · differential methylation bases ·
differential methylation tiles · differential abundance table.
Many carry a ` - supplementary` suffix (e.g. `differential expression table -
supplementary` for rRNArm variants). Match with regex:
`file.data%20type=/differential%20expression%20table/`.

## 4. Factor-value and characteristic sub-fields (most common, sample counts)

Factor values (`study.factor%20value.<name>`): ionizing radiation 8154 ·
absorbed radiation dose 7382 · strain 7260 · time of sample collection after
treatment 7197 · group id 6383 · spaceflight 3310 · time 1204 · treatment 1113 ·
altered gravity 801 · genotype 760 · sample location 626 · organism part 510 ·
age 510 · sex 484 · hindlimb unloading 411 · dissection condition 410 ·
euthanasia location 368 · microgravity simulation 350 · duration 243 ·
tissue 206 · assay time post-irradiation 174 · temperature 165 · altered
gravity simulator 148 · growth environment 102 · dose 75 · diet 57 ·
preservation method 49 · infection 47 · bed rest 37 · cell line 18 (145 distinct).

Characteristics (`study.characteristics.<name>`): organism 4196 · material type
3758 · strain 2502 · sex 2305 · animal source 1958 · genotype 1590 · duration
1181 · age at experiment start 1121 · body mass at euthanasia 1119 · age 644 ·
study subject 338 · developmental stage 332 · age at launch 271 · host organism
264 · diet 214 · organism part 181 · cell type 166 · cell line 160 · mission
collected 114 · ecotype 84 · age at irradiation 82 · launch mission 33 ·
cultivar 29 · age at assay 44 (169 distinct).

## 5. File fields — how they combine

On `/v2/query/assays/` (or `/samples/`), adding any `file.*` field makes one
row per file. Typical file-listing query:
```
…/v2/query/assays/?id.accession=OSD-104&file.filename=/./&file.subcategory&file.data%20type&file.remote_url&format=json.records
```
Narrow with `file.filename=/differential_expression/`, `/Normalized_Counts/`,
`/fastq\.gz/`, `/tiff|png/`, etc.
