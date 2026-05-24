# ADR: Permalink-with-guard pattern for contaminated artifacts

- **ID**: ADR-252ceb7ed9
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-24
- **Source retrospective**: ../2026-05-24-128.md
- **PRs covered**: #128

## Context

Phase-2 of the v3 architecture synthesis produced 16 contamination-bearing artifacts (9 contaminated tracks, 4 bias-guard audits that diagnosed the contamination, 3 diagnostic follow-up tracks). After the contamination was identified, the lead agent needed to fence these off so the next session executing the Phase-2 re-run would not read them as input — but the user also wanted them preserved as historical record (so a human reviewer or a future archaeologist could retrieve them on demand).

The lead agent's first attempt was to move the artifacts to a `tracks-superseded/` subdirectory with a sibling `ARCHIVE.md` listing each file. The user explicitly rejected this design with the framing "you are just hanging out in front of a curious agent the forbidden fruit." The structural problem: a moved-but-visible directory advertises the artifacts to any agent that lists the tree; the curious-agent failure mode the cleanup was supposed to prevent remains live.

Two alternatives existed: (a) pure deletion (loses archaeological access), (b) in-place sanitization (rewrite the artifacts to remove the contamination while keeping the substance). In-place sanitization was tried at small scale (rewording a single F-mode mechanism field) and worked there, but applying it to 16 multi-page documents was infeasible at this point in the session, and would have produced ambiguous results (was the sanitized version corpus-faithful, or had the lead agent re-introduced different bias?).

The user-mandated pattern: a single reference document under a `history/` directory, with a guard header at the top explicitly telling any agent that finds the doc "do not read these into your context window." Per-artifact entries give the original path, a one-line description, and a `git show <commit>:<path>` retrieval command. The active tree loses the artifacts entirely; the reference doc is the only entry point.

## Decision

Contaminated or context-risky artifacts that must be removed from active use but preserved for archaeology are fenced off via the permalink-with-guard pattern:

1. **Create a single reference doc** at a path that names it as historical material (this project: `architectures/v3/history/HISTORICAL-RECORD.md`).
2. **Guard header at the top.** The first content section is a "⚠ STOP — do not read these into your context window" warning. The warning explains why (re-introducing bias) and what to do if archaeological access is genuinely needed (use the git-show retrieval command, ideally outside the agent context).
3. **Per-artifact entries.** Each entry gives the original path, a one-line description of what the artifact was (no detail beyond identification), and a `git show <commit>:<path>` retrieval command. The commit hash is the last commit where the file existed at its original path.
4. **Active tree loses the artifacts entirely.** No moved-but-visible directory. The contamination cannot leak by simple `ls`.

In-place sanitization is reserved for small-scale cases where the value-to-risk ratio is clearly favorable (e.g., rewording a single F-mode field whose substance is corpus-real but whose expression smuggled in an architectural commitment).

## Alternatives considered

- **Move to a `*-superseded/` directory with index.** Rejected per user veto: moved-but-visible directories advertise the artifacts; the curious-agent failure mode remains.
- **Pure deletion (no reference doc).** Rejected: loses archaeological access. The artifacts retain genuine historical value for a future human reviewer who wants to understand what the original contamination looked like.
- **In-place sanitization for all 16 artifacts.** Rejected at this scale: rewriting 16 multi-page documents while preserving substance and removing bias is too error-prone; would produce ambiguous results that themselves require audit.
- **Move to git-archive branch / orphan branch.** Rejected: adds branch-management complexity; the permalink approach achieves the same archaeological-access goal using existing git history.

## Consequences

What becomes easier: the next session opens to a tree that contains no contamination-bearing artifacts at all. The curious-agent failure mode is mechanically prevented (the agent cannot read what does not exist in the live tree).

What becomes harder: archaeological retrieval requires a `git show <commit>:<path>` command instead of a simple file read. A human reviewer who wants to skim multiple contaminated artifacts must run multiple git commands. The reference doc itself must be kept current (its commit-hash permalinks become stale if the underlying commits are ever rebased).

Trade-off knowingly accepted: archaeological access has one extra friction step. The benefit is that the active tree is provably clean.

## References

- [`../2026-05-24-128.md`](../2026-05-24-128.md) — the source retrospective.
- [`./SKILL-SPEC-edcdfe6ec1-contamination-permalink-archival.md`](./SKILL-SPEC-edcdfe6ec1-contamination-permalink-archival.md) — the skill spec that operationalizes this pattern.
- [`./AGENTS-MD-ffde776858-permalink-with-guard-for-archived-do-not-read-artifacts.md`](./AGENTS-MD-ffde776858-permalink-with-guard-for-archived-do-not-read-artifacts.md) — the AGENTS.md rule.
- Live example: [`architectures/v3/history/HISTORICAL-RECORD.md`](../../architectures/v3/history/HISTORICAL-RECORD.md) at the time this ADR was drafted.
- PR #128 — Phase-2 cleanup where the pattern was developed and applied.
