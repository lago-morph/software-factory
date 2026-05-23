# v3 Phase-0 decisions captured

**Purpose.** Durable record of user-given decisions made during the Phase-0 bias-guard review of [`00-brief-v3.md`](00-brief-v3.md). Captured immediately to disk so they cannot be lost to session-context truncation again.

**Context.** Two parallel Claude Code sessions both ran the Phase-0 bias guards (Skeptic, Naive newcomer, Historian) on the v3 brief. The other session captured user decisions in chat but did not commit them to the repo; that context was lost when the session ended. This file is the recovered + re-confirmed decision set, captured in the surviving session on 2026-05-23.

---

## D1 — Phase-2 fanout: 9 parallel tracks (3 + 3 + 3)

**Decision.** Phase 2 dispatches **9 parallel subagents**, not 6:

- **3 greenfield tracks** (substrate-first / methodology-first / cold-start-first) — as originally planned.
- **3 brownfield tracks** (substrate-first / methodology-first / legacy-ingestion-first) — as originally planned.
- **3 both-mandates tracks** (`no-axis-prescribed`) — each tasked to produce ONE architecture that addresses both mandates; each picks its own organizing axis and defends it.

**Why.** Skeptic finding #3 (skeptic-critique.md item 5): the 6-track design was structurally incapable of finding a both-mandates architecture because no track was tasked to build one. Phase-3 cross-mandate adversarial pass operating on outputs that were *not built* to be cross-mandate could not have falsified the "no single architecture works for both" hypothesis. Adding the 3 both-mandates tracks makes the hypothesis genuinely falsifiable.

**Implications.**
- Phase 3 has **3 merged drafts** to produce, not 2: `greenfield-synthesis-v1.md`, `brownfield-synthesis-v1.md`, `unified-synthesis-v1.md`.
- The cross-mandate adversarial pass shape changes: instead of 4 cross-mandate subagents (G→B advocate/attacker, B→G advocate/attacker), the unified drafts get their own adversarial pass (`unified-mandate-attacker`: "argue this architecture CANNOT work for one of the two mandates").
- Phase 4 (shared/divergent extraction) considers all three syntheses, not two.
- The Phase-2 fanout discipline: 9 subagents in a single parallel-fanout message via the [`parallel-subagent-fanout`](../../.claude/skills/parallel-subagent-fanout/SKILL.md) skill.

**No-axis-prescribed brief discipline.** Each of the 3 both-mandates subagents receives identical inputs and the explicit instruction: *"Find ONE architecture that addresses both mandates. Pick your own organizing axis — mandate is NOT required to be primary. Defend the axis choice. The other 8 tracks exist for a reason; you do not need to be comprehensive — you need to be strong on the unified case."* The three are expected to pick different axes; that divergence is the signal.

**Also resolves Skeptic #1** (whether regime/stakes/synchronicity should be primary axes alongside mandate). The 3 no-axis-prescribed tracks have explicit authorization to find them; the corpus will surface them if they're load-bearing.

---

## D2 — Mandate-fit is per-(architecture × work-unit-class), not per-architecture

**Decision.** The mandate-fit matrix in [`00-comparison-v3.md`](00-comparison-v3.md) (Phase 6.3) is a **2D matrix**: rows = architectures; columns = work-unit-classes; cells = `greenfield-fit | brownfield-fit | both | n/a`.

**Why.** Skeptic finding #7: a single per-architecture mandate-fit tag conflates the reality that one architecture may run at L4-lights-out for some work-unit-classes (e.g., regression fixes against a stable spec) and at L3-augmented for others (e.g., initial spec authoring). The 2D matrix exposes this.

**Implications.**
- Architecture spec YAML header (Phase 6) carries a richer `mandate-fit` block, not a single tag. Schema TBD in Phase-5 ADRs; lead-agent best draft:
  ```yaml
  mandate-fit:
    initial-spec: greenfield | brownfield | both | n/a
    refactor: greenfield | brownfield | both | n/a
    mvp: greenfield | brownfield | both | n/a
    post-mvp-evolution: greenfield | brownfield | both | n/a
    regression-fix: greenfield | brownfield | both | n/a
  ```
- The work-unit-class taxonomy itself is a Phase-2/3/4 decision. The initial 5-class list above is illustrative; the synthesis may produce a different cut.
- The headline matrix in [`00-comparison-v3.md`](00-comparison-v3.md) honors the user's original ask (top-level columns greenfield/brownfield) but the body shows per-(architecture × work-unit-class) detail.

---

## D3 — §4 invariants relaxed to "defaults" with per-track accept/challenge

**Decision.** Section 4 of the v3 brief renamed from *"What's invariant"* to **"Round-1/Round-2 defaults carried forward"**. Every Phase-2 track (all 9) **must mark each of the 7 items** as either:

- `accepted with justification` — track agrees this default applies in its framing; brief justification.
- `challenged` — track has corpus evidence this default does not apply (or applies only conditionally) in its framing; cite the corpus.

**Why.** Skeptic finding #4: the 'free to challenge' note in the original brief was socially costly to act on — subagents would not challenge items labelled *invariant*. Two items are particularly fragile and likely to be challenged by brownfield tracks: *"scenarios outside codebase"* (brownfield inherits scenarios FROM the codebase) and *"Agent = Model + Harness"* (graph-node and population architectures don't decompose cleanly).

**Implications.**
- Each Phase-2 track output carries an explicit `## §4 defaults: accepted vs challenged` section.
- Phase 3 merge surfaces challenges as DECISIONS-PENDING items for user review.
- Phase 4 (shared/divergent extraction) re-derives substrate primitives from scratch rather than inheriting Round-2's list.

---

## D4 — Other Phase-0 bias-guard fixes (lead-agent revision, no further user input needed)

The user authorized **"ask the rest fresh"** for items beyond the 9-track decision. These are the remaining bias-guard fixes the lead agent will apply during the brief + plan revision without further checkpoint:

### From Newcomer (vocabulary / definitional)

- Add a §0 glossary defining `lights-out`, `harness`, `scaffold`, `substrate`, `code-archaeological`, `spec-malleable`, `OpenHands V1`, `RouterLLM`, `Daemon/Triage/Patrol`, `Atelier-style`, `Refinery-style`, `docs/solutions/`.
- Inline-enumerate L0–L5 (Shapiro's Five Levels) with one-line summaries each.
- Inline-define K=5 consistency, prompt-paraphrase robustness, safety-incident severity (Jaymin's threshold metrics).
- Rename `constraints-extracted.md` constraints from `C1–C8` → `UC1–UC8` (User Constraint) to remove namespace collision with Round-2 `C10–C16`. Update all references.
- Add topic tags to every "report N" / "followup N" citation (e.g., "report 09 (Jaymin, *Agentic Engineering* harnesses & practices)").
- Add a phase map at the top of the brief with one-line description per phase.
- Add one-line gloss on each Phase-6 output (failure-mode catalog, contradictions register, etc.).
- Inline-define `mandate-fit` YAML schema allowed values.
- Define "back-fill," "adversarial pass," "persona-diverse review" inline at first use.
- Footnote numeric anchors (CodeRabbit 1.4×, Veracode 45%, METR 19%) with study population + methodology + applicability caveat.
- Footnote `OpenHands V1` numbers (sub-ms persist, 7.4ms recovery) with measurement context.

### From Historian

- **M1.** Apply ADR-0004 YAML header convention (`based-on-commit` + `based-on-date`) to every v3 artifact. Add an explicit reminder in the brief's "operating discipline" section.
- **M2.** Inherit ADR-0005 concrete-task criterion — TBD / DECISIONS-PENDING items must each name an explicit next action (who does what to which file). Mention in the brief.
- **M3.** Inherit ADR-0002 three-layer pipeline citation discipline — architecture specs cite synthesis, ADRs do not cite reports. Add explicit instruction in the brief.
- **M4.** Promote cold-start from OQ-B5 (one of six open questions) to a **mandatory dedicated synthesis section** in every greenfield Phase-2 track output.
- **M5.** Name reports 25/26/30/31 + followup/10 as required inputs to the cold-start treatment. Add to the brief.
- **M6.** Add an explicit "F36/F37 numbering collision triage is a lead-agent call, not a subagent call" line in the brief (currently in plan, missing from brief that subagents read).
- **Contamination footnote.** Add a footnote at §3 noting that "spec-malleable" and "code-archaeological + existing-architecture-as-given" are lead-agent shorthand for UC4's longer prose. Adversarial subagents should challenge the underlying claim, not the labels.

### From Skeptic (the non-architectural ones)

- **#6.** Redefine greenfield as *"the target system has no pre-existing implementation; priors from adjacent domains, exemplar projects, and operator-curated knowledge are permitted and expected"* rather than "no priors."
- **#8.** Reframe OQ-B3 from binary ("no human ever vs. no human in inner loop") to: *"What is the re-entry mechanism — what conditions cause a human to enter the inner loop, who decides, and what is the substrate-level protocol for handing back?"*
- **#10.** Flag Jaymin's thresholds as *corpus-derived recommendation, not user-mandated constraint*. Add an open question: "Which empirical bars should the lights-out architectures be required to clear, and from which source(s)?"
- **#11.** Restate the RouterLLM scope exclusion as: *"Specific provider selection is deferred to operator time, but architectures may declare provider-property requirements (diversity, long-context, vision, tool-calling latency). The RouterLLM-equivalent abstraction is itself open for challenge."*
- **#12.** Move "methodology evolution as a separate sub-architecture" out of §5 (scope-exclusion) and into the open-questions list: *"Is methodology evolution a per-architecture concern or a shared-substrate primitive?"*
- **#13.** Reword §2.1 to acknowledge: *"lights-out (as the user used the term) is not necessarily L5 (as Jaymin used the term). The tension is real only if these vocabularies map onto each other; the first task is to test the mapping."*
- **#14.** Remove the substrate enumeration from §1 (don't pre-decide Phase 4). Replace with: *"They may share substrate; which primitives are shared is determined in Phase 4, not pre-listed here."*
- **#15.** Add a §7.x explicit acknowledgment: *"Archive-and-rebuild prioritizes anchor-avoidance over insight-preservation. The back-fill audit (Phase 7) is the asymmetric mitigation, and is itself subject to recency bias. Lead agent should be especially generous toward archive items in Phase 7."*

---

## What this file does NOT change

- Anything in [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) beyond Phase 2 (9 tracks not 6) and Phase 3 (3 syntheses not 2). The phase structure (0 → 8) survives.
- Phase 0 archival sequencing (0.4–0.6 still after the 0.3 checkpoint).
- The bias-guard catalog (§3 of the plan) — persona-diverse review continues at every phase.
- The skill-extraction intent — after v3 lands, the pattern converts to a reusable skill.

---

*End of decisions-captured.md.*
