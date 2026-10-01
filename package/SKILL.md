---
name: osdr-biodata-api
description: Build and run NASA OSDR (Open Science Data Repository / GeneLab) Biological Data API queries. Use when a user asks to find, list, filter, count, or download OSDR/GeneLab datasets, assays, samples, or processed data files (RNA-seq, microarray, methylation, 16S/amplicon, proteomics, behaviour, imaging, etc.) by organism, tissue, mission (RR-1, Inspiration4, Bion-M1…), spaceflight/radiation/ground-analog factor, sex, strain, age, technology, or accession (OSD-###, GLDS-###); to pull differential expression / abundance / count tables or download URLs; or to assemble cross-study cohorts. Every call is a public HTTPS GET URL with no API key. Does NOT cover environmental telemetry, radiation dosimetry, biospecimens, or NASA astronaut records — for those it only points to EDA, RadLab, NBISC, SMCC and NLSP.
license: Public domain (NASA data); skill text CC0
compatibility: Needs outbound HTTPS to visualization.osdr.nasa.gov (and osdr.nasa.gov for downloads). Optional helper script needs Python 3.8+ (standard library only).
metadata:
  version: "1.0.0"
  author: OSDR_Skill_Sheets project
  api-version: "v2 (OpenAPI 2.0.0)"
---

# OSDR Biological Data API

Build one plain HTTPS GET URL per question, run it, and report the result.
No key, no login. Check scope first (§0); if a result is empty, apply §5
before saying "no data"; if a call returns 504, retry it (§2 step 6).

## Contents

0. Scope gate — answer these WITHOUT building a query
1. Quick reference (the 80% case)
2. Step-by-step procedure
3. URL grammar rules
4. Choosing the endpoint and keeping queries cheap
5. Empty-result fallbacks
6. Pulling the rows of a data file
7. Subjects, cohorts and cross-study questions
8. Reporting results
9. Reference files and script

---

## 0. Scope gate — check before anything else

This skill covers OSDR **biological** data only. If the request is one of
the following, answer with the fixed text below, do not build or run any
biodata URL, and do not probe or reverse-engineer any other API (EDA, RadLab…).
If a separate skill for that resource is installed, hand off to it.

| Request is about | Reply (first sentence, verbatim) then the link(s) |
|---|---|
| **NASA astronaut / crew data** (astronaut health, flight crew samples, "human spaceflight data") | "OSDR does not host NASA human astronaut data." → NASA Life Sciences Portal (NLSP) https://www.nasa.gov/hrp/nlsp/ · Life Sciences Data Archive (LSDA) https://nlsp.nasa.gov/explore/mtable/lsda_experiment/lsda_experiment · Lifetime Surveillance of Astronaut Health (LSAH) https://nlsp.nasa.gov/explore/lsdahome/lsahhome. **Only after that**, offer (and, if the user wants them, query) what OSDR does hold that involves humans, each labelled: non-NASA crew studies (Inspiration4, `Project%20Identifier=/Inspiration/`), human ground analogs (bed rest, confinement, limb suspension), and in-vitro human cell/organoid studies (`organism=/sapiens/`, then classify by project type + material type). |
| **Environmental telemetry** (temperature, humidity, CO₂, cabin environment, radiation *environment*) | "Environmental telemetry is outside this skill; it is served by the OSDR Environmental Data Application (EDA)." → https://visualization.osdr.nasa.gov/eda/ |
| **Radiation dosimetry** (dose measurements, dosimeters) | "Radiation dosimetry is outside this skill; it is served by RadLab." → https://visualization.osdr.nasa.gov/radlab/gui/overview/ |
| **Physical biospecimens** (request tissue/samples) | "Biospecimen requests are outside this skill; use NBISC." → https://visualization.osdr.nasa.gov/nbisc/home/ (background https://science.nasa.gov/biological-physical/data/nbisc/) |
| **Microbe specimens / isolates** | "Microbial isolate requests are outside this skill; use SMCC." → https://visualization.osdr.nasa.gov/smcc/ |
| Full-text search, GEO/PRIDE/SRA, compute | see `references/scope.md` |

After the redirect you may offer an in-scope follow-up ("I can list the RR-9 biological datasets in OSDR"). Radiation as an *experimental factor* of a biology study (`study.factor%20value.absorbed%20radiation%20dose`, `Project%20Identifier=/Irradiation/`) IS in scope.

---

## 1. Quick reference

```
BASE = https://visualization.osdr.nasa.gov/biodata/api

Find assays:    BASE/v2/query/assays/?<filters>&format=json.records
Find samples:   BASE/v2/query/samples/?<filters>&format=json.records
Find datasets:  BASE/v2/query/datasets/?<filters>&format=json.records
File contents:  BASE/v2/query/data/?id=OSD-###&file.filename=<one file>&column.*&format=csv
Known dataset:  BASE/v2/dataset/OSD-###/   (also /files/ and /assays/; fast, never times out)
```

Filters most questions need. Values go inside `/.../` (regex, case-insensitive).
OR is a plain pipe `|` (see the block after the table — a markdown table cannot
show it, and `\|` in a URL matches nothing).

| Ask about | Filter |
|---|---|
| organism | `study.characteristics.organism=/musculus/` (`/rattus/`, `/sapiens/`, `/arabidopsis/`, `/drosophila/`) |
| host of a microbiome / 16S / ITS study | `study.characteristics.host%20organism=/lactuca/` — in amplicon studies `organism` is literally "Microbiota"; plant list in the OR block below; unsure → list values with `host%20organism=/./` first |
| tissue | `study.characteristics.material%20type=/liver/` — OR in synonyms and sub-parts (eye block below) |
| technology | `investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/` = bulk RNA-seq only; `/microarray/`, `/bisulfite/`, `/16S/`, `/mass%20spectrometry/`, `/single-cell/`; all RNA sequencing types: OR block below |
| behavioural data | `investigation.study%20assays.study%20assay%20measurement%20type=/behavior/` |
| one mission | `investigation.study.comment.Project%20Identifier=/RR-1([^\d]|$)/` — keep the anchor: `/RR-1/` also matches RR-10…RR-18 |
| any Rodent Research mission | see OR block below (anchored) — unanchored `/RR/` matches "I**rr**adiation"; labels can be comma-joined (`RR-1, RR-3`), report them as stored. **RRRM-1 = RR-8** (stored as `RRRM-1 (RR-8)`) and **RRRM-2 = RR-17** (RRRM = Rodent Research Reference Mission). When grouping or counting by mission, merge each pair into one row labelled `RR-8 / RRRM-1` or `RR-17 / RRRM-2` |
| other missions / ground analogs | `…Project%20Identifier=/Inspiration/`, `/Bion/`, `/MHU/`, `/Hindlimb_Unloading/`, `/Irradiation/` — for mission questions filter on Project Identifier, never on organism |
| flight vs ground study | `investigation.study.comment.project%20type=/spaceflight/` or `=/ground/` |
| spaceflight factor | `study.factor%20value.spaceflight=/space%20flight/` |
| sex / strain / genotype | `study.characteristics.sex=/female/` · `…strain=/C57BL/` (substrains vary) · `…genotype=/…/`; if 0 rows use `study.factor%20value.<same>` |
| age (name varies) | `study.characteristics.age=/./`; else `…age%20at%20launch`, `…age%20at%20experiment%20start`, or discover (§5.4) |
| one / several datasets | `id.accession=OSD-104` · `id.accession=/^OSD-10[24]$/` |
| has data files (any kind) | add bare `&file.category` — lists every dataset that has files, raw or processed, with the categories. "Data files" / "files" means this; apply the GeneLab-processed filter below **only when the user says GeneLab-processed / processed** |
| has a processed file | `file.filename=/differential_expression/` · `/Normalized_Counts/` · `/differential_methylation/` · `/differential_abundance/` |
| has **GeneLab-processed** data (any omics type) | use the "GeneLab-processed data (real)" line in the OR block below: `file.category=/genelab%20processed/` **plus** a filename filter that drops the QC-only files (FastQC/MultiQC reports, md5 lists) which also sit under the "GeneLab Processed" category. Report each dataset's `file.category` values as its processed data types (RNA-Seq, WGBS, Metagenomics …). Never use `file.category` alone: it labels datasets that only have QC reports (Inspiration4: 8 labelled, 4 real) |
| study DOI (citation) | add bare `&investigation.study.comment.doi` |

OR patterns (copy exactly; the pipe is a plain `|`):

```
any Rodent Research mission:   investigation.study.comment.Project%20Identifier=/^RR-?\d|^RRRM/
one mission, both spellings:   investigation.study.comment.Project%20Identifier=/RR-1([^\d]|$)|RR1([^\d]|$)/
rodents:                       study.characteristics.organism=/musculus|rattus/
plant hosts (amplicon):        study.characteristics.host%20organism=/lactuca|brassica|capsicum|solanum|raphanus|pisum|triticum/
eye tissue:                    study.characteristics.material%20type=/eye|retina|optic|cornea|lens/
leg muscles:                   study.characteristics.material%20type=/soleus|gastrocnemius|tibialis|quadriceps/
all RNA sequencing types:      investigation.study%20assays.study%20assay%20technology%20type=/rna%20sequencing|rna-seq/
methylation assays:            investigation.study%20assays.study%20assay%20technology%20type=/bisulfite|methylation/
amplicon assays:               investigation.study%20assays.study%20assay%20technology%20type=/16S|ITS/
DE or microarray:              investigation.study%20assays.study%20assay%20technology%20type=/rna-seq|microarray/
GeneLab-processed data (real): file.category=/genelab%20processed/&file.filename=/^(?!.*(fastqc|multiqc|md5sum)).*/&file.category
```

Copy-paste examples (verified live; row counts change as OSDR grows):

```
# mouse RNA-seq assays (~113 rows, ~111 datasets)
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/&study.characteristics.organism=/musculus/&format=json.records

# every RR-1 assay with technology + tissue (~80 rows, 25 datasets)
BASE/v2/query/assays/?investigation.study.comment.Project%20Identifier=/RR-1([^\d]|$)|RR1([^\d]|$)/&investigation.study%20assays.study%20assay%20technology%20type&study.characteristics.material%20type&format=json.records

# female mouse liver samples (~820 rows)
BASE/v2/query/samples/?study.characteristics.organism=/musculus/&study.characteristics.material%20type=/liver/&study.characteristics.sex=/female/&format=json.records

# DE genes for OSD-515, adj p ≤ 0.05, Space Flight vs Ground Control, default columns (see §6; always read the contrasts file first)
BASE/v2/query/data/?id=OSD-515&file.filename=GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv&column.SYMBOL&column.Log2fc_(Space%20Flight)v(Ground%20Control)&column.Adj.p.value_(Space%20Flight)v(Ground%20Control)%3C=0.05&column.Stat_(Space%20Flight)v(Ground%20Control)&column.Group.Mean_(Space%20Flight)&column.Group.Stdev_(Space%20Flight)&column.Group.Mean_(Ground%20Control)&column.Group.Stdev_(Ground%20Control)&format=csv
```

---

## 2. Step-by-step procedure

1. **Scope gate (§0).** Out of scope → fixed reply, stop.
2. **Classify** with §4 → pick ONE endpoint. For an assay type or study
   family you have not queried before, first discover its real field names
   with one cheap bare-prefix call (§5.4) instead of guessing.
3. **Map each constraint** to a filter from §1 or `references/fields.md`;
   one `field=/regex/` per constraint.
4. **Add output columns** as bare field names (e.g. `&study.characteristics.material%20type`).
   Filtered fields come back automatically. If the call times out twice,
   drop the bare columns and enrich per accession instead (§4 cost ladder).
5. **Append `&format=json.records`** (or `csv`); assemble
   `BASE + endpoint + ? + filters joined by &`; run the checklist in §3.
6. **Execute** with the HTTP tool, `curl -sg -m 200 "<url>"`, or
   `python3 scripts/osdr_query.py` (retries built in). Rules:
   - always `-g` (`--globoff`) with curl — `[ ]`/`( )` otherwise break curl silently; quote the URL;
   - **HTTP 504 = server timeout, not a bad URL.** Retry the *identical* URL
     up to 3 times, 10–15 s apart, before changing anything (the second try
     usually succeeds); check the body starts with `[` or `{` before parsing;
   - host blocked / not in allowlist → do not rewrite the URL; see
     `references/network-setup.md` and hand the URL to the user.
7. **If 0 rows**, apply §5 before reporting "no data".
8. **Report** per §8.

---

## 3. URL grammar rules

- **Spaces are `%20`** in field names AND values. Never `+`.
- **Wrap values in slashes** for regex / substring / case-insensitive match:
  `=/musculus/`. Use regex unless you know the complete exact value
  (`=Mus` matches nothing; `=/mus/` matches `Mus musculus`).
- **OR inside one value = a plain pipe** `=/rna-seq|microarray/` (never `\|` — that is markdown table escaping and matches nothing); **AND across fields = `&`**.
- **Bare field (no `=`) = add that column without filtering.** A prefix
  returns every sub-field: `&study.characteristics`, `&study.factor%20value`,
  `&investigation.study.comment`.
- **Matching is case-insensitive substring — anchor short tokens.** `/RR/`
  hits "Irradiation", `/RR-1/` hits RR-10…RR-18, `/male/` hits Female. Use
  `^` and `$` or `([^\d]|$)`; both work server-side. Escape a literal dot `\.`;
  leave `( ) [ ] | ^ $` unencoded.
- **A literal `&` inside a value or column name is `%26`**
  (`(Space%20Flight%20%26%20Carcass)`).
- **Comparison operators (data endpoint):** `%3C` `<`, `%3E` `>`, `%3C=` `<=`,
  `%3E=` `>=`, `!=`. One column, one direction per operator.
- **Field names are case-insensitive; results come back lower-cased**
  (`id.assay name`, `investigation.study.comment.project identifier`).
- **`format=`**: `json.records` (list of row objects — best), `csv` (default),
  `tsv`, `json.table`, `json.split`; `browser` is an HTML viewer, never fetch it.
- Unknown field: bare → `null` column; filter → 0 rows (no error).

**Pre-flight checklist:** `[ ] in scope  [ ] starts with BASE  [ ] endpoint ends with /
[ ] every space %20  [ ] every value in /…/ unless exact  [ ] short tokens anchored
[ ] format=json.records or csv  [ ] /data/ uses id= and exactly one file  [ ] curl -g -m 200`

---

## 4. Choosing the endpoint and keeping queries cheap

Rows are the **distinct combinations** of the endpoint's id columns plus every
column you request; requesting a finer field expands the rows (a bare assay-level
column on `/datasets/` repeats an accession once per value — count distinct
`id.accession`, never raw rows, when the question is "how many datasets").

| User wants | Endpoint | id columns |
|---|---|---|
| Which datasets match … / how many | `/v2/query/datasets/` | `id.accession` |
| Which assays / technologies (default for "find/list") | `/v2/query/assays/` | + `id.assay name` |
| Per-sample rows (sample names, sex, strain, factor values, replicate counts, subjects) | `/v2/query/samples/` (`/metadata/` is identical) | + `id.sample name` |
| The numbers inside a processed file | `/v2/query/data/` | file columns (§6) |
| Everything about ONE accession / its file list | `/v2/dataset/OSD-###/`, `…/files/`, `…/assays/` | JSON tree |

**Cost ladder — narrow, then expand.** Broad queries can 504 at ~60 s;
per-accession calls answer in 0.5–3 s and never timed out in testing.

- Cheap: anything with `id.accession`; the `/v2/dataset/OSD-###/` tree (safe to
  call in parallel for 100+ accessions); one filter on technology, organism,
  project type or project identifier.
- Expensive: several filters plus several bare columns; **repository-wide
  `file.filename` or `file.category` scans with no accession or technology
  filter — these may never complete.**
- Pattern: (a) one cheap filter → accession list; (b) enrich per accession —
  `/v2/dataset/OSD-###/` for title, organism, material type, project
  identifier/type, mission name, technology; `/v2/query/assays/?id.accession=OSD-###&file.filename=/…/`
  for files; (c) AND two facets by intersecting accession lists client-side
  (a single assay row is never both RNA-seq and methylation).
  Enrichment snippet and worked cases: `references/cohorts.md`.

`/v2/query/metadata/` and `/v2/query/data/` are live but absent from
`openapi.json`; `/v2/metadata/fields/` is in the spec but returns 404.

---

## 5. Empty-result fallbacks (mandatory before saying "no data")

1. **Regex, not exact**: `=Value` → `=/value/`; loosen (`/mus musculus/` → `/musculus/`).
2. **Characteristic ↔ factor.** Sex, strain, age, genotype, tissue, treatment,
   dose can be either. `study.characteristics.X` empty → rerun with
   `study.factor%20value.X` (and vice versa). Only after both are empty may
   you report no data.
3. **Wrong field family.** Microbiome host → `host%20organism` (not
   `organism`); tissue may be `material%20type`, `organism%20part`, or
   `factor%20value.tissue`; missions may be under `mission%20name`
   (`/SpaceX-4/`) when `project identifier` is null.
4. **Discover the real field names** for one study with bare prefixes:
   `BASE/v2/query/assays/?id.accession=OSD-104&study.characteristics&study.factor%20value&format=json.records`
   Then **discover values** across OSDR with `/./`:
   `…?study.characteristics.strain=/./&format=json.records`. Vocabularies
   with counts: `references/fields.md`.
5. **File-name fallback.** `/…_GLbulkRNAseq\.csv/` empty → older studies lack
   the `_GL…` token; retry `/differential_expression/`.
6. **Two facets** → two cheap queries intersected on `id.accession` (§4). Note
   "has a methylation *assay*" (≈16 datasets with a DE file) is not "has a
   differential-methylation *file*" (4: OSD-47, 48, 103, 105); say which you mean.

---

## 6. Pulling the rows of a data file (`/v2/query/data/`)

Must resolve to **exactly one file** or it returns 422. Always three steps.

**A — list files** (cheap):
`BASE/v2/query/assays/?id.accession=OSD-48&file.filename=/differential_expression|Counts|contrasts|abundance|methylation/&file.subcategory&format=json.records`
Pick one exact `file.filename` (prefer the plain over the `_rRNArm_` variant unless asked).
The file type follows the request, not the organism: "differential expression"
→ `differential_expression` (microbial RNA-seq studies such as OSD-145 have one);
"differential abundance" → `differential_abundance` (amplicon / metagenomics).

**B — read the contrasts file (mandatory, tiny):**
`BASE/v2/query/data/?id=OSD-48&file.filename=/contrasts_GLbulkRNAseq/&format=json.records`
(use the exact contrasts file name from step A; a bare `/contrasts_GL/` returns
422 when a study also has a methylation contrasts file).
Its column names are the exact `(group1)v(group2)` strings. **A group is one
unique combination of the study's factor values** (however many factors there
are), joined with ` & ` inside parentheses; every pair of groups is a contrast,
in both directions, and the same group names are used in the differential
methylation and abundance files. To build a study's groups yourself:
`BASE/v2/query/samples/?id.accession=OSD-48&id.assay%20name=/rna-seq/&study.factor%20value&format=json.records`
→ the distinct combinations of the `study.factor value.*` columns, with their n
(OSD-48: Space Flight/Ground Control × Carcass/Upon euthanasia = 4 groups →
12 contrasts). The contrasts file fixes the exact spelling and factor order.
So **multi-factor studies have no plain `(Space Flight)v(Ground Control)`
column** — OSD-48 only has `(Space Flight & Carcass)v(Ground Control & Carcass)`
and `(Space Flight & Upon euthanasia)v(Ground Control & Upon euthanasia)`.
**If the user's comparison matches more than one contrast (or none), list the
available contrasts and ask the user which one(s) they want — do not pick one
and do not run all of them.** When a contrasts file exists, offer only strings
that are literally column names in it — do not compose group names from
factor levels (OSD-145 has no `Space Flight & Not frozen` group). Only when
the study has **no** contrasts file build the groups from the factor levels
(samples query above) and confirm them against the data file's header
(`…&column.*&format=csv`, first line). Encode `&` as `%26`.

**C — pull rows.** For differential-expression results always request these
columns for the chosen contrast `C` = `(g1)v(g2)`: the identifier column
(`ENSEMBL` animals, `TAIR` plants, `gene_id` microbes — always returned first
whether or not you request it; **always show it as the first column of every
table**), `SYMBOL`, `Log2fc_C`, `Adj.p.value_C` (filtered
`%3C=0.05`), `Stat_C` (Wald statistic), and the mean and standard deviation of
each compared group, `Group.Mean_(g1)`, `Group.Stdev_(g1)`, `Group.Mean_(g2)`,
`Group.Stdev_(g2)` (same for differential methylation and abundance tables):
`BASE/v2/query/data/?id=OSD-48&file.filename=<exact name>&column.SYMBOL&column.Log2fc_(Space%20Flight%20%26%20Carcass)v(Ground%20Control%20%26%20Carcass)&column.Adj.p.value_(Space%20Flight%20%26%20Carcass)v(Ground%20Control%20%26%20Carcass)%3C=0.05&column.Stat_(Space%20Flight%20%26%20Carcass)v(Ground%20Control%20%26%20Carcass)&column.Group.Mean_(Space%20Flight%20%26%20Carcass)&column.Group.Stdev_(Space%20Flight%20%26%20Carcass)&column.Group.Mean_(Ground%20Control%20%26%20Carcass)&column.Group.Stdev_(Ground%20Control%20%26%20Carcass)&format=json.records`
(→ 635 rows). Then report: the number of significant genes (adj p ≤ 0.05),
the **top 10 up-regulated and top 10 down-regulated genes by `Log2fc`** as two
tables with those columns, and **end the answer with the question:
"Would you like a downloadable CSV of all significant genes?"** (write the
file only if they say yes). Always request `SYMBOL` (animal and plant tables
have it); if the call returns **500**, the table has no `SYMBOL` (some microbe
studies, e.g. OSD-95, OSD-145) — rerun the same URL without `column.SYMBOL`,
say that no gene symbols are annotated, and offer to list the file's remaining
columns (header: `…&column.*&column.Adj.p.value_C%3C=0.05&format=csv`, first line).

- `column.*` all columns; `column.<Name>` select; `column.<Name>%3C=0.05` filter (also selects).
- **Operators are one column, one direction.** For |log2FC| > 1 filter adj p
  server-side and apply the fold-change threshold client-side (or run
  `%3E=1` and `%3C=-1` separately).
- Returned columns are prefixed `OSD-48/<assay name>/`; strip when presenting.
  Unannotated genes have SYMBOL `null` or the string `"NaN"` — handle both.
  Strict `%3C0.05` and `%3C=0.05` both work.
- Unfiltered tables are 10–60 MB: always select columns or filter rows.
- Errors: `422 multiple files` → pin one name; `422 only available in
  format=raw` → the API has not tabulated that file; `&format=raw` redirects to
  its download URL; `500` a `column.` name does not exist (contrast not in the file, or `SYMBOL` in a microbe table) → fix or drop the name, the dataset is fine;
  `400 Invalid characters` → unencoded `&`.

File names, columns, per-omics conventions, `file.category` recipe:
`references/processed-files.md`.

---

## 7. Subjects, cohorts and cross-study questions

- **Subject ID = Project Identifier + " | " + Source Name.** Pull
  `/v2/query/samples/?…&investigation.study.comment.Project%20Identifier&study.source%20name&study.characteristics.material%20type`
  and group client-side; e.g. `RR-1 | RR1_FLT_M23` is the same animal in the
  OSD-102 kidney and OSD-104 soleus datasets. There is no subject field.
- Exclude QC/pool rows before counting (sample names or values like
  `Empty Pool`, `Pool of all FLT samples`, organism/sex `Not Applicable`);
  lower-case values before grouping (`Female`/`female`, `Male`/`male`).
- "Datasets where *all* samples are female" is a dataset-level property:
  samples endpoint + group-by; `sex=/female/` alone means *any* female sample.
- Recipes (per-subject table, female-only datasets, meta-analysis corpus,
  "has file X AND file Y", enrichment snippet): `references/cohorts.md`.

---

## 8. Reporting results

- Row count from the **complete** response (`wc -l`, `len(json)`), never after
  `head`; what a row is (dataset / assay / sample); distinct `OSD-###`
  (`GLDS-###`/`LSDS-###` in file names are ids inside the same study).
- Show the exact URL(s) you ran.
- Download URLs: `file.remote_url` from `/v2/query/…` is **relative** —
  prefix `https://osdr.nasa.gov`; the `URL` field in `/v2/dataset/OSD-###/files/`
  is already absolute (that JSON has only `URL` and `REST_URL`, no category).
- Sanity-check organism against the study title before asserting it (a few
  datasets are mis-tagged, e.g. rat studies under *Homo sapiens*).
- Citation: `BASE/v2/query/datasets/?id.accession=OSD-###&investigation.study.comment.doi&format=json.records`
  (DOI present for ~94% of studies; else the landing page
  https://osdr.nasa.gov/bio/repo/data/studies/OSD-###). Version is not in the
  API (highest `version-N` folder in `s3://nasa-osdr/OSD-###/`). End every
  data/metadata answer with: "Source: OSDR OSD-### (DOI <doi>); dataset
  version = highest version-N folder in s3://nasa-osdr/OSD-###/ — please cite
  the DOI and state the version." For lists of many datasets write instead:
  "Source: OSDR; cite each dataset by its DOI (add `&investigation.study.comment.doi`
  to the query) and state its version (highest version-N folder in s3://nasa-osdr/OSD-###/)."

---

## 9. Reference files and script

Read only what the task needs (paths relative to this folder):

- `references/fields.md` — field paths, alias order (age/tissue/strain/mission
  variants), live vocabularies with counts (organism, host organism,
  technology, measurement, project identifier/type, spaceflight, sex,
  file category/subcategory/data type, factor and characteristic names).
- `references/processed-files.md` — GeneLab file names per omics type, columns,
  contrast naming, `file.category` recipe, size limits.
- `references/cohorts.md` — subject IDs, female-only datasets, two-file
  intersections, per-accession enrichment code, retry snippet.
- `references/examples.md` — 61 verified question → URL pairs (templates).
- `references/network-setup.md` — hosts to allow-list; per-client notes.
- `references/scope.md` — identifier model (OSD/GLDS/LSDS), DOI/version,
  out-of-scope reply templates, current API limitations.
- `scripts/osdr_query.py` — builds, runs (with 504 retries) and summarises a
  query: `python3 scripts/osdr_query.py assays organism=musculus tech=rna-seq`;
  `… files OSD-515`; `… contrasts OSD-48`; `… dataset OSD-104` (enrichment);
  `--help` for all options.
