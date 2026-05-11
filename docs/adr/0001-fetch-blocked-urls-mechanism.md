# 0001. Use the `fetch-blocked-urls` action for sandbox-blocked sources

- **Status**: Accepted
- **Date**: 2026-05-11
- **Deciders**: session (rationale and reconciliation are recorded in the linked research)

## Context

Claude Code agent sessions in this repo run in a sandbox that returns HTTP
403 ("host not allowed") for nearly every host other than
`raw.githubusercontent.com`. This blocks the canonical sources for most
research the project needs: factory.strongdm.ai, every.to,
simonwillison.net, news.ycombinator.com, lennysnewsletter.com, el-kaim.com,
and others. The blocking is documented in
[`research/blocked-urls.md`](../../research/blocked-urls.md), with the
specific reachability matrix and per-source impact in
[the v2 synthesis revision notes](../../research/00-synthesis.md#0-revision-notes-v2)
and the round-2 follow-up in
[`research/blocked-urls-round-2.md`](../../research/blocked-urls-round-2.md).

Reconstructing primary sources from secondary coverage during v1 produced
five distinct fabrications that propagated into the architecture specs
before the v2 pass caught them — see
[research synthesis §0 (revision notes)](../../research/00-synthesis.md#0-revision-notes-v2)
for the inventory. The cost of *not* having primary access is high enough
to warrant infrastructure rather than ad-hoc manual fetches.

Two agents independently approached the problem in parallel: one branch
(`claude/followup-and-fetch-skill`) proposed a label-and-author-allowlist
gated workflow committing into the repo root; the round-2 branch
(merged into `main` as PR #3) shipped a label-only gated workflow that
commits to per-issue side branches. The reconciliation that resolved this
collision is documented in the present ADR.

## Decision

Use the `fetch-blocked-urls` GitHub Action at
[`.github/workflows/fetch-blocked-urls.yml`](../../.github/workflows/fetch-blocked-urls.yml)
as the **single mechanism** for retrieving sandbox-blocked web sources.

The mechanism's contract:

1. **Trigger.** An agent files a GitHub issue, titled `[fetch-urls] <description>`,
   body containing one URL per line (markdown links accepted). The issue
   carries the `fetch-urls` label.
2. **Authorization.** Label-only, via GitHub's Triage-role-required-to-label
   rule. The label is the security boundary; `author_association` is **not**
   used (the webhook payload and the REST API disagree for the same user —
   the explicit rationale is in
   [`research/PLAN.md` §6](../../research/PLAN.md#6-github-action--security-stance)).
3. **Fetcher.** A normal GitHub runner curl-fetches each URL (50-URL cap,
   30s per-URL timeout) using a realistic User-Agent.
4. **Output.** Two files per URL, written into
   `research/fetched/issue-<N>/`: raw HTML and best-effort html2text
   markdown.
5. **Branch.** A new branch `fetched/issue-<N>` (never `main`, never the
   triggering branch). The agent merges that branch into their working
   branch via the instructions in the issue comment.
6. **Documentation surface.** The agent-facing entry point is the
   [`fetch-blocked-urls` skill](../../.claude/skills/fetch-blocked-urls/SKILL.md);
   the operational scripts are
   [`extract_urls.py`](../../.github/scripts/extract_urls.py) and
   [`fetch_urls.sh`](../../.github/scripts/fetch_urls.sh), with helper
   documentation in
   [`.github/scripts/README.md`](../../.github/scripts/README.md).

## Consequences

What this buys:

- **Primary-source access** for research domains the sandbox blocks. Issue
  #4 used this mechanism to retrieve 13 of 14 Tier-1 and Tier-2 round-2
  sources, materially improving report fidelity (see
  [`research/PLAN.md` §10.1](../../research/PLAN.md#101-fetch-action-history)).
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
  authentication, JS rendering, or aggressive rate limiting is out of scope.
- It is not pushed to `main`. The 1:1 mapping is "one issue, one side
  branch."

## Alternatives Considered

- **Manual curl from within the sandbox.** Rejected: the sandbox 403s the
  source domains. This is the problem the ADR addresses.
- **`WebFetch` tool.** Useful for directory listings or "give me the gist
  of this page", but uses a small model that may summarize — observed in
  this session, where one of three SKILL.md fetches returned a paraphrase
  rather than verbatim content. Rejected as the *single* mechanism;
  retained as a complement for low-fidelity reads.
- **Manual browser save + commit.** Listed as a fallback in the
  [`fetch-blocked-urls` skill's "Fallbacks" section](../../.claude/skills/fetch-blocked-urls/SKILL.md#fallbacks-when-the-action-also-gets-blocked).
  Rejected as the primary path: slow, unscriptable, depends on a human at a
  desktop browser.
- **A label-plus-author-allowlist gate** (the original proposal on the
  `claude/followup-and-fetch-skill` branch). Rejected during reconciliation
  because the label alone — via GitHub's Triage-role-required-to-label rule
  — is sufficient and avoids the `author_association` footgun documented
  in [PLAN §6](../../research/PLAN.md#6-github-action--security-stance).
  `author_association` reports `CONTRIBUTOR` in the webhook and `MEMBER`
  in the REST API for the same user — the inconsistency causes silent-skip
  failures.
- **Pushing fetched output to the triggering branch directly.** Rejected:
  conflates the fetched-content commit history with the working-branch
  history and makes it harder to discard a bad fetch. The side-branch
  design keeps `main` clean and review-friendly.
- **A third-party scraping service.** Rejected: security exposure (secrets
  in URLs), cost, and an external dependency we don't otherwise need.

## References

- (skill) [`.claude/skills/fetch-blocked-urls/SKILL.md`](../../.claude/skills/fetch-blocked-urls/SKILL.md) — the agent-facing trigger surface.
- (workflow) [`.github/workflows/fetch-blocked-urls.yml`](../../.github/workflows/fetch-blocked-urls.yml) — the action definition with inline security commentary.
- (scripts) [`.github/scripts/extract_urls.py`](../../.github/scripts/extract_urls.py), [`.github/scripts/fetch_urls.sh`](../../.github/scripts/fetch_urls.sh), [`.github/scripts/README.md`](../../.github/scripts/README.md).
- (plan) [`research/PLAN.md` §5 — the blocked-URL fetch loop](../../research/PLAN.md#5-the-blocked-url-fetch-loop) and [§6 — security stance](../../research/PLAN.md#6-github-action--security-stance).
- (plan) [`research/PLAN.md` §10.1 — fetch action history](../../research/PLAN.md#101-fetch-action-history) — record of issue #4 (13/14 URLs fetched).
- (research) [`research/blocked-urls.md`](../../research/blocked-urls.md) — round-1 inventory of blocked URLs.
- (research) [`research/blocked-urls-round-2.md`](../../research/blocked-urls-round-2.md) — round-2 inventory.
- (research) [`research/00-synthesis.md` §0 — revision notes (v2)](../../research/00-synthesis.md#0-revision-notes-v2) — the v1→v2 fabrications, including the cost of *not* having primary access.
- (external) [Michael Nygard, "Documenting Architecture Decisions"](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — the original ADR essay.
