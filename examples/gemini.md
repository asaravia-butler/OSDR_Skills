# Examples — Gemini

Applies to Gemini Spark (gemini.google.com and the Gemini desktop app) and
the Gemini CLI. Installation:
[`../docs/install-gemini.md`](../docs/install-gemini.md).
Expected results for every example: [`README.md`](README.md).

**Status:** the expected outputs below come from the live API and are
identical to those validated in Claude. Gemini transcripts from testers
should be added here (open a PR on this branch with the model and date).

## How the skill is invoked

- **Gemini Spark (web / desktop):** in a Spark task type `/` and choose
  **osdr-biodata-api**, or just ask. Spark fetches the API URLs with its
  browsing tool. It **cannot run** `scripts/osdr_query.py` (no network from
  scripts), so all answers come from the plain URLs — every recipe in the
  skill supports that.
- **Gemini CLI:** ask, or mention the skill name. Gemini asks you to approve
  activating the skill, then runs `curl -g …` (or the Python helper) through
  its shell tool; approve those calls.
- A correct answer always lists the URL(s) run.

---

## Example 1 — E1, simple discovery

**Prompt:** `/osdr-biodata-api List all Drosophila datasets in OSDR with their titles.`

**Expected answer:** 17 datasets (OSD-1, 3, 27, 34, 36, 70, 85, 96, 207,
278, 347, 514, 588, 590, 592, 595, 596) with titles, the URL
`…/v2/query/datasets/?study.characteristics.organism=/drosophila/&investigation.study.study%20title&format=json.records`,
and the DOI / version reminder.

**Gemini CLI transcript shape:**

```
> List all Drosophila datasets in OSDR with their titles.
✦ The osdr-biodata-api skill matches this request. Activate it? (y/n) y
✦ Running: curl -g -s "https://visualization.osdr.nasa.gov/biodata/api/v2/query/datasets/?study.characteristics.organism=/drosophila/&investigation.study.study%20title&format=json.records"
✦ Found 17 Drosophila datasets: …
```

---

## Example 2 — E7, set difference

**Prompt:** `Which Rodent Research datasets used only female mice?`

**Expected answer:** ~89 datasets. Two acceptable methods, and the answer
must say which was used:

- **Two queries:** all RR datasets
  (`Project%20Identifier=/^RR-?\d|^RRRM/`, 130) minus RR datasets with any
  sample where `study.characteristics.sex=/male/` **anchored as `/^male/`**
  (because `/male/` also matches *female*); or
- **One query:** `/samples/` for RR datasets with the `sex` column, grouped
  per dataset in the answer, keeping datasets whose only value is *Female*.

Common failure: using `/male/` unanchored and reporting zero female-only
datasets.

---

## Example 3 — E4, differential expression

**Prompt:** `Show me the differentially expressed genes for OSD-515, space flight vs ground control.`

**Expected answer:** files call → pin
`GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv` → contrast
`(Space Flight)v(Ground Control)` → **3,947 significant genes** → top-10 up
and top-10 down tables (ENSEMBL, SYMBOL, log2FC, adj p, Wald stat, group
mean/SD for both groups; values in
[`README.md` E4](README.md#e4--genelab-processed-differential-expression-unambiguous))
→ *Would you like a downloadable CSV of all significant genes?*

In Spark, the CSV offer is fulfilled by giving the `format=csv` URL for the
same query (Spark cannot write files); in the CLI the file is written to the
working directory.

---

## Example 4 — E5, ambiguous comparison

**Prompt:** `Get the differentially expressed genes for flight vs ground in OSD-48 with adj p < 0.05 and |log2FC| > 1.`

**Expected answer:** reads `GLDS-48_rna_seq_contrasts_GLbulkRNAseq.csv`,
finds the two flight-vs-ground contrasts (Carcass pair; Upon-euthanasia
pair), lists them and **asks** which one. Note that the methylation contrasts
file (`_GLMethylSeq`) must not be used, and a regex such as
`/contrasts_GL/` matches both files and returns HTTP 422 — the skill tells
the assistant to use the exact file name.

---

## Example 5 — E9, GeneLab-processed detection

**Prompt:** `Which Inspiration4 datasets contain GeneLab-processed data files?`

**Expected answer:** OSD-572, OSD-573, OSD-574, OSD-630 only. The URL
contains `file.filename=/^(?!.*(fastqc|multiqc|md5sum)).*/`. If Gemini's
browsing tool rewrites the regex (some URL sanitisers drop `(?!`), it should
fall back to fetching `file.filename` for all GeneLab-Processed files and
filtering client-side — still four datasets.

---

## Example 6 — E12–E14, out-of-scope redirects

| Prompt | Expected |
|---|---|
| `Show me the temperature and CO2 readings on ISS during RR-1.` | First sentence: outside this skill → `https://visualization.osdr.nasa.gov/eda/`. No biodata URL. |
| `List all human astronaut datasets in OSDR.` | Redirect to NLSP / LSDA / LSAH; no query. |
| `I need physical tissue samples from the RR-9 mice — how do I get them from OSDR?` | Redirect to NBISC; no query. |

---

## Recording a transcript

When adding a real transcript, include: client (Spark web / desktop / CLI),
model, date, the prompt verbatim, the URLs or commands the assistant ran,
the row counts it reported, and whether the behaviour matched the
expectation above.
