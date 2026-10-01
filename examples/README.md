# Examples

Example prompts for the `osdr-biodata-api` skill and the answers you should
expect. The **expected results are the same in every client** — they come
from the live API — so they are collected here once; the per-client files
show how the skill is invoked in that client and what a complete answer
looks like there.

| Client | File |
|---|---|
| Claude (claude.ai, desktop, Cowork, Claude Code) | [`claude.md`](claude.md) |
| ChatGPT / Codex | [`chatgpt.md`](chatgpt.md) |
| Gemini (Spark web app, Gemini CLI) | [`gemini.md`](gemini.md) |
| VS Code / GitHub Copilot | [`vscode-copilot.md`](vscode-copilot.md) |

Counts were taken from the live API in September 2026; OSDR grows, so
expect small increases over time. `BASE` =
`https://visualization.osdr.nasa.gov/biodata/api`.

---

## E1 — Simple discovery with titles

**Prompt:** *List all Drosophila datasets in OSDR with their titles.*

**Expected:** one `/datasets/` call, 17 datasets.

```
BASE/v2/query/datasets/?study.characteristics.organism=/drosophila/&investigation.study.study%20title&format=json.records
```

| Accession | Title (abridged) |
|---|---|
| OSD-1 | Expression data from drosophila melanogaster |
| OSD-3 | Drosophila melanogaster gene expression changes after spaceflight |
| OSD-27 | Transcription profiling of Drosophila exposed to a levitation magnet … |
| OSD-34 | Environmental and simulation facility conditions can modulate a behavioral-driven altered … |
| OSD-36 | Transcription profiling of Drosophila after exposure to microgravity in the ISS |
| OSD-70 | Environmental and facility conditions promote singular gravity responses of transcriptome … |
| OSD-85 | Transcriptomic response of Drosophila melanogaster pupae developed in hypergravity |
| OSD-96 | The development of Drosophila melanogaster during space flight |
| OSD-207 | Correlated Gene and Protein Expression in heads from Drosophila reared in microgravity |
| OSD-278 | Spaceflight and simulated microgravity conditions increase virulence of Serratia marcescens … |
| OSD-347 | Heart Flies – effect of microgravity on heart function in Drosophila |
| OSD-514, OSD-592, OSD-595, OSD-596 | Artificial gravity partially protects space-induced neurological deficits in Drosophila … |
| OSD-588 | Drosophila parasitoids go to space … |
| OSD-590 | First transcriptome profiling of D. melanogaster after development in a deep underground … |

The answer ends with the URL run and the reminder to cite each study's DOI
and dataset version.

---

## E2 — Mission discovery with anchored regex and aliases

**Prompt:** *Which OSDR datasets come from the RR-1 mission, and what assays and tissues do they include?*

**Expected:** one `/assays/` call, **80 rows → 25 datasets**. The regex is
anchored (`RR-1([^\d]|$)`) so RR-10…RR-19 are excluded, and `RR-1_BSP`
(OSD-212, 16S faeces) and comma-joined labels (`RR-1, RR-3`; `RR-1, RR-9`)
are included.

```
BASE/v2/query/assays/?investigation.study.comment.Project%20Identifier=/RR-1([^\d]|$)|RR1([^\d]|$)/&investigation.study%20assays.study%20assay%20technology%20type&study.characteristics.material%20type&format=json.records
```

| Accession | Assays | Tissue(s) |
|---|---|---|
| OSD-47 | Microscopy, RNA-seq, WGBS, mass spectrometry | Liver |
| OSD-48 | Microscopy, RNA-seq, WGBS, WTBS, mass spectrometry | Liver |
| OSD-98 | RNA-seq, WGBS, mass spectrometry | Adrenal glands |
| OSD-99 | RNA-seq, WGBS | Extensor digitorum longus |
| OSD-101 | RNA-seq, WGBS, WTBS, mass spectrometry | Left gastrocnemius |
| OSD-102 | RNA-seq, WGBS, WTBS, mass spectrometry | Left kidney |
| OSD-103 | RNA-seq, WGBS, WTBS, mass spectrometry | Left quadriceps femoris |
| OSD-104 | RNA-seq, WGBS | Soleus |
| OSD-105 | RNA-seq, WGBS, WTBS, mass spectrometry | Left tibialis anterior |
| OSD-164 | RNA-seq | Liver, Spleen |
| OSD-168 | RNA-seq | Liver (RR-1, RR-3) |
| OSD-212 | 16S | Feces (RR-1_BSP) |
| OSD-397 | RNA-seq, RRBS | Left / right retina |
| OSD-419 | RNA-seq | Right gastrocnemius |
| OSD-488 | Spectrofluorimetric assay, Western blot | Soleus, tibialis anterior (RR-1, RR-9) |
| OSD-489 | Micro-CT | Lumbar vertebra 4 |
| OSD-662 | Contractility, Microscopy, Western blot | Soleus (RR-1, RR-9, RR-18, Bion-M1, GROUND-2) |
| OSD-702 | Atomic force microscopy | Quadriceps femoris |
| OSD-738 | ECLIA, Western blot | Brain |
| OSD-751 / OSD-752 | ECLIA | Cortex / Hippocampus |
| OSD-804 | Micro-CT | Femur, Vertebrae |
| OSD-952 | Behavioral segmentation, Pose estimation | Whole organism |
| OSD-969 / OSD-970 | real-time PCR | Brown / White adipose tissue |

---

## E3 — Sample-level filter

**Prompt:** *Find female mouse liver samples.*

**Expected:** one `/samples/` call, ~**820 samples**, grouped by dataset in
the answer, with a note that the fallback (factor value ↔ characteristic
for sex) was not needed.

```
BASE/v2/query/samples/?study.characteristics.organism=/musculus/&study.characteristics.material%20type=/liver/&study.characteristics.sex=/female/&format=json.records
```

---

## E4 — GeneLab-processed differential expression (unambiguous)

**Prompt:** *Show me the differentially expressed genes for OSD-515, space flight vs ground control.*

**Expected:** three steps — list files, confirm the single contrast, pull
rows — then the output contract.

1. `BASE/v2/dataset/OSD-515/files/` → two DE files; pin
   `GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv` (not the
   `_rRNArm_` variant).
2. Contrast `(Space Flight)v(Ground Control)` is the only flight-vs-ground
   comparison, so no question is needed.
3. Data pull with default columns and adj p ≤ 0.05:

```
BASE/v2/query/data/?id=OSD-515&file.filename=GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv&column.ENSEMBL&column.SYMBOL&column.Log2fc_(Space%20Flight)v(Ground%20Control)&column.Adj.p.value_(Space%20Flight)v(Ground%20Control)%3C=0.05&column.Stat_(Space%20Flight)v(Ground%20Control)&column.Group.Mean_(Space%20Flight)&column.Group.Stdev_(Space%20Flight)&column.Group.Mean_(Ground%20Control)&column.Group.Stdev_(Ground%20Control)&format=json.records
```

**3,947 significant genes** (2,795 up, 1,152 down in space flight).

Top 10 up-regulated by log2FC:

| ENSEMBL | SYMBOL | log2FC | adj p | Wald stat | Mean SF | SD SF | Mean GC | SD GC |
|---|---|---|---|---|---|---|---|---|
| ENSMUSG00000099908 | — | 21.02 | 1.0e-05 | 5.68 | 20.8 | 46.6 | 1.0 | 0.0 |
| ENSMUSG00000112022 | Gm2436 | 6.26 | 3.6e-02 | 2.83 | 23.7 | 29.5 | 1.2 | 0.5 |
| ENSMUSG00000027157 | Potefam1 | 6.00 | 6.9e-03 | 3.61 | 12.5 | 16.2 | 1.0 | 0.0 |
| ENSMUSG00000073063 | Hbq1b | 5.34 | 3.5e-05 | 5.33 | 18.2 | 24.8 | 1.4 | 1.1 |
| ENSMUSG00000120464 | — | 5.26 | 7.9e-05 | 5.12 | 12.5 | 12.2 | 1.3 | 0.6 |
| ENSMUSG00000022441 | Efcab6 | 4.52 | 4.5e-04 | 4.62 | 85.5 | 108.5 | 4.6 | 5.1 |
| ENSMUSG00000078597 | Cyp4a12b | 4.52 | 1.1e-02 | 3.40 | 1030.5 | 1571.7 | 46.0 | 74.3 |
| ENSMUSG00000056162 | Cndp1 | 4.34 | 8.9e-03 | 3.49 | 5.5 | 5.5 | 1.1 | 0.2 |
| ENSMUSG00000022759 | Lrrc74b | 4.29 | 1.1e-02 | 3.38 | 221.3 | 277.4 | 12.2 | 16.0 |
| ENSMUSG00000048939 | Atp13a5 | 4.23 | 4.5e-02 | 2.70 | 226.3 | 370.0 | 13.0 | 23.1 |

Top 10 down-regulated by log2FC:

| ENSEMBL | SYMBOL | log2FC | adj p | Wald stat | Mean SF | SD SF | Mean GC | SD GC |
|---|---|---|---|---|---|---|---|---|
| ENSMUSG00000095923 | — | −4.51 | 1.0e-02 | −3.43 | 1.5 | 0.6 | 11.6 | 18.4 |
| ENSMUSG00000095338 | Igkv3-9 | −3.79 | 4.9e-02 | −2.66 | 1.6 | 1.0 | 7.5 | 14.8 |
| ENSMUSG00000094315 | Igkv4-78 | −3.56 | 2.2e-02 | −3.07 | 1.4 | 0.7 | 5.2 | 5.1 |
| ENSMUSG00000029019 | Nppb | −3.02 | 1.8e-02 | −3.17 | 13.8 | 14.3 | 104.1 | 214.6 |
| ENSMUSG00000097083 | — | −2.95 | 1.5e-03 | −4.21 | 2.0 | 1.3 | 9.3 | 5.8 |
| ENSMUSG00000059003 | Grin2a | −2.90 | 2.0e-02 | −3.12 | 1.6 | 0.9 | 7.8 | 8.9 |
| ENSMUSG00000043549 | Fam90a1b | −2.59 | 2.2e-03 | −4.07 | 1.9 | 0.9 | 7.6 | 4.0 |
| ENSMUSG00000116864 | — | −2.57 | 1.8e-02 | −3.17 | 2.0 | 2.2 | 7.6 | 4.6 |
| ENSMUSG00000041550 | Serpina5 | −2.56 | 4.1e-03 | −3.82 | 2.1 | 0.8 | 8.1 | 3.5 |
| ENSMUSG00000094322 | Ighv9-4 | −2.42 | 2.0e-02 | −3.12 | 31.5 | 35.0 | 163.1 | 260.6 |

The answer ends with: *Would you like a downloadable CSV of all 3,947
significant genes?*

---

## E5 — Ambiguous comparison: list and ask

**Prompt:** *Get the differentially expressed genes for flight vs ground in OSD-48 with adj p < 0.05 and |log2FC| > 1.*

**Expected:** the assistant reads
`GLDS-48_rna_seq_contrasts_GLbulkRNAseq.csv` (not the `_GLMethylSeq`
contrasts file), sees that groups combine two factors (Spaceflight ×
Euthanasia location), and finds **two** flight-vs-ground comparisons. It
**does not run either**; it asks:

> OSD-48 has two flight-vs-ground comparisons:
> 1. `(Space Flight & Carcass)v(Ground Control & Carcass)`
> 2. `(Space Flight & Upon euthanasia)v(Ground Control & Upon euthanasia)`
>
> Which one would you like? (The other contrasts in the file compare
> carcass vs upon-euthanasia within a condition, or cross conditions.)

After you choose (1), the answer follows the E4 contract (635 genes at
adj p ≤ 0.05; then filtered to |log2FC| > 1).

---

## E6 — Cohort intersection across datasets

**Prompt:** *Which animals appear in both OSD-102 and OSD-104, and what tissues and assays does each have?*

**Expected:** two `/samples/` calls (one per dataset, with Source Name and
Project Identifier), subject IDs built as `RR-1 | <Source Name>`
(e.g. `RR-1 | RR1_FLT_M23`), **12 shared subjects**, a table of subject →
tissue (kidney / soleus) → assays. 76 rows are returned in total across the
two calls.

---

## E7 — Set difference

**Prompt:** *Which Rodent Research datasets used only female mice?*

**Expected:** ~**89 datasets**. Either two `/datasets/` calls (all RR
datasets; RR datasets with any male sample) and a set difference, or one
`/samples/` call with sex grouped per dataset. The answer states the method.

---

## E8 — Host organism (microbiome)

**Prompt:** *List all amplicon sequencing datasets where a plant was the host organism.*

**Expected:** ~**11 datasets** (26 assay rows) from a `/assays/` call using
`study.characteristics.host%20organism` with a plant-genus OR regex.

---

## E9 — "Has GeneLab-processed data"

**Prompt:** *Which Inspiration4 datasets contain GeneLab-processed data files?*

**Expected:** exactly **OSD-572, OSD-573, OSD-574, OSD-630** (metagenomics,
whole-genome shotgun), from

```
BASE/v2/query/datasets/?investigation.study.comment.Project%20Identifier=/Inspiration/&file.category=/genelab%20processed/&file.filename=/^(?!.*(fastqc|multiqc|md5sum)).*/&file.category&format=json.records
```

The other six Inspiration4 datasets have only FastQC/MultiQC reports in that
category and must **not** be listed.

**Prompt:** *List all Inspiration4 datasets that contain data files.*

**Expected:** this does **not** say "processed", so no FastQC/MultiQC
filter: one call with bare `&file.category`, returning all **10**
Inspiration4 datasets (OSD-569, 570, 571, 572, 573, 574, 575, 630, 656, 687)
with their file categories (raw and GeneLab-processed).

```
BASE/v2/query/datasets/?investigation.study.comment.Project%20Identifier=/Inspiration/&file.category&format=json.records
```

**Prompt:** *Which Rodent Research liver datasets have GeneLab-processed data, and of what type?*

**Expected:** 9 datasets with their processed-file category; OSD-137 is
listed as RNA-seq (not WGBS).

---

## E10 — Microbial differential expression (single matching contrast)

**Prompt:** *List the differentially expressed genes for OSD-145 flight vs ground control comparison, filtered to adj p < 0.05 and |log2FC| > 1.*

**Expected:** OSD-145 is *Staphylococcus aureus* RNA-seq. The organism does
not change the file type — the request says *differential expression*, so the
`GLDS-145_rna_seq_differential_expression_GLbulkRNAseq.csv` file is used (not
a differential-abundance table). The contrasts file has two factors
(spaceflight × frozen) but only **one** flight-vs-ground column,
`(Space Flight & Frozen)v(Ground Control & Frozen)`, so the assistant proceeds
without asking and never offers a non-existent "Not frozen" spaceflight
contrast.

```
BASE/v2/query/data/?id=OSD-145&file.filename=GLDS-145_rna_seq_differential_expression_GLbulkRNAseq.csv&column.Log2fc_(Space%20Flight%20%26%20Frozen)v(Ground%20Control%20%26%20Frozen)&column.Adj.p.value_(Space%20Flight%20%26%20Frozen)v(Ground%20Control%20%26%20Frozen)%3C=0.05&column.Stat_(Space%20Flight%20%26%20Frozen)v(Ground%20Control%20%26%20Frozen)&column.Group.Mean_(Space%20Flight%20%26%20Frozen)&column.Group.Stdev_(Space%20Flight%20%26%20Frozen)&column.Group.Mean_(Ground%20Control%20%26%20Frozen)&column.Group.Stdev_(Ground%20Control%20%26%20Frozen)&format=json.records
```

`column.SYMBOL` is requested as usual (animal and plant tables have it); here
it returns HTTP 500 because this microbial table has no `SYMBOL`, so the same
URL is rerun without it. `gene_id` comes back automatically and is the first
column of every table. **1,513** genes at adj p ≤ 0.05; **239** with |log2FC| > 1
(168 up, 71 down).

Top 5 up / top 5 down by log2FC:

| gene_id | log2FC | adj p | Wald stat | Mean SF | SD SF | Mean GC | SD GC |
|---|---|---|---|---|---|---|---|
| QV15_10390 | 6.92 | 9.5e-199 | 30.29 | 9207.8 | 2537.9 | 76.9 | 39.2 |
| QV15_00805 | 4.42 | 4.2e-76 | 18.77 | 1228.8 | 667.5 | 58.2 | 14.3 |
| QV15_10410 | 3.96 | 1.4e-254 | 34.31 | 37769.0 | 6707.0 | 2423.1 | 504.7 |
| QV15_10405 | 3.94 | 2.5e-240 | 33.32 | 35928.7 | 6097.5 | 2341.7 | 531.7 |
| QV15_10400 | 3.93 | 1.4e-172 | 28.23 | 3618.3 | 702.1 | 238.2 | 64.7 |
| QV15_01890 | −3.43 | 1.1e-164 | −27.57 | 1096.5 | 286.6 | 11818.8 | 1424.4 |
| QV15_01885 | −3.11 | 1.1e-97 | −21.26 | 653.5 | 201.3 | 5627.0 | 519.4 |
| QV15_00850 | −2.63 | 2.0e-14 | −8.01 | 896.6 | 502.2 | 5549.3 | 2525.7 |
| QV15_08145 | −2.10 | 5.4e-03 | −3.06 | 2.0 | 1.2 | 5.3 | 3.6 |
| QV15_12890 | −2.03 | 5.9e-15 | −8.16 | 3043.5 | 854.0 | 12466.5 | 7697.1 |

The answer notes that no gene symbols are annotated, offers to list the
file's other columns, and ends with the CSV offer.

---

## E11 — Dataset report

**Prompt:** *Tell me about OSD-248: what was studied, what are the treatment groups and how many samples in each?*

**Expected:** `BASE/v2/dataset/OSD-248/` (title, description, DOI,
organism, assays) plus one `/samples/` call with the factor columns; a
groups table with sample counts (58 samples in total); DOI and the version
reminder.

---

## E12–E14 — Out-of-scope redirects (no biodata query)

| Prompt | Expected first sentence |
|---|---|
| *Show me the temperature and CO₂ readings on ISS during RR-1.* | Environmental telemetry is outside this skill; use the OSDR Environmental Data Application: https://visualization.osdr.nasa.gov/eda/ |
| *List all human astronaut datasets in OSDR.* | NASA astronaut / crew data are not in the biodata API; see NLSP (https://nlsp.nasa.gov/), LSDA (https://lsda.jsc.nasa.gov/) and LSAH. |
| *I need physical tissue samples from the RR-9 mice for my own assay — how do I get them from OSDR?* | Physical biospecimens are distributed by NBISC (https://nbisc.arc.nasa.gov/), not the biodata API. |

In all three the assistant builds **no** `/biodata/api` URL and does not
probe `/eda/api`, `/radlab/…` or any other guessed endpoint.
