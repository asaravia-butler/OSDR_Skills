#!/usr/bin/env python3
"""
osdr_query.py — build, run and summarise NASA OSDR Biological Data API calls.

Standard library only (Python 3.8+). No API key needed.

USAGE
  python3 osdr_query.py <endpoint> [shortcut=value ...] [field=value ...] [options]
  python3 osdr_query.py url "<full or BASE-relative URL>" [options]
  python3 osdr_query.py files OSD-515 [pattern]           # list processed files
  python3 osdr_query.py contrasts OSD-515 [token|file]    # contrast names (default bulk RNA-seq file)
  python3 osdr_query.py data OSD-515 <exact file name> [column.X=...] [options]
  python3 osdr_query.py dataset OSD-104 [OSD-105 ...]    # fast per-accession enrichment

ENDPOINTS  datasets | assays | samples | metadata | data | url | files | contrasts | dataset

SHORTCUTS (expanded to canonical field paths; values are wrapped in /regex/
unless they already start with '/' or you pass --exact)
  organism=   -> study.characteristics.organism
  tissue=     -> study.characteristics.material type
  tech=       -> investigation.study assays.study assay technology type
  measure=    -> investigation.study assays.study assay measurement type
  project=    -> investigation.study.comment.Project Identifier   (mission / ground study)
  factor.X=   -> study.factor value.X          e.g. factor.spaceflight=space flight
  char.X=     -> study.characteristics.X       e.g. char.sex=female
  sex= strain= age= genotype=  -> study.characteristics.<name>
  accession=  -> id.accession (exact)
  file=       -> file.filename
  title=      -> investigation.study.study title
  Any other  name=value  is passed through as a raw field path.
  A bare name (no '=') adds that column without filtering, e.g.  tissue  or  study.factor%20value

OPTIONS
  --format F      json.records (default) | csv | tsv
  --exact         do not wrap values in /…/
  --limit N       rows to print (default 10)
  --out PATH      save the raw response to PATH
  --url-only      print the URL and exit (no network)
  --fallback      if 0 rows and a char.X / sex / strain / age / genotype filter was used,
                  automatically retry with the factor-value field (and vice versa)
  --retries N     attempts on HTTP 504/5xx or a non-JSON body (default 3; identical URL)
  --wait S        seconds between retries (default 12)
  --timeout S     per-request timeout in seconds (default 200)

EXAMPLES
  python3 osdr_query.py assays organism=musculus tech=rna-seq
  python3 osdr_query.py samples organism=musculus tissue=liver sex=female --fallback
  python3 osdr_query.py assays project='RR-1([^\\d]|$)' tech tissue
  python3 osdr_query.py files OSD-515 differential
  python3 osdr_query.py contrasts OSD-515
  python3 osdr_query.py data OSD-515 GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv \\
        'column.SYMBOL' 'column.Adj.p.value_(Space Flight)v(Ground Control)<=0.05' --format csv --out de.csv
"""
import sys, json, re, urllib.parse, urllib.request, urllib.error

BASE = "https://visualization.osdr.nasa.gov/biodata/api"
# Broad queries can hit the gateway's ~60 s limit and return 504; a retry of the
# identical URL usually succeeds (server-side caching of the first computation).
TIMEOUT = 200      # per request; large data-file pulls can stream for a while
RETRIES = 3        # total attempts on 504/5xx or non-JSON body
WAIT = 12          # seconds between attempts

SHORTCUTS = {
    "organism": "study.characteristics.organism",
    "tissue": "study.characteristics.material type",
    "tech": "investigation.study assays.study assay technology type",
    "measure": "investigation.study assays.study assay measurement type",
    "project": "investigation.study.comment.Project Identifier",
    "mission": "investigation.study.comment.Project Identifier",
    "sex": "study.characteristics.sex",
    "strain": "study.characteristics.strain",
    "age": "study.characteristics.age",
    "genotype": "study.characteristics.genotype",
    "accession": "id.accession",
    "file": "file.filename",
    "title": "investigation.study.study title",
}
EXACT_FIELDS = {"id.accession", "id", "id.assay name", "format"}


def enc(s):
    """URL-encode a field name or value, keeping the regex-safe characters readable."""
    return urllib.parse.quote(s, safe="/|()[]^$.*+?\\=<>!,:-_")


def expand(name):
    if name.startswith("factor."):
        return "study.factor value." + name[7:]
    if name.startswith("char."):
        return "study.characteristics." + name[5:]
    return SHORTCUTS.get(name, name)


def build(endpoint, args, fmt, exact):
    parts = []
    for a in args:
        if "=" in a and not a.startswith("column."):
            k, v = a.split("=", 1)
            k = expand(k)
            if v and not exact and k not in EXACT_FIELDS and not v.startswith("/"):
                v = "/" + v + "/"
            parts.append(enc(k) + "=" + enc(v))
        elif a.startswith("column."):
            # column.<name><op><value>  — encode operators
            m = re.match(r"^(column\.[^<>!=]+)(<=|>=|!=|<|>|=)(.*)$", a)
            if m and m.group(2):
                parts.append(enc(m.group(1)) + urllib.parse.quote(m.group(2)) + enc(m.group(3)))
            else:
                parts.append(enc(a))
        else:
            parts.append(enc(expand(a)))
    if not any(p.startswith("format=") for p in parts):
        parts.append("format=" + fmt)
    return f"{BASE}/v2/query/{endpoint}/?" + "&".join(parts)


def fetch(url, out=None):
    """GET with retries. 504/5xx or an HTML body -> retry the identical URL."""
    import time
    code, body = 0, b""
    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
                body = r.read()
                code = r.status
        except urllib.error.HTTPError as e:
            body = e.read()
            code = e.code
        except Exception as e:  # network / DNS / proxy / timeout
            code, body = 0, str(e).encode()
        looks_html = body.lstrip()[:1] == b"<"
        if code == 200 and not looks_html:
            break
        if code and code < 500 and not looks_html:
            break                       # 400/404/422: fix the URL, don't retry
        if attempt < RETRIES:
            print(f"attempt {attempt}: HTTP {code or 'no response'} (server timeout / gateway); "
                  f"retrying the same URL in {WAIT}s ...", file=sys.stderr)
            time.sleep(WAIT)
    if code == 0:
        print(f"ERROR: could not reach OSDR ({body.decode(errors='replace')[:200]}).\n"
              "If this is a DNS/allowlist error the URL is probably fine; allow outbound HTTPS to "
              "visualization.osdr.nasa.gov (see references/network-setup.md).")
        print("URL:", url)
        sys.exit(2)
    if out:
        open(out, "wb").write(body)
    return code, body


def summarise(url, code, body, fmt, limit):
    print("URL:", url)
    print("HTTP:", code, f"({len(body):,} bytes)")
    txt = body.decode("utf-8", "replace")
    if code != 200:
        msg = txt[:300]
        if code == 422:
            msg += "\nHINT: the file filter matched more than one file; use the exact file name (run: files OSD-###)."
        elif code == 500 and "column." in url:
            msg += "\nHINT: a column. name does not exist in this file; run: contrasts OSD-### or read the CSV header."
        elif code == 400:
            msg += "\nHINT: unencoded character (& # space) in a field name; & must be %26."
        elif code in (502, 503, 504):
            msg += ("\nHINT: gateway timeout on a broad query, not a URL error. Retry later, or narrow "
                    "(add id.accession / a technology filter, drop bare columns) and enrich per accession "
                    "with: dataset OSD-###.")
        print("ERROR:", msg)
        return 1
    if fmt == "json.records":
        try:
            rows = json.loads(txt)
        except Exception:
            print(txt[:500]); return 0
        if not isinstance(rows, list):
            print(json.dumps(rows, indent=1)[:2000]); return 0
        print("ROWS:", len(rows))
        if not rows:
            print("No rows. Fallbacks: use /regex/ values; swap study.characteristics.X <-> study.factor value.X; "
                  "discover fields with bare prefixes (study.characteristics, study.factor value).")
            return 0
        cols = list(rows[0].keys())
        short = [re.sub(r"^OSD-\d+/[^/]+/", "", c) for c in cols]
        print("COLUMNS:", ", ".join(short))
        if "id.accession" in cols:
            accs = sorted({r["id.accession"] for r in rows}, key=lambda a: int(a.split("-")[1]) if a.split("-")[1].isdigit() else 0)
            print(f"DATASETS ({len(accs)}):", ", ".join(accs[:60]) + (" …" if len(accs) > 60 else ""))
        print(f"FIRST {min(limit, len(rows))} ROWS:")
        for r in rows[:limit]:
            print("  " + json.dumps({s: v for s, v in zip(short, r.values())}, ensure_ascii=False)[:400])
    else:
        lines = txt.splitlines()
        print("ROWS:", max(len(lines) - 1, 0))
        for l in lines[:limit + 1]:
            print("  " + l[:400])
    return 0


# Attributes that OSDR curates as a characteristic in some studies and as a
# factor value in others. Only these are swapped by --fallback.
EITHER = ["sex", "strain", "age", "genotype", "treatment", "dose", "tissue",
          "organism%20part", "material%20type", "cell%20line", "diet", "duration", "time"]


def swap_char_factor(url):
    alt = url
    for f in EITHER:
        alt = alt.replace(f"study.characteristics.{f}=", f"study.factor%20value.{f}=") \
                 .replace(f"study.factor%20value.{f}=", f"study.characteristics.{f}=") \
            if f"study.characteristics.{f}=" in alt or f"study.factor%20value.{f}=" in alt else alt
    return alt if alt != url else None


# Keys inside /v2/dataset/OSD-###/ -> ["OSD-###"]["metadata"]. "mission" is a dict
# {name, start date, end date}; the DOI is NOT in this tree (use the query
# endpoint with investigation.study.comment.doi).
ENRICH_KEYS = ["study title", "organism", "material type", "project identifier",
               "project type", "mission", "study assay technology type",
               "study assay measurement type", "study factor name"]


def _find_key(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            r = _find_key(v, key)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = _find_key(v, key)
            if r is not None:
                return r
    return None


def enrich_datasets(accs):
    """Fast per-accession summary from /v2/dataset/OSD-###/ (never times out)."""
    from concurrent.futures import ThreadPoolExecutor

    def one(acc):
        code, body = fetch(f"{BASE}/v2/dataset/{acc}/")
        if code != 200:
            return {"accession": acc, "error": f"HTTP {code}"}
        tree = json.loads(body)
        row = {"accession": acc}
        for k in ENRICH_KEYS:
            v = _find_key(tree, k)
            if k == "mission" and isinstance(v, dict):
                v = v.get("name")
            row["mission name" if k == "mission" else k] = ", ".join(map(str, v)) if isinstance(v, list) else v
        return row

    with ThreadPoolExecutor(6) as ex:
        rows = list(ex.map(one, accs))
    print("ROWS:", len(rows))
    for r in rows:
        print("  " + json.dumps(r, ensure_ascii=False)[:600])
    return 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); return 0
    global RETRIES, WAIT, TIMEOUT
    fmt, exact, limit, out, url_only, fallback = "json.records", False, 10, None, False, False
    args = []
    it = iter(argv)
    for a in it:
        if a == "--retries": RETRIES = int(next(it))
        elif a == "--wait": WAIT = float(next(it))
        elif a == "--timeout": TIMEOUT = float(next(it))
        elif a == "--format": fmt = next(it)
        elif a == "--exact": exact = True
        elif a == "--limit": limit = int(next(it))
        elif a == "--out": out = next(it)
        elif a == "--url-only": url_only = True
        elif a == "--fallback": fallback = True
        else: args.append(a)
    ep, rest = args[0], args[1:]

    if ep == "dataset":
        return enrich_datasets(rest)
    if ep == "url":
        url = rest[0]
        if not url.startswith("http"):
            url = BASE + ("/" if not url.startswith("/") else "") + url
        fmt = "json.records" if "json.records" in url else ("csv" if "format=csv" in url or "format=" not in url else fmt)
    elif ep == "files":
        acc = rest[0]; pat = rest[1] if len(rest) > 1 else "."
        url = build("assays", [f"id.accession={acc}", f"file.filename=/{pat}/", "file.subcategory", "file.data type", "file.remote_url"], "json.records", True)
    elif ep == "contrasts":
        # default to the bulk RNA-seq contrasts file; a bare /contrasts_GL/ gives 422 when a
        # study also has methylation/microarray contrasts. Pass a token or exact name as 2nd arg.
        acc = rest[0]
        tok = rest[1] if len(rest) > 1 else "contrasts_GLbulkRNAseq"
        fname = tok if "." in tok else f"/{tok}/"
        url = f"{BASE}/v2/query/data/?id={acc}&file.filename={enc(fname)}&format=json.records"
    elif ep == "data":
        acc, fname = rest[0], rest[1]
        cols = rest[2:] or ["column.*"]
        url = build("data", [f"id={acc}", f"file.filename={fname}"] + cols, fmt, True)
        # file name is exact (regex only if the user wrapped it in slashes)
    else:
        if ep not in ("datasets", "assays", "samples", "metadata"):
            print("Unknown endpoint:", ep); print(__doc__); return 1
        url = build(ep, rest, fmt, exact)

    if url_only:
        print(url); return 0
    code, body = fetch(url, out)
    rc = summarise(url, code, body, fmt, limit)
    if fallback and code == 200 and fmt == "json.records" and body.strip() in (b"[]", b""):
        alt = swap_char_factor(url)
        if alt:
            print("\n--- 0 rows: retrying with characteristic<->factor swapped ---")
            code, body = fetch(alt, out)
            rc = summarise(alt, code, body, fmt, limit)
    if out:
        print("Saved raw response to", out)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
