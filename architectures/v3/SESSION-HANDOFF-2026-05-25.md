# Session handoff — 2026-05-25

This is a session-state snapshot for the next agent picking up the v3 architecture-synthesis work after this session terminates.

## Where we are in the pipeline

**Phase 3.4 is in progress.** The integration brief is published at [`phase-3.4-integration-brief.md`](phase-3.4-integration-brief.md). The user is working through the Tier-1 decisions one at a time.

**Status of the 4 Tier-1 decisions:**

| Decision | Status | Reference |
|---|---|---|
| DEC-1 (unification verdict) | **PENDING** — user said "I'll get to DEC-1 in a minute" but session ended first | [`decisions/dec-1-unification-verdict.md`](decisions/dec-1-unification-verdict.md) |
| DEC-2 (cognitive escrow placement) | **RESOLVED: methodology layer** | [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) |
| DEC-3 (greenfield methodology shape) | **RESOLVED: carry all defensible candidates (GF-C, GF-M, GF-S)** | same |
| DEC-4 (brownfield methodology shape) | **RESOLVED: carry all defensible candidates (BF-L, BF-M, BF-S)** | same |

## The load-bearing reframe from the user's last message

In addition to the three decisions above, the user declared two cross-cutting orientations that affect everything downstream:

### Scoping principle (immutable per user)

**Carry forward every candidate methodology / architecture that defended itself against Phase-3.2/3.3 critique. Do not eliminate at end-of-Phase-3.** The corpus has no validated working factory; source authors have incentives; crossover synergies between candidates only emerge if candidates stay alive. Pressure-testing happens in Phase-8 lean-evals and downstream simulation, not at the Phase-3.4 checkpoint.

This is a major reframe of the integration brief's framing. The brief posed each Tier-1 decision as "pick one option" (e.g., DEC-1 options A/B/C/D, DEC-3 options A/B/C/D). Under the scoping principle, most of those decisions become "carry all options that defended themselves" rather than "pick one." DEC-3 and DEC-4 are already resolved this way (carry all); DEC-1 likely resolves similarly when the user gets to it.

### Methodology-over-substrate orientation

User: "We should be trying to find **methodologies**, not substrates. The methodologies should issue requirements for a substrate. It is incredibly unlikely that a substrate requirement will not be able to be implemented quickly on any cloud platform if it is sufficiently detailed."

**Lead-agent pushback (recorded in [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) cross-cutting section):** directionally correct, with one substantive caveat. Some primitives the corpus called "substrate" are non-commodity designed systems — `CodebaseModel` (brownfield-side, five sub-stores including symbol index, dependency-and-impact graph, runtime/telemetry view with role-based partitioning, attribution at symbol level, invariant/debt view) is the clearest example. Calling these "easy to implement on cloud" understates the design. Refined orientation: methodology drives; substrate requirements fall out per methodology; *but* when a methodology requires a primitive that is itself a designed system (not a configuration), name that primitive explicitly.

The user did not yet acknowledge this pushback before the session-handoff request. The next agent should surface the pushback to the user as part of resolving DEC-1 and beyond.

## What needs to change in prior and future work

**Prior work survives — re-framed, not invalidated.** All Phase 1, Phase 2, and Phase 3.1/3.2/3.3 artifacts stay in the repo as inputs. Phase 3.2/3.3 critiques reframe purpose: from "should this draft be demoted?" → "what must this candidate address before carrying forward?" Critiques become improvement requirements, not elimination grounds.

**Phase 4 reframes** from "shared/divergent extraction over surviving syntheses" to "substrate-requirements extraction per surviving candidate; primitive-overlap analysis as side artifact."

**Phase 5/6/7/8 each scale up** in candidate count. ADR count grows; spec count grows (one per candidate); back-fill audit per candidate; lean-eval brief per candidate.

**Downstream** of the synthesis pipeline (post-Phase-8), the user has named simulation / mock-up evaluation of candidates against each other. The scoping principle is designed to keep candidates alive for that evaluation.

## Open questions for the next agent

1. **DEC-1 resolution — user reframed; do NOT use the original DEC-1 options directly.** The original integration brief's DEC-1 ("pick one of: 1 unified arch / 2 separate archs / 2 unified candidates / defer") is superseded by the user's reframe in the final message of this session. The user's hypothesis (paraphrased):
   - There is likely **no methodology** that serves both greenfield and brownfield together.
   - But there are **substrates and disciplines/philosophy** that *do* fit both mandates.
   - The differentiator is the **methodology layer**.
   - **Greenfield → brownfield continuity matters.** Greenfield factories eventually turn into brownfield work as the codebase matures. A greenfield methodology that produces the right artifacts (specs in a particular format, etc.) makes the subsequent brownfield methodology easier — using the same principles as building the system in the first place.
   - So the reframed DEC-1 question is something like: *"What substrates and disciplines apply across both mandates? What methodology layer differs per mandate? What artifacts does a greenfield methodology need to produce to support the brownfield methodology that eventually takes over the same codebase?"*
   - The user explicitly noted: this hypothesis may be wrong; the next session may surface a single architecture (substrate + methodology + discipline) that serves both. But the hypothesis is the *starting* frame.

   **Concrete next-session work on DEC-1:**
   - Re-author [`decisions/dec-1-unification-verdict.md`](decisions/dec-1-unification-verdict.md) with the reframed question.
   - Carry **all unified-methodology candidates that defended themselves** forward into the catalog (per the scoping principle): U-A (Escrow-Graph Factory), U-B (Pace-Layered Escrow Factory), U-C (Anchor-Distance Factory), and the D7-U-1 alternative (Adversarial-Falsification Topology). These remain candidate *methodologies* in the catalog. The unification claim moves from "this architecture serves both mandates" to a more granular question per the user's hypothesis.
   - The Phase-4 work changes shape: it now produces (a) a shared-substrate inventory with buildability per primitive (regardless of which methodologies claim each primitive at this stage); (b) a shared-discipline inventory; (c) per-mandate methodology candidates; (d) explicit greenfield → brownfield continuity analysis (which greenfield methodology outputs become brownfield methodology inputs).

   **What "successfully defended itself" means concretely (per-candidate defense criterion):**

   A candidate is "carried forward" when it satisfies all three:

   (i) **Critique-finding response.** Each Phase-3.2 critique finding against the candidate is either (a) addressed by content already in the candidate's Phase-2 track, (b) addressed by content in the Phase-3.1 draft that merged the candidate's track group, or (c) noted as an open concern the candidate accepts. If (c), the candidate carries forward as a *placeholder pending defense* — preserved in the catalog but cannot proceed to Phase 5/6 until the defense is authored.

   (ii) **Buildability sketch per substrate primitive.** Per Phase 3.5 (the new sub-phase), each substrate primitive the candidate requires has a buildability sketch — construction path + corpus-why. Candidates whose primitives lack buildability sketches are placeholders pending Phase-3.5 work.

   (iii) **Corpus-grounded justification.** Each load-bearing claim cites the corpus, not just other Phase-3 artifacts.

   **Per-candidate defense status (lead-agent quick assessment for the next agent to verify):**

   - **U-A (Escrow-Graph Factory).** Largely defended after DEC-2 demotes EscrowSurface to methodology. Open: DPU-1 typed-object granularity (process-state node, many per cycle); X_UNM_B CodebaseModel gap if applied to brownfield; X_UNM_G graduation-criteria-not-measurable-across-mandates. Carries forward; defense placeholder on those three.
   - **U-B (Pace-Layered Escrow Factory).** Similar status. Pace-layer framing as methodology survives DEC-2. Open: same CodebaseModel and cross-mandate-measurability concerns; OQ-PLEF-5 (operator engagement with substrate-fired prompts is itself voluntary — now moot since escrow moves to methodology). Carries forward.
   - **U-C (Anchor-Distance Factory).** Anchor + distance estimator survives as methodology pattern. Open: F47 Goodhart on distance estimator (agents game distance scoring); distance-estimator buildability path needed at Phase 3.5. Carries forward; defense placeholder on Goodhart and buildability.
   - **D7-U-1 (Adversarial-Falsification Topology).** Falsification Commitment (FC) primitive survives as methodology pattern. Own honest concession (F42 not closed at substrate) is moot under DEC-2. Open: FC buildability path; independence-auditor recursion (who audits the auditor). Carries forward; defense placeholder on both.
   - **GF-S / GF-M / GF-C, BF-S / BF-M / BF-L (mandate-specific).** Per DEC-3/4, all six carry forward. Same defense criterion applies — Phase-3.2 persona critiques against each draft become per-candidate defense placeholders. The next session should produce a "defense status" addendum per candidate listing open critique findings.

   **DEC-1 vs Phase 4 scope split:**

   The user's reframe shifts most of what the original DEC-1 asked into Phase 4 normal work. What's *left* for the user to decide at the new DEC-1:

   - **Decision DEC-1.a: confirm the working hypothesis.** Synthesis proceeds under the user's stated hypothesis — no methodology serves both mandates; substrates and disciplines do. This is the orienting commitment for Phase 4.
   - **Decision DEC-1.b: confirm the greenfield → brownfield continuity is a primary design concern.** Phase 4 must explicitly extract which greenfield-methodology outputs become brownfield-methodology inputs. This is *not* in the original Phase-4 plan and needs the user to confirm it as additional Phase-4 scope.
   - **Decision DEC-1.c: confirm the candidate set.** The lead agent will produce a candidate list (3 greenfield + 3 brownfield + 4 unified-attempt = 10 methodology candidates) with defense status per candidate. The user confirms — or strikes any specific candidate they want removed despite the scoping principle.

   What's *no longer* a DEC-1 decision (now Phase 4 normal work):
   - Substrate-inventory extraction (with buildability per primitive, including orphans)
   - Discipline-inventory extraction
   - Methodology-candidate listing
   - Greenfield → brownfield continuity analysis (per DEC-1.b confirmation)
   - Cross-reference matrix (which methodology requires which substrate primitives)

   What's *no longer* a DEC-1 decision (now Phase 5 normal work):
   - ADRs per primitive (constrained by Phase-3.5 buildability sketches)
   - ADRs per methodology choice
   - ADRs per discipline

   What's *no longer* a DEC-1 decision (now Phase 6 normal work):
   - Architecture spec per surviving candidate
   - Mandate-fit matrix (with one row per surviving candidate)

   The new DEC-1 brief should therefore be much *shorter* than the original — three confirmations (DEC-1.a, DEC-1.b, DEC-1.c) plus the per-candidate defense-status addendum, not a binary architecture pick.

2. **`X_UNM_B`'s CodebaseModel finding** under DEC-1 multi-candidate disposition. If a unified candidate carries forward without a CodebaseModel primitive equivalent, the brownfield-critical F-modes (F21, F28, F34) remain unmitigated for that candidate. Does this disqualify it (per "successfully defended itself") or does the candidate get a CodebaseModel addition?

3. **DEC-2 ripple.** Demoting cognitive escrow from substrate primitive to methodology pattern means each surviving candidate must articulate its own F42/F53 (cognitive-escrow / voluntary-discipline-fragility) mitigation. This becomes an addendum each carrying-forward draft must include.

4. **Methodology-over-substrate reframe — user accepted, then sharpened.** The user accepted the refined "methodology drives, designed-system substrates get extra scrutiny" framing. They then sharpened it further: a substrate primitive without a construction path is handwaving. See [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) "Working definitions" + "Refined two-part rule" sections for the resulting buildability rule. Confirmed user position is recorded; the next agent does not need to re-confirm.

5. **Buildability rule applies at Phase 3.5 with a two-part test (NOT three).** The user *removed* the "methodology-justifies-substrate attestation" criterion from the Phase 3.5 buildability check. Final rule:
   - Construction path (existing tools, named techniques, prior-art references; research-grade flag if uncertain)
   - Corpus citation for the *why*

   Methodology-to-substrate matching is **deferred** to the later stage where methodologies and substrate primitives are combined. Orphan primitives (those with no current methodology claimant) are deliberately preserved through the buildability stage as cross-pollination fuel — the justification + construction path can stimulate reviewers to recognise that a primitive enables alternatives a methodology proposer hadn't considered (or had proposed in a more awkward way). At the matching stage, orphans simply don't get used by the chosen combinations, but they stay in the catalog.

6. **Phase 4 dispatch shape under the scoping principle + DEC-1 reframe.** The Phase 4 step in the synthesis plan presupposes 3 surviving syntheses. Under "carry all candidates" + the DEC-1 reframe, Phase 4 produces:
   - One shared-substrate inventory (with buildability per primitive, including orphans).
   - One shared-discipline inventory.
   - Per-mandate methodology candidate set (3 greenfield methodologies surviving from GF-S/GF-M/GF-C; 3 brownfield from BF-S/BF-M/BF-L; up-to-4 unified-mandate-attempt methodologies from U-A/U-B/U-C/D7-U-1).
   - An explicit greenfield → brownfield continuity analysis (which greenfield-methodology outputs become brownfield-methodology inputs).

   This is a different shape than the original Phase 4. The synthesis plan's Phase 4 description ([`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) §Phase-4) needs revision to match.

## Concrete pickup steps for the next agent

1. Read [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) for the recorded decisions and scoping principle.
2. Read this handoff doc.
3. Read [`phase-3.4-integration-brief.md`](phase-3.4-integration-brief.md) for the Tier-1/2/3 decision queue (knowing now that the framing should be re-interpreted per the scoping principle).
4. Read the four [`decisions/`](decisions/) briefs for the Tier-1 detail.
5. Surface to the user: confirmation request on the methodology-over-substrate pushback; confirmation that DEC-1 resolves under the scoping principle; the open questions in section above.
6. Once DEC-1 resolves, update [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md). When all four Tier-1 decisions are resolved, begin writing the post-adversarial syntheses (one per surviving candidate). This is Phase-3.4 integration proper.

## Current git state

Branch: `claude/agents-md-hook-fire-c0l3z`
PR: [#132](https://github.com/lago-morph/software-factory/pull/132)

Recent commits in order of recency:
- this commit (session handoff + DEC-2/3/4 resolution)
- `a6933e6` Tier-1 decision briefs (one file per question)
- `4e26492` primer: round-5 review fixes
- `bea6ef4` primer: round-4 review fixes
- (earlier history is the Phase 3.1/3.2/3.3 dispatch and critique work)
