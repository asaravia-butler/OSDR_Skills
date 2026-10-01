# Examples — Claude

Applies to claude.ai (browser), the Claude desktop app, Cowork and Claude
Code. Installation: [`../docs/install-claude.md`](../docs/install-claude.md).
Expected results for every example: [`README.md`](README.md).

**Status:** the transcripts below were produced with the 1.0.0 package on
Claude Sonnet and Haiku and checked on Opus (September 2026). Row counts may
have grown since.

## How the skill is invoked

- claude.ai / desktop: ask the question; a **"Using osdr-biodata-api"**
  chip appears above the response. No slash command is needed.
- Claude Code / Cowork: ask, or type `/osdr-biodata-api <question>`. Claude
  runs `curl -g …` or `python3 scripts/osdr_query.py …`; approve the tool
  call when prompted.
- Claude cites the URLs it ran at the end of every answer; you can paste
  them into a browser to see the raw JSON.

---

## Transcript 1 — E1, simple discovery

**You:** List all Drosophila datasets in OSDR with their titles.

**Claude:**

> Using osdr-biodata-api
>
> I found **17 Drosophila datasets** in OSDR:
>
> | Accession | Title |
> |---|---|
> | OSD-1 | Expression data from drosophila melanogaster |
> | OSD-3 | Drosophila melanogaster gene expression changes after spaceflight |
> | OSD-27 | Transcription profiling of Drosophila exposed to a levitation magnet … |
> | … | … |
> | OSD-596 | Artificial gravity partially protects space-induced neurological deficits in Drosophila melanogaster |
>
> Note that OSD-514, 592, 595 and 596 share one title (one study split into
> several datasets by assay/tissue).
>
> **Query run:**
> `https://visualization.osdr.nasa.gov/biodata/api/v2/query/datasets/?study.characteristics.organism=/drosophila/&investigation.study.study%20title&format=json.records`
>
> When citing, use each study's DOI (`investigation.study.comment.doi`) and
> state the dataset version.

---

## Transcript 2 — E4, differential expression with the output contract

**You:** Show me the differentially expressed genes for OSD-515, space flight vs ground control.

**Claude:**

> Using osdr-biodata-api
>
> **Step 1 – files.** OSD-515 has two GeneLab bulk RNA-seq DE tables; I used
> `GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv` (the standard
> one, not the rRNA-removed variant).
>
> **Step 2 – contrast.** The study has one flight-vs-ground comparison:
> `(Space Flight)v(Ground Control)`.
>
> **Step 3 – results.** **3,947 genes** are significant at adjusted
> p ≤ 0.05 (2,795 up in space flight, 1,152 down).
>
> **Top 10 up-regulated (by log2FC)**
>
> | ENSEMBL | SYMBOL | log2FC | adj p | Wald stat | Mean SF | SD SF | Mean GC | SD GC |
> |---|---|---|---|---|---|---|---|---|
> | ENSMUSG00000099908 | — | 21.02 | 1.0e-05 | 5.68 | 20.8 | 46.6 | 1.0 | 0.0 |
> | ENSMUSG00000112022 | Gm2436 | 6.26 | 3.6e-02 | 2.83 | 23.7 | 29.5 | 1.2 | 0.5 |
> | … 8 more rows … |
>
> **Top 10 down-regulated (by log2FC)**
>
> | ENSEMBL | SYMBOL | log2FC | adj p | Wald stat | Mean SF | SD SF | Mean GC | SD GC |
> |---|---|---|---|---|---|---|---|---|
> | ENSMUSG00000095923 | — | −4.51 | 1.0e-02 | −3.43 | 1.5 | 0.6 | 11.6 | 18.4 |
> | ENSMUSG00000095338 | Igkv3-9 | −3.79 | 4.9e-02 | −2.66 | 1.6 | 1.0 | 7.5 | 14.8 |
> | … 8 more rows … |
>
> Group means/SDs are normalised counts. Queries run:
> `…/v2/dataset/OSD-515/files/` and
> `…/v2/query/data/?id=OSD-515&file.filename=GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv&column.ENSEMBL&column.SYMBOL&column.Log2fc_(Space%20Flight)v(Ground%20Control)&column.Adj.p.value_(Space%20Flight)v(Ground%20Control)%3C=0.05&column.Stat_(Space%20Flight)v(Ground%20Control)&column.Group.Mean_(Space%20Flight)&column.Group.Stdev_(Space%20Flight)&column.Group.Mean_(Ground%20Control)&column.Group.Stdev_(Ground%20Control)&format=json.records`
>
> **Would you like a downloadable CSV of all 3,947 significant genes?**

(Full tables: [`README.md` E4](README.md#e4--genelab-processed-differential-expression-unambiguous).)

---

## Transcript 3 — E5, ambiguous comparison

**You:** Get the differentially expressed genes for flight vs ground in OSD-48 with adj p < 0.05 and |log2FC| > 1.

**Claude:**

> Using osdr-biodata-api
>
> I checked the contrasts file for OSD-48
> (`GLDS-48_rna_seq_contrasts_GLbulkRNAseq.csv`). The sample groups combine
> two factors — spaceflight condition and euthanasia location — so there are
> **two** flight-vs-ground comparisons:
>
> 1. `(Space Flight & Carcass)v(Ground Control & Carcass)`
> 2. `(Space Flight & Upon euthanasia)v(Ground Control & Upon euthanasia)`
>
> Which would you like? (The remaining ten contrasts compare carcass vs
> upon-euthanasia within or across conditions.)

**You:** The carcass one.

**Claude:** *(follows the E4 contract: 635 genes at adj p ≤ 0.05, of which
the |log2FC| > 1 subset is tabulated; top-10 up/down; CSV offer.)*

---

## Transcript 4 — E9, GeneLab-processed detection

**You:** Which Inspiration4 datasets contain GeneLab-processed data files?

**Claude:**

> Using osdr-biodata-api
>
> Four Inspiration4 datasets have GeneLab-processed data (excluding
> FastQC/MultiQC reports):
>
> | Accession | Processed-file category | Assay |
> |---|---|---|
> | OSD-572 | GeneLab Processed Metagenomics Files | Whole-genome shotgun sequencing |
> | OSD-573 | GeneLab Processed Metagenomics Files | Whole-genome shotgun sequencing |
> | OSD-574 | GeneLab Processed Metagenomics Files | Whole-genome shotgun sequencing |
> | OSD-630 | GeneLab Processed Metagenomics Files | Whole-genome shotgun sequencing |
>
> The other Inspiration4 datasets (OSD-569–571, 575, 656, 687 …) carry only
> QC reports under the GeneLab Processed category and have no processed
> data tables yet.
>
> Query run:
> `…/v2/query/datasets/?investigation.study.comment.Project%20Identifier=/Inspiration/&file.category=/genelab%20processed/&file.filename=/^(?!.*(fastqc|multiqc|md5sum)).*/&file.category&investigation.study%20assays.study%20assay%20technology%20type&format=json.records`

---

## Transcript 5 — E9 variant, "data files" without "processed" (Haiku)

**You:** list all inspiration 4 datasets that contain data files

**Claude:**

> Using osdr-biodata-api
>
> There are **10 Inspiration4 datasets** with data files:
>
> | Dataset | File categories |
> |---|---|
> | OSD-569 | Complete Blood Count; targeted sequencing; long read RNA-Seq; m6A Direct RNAseq; GeneLab Processed RNA-Seq / long read RNA-Seq / Whole Genome Sequencing |
> | OSD-570 | scRNA-Seq; snRNA-Seq; snATAC-Seq; GeneLab Processed scRNAseq / snRNAseq / snATACseq |
> | OSD-571 | Proteomics; Metabolomics; GeneLab Processed RNA-Seq / Whole Genome Sequencing |
> | OSD-572 | Metagenomics; Metatranscriptomics; GeneLab Processed Metagenomics |
> | OSD-573 | Metagenomics; Metatranscriptomics; GeneLab Processed Metagenomics |
> | OSD-574 | Metagenomics; Metatranscriptomics; Spatial Transcriptomics; GeneLab Processed Metagenomics / Spatial Transcriptomics |
> | OSD-575 | Comprehensive Metabolic Panel; Immunoassay |
> | OSD-630 | Metagenomics; GeneLab Processed Metagenomics |
> | OSD-656 | Immunoassay |
> | OSD-687 | ChIC-seq; GeneLab Processed Chromatin Immunocleavage Sequencing |
>
> Query run:
> `…/v2/query/datasets/?investigation.study.comment.Project%20Identifier=/Inspiration/&file.category&format=json.records`

One call, no FastQC/MultiQC exclusion — that filter is applied only when the
question says *GeneLab-processed*.

---

## Transcript 6 — E10, microbial DE with one matching contrast (Sonnet)

**You:** List the differentially expressed genes for OSD-145 flight vs ground control comparison, filtered to adj p < 0.05 and |log2FC| > 1

**Claude:**

> Using osdr-biodata-api
>
> **File:** `GLDS-145_rna_seq_differential_expression_GLbulkRNAseq.csv`
> (bulk RNA-seq differential expression; OSD-145 is *Staphylococcus aureus*).
> **Contrast:** the contrasts file has one flight-vs-ground comparison,
> `(Space Flight & Frozen)v(Ground Control & Frozen)`, so I used it.
>
> **1,513** genes at adj p ≤ 0.05; **239** with |log2FC| > 1 (168 up, 71 down).
> No gene symbols are annotated in this microbial table (the request with
> `SYMBOL` returned 500, so I reran it without) — genes are keyed by
> `gene_id`. I can list the file's other columns if useful.
>
> **Top 10 up-regulated**
>
> | gene_id | Log2FC | Adj p | Stat | Mean SF | SD SF | Mean GC | SD GC |
> |---|---|---|---|---|---|---|---|
> | QV15_10390 | 6.921 | 9.51e-199 | 30.29 | 9207.8 | 2537.9 | 76.9 | 39.2 |
> | QV15_00805 | 4.424 | 4.23e-76 | 18.77 | 1228.8 | 667.5 | 58.2 | 14.3 |
> | … 8 more rows … |
>
> **Top 10 down-regulated**
>
> | gene_id | Log2FC | Adj p | Stat | Mean SF | SD SF | Mean GC | SD GC |
> |---|---|---|---|---|---|---|---|
> | QV15_01890 | −3.431 | 1.15e-164 | −27.57 | 1096.5 | 286.6 | 11818.8 | 1424.4 |
> | QV15_01885 | −3.108 | 1.10e-97 | −21.26 | 653.5 | 201.3 | 5627.0 | 519.4 |
> | … 8 more rows … |
>
> Queries run: `…/v2/query/assays/?id.accession=OSD-145&file.filename=/differential_expression|Counts|contrasts|abundance|methylation/&file.subcategory&format=json.records`,
> `…/v2/query/data/?id=OSD-145&file.filename=GLDS-145_rna_seq_contrasts_GLbulkRNAseq.csv&format=json.records`,
> and the data call in [`README.md` E10](README.md#e10--microbial-differential-expression-single-matching-contrast).
>
> **Would you like a downloadable CSV of all significant genes?**

---

## Transcript 7 — E12, out-of-scope redirect

**You:** Show me the temperature and CO2 readings on ISS during RR-1.

**Claude:**

> Using osdr-biodata-api
>
> Environmental telemetry (temperature, humidity, CO₂, radiation environment)
> is outside the OSDR biological data API this skill covers. Use the OSDR
> **Environmental Data Application (EDA)**:
> https://visualization.osdr.nasa.gov/eda/ — select the RR-1 mission /
> SpaceX-4 dates there.
>
> If you also want the biological datasets from RR-1 (25 datasets), I can
> list those.

No biodata URL is built.

---

## What a failure looks like

If Claude returns **0 rows** for a mission or organism query, check the
URL it printed: a `\|` inside the regex means it copied a markdown-escaped
pipe (fixed in 1.0.0 by moving all OR patterns into code blocks; report it
if you still see it). If Claude answers a DE question with a 422, it passed
a regex that matched several files instead of pinning one exact file name.
