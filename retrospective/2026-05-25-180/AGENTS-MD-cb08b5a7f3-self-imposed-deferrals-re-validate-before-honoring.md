# agent instruction

**Self-imposed deferrals re-validate before honoring.** When an earlier decision brief established a deferral (e.g., "defer wave X to next run due to PR-cap pressure"), the deferral is a checkpoint to re-validate against actual constraints at the deferral point — not an unconditional stop. If the constraint cited in the deferral is not actually binding at the time the deferral would fire (e.g., actual PR count is 13 against a 30 cap when the deferral cited a 20-margin worry), lift the deferral and continue.

*Grounded in: auto-005 Round-2 deferred Wave 5.3 citing PR-cap risk; this run landed at 13 PRs at the deferral checkpoint with 17 PRs of margin; the deferral was honored mechanically rather than re-checked; user surfaced this as "I am very confused why you did not continue".*

# justification

auto-005 Round-1's cost-hawk reviewer made a defensible estimate at brief-write time (~20 PRs of work; 10 margin against the 30 cap) that justified the Wave-5.3 deferral. By the time the deferral checkpoint fired, the actual PR count was 13 — well under the cited concern. The lead agent honored the deferral mechanically without re-checking whether the cited constraint still applied. The subsequent extended-run delivery (Wave 5.3 in 4 sub-waves = ~4 PRs) put total at ~17, still 13 PRs of margin.

Cost of the rule: one re-check at each deferral fire-point — a mechanical 5-second operation (e.g., `gh pr list --state open | wc -l` against the autonomous-run skill's 30-PR cap, or analogous for whatever constraint was cited).

Asymmetric cost without: hours of user round-trip + delayed delivery. The user's 2026-05-25 session was structured around the deferral being honored; they would have continued same-session if asked. Treating brief-time estimates as binding at fire-time misrepresents the constraint as more rigid than the brief author intended.

The rule does NOT override hard constraints. If the deferral cited "no Wave 5.3 because Phase 6 spec must be authored first" (a structural constraint), re-validation would still confirm it's binding. The rule only lifts deferrals whose cited constraints aren't actually binding at fire-time.
