# Scope, identifiers, versions, citations

## Identifier model

- `OSD-###` — the study / dataset accession. Query with this.
- `GLDS-###` — the omics data id inside a study (legacy "GeneLab" name). Same
  number as the OSD id for older studies; file names still start with it.
- `LSDS-###` — non-omics (physiological, imaging, phenotypic) data id inside a
  study. A study can have GLDS and/or LSDS ids.
- Treat `OSD-###` as canonical; recognise `GLDS-###` as its omics alias. One
  OSD accession can hold both GLDS- and LSDS-prefixed files (OSD-569 has
  GLDS-561 omics files and LSDS-7 clinical panels).

## Version and citation

- **Citation / DOI**: in the API — `investigation.study.comment.doi`
  (populated for 597 of 636 studies). Query:
  `BASE/v2/query/datasets/?id.accession=OSD-###&investigation.study.comment.doi&investigation.study.study%20title&format=json.records`
  Fallback: the study landing page `https://osdr.nasa.gov/bio/repo/data/studies/OSD-###`.
- **Version**: not in the API. Highest `version-N` folder under
  `s3://nasa-osdr/OSD-###/`: `aws s3 ls --no-sign-request s3://nasa-osdr/OSD-###/`
  or `https://nasa-osdr.s3.amazonaws.com/?list-type=2&prefix=OSD-###/&delimiter=/`.

Report both with any answer that returns OSDR data or metadata.

## Other study-level comment fields (bare `investigation.study.comment` lists all)

`project type` (Spaceflight Study 341 · Ground Study 264 · High Altitude Study ·
Parabolic Study · Suborbital Flight Study), `project identifier`, `mission name`
(SpaceX-4, SpaceX-16 …; 318 populated), `mission start` / `mission end`
(MM/DD/YYYY), `flight program` (ISS, STS, …), `space program` (NASA 347, JAXA 23,
ESA 19, DLR 5), `experiment platform` (Rodent Habitat 91, AEM 14 …),
`managing nasa center`, `funding`, `study grant number`, `data source accession`
(GEO/PRIDE ids), `date of experiment`.

## Raw files and bulk download

- Per-file: `file.remote_url` (relative → prefix `https://osdr.nasa.gov`) or
  `BASE/v2/dataset/OSD-###/files/` (absolute `URL` field).
- Bulk: `aws s3 cp --no-sign-request s3://nasa-osdr/OSD-###/ . --recursive`
  (layout `OSD-###/version-N/<data-type>/`).

## Out-of-scope reply templates (use verbatim as the FIRST sentence)

- Astronaut data: "OSDR does not host NASA human astronaut data. For astronaut
  data use the NASA Life Sciences Portal (NLSP) https://www.nasa.gov/hrp/nlsp/ —
  the Life Sciences Data Archive (LSDA)
  https://nlsp.nasa.gov/explore/mtable/lsda_experiment/lsda_experiment and the
  Lifetime Surveillance of Astronaut Health (LSAH)
  https://nlsp.nasa.gov/explore/lsdahome/lsahhome." Then, optionally: "OSDR does
  hold some human data this API can serve: non-NASA crew studies (Inspiration4),
  human ground-analog studies (bed rest, confinement, limb suspension) and
  in-vitro human cell studies — say if you want those."
- Environmental telemetry: "Environmental telemetry (temperature, humidity,
  CO₂ …) is outside this skill; it is served by the OSDR Environmental Data
  Application (EDA): https://visualization.osdr.nasa.gov/eda/."
- Radiation dosimetry: "Radiation dosimetry is outside this skill; it is served
  by RadLab: https://visualization.osdr.nasa.gov/radlab/gui/overview/."
- Biospecimens: "Physical biospecimen requests are outside this skill; use
  NBISC: https://visualization.osdr.nasa.gov/nbisc/home/ (background:
  https://science.nasa.gov/biological-physical/data/nbisc/)."
- Microbe specimens: "Microbial isolate requests are outside this skill; use
  SMCC: https://visualization.osdr.nasa.gov/smcc/."

Do not probe these services' APIs from this skill; a separate skill sheet
covers EDA and RadLab.

## Not covered by this API → where to send the user

| Request | Go to |
|---|---|
| Full-text / keyword search across studies | OSDR search UI `https://osdr.nasa.gov/bio/repo/search` (crude API substitute: regex on `investigation.study.study%20title`) |
| Environmental telemetry (temperature, CO₂, humidity, radiation environment) | EDA `https://visualization.osdr.nasa.gov/eda/` |
| Radiation dosimetry | RadLab `https://visualization.osdr.nasa.gov/radlab/gui/overview/` |
| Physical biospecimens | NBISC `https://visualization.osdr.nasa.gov/nbisc/home/` |
| Microbial isolates | SMCC `https://visualization.osdr.nasa.gov/smcc/` |
| Human astronaut data | NLSP `https://www.nasa.gov/hrp/nlsp/` — LSDA and LSAH (OSDR does host some human *analog* studies, which this API serves) |
| GEO / PRIDE / SRA federated search | those repositories directly |
| Compute / analysis | OSDR provides no compute; its multi-study visualization portal `https://visualization.genelab.nasa.gov/data/` runs analyses on transcriptomics studies; external compute such as NSF ACCESS `https://access-ci.org/` |

## Current API limitations (state plainly when relevant)

- `/v2/metadata/fields/` is in the OpenAPI spec but returns 404; discover
  fields with bare prefixes instead.
- No count endpoint: count rows client-side.
- No dataset-version field (DOI is available via `investigation.study.comment.doi`).
- `/v2/query/metadata/` and `/v2/query/data/` are live but absent from
  `openapi.json`.
