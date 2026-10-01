# Examples — ChatGPT and Codex

Applies to the ChatGPT web app and desktop app (Business / Enterprise / Edu
workspaces with skills enabled) and to Codex (app, IDE extension, CLI).
Installation: [`../docs/install-chatgpt.md`](../docs/install-chatgpt.md).
Expected results for every example: [`README.md`](README.md).

**Status:** the expected outputs below come from the live API and are
identical to those validated in Claude. Client-specific transcripts from
ChatGPT / Codex testers should be added here (open a PR on this branch with
the model and date).

## How the skill is invoked

- **ChatGPT:** type `@osdr-biodata-api` at the start of the message to force
  the skill, or just ask — it loads silently when the description matches.
  ChatGPT fetches the API URLs with its browsing tool. It does not always
  show which skill it used; ask *"which skill did you use?"* if unsure.
- **Codex:** type `$osdr-biodata-api` to force it, or just ask. Codex runs
  `curl -g …` or `python3 scripts/osdr_query.py …` in its sandbox; approve
  the command (and enable network for the thread if the first call fails).
- A correct answer always lists the URL(s) run.

---

## Example 1 — E1, simple discovery

**Prompt:** `@osdr-biodata-api List all Drosophila datasets in OSDR with their titles.`

**Expected answer:**

- 17 datasets in a table (OSD-1, 3, 27, 34, 36, 70, 85, 96, 207, 278, 347,
  514, 588, 590, 592, 595, 596) with titles;
- the URL
  `…/v2/query/datasets/?study.characteristics.organism=/drosophila/&investigation.study.study%20title&format=json.records`;
- the DOI / version reminder.

**Codex variant:** the command shown in the transcript is
`python3 ~/.agents/skills/osdr-biodata-api/scripts/osdr_query.py datasets organism=drosophila title`
or the equivalent `curl -g`; the summary line reads `DATASETS (17): OSD-1, OSD-3, …`.

---

## Example 2 — E2, mission discovery

**Prompt:** `Which OSDR datasets come from the RR-1 mission, and what assays and tissues do they include?`

**Expected answer:** 25 datasets (80 assay rows) in a dataset × assays ×
tissue table, including OSD-212 (`RR-1_BSP`, 16S faeces) and datasets whose
label is comma-joined (OSD-168 `RR-1, RR-3`; OSD-662 `RR-1, RR-9, RR-18,
Bion-M1, GROUND-2`); none of RR-10…RR-19. The URL contains
`Project%20Identifier=/RR-1([^\d]|$)|RR1([^\d]|$)/`.

Common failure to watch for: an unanchored `/RR-1/` regex, which pulls in
RR-10 to RR-19 (~40 extra datasets).

---

## Example 3 — E4, differential expression

**Prompt:** `Show me the differentially expressed genes for OSD-515, space flight vs ground control.`

**Expected answer:** in order,

1. the files call (`…/v2/dataset/OSD-515/files/`) and the chosen file
   `GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv`;
2. the contrast `(Space Flight)v(Ground Control)`;
3. **3,947 significant genes** at adj p ≤ 0.05;
4. top-10 up and top-10 down tables with ENSEMBL, SYMBOL, log2FC, adj p,
   Wald stat, group mean/SD for both groups (values in
   [`README.md` E4](README.md#e4--genelab-processed-differential-expression-unambiguous));
5. the closing question *Would you like a downloadable CSV of all significant
   genes?* — in ChatGPT the CSV is produced with the code-interpreter tool;
   in Codex it is written to the working directory.

---

## Example 4 — E5, ambiguous comparison

**Prompt:** `Get the differentially expressed genes for flight vs ground in OSD-48 with adj p < 0.05 and |log2FC| > 1.`

**Expected answer:** no DE rows yet. The assistant reads
`GLDS-48_rna_seq_contrasts_GLbulkRNAseq.csv`, lists the two flight-vs-ground
contrasts (`Carcass` pair and `Upon euthanasia` pair) and asks which to use.
Running both, or choosing one silently, is a failure.

---

## Example 5 — E9, GeneLab-processed detection

**Prompt:** `Which Inspiration4 datasets contain GeneLab-processed data files?`

**Expected answer:** OSD-572, OSD-573, OSD-574, OSD-630 only (metagenomics).
The URL must contain
`file.filename=/^(?!.*(fastqc|multiqc|md5sum)).*/`. Listing ten datasets
means the FastQC/MultiQC exclusion was dropped.

---

## Example 6 — E12–E14, out-of-scope redirects

| Prompt | Expected |
|---|---|
| `Show me the temperature and CO2 readings on ISS during RR-1.` | First sentence: outside this skill → EDA link `https://visualization.osdr.nasa.gov/eda/`. No biodata URL; no attempt to browse `/eda/api`. |
| `List all human astronaut datasets in OSDR.` | Redirect to NLSP / LSDA / LSAH; no query. |
| `I need physical tissue samples from the RR-9 mice — how do I get them from OSDR?` | Redirect to NBISC; no query. |

ChatGPT's browsing tool may be tempted to open the EDA page and summarise
it; that is acceptable, but building biodata URLs for telemetry is not.

---

## Recording a transcript

When adding a real transcript, include: client (ChatGPT web / desktop /
Codex app / CLI), model, date, the prompt verbatim, the URLs or commands
the assistant ran, the row counts it reported, and whether the behaviour
matched the expectation above.
