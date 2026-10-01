# Standardized processed files (GeneLab pipelines) and `/v2/query/data/`

Contents: 1 Naming rules · 2 Three-step pull recipe · 3 Group/contrast names ·
4 Per-omics file lists and columns · 5 Sizes and limits · 6 "Has GeneLab-processed data" via file.category

## 1. Naming rules

GeneLab processes every assay with a versioned pipeline (GL-DPPD documents at
`github.com/nasa/GeneLab_Data_Processing`) that writes files with a fixed
suffix token. Deposited names add a prefix:

```
GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv
GLDS-515_rna_seq_differential_expression_rRNArm_GLbulkRNAseq.csv   <- rRNA-removed variant
GLDS-47_Gwgbs_differential_methylation_tiles_GLMethylSeq.csv
GLDS-3_array_differential_expression_GLmicroarray.csv
GLDS-1_array_differential_expression.csv                           <- legacy, no token
```

Rules:
- Match by regex on the stable core, not a literal: `file.filename=/differential_expression/`.
- Many RNA-seq datasets have BOTH a plain and an `_rRNArm_` (rRNA-removed)
  file. Prefer the plain one unless the user asks; the `rRNArm` one is tagged
  `file.data type = differential expression table - supplementary`.
- Legacy datasets (e.g. OSD-1) have no `_GL…` token. If a token regex finds
  nothing, retry without it.
- `/v2/query/data/` must resolve to ONE file; otherwise HTTP 422
  `Request resolves to multiple files that cannot be merged`.

## 2. Three-step pull recipe (list files → read contrasts → pull rows)

```
# A. list files (fast, small)
BASE/v2/query/assays/?id.accession=OSD-515&file.filename=/differential_expression|Counts|contrasts|abundance|methylation/&file.subcategory&format=json.records

# B. read the contrasts file (exact group strings; see §3) — use the name from step A;
#    a bare /contrasts_GL/ gives 422 when the study also has a methylation contrasts file
BASE/v2/query/data/?id=OSD-515&file.filename=/contrasts_GLbulkRNAseq/&format=json.records

# C. pull one file's rows — exact name from step A, contrast strings from step B
BASE/v2/query/data/?id=OSD-515&file.filename=GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv&column.*&format=csv
```

Row/column controls on `/v2/query/data/`:

| Parameter | Effect |
|---|---|
| `column.*` | all columns |
| `column.SYMBOL` | select one column (repeatable) |
| `column.Adj.p.value_(Space%20Flight)v(Ground%20Control)%3C=0.05` | keep rows where column ≤ 0.05 (also selects it) |
| `column.Log2fc_(Space%20Flight)v(Ground%20Control)%3E=1` | keep rows where column ≥ 1 |
| operators | `%3C` < · `%3E` > · `%3C=` ≤ · `%3E=` ≥ · `!=` |

Without any `column.` parameter the API returns the index column plus every
filtered column only. Column names in the response are prefixed
`OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/`.

Server-side comparison operators apply to **one column in one direction**.
For |log2FC| > 1 filter adj p server-side and apply the fold-change cut
client-side, or issue two requests (`%3E=1` and `%3C=-1`). Unannotated rows
have SYMBOL/GENENAME as JSON `null` or the string `"NaN"` — handle both.

Typical "significant genes" call:
```
BASE/v2/query/data/?id=OSD-515&file.filename=GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv&column.SYMBOL&column.Log2fc_(Space%20Flight)v(Ground%20Control)&column.Adj.p.value_(Space%20Flight)v(Ground%20Control)%3C=0.05&format=json.records
```
(3,947 rows; add `&column.Log2fc_(Space%20Flight)v(Ground%20Control)%3E=1` → 2,066 rows up-regulated.)

## 3. Group and contrast names

A sample **group** is one unique combination of the study's factor values
(any number of factors) joined with ` & ` inside parentheses, e.g.
`(Space Flight)`, `(Space Flight & Left kidney)`,
`(Space Flight & ~60 day & On ISS & Carcass)`. A **contrast** is
`(group1)v(group2)`; all pairs exist in both directions, and the same group
names are used in differential methylation and differential abundance files
and in the `Group.Mean_`/`Group.Stdev_` columns. Build a study's groups from
`BASE/v2/query/samples/?id.accession=OSD-###&id.assay%20name=/rna-seq/&study.factor%20value&format=json.records`
(distinct combinations of the `study.factor value.*` columns, with n); the
contrasts file gives the exact spelling and factor order (e.g. OSD-48 writes
spaceflight first, OSD-95 writes dose first). If the user's comparison matches
several contrasts, list them and ask which they want. Statistic columns embed the contrast:
`Log2fc_(Space Flight)v(Ground Control)`. URL-encode spaces only:
`Log2fc_(Space%20Flight)v(Ground%20Control)`.

**Always read the contrasts file before building a `column.` filter** — it
is tiny and it is the only reliable source of the exact strings. Two-factor
studies have NO single-factor contrast: OSD-48 (RR-1 liver, factors
spaceflight × dissection condition) offers only
`(Space Flight & Carcass)v(Ground Control & Carcass)` and
`(Space Flight & Upon euthanasia)v(Ground Control & Upon euthanasia)`;
answer "flight vs ground" with the like-for-like pairs.
```
BASE/v2/query/data/?id=OSD-515&file.filename=/contrasts_GLbulkRNAseq/&format=json.records
```
Its column names are the contrasts, e.g. `(Space Flight)v(Ground Control)`,
`(Ground Control)v(Vivarium Control)`. Microarray files contain contrasts in
both directions; amplicon (16S/ITS) files write `(group2)v(group1)`.

Legacy datasets have no contrasts file: read the header line of
`…&column.*&format=csv` instead (stream and stop after the first line).
Multi-factor groups contain ` & `, which must be encoded as `%26`:
`Adj.p.value_(Space%20Flight%20%26%20uninfected)v(Ground%20Control%20%26%20uninfected)`.
A `column.` name that does not exist returns HTTP 500; an unencoded `&`
returns HTTP 400 `Invalid characters in field name`. Files the API has not
tabulated (e.g. the methylation `contrasts_GLMethylSeq.csv`) answer
`422 Requested data only available in format=raw`: add `&format=raw` and the
API redirects to the file's download URL on osdr.nasa.gov (follow with
`curl -L`, or read the header locally).

## 4. Per-omics files and columns

### Bulk RNA-seq — GL-DPPD-7101, token `_GLbulkRNAseq`
Files: `differential_expression_GLbulkRNAseq.csv`, `Normalized_Counts_GLbulkRNAseq.csv`,
`VST_Counts_GLbulkRNAseq.csv`, `RSEM_Unnormalized_Counts_GLbulkRNAseq.csv`,
`STAR_Unnormalized_Counts_GLbulkRNAseq.csv`, `SampleTable_GLbulkRNAseq.csv`,
`contrasts_GLbulkRNAseq.csv` (each may also exist as `_rRNArm_`).
Subcategories: `Differential gene expression analysis`, `Normalized Counts Data`,
`Raw Counts Tables`.
DE columns: identifier first — `ENSEMBL` (animals), `TAIR`/`LOCUS` (plants),
`gene_id` (microbes; e.g. OSD-95, OSD-145) — always returned even when not
requested; then `SYMBOL` (animal and plant tables, and some microbe tables;
absent ones return 500 if requested → rerun without it), `GENENAME`, `REFSEQ`,
`ENTREZID`, `STRING_id`, `GOSLIM_IDS` (animals); one column per sample, then per contrast
`Log2fc_`, `Stat_`, `P.value_`, `Adj.p.value_`, then `All.mean`, `All.stdev`,
`LRT.p.value`, `Group.Mean_(group)`, `Group.Stdev_(group)`.

### Microarray — GL-DPPD-7114 (Affymetrix) / 7112 (Agilent), token `_GLmicroarray`
Files: `differential_expression_GLmicroarray.csv`,
`normalized_expression_probeset_GLmicroarray.csv`,
`normalized_intensities_probe_GLmicroarray.csv`, `SampleTable_GLmicroarray.csv`,
`contrasts_GLmicroarray.csv`, `visualization_PCA_table_GLmicroarray.csv`.
Subcategories: `Differential gene expression analysis`, `Normalized Data`.
DE columns: annotation block + `ProbesetID` (Affy) or `ProbeUID`/`ProbeName`
(Agilent), per-sample values, per contrast `Log2fc_`, `T.stat_`, `P.value_`,
`Adj.p.value_`, then `All.mean`, `All.stdev`, `F`, `F.p.value`, group stats.
Legacy files (no token) exist for early datasets (OSD-1…).

### Methylation-seq — GL-DPPD-7113, token `_GLMethylSeq` (RNA methylation: `_GLRNAMethylSeq`)
Files: `differential_methylation_bases_GLMethylSeq.csv`,
`differential_methylation_tiles_GLMethylSeq.csv`, `SampleTable_GLMethylSeq.csv`,
`contrasts_GLMethylSeq.csv`; per-sample Bismark `*.bismark.cov.gz`, `*.bedGraph.gz`.
DM columns: gene annotation, `feature.name`, `chr`, `start`, `end`, `strand`,
`dist.to.feature`, `prom`, `exon`, `intron`, per-sample % methylation, per
contrast `meth.diff_`, `pvalue_`, `qvalue_`.

### Amplicon 16S / ITS — GL-DPPD-7104, token `_GLAmpSeq`
Differential abundance is written once per method — pick by token:
`ancombc1_differential_abundance_16S_GLAmpSeq.csv`,
`ancombc2_differential_abundance_16S_GLAmpSeq.csv`,
`deseq2_differential_abundance_16S_GLAmpSeq.csv` (`ITS` infix for fungal).
Subcategory: `Differential Abundance`. Feature tables:
`taxonomy-and-counts_GLAmpSeq.tsv`, `counts_GLAmpSeq.tsv`, `taxonomy_GLAmpSeq.tsv`,
`ASVs_GLAmpSeq.fasta`.
DA columns: `ASV`, `domain`…`species`, `taxonomy`, `NCBI id`, per-sample
abundance, then per contrast — DESeq2: `baseMean_`, `Log2fc_`, `lfcSE_`,
`Stat_`, `P.value_`, `Adj.p.value_`; ANCOMBC: `Lnfc_`, `Lnfc.SE_`, `Stat_`,
`P.value_`, `Q.value_`, `Diff_` (ANCOMBC2 adds `Passed_ss_`).
Verified example: `…/v2/query/data/?id=OSD-267&file.filename=/ancombc1_differential_abundance_16S_GLAmpSeq\.csv/&format=csv` (134 ASV rows).

### Metagenomics — GL-DPPD-7107, token `_GLmetagenomics`
Taxonomy tables, gene-family/KO tables, pathway abundance/coverage, assemblies,
MAGs. **No standardized differential-abundance file** — say so; the user
computes it from the tables.

### Single-cell RNA-seq — GL-DPPD-7111
Standardized outputs stop at STARsolo count matrices (`barcodes.tsv`,
`features.tsv`, `matrix.mtx`) with generic names and no `_GL` token. No
standardized clustering, marker, or DE tables.

For any other omics type, check `github.com/nasa/GeneLab_Data_Processing` for
its GL-DPPD document; if no standard name is found, say so rather than guess.

## 5. Sizes and limits

- A full DE table with `column.*` is 10–60 MB (OSD-515: 16 MB json; OSD-1
  microarray: 58 MB csv). Select columns or filter rows, or download the file
  via its `file.remote_url` (`https://osdr.nasa.gov` + relative path) and
  filter locally.
- Some fetch proxies refuse large bodies with a generic 403; that is a payload
  problem, not a URL problem.
- Queries with no filters (`/v2/query/samples/` alone → 51 k rows, 7.5 MB)
  take a few seconds; typical filtered queries return in 1–10 s, but broad
  ones can hit the gateway's ~60 s limit (HTTP 504): retry the same URL.

## 6. "Has GeneLab-processed data" via `file.category`

Use this only when the user asks for *GeneLab-processed* / *processed* data.
"Datasets with data files" (any kind) = bare `&file.category` with no filter.

`file.category=/genelab%20processed/` labels pipeline outputs for every omics
type, **but the same category also holds QC-only files** (FastQC/MultiQC
reports, md5 lists, subcategory `Merged Sequence Data`), so many datasets
carry the label with no real output (Inspiration4: 8 labelled, 4 real;
OSD-905 has only MultiQC reports). Always add the filename exclusion:

```
…&file.category=/genelab%20processed/&file.filename=/^(?!.*(fastqc|multiqc|md5sum)).*/&file.category&format=json.records
```
The negative look-ahead works server-side. Verified: Inspiration4 → OSD-572,
573, 574, 630 (metagenomics); Rodent Research liver → 9 datasets, OSD-47/48
with RNA-Seq + WGBS output, OSD-137 RNA-Seq only. Report the `file.category`
values per dataset as the data types that were processed. Never run
`file.category` repository-wide without an accession, project or technology
filter — it times out.
