# Installing `osdr-biodata-api` in VS Code / GitHub Copilot

Covers **VS Code (desktop app)** with Copilot Chat, the **Copilot cloud
agent on github.com** (formerly the coding agent) and the **Copilot CLI**.
Download [`osdr-biodata-api.zip`](../osdr-biodata-api.zip) first.

Official documentation (check it for the latest steps):
[Use Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills) ·
[Adding agent skills for GitHub Copilot (cloud agent)](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills) ·
[Adding agent skills for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) ·
[Customizing or disabling the firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall).

Copilot reads skills from a folder inside the repository (`.github/skills/`,
also `.agents/skills/` or `.claude/skills/`) or from your personal folder
(`~/.copilot/skills/` or `~/.agents/skills/`). No upload dialog is involved,
and no VS Code setting needs changing.

---

## 1. VS Code desktop app (no terminal needed)

1. Unzip `osdr-biodata-api.zip`.
2. In Finder (Mac) or File Explorer (Windows) open your **home folder** and
   create a folder named `.agents`, then inside it a folder named `skills`,
   if they don't already exist. Folders whose names start with a dot are
   hidden by default: on Mac press **⌘⇧.** (Command-Shift-period) in Finder
   to show them, or use **Go → Go to Folder…** (⌘⇧G) and type `~/.agents`;
   on Windows open **View → Show → Hidden items** in File Explorer, or type
   `%USERPROFILE%\.agents` in the address bar.
3. Drag and drop the unzipped `osdr-biodata-api` folder into that `skills`
   folder, so that `~/.agents/skills/osdr-biodata-api/SKILL.md` exists. This
   is a personal install that works in every project (and is also read by
   Codex and the Gemini CLI).
   *Project alternative:* in VS Code, **File → Open Folder…** the project,
   create `.github/skills/` in the **Explorer** pane and drop the folder
   there instead; commit it so everyone who clones the repo gets the skill.
4. Open **Copilot Chat** and set the mode picker to **Agent**.
5. Verify: Command Palette → **Chat: Open Customizations** → **Skills**
   lists *osdr-biodata-api*; or type **/** in the chat box and look for
   `/osdr-biodata-api`.
6. Ask an OSDR question, or type **/osdr-biodata-api** followed by the
   question. Copilot runs `curl -g …` or `python3 scripts/osdr_query.py …` in
   the integrated terminal — click **Allow** when asked.

---

## 2. github.com — Copilot cloud agent

The cloud agent only sees skills that live **inside the repository**.

1. On github.com open the repository, **Add file → Upload files**, and drag
   the unzipped `osdr-biodata-api` folder in so it lands at
   `.github/skills/osdr-biodata-api/` (navigate into `.github/skills` first,
   creating the path with **Add file → Create new file** if needed). Commit
   to the default branch.
2. Allow the API host through the agent's firewall: repository **Settings →
   Copilot → Internet access → Copilot in the cloud → Custom allowlist**, add
   `visualization.osdr.nasa.gov` and `osdr.nasa.gov`, **Add rule → Save
   changes**. (Repository rules require the organization setting *Allow
   repository custom rules*; org owners can instead add them under the
   organization's **Settings → Copilot → Internet access**.)
3. Assign an issue to Copilot or open Copilot on the repo and ask your OSDR
   question; the agent picks the skill from its description.

---

## 3. Copilot CLI

Place the folder in `~/.copilot/skills/osdr-biodata-api/` (personal) or in
the repo's `.github/skills/`. `copilot skill list` (terminal) or
`/skills list` (in a session) shows it; invoke with
`Use the /osdr-biodata-api skill to …` or just ask.

The folder name **must stay `osdr-biodata-api`** — it must match the `name`
field in `SKILL.md`.

---

## 4. Check it works

In a fresh Agent-mode chat:

| Ask | Expect |
|---|---|
| *List all Drosophila datasets in OSDR with their titles.* | 17 datasets from a `/datasets/` URL with `organism=/drosophila/` |
| *Which OSDR datasets come from the RR-1 mission, and what assays and tissues do they include?* | 25 datasets (80 dataset × assay × tissue rows), including the `RR-1_BSP` alias |
| *I need physical tissue samples from the RR-9 mice — how do I get them from OSDR?* | No biodata query; a redirect to NBISC (NASA Biological Institutional Scientific Collection) |

**GeneLab Knowledge Graph (optional).** If the `mcp-genelab` MCP server is
connected in this client, the skill uses it first for known-study questions
and labels every answer part as KG or API; nothing in the skill needs
configuring. To connect the server, follow the VS Code / Copilot instructions
in the mcp-genelab repository:
<https://github.com/sbl-sdsc/mcp-genelab/tree/main#vs-code-with-github-copilot>.

More cases: [`testing.md`](testing.md) and
[`../examples/vscode-copilot.md`](../examples/vscode-copilot.md).
