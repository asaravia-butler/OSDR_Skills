# Installing `osdr-biodata-api` in Gemini

Covers the **Gemini web app** (gemini.google.com), the **Gemini desktop app**
and the **Gemini CLI**. Two downloads exist on this branch:

- `osdr-biodata-api-flat.zip` — `SKILL.md` at the root of the zip. **Use this
  for the Gemini web / desktop app**, whose uploader requires it.
- `osdr-biodata-api.zip` — the `osdr-biodata-api/` folder as zip root. Use
  this for the Gemini CLI.

> **Plan note.** Skills in the Gemini app live in **Gemini Spark** and require
> a personal Google account (18+) with **Google AI Pro or Ultra**. At the time
> of writing they are not available in the EEA, UK, Switzerland or Nigeria, or
> on Workspace accounts. The Gemini CLI has no such restriction.

---

## 1. Gemini web app and Gemini desktop app

Same interface in both.

1. Go to gemini.google.com (or open the desktop app), click **Switch to
   Spark**, then open **Skills** in the left panel.
2. Click **Upload** and choose **`osdr-biodata-api-flat.zip`**.
3. Gemini reads the name and description from `SKILL.md`. Review them and
   click **Create**.
4. The skill is enabled by default. In a Spark task, type **/** and pick
   **osdr-biodata-api**, or just ask an OSDR question and let it trigger.
5. Gemini fetches the API URLs with its own browsing tool. Spark does **not**
   run scripts that need internet access, so `scripts/osdr_query.py` is
   ignored there — that is expected; every recipe in the skill also works as
   plain URLs.

**Manage:** on the Skills page click the skill → **More** → **Disable / Edit /
Download / Delete**.
**Update:** delete the old skill and upload the new flat zip (or use **Edit**
to replace files).

---

## 2. Gemini CLI

1. Unzip `osdr-biodata-api.zip`.
2. Move the `osdr-biodata-api` folder to one of:
   - `~/.gemini/skills/osdr-biodata-api/` — personal, all projects;
   - `<project>/.gemini/skills/osdr-biodata-api/` — one project;
   - `~/.agents/skills/osdr-biodata-api/` — also read by Gemini CLI, so a
     single copy can serve Codex and Gemini.
   (macOS Finder: **⌘⇧G** and type the path; Windows File Explorer: type
   `%USERPROFILE%\.gemini\skills` in the address bar.)
3. Start `gemini`. `/skills list` shows the skill. When a prompt matches,
   Gemini asks you to **approve activating** the skill, then runs
   `curl -g …` or the Python helper through its shell tool — approve those
   too, or allow them for the session.
4. If the shell tool is sandboxed without network, enable network or run
   with the sandbox off for this project.

The folder name **must stay `osdr-biodata-api`** (it must match the `name:`
field in `SKILL.md`).

---

## 3. Check it works

In a fresh task / session:

| Ask | Expect |
|---|---|
| *List all Drosophila datasets in OSDR with their titles.* | 17 datasets from a `/datasets/` URL with `organism=/drosophila/` |
| *Which Rodent Research datasets used only female mice?* | ~89 datasets: two queries (RR datasets, then those with any male samples) and a set difference, or one per-dataset sex breakdown |
| *Show me the temperature and CO₂ readings on ISS during RR-1.* | No biodata query; a redirect to the OSDR Environmental Data Application (EDA) |

More cases: [`testing.md`](testing.md) and
[`../examples/gemini.md`](../examples/gemini.md).
