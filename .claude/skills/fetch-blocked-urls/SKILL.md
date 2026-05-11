---
name: fetch-blocked-urls
description: Use when a web source is unreachable from the Claude Code sandbox — typical signals are WebFetch returning HTTP 403, "host not allowed", a tiny response (< 6 KB) whose body contains "Just a moment..." (Cloudflare challenge), or "Attention Required". The skill files a GitHub issue listing the URLs; the repository's `fetch-blocked-urls` action picks it up from a normal HTTP environment, fetches each page, commits the saved HTML and html2text markdown to a new `fetched/issue-N` branch, comments with merge instructions, and leaves the issue open for you to close once merged. Triggers on phrases like "fetch this URL", "the page is blocked", "Cloudflare is blocking us", "save these sources", "I need to read this page but I can't access it".
tags: [research, github, actions, blocked-sources]
allowed-tools: [Bash]
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

Use the `gh` CLI. Standard template:

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

Notes:
- The `fetch-urls` label is mandatory; the workflow exits cleanly without it. If the label doesn't exist in the repo yet, create it once via `gh label create fetch-urls --description "Trigger fetch-blocked-urls.yml workflow"`.
- One URL per line is safest. List markers (`-`, `*`, `+`) are tolerated. Markdown link syntax `[text](url)` is parsed correctly. Bare URLs inline in prose also work — the extractor picks up every `http(s)://...` match and deduplicates.
- The issue **title** is convention only (`[fetch-urls] …`). The workflow does not read the title for gating.
- The `gh` CLI must be authenticated to a user with Triage role or higher in this repo, so it can apply the label. Run `gh auth status` first if uncertain.

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
4. **Manual save.** As a last resort, open the page in a real browser yourself, "Save as → Web page complete (single file)", and commit the HTML to `research/fetched/manual/` on a branch.

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
