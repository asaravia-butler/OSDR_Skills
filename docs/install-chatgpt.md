# Installing `osdr-biodata-api` in ChatGPT and Codex

Covers the **ChatGPT web app**, the **ChatGPT desktop app**, and **Codex**
(app, IDE extension, CLI). Download
[`osdr-biodata-api.zip`](../osdr-biodata-api.zip) first.

Official documentation (check it for the latest steps):
[Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) ·
[Build skills (ChatGPT and Codex)](https://learn.chatgpt.com/docs/build-skills).

> **Plan note.** Skills are available on all paid ChatGPT plans (Plus, Pro,
> Business, Enterprise, Healthcare and Edu); on Business / Enterprise / Edu
> workspaces an admin must have enabled skills and skill uploading. The Free
> plan cannot add skills — use **Codex** (section 2) or a paid plan.

---

## 1. ChatGPT web app (chatgpt.com) and ChatGPT desktop app

Same interface in both.

1. Unzip `osdr-biodata-api.zip` so you have the `osdr-biodata-api` folder.
2. In the sidebar open **Skills** (on some workspaces it is under
   **Plugins → Skills** tab).
3. Click **Add → Upload from your computer** and selec (or drag and drop)t the
   `osdr-biodata-api` folder (`SKILL.md` must be at the top level of what you
   upload; the zip itself is accepted where the uploader allows archives).
4. ChatGPT scans the upload. When it no longer shows **Needs review** or
   **Blocked** it is ready; if it is blocked on a workspace plan, ask your
   admin.
5. In a new chat type **@** and pick **osdr-biodata-api**, or just ask an
   OSDR question — the skill loads automatically when the question matches
   its description. ChatGPT fetches the API URLs with its browsing tool, so
   browsing must be enabled.

**Share with colleagues:** on the skill's **•••** menu choose **Share**
(people, groups or link); recipients install it from *Shared with me*.

---

## 2. Codex (desktop app, IDE extension, CLI)

Codex loads skills from folders on your machine; no upload is needed.

1. Unzip `osdr-biodata-api.zip`.
2. Move the `osdr-biodata-api` folder to one of
   - `~/.agents/skills/osdr-biodata-api/` — personal, all projects (Finder:
     **⌘⇧G** → `~/.agents/skills`; Windows: `%USERPROFILE%\.agents\skills`
     in the File Explorer address bar; create the folders if needed);
   - `<repo>/.agents/skills/osdr-biodata-api/` — one repository.
3. Start Codex (or open a new thread). `/skills` lists it; type
   **$osdr-biodata-api** in the prompt to force it, otherwise it triggers on
   matching questions.
4. Approve the `curl -g …` or `python3 scripts/osdr_query.py …` commands when
   asked. If calls fail, turn on network access for the thread/workspace
   (Codex's sandbox has network off by default).

The folder name **must stay `osdr-biodata-api`** (it must match the `name`
field in `SKILL.md`).

---

## 3. Check it works

In a fresh chat or thread:

| Ask | Expect |
|---|---|
| *List all Drosophila datasets in OSDR with their titles.* | 17 datasets from a `/datasets/` URL with `organism=/drosophila/` |
| *Which Inspiration4 datasets contain GeneLab-processed data files?* | OSD-572, OSD-573, OSD-574, OSD-630 (metagenomics) |
| *List all human astronaut datasets in OSDR.* | No biodata query; a redirect to NLSP / LSDA / LSAH |

**GeneLab Knowledge Graph (optional).** If the `mcp-genelab` MCP server is
connected in this client, the skill uses it first for known-study questions
and labels every answer part as KG or API; nothing in the skill needs
configuring. To connect the server, follow the ChatGPT instructions in the
mcp-genelab repository:
<https://github.com/sbl-sdsc/mcp-genelab/tree/main#chatgpt>.

More cases: [`testing.md`](testing.md) and
[`../examples/chatgpt.md`](../examples/chatgpt.md).
