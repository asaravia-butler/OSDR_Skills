# Installing `osdr-biodata-api` in Gemini

Covers the **Gemini web app** (gemini.google.com), the **Gemini app on Mac**
and the **Gemini CLI**. Two downloads exist on this branch:

- [`osdr-biodata-api-flat.zip`](../osdr-biodata-api-flat.zip) — `SKILL.md`
  at the root of the zip. **Use this for the Gemini web / Mac app**, whose
  uploader requires it.
- [`osdr-biodata-api.zip`](../osdr-biodata-api.zip) — the `osdr-biodata-api/`
  folder as zip root. Use this for the Gemini CLI.

Official documentation (check it for the latest steps):
[Create & manage skills for Gemini Apps](https://support.google.com/gemini/answer/17094296) ·
[About the transition from Gems to skills](https://support.google.com/gemini/answer/18560919) ·
[Gemini CLI: Agent Skills](https://geminicli.com/docs/cli/skills/).

> **Eligibility.** Skills in the Gemini app are available to individuals aged
> 18 or over signed in to a **personal Google Account**, without a Google AI
> subscription.

---

## 1. Gemini web app and Gemini app on Mac

Same interface in both.

1. Go to gemini.google.com (or open the Mac app). In the sidebar click
   **Customize** (click **More** first if you don't see it), then at the top
   click **Skills**.
2. Click **Create → Upload** and select (or drag and drop) **`osdr-biodata-api-flat.zip`**
   (Google requires `SKILL.md` in the root of the upload; total size limit
   100 MB). Click **Open**, then **Upload**.
3. Review the name and description Gemini reads from `SKILL.md` and click
   **Create**.
4. The skill is active by default. In a chat type **/** (or **@** with the
   updated shortcut) and pick **osdr-biodata-api**, or just ask an OSDR
   question — Gemini uses active skills automatically.
5. Gemini fetches the API URLs with its browsing tool. The app does **not**
   run scripts that need internet access, so `scripts/osdr_query.py` is
   ignored there — expected; every recipe in the skill also works as plain
   URLs.

**Manage:** click the skill → **More** → **Deactivate / Activate**, **Edit
with Gemini** or **Replace skill** (re-upload the whole package to change its
files).

---

## 2. Gemini CLI

1. Unzip `osdr-biodata-api.zip`.
2. Move the `osdr-biodata-api` folder to **one** of
   - `~/.gemini/skills/osdr-biodata-api/` — personal, all projects;
   - `~/.agents/skills/osdr-biodata-api/` — personal, also read by Codex (if
     both exist, `.agents` wins and the CLI reports a conflict);
   - `<project>/.gemini/skills/osdr-biodata-api/` — one project (also
     `.agents/skills/`).
3. Check with `gemini skills list --all` (from a terminal) or `/skills list`
   inside a session.
4. Ask an OSDR question. Gemini asks you to approve activating the skill the
   first time, then runs `curl -g …` or the Python helper through its shell
   tool — approve those too. If you run with the sandbox on and a call is
   denied network access, approve the *Sandbox Expansion Request* or use a
   profile that allows network; the hosts the skill needs are
   `visualization.osdr.nasa.gov`, `osdr.nasa.gov` and
`nasa-osdr.s3-website-us-west-2.amazonaws.com`.

The folder name **must stay `osdr-biodata-api`** (it must match the `name`
field in `SKILL.md`). Note: Google's docs state that for unpaid-tier and
Google One users Gemini CLI was replaced by **Antigravity CLI** in June 2026;
the same skill folders apply there.

---

## 3. Check it works

In a fresh chat / session:

| Ask | Expect |
|---|---|
| *List all Drosophila datasets in OSDR with their titles.* | 17 datasets from a `/datasets/` URL with `organism=/drosophila/` |
| *Which Rodent Research datasets used only female mice?* | ~89 datasets: two queries (RR datasets, then those with any male samples) and a set difference, or one per-dataset sex breakdown |
| *Show me the temperature and CO₂ readings on ISS during RR-1.* | No biodata query; a redirect to the OSDR Environmental Data Application (EDA) |

**GeneLab Knowledge Graph (optional).** If the `mcp-genelab` MCP server is
connected in this client, the skill uses it first for known-study questions
and labels every answer part as KG or API; nothing in the skill needs
configuring. To connect the server, follow the Gemini instructions in the
mcp-genelab repository:
<https://github.com/sbl-sdsc/mcp-genelab/tree/main#gemini>.

More cases: [`testing.md`](testing.md) and
[`../examples/gemini.md`](../examples/gemini.md).
