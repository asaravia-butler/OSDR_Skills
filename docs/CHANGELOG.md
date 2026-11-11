# Changelog — `osdr-biodata-api`

All notable changes to the skills package. Versions follow
[Semantic Versioning](https://semver.org/); the version is recorded in
`metadata.version` in `SKILL.md`.

## 1.0.0 — 2026-11-09

First public release.

**Package**

- `SKILL.md` (414 lines): scope gate with verbatim redirects (astronaut data
  → NLSP/LSDA/LSAH; environmental telemetry → EDA; dosimetry → RadLab;
  biospecimens → NBISC; microbial isolates → SMCC); knowledge-graph-first
  rules for the `mcp-genelab` MCP server (§0b); quick-reference filter table
  with all OR-regex selectors in a code block; step-by-step procedure
  (`curl -g`, 504 retry); URL grammar; endpoint/cost ladder; empty-result
  fallbacks; GeneLab-processed data recipe and output contract; subject/cohort
  rules; reporting and provenance rules.
- `references/`: `fields.md` (canonical paths, alias order, live
  vocabularies with counts), `processed-files.md` (GeneLab file names,
  columns, group and contrast construction, processed-data detection),
  `mcp-genelab.md` (KG tool map, coverage, KG-vs-API split, provenance
  wording), `cohorts.md` (Python snippets), `examples.md` (verified
  question → URL pairs), `network-setup.md`, `scope.md` (identifier model,
  DOI/version, out-of-scope templates, API limitations).
- `scripts/osdr_query.py`: standard-library helper with retries and the
  `assays` / `datasets` / `samples` / `files` / `contrasts` / `dataset`
  subcommands and `--fallback`.

**Behaviours established in this release**

- Mission aliases: `RRRM-1 (RR-8)` = RR-8, `RR-17` = RRRM-2, `RR-1_BSP` =
  RR-1; comma-joined identifiers; ~22 datasets carry a `mission name` but no
  Project Identifier.
- Sample groups = unique combinations of factor values joined by ` & `, in
  the order used by the study's contrasts file; a group may combine more than
  two factors.
- When a study has more than one comparison matching the request (e.g.
  OSD-48 carcass vs upon-euthanasia), the assistant lists the available
  contrasts and asks rather than choosing.
- Differential-expression output: default columns `ENSEMBL`, `SYMBOL`,
  `Log2fc_(g1)v(g2)`, `Adj.p.value_(g1)v(g2)` (≤ 0.05), `Stat_(g1)v(g2)`,
  plus `Group.Mean_` / `Group.Stdev_` for both groups; count of significant
  features; top-10 up- and down-regulated by log2FC; ends by offering a CSV
  of all significant features.
- "Has GeneLab-processed data" = at least one file in the *GeneLab Processed*
  category whose name does not contain `fastqc`, `multiqc` or `md5sum`
  (`file.filename=/^(?!.*(fastqc|multiqc|md5sum)).*/`). Inspiration4 →
  OSD-572/573/574/630; RR liver → 9 datasets with correct assay categories.
- Subject identifier = Project Identifier + ` | ` + Source Name
  (e.g. `RR-1 | RR1_FLT_M23`), used for cross-dataset subject matching.
- Study title via `investigation.study.study%20title`; DOI via
  `investigation.study.comment.doi`.
- "Datasets with data files" (no mention of *processed*) = bare
  `&file.category`, all file kinds; the FastQC/MultiQC exclusion applies only
  when the user asks for GeneLab-processed data.
- The data-file type follows the request, not the organism: microbial
  RNA-seq studies (e.g. OSD-145) have `differential_expression` files.
- When a contrasts file exists, only contrasts that appear verbatim in it
  are offered; groups are built from factor levels only for studies with no
  contrasts file (then confirmed against the data-file header).
- The identifier column (`ENSEMBL` / `TAIR` / `gene_id`) is always shown
  first; `SYMBOL` is always requested (animal and plant tables have it) and
  dropped on a 500 (some microbe tables lack it).

**GeneLab Knowledge Graph (`mcp-genelab`)**

- §0b in `SKILL.md` and `references/mcp-genelab.md`: when `mcp-genelab:*`
  tools are present, questions about a known OSD accession go to the KG first
  (`get_study_info`, `select_assays`, `find_differentially_expressed_genes`,
  `…methylated_regions`, `…abundant_organisms`, `find_common_*`); studies or
  assays the KG lacks, sample-level metadata, files, counts tables and all
  OSDR-wide discovery go to the API; mixed answers use both. Without the
  server the skill is API-only and does not mention the KG.
- Every answer labels its parts: `Source: GeneLab KG via mcp-genelab —
  <tool>(<args>)` or `Source: OSDR BioData API — <URL>`.

**Compatibility**

Agent Skills format; loads unchanged in Claude (claude.ai, desktop, Cowork,
Claude Code), ChatGPT / Codex, Gemini (Spark, CLI) and VS Code / GitHub
Copilot. Tested on Claude Haiku, Sonnet, Opus and Fable, with and without
the `mcp-genelab` server connected.
