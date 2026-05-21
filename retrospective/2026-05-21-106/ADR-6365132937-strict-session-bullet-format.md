# ADR: Strict three-component session-bullet format in research/PLAN.md

- **ID**: ADR-6365132937
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-106.md
- **PRs covered**: #106

## Context

`research/PLAN.md` §1 was originally a top-level "current state (TL;DR)" but had evolved into an accreted log of session bullets, one per drain. Each bullet was a 100-300 word paragraph written by the research-pipeline skill's drain-time auto-append (per the skill's `_plan/update-discipline.md`). Over 17+ sessions this produced ~30 KB of accreted prose under §1 alone. The most recent bullet (Round-10, PR #67) was a single ~600-word paragraph spanning cluster-by-cluster narrative, surprises, refutations, and follow-ups — readable in isolation, but unreadable as part of the doc's status line.

During the cleanup-plan iteration the agent (me) tried two compressions in succession: v2 used a one-sentence summary with PR hyperlink (~30-50 words per bullet); v3 used the strict three-component form (date + 24h-time + run name + PR link, under 10 words). User feedback on v2: "you are cheating and turning three sentences into 1 with semicolons. The new one in your example should only have date and time (24 hour format), round 11 manual drain, and link to pr. That's it." The strict form is what landed in cleanup-plan v3.

## Decision

Session bullets in `research/PLAN.md` §1 are exactly date, 24-hour time, run name, and PR hyperlink — no prose narrative, no content summary, no semicolon-joined clauses. Format: `**YYYY-MM-DD HH:MM <Run-name>** [#nn](pr-url)`.

## Alternatives considered

- **One-sentence per bullet, with PR link.** Rejected: tested in cleanup-plan v2; produced 30-50 word bullets and tempted semicolon-cheating. The user's correction surfaced the failure mode that "one sentence" is not a useful constraint when the LLM can compress arbitrary structure into one sentence.
- **Delete the §1 bullet log entirely; rely on §10 round-by-round table and git log.** Considered: §10 already serves the audit-trail role. Rejected on the narrower ground that the drain pipeline auto-appends bullets and the discipline of "every drain has a §1 bullet" is enforced by the research-pipeline skill's `_plan/check-plan-consistency.py` lint. Keeping the bullets but tightening the format preserves the discipline without the verbosity.
- **Use markdown checklist `- [x]` per session.** Rejected as semantically misleading — these aren't tasks to complete, they're things that already happened.

## Consequences

**Easier:**
- §1 stays short enough to actually serve as a TL;DR — readers can scan all sessions in seconds instead of minutes.
- The drain pipeline's auto-emit logic is simpler: assemble four fields, format, append.
- No cross-bullet inconsistency in tone, formatting, or length.

**Harder:**
- The "what changed in this drain?" content has to live in the PR description (which is git-versioned and durable) rather than in PLAN.md. PR authors must write good PR descriptions or the audit trail is incomplete. Existing PR-description discipline is moderate-to-good in this repo; this rule depends on it.

**Trade-off accepted:** PLAN.md is no longer a self-contained narrative log; readers needing detail follow the PR hyperlink. This is consistent with the broader principle that source-of-truth content lives in its native register (catalog state in sources.json, decision rationale in ADRs, audit content in git log + PR descriptions) and PLAN.md is an index, not a duplicate.

## References

- [`../2026-05-21-106.md`](../2026-05-21-106.md) — the source retrospective.
- [`./AGENTS-MD-14c22afe82-strict-session-bullet-format.md`](./AGENTS-MD-14c22afe82-strict-session-bullet-format.md) — the corresponding AGENTS.md rule.
- [`./SKILL-SPEC-d5f8b37eeb-plan-doc-curation.md`](./SKILL-SPEC-d5f8b37eeb-plan-doc-curation.md) — the plan-doc curation skill, which applies this rule during cleanup.
- PR the decision was made in: #106.
- Pre-existing skill resource to update: `.claude/skills/research-pipeline/resources/_plan/update-discipline.md`.
