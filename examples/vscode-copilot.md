# Examples — VS Code / GitHub Copilot

Applies to Copilot Chat in VS Code (Agent mode), the Copilot coding agent
on github.com and the Copilot CLI. Installation:
[`../docs/install-vscode-copilot.md`](../docs/install-vscode-copilot.md).
Expected results for every example: [`README.md`](README.md).

**Status:** the expected outputs below come from the live API and are
identical to those validated in Claude. Copilot transcripts from testers
should be added here (open a PR on this branch with the model and date).

## How the skill is invoked

- **VS Code:** open Copilot Chat, set the mode picker to **Agent**, and ask
  — or type `/osdr-biodata-api` followed by the question. Copilot shows a
  *"Used skill: osdr-biodata-api"* reference and runs `curl -g …` or
  `python3 .github/skills/osdr-biodata-api/scripts/osdr_query.py …` in the
  integrated terminal; click **Allow** on the terminal-command prompt.
- **github.com:** open Copilot on the repository (or assign an issue). The
  agent reads `.github/skills/osdr-biodata-api/` and runs the calls in its
  cloud sandbox — remember the firewall allowlist in the install guide.
- **Copilot CLI:** ask; the skill is loaded when the prompt matches.
- A correct answer always lists the URL(s) or commands run.

---

## Example 1 — E1, simple discovery

**Prompt:** `/osdr-biodata-api List all Drosophila datasets in OSDR with their titles.`

**Expected answer:** 17 datasets (OSD-1, 3, 27, 34, 36, 70, 85, 96, 207,
278, 347, 514, 588, 590, 592, 595, 596) with titles; the URL
`…/v2/query/datasets/?study.characteristics.organism=/drosophila/&investigation.study.study%20title&format=json.records`;
DOI / version reminder.

**Typical VS Code transcript shape:**

```
Used skill: osdr-biodata-api
▶ Run in terminal
  python3 .github/skills/osdr-biodata-api/scripts/osdr_query.py datasets organism=drosophila title
  …
  DATASETS (17): OSD-1, OSD-3, OSD-27, OSD-34, OSD-36, OSD-70, OSD-85, OSD-96, OSD-207, OSD-278, OSD-347, OSD-514, OSD-588, OSD-590, OSD-592, OSD-595, OSD-596

There are 17 Drosophila datasets in OSDR:
| Accession | Title | …
```

---

## Example 2 — E2, mission discovery

**Prompt:** `Which OSDR datasets come from the RR-1 mission, and what assays and tissues do they include?`

**Expected answer:** 25 datasets (80 rows) in a dataset × assays × tissue
table; includes OSD-212 (`RR-1_BSP`) and comma-joined labels (OSD-168,
OSD-488, OSD-662); excludes RR-10…RR-19. URL contains
`Project%20Identifier=/RR-1([^\d]|$)|RR1([^\d]|$)/`.

Script form: `osdr_query.py assays 'project=/RR-1([^\d]|$)|RR1([^\d]|$)/' tech tissue`.

---

## Example 3 — E6, cohort intersection

**Prompt:** `Which animals appear in both OSD-102 and OSD-104, and what tissues and assays does each have?`

**Expected answer:** two `/samples/` calls (one per accession, with
`study.source%20name` and Project Identifier),
subject IDs of the form `RR-1 | RR1_FLT_M23`, **12 shared subjects**, and a
table subject → tissue (kidney in OSD-102, soleus in OSD-104) → assays.
Copilot typically does the intersection in a short Python snippet in the
terminal, which is fine.

---

## Example 4 — E4, differential expression

**Prompt:** `Show me the differentially expressed genes for OSD-515, space flight vs ground control.`

**Expected answer:** `osdr_query.py files OSD-515` (or the files URL) →
pin `GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv` →
`osdr_query.py contrasts OSD-515` → `(Space Flight)v(Ground Control)` →
data call with the default columns and adj p ≤ 0.05 → **3,947 genes** →
top-10 up / down tables with ENSEMBL, SYMBOL, log2FC, adj p, Wald stat,
group mean/SD (values in
[`README.md` E4](README.md#e4--genelab-processed-differential-expression-unambiguous))
→ *Would you like a downloadable CSV of all significant genes?* (Copilot
writes it into the workspace, e.g. `OSD-515_DE_significant.csv`.)

---

## Example 5 — E5, ambiguous comparison

**Prompt:** `Get the differentially expressed genes for flight vs ground in OSD-48 with adj p < 0.05 and |log2FC| > 1.`

**Expected answer:** `osdr_query.py contrasts OSD-48` → two flight-vs-ground
contrasts (Carcass pair; Upon-euthanasia pair) → Copilot **asks** which one
before pulling any rows.

---

## Example 6 — E9, GeneLab-processed detection

**Prompt:** `Which Inspiration4 datasets contain GeneLab-processed data files?`

**Expected answer:** OSD-572, OSD-573, OSD-574, OSD-630 only; URL includes
`file.filename=/^(?!.*(fastqc|multiqc|md5sum)).*/`. Because the pattern
contains `(`, `!` and `|`, the terminal command must quote the URL in single
quotes and use `curl -g`; an unquoted command fails in bash/zsh and Copilot
should retry with quoting rather than change the query.

---

## Example 7 — E12–E14, out-of-scope redirects

| Prompt | Expected |
|---|---|
| `Show me the temperature and CO2 readings on ISS during RR-1.` | First sentence: outside this skill → `https://visualization.osdr.nasa.gov/eda/`. No biodata URL, no terminal command. |
| `List all human astronaut datasets in OSDR.` | Redirect to NLSP / LSDA / LSAH; no query. |
| `I need physical tissue samples from the RR-9 mice — how do I get them from OSDR?` | Redirect to NBISC; no query. |

---

## Recording a transcript

When adding a real transcript, include: surface (VS Code / github.com /
CLI), model, date, the prompt verbatim, the commands or URLs run, the row
counts reported, and whether the behaviour matched the expectation above.
