# Installing `osdr-biodata-api` in Claude

Covers **claude.ai in the browser**, the **Claude desktop app**, **Cowork**
and **Claude Code**. Download `osdr-biodata-api.zip` from this branch first.

Skills are available on Free, Pro, Max, Team and Enterprise plans. The skill
needs no API key: Claude fetches the OSDR URLs itself.

---

## 1. claude.ai (web browser) and Claude desktop app

The two share one interface; the steps are identical.

1. **One-time setting.** Open **Settings → Capabilities** and turn on
   **Code execution and file creation**. (Team / Enterprise: an admin enables
   skills under **Organization settings → Skills** first.)
2. Open **Customize → Skills** (left sidebar, or Settings → Customize).
3. Click **+** → **Create skill** → **Upload a skill**.
4. Choose `osdr-biodata-api.zip`. Claude unpacks it and shows
   *osdr-biodata-api* in the list with the description from `SKILL.md`.
5. Make sure the toggle next to the skill is **on**.
6. Start a **new chat** and ask, for example:
   *List all Drosophila datasets in OSDR with their titles.*
   Claude shows a "Using osdr-biodata-api" indicator, fetches the API URL(s),
   and returns the table with the URLs it ran.

**Update:** upload the new zip the same way; it replaces the existing version.
**Remove:** open the skill in Customize → Skills, toggle it off, then
**… → Delete**.

**Enterprise networks:** if Claude reports that it cannot reach
`visualization.osdr.nasa.gov`, an admin may need to allow that host in the
organization's network egress settings.

---

## 2. Cowork (Claude desktop app, agent mode)

Cowork reads skills from the same account-level list as claude.ai, so a skill
uploaded in step 1 is available. Two extra points:

- In the Cowork task settings, under **Allow network egress → Additional
  allowed domains**, add `visualization.osdr.nasa.gov` and `osdr.nasa.gov`
  (only if egress is restricted to an allow-list; unrestricted egress needs
  nothing).
- Cowork can run `scripts/osdr_query.py`, so answers may come from the script
  rather than raw `curl` calls; both produce the same URLs.

Alternatively, install locally: unzip and place the `osdr-biodata-api` folder
in `~/.claude/skills/` (Finder: **⌘⇧G** and type `~/.claude/skills`; Windows:
type `%USERPROFILE%\.claude\skills` in the File Explorer address bar; create
the folders if missing).

---

## 3. Claude Code (terminal or IDE extension)

1. Unzip `osdr-biodata-api.zip`.
2. Move the `osdr-biodata-api` folder to one of:
   - `~/.claude/skills/osdr-biodata-api/` — personal, all projects;
   - `<project>/.claude/skills/osdr-biodata-api/` — this project only
     (commit it so teammates get it).
3. Start (or restart) Claude Code. `/skills` lists it; invoke with
   `/osdr-biodata-api <question>` or just ask an OSDR question.
4. Approve the `curl` / `python3` calls when prompted, or pre-approve them in
   `.claude/settings.json` (`"permissions": {"allow": ["Bash(curl *)",
   "Bash(python3 *)"]}`).

The folder name **must remain `osdr-biodata-api`** — it has to match the
`name:` field in `SKILL.md`.

---

## 4. Check it works

In a fresh chat:

| Ask | Expect |
|---|---|
| *List all Drosophila datasets in OSDR with their titles.* | 17 datasets, a `/datasets/` URL containing `organism=/drosophila/` |
| *Show me the differentially expressed genes for OSD-515, space flight vs ground control.* | ~3,947 significant genes, top-10 up/down tables with log2FC, adj p, Wald stat and group mean/SD, an offer of a CSV |
| *Show me the temperature and CO₂ readings on ISS during RR-1.* | No biodata query; a short redirect to the OSDR Environmental Data Application (EDA) |

More cases: [`testing.md`](testing.md) and [`../examples/claude.md`](../examples/claude.md).
