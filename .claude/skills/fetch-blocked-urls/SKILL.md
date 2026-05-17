---
name: fetch-blocked-urls
description: Use when a web source is unreachable from the Claude Code sandbox — typical signals are WebFetch returning HTTP 403, "host not allowed", a tiny response (< 6 KB) whose body contains "Just a moment..." (Cloudflare challenge), or "Attention Required". The skill files a GitHub issue listing the URLs; the repository's `fetch-blocked-urls` action picks it up from a normal HTTP environment, fetches each page, commits the saved HTML and html2text markdown to a new `fetched/issue-N` branch, comments with merge instructions, and leaves the issue open for you to close once merged. Triggers on phrases like "fetch this URL", "the page is blocked", "Cloudflare is blocking us", "save these sources", "I need to read this page but I can't access it".
tags: [research, github, actions, blocked-sources]
allowed-tools: [Bash, mcp__github__issue_write, mcp__github__issue_read]
---

# Fetch blocked URLs

## When to use

Trigger this skill when **all** of the following are true:

- A web page is unreachable from this sandbox (`WebFetch` returns 403 / "host not allowed" / a Cloudflare challenge / a tiny suspicious response).
- You have already verified the issue is not a typo or a redirect (e.g., for GitHub repos you tried `raw.githubusercontent.com`; for blogs you tried both the canonical URL and any obvious mirror).
- You actually need the content to make progress — don't trigger for incidental references that aren't load-bearing.

If the source is paywalled (Every.to chain-of-thought past the visible portion; Lenny's Newsletter interview bodies), the fetcher cannot bypass that. It will commit whatever the action receives, which for paywalled content means the visible "subscribe to read" portion only. Note the limit and move on.

## What it does

The repository's `.github/workflows/fetch-blocked-urls.yml` workflow does the work. When you file a labelled issue:

1. Workflow triggers on `issues: opened | edited | labeled | reopened` (and supports `workflow_dispatch` for re-runs). Every event spins up a runner so the gate decisions are visible in the Actions UI logs — this is deliberate; an earlier job-level `if:` gate silent-skipped without leaving evidence.
2. **Label gate.** The workflow's first logged step checks the issue carries the `fetch-urls` label and exits cleanly otherwise. The label is the security boundary (see *Authorization model* below).
3. URLs are extracted from the issue body (`extract_urls.py`) — bare `https://…`, markdown `[text](url)`, and URLs inside fenced code blocks all work. Duplicates dropped (first occurrence wins). Trailing punctuation (`.`, `,`, `;`, `:`, `!`, `?`, quotes) is stripped.
4. Cap: at most **50 URLs per issue**, 30-second per-URL timeout. Over the cap → the workflow comments and exits non-zero.
5. Each URL is fetched with `curl -L -A 'Mozilla/5.0 (compatible; software-factory-fetch/1.0; …)' --max-time 30` (`fetch_urls.sh`).
6. For each URL, two files are written:
   - `research/fetched/issue-<N>/<sha1prefix>_<sanitized-host-and-tail>.html` — raw response body
   - `research/fetched/issue-<N>/<sha1prefix>_<sanitized-host-and-tail>.md` — best-effort html2text conversion (only written on HTTP 200)
7. The output is committed to a **new branch** `fetched/issue-<N>` (never to `main`, never to your working branch). If the branch already exists from a previous run, it is force-updated (the issue body is the source of truth).
8. The action comments on the issue with merge instructions and a per-URL summary, then leaves the issue open until you close it.

## Authorization model

**Label-only.** The `fetch-urls` label is the security gate.

Why this works: in GitHub, only users with **Triage role or higher** can apply labels to issues. A drive-by user opening an issue cannot satisfy the gate even if they know the magic label name — they don't have the permission to apply it. Triage is granted explicitly by a repo admin.

The earlier (pre-2026-05-10) version of this workflow gated on `author_association` instead. That gate silently failed because the **webhook payload and the REST API report different values** for the same user on the same event (the webhook said `CONTRIBUTOR`, the REST API said `MEMBER`). Don't reintroduce that check — the label is sufficient and not subject to that footgun.

The job is also bounded by:
- `permissions: contents: write, issues: write` — no secrets, no other repos
- 50-URL per-issue cap, 30s per-URL timeout
- **Never pushes to `main`** — always creates `fetched/issue-<N>`
- No `if: ${{ secrets.X != '' }}` checks (which would allow secret-conditioned behavior)

Residual risk: a compromised collaborator account could trigger fetches of arbitrary URLs. The action does not execute fetched content — it only stores it as files. Worst case: a junk branch gets created and is deleted.

## Usage from this session

Two paths depending on what your harness exposes. **Pick whichever is available** — both invoke the same action via the same GitHub issue gateway, so the outcome is identical.

### Path A — `gh` CLI (preferred when available)

```bash
gh issue create \
  --label fetch-urls \
  --title "[fetch-urls] <short description>" \
  --body "$(cat <<'EOF'
URLs to fetch (one per line; markdown links are accepted):

- https://example.com/some-page
- https://another.example.com/article
- https://third.example/post?id=42

Context (optional): why we need these / which research thread this serves.
EOF
)"
```

The `gh` CLI must be authenticated to a user with Triage role or higher in this repo, so it can apply the label. Run `gh auth status` first if uncertain.

### Path B — restricted GitHub MCP server (when `gh` isn't available)

The Claude Code on the Web sandbox doesn't ship `gh`; it provides a restricted GitHub MCP server instead. The whole skill was designed around what that limited toolset can do — file an issue with a label is one of the supported operations.

Use `mcp__github__issue_write` with `method="create"` and the `labels` array:

```python
mcp__github__issue_write(
    method="create",
    owner="<owner>",       # e.g., "lago-morph"
    repo="<repo>",         # e.g., "software-factory"
    title="[fetch-urls] <short description>",
    body=(
        "URLs to fetch (one per line; markdown links are accepted):\n\n"
        "- https://example.com/some-page\n"
        "- https://another.example.com/article\n"
        "- https://third.example/post?id=42\n\n"
        "Context (optional): why we need these / which research thread this serves.\n"
    ),
    labels=["fetch-urls"],
)
```

The MCP server token is provisioned with `issues: write` for the repo and can apply labels (the equivalent of Triage role), so the label gate is satisfied. The tool returns the created issue's number — capture it for the `git fetch origin fetched/issue-<N>` step later.

### Auto-detection

A research-pipeline integration script (`scripts/file-fetch-issue.py`) reads the catalog's `want` records and tries Path A first; on failure, falls back to Path B via the MCP server. See [research-pipeline](../research-pipeline/SKILL.md#integration-with-fetch-blocked-urls) for the catalog-driven invocation pattern.

### Common notes (both paths)

- The `fetch-urls` label is **mandatory**; the workflow exits cleanly without it. If the label doesn't exist in the repo yet, create it once (`gh label create fetch-urls --description "..."` or via MCP).
- One URL per line is safest. List markers (`-`, `*`, `+`) are tolerated. Markdown link syntax `[text](url)` is parsed correctly. Bare URLs inline in prose also work — the extractor picks up every `http(s)://...` match and deduplicates.
- The issue **title** is convention only (`[fetch-urls] …`). The workflow does not read the title for gating.
- The action will post a comment on the issue with per-URL status and merge instructions within ~1–3 minutes.

After the action completes (typically 1–3 minutes), you'll see a comment on the issue with per-URL status and merge instructions. To pull the fetched content into your working branch:

```bash
git fetch origin fetched/issue-<N>
git merge --no-ff origin/fetched/issue-<N>
```

The action does not auto-close the issue — close it manually once you've merged so other agents know it's handled.

## Re-running against an existing issue

If you need to re-fetch (e.g., a URL was transient and might work now, or you edited the issue body), two paths:

- **Edit the issue body.** The `edited` trigger re-runs the workflow. The `fetched/issue-<N>` branch is force-updated (history reset) so the latest issue body is the source of truth.
- **`workflow_dispatch`.** Trigger manually from the Actions UI with `issue_number: <N>`. Useful for testing without editing the issue. Requires `actions:write` (i.e., a repo collaborator).

```bash
gh workflow run fetch-blocked-urls.yml -f issue_number=<N>
```

Via MCP, edit the issue body to add a no-op edit (e.g., append a timestamp comment line) using `mcp__github__issue_write` with `method="update"` and a tweaked body — that fires the `edited` trigger.

## Filename convention

Files fetched via this action live under `research/fetched/issue-<N>/` with sha1-prefixed sanitized names:

```
<sha1(url)[:10]>_<host-and-tail-sanitized>.html
<sha1(url)[:10]>_<host-and-tail-sanitized>.md
```

The sha1 prefix guarantees uniqueness even for pathological URLs (very long, query-heavy, or characters that collide after sanitization). The trailing host-and-path component is included verbatim (up to 80 chars) so file listings are still browsable.

Example: `https://www.jayminwest.com/agentic-engineering-book/6-harnesses` →
`4f2b8a91c3_www.jayminwest.com__agentic-engineering-book__6-harnesses.html`

This is **different** from the existing top-level repo convention (e.g. `factory.strongdm.ai__principles.html` at the repo root). The two coexist by design: the existing root files were manually curated and named to mirror the URL; the action's files are bulk-fetched into a per-issue subdirectory and need deterministic disambiguation. Don't conflate the two layouts.

## Result classification (per-URL summary)

Each fetched URL appears in the issue comment under "Per-URL summary" with a status:

- `(HTTP 200, N bytes)` — saved. Inspect for content quality (Cloudflare challenges can return 200 with a fake body; check the size and the first few KB).
- `FAILED (HTTP 4xx/5xx, …)` — saved (with whatever partial body came back) plus the first 200 chars of curl's stderr. Useful for debugging.
- `FAILED (HTTP 000, 0 bytes)` — connection error (DNS, TLS, timeout). Nothing useful saved.

When a Cloudflare challenge slips through as HTTP 200, the HTML body will be small (~5–10 KB) and contain "Just a moment..." / "challenge-platform". Inspect, then switch to a fallback.

## Fallbacks when the action also gets blocked

For sources whose Cloudflare challenge the action cannot solve (the runner is not a real browser, so JavaScript challenges fail):

1. **Wayback Machine.** `https://web.archive.org/web/2026*/<original-url>` — file a follow-up issue with the wayback URLs instead. Wayback snapshots are post-render, so they often work where the live URL doesn't.
2. **Google Cache** (when available): prefix the URL with `https://webcache.googleusercontent.com/search?q=cache:`
3. **Medium alternative front-ends.** For Medium articles, try `scribe.rip` or `freedium.cfd` mirrors with the same path.
4. **Manual browser save by the user** — see next section. After exhausting the action + Wayback, hand the still-failing URLs back to the user with a runnable script.

## When automation has been exhausted — emit manual-recovery artifacts

After every fetch issue lands, you'll know which URLs returned ❌ even from a normal HTTP environment (Cloudflare interactive challenges, paywalled bodies, login-required pages). For those, the next step is the user's own browser — only a real browser session has the cookies and the JS engine to bypass these.

**As soon as you have a confirmed list of URLs that survived the action AND any Wayback retry, write two artifacts in `research/`:**

1. **`research/unfetched-sources.md`** — link list with the rationale per URL: *why* it failed (Cloudflare / paywall / login), *what we need from it*, *which report it affects*. This is the user-facing inventory; keep it updated as URLs get resolved or new ones get added.

2. **`research/fetch-from-browser.sh`** — a runnable bash script that takes the user's exported browser cookies (Netscape format) and runs `curl -b <cookies> -A <recent-realistic-UA>` against the URL list. It must:
   - Output to `research/manual/` (not `research/fetched/issue-N/`, which is reserved for the action).
   - Use a sha1-prefixed sanitized filename matching this skill's convention (so the research-pipeline skill can deduplicate across sources).
   - Detect Cloudflare stubs in the response (small body containing "Just a moment" / "Attention Required" / "cf-mitigated") and rename them `*.cloudflare-stub` rather than passing them off as content.
   - Print clear instructions for the cookies-export step at the top of the file (extension names per browser).
   - Note which URLs even cookies+UA won't solve (interactive Cloudflare challenges) — for those, instruct the user to use **File → Save Page As → Web Page Complete** in their browser and drop the HTML into `research/manual/` directly.

A canonical version of both files lives in `research/` once you've done this; the user can re-run the script anytime new URLs get added to the list. The corresponding "drain" step belongs to the [`research-pipeline`](../research-pipeline/SKILL.md) skill (Phase 0 — scan `research/` subdirectories for new content and dispatch subagents to incorporate them).

**Do not skip the artifact step.** It's tempting to just tell the user "go fetch these in your browser" in chat, but that loses the URL list, the per-URL rationale, and the runnable retry path the next time around. Commit both files; they are part of the research record.

## Limitations

- **No login / no paywall bypass.** The action cannot authenticate. Captured content for paywalled URLs is the visible "subscribe to read" portion only.
- **JavaScript challenges.** Cloudflare's interactive challenges cannot be solved by curl. Use Wayback or manual save.
- **No JS-rendered DOM.** The fetcher receives the initial HTML response, not the rendered DOM. For SPAs that render content client-side, the saved HTML may be skeletal. Wayback's post-render snapshots are usually a fix.
- **Runner minute quota.** GitHub Actions minutes are not unlimited. Bundle related URLs into one issue rather than firing many small issues.
- **Each issue produces a new branch.** Don't be surprised by branch proliferation; `fetched/issue-*` branches are safe to delete after merge.

## Disabling

- **Skill:** delete `.claude/skills/fetch-blocked-urls/`.
- **Action:** delete `.github/workflows/fetch-blocked-urls.yml` (or rename to `.yml.disabled`).
- **Soft-disable:** remove the `fetch-urls` label from the repo. New issues then can't satisfy the gate.

## See also

- `.github/workflows/fetch-blocked-urls.yml` — the workflow definition (with inline security commentary)
- `.github/scripts/extract_urls.py` — URL extractor (bare + markdown-link + dedup)
- `.github/scripts/fetch_urls.sh` — per-URL curl + html2text + summary writer
- `.github/scripts/README.md` — short helper documentation with local-test recipes
- `research/PLAN.md` §5–6 — the original design rationale, including the `author_association` footgun discussion
- `research/blocked-urls-round-2.md` — the Round-2 URL inventory; the canonical example of how to format issue bodies
