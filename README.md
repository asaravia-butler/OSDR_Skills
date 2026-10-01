# OSDR BioData API skill — `osdr-biodata-api` v1.0.0

A skills package that lets an AI assistant (Claude, ChatGPT/Codex, Gemini,
VS Code / GitHub Copilot) answer natural-language questions about NASA OSDR
biological data by building and running the correct
[OSDR Biological Data API](https://visualization.osdr.nasa.gov/biodata/api/)
calls. The API is public — no key, no login — and every call is a plain HTTPS
GET URL.

## What it does

With the skill installed you can ask things like:

- *List all mouse RNA-seq datasets from spaceflight missions.*
- *Which OSDR datasets come from the RR-1 mission, and what assays and tissues do they include?*
- *Find female mouse liver samples.* / *Which Rodent Research datasets used only female mice?*
- *List all amplicon-seq datasets where a plant was the host organism.*
- *Which Inspiration4 datasets contain GeneLab-processed data files?*
- *Show me the differentially expressed genes for OSD-515, space flight vs ground control.*
- *Which animals appear in both OSD-102 and OSD-104, and what tissues and assays does each have?*
- *Tell me about OSD-248: what was studied, what are the treatment groups and how many samples in each?*

and the assistant will:

- pick the right endpoint (`datasets`, `assays`, `samples`, `data`, or the
  per-dataset REST tree) and build a correctly encoded URL;
- filter on the canonical metadata fields (organism, tissue, technology,
  mission / project identifier, spaceflight and other factors, sex, strain,
  age, host organism for microbiome studies, file names and categories);
- fall back correctly when a first query is empty (characteristic ↔ factor
  value, field-name discovery, legacy file names);
- pull rows from GeneLab-processed tables (differential expression,
  methylation, abundance, counts) — reading the study's contrasts file first,
  asking which comparison you mean when a study has several, and returning
  ENSEMBL/SYMBOL, log2 fold change, adjusted p, Wald statistic and the group
  means/SDs, with top-10 up/down tables and an offer of a CSV;
- report distinct OSD accessions, the URLs it ran, and the study DOI /
  version reminder;
- **redirect** out-of-scope requests (astronaut data → NLSP/LSDA/LSAH,
  environmental telemetry → EDA, radiation dosimetry → RadLab, biospecimens →
  NBISC, microbial isolates → SMCC) without running a biodata query.

## Limitations

- **Scope.** Biological data in OSDR only. Environmental telemetry, radiation
  dosimetry, physical biospecimens, microbial isolates and NASA human
  astronaut records live in other systems; the skill points to them but does
  not query them.
- **Network.** The assistant's environment must be able to reach
  `https://visualization.osdr.nasa.gov` (and `osdr.nasa.gov` for file
  downloads). Sandboxed clients may need that host allow-listed — see the
  installation guides.
- **Server timeouts.** Very broad queries (repository-wide file-name scans,
  many filters plus many output columns) can return HTTP 504 after ~60 s. The
  skill retries the same URL and prefers a narrow-then-expand strategy, but a
  few questions may take more than one call.
- **Not in the API.** Dataset version numbers (use the S3 bucket), full-text
  search, a count endpoint, and the `/v2/metadata/fields/` endpoint listed in
  the OpenAPI spec (currently 404). Study DOIs *are* available.
- **Model dependence.** Tested with Claude (Haiku, Sonnet, Opus, Fable). The
  package follows the Agent Skills format that ChatGPT/Codex, Gemini and
  Copilot load, and the instructions are written for smaller models, but
  answer completeness varies with the model; the `docs/evals.json` cases are
  the acceptance test for any client.
- **Gene annotation.** Some microbial differential-expression tables have no
  `SYMBOL` column; results are then keyed by `gene_id` only and the skill
  offers to list the remaining columns.

## What is in the package

Download **`osdr-biodata-api.zip`** (the folder `osdr-biodata-api/` is the zip
root — use this for Claude, ChatGPT/Codex, Gemini CLI and VS Code) or
**`osdr-biodata-api-flat.zip`** (`SKILL.md` at the zip root — for uploaders
that require it, e.g. the Gemini web app). The unpacked package is also in
[`package/`](package/) for browsing.

| File | Required? | What it is |
|---|---|---|
| `SKILL.md` | **Yes** | The skill: frontmatter (`name`, `description`) that the client uses to decide when to load it, plus the instructions — scope gate, quick-reference filters, step-by-step procedure, URL grammar, endpoint choice and cost ladder, empty-result fallbacks, data-file (DE/DM/DA) recipe and output contract, subject/cohort rules, reporting rules. 370 lines. |
| `references/fields.md` | Recommended | Canonical metadata field paths, alias order (age, tissue, strain, mission variants), and live vocabularies with counts (organisms, host organisms, technologies, measurement types, project identifiers incl. RR/RRRM aliases, spaceflight values, sex, file categories/subcategories/data types, factor and characteristic names). |
| `references/processed-files.md` | Recommended | GeneLab standardized file names per omics type, their columns, how sample groups and contrasts are named and built, the three-step data-pull recipe, the "has GeneLab-processed data" rule, and size limits. |
| `references/cohorts.md` | Recommended | Python snippets: retry helper, per-accession enrichment, subject IDs (Project Identifier + Source Name), "all samples are X" datasets, two-facet intersections, meta-analysis corpus, astronaut/human requests. |
| `references/examples.md` | Recommended | 65 verified question → URL pairs (copy-paste templates with expected row counts). |
| `references/network-setup.md` | Recommended | Hosts to allow-list, how to run calls (`curl -g`), per-client network notes. |
| `references/scope.md` | Recommended | OSD/GLDS/LSDS identifier model, DOI and version lookup, verbatim out-of-scope reply templates, current API limitations. |
| `scripts/osdr_query.py` | Optional | Standard-library Python helper that builds, runs (with retries) and summarises a query: `python3 scripts/osdr_query.py assays organism=musculus tech=rna-seq`, `… files OSD-515`, `… contrasts OSD-48`, `… dataset OSD-104`. Useful in clients that can run code; harmless where they cannot. |

The reference files are loaded by the assistant only when `SKILL.md` points to
them, so they cost nothing until needed.

## Installation

One guide per client, each covering the **web/browser app**, the **desktop
app**, and (where relevant) the command-line tool:

- [Claude (claude.ai, Claude desktop, Claude Code, Cowork)](docs/install-claude.md)
- [ChatGPT and Codex](docs/install-chatgpt.md)
- [Gemini (web app and Gemini CLI)](docs/install-gemini.md)
- [VS Code / GitHub Copilot (desktop and github.com)](docs/install-vscode-copilot.md)

After installing, run the short test in [`docs/testing.md`](docs/testing.md).

## Examples

[`examples/`](examples/) contains a shared set of example prompts with the
expected answers (counts, accessions, tables) and one file per client showing
how to invoke the skill there and what a correct response looks like.

## Other documentation

- [`docs/testing.md`](docs/testing.md) — how to run the acceptance tests; `docs/evals.json` holds the 23 cases.
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md) — version history.
- [`docs/design-notes.md`](docs/design-notes.md) — why the package is structured this way and the API behaviours it encodes.

## Sources

- API: <https://visualization.osdr.nasa.gov/biodata/api/> (OpenAPI: `/openapi.json`)
- Tutorial: <https://osdr-tutorials.readthedocs.io/en/latest/pages/guides/biological_data_api.html>
- GeneLab processing pipelines: <https://github.com/nasa/GeneLab_Data_Processing>

## Citation and licence

Cite OSDR studies by DOI and state the dataset version. OSDR data are public
domain; the skill text is CC0.
