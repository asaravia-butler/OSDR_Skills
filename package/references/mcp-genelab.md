# `mcp-genelab` — the GeneLab Knowledge Graph (KG) as first source

Read this when `mcp-genelab:*` tools are present in the session. If they are
not, skip this file entirely and use the API.

Contents: 1 Tools · 2 Coverage and the KG-vs-API split · 3 Workflows ·
4 Provenance wording · 5 Differences between KG and API output

## 1. Tools (fully-qualified names)

| Tool | Use for | Notes |
|---|---|---|
| `mcp-genelab:create_session` | once per conversation | returns `session_id`; pass it to every other call; re-create if a tool says the session is unknown/expired |
| `mcp-genelab:get_study_info(study_id)` | "tell me about OSD-###", project title/description, organism, mission, assay inventory | one row per **assay = one contrast**: `factors_1` vs `factors_2`, technology, measurement, method (DESeq2 …), material. "No study found" ⇒ not in KG → API |
| `mcp-genelab:select_assays(study_id)` | groups / conditions of a study | numbered menu of factor combinations = the study's groups |
| `mcp-genelab:select_assays(study_id, selection="i,j")` | resolve group i vs group j to an assay id | `OSD-515-79b621bb…`; condition 1 = i (numerator), condition 2 = j |
| `mcp-genelab:find_differentially_expressed_genes(assay_id, adj_p_threshold, top_n)` | DE genes (RNA-seq, microarray) | returns top-N up and down with symbol, gene name, log2FC, adj p, group mean/SD, plus inline CSV; `top_n=None` = all passing rows |
| `mcp-genelab:find_differentially_methylated_regions(assay_id, …)` | DMRs (WGBS) | promoter/exon/intron filters; can pool replicate assays |
| `mcp-genelab:find_differentially_abundant_organisms(assay_id, …)` | DA organisms (16S/ITS; DESeq2 or ANCOM-BC) | method-aware significance |
| `mcp-genelab:find_common_*` | overlaps across assays / studies | DE genes, DMRs, DA organisms, DE∩DM |
| `mcp-genelab:create_volcano_plot`, `create_venn_diagram` | plots | only if asked |
| `mcp-genelab:query` | ad-hoc Cypher | last resort; the specialist tools above are preferred |

## 2. Coverage and the KG-vs-API split

KG = spoke-genelab v0.3.1 (built 11 March 2026): 212 studies, ~13 100
contrast-level assays; technologies
RNA Sequencing (RNA-Seq), DNA microarray, Whole Genome Bisulfite Sequencing,
16S, ITS; organisms incl. mouse, rat, human, Arabidopsis, Drosophila,
C. elegans, zebrafish, yeast, "Microbiota". `Mission` nodes are launch
vehicles (SpaceX-4 …), **not** Project Identifiers (RR-1, Inspiration4).

| Question | Source |
|---|---|
| What is OSD-### about; its groups / comparisons; which omics it has (of the KG types) | **KG** |
| DE genes / DMRs / DA organisms for a contrast in a KG study | **KG** |
| Overlap of DE/DM/DA results across contrasts or studies in the KG | **KG** |
| Study not in KG (e.g. OSD-145, OSD-95 microbial RNA-seq; OSD-572 metagenomics) | **API** (§6 of SKILL.md) |
| Sample-level metadata: n per group, sex, strain, age, source names, subjects across studies | **API** `/samples/` |
| File names, download URLs, count / normalized tables, GeneLab-processed inventory | **API** |
| Proteomics, imaging, micro-CT, behaviour, methylation *counts*, any non-KG assay | **API** |
| Discovery: datasets by organism / tissue / mission / factor / technology / file | **API** |
| DOI, study title field, version reminder | **API** (`investigation.study.comment.doi`) |

Mixed requests take both, each part labelled. Examples:
"Tell me about OSD-248: what was studied, the groups, and how many samples
per group" → KG `get_study_info` (title, description, groups) + API
`/samples/?id.accession=OSD-248&study.factor%20value&…` (n per group) + DOI.
"What data does OSD-47 have?" → KG lists RNA-seq and WGBS contrasts; API
`/v2/dataset/OSD-47/assays/` adds the microscopy and mass-spectrometry
assays the KG does not hold — report both, say which came from where.

## 3. Workflows

**DE / DM / DA for a known study (KG path)**
1. `create_session` (once).
2. `select_assays(study_id)` → group menu. Apply the same rule as SKILL.md
   §6 B: if the user's comparison matches more than one pair (or none), list
   the pairs and **ask**; do not pick or run all.
3. `select_assays(study_id, selection="i,j")` → assay id (check technology:
   RNA-seq/microarray → DE; WGBS → DM; 16S/ITS → DA).
4. `find_differentially_expressed_genes(assay_id, adj_p_threshold=0.05,
   top_n=10)` (or the DM/DA tool). Report the counts of significant up/down,
   the two top-10 tables (symbol, gene name, log2FC, adj p, group mean/SD),
   and end with "Would you like a downloadable CSV of all significant
   genes?" — on yes, rerun with `top_n=None` and save the CSV.
5. |log2FC| or other thresholds the tool does not expose → apply client-side
   to the `top_n=None` result.
6. Study or assay type absent → fall back to the API three-step recipe
   (SKILL.md §6) and say so.

**Study report (mixed path)**: `get_study_info` → KG part; then API for
sample counts, files and DOI as needed.

**Discovery (API path)**: skip the KG; optionally, once accessions are
known, use `get_study_info` to enrich those that are in the KG.

## 4. Provenance wording (mandatory in every answer)

- KG only: `Source: GeneLab KG via mcp-genelab — get_study_info("OSD-248");
  select_assays("OSD-248", "15,3"); find_differentially_expressed_genes("OSD-248-a0ba…", 0.05, 10)`
- API only: `Source: OSDR BioData API — <full URL(s)>`
- Mixed: one "Source:" line per part, e.g.
  `Study description and groups — GeneLab KG via mcp-genelab (get_study_info)` /
  `Sample counts per group — OSDR BioData API: <URL>`.
- Keep the existing DOI / version sentence from SKILL.md §8 after it.

## 5. Differences between KG and API output

- KG DE tables: gene **symbol** and name, log2FC, adj p, group mean/SD. No
  ENSEMBL/TAIR/gene_id column and no Wald statistic; genes without a symbol
  are not in the KG. Hence totals differ (OSD-515 Space Flight vs Ground
  Control: KG 2,511 up + 1,043 down = 3,554; API file 3,947 incl. unannotated
  genes). State the KG count as "annotated genes in the KG" and offer the API
  file if the user wants ENSEMBL ids, Wald statistics or every gene.
- KG contrast naming: `factors_1` vs `factors_2` as comma-joined lists
  (`Space Flight,Carcass`); the API file uses `(Space Flight & Carcass)v(Ground
  Control & Carcass)`. Same groups, different spelling.
- KG has no `rRNArm` variants and no legacy (pre-GeneLab-pipeline) results.
