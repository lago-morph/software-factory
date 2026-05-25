# Session handoff — 2026-05-25 (Phase 3.4 closed) [SUPERSEDED]

> **Superseded by** [`SESSION-HANDOFF-2026-05-25-phase-3.5-close.md`](SESSION-HANDOFF-2026-05-25-phase-3.5-close.md) — Phase 3.5 is now closed; the next work is Phase 4. This file is preserved as the historical Phase-3.4-close handoff record but is no longer the active pickup brief.

---

This is the pickup brief for the next agent. Phase 3.4 is **closed**. The next work is Phase 3.5 (substrate-primitive buildability sketches) and synthesis-plan revision.

## Where we are

**Phase 3.4 is closed.** All four Tier-1 decisions resolved:

| Decision | Status | Detail |
|---|---|---|
| DEC-1 (unification verdict) | **RESOLVED (three sub-confirmations)** | [`phase-3.4-decisions-resolved.md` § DEC-1](phase-3.4-decisions-resolved.md#dec-1--unification-verdict-resolved-reframed-into-three-sub-confirmations) |
| DEC-2 (cognitive escrow placement) | **RESOLVED: methodology layer** | [`phase-3.4-decisions-resolved.md` § DEC-2](phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology) |
| DEC-3 (greenfield methodology shape) | **RESOLVED: carry GF-C / GF-M / GF-S** | [`phase-3.4-decisions-resolved.md` § DEC-3](phase-3.4-decisions-resolved.md#dec-3--greenfield-methodology-shape-carry-all-defensible-candidates) |
| DEC-4 (brownfield methodology shape) | **RESOLVED: carry BF-L / BF-M / BF-S** | [`phase-3.4-decisions-resolved.md` § DEC-4](phase-3.4-decisions-resolved.md#dec-4--brownfield-methodology-shape-carry-all-defensible-candidates) |

Plus three cross-cutting commitments (recorded in the same file):

- **Scoping principle** — carry forward every candidate that defended itself; do not eliminate at end-of-Phase-3.
- **Methodology-over-substrate orientation + two-part buildability rule** — methodologies drive; each substrate primitive must ship with a construction-path sketch + corpus-why.
- **Working definitions of architecture / substrate / methodology / discipline AND greenfield / brownfield (entry-mode framing)** — both definition sections are binding for the rest of the synthesis.

## What the user resolved most recently (DEC-1)

Two follow-up messages from the user after the previous handoff. Key points the next agent should internalise:

1. **DEC-1.a confirmed as hypothesis, NOT axiom.** "No methodology serves both mandates; substrates and disciplines do" is the orienting frame for Phase 4 onward, but Phase-8 lean-evals and downstream simulation can overturn it. The four unified-attempt candidates (U-A, U-B, U-C, D7-U-1) carry forward as candidate methodologies *and* as active falsifiers.

2. **DEC-1.b is N/A.** The lead agent (me) initially proposed a "GF → BF continuity matrix" Phase-4 deliverable, on the misreading that greenfield codebases eventually become brownfield. The user corrected: **greenfield/brownfield is entry-mode, not temporal.** A greenfield-born system stays greenfield as long as the same methodology governs it; brownfield is the entry mode where the system arrives as pre-existing legacy artifacts. There is no GF → BF handoff to design. The continuity matrix is withdrawn (struck through in [`candidate-registry.md`](candidate-registry.md#greenfield--brownfield-continuity--withdrawn) for traceability; resolved framing in [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md#working-definitions-greenfield-brownfield-entry-mode-framing)).

3. **Two within-greenfield hypotheses are now on record (NOT axioms).** The synthesis MUST NOT foreclose either possibility for greenfield candidates:
   - "Maintenance is just implementation as the spec grows" applies only to greenfield (brownfield methodologies may have very different answers — per-candidate question).
   - Initial-spec discovery *may* differ across greenfield's own early-vs-mature stages. Some greenfield methodologies have separate cold-start vs. steady-state regimes (GF-C, GF-M's Regime A → B); others may treat early and mature the same. **Both shapes are admissible. Don't foreclose either.**

4. **DEC-1.c confirmed.** All 10 candidates in [`candidate-registry.md`](candidate-registry.md) carry forward. User's rationale: variety and approach-from-different-directions produce richer Phase-8 pressure-testing options than any pre-narrowed set.

## What changed in this session

| File | Change |
|---|---|
| [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) | DEC-1.a/b/c resolution added; entry-mode greenfield/brownfield working definitions added; within-greenfield variation note added; Phase 3.4 marked closed. |
| [`candidate-registry.md`](candidate-registry.md) | GF→BF continuity section withdrawn (struck through with explanatory note). |
| [`decisions/dec-1-unification-verdict-reframed.md`](decisions/dec-1-unification-verdict-reframed.md) | NEW — three-sub-confirmation brief authored, then marked RESOLVED. |
| [`decisions/dec-1-unification-verdict.md`](decisions/dec-1-unification-verdict.md) | Unchanged (still bears its earlier "superseded" banner). |

## The next work — Phase 3.5 (substrate buildability)

Per the [refined two-part rule](phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive), each substrate primitive named by a surviving candidate must ship with:

1. **Construction path** — existing tools, libraries, techniques; corpus references of others who have built something in this shape; research-grade-uncertainty flag if no plausible path exists.
2. **Corpus citation for the *why*** — what problem in the corpus this primitive solves.

**A methodology-uses-this-primitive attestation is NOT required at Phase 3.5.** Orphan primitives (no current methodology claimant) are preserved as cross-pollination fuel. Methodology-to-substrate matching is deferred to a later stage.

**Suggested Phase 3.5 shape:**

1. **Enumerate** the de-duplicated union of substrate primitives across all 10 candidates. The [registry's per-candidate "Buildability owed for Phase 3.5" entries](candidate-registry.md) are the starting point — roughly 25-30 primitives after de-duplication is the lead-agent's quick estimate.
2. **Dispatch** buildability-sketch subagents (one per primitive or one per cluster of related primitives — TBD by the next agent).
3. **Per primitive, produce** a buildability sketch per the two-part rule. Flag research-grade-uncertainty primitives explicitly.
4. **Re-check the candidates.** Any candidate whose load-bearing primitive turns out to be unbuildable shrinks (loses that primitive) or — if the primitive is structurally required — self-eliminates. (The user noted that BF-L's Codebase Model is the largest defense burden; Phase 3.5 is the right surface to adjudicate it.)

The synthesis plan ([`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md)) does not yet include a Phase 3.5 section. The plan was sized for 1-3 syntheses, not 10 candidates; **the plan needs revision** to reflect the scoping principle's cascade through Phase 4/5/6/7/8 (per-candidate ADRs, per-candidate spec, per-candidate back-fill audit, per-candidate lean-eval). This revision is itself substantive work the next agent should surface to the user before doing.

## Open questions / suggestions for the next agent to surface

1. **Synthesis plan revision.** The plan needs a Phase 3.5 section and revised Phase 4-8 sections reflecting 10 candidates. Ask the user whether to revise the plan first or dispatch Phase 3.5 first. (Lead-agent recommendation: revise the plan first — it's cheap, it produces a shared map of the larger scope, and it lets the user catch any plan-shape disagreement before Phase 3.5 commits work.)

2. **Phase 3.5 dispatch shape.** Per-primitive subagents vs. per-cluster subagents. Per-cluster is more cost-efficient and surfaces overlap naturally; per-primitive is more thorough per item. Ask the user.

3. **`X_UNM_B`'s CodebaseModel finding** for unified candidates. If a unified candidate carries forward without a CodebaseModel equivalent, F21/F28/F34 remain unmitigated for the brownfield mandate. Under the new entry-mode framing, a unified candidate that handles only greenfield is just a greenfield candidate; a unified candidate that handles brownfield must address how it acquires the codebase model from legacy artifacts. Each unified-attempt candidate must articulate this in its Phase 3.5 / Phase 4 deliverables.

4. **DEC-2 ripple.** Demoting cognitive escrow from substrate to methodology means each surviving candidate must articulate its own F42/F53 mitigation. This becomes an addendum each candidate's draft must include before Phase 5/6.

5. **Phase 4 shape under the scoping principle.** Phase 4 is now: one shared-substrate inventory (with buildability per primitive from Phase 3.5); one shared-discipline inventory; per-mandate methodology candidate sets (3 GF + 3 BF + 4 unified-attempt). No GF→BF continuity matrix.

## Concrete pickup steps for the next agent

1. Read [`AGENTS.md`](../../AGENTS.md) (project conventions).
2. Read [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) — all four Tier-1 decisions plus scoping principle, working definitions, and buildability rule.
3. Read this handoff doc.
4. Read [`candidate-registry.md`](candidate-registry.md) — the 10 candidates with per-candidate defense status and buildability sketches owed.
5. Surface to the user: synthesis-plan revision question (do it first, or skip ahead to Phase 3.5?). Then proceed per the answer.

## Current git state

Branch: `claude/keen-albattani-J2C7W`
PR: [#134](https://github.com/lago-morph/software-factory/pull/134) (ready for review; CI has nothing to check on doc-only changes).

Recent commits (most recent first, after this handoff edit lands):
- this commit (DEC-1 resolution + entry-mode working definitions + continuity withdrawal + handoff rewrite)
- `f0d1a06` DEC-1 reframed brief: three sub-confirmations
- (earlier history: DEC-2/3/4 resolution + scoping principle + candidate registry)
