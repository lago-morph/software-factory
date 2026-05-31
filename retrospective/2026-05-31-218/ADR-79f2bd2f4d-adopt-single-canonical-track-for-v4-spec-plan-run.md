# ADR: Adopt single canonical track for v4 spec/plan run

- **ID**: ADR-79f2bd2f4d
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-31
- **Source retrospective**: ../2026-05-31-218.md
- **PRs covered**: #218

## Context

The v4 architecture run was originally structured as two parallel tracks (`spec-faithful/` + `plan-faithful/` rendering v4 as a fixed proof; `spec-optimized/` + `plan-optimized/` improving v4 with named DELTAs) so that adversarial agents could attack the design from both fidelity and improvement angles, and so the operator could diff the two tracks per-component before committing. The original session built 23 of 57 components on both tracks, producing 148 named DELTAs in the optimized track. Three research files — `optimized-deltas-enumeration.md` (the 148 deltas), `optimized-deltas-force-skeptic.md` (per-delta force-justification verdict), and `optimized-deltas-independence.md` (per-delta cluster/portability cost) — characterized the divergence.

This session's analysis surfaced two findings that made the parallel-track structure untenable for the remaining 34 components: (a) three of the four systemic architectural bets in the optimized track are blocked on external decisions the operator cannot force (G37 secrets store, FE-1 second-provider credential, Max ToS clarification for unattended pooling); (b) the fourth bet — substrate portability contracts (C01/C04/C21/C28-01) — was flagged by the skeptic as the weakest-justified cluster in the corpus. Continuing both tracks would therefore double the authoring cost for 34 more components while the divergent track's architectural contributions remained mostly inaccessible. The operator established a tighter capability-for-principle bar mid-session ("does this addition give us MORE capability tied to a specific 12-principle?") that further reduced the survivor count in the divergent track to 25 minimal-form deltas — all of which turned out to already be present in the canonical track in minimal form (close-read verified during the survivor-pass apply).

## Decision

The v4 spec/plan run converges to one canonical track at `architectures/v4/spec/` (formerly `spec-faithful/`) plus its build companion `plan-faithful/`; `spec-optimized/` and `plan-optimized/` become frozen reference; the four architectural bets in the optimized track are parked as FE-1..FE-4 in `_meta/FUTURE-ENHANCEMENTS.md` with explicit external triggers.

## Alternatives considered

**Continue both tracks through the remaining 34 components.** Maintains maximum exploration, gives the operator the full diffable view per component. Rejected because: (a) ~2× subagent cost per wave for 34 more components, (b) three of the four architectural bets are blocked on external decisions Track B cannot solve, so the elaborated optimized specs for the unbuilt 34 would mostly be elaborating blocked work, (c) the operator explicitly weighted scope-creep avoidance and velocity over diffability.

**Switch to optimized-only.** Adopts the four architectural bets as the operating architecture. Rejected because the same external blockers (G37, FE-1 credential, Max ToS) prevent fully shipping the optimized architecture, and the skeptic-flagged weakest cluster (portability contracts) would have been forced on the canonical track without a peer implementation to validate against.

**Broad raid (cherry-pick ~35–40 well-justified deltas into faithful).** The independence-analysis recommendation. Rejected because the operator's refined bar ("capability-for-principle, partial satisfaction by upstream stack counts") drove the survivor set from ~35–40 down to 25, and the apply phase showed 21 of 25 were already present in the canonical track — so the broad raid would have been ~85% no-ops + a small number of edits that turned out to either reverse the canonical author's deliberate decisions (3) or precede their consumers' construction (1).

## Consequences

**Easier:**
- Single authoring track for the remaining 34 components — half the subagent budget per wave.
- Tracking docs (HANDOFF, STATUS) become single-track, easier for a fresh-session agent to resume from.
- Cross-component consistency checks are simpler (only one set of specs to keep coherent).
- The operator's capability-for-principle bar applies cleanly to the single track without per-track interpretation.

**Harder:**
- Lost the per-component diffable view that would surface architectural alternatives at review time. Mitigated by `spec-optimized/` being retained as frozen reference (any reviewer can still diff a canonical spec against its optimized sibling).
- The four deferred bets are now opt-in rather than implicit (someone has to read `FUTURE-ENHANCEMENTS.md`). Mitigated by HANDOFF §6 enumerating them with triggers.

**Knowingly accepted trade-off:**
- If a future review of a canonical component spec would benefit from "show me the alternative architectural framing" (e.g., for an integration with the FE-3 signing path once G37 lands), the reviewer must read the frozen `spec-optimized/<C>.md` sibling separately. The cross-track links in the canonical specs are preserved (this is the load-bearing reason for archiving in place rather than physically moving; see companion ADR `ADR-59ece58eb9`).

## References

- [`../2026-05-31-218.md`](../2026-05-31-218.md) — the source retrospective.
- [`./SKILL-SPEC-4dd2d9475c-survivor-pass-for-track-convergence.md`](./SKILL-SPEC-4dd2d9475c-survivor-pass-for-track-convergence.md) — the survivor-pass methodology used to converge.
- [`./ADR-59ece58eb9-archive-frozen-references-in-place-rather-than-physically-moving-them.md`](./ADR-59ece58eb9-archive-frozen-references-in-place-rather-than-physically-moving-them.md) — companion decision on how the frozen tracks are archived.
- PR the decision was made in: #218.
- Survivor-pass ledger persisting the per-delta verdict: `architectures/v4/_meta/SURVIVOR-PASS.md`.
- Deferred items: `architectures/v4/_meta/FUTURE-ENHANCEMENTS.md` (FE-1..FE-5).
