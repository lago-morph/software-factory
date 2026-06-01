# Spec: `inventory-backbone-closure`

- **ID**: SKILL-SPEC-45a01d510b
- **Source retrospective**: ../2026-06-01-225.md

## Intent

Given an architecture documented as a component inventory with a "Depends on" column, compute the **minimal backbone** — the smallest set of components needed to reach a chosen *capability milestone* — and present it honestly as concentric rings rather than a single flat list. This session needed exactly this: "what is the most aggressive build order that gets the factory to where it can safely build itself?" The naive answer (the existing one-line "long pole") was dangerously incomplete because it was eyeballed, not computed, and because it stopped at the dependency edges instead of asking what it takes to actually *run* the milestone. The skill turns that question into a repeatable, script-verified, adversarially-checked procedure that produces a defensible backbone plus the components it deliberately defers.

## Trigger

Activate when:
- The user asks for "the minimum / most aggressive / shortest path to <capability>", "the backbone", "the critical path to <milestone>", or "what do we actually need before we can <do X>" against a documented component/dependency set.
- A build-order or roadmap doc needs a vertical slice extracted from a breadth-first phase list.
- Direct phrases: "minimal backbone", "what's the smallest set that gets us to", "compute the closure", "what gates <component>".

Negative triggers (do **not** use):
- There is no dependency table to compute from (the inputs don't exist yet — author the inventory first).
- The user wants the *full* breadth build, not a milestone slice (that's a plain topological order, not a backbone).

## Inputs

- The component inventory / dependency table (a "Depends on" column keyed by component ID).
- The **target milestone** component(s) — the apex the backbone must reach (e.g. "first safe self-build" → `{C53 bootstrap-validation, C43 fence}`).
- Any binding decisions that split or re-scope a component (e.g. a decision that a fence's twin half defers).
- Knowledge of which edges are *spec* dependencies vs *runtime* dependencies (from the specs themselves).

## Outputs

- A closure script (kept in `/tmp` or committed if the repo wants it) that computes the transitive closure and the ring deltas.
- A backbone section in the target doc: the ring breakdown, a cluster grouping, and an explicit "what this defers" list.
- A short list of components that are *functionally* required but *not* in the edge-closure, each with the runtime justification.

## Workflow

1. **Transcribe the dependency map** from the inventory's "Depends on" column into a script (dict of id → list of deps). Break any documented cycles the way the source does (e.g. treat the substrate root's contract-deps as empty), and note each break.
2. **Compute the strict transitive closure** of the target milestone set. This is **Ring 1** (the bare graph answer).
3. **Walk the runtime story** of the milestone in prose: what has to happen, step by step, for the capability to actually execute. Name every component that story touches. Diff against Ring 1. The components the story needs but the closure omits are the **run-flow** additions → **Ring 2**. Treat any inventory edge that names only a *spec* dependency as suspect for this reason.
4. **Add the safety/trust requirements** that separate "possible" from "safe" (e.g. holdout integrity so the gate's signal can't be gamed; attribution; audit). This is **Ring 3** — the honest "minimum to *safe* <milestone>".
5. **Re-verify every ring with the script** after any change, and **recompute the count programmatically** — never carry a stated total across a membership edit.
6. **Group the backbone into implementation clusters**, keyed by *product* where possible ("adopting product X delivers components [...]"), so the staffing view distinguishes adopt-and-configure work from build-from-scratch work.
7. **Pressure-test with real adversarial + cooperative subagents** (not inline-simulated): one set attacks completeness ("what necessary component is missing?") and over-inclusion ("what can defer?"); the other independently re-derives the closure and completes the graph. Verify every structure-changing finding against its cited primary source before integrating.
8. **State what the backbone defers** explicitly, so the breadth view and the slice view reconcile.

## Concrete examples

**Example 1 — the v4 safe-self-build backbone.** Target `{C53, C43}`. Ring 1 = strict closure = 19 components. Walking the runtime story ("the factory authors a spec, *dispatches an agent*, runs the build, the held-out scenario is *run* and *judged*, a human reviews, the gate deploys") surfaced that C05 sling, C09 prompt-binding, C18 reconciler, and C31 scenario-runner were all needed but only some were edge-named → Ring 2 = 22. Adding C34 holdout (so the gate's satisfaction signal can't be gamed), C41 attribution, C23 event bus → Ring 3 = 25. Script output:
```
STRICT closure {C53,C43}: 19 ; +runflow {C05,C09,C18} -> 22 ; +safety {C23,C34,C41} -> 25
```
Two corrections came from adversarial subagents and were verified against sources: C31 required (spec/C53 AC-9 "composes C30/C31/C32/C33"), and C43 splits per decision D-20 so C44 defers (panel/VERDICT.md) — a C44→C31 swap that kept the total at 25.

**Example 2 — product-cluster grounding.** The 25 were grouped into six clusters, the largest being "adopt & configure Gas City," which one product adoption discharges: C01,C02,C03,C04,C05,C17,C18,C19,C23,C41,C42 — eleven backbone components from one install. A `Product | Components | adopt-vs-build` table made "install and configure Gas City" legible as one workstream rather than eleven tickets, and isolated the genuinely-custom rows (spec format, bead types, eval-tier authoring, fence policy, bootstrap).

## Anti-patterns

- **Eyeballing the backbone.** The pre-existing one-line "long pole" omitted C04/C05/C19/C28 because it was hand-drawn; compute the closure.
- **Stopping at the edge-closure.** Spec-dependency edges under-specify runtime needs; always walk the runtime story (step 3).
- **Inline-simulated adversaries.** Per the project's standing rule, adversarial review must be real subagent dispatches; simulated reviewers inherit the author's anchoring.
- **Trusting a subagent's structural claim unverified.** Verify against the cited source before integrating a finding that changes membership.
- **Carrying a stated count across a membership swap.** Recompute; the "obvious" net-zero swap is exactly where stale totals hide.

## Acceptance criteria

1. The strict closure, run-flow delta, and safety delta are each reproducible by a committed/inspectable script, and the document's stated counts match the script.
2. Every component in the backbone is either in the edge-closure or carries a one-line runtime justification for its functional inclusion.
3. The backbone explicitly lists what it defers, and the deferred set ∪ backbone = a partition consistent with the full inventory.
4. At least one real adversarial and one real cooperative subagent reviewed completeness, and every structure-changing finding cites a verified primary source.
5. Counts are consistent across every mention in the final document (grep-verified).

## Files this skill creates / modifies

- A closure script (e.g. `/tmp/closure.py` or a repo `scripts/` helper) — computes rings and deltas from the dependency map.
- The target build-order / dependencies document — adds the backbone rings, the cluster grouping (product-keyed where possible), and the deferred-set section.
