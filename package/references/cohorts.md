# Cohorts, subjects and multi-step recipes

Contents: 1 Retry helper · 2 Per-accession enrichment · 3 Subject IDs and
per-subject tables · 4 "All samples are X" datasets · 5 Two facets / two
files (narrow-then-expand) · 6 Meta-analysis corpus · 7 Astronaut / human
requests

All snippets are Python 3 standard library. `BASE` =
`https://visualization.osdr.nasa.gov/biodata/api`.

## 1. Retry helper (504 = server timeout, not a bad URL)

```python
import json, time, urllib.request, urllib.error
BASE = "https://visualization.osdr.nasa.gov/biodata/api"

def get_json(url, tries=3, wait=12, timeout=200):
    """GET a json.records URL; retry the identical URL on 504/5xx or HTML body."""
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                body = r.read()
            if body[:1] in (b"[", b"{"):
                return json.loads(body)
        except urllib.error.HTTPError as e:
            if e.code < 500:            # 400/422 = fix the URL, do not retry
                raise
        except Exception:
            pass
        time.sleep(wait)
    raise RuntimeError("OSDR did not answer after retries: " + url)
```

## 2. Per-accession enrichment (fast, parallel-safe)

`/v2/dataset/OSD-###/` answers in 0.5–3 s and never timed out in testing.
Keys are lower-case with spaces; multi-assay values are lists.

```python
from concurrent.futures import ThreadPoolExecutor

# keys live under tree["OSD-###"]["metadata"]; "mission" is {name, start date, end date};
# the DOI is not in this tree (query investigation.study.comment.doi instead)
WANT = ["study title", "project identifier", "project type", "mission",
        "material type", "organism", "study assay technology type", "study factor name"]

def find_key(obj, key):
    """Recursive lookup; the tree nesting varies by study."""
    if isinstance(obj, dict):
        if key in obj: return obj[key]
        for v in obj.values():
            r = find_key(v, key)
            if r is not None: return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_key(v, key)
            if r is not None: return r
    return None

def enrich(acc):
    tree = get_json(f"{BASE}/v2/dataset/{acc}/")
    row = {"accession": acc}
    for k in WANT:
        v = find_key(tree, k)
        if k == "mission" and isinstance(v, dict):
            v = v.get("name")
        row[k] = ", ".join(map(str, v)) if isinstance(v, list) else v
    return row

accs = [r["id.accession"] for r in get_json(
    BASE + "/v2/query/datasets/?study.characteristics.organism=/drosophila/&format=json.records")]
with ThreadPoolExecutor(6) as ex:
    table = list(ex.map(enrich, accs))
```

Use this instead of adding many bare columns to a broad `/v2/query/` call.

## 3. Subject IDs and per-subject tables

OSDR has no subject field. **Subject ID = Project Identifier + " | " + Source
Name.** Source name is the study's stable per-animal / per-plant / per-culture
label (e.g. `RR1_FLT_M23`), and it is shared by every tissue dataset of that
mission, so the pair identifies one individual across studies.

```
BASE/v2/query/samples/?study.characteristics.organism=/musculus|rattus/&investigation.study.comment.Project%20Identifier&study.source%20name&study.characteristics.material%20type&format=json.records
```

```python
from collections import defaultdict
rows = get_json(URL_ABOVE)
subj = defaultdict(lambda: {"tissues": set(), "assays": set(), "datasets": set()})
for r in rows:
    name = r.get("id.sample name", "")
    if any(t in name.lower() for t in ("pool", "empty", "blank")) \
       or r.get("study.characteristics.organism") == "Not Applicable":
        continue                                   # QC / pooled samples
    sid = f'{r["investigation.study.comment.project identifier"]} | {r["study.source name"]}'
    subj[sid]["tissues"].add(r["study.characteristics.material type"])
    subj[sid]["assays"].add(r["id.assay name"])
    subj[sid]["datasets"].add(r["id.accession"])
ranked = sorted(subj.items(), key=lambda kv: (-len(kv[1]["tissues"]), -len(kv[1]["assays"])))
```

Example: OSD-102 (kidney) and OSD-104 (soleus) share 12 subjects
`RR-1 | RR1_FLT_M23 … RR1_GC_M38`. Restrict with `id.accession=/^OSD-10[24]$/`.

## 4. "Datasets where all samples are X" (e.g. female-only)

`sex=/female/` returns datasets with *any* female sample. For "female only"
pull samples with both sex fields and classify per dataset:

```
BASE/v2/query/samples/?study.characteristics.organism=/musculus/&investigation.study.comment.Project%20Identifier=/^RR-?\d|^RRRM/&study.characteristics.sex&study.factor%20value.sex&format=json.records
```

```python
by = defaultdict(set)
for r in rows:
    s = r.get("study.characteristics.sex") or r.get("study.factor value.sex")
    if s and s.lower() not in ("not applicable", "not available"):
        by[r["id.accession"]].add(s.lower())
female_only = sorted(a for a, s in by.items() if s == {"female"})
```

## 5. Two facets or two files — narrow, then expand

A single assay row is never both RNA-seq and methylation, and repository-wide
`file.filename` scans can time out. So:

1. Cheap facet → accession list, e.g.
   `BASE/v2/query/datasets/?investigation.study%20assays.study%20assay%20technology%20type=/bisulfite|methylation/&format=json.records` (≈21).
2. Per accession, check files:
   `BASE/v2/query/assays/?id.accession=OSD-47&file.filename=/differential_expression|differential_methylation/&format=json.records`
3. Keep accessions that have both. Result at time of writing: **OSD-47, 48,
   103, 105** have both DE and DM tables; ~16 further methylation datasets have
   a DE table but only raw RRBS/WGBS reads.

Same pattern for "RR-# liver datasets": `Project%20Identifier=/^RR-?\d|^RRRM/`
→ accessions; `material%20type=/liver/` → accessions; intersect (10 datasets).

## 6. Meta-analysis corpus

"All mouse liver RNA-seq with ≥3 replicates and matched controls": enumerate
by organism + tissue + technology (one assays query), then per accession pull
sample rows (`/v2/query/samples/?id.accession=OSD-###&study.factor%20value`)
to count replicates per factor-value group and confirm a control group exists.
Replicate count and "matched control present" are not query facets.
Harmonisation (reprocessing, orthology) is the user's job.

## 7. Astronaut / human requests

First sentence, always: "OSDR does not host NASA human astronaut data" + the
NLSP/LSDA/LSAH links (SKILL.md §0). Then, if useful, what OSDR does hold:

```
# non-NASA crew (Inspiration4) — filter on the project, not organism (3 of 10 are Microbiota)
BASE/v2/query/datasets/?investigation.study.comment.Project%20Identifier=/Inspiration/&investigation.study.comment.project%20type&format=json.records
# all Homo sapiens datasets, then classify with project type + material type (in-vitro = Cells / Cultured)
BASE/v2/query/datasets/?study.characteristics.organism=/sapiens/&format=json.records   → enrich per accession (§2)
```
Ground analogs (bed rest, confinement, limb suspension) and in-vitro cell
studies must be labelled as such, never as astronaut data.
