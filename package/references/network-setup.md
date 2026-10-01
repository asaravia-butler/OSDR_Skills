# Network setup — letting the agent reach OSDR

The API needs **no key, no login, no auth**. The only prerequisite is that the
agent's sandbox may make outbound HTTPS requests to these hosts:

```
visualization.osdr.nasa.gov   # the API (all query / metadata / data calls)
osdr.nasa.gov                 # file downloads (file.remote_url targets)
nasa-osdr.s3.amazonaws.com    # public S3 bucket (bulk data, version-N folders)
s3.us-west-2.amazonaws.com    # S3 region endpoint (path-style listing)
```

`visualization.osdr.nasa.gov` alone covers every query in SKILL.md.

## How to run a call (in order of preference)

1. The client's built-in web-fetch / HTTP tool on the exact URL.
2. `curl -sgL "<url>"` (the `-g`/`--globoff` flag is required: `[ ]` and `( )` in
   OSDR regexes and column names otherwise trigger curl's URL globbing and the
   call fails with exit code 3 and no output) or `python3 scripts/osdr_query.py …`.
3. Python `urllib`/`requests` when you need to post-process (intersections,
   per-subject aggregation).

## Recognising a blocked call

`Host not in allowlist`, `403 blocked-by-allowlist`, `ENOTFOUND`, a refused
"parameterized fetch", or a fetch that returns nothing in < 1 s means **egress
is blocked, not that the URL is wrong**. Do not rewrite the query. Hand the URL
to the user with the one setup step below, or ask them to paste the response.

## Per-client notes

**Claude (claude.ai chat, Cowork, Claude Code)** — claude.ai chat uses its web
fetch tool; nothing to configure. Cowork / Claude Code sandboxes: enable
network egress and add the hosts to the allowed-domains list ("Allow network
egress" → "Additional allowed domains"; enter full hostnames). For Team /
Enterprise an admin may need to allow it under Admin settings → Capabilities.

**ChatGPT / Codex** — ChatGPT with browsing can fetch the URLs directly. Codex
CLI / IDE sandboxes have network off by default: run with network enabled (e.g.
`codex --sandbox danger-full-access` or set `[sandbox_workspace_write]
network_access = true` in `~/.codex/config.toml`), or approve the command when
prompted.

**Gemini CLI** — shell tool commands (`curl`, `python3`) run on the host and
normally have network. If a sandbox (`--sandbox`) is on, allow the hosts or
run without the sandbox. The built-in `web_fetch` tool also works for
`json.records` / `csv` URLs.

**VS Code Copilot (agent mode)** — uses the integrated terminal for `curl` /
`python3`, so the developer's own network applies; the `fetch` tool
(`#fetch <url>`) also works. Corporate proxies must allow the hosts above.

## If egress cannot be enabled

Still build the exact URL(s), give them to the user, state the one setup step
needed, and offer to interpret the response if they paste it back.
