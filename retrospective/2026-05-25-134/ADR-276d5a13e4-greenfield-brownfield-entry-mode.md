# ADR: Greenfield and brownfield are entry-modes, not temporal phases

- **ID**: ADR-276d5a13e4
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-134.md
- **PRs covered**: #134
- **Supersedes**: [`ADR-ff2a376c34`](../2026-05-25-132/ADR-ff2a376c34-greenfield-to-brownfield-continuity.md) — that ADR was authored on a misreading of the user's framing and is now overturned. See "Context" below.

## Context

The v3 architecture synthesis has been hunting for "greenfield" and "brownfield" methodologies in parallel. Through Phases 1-3.3 the two terms were used colloquially — "starting from scratch" vs. "working with existing code" — without a binding definition. At Phase 3.4, when the user reframed DEC-1 (unification verdict), the lead agent interpreted a user remark about "greenfield → brownfield continuity" temporally: greenfield codebases mature over time and eventually become brownfield work, so a Phase-4 "continuity matrix" should map greenfield-methodology outputs to brownfield-methodology inputs. That reading was recorded in PR #132's retrospective as [`ADR-ff2a376c34`](../2026-05-25-132/ADR-ff2a376c34-greenfield-to-brownfield-continuity.md), in [`candidate-registry.md`](../../architectures/v3/candidate-registry.md), and in the session handoff.

In PR #134 the user corrected the framing. Their actual definition is **entry-mode, not temporal**: greenfield means the system *originates inside the methodology* (spec, intent, CodebaseModel-equivalents accrete as code is written); brownfield means the system *enters the methodology as pre-existing artifacts* (legacy code, docs, telemetry, with the pathologies of legacy systems). A greenfield-born system does not "become" brownfield as it matures — as long as the same methodology continues to govern it, it remains greenfield at any age or scale. The user added two within-greenfield hypotheses (recorded as hypotheses, not axioms): (a) "maintenance is just implementation as the spec grows" applies only to greenfield; (b) initial-spec discovery *may* differ across greenfield's own early-vs-mature stages, but methodologies that handle early and mature uniformly are equally admissible.

## Decision

**Greenfield and brownfield in the v3 synthesis are defined by entry-mode (how the system enters the methodology), not by temporal phase (age or maturity of the codebase).** Greenfield = system originates inside the methodology. Brownfield = system enters as pre-existing legacy artifacts. There is no GF → BF transition to design; a greenfield-born codebase stays greenfield as long as the same methodology governs it. The "GF → BF continuity matrix" proposed in [`ADR-ff2a376c34`](../2026-05-25-132/ADR-ff2a376c34-greenfield-to-brownfield-continuity.md) is withdrawn as a Phase-4 deliverable. Long-run drift concerns (F40 last-mile drift, F8 stale-knowledge) against greenfield candidates are addressed within each greenfield candidate's own methodology (steady-state regime, or whatever within-greenfield regime structure that candidate specifies), not by a cross-mandate continuity deliverable.

## Alternatives considered

- **Temporal-continuity reading (the superseded ADR-ff2a376c34).** Greenfield codebases mature and become brownfield work over time; Phase 4 should produce a continuity matrix. Rejected because the user explicitly overturned this reading: the entry-mode framing is what the user actually meant; "long-term maintenance is an inherent requirement for a greenfield project to work long-term" did not mean "greenfield becomes brownfield" — it meant maintenance is just implementation as the spec grows, under the same methodology.
- **Hybrid framing (entry-mode primary, temporal as secondary axis).** Each candidate carries an entry-mode declaration plus a "what happens at day 1800" annex. Rejected because the user explicitly said "I do not think we should treat greenfield day 180 from greenfield day 1800" — they consider this a within-greenfield methodology concern (covered by the candidate's own regime design), not a cross-cutting axis. A second axis would re-introduce the temporal framing through the back door.
- **Defer the definition to Phase 6 architecture specs.** Let each candidate define greenfield/brownfield in its own terms. Rejected because two candidates using the same term differently across the catalog produces non-comparable specs and breaks the mandate-fit matrix.

## Consequences

**Easier.** Each candidate's scope is bounded by entry-mode; the synthesis stops worrying about a "transition" that doesn't exist by definition. The candidate registry shrinks by one section (the withdrawn continuity matrix). Phase 4 has one fewer deliverable (continuity matrix removed; substrate inventory + discipline inventory + per-mandate methodology candidates remain). Long-run drift critiques (F40, F8) against greenfield candidates become per-candidate defense items, not a cross-mandate matrix.

**Harder.** Some upstream artifacts (Phase 1-3.3 outputs) implicitly assumed the temporal reading in places. A future grep pass may surface stale phrasings ("greenfield will eventually need to handle...") that need rewriting. The brownfield mandate now has a sharper edge: anything that *isn't* legacy-artifact-entry is greenfield, even if the codebase is mature — which means brownfield candidates can't use "operating an aged codebase" arguments unless the codebase actually entered as legacy.

**Accepted trade-off.** A simpler definition (entry-mode is a binary) at the cost of one upstream-rewrite pass to align stale temporal phrasings. The simpler definition is load-bearing for the rest of the synthesis (DEC-1's working hypothesis depends on it).

## References

- [`../2026-05-25-134.md`](../2026-05-25-134.md) — source retrospective.
- [`../2026-05-25-132/ADR-ff2a376c34-greenfield-to-brownfield-continuity.md`](../2026-05-25-132/ADR-ff2a376c34-greenfield-to-brownfield-continuity.md) — the superseded ADR.
- [`../../architectures/v3/phase-3.4-decisions-resolved.md`](../../architectures/v3/phase-3.4-decisions-resolved.md) — binding working definitions live here.
- [`../../architectures/v3/candidate-registry.md`](../../architectures/v3/candidate-registry.md) — has the withdrawn-continuity strikethrough section preserving audit trail.
- PRs the decision was made in: #134.