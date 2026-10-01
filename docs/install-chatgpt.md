# Installing `osdr-biodata-api` in ChatGPT and Codex

Covers the **ChatGPT web app**, the **ChatGPT desktop app**, the **Codex
desktop app / IDE extension** and the **Codex CLI**. Download
`osdr-biodata-api.zip` from this branch first.

> **Plan note.** The *Skills* tab inside ChatGPT is offered to **Business,
> Enterprise, Healthcare and Edu** workspaces (a workspace admin must have
> *Enable skills* and *Enable skill uploading* switched on). Free, Plus and Pro
> accounts do not see it; use **Codex** (section 2), which reads the same
> package from a folder on your computer.

---

## 1. ChatGPT web app (chatgpt.com) and ChatGPT desktop app

Same interface in both.

1. In the left sidebar open **Plugins → Plugin Directory**, then the
   **Skills** tab.
2. Click **Create → Upload from your computer** and choose
   `osdr-biodata-api.zip`.
3. ChatGPT scans the upload. When the status shows **Available** (not *Needs
   review* or *Blocked*) it is ready. If it is blocked, ask your workspace
   admin to approve it in **Workspace settings → Skills**.
4. Make sure **Browsing / web search** is enabled for your chats — ChatGPT
   uses it to fetch the OSDR API URLs.
5. In a new chat either type **@** and pick **osdr-biodata-api**, or simply
   ask an OSDR question; the skill is loaded silently when the question
   matches its description. (ChatGPT does not always show a skill indicator —
   ask *"which skill did you use?"* if unsure.)

**Share with colleagues:** open the skill's **•••** menu → **Share** (people,
groups, or a link).
**Update:** upload the new zip through the same **Create → Upload** flow; the
newer version replaces the older one.
**Remove:** **••• → Delete**.

**Network:** ChatGPT's browsing tool fetches public URLs directly. If a call
returns "unable to fetch", retry once (the server can return HTTP 504 on very
broad queries) before assuming a block.

---

## 2. Codex app (desktop), Codex in your IDE, and Codex CLI

Codex loads skills from folders on your machine; no upload is needed.

1. Unzip `osdr-biodata-api.zip`.
2. Move the `osdr-biodata-api` folder to one of:
   - `~/.agents/skills/osdr-biodata-api/` — personal, all projects
     (macOS Finder: **⌘⇧G**, type `~/.agents/skills`; Windows File Explorer
     address bar: `%USERPROFILE%\.agents\skills`; create the folders if they do
     not exist);
   - `<project>/.agents/skills/osdr-biodata-api/` — one repository.
3. Restart Codex (or open a new thread). Type **/skills** to see the list,
   or **$osdr-biodata-api** in the prompt to force it; otherwise it triggers
   on matching questions.
4. When Codex asks permission to run `curl -g …` or
   `python3 scripts/osdr_query.py …`, **approve** it. Codex's sandbox has
   network access **off** by default; if calls fail, turn on network access
   for the thread/workspace (Settings → Sandbox / approvals) or add
   `visualization.osdr.nasa.gov` to the allowed hosts.

The folder name **must stay `osdr-biodata-api`** (it must match the `name:`
field in `SKILL.md`).

---

## 3. Check it works

In a fresh chat or thread:

| Ask | Expect |
|---|---|
| *List all Drosophila datasets in OSDR with their titles.* | 17 datasets from a `/datasets/` URL with `organism=/drosophila/` |
| *Which Inspiration4 datasets contain GeneLab-processed data files?* | OSD-572, OSD-573, OSD-574, OSD-630 (metagenomics) |
| *List all human astronaut datasets in OSDR.* | No biodata query; a redirect to NLSP / LSDA / LSAH |

More cases: [`testing.md`](testing.md) and
[`../examples/chatgpt.md`](../examples/chatgpt.md).
