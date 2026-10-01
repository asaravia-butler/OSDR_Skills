# Installing `osdr-biodata-api` in VS Code / GitHub Copilot

Covers **VS Code (desktop app)** with Copilot Chat, **github.com** (Copilot
coding agent / cloud agent in the browser) and the **Copilot CLI**. Download
`osdr-biodata-api.zip` from this branch first.

Copilot loads skills from a folder inside a repository (`.github/skills/`)
or from your personal skills folder (`~/.copilot/skills/`). No upload dialog
is involved.

---

## 1. VS Code desktop app (no terminal needed)

1. Unzip `osdr-biodata-api.zip`.
2. In VS Code, **File → Open Folder…** and open the project you want the
   skill in.
3. In the **Explorer** pane, create the folders `.github` and, inside it,
   `skills` (right-click → **New Folder…**) if they do not exist.
4. Drag the unzipped `osdr-biodata-api` folder from Finder / File Explorer
   into `.github/skills/` in the Explorer pane, so the file
   `.github/skills/osdr-biodata-api/SKILL.md` exists.
   *Personal, all-projects alternative:* put the folder in
   `~/.copilot/skills/osdr-biodata-api/` instead (Finder **⌘⇧G** →
   `~/.copilot/skills`; Windows address bar → `%USERPROFILE%\.copilot\skills`).
5. Open **Copilot Chat** (side bar) and set the mode picker to **Agent**.
6. Type **/skills** to open **Configure Skills** and check that
   **osdr-biodata-api** is listed and ticked. (Same list under the chat
   **gear → Configure Chat → Skills**.) If the list is empty, make sure the
   setting `chat.useAgentSkills` is enabled and reload the window.
7. Ask an OSDR question, or type **/osdr-biodata-api** followed by the
   question. Copilot runs `curl -g …` or `python3 scripts/osdr_query.py …` in
   the integrated terminal; click **Allow** (or *Always allow* for this
   session) when asked.

Commit `.github/skills/osdr-biodata-api/` so everyone who clones the repo
gets the skill.

---

## 2. github.com in the browser (Copilot coding agent / cloud agent)

Copilot on github.com only sees skills that live **inside the repository**.

1. Open your repository on github.com.
2. Click **Add file → Upload files**.
3. Drag the unzipped `osdr-biodata-api` **folder** into the drop zone (the
   browser keeps its sub-folders). Before committing, make sure the path shown
   is `.github/skills/osdr-biodata-api/…` — if you are not already inside
   `.github/skills`, navigate there first (create the folders by using
   **Add file → Create new file** with the name
   `.github/skills/osdr-biodata-api/SKILL.md` and pasting the file's content,
   then upload the rest).
4. Commit to the default branch (or open a pull request and merge it).
5. Open **Copilot** on the repo (the Copilot icon, or assign an issue to
   Copilot) and ask your OSDR question. The agent reads `.github/skills/`
   automatically and runs the `curl` calls in its cloud sandbox.

**Firewall:** the Copilot coding agent's sandbox allows only listed hosts by
default. In the repository's **Settings → Copilot → Coding agent → Custom
allowlist**, add `visualization.osdr.nasa.gov` and `osdr.nasa.gov`.

---

## 3. Copilot CLI

Place the folder in `~/.copilot/skills/osdr-biodata-api/` (or in the repo's
`.github/skills/`). `copilot` then lists it under `/skills` and loads it when
a prompt matches.

The folder name **must stay `osdr-biodata-api`** — VS Code validates that it
equals the `name:` field in `SKILL.md`.

---

## 4. Check it works

In a fresh Agent-mode chat:

| Ask | Expect |
|---|---|
| *List all Drosophila datasets in OSDR with their titles.* | 17 datasets from a `/datasets/` URL with `organism=/drosophila/` |
| *Which OSDR datasets come from the RR-1 mission, and what assays and tissues do they include?* | 25 datasets (80 dataset × assay × tissue rows), including the `RR-1_BSP` alias |
| *I need physical tissue samples from the RR-9 mice — how do I get them from OSDR?* | No biodata query; a redirect to NBISC (NASA Biological Institutional Scientific Collection) |

More cases: [`testing.md`](testing.md) and
[`../examples/vscode-copilot.md`](../examples/vscode-copilot.md).
