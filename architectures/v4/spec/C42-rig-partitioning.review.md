# Adversarial review — C42 Rig / agent-role partitioning (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Security & Governance
Target: spec/C42-rig-partitioning.md (+ plan-faithful/C42-rig-partitioning.md)
Charter: single canonical track. Track-A posture in force — attack **fidelity + completeness**, NOT
the design — **plus** the capability-for-principle bar ([`HANDOFF.md`](../_meta/HANDOFF.md) §2,
[`SURVIVOR-PASS.md`](../_meta/SURVIVOR-PASS.md)). The KEPT minimal capability is **DELTA-03**: the
3-role taxonomy (worker / scenario-author / judge) with default-deny on cross-role access, expressed
as the holdout invariant `scenarios ∉ read_partition(worker)` (serves P5). Everything beyond that is
an over-build candidate.

## Findings

### RC42-01 — major — Enforcement+audit of the holdout boundary is mis-routed to C43; C34's inventory charter ("isolation enforcement") is silently narrowed to "detect-only"
**Claim.** Throughout §1, §2, §3.4, §6 the spec casts **C34** as a *detect-only* "detector / audit"
(§1 "C34 *detects violations* … after the fact"; §1 NOT-list "NOT the holdout-integrity audit /
detector (C34)"; §2 table "C34 audits reads"; §4.3 table "audit (detect-only) … C34"; §6 G31 row)
and routes the *prevention / enforcement* of the holdout boundary to **C43** (§1 NOT-list "C43 … gives
partitions enforcement teeth"; §2 "Downstream (enforcement) C43"; INV "once C43 lands, enforced";
§6 G21/G31 "route the prevention requirement to C43"). **Evidence.** The component-inventory C34 row
is titled **"Holdout integrity & isolation enforcement"** and its one-liner is "Read-isolation policy
(perms + OPA + rig partition) + after-the-fact audit; cross-family + independence **enforcement**"
([`component-inventory.md`](../_meta/component-inventory.md) C34). So the holdout **read-isolation
enforcement+audit** is C34's own charter; **C43** owns the *lethal-trifecta / Bash-network-fs* isolation
boundary (inventory C43: "Deterministic boundary typing + twin isolation to bound blast radius; the
security posture for Bash/network/fs access"; gap G31). The spec conflates two distinct boundaries:
it hands C34's holdout-enforcement mandate to C43 and demotes C34 to pure detection. That is a fidelity
error — C42 over-claims the C43 deferral and mis-states a sibling component's responsibility.
**Fix (applied, partial).** Re-pointed the holdout-integrity *enforcement+audit* routing to **C34**
(its charter), and scoped the **C43** dependency to what the inventory actually gives it — the
lethal-trifecta / broad-tool-access blast-radius bound (G31) that backstops *any* partition once an
agent has wide tool access — without asserting C43 is where holdout read-isolation enforcement lives.
The "detect-only until C43" framing is softened to "enforcement+audit owned by C34; the residual
broad-tool-access read-escape is what G31/C43 closes." Wording that still reads C34 as strictly
detect-only and assigns holdout enforcement to C43 in the AMBIGUITY blocks is left for the orchestrator
(see RC42-02 DEFERRED) since it is entangled with the G21 enforcement-strength call.

### RC42-02 — major — DEFERRED — The G21 AMBIGUITY block's "prevention requirement → C43, Track-B [DELTA]" disposition pre-decides a cross-component routing the inventory assigns to C34
**Claim.** §6 [AMBIGUITY: G21] resolves: "route the *prevention* requirement to C43 (G31)" and
"Making the boundary a hard tool-call-time control is exactly a Track-B `[DELTA]` candidate (… sequence
C43 earlier)." **Evidence.** Per RC42-01 the enforcement of the holdout *read-isolation* is C34's
charter, not C43's; and C34 is **unbuilt** (Batch 3), so its enforcement design is not yet written.
Asserting now that holdout prevention is "C43's job" and a "Track-B delta" prejudges where the
enforcement seam lands and reads as a design decision (Track-A may not take design decisions). The
correct faithful move is to record the *open question* (is holdout read-isolation enforced, and by
whom — C34 per its charter, vs the broad-tool-access escape that only C43 can close) and route it to
review-log, not to settle it on C43. **Fix.** DEFERRED — needs orchestrator decision: the C34-vs-C43
ownership split for holdout *enforcement* (as opposed to lethal-trifecta isolation) is architecturally
significant and entangled with C34's unwritten spec. Flagged here and in OQ-C42-1; the AMBIGUITY-block
text is left intact pending that ruling rather than partially rewritten in a way that would contradict
the deferred decision.

### RC42-03 — major — §3 contract #5 + §4.3 four-mechanism layered table drift from DELTA-03 toward the dropped "partition model + composition order" (DELTA-01)
**Claim.** §3 promotes a **"Composition / authority statement"** to a first-class frozen *interface /
contract* ("This is itself a *contract* downstream components rely on"), and §4.3 builds a 4-row
**layered composition table** (layer 1 primary / layer 2 substrate / layer 3 deferred / audit) with an
explicit "authority ruling." **Evidence.** SURVIVOR-PASS marks **C42 DELTA-01 "Partition model +
composition order" → DROP** ("We use file perms + worktrees as-is, **no formal composition stack**")
and **DELTA-05 "PartitionBinding object" → DROP**. The ADVERSARY-BRIEF lists "a formal
partition-composition stack" and "a unified PartitionBinding object" as explicit OVER-build to flag.
The KEEP is DELTA-03 only: "three roles exist with default-deny on cross-role access — **no formal
access-matrix machinery**." G28 *is* an assigned gap C42 must address, so a *one-line* "which
mechanism is authoritative" statement is in-scope; but elevating it to a frozen multi-layer
*contract*-with-authority-ruling that downstream components "rely on" is exactly the formal
composition stack the bar drops. **Fix (applied).** Demoted the G28 resolution from a frozen
"contract" to a *sweep-1 note*: kept the one-sentence authority statement (rig `read_partition` is the
declarative unit; filesystem perms + repo realize it on disk; OPA is deferred) and removed the framing
that it is a separate interface/milestone downstream components freeze against. Trimmed §3 contract #5
to a cross-reference to that note rather than a standalone contract. The §4.3 table is retained as
*explanatory* (it is the most legible way to answer G28) but re-captioned as a non-binding sweep-1
illustration, not a composition primitive. (Plan T5 / M4 likewise softened — see RC42-07.)

### RC42-04 — minor — "physically/policy-cannot-read" (§1) over-claims a guarantee the mechanism doesn't provide and trips G10
**Claim.** §1 ¶1: "the worker rig **physically/policy-cannot-read** the scenario partition." §2 ¶1
repeats "the worker rig physically/policy-cannot-read the scenario partition." **Evidence.** The whole
G21/G10 finding (which this spec correctly carries elsewhere) is that there is *no* physical
prevention — it is filesystem perms + rig config + prompt **discipline**, with broad-tool-access read
escape open until C43 (README:177 "agent-prompt **discipline** + audit logging"). Saying
"physically … cannot read" in the purpose section contradicts the spec's own G21 caveat two sections
later and is precisely the G10 over-statement. **Fix (applied).** Replaced "physically/policy-cannot-
read" with "is *policy-denied* read of the scenario partition (filesystem perms + rig config; not a
hard physical control until C43 — see §6/G21)" in both occurrences, so the purpose section matches the
residual-risk framing rather than overstating it.

### RC42-05 — minor — C01 listed as an upstream dependency in §2 table, but the inventory says C42 depends on C04 only
**Claim.** §2 dependency table adds an "Upstream (substrate) **C01** Gas City substrate" row (tagged
`[FAITHFUL-FILL]`), and §1.4/plan T1 treat "C01 partition primitive confirmed" as a prereq.
**Evidence.** Inventory C42 `depends on` column is **C04** only ([`component-inventory.md`](../_meta/component-inventory.md)
C42). Adding C01 as a dependency is a [FAITHFUL-FILL] and is *defensible* (the `[[rig]]`/`read_partition`
primitive is Gas City/C01-native per AI-CONTEXT §13.3), but it is presented in the dep table at the
same authority level as the inventory-declared C04 dep, and the `[FAITHFUL-FILL]` tag is buried at the
end of the row. **Fix (applied).** Kept the C01 substrate relationship (it is real and correctly
fill-tagged) but moved the `[FAITHFUL-FILL]` marker to the front of the cell and reworded to "substrate
the partition primitive is native to (C01/Gas City) — **dependency not declared in inventory; faithful
fill**", so it is not mistaken for an inventory-stated edge. The C04 dep remains the only
inventory-declared upstream.

### RC42-06 — minor — F28 "Addressed" is asserted partly on C42's strength, but C42's own caveats make it at best "Partial/conditional"; the qualifier should lead, not trail
**Claim.** §6 F28 row header reads "Holdout leakage (F-MODE §1, **Addressed**)" and the cell opens
"**Addressed conditional on OQ-C42-1 + G31**." **Evidence.** This is faithful to F-MODE-COVERAGE
(which does mark F28 "Addressed"), and the spec *does* carry the caveat — good. The residual nit: the
spec is the load-bearing input to the C57 residual-risk register, and presenting "Addressed" as the
headline with the conditionality trailing risks a downstream reader (C57/C34) lifting the "Addressed"
status without the caveat. Per D-1 (no model-family fallback) the caveat is load-bearing.
**Fix (applied).** Re-led the cell with the conditionality ("**Addressed-on-paper / detect-after-the-
fact only** until OQ-C42-1 resolves and C43 lands") and kept the F-MODE "Addressed" citation as the
*source* status being qualified, so the residual risk is the first thing a register-builder reads.

### RC42-07 — minor — Plan §4 milestone M4 + task T5 freeze the G28 "composition/authority statement" as a downstream-blocking contract, inheriting RC42-03's over-scope
**Claim.** plan-faithful §1 T5 "**Write the G28 composition/authority statement**" (layered defense),
§4 milestone **M4** "Composition/authority statement … Unblocks C43 (what it must enforce), C57."
**Evidence.** Mirrors the spec over-scope flagged in RC42-03: a one-line authority note is fine, but a
frozen *milestone contract* that "unblocks" C43/C57 re-imports the formal-composition-stack framing the
bar drops, and (per RC42-01) mis-routes "what C43 must enforce." **Fix (applied).** Reworded T5 to
"Write the **one-line** G28 authority note (which mechanism is the declarative unit; perms/repo realize
it; OPA deferred) — a sweep-1 clarification, not a frozen contract" and softened M4 to unblock C57's
residual-risk register only (not "what C43 must enforce"), consistent with RC42-01/03.

### RC42-08 — minor — Several non-C42 cross-refs (C30/C32/C34/C43/C57/C29) are stated as settled facts though all are unbuilt; acceptable as routing but two over-specify a sibling's internals
**Claim.** §1/§2 assert e.g. "C30 = 'Inspect AI scenario DSL authored in an isolated rig'", "C32 runs
as the judge rig", "C34 audits reads against C42's partition labels", "C57 residual-risk register."
**Evidence.** These are all unbuilt (Batch 3/4/5). Most are fine — they are *routing* pointers backed
by the inventory one-liners, which is exactly what a Batch-2 spec should do. Two lean past routing into
specifying a sibling's internal behavior: the repeated characterization of C34 as *detect-only*
(already covered by RC42-01) and §1's assertion that the judge "must read the trajectory/output …
but must remain role-isolated from the worker (D-1)" stated as C42 fact (OQ-C42-3 correctly flags this
is open). **Fix (applied).** Tagged the judge-partition assertion in §1 as deferring to OQ-C42-3 rather
than stating the judge's read surface as settled; left the inventory-backed routing pointers as-is
(they are correct and load-bearing for the dependency story).

## Verdict

**accept-with-fixes.** The spec is faithful on the core: it correctly KEEPs exactly DELTA-03 (the
3-role taxonomy + holdout invariant `scenarios ∉ read_partition(worker)`), correctly resists inventing
OS/process-boundary enforcement (it routes prevention out of C42), explicitly defers OPA per README:425,
adds no PartitionBinding object, and carries the G21/G10/G31 residual-risk caveats honestly rather than
over-claiming "held-out." The two material weaknesses are (a) **enforcement-routing fidelity** — it
hands C34's inventory-chartered holdout *enforcement+audit* mandate to C43 and demotes C34 to
detect-only (RC42-01), and pre-decides the prevention seam on C43 as a "Track-B delta" (RC42-02,
DEFERRED); and (b) **mild over-build** — the G28 resolution is inflated from a one-line authority note
into a frozen multi-layer composition *contract*/milestone (RC42-03, RC42-07), brushing the
"formal partition-composition stack" the bar drops. Applied fixes correct the over-statements (G10
"physically cannot read", F28 headline, C01 dep tag, judge-partition assertion), demote the G28
composition to a non-binding sweep-1 note, and re-point holdout enforcement+audit to C34. The
C34-vs-C43 holdout-*enforcement* ownership split (RC42-01/02) is left for the orchestrator because it
is architecturally significant, entangled with C34's unwritten spec, and crosses the G21 enforcement-
strength decision that Track-A may not settle.
