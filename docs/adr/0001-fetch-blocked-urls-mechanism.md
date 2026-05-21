# ADR 0001: Use the fetch-blocked-urls action for sandbox-blocked sources

- **Status**: Accepted
- **Date**: 2026-05-11

## Context

Claude Code agent sessions in this repo run in a sandbox that returns
HTTP 403 ("host not allowed") for nearly every host other than
`raw.githubusercontent.com`. This blocks the canonical sources for most
research the project needs: factory.strongdm.ai, every.to,
simonwillison.net, news.ycombinator.com, lennysnewsletter.com,
el-kaim.com, and others. The blocking and its per-source impact are
documented in `research/blocked-urls.md` and the round-2 inventory in
`research/blocked-urls-round-2.md`.

Reconstructing primary sources from secondary coverage during the v1
research pass produced five distinct fabrications that propagated into
the architecture specs before the v2 pass caught them. The cost of *not*
having primary access is high enough to warrant infrastructure rather
than ad-hoc manual fetches.

Two agents independently approached the problem in parallel: one branch
proposed a label-and-author-allowlist gated workflow committing into the
repo root; the round-2 branch shipped a label-only gated workflow that
commits to per-issue side branches. The reconciliation that resolved
this collision is documented in the present ADR.

## Decision

Use the `fetch-blocked-urls` GitHub Action at
`.github/workflows/fetch-blocked-urls.yml` as the **single mechanism**
for retrieving sandbox-blocked web sources.

The mechanism's contract:

1. **Trigger.** An agent files a GitHub issue, titled `[fetch-urls] <description>`,
   body containing one URL per line (markdown links accepted). The issue
   carries the `fetch-urls` label.
2. **Authorization.** Label-only, via GitHub's Triage-role-required-to-label
   rule. The label is the security boundary; `author_association` is
   **not** used (the webhook payload and the REST API disagree for the
   same user — silent-skip failure mode documented in the linked plan).
3. **Fetcher.** A normal GitHub runner curl-fetches each URL (50-URL cap,
   30s per-URL timeout) using a realistic User-Agent.
4. **Output.** Two files per URL, written into
   `research/fetched/issue-<N>/`: raw HTML and best-effort html2text
   markdown.
5. **Branch.** A new branch `fetched/issue-<N>` (never `main`, never the
   triggering branch). The agent merges that branch into their working
   branch via the instructions in the issue comment.
6. **Documentation surface.** Agent-facing entry point is the
   `fetch-blocked-urls` skill; the operational scripts are
   `extract_urls.py` and `fetch_urls.sh` with helper documentation in
   `.github/scripts/README.md`.

## Alternatives considered

- **Manual curl from within the sandbox.** Rejected: the sandbox 403s
  the source domains. This is the problem the ADR addresses.
- **`WebFetch` tool as the primary path.** Useful for directory listings
  or "give me the gist of this page", but uses a small model that may
  summarize. Observed in this session: one of three SKILL.md fetches
  returned a paraphrase rather than verbatim content. Rejected as the
  *single* mechanism; retained as a complement for low-fidelity reads.
- **Manual browser save + commit.** Listed as a fallback in the
  skill's "Fallbacks" section. Rejected as the primary path: slow,
  unscriptable, depends on a human at a desktop browser.
- **A label-plus-author-allowlist gate** (the original proposal on the
  `claude/followup-and-fetch-skill` branch). Rejected during
  reconciliation because the label alone — via GitHub's
  Triage-role-required-to-label rule — is sufficient and avoids the
  `author_association` footgun. `author_association` reports
  `CONTRIBUTOR` in the webhook and `MEMBER` in the REST API for the same
  user; the inconsistency causes silent-skip failures.
- **Pushing fetched output to the triggering branch directly.** Rejected:
  conflates the fetched-content commit history with the working-branch
  history and makes it harder to discard a bad fetch. The side-branch
  design keeps `main` clean and review-friendly.
- **A third-party scraping service.** Rejected: security exposure
  (secrets in URLs), cost, and an external dependency we don't otherwise
  need.

## Consequences

What this buys:

- **Primary-source access** for research domains the sandbox blocks.
  Issue #4 used this mechanism to retrieve 13 of 14 Tier-1 and Tier-2
  round-2 sources, materially improving report fidelity.
- **A small audit trail.** Each fetch is one issue → one comment → one
  branch. Provenance is explicit and reviewable.
- **A reusable workflow** rather than per-source manual saves.

What this costs:

- **One side branch per issue.** `fetched/issue-*` branches proliferate;
  they're safe to delete after merge but operationally noisy.
- **No paywall / JavaScript-challenge bypass.** Cloudflare interactive
  challenges and login walls remain unsolved; for those, the skill
  documents fallbacks (Wayback Machine, manual save).
- **Trust assumption.** Anyone with Triage role on the repo can trigger
  fetches. Mitigated by the action not executing fetched content and by
  scoped permissions (`contents: write`, `issues: write` only).

What this is explicitly **not** promising:

- It is not a general scraping infrastructure. Anything that needs
  authentication, JS rendering, or aggressive rate limiting is out of
  scope.
- It is not pushed to `main`. The 1:1 mapping is "one issue, one side
  branch."

## References

- [`.github/workflows/fetch-blocked-urls.yml`](../../.github/workflows/fetch-blocked-urls.yml) — the action definition.
- [`.github/scripts/`](../../.github/scripts/README.md) — [extract_urls.py](../../.github/scripts/extract_urls.py), [fetch_urls.sh](../../.github/scripts/fetch_urls.sh).
- [`.claude/skills/fetch-blocked-urls/SKILL.md`](../../.claude/skills/fetch-blocked-urls/SKILL.md) — agent-facing trigger surface.
- [`research/PLAN.md`](../../research/PLAN.md) [§5](../../research/PLAN.md#5-the-blocked-url-fetch-loop), [§6](../../research/PLAN.md#6-github-action--security-stance), [§10.1](../../research/PLAN.md#101-fetch-action-history) — the blocked-URL fetch loop, security stance, and fetch-action history (issue #4 outcome).
- [`research/blocked-urls.md`](../../research/blocked-urls.md), [`research/blocked-urls-round-2.md`](../../research/blocked-urls-round-2.md) — the round-1 and round-2 URL inventories.
- [`research/synthesis/00-synthesis.md`](../../research/synthesis/00-synthesis.md) [§0 (revision notes v2)](../../research/synthesis/00-synthesis.md#0-revision-notes-v2) — the v1→v2 fabrications, including the cost of *not* having primary access.
- [Michael Nygard, "Documenting Architecture Decisions"](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — the original ADR essay.
