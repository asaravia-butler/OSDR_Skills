# Installing `osdr-biodata-api` in Claude

Covers **claude.ai in the browser**, the **Claude desktop app**, **Cowork**
and **Claude Code**. Download
[`osdr-biodata-api.zip`](../osdr-biodata-api.zip) first (the `osdr-biodata-api/`
folder is the root of the zip, which is what Claude's uploader expects).

Official documentation (check it for the latest steps):
[Use skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude) ·
[How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) ·
[Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills).

Requires a paid plan (Pro, Max, Ultra, Team or Enterprise); the skill cannot
be used on the Free plan. No API key is needed: Claude fetches the OSDR URLs
itself.

---

## 1. claude.ai (web browser) and Claude desktop app

The two share one interface; the steps are identical.

1. **Settings → Capabilities:** turn on **Create and edit files** (skills need
   this) and **Use the internet while making files**. On Team / Enterprise an
   owner enables skills under **Organization settings → Plugins & skills →
   Policy** and controls internet access under **Organization settings →
   Capabilities**.
2. **Settings → Capabilities → Allowed websites:** add the three OSDR hosts
   the skill uses (Team / Enterprise: an owner adds them in the organization
   settings, or allows all domains):

   | Host | Used for |
   |---|---|
   | `visualization.osdr.nasa.gov` | every BioData API call |
   | `osdr.nasa.gov` | file downloads (`file.remote_url` links) |
   | `nasa-osdr.s3-website-us-west-2.amazonaws.com` | the public OSDR S3 bucket (dataset version folders, bulk file access) |

3. Go to **Customize → Skills** (<https://claude.ai/customize/skills>).
4. Click **+ Add**, then **Upload skill**.
5. Select (or drag and drop) `osdr-biodata-api.zip`. Claude unpacks it and lists
   *osdr-biodata-api* with the description from `SKILL.md`.
6. Make sure the skill's toggle is **on**.
7. Start a **new chat** and ask, for example, *List all Drosophila datasets
   in OSDR with their titles.* Claude shows a "Using osdr-biodata-api"
   indicator, runs the API URL(s) and reports them with the result.

Upload errors come from a folder name that differs from the `name` in
`SKILL.md`, a missing `SKILL.md`, or files placed at the zip root instead of
inside the folder — the branch zip is already laid out correctly.

**If Claude says it cannot reach `visualization.osdr.nasa.gov`:** the hosts in
step 2 are not in **Allowed websites** yet. Claude should hand you the URL to
open yourself rather than rewrite the query.

---

## 2. Cowork

Skills enabled on your claude.ai account appear in Cowork automatically —
nothing extra to install. Cowork can run `scripts/osdr_query.py`, so some
answers come from the script rather than raw `curl`; the URLs are the same.
If a task's network access is restricted to an allow-list, add the same three
hosts as in section 1 step 2 (`visualization.osdr.nasa.gov`, `osdr.nasa.gov`,
`nasa-osdr.s3-website-us-west-2.amazonaws.com`) to the task's allowed
websites.

---

## 3. Claude Code (terminal or IDE extension)

Claude Code is a separate install from the chat app (see
[Set up Claude Code](https://code.claude.com/docs/en/setup)). Skills uploaded
to claude.ai also sync to Claude Code (they appear under
`~/.claude/skills/synced/`; run `/skills` to see them). To install locally
instead:

1. Unzip `osdr-biodata-api.zip`.
2. Move the `osdr-biodata-api` folder to one of
   - `~/.claude/skills/osdr-biodata-api/` — personal, all projects
     (Finder: **⌘⇧G** → `~/.claude/skills`; Windows: type
     `%USERPROFILE%\.claude\skills` in the File Explorer address bar);
   - `<project>/.claude/skills/osdr-biodata-api/` — this project only; commit
     it to share with the team.
3. Start (or restart) Claude Code. `/skills` lists it; invoke with
   `/osdr-biodata-api <question>` or just ask an OSDR question.
4. Approve the `curl` / `python3` calls when prompted, or pre-approve them in
   `.claude/settings.json`: `"permissions": {"allow": ["Bash(curl *)",
   "Bash(python3 *)"]}`.

The folder name **must remain `osdr-biodata-api`** — it has to match the
`name` field in `SKILL.md`. (`synced` and `anthropic-skills` are reserved
folder names.)

---

## 4. Check it works

In a fresh chat:

| Ask | Expect |
|---|---|
| *List all Drosophila datasets in OSDR with their titles.* | 17 datasets, a `/datasets/` URL containing `organism=/drosophila/` |
| *Show me the differentially expressed genes for OSD-515, space flight vs ground control.* | ~3,947 significant genes, top-10 up/down tables with log2FC, adj p, Wald stat and group mean/SD, an offer of a CSV |
| *Show me the temperature and CO₂ readings on ISS during RR-1.* | No biodata query; a short redirect to the OSDR Environmental Data Application (EDA) |

**GeneLab Knowledge Graph (optional).** If the `mcp-genelab` MCP server is
connected in this client, the skill uses it first for known-study questions
and labels every answer part as KG or API; nothing in the skill needs
configuring. To connect the server, follow the Claude instructions in the
mcp-genelab repository:
<https://github.com/sbl-sdsc/mcp-genelab/tree/main#claude-desktop-or-claudeai>.

More cases: [`testing.md`](testing.md) and [`../examples/claude.md`](../examples/claude.md).
