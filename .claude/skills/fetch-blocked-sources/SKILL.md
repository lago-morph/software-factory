---
name: fetch-blocked-sources
description: Use when a web source is unreachable from the Claude Code sandbox — typical signals are WebFetch returning HTTP 403, "host not allowed", a tiny response (< 6 KB) whose body contains "Just a moment..." (Cloudflare challenge), or "Attention Required". The skill files a GitHub issue listing the URLs; a repository action picks it up from a normal HTTP environment, fetches each page, commits the saved HTML to the repo at the root, comments back on the issue, and closes it. Triggers on phrases like "fetch this URL", "the page is blocked", "Cloudflare is blocking us", "save these sources", "I need to read this page but I can't access it".
tags: [research, github, actions, blocked-sources]
allowed-tools: [Bash]
---

# Fetch blocked sources

## When to use

Trigger this skill when **all** of the following are true:

- A web page is unreachable from this sandbox (`WebFetch` returns 403 / "host not allowed" / a Cloudflare challenge / a tiny suspicious response).
- You have already verified the issue is not a typo or a redirect (e.g., for GitHub repos you tried `raw.githubusercontent.com`; for blogs you tried both the canonical URL and any obvious mirror).
- You actually need the content to make progress — don't trigger this for incidental references that aren't load-bearing.

If the source is paywalled (Every.to chain-of-thought articles past the visible portion; Lenny's Newsletter interview bodies), the fetcher cannot bypass that. It will commit whatever the action receives, which for paywalled content means the visible "subscribe to read" portion only. Note the limit and move on.

## What it does

1. You create a GitHub issue with title and body describing what you want fetched. The body lists one URL per line (with or without markdown list markers).
2. You tag the issue with the label `fetch-sources`.
3. The action at `.github/workflows/fetch-blocked-sources.yml` triggers if and only if:
   - The issue carries the `fetch-sources` label, AND
   - The issue author is in the allowlist (defaults to the repository owner; configurable via the `FETCH_ALLOWED_AUTHORS` repository variable).
4. The action fetches each URL with a realistic User-Agent, saves the HTML at the repo root using the existing filename convention (`example.com__foo__bar.html`), commits the new files to the same branch the workflow ran on (typically `main`), comments the result list on the issue, and closes the issue.
5. You then `git fetch` / `git pull` to access the new files.

## Authorization model

Two layered checks prevent unrelated users from triggering compute:

- **Label check.** `fetch-sources` label required. Random new issues without it do nothing.
- **Author allowlist.** Issue author must match the repository owner by default. To allow additional usernames, set the repository variable `FETCH_ALLOWED_AUTHORS` to a JSON array of usernames (e.g., `["lago-morph","my-other-handle"]`).

Both checks must pass. If either fails, the job silently does nothing (no comment, no compute spent).

## Usage from this session

You can file the issue directly via the `gh` CLI. The standard template:

```bash
gh issue create \\
  --label fetch-sources \\
  --title "Fetch blocked sources: <short description>" \\
  --body "$(cat <<'EOF'
URLs to fetch (one per line):
- https://example.com/some-page
- https://another.example.com/article
- https://third.example/post?id=42

Context (optional): why we need these / which research thread this serves.
EOF
)"
```

Notes:
- The `fetch-sources` label is required; the action's authorization check is a hard gate.
- One URL per line is the safest format. Markdown list markers (`-`, `*`, `+`) are stripped automatically. Plain inline URLs in prose also work — the script extracts every `http(s)://...` match in the body and deduplicates.
- The `gh` CLI must be installed and authenticated to a user that's in the `FETCH_ALLOWED_AUTHORS` allowlist (typically the repo owner). Run `gh auth status` first if uncertain.

After filing, the action typically completes in 1–3 minutes. You'll see a comment on the issue with per-URL status, and the issue will be closed when done.

To wait for completion programmatically:

```bash
# Poll until the action's comment appears, then pull
issue_number=42  # replace with the issue number you just created
until gh issue view "$issue_number" --json comments --jq '.comments | length > 0' | grep -q true; do
  sleep 15
done
git pull
```

(In an interactive session, just check the issue tab manually rather than polling.)

## Filename convention the action uses

The action's filenames match what's already in the repo:

| URL | Filename |
|---|---|
| `https://factory.strongdm.ai/` | `factory.strongdm.ai.html` |
| `https://factory.strongdm.ai/principles` | `factory.strongdm.ai__principles.html` |
| `https://factory.strongdm.ai/techniques/dtu` | `factory.strongdm.ai__techniques__dtu.html` |
| `https://news.ycombinator.com/item?id=46924426` | `news.ycombinator.com__item__q__id_eq_46924426.html` |
| `https://medium.com/@welkaim/about` | `medium.com___at_welkaim__about.html` |

Rules:
- Scheme stripped; host kept lowercase
- `/` → `__`
- `@` → `_at_`
- `?` separator → `__q__`
- `=` (in query keys) → `_eq_`
- `&` → `_amp_`
- Filename always ends in `.html`

## Result classification

Each fetched URL is marked in the comment:

- ✅ Success (≥ 2 KB and no Cloudflare markers)
- ⚠️ Cloudflare challenge (the HTML body contains markers like "Just a moment...", "challenge-platform", "checking your browser") — the file is still saved so you can inspect it, but the content is not useful
- ⚠️ Small response (< 2 KB) — possibly a block page; save and inspect
- ❌ Fetch failed (HTTP error, timeout, etc.) — no file written

When you see ⚠️ for a Cloudflare challenge, try one of the fallbacks below before declaring the source unreachable.

## Fallbacks when the action also gets blocked

For genuinely unreachable sources (the action saw the same Cloudflare challenge a manual browser would have to solve), try in order:

1. **Wayback Machine.** `https://web.archive.org/web/2026*/<original-url>` — file a follow-up issue with the wayback URL instead.
2. **Google Cache** (when available): prefix the URL with `https://webcache.googleusercontent.com/search?q=cache:`
3. **Medium alternative front-end.** For Medium articles, try `scribe.rip` or `freedium.cfd` mirrors with the same path.
4. **Manual save.** As a last resort, open the page in a real browser yourself, "Save as → Web page complete (single file)", and commit the HTML to the repo manually.

## Limitations

- **No login.** The action cannot authenticate to paywalled sites. Captured content for paywalled URLs is the visible "subscribe to read" portion only.
- **Active challenges.** Cloudflare's JavaScript challenges cannot be solved by a curl-style fetch. The action commits the challenge HTML so you have evidence; switch to a fallback (Wayback, manual save) for the actual content.
- **Quotas.** GitHub Actions runner minutes are not unlimited; bursting hundreds of fetches per day is wasteful. Batch related URLs into one issue.
- **No JavaScript rendering.** The fetcher receives the initial HTML response, not the JS-rendered DOM. For SPAs that render content client-side, the saved HTML may be empty / skeletal. Reach for the Wayback Machine if so — its snapshots are usually post-render.
- **One issue → one branch.** The action commits to whatever branch it was triggered from. If you create the issue while on a feature branch with the workflow file present on that branch, the action runs against `main` (the default). Issues are pull-request-agnostic.

## Updating the allowlist

To add a username to the allowlist without editing the workflow:

```bash
gh variable set FETCH_ALLOWED_AUTHORS --body '["lago-morph","another-handle"]'
```

The variable is read at job-run time. JSON-array format is required.

## Disabling the skill / action

- **Skill:** delete or move `.claude/skills/fetch-blocked-sources/`.
- **Action:** delete `.github/workflows/fetch-blocked-sources.yml` (or rename it to `.yml.disabled`).
- **Soft-disable:** remove the `fetch-sources` label from the repository's labels. New issues with the label name won't be accepted because the label won't exist; existing labelled issues are harmless once the label is gone (the workflow's `contains(...)` check returns false).
