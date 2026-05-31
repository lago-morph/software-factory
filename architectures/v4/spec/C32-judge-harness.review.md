# Adversarial review — C32 LLM-as-judge Harness (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Evaluation & Judge
Target: spec/C32-judge-harness.md (+ plan-faithful/C32-judge-harness.md)
Charter: canonical track → attack FIDELITY and COMPLETENESS only (not the design), **plus** the
capability-for-principle bar (HANDOFF §2): flag any addition that is hardening on existing stack
capability rather than new capability tied to a 12-principle.

## Summary of attack vectors run

- **D-1** (same-provider judge; cross-family RELAXED → FE-1): verified C32 stamps the level, builds no
  cross-family / second-provider-credential machinery, does not re-assert the inventory's "different model
  family" as a hard requirement. **PASS** (see RC32-05).
- **THE BAR** (judge = Claude Code + Inspect AI scorer off-the-shelf; only KEEP = trajectory↔rubric binding
  + ScoreRecord emission; judge SECONDARY to P4 guard): verified. C32 adopts the Inspect AI scorer, authors
  no scoring engine, and the only custom glue is the binding + the typed record. The secondary-guard
  invariant (I1) is correctly grounded in F33/F51. **PASS** (no over-build found — see RC32-04).
- **D-13** (C34 enforces/audits holdout + independence; C32 is scorer, not enforcer): boundaries are clean
  and explicit (§1 NOT-list, I2, I3, AC6). **PASS**.
- **Fidelity** (mis-cited source? fill-as-fact? contradicts C29/C30/C31/C33/C34?): one genuine
  **mis-citation** found (RC32-01, major) and one **fill-as-fact / contradicts-peer-OQ** found (RC32-02,
  major). Remaining findings minor.

## Findings

### RC32-01 — major — the `judge` rig is mis-cited to AI-CONTEXT §13.3, which contains no judge rig
**Claim.** §2 (Context table, "Runs inside" row) and §7 (Security) state *"The judge runs as the **judge
rig** (role/partition isolated from the implementer, **AI-CONTEXT §13.3**)"* and *"C32 runs in the **judge
rig** (role/partition isolated, **AI-CONTEXT §13.3**)"* — citing §13.3 as the source for the judge rig.
**Evidence.** AI-CONTEXT §13.3 (L582–608, read directly) declares exactly two `[[rig]]` blocks —
`scenario_authoring` and `implementer` — plus one `inspect_eval` `[[tool]]` (`type="subprocess"`,
`work_partition = "scenarios"`). **There is no `judge` rig in §13.3**, and "judge" does not appear as a rig
name anywhere in README or AI-CONTEXT (the only rig names in the corpus are `v4-bootstrap`, `worker`,
`langfuse`, `cxdb`, `otel_collector`, `scenario_authoring`, `implementer`). The judge *role* IS grounded —
but in the **component-inventory C42 row** ("Worker/**scenario/judge** roles with read/write partitions",
mapping A22i/A22k/A22l/B85) and in **C42's own spec** (which fixes the role set `{worker/implementer,
scenario-author, judge}` as a `[FAITHFUL-FILL]`), **not** in §13.3. So §13.3 backs the *implementer /
scenario_authoring* rigs and the inspect tool — not a judge rig. Citing it as the judge rig's source
mislabels an inferred fill (sourced from the inventory/C42) as a v4 textual fact. **Fix (applied).**
Re-pointed both citations to the real source — the **inventory C42 row + spec/C42** — and demoted §13.3 to
backing only the `inspect_eval` tool node + the `scenario_authoring`/`implementer` rigs (which it does
support). The judge *role/rig* stays (it is grounded in the inventory/C42); only the source attribution was
wrong.

### RC32-02 — major — C32 asserts the judge's *partition* as settled; C42 and C34 both flag it as an OPEN question
**Claim.** I3 ("C32 reads the scenario only through the **judge rig's** partition"), AC2, the §1 interface
preconditions ("the scenario is resolvable in the **judge rig's partition**"), and the §6 G08 resolution
("a Claude Code judge in a **separate `judge` rig**") all treat the judge as having **its own distinct
partition**, asserted flatly. **Evidence.** Whether the judge is a *third partition* or instead *reads
`code` + scenario outputs role-isolated from the worker* is an **explicit open question** in the two specs
that own the partition model: **C42 OQ-C42-3** ("is the judge a third partition, or does it read `code` +
scenario *outputs* role-isolated from the worker, D-1?") and **C34 OQ-C34-3** ("the precise predicate …
including the judge's partition … Confirm with C42/C32"). C42's own context table is careful: *"The judge's
*partition* read surface — third label vs `code`+results — is **OQ-C42-3**, not settled here."* C32 instead
states it as fact in invariant I3 and acceptance AC2, contradicting the deferral posture of its own
dependencies. This over-asserts a cross-component seam C32 does not own. Note C32 *does* tag the rig
**placement** as `[FAITHFUL-FILL]` in the §2 row and §6 narrative — but the **partition-read-surface**
specifics in I3/AC2/§1 are stated without that qualifier, which is the fidelity defect. **Fix (applied).**
Qualified I3, AC2, the §1 precondition, and the §6 G08 text so the judge runs *role/prompt-isolated from the
implementer in a `judge` rig*, while the **exact judge partition read-surface (own `judge` partition vs
role-isolated read of `code`+scenario-outputs) is deferred to OQ-C42-3 / OQ-C34-3** and added as a new OQ5
in §9. C32's load-bearing claim (it reads scenarios *role-isolated*, does not hand them to the implementer,
I3) is preserved; only the unsettled *partition shape* is now deferred rather than asserted.

### RC32-03 — minor — F1/F27 marked "Addressed" while C29 (peer) marks F46 "Partial" and the F-mode doc marks F1/F27 differently than the per-component cells imply
**Claim.** §6 F-mode table marks **F1** "Addressed at v4 level; Phase-0 mechanism = L1 isolation" and
**F27** "Addressed at Phase-0 isolation level". **Evidence.** This is defensible and matches the C29 spec's
identical wording for F1/F27, and matches F-MODE-COVERAGE (F1/F27 are "Addressed" there). The minor risk is
the same one C29 already absorbs: under D-1 the same-provider judge shares the coder's training
distribution, so calling F27 (circularity / same-model build+validate) "Addressed" is *stronger* than the
underlying mechanism (rig/role/prompt isolation bounds **context** sharing, not **distribution** sharing —
the residual the spec itself acknowledges for F48). C32 already flags this honestly for F48 (Partial) and in
OQ1, so the table is internally consistent — but the F27 "Addressed" cell would read more faithfully as
"Addressed at the Phase-0 **isolation** level; distribution-sharing residual = F48/FE-1," mirroring how it
already qualifies F46. **Fix (applied).** Added the "(isolation level; distribution-sharing residual →
F48/FE-1)" qualifier to the F27 cell so it does not over-read as full circularity-defeat, consistent with
the spec's own F48 caveat. Kept the "Addressed" status (it matches F-MODE-COVERAGE and the C29 peer).

### RC32-04 — minor — capability-for-principle bar: ensemble (T6 / AC4 / interface 6) is at the KEEP line; confirm it is not stack-hardening
**Claim.** The multi-judge ensemble (interface 6, §1 responsibility 4, AC4, plan T6) is presented as a C32
deliverable ("C32 owns the thin policy of requesting N judges and emitting their disagreement"). **Evidence
/ reasoning.** Under the bar (HANDOFF §2), this is *on the KEEP side but worth checking*: README:187 states
"Multi-judge ensemble | Disagreement detection across judges | **Inspect AI supports multiple scorers**;
transfusion from this pattern" — i.e. the multi-scorer *mechanism* is Inspect AI's (off-the-shelf), so C32
must **not** author ensemble machinery. The spec already says exactly this ("Inspect AI provides the
multi-scorer mechanism; C32 owns the thin policy of *requesting N judges and emitting their disagreement*").
That thin request+surface policy is genuine glue tied to P5-Ashby variety + F46, so it passes the bar — but
only as long as the *reduction* stays a thin emit (it is explicitly deferred to sweep-2, §interface 6). No
over-build at sweep-1. **Fix (applied).** Added one clause to interface 6 and T6 making explicit that the
*multi-scorer execution is Inspect AI's* and C32 authors no ensemble engine — only the request + the
disagreement field on the record — so a sweep-2 author cannot drift into building a scorer pool. Status:
KEEP confirmed, hardened against scope creep.

### RC32-05 — minor — D-1 compliance is correct; one residual over-precision in the inventory "different family" handling
**Claim.** §6 G08 block and the source header both correctly relax the inventory's "must be a different
model family" to advisory and route cross-family to FE-1. **Evidence.** This is exactly right per D-1 and
matches C29/C34. The only nit: the spec's source-header still **quotes** the inventory line "must be a
different model family than coder" inside the Source block without an inline "(RELAXED → advisory, D-1/FE-1)"
marker at the point of quotation (the relaxation is explained later in §6). A reader skimming the header
could read the quoted requirement as live. **Fix (applied).** Added an inline "(RELAXED to advisory per
D-1; cross-family = FE-1)" parenthetical at the header's quotation of the inventory line so the relaxation
travels with the quote. No semantic change — C32 already builds no cross-family machinery (T9, AC2, I2).

### RC32-06 — minor — "judge rig" partition-miss / fail-closed degraded path inherits the RC32-02 ambiguity
**Claim.** §5 degraded behavior: "If the scenario is unresolvable in the partition, scoring fails closed
(no score) rather than reaching outside the judge rig (I3)." **Evidence.** This is sound behavior, but
"outside the judge rig" again presumes the unsettled judge-partition shape (RC32-02). The *intent* —
fail-closed rather than escape role isolation — is correct and worth keeping. **Fix (applied).** Reworded to
"rather than reaching outside its role-isolated read surface (I3; exact partition = OQ5)" so the fail-closed
guarantee no longer hard-codes the deferred partition shape. Behavior unchanged.

## What was fixed in place vs deferred

**Fixed in place (all confident fidelity corrections, no architectural change):**
- RC32-01: re-cited the judge rig to the inventory-C42 row + spec/C42; §13.3 now backs only the tool node +
  scenario_authoring/implementer rigs.
- RC32-02: deferred the judge *partition read-surface* to OQ-C42-3/OQ-C34-3 (new OQ5); kept the role/prompt
  isolation claim.
- RC32-03: qualified the F27 "Addressed" cell with the distribution-sharing residual.
- RC32-04: made Inspect-AI-owns-multi-scorer explicit in interface 6 + plan T6 (scope-creep guard).
- RC32-05: inline-marked the relaxed "different family" quote in the header.
- RC32-06: de-hardcoded the deferred partition from the fail-closed degraded path.

**Deferred (needs orchestrator decision):**
- **OQ5 / RC32-02 (architecturally significant cross-component seam).** The exact judge **partition**
  (a dedicated `judge` partition vs role-isolated read of `code`+scenario-outputs) is jointly **OQ-C42-3 +
  OQ-C34-3** — it must be settled across C42/C34/C32 together, not by C32 alone. Left `DEFERRED — needs
  orchestrator decision`; C32 now matches its peers' open-question posture instead of pre-deciding it.
- **OQ2 (ScoreRecord schema)** and **OQ4 (C31↔C32 runner/scorer seam)** were already correctly flagged by
  the builder as sweep-2 cross-component freezes; verified consistent with C33 (reads judge-output beads,
  README:426) and C31 (verdict-blind, emits trajectory for C32 to score). No change needed — they are
  genuine sweep-2 contract freezes, not fidelity defects.

## Verdict

**accept-with-fixes.** The spec is faithful, well-traced, and correctly minimal: it adopts the Inspect AI
scorer off-the-shelf, keeps only the trajectory↔rubric binding + typed ScoreRecord emission as custom glue,
holds the secondary-guard (I1) and honor-don't-enforce (I2/I3, D-13) boundaries cleanly, and builds no
cross-family / second-provider machinery (D-1/FE-1). The two material fidelity defects — a mis-cited source
for the judge rig (RC32-01) and asserting-as-settled a judge-partition question its own dependencies leave
open (RC32-02) — are corrected in place by re-citation and deferral, with the one genuinely cross-component
item (the judge partition shape) left DEFERRED to the C42/C34 joint OQ. No blockers; nothing over-built.
