# OSDR_Skills

Agent **skills packages** for NASA's [Open Science Data Repository (OSDR)](https://science.nasa.gov/biological-physical/data/osdr/).

A skills package is a small folder (a `SKILL.md` instruction file plus optional
reference files and scripts) that teaches an AI assistant how to use an OSDR
resource correctly. For OSDR API skills, this includes which API endpoints exist, how to build a valid call,
which metadata fields and values to filter on, and how to report the result.
The packages follow the open [Agent Skills](https://agentskills.io/specification)
format, so each OSDR Skills package works in Claude, ChatGPT/Codex,
Gemini and VS Code / GitHub Copilot. Once a package is installed, users ask
questions in natural language and the assistant translates them into the
correct OSDR API calls.

## Skills in this repository

Each OSDR skill package lives on its own branch. The branch holds the installable zip,
the unpacked package for browsing, installation guides for each client, and example prompts.

| Skill | Branch | OSDR resource | Status |
|---|---|---|---|
| **OSDR BioData API** — find and pull biological datasets, assays, samples and GeneLab-processed data tables (e.g. RNA-seq, microarray, methylation, amplicon, …) | [`OSDR_BioData_API`](../../tree/OSDR_BioData_API) | [Biological Data API](https://visualization.osdr.nasa.gov/biodata/api/) | v1.0.0 |
| **OSDR EDA API** — environmental telemetry (temperature, humidity, CO₂, radiation environment) for flight missions | `OSDR_EDA_API` | [Environmental Data Application](https://visualization.osdr.nasa.gov/eda/) | planned |
| **OSDR RadLab API** — radiation dosimetry | `OSDR_RadLab_API` | [RadLab](https://visualization.osdr.nasa.gov/radlab/gui/data-api/) | planned |

## How to use a skill

1. Open the skill's branch and download `<skill-name>.zip` (or the `-flat.zip`
   variant where instructed to do so).
2. Follow the installation guide for your client in that branch's `docs/`
   folder: Claude, ChatGPT/Codex, Gemini, or VS Code / GitHub Copilot — each
   guide covers the browser and desktop apps as well as the command line.
3. Start a new chat and ask a question; the `examples/` folder on each branch
   shows typical prompts and the answers you should expect.

## Contributing

Test reports (prompt, client, model, answer, what was wrong) are the most
useful contribution. Open an issue on the relevant branch with the prompt you
used and the response you got; the eval set in each branch's `docs/` folder
is the regression suite that changes are checked against.

## Data citation

Every answer produced with these skills should cite the OSDR study DOI(s) and
state the dataset version. OSDR data are in the public domain; the
skill text in this repository is released under CC0.
