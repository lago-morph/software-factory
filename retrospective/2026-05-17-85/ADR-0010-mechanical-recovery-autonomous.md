# ADR 0010: Mechanical recovery is autonomous; judgment recovery is prompted

## Context

Skills and AI workflows constantly encounter "is the world in the expected state?" checks. When the answer is no, there are two responses:
1. **Ask the user before fixing** — "I noticed X is missing. Should I install it?"
2. **Fix it silently** — apply the recovery, log what was done.

Most AI workflows default to (1) for caution. But "ask the user" has real costs:
- Adds friction to every session.
- Trains the user to reflexively answer "yes" (the prompts become noise).
- Causes drift when the user is away — half-completed states accumulate.

During PR #85, the user explicitly directed: when the recovery is mechanical and deterministic (regenerate a workflow from a template), **do it without asking**. The argument: the install is recoverable (just re-run with `--force`), the template IS the source of truth, and asking serves no purpose because there's no decision to make.

But the same rule applied universally would be reckless. Some recoveries DO require user input:
- Choosing between equally-valid alternatives.
- Operations that touch user-edited content (might clobber something the user wanted).
- Irreversible operations (deletions, force-pushes to shared branches).

## Decision

**An AI workflow may perform recovery without prompting the user when ALL of the following hold:**
1. **Mechanical** — the action is deterministic; the same starting state always produces the same recovery.
2. **Recoverable** — if the action was wrong, it can be undone (or re-done) without data loss.
3. **No user-edited content at risk** — the action only touches templated/derived artifacts, not user content.

**If any of these fail, the AI MUST prompt the user before acting.**

Examples of "do it autonomously":
- Regenerate a derived file from its template (the self-syncing workflow installer, ADR 0006).
- Re-render a markdown view from a JSON source.
- Normalize an out-of-order JSON file via `jq -S`.
- Install missing CI workflows from a template.
- Recompute and update a sha256 in catalog after legitimate file edit.

Examples of "ask the user":
- Delete a record from the catalog (might lose audit trail).
- Choose between two valid category tags for an ambiguous source.
- Apply a content-merge operation that combines two files (judgment call about which content wins).
- Force-push to a branch that has open PRs from other people.
- Run `git rm` on a file in a manual drop directory when the LLM isn't certain it's a duplicate.

## Alternatives considered

- **Always ask** — safe but high-friction. Rejected per the PR #85 design conversation.
- **Always autonomous** — too risky for judgment-heavy decisions. Rejected.
- **Decide case-by-case at code-write time, no general rule** — fragmented; future skill authors won't have a consistent heuristic. Rejected; the rule above provides the heuristic.
- **Confidence-based switching** ("if model confidence > 0.9, act; else ask") — would require explicit confidence introspection that LLMs handle poorly. Rejected.

## Consequences

**Positive:**
- High-friction friction-free pattern: routine state-maintenance happens silently; the user is involved only when their judgment is needed.
- Skill authors have a clear rubric for when to add user prompts.
- The self-syncing workflows pattern (ADR 0006) is grounded in this principle.
- The audit-records flow (PR #86 follow-on) inherits the same principle: batch presentation of judgment calls; mechanical fixes auto-applied.

**Negative:**
- The "mechanical / recoverable / no user content" three-part test requires judgment to apply, which is the very thing we're trying to bypass. Mitigation: when in doubt, ask. The cost of an unnecessary prompt is small; the cost of an unnecessary destructive action is large.
- "Recoverable" is fuzzy — `git mv` is recoverable via `git reset`, but only if the user notices. Mitigation: scope "recoverable" tightly to "would `git reset --hard HEAD~1` restore the state?" — anything beyond that requires prompting.
- New users may be surprised by the AI's autonomous actions until they understand the rule. Mitigation: AGENTS.md (or the relevant skill) documents which actions are autonomous so users can audit.

## References

- [ADR 0006 — skill self-bootstrapping](./ADR-0006-skill-self-bootstrapping.md) — concrete application of this principle
- `.claude/skills/research-pipeline/SKILL.md` — pre-flight section follows the rule
- [Retrospective 2026-05-17-85, Phase 9](../2026-05-17-85.md) — user directive that produced this ADR
- AGENTS.md (Suggestion 6 in [AGENTS-suggestions.md](./AGENTS-suggestions.md)) — proposed rule for the agents file
