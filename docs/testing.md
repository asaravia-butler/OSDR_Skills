# Testing `osdr-biodata-api`

The acceptance suite is [`evals.json`](evals.json): 23 prompts, each with the
expected endpoint, URL fragments, row count and behaviour. It is the
regression set every change to the package is checked against, and the
quickest way to find out whether the skill works in a given client / model.

## Smoke test (5 minutes)

Run these seven in a **fresh chat** after installing:

| # | Prompt | Pass when |
|---|---|---|
| 21 | List all Drosophila datasets with their titles. | 17 datasets; URL has `organism=/drosophila/` and `investigation.study.study%20title` |
| 2 | Which OSDR datasets come from the RR-1 mission, and what assays and tissues do they include? | 25 datasets / 80 rows; regex anchored so RR-10…RR-19 are excluded; `RR-1_BSP` included |
| 18 | Show me the differentially expressed genes for OSD-515, space flight vs ground control. | Lists files → picks the one `_GLbulkRNAseq_differential_expression` file (not `rRNArm`) → ~3,947 genes at adj p ≤ 0.05 → top-10 up/down with log2FC, adj p, Wald stat, group mean/SD → offers a CSV |
| 14 | Get the differentially expressed genes for flight vs ground in OSD-48 with adj p < 0.05 and \|log2FC\| > 1. | Reads the contrasts file, finds **two** flight-vs-ground comparisons, lists them and **asks** which one instead of choosing |
| 22 | list all inspiration 4 datasets that contain data files | All **10** Inspiration4 datasets with their file categories; one call with bare `&file.category` and **no** FastQC/MultiQC filter (that filter is only for "GeneLab-processed") |
| 23 | List the differentially expressed genes for OSD-145 flight vs ground control comparison, filtered to adj p < 0.05 and \|log2FC\| > 1 | Uses the `differential_expression` file (microbial RNA-seq, not differential abundance); only one flight-vs-ground contrast exists so no question; `gene_id` is the first column; `SYMBOL` requested → 500 → same URL rerun without it; 1,513 significant, 239 with \|log2FC\| > 1 |
| 9 | Show me the temperature and CO2 readings on ISS during RR-1. | First sentence says this is outside the skill and links the EDA; **no** biodata URL and no probing of other APIs |

## Full protocol (about 20 minutes per client)

For each case in `evals.json`, in a fresh chat, paste the `prompt` and check:

1. **Triggering.** The skill activates. Claude and Gemini show it; ChatGPT
   and Copilot load it silently — ask *"which skill did you use?"* if unsure.
   If an OSDR question does not trigger the skill, note the wording; the
   `description` in `SKILL.md` probably needs those words.
2. **URL shape.** Every fragment in `expected_url_contains` appears in a URL
   the assistant ran (it must report its URLs).
3. **Execution.** HTTP 200 and a row/dataset count within about ±30% of
   `expected_rows` (OSDR grows; counts in this file were taken in September
   2026). A blocked call must be reported as a network problem with the URL
   handed to you, not silently rewritten into a different query.
4. **Behaviour.** The note in `behaviour` — e.g. the two-query set difference
   for case 16, the ask-before-choosing rule for case 14, the DOI / version
   reminder in dataset-level answers, verbatim redirects for cases 9, 11, 17.

Record per client and model: case id · pass / fail · what the assistant did
instead. Failures with the transcript attached are the most useful input for
the next version — open an issue on this branch.

## Known-good results at 1.0.0

Tested with Claude Haiku, Sonnet, Opus and Fable (claude.ai and Cowork). All
23 cases pass on Sonnet and above; on Haiku the remaining variability is
occasionally choosing `column.*` for a whole table (case 4) or forgetting the
CSV offer. Other clients load the same package; their transcripts should be
added to `examples/` as they are collected.

## Regenerating the reference counts

`references/examples.md` in the package lists 65 verified URLs with row
counts. To re-verify them against the live API (all are plain GETs):

```bash
cd package
grep -o 'https://visualization.osdr.nasa.gov[^ )`]*' references/examples.md | sort -u | \
while read u; do printf '%s ' "$u"; curl -g -s -o /dev/null -w '%{http_code}\n' "$u"; done
```

Anything other than `200` (or a transient `504`) means the API or vocabulary
has changed and the corresponding line should be updated.
