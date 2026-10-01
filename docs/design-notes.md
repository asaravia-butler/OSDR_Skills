# Design notes — `osdr-biodata-api`

Why the package is shaped the way it is, and the API behaviours it encodes.
Read this before changing the skill.

## 1. Structure

**One folder, one format, four clients.** Claude, ChatGPT/Codex, Gemini and
VS Code / Copilot all load the [Agent Skills](https://agentskills.io/specification)
layout: a `SKILL.md` with YAML frontmatter (`name`, `description`, optional
`metadata`) plus `references/` and `scripts/`. The folder name must equal
`name`, the description must be ≤ 1024 characters, and `SKILL.md` should stay
under 500 lines. Nothing in the package is client-specific.

**Progressive disclosure.** Only the frontmatter is always in context; the
client loads the body of `SKILL.md` when the description matches, and the
reference files only when `SKILL.md` points to them. So `SKILL.md` holds the
decision procedure and the ten most-used filters, while vocabularies (fields
and values with counts), GeneLab file naming, Python snippets and the 65
worked examples live in `references/`.

**The description is the trigger.** It lists the nouns users actually type
(OSDR, GeneLab, OSD-###, GLDS, spaceflight, Rodent Research, RNA-seq, mission
names, tissues, differential expression…) and the out-of-scope nouns too
(astronaut, environmental, radiation), because the scope gate only works if
the skill loads for those questions.

**Written for small models.** Every rule that a small model got wrong in
testing is stated once, imperatively, close to where it is used:

- OR-regexes live in a fenced code block, not in a markdown table — Haiku
  copied the table-cell escape `\|` into URLs and got zero rows.
- `curl -g` is mandatory (`[`, `(` in URLs otherwise fail silently).
- "List the contrasts and ask" is spelled out as a rule with the OSD-48
  example, because the default behaviour was to run every contrast.
- HTTP 500 on a missing column is explained (small models read it as "the
  dataset does not exist").
- Output contracts (DE tables, subject tables, dataset reports) are given as
  column lists rather than prose.

An earlier iteration that added *adaptive* logic (relax the adjusted-p cutoff
when few genes pass, probe headers to decide columns, extra script
subcommands) made small models worse — more branches, more places to go
wrong. It was withdrawn; the current package prefers fixed defaults plus
"ask the user".

**The script is optional.** `scripts/osdr_query.py` is standard-library
Python that builds the same URLs the text describes, adds retries and
summarises results. Clients that cannot run code (Gemini Spark) ignore it
and use the URLs directly; nothing depends on it.

## 2. API behaviours encoded in the skill

All verified against the live API in September 2026.

**Endpoints.** `/v2/query/{datasets,assays,samples,metadata,data}/` and the
per-dataset REST tree `/v2/dataset/OSD-###/{,files/,assays/}`. The
`/v2/metadata/fields/` endpoint listed in the OpenAPI spec returns 404.

**Row granularity.** A bare field selector (e.g. `&organism`) adds a column
*and* changes what a row is: rows are distinct combinations of the id
columns plus every requested field. Ask for `datasets` when you want
accessions, `assays` for accession × assay, `samples` for individual samples.

**Matching.** `field=value` must equal the whole value; `/…/` is a
case-insensitive regex substring search evaluated server-side, so anchors
(`^`, `$`, `([^\d]|$)`) and negative lookahead
(`/^(?!.*(fastqc|multiqc|md5sum)).*/`) all work. `RR-1` needs
`/^RR-1([^\d]|$)/` to exclude RR-10…RR-19 while keeping `RR-1_BSP`.

**Encoding.** Spaces as `%20`, `&` inside values as `%26`, comparison
operators as `%3C` / `%3E`. Returned keys are lower-cased; data columns are
prefixed `OSD-###/<assay name>/`.

**Fields worth knowing.** Study title is
`investigation.study.study%20title` (not `.title`, which is always null).
DOI is `investigation.study.comment.doi`. `project type` distinguishes
Spaceflight / Ground / Flight studies. Amplicon studies record the host in
`host organism`. `organism part` is populated in ~112 datasets (mostly plants,
some mouse) — it is a tissue alias, not a plant-only field.

**Missions.** Project Identifier is the primary mission field; values are
free text with aliases (`RRRM-1 (RR-8)`, `RR-17` for RRRM-2, `RR-1_BSP`,
comma-joined lists). About 22 datasets have a `mission name` but a null
Project Identifier (e.g. OSD-100, SpaceX-4). Mission questions therefore
query both fields and merge.

**Data files.** `/data/` accepts exactly one file (422 for zero or many),
returns 500 for a nonexistent column and 422 `format=raw` for files that are
not tabulated. GeneLab standardized names carry the pipeline tag
(`_GLbulkRNAseq`, `_GLmicroarray`, `_GLMethylSeq`, `_GLAmpSeq`,
`_GLmetagenomics`) and `_rRNArm_` variants exist for some RNA-seq studies;
pin the non-rRNArm file unless asked otherwise. Contrasts are named
`(group1)v(group2)`, where a group is the unique combination of factor values
joined by ` & ` in the order the contrasts file uses (OSD-48: spaceflight
first; OSD-95: dose first — the metadata order is not reliable).
`Group.Mean_<group>` / `Group.Stdev_<group>` columns are present in all DE,
methylation and abundance tables. The identifier column (`ENSEMBL` for
animals, `TAIR` for Arabidopsis, `gene_id` for microbes) is always returned by
`/data/` even when not requested; `SYMBOL` exists in animal and plant tables and some
microbe tables; where absent, requesting it returns 500 and the call is
rerun without it. Microbial RNA-seq studies (OSD-145,
*S. aureus*) have ordinary `differential_expression` files — the organism
does not decide the file type. When a contrasts file exists, only contrast strings
from it are offered (OSD-145 has no "Not frozen" spaceflight group even
though both factor levels exist); groups are composed from factor levels
only for studies without a contrasts file.

**Processed-data detection.** `file.category=/genelab%20processed/` alone
over-counts, because FastQC/MultiQC reports and checksums sit in that
category. The negative-lookahead filename filter fixes it: Inspiration4 →
4 metagenomics datasets; RR liver → 9 datasets with the right assay type
(OSD-137 is RNA-seq, not WGBS).

**Timeouts.** Broad scans (repository-wide file-name regexes, many filters +
many columns) return 504 after ~60 s. The same URL usually succeeds on retry;
the skill retries once, then narrows.

**File URLs.** `file.remote_url` is relative; prefix `https://osdr.nasa.gov`.

## 3. Scope

The biodata API covers biological datasets only. The skill hard-codes
redirects — first sentence, no query, link — for NASA human astronaut data
(NLSP / LSDA / LSAH), environmental telemetry (EDA), radiation dosimetry
(RadLab), physical biospecimens (NBISC) and microbial isolates (SMCC). This
was needed because assistants otherwise probed `/eda/api` and similar
guesses. Human *cell line* and ex-vivo tissue studies (e.g. OSD-815–817,
human eyes) are in scope.

## 4. Things deliberately left out

- No adaptive statistical thresholds; adj p ≤ 0.05 is fixed and the user is
  asked before changing it.
- No plant/microbe default column sets yet — list and ask.
- No full-text search, counting endpoint or version lookup (not in the API;
  version comes from the S3 bucket listing).
- No client-specific instructions inside the package; those live in this
  repository's `docs/`.
