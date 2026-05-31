# Adversarial review — C34 Holdout integrity & isolation enforcement (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Evaluation & Judge / holdout-integrity
Target: spec/C34-holdout-integrity.md (+ plan-faithful/C34-holdout-integrity.md)
Charter: single canonical track. Track-A posture in force — attack **fidelity + completeness**, NOT
the design — **plus** the capability-for-principle bar ([`HANDOFF.md`](../_meta/HANDOFF.md) §2,
[`SURVIVOR-PASS.md`](../_meta/SURVIVOR-PASS.md)). The KEPT minimal capability for C34 is the **"custom,
small" read-audit + the judge↔worker independence check**; OPA / Rego / custom-MAC / a model-family-
difference enforcer are over-build candidates (SURVIVOR-PASS C42-06 "no OPA in scope"; D-1→FE-1).

## Findings

### RC34-01 — major — §2 dependency table conflates C35 (override/why loop) with C57 (residual-risk register); the residual register is C57's, not C35's
**Claim.** §2 table row reads "Downstream (override / why loop) | **C35** Override → why loop ·
**residual-risk register** | … A holdout-leak or independence-violation finding is a candidate for the
override/why discipline **and the residual-risk register** (so 'held-out' is not over-trusted, G10)."
The same conflation recurs in §1's "residual-risk register" mentions tied to C35's row, §5 "publish time"
(C35 + register lumped), §6 G10 ("C34's status feed carries this caveat to the residual-risk register"
without naming the owner), and §8.5/§8.7.
**Evidence.** Inventory: **C35** = "Override → pattern → rule loop … Hooks detect operator overrides …
convert to new validation rules" — it is *not* the residual-risk register. The **residual-risk register**
is **C57** ("Failure-mode coverage map & residual-risk register … owns … the honest residual/caution
register"). The **plan gets this right** — it consistently routes the findings feed to "C33 / C35
(override/why) / **C57** (residual register)" (plan T4, §2 graph, M4/M5, §5, §6). So the spec's §2 table
mis-attributes C57's register to C35, contradicting both the inventory and its own plan. This is a
fidelity (mis-cited owner) error, not a design call.
**Fix (applied).** Split the conflated row: C35 row scoped to the **override/why loop** only; added a
distinct **C57 — residual-risk register** downstream row; and re-pointed the §1/§5/§6/§8 "residual-risk
register" mentions to **C57** (matching the plan). C35 still receives the finding as an override/why
candidate; C57 is the register owner that must carry the G10 "do not over-trust 'held-out'" caveat.

### RC34-02 — minor — §6 F1/F27/F46 row asserts v4 "attributes these to cross-family enforcement"; F-MODE attributes them to independence/diversity broadly, and the row over-claims a single v4 mechanism
**Claim.** §6 row F1/F27/F46: "v4 attributes these to *cross-family* enforcement; per **D-1** cross-family
is relaxed (FE-1), so C34 delivers the independence these rely on via rig/role/prompt isolation."
**Evidence.** F-MODE-COVERAGE §1 lists F27 "Circularity / same-model build+validate" and F46 "Single-model
review blindspot" as resting on judge **independence / a different reviewer**, of which cross-family is the
v4-named *mechanism* but not the only framing (F48's mechanism is "Cross-family judge **+ independence
auditor**" — independence is a separate lever). Saying v4 "attributes these to cross-family enforcement"
slightly overstates: the underlying need is *independence*, which v4 proposes to satisfy partly by
cross-family. The substance of the row (C34 delivers independence by isolation per D-1; the model-family
residual is FE-1) is correct and faithful; only the attribution clause is too strong.
**Fix (applied).** Softened "v4 attributes these to cross-family enforcement" to "v4's named mechanism for
the independence these rest on is partly cross-family enforcement (F48 pairs it with an independence
auditor)", so the row does not assert cross-family is the sole v4 framing while keeping the D-1/FE-1
resolution intact.

### RC34-03 — minor — OQ-C34-1 / §6 G21 row cite both "G11" and "G21/G11" for the same substrate question; the canonical gap is G21 (G11 is the `gc`-unverified blocker it rides on)
**Claim.** §6 G21 row: "the substrate sub-question … is OQ-C34-1 / **G11**"; §9 OQ-C34-1 header:
"(G21/G11, top open question)" then "(G11)"; §8.1 "OQ-C34-1 / **G11**".
**Evidence.** The assigned gap is **G21** ("holdout-integrity enforcement has no real mechanism …
detect-after-the-fact"). **G11** is the distinct blocker "the whole plan assumes Gas City exists / no one
has run `gc`". The prevent-vs-detect substrate question *is* G21; it is *unanswerable* until G11 (a runnable
`gc`) is retired — they are related but not interchangeable. Tagging the OQ "G11" in some places and "G21"
in others is a minor mis-citation that could mislead a reader into thinking the substrate question is the
G11 availability blocker rather than the G21 enforcement-strength gap. (The plan is cleaner: it ties
OQ-C34-1 to "G21/OQ-C34-1" and the spike T7 to "G11-class `gc` availability" — keeping the two gaps
distinct.)
**Fix (applied).** Normalized the citations to **"G21 (gated on G11-class `gc` availability)"** at §6 G21
row, §8.1, and §9 OQ-C34-1, so the substrate question is consistently the G21 enforcement-strength gap that
*depends on* G11 being retired, not G11 itself.

### RC34-04 — minor — §2 "C41 / read-event source" row + §4.4/OQ-C34-2 name C41 as the read/tool-call trail provider, but C41's spec disclaims the read-event surface (it owns actor attribution, not the read trail)
**Claim.** §2 table row "Upstream (actor / read events) | **C41** Identity / actor model · event/telemetry
trail | … the read/tool-call trail (README:173 'agent reads') … C34 consumes the actor attribution + read
events." §4.4 and OQ-C34-2 likewise treat C41 as (one) source of the per-actor read trail.
**Evidence.** The faithful split (consistent with C41↔C23/C42 in the corpus) is that **C41 owns *who acted*
(`created_by` attribution)** and the **event/telemetry trail (the *reads themselves* — tool-call/filesystem
events) is C23 (event bus) / C25 (OTLP raw bodies) / CXDB**, not C41. The spec's own OQ-C34-2 actually
*lists* "Gas City event bus / OTLP raw bodies / CXDB / C41 attribution" as candidate sources — i.e., it
already knows C41 supplies *attribution* while the *read events* come from the event/telemetry trail. The
§2 row collapses these into "C41 … read events", which slightly over-assigns the read-event surface to C41.
This is a [FAITHFUL-FILL] row (already tagged as not-a-declared-edge), so it is not a hard fidelity error,
but the attribution-vs-read-trail seam should be split to match the corpus and the spec's own OQ.
**Fix (applied).** Reworded the §2 row to "**C41** supplies *actor attribution* (`created_by` — which rig
acted); the *read/tool-call events themselves* come from the event/telemetry trail (C23 event bus / C25
OTLP / CXDB), the exact source being OQ-C34-2", and made the matching §4.4 reference name C41 as the
attribution source joined to the read trail rather than the read-trail owner. Kept the [FAITHFUL-FILL] tag.

### RC34-05 — minor — §3 contract #3 / §6 F48 say the independence check verifies the judge "did not share the worker's context [window]", but OQ-C34-3 admits the predicate (incl. shared-context-window) is not yet defined; stated as a built capability it overstates sweep-1
**Claim.** §3 contract #3: the independence predicate verifies the judge "did not share the worker's
context"; §6 F48: "collusion-via-shared-*context* is caught"; §4.2 independence finding "shared
rig/prompt/partition". **Evidence.** §9 OQ-C34-3 explicitly defers the *exact* predicate — "distinct rig +
distinct prompt + partition distinct from the worker + **no shared context window** — needs definition,
including the judge's partition (… C42 OQ-C42-3)". So "no shared context window" is an *open* element of the
predicate, not a settled capability. Stating in §3/§6 that C34 *catches* shared-context collusion reads as
a frozen guarantee, while the mechanism for detecting a shared context window (vs merely distinct
rig/prompt/partition) is undefined and entangled with C42's open judge-partition question. The rig/prompt/
partition-distinctness portion is faithful and buildable; the shared-context-window portion is aspirational
at sweep 1. **Fix (applied).** Qualified the §3/§6/§4.2 wording: the sweep-1 independence predicate is
**distinct rig + distinct prompt + partition distinct from the worker**; "**no shared context window**" is
flagged as the **open element of the predicate (OQ-C34-3)**, so F48's "collusion via shared *context*"
catch is scoped to "shared rig/prompt/partition today; shared-context-window detection pending OQ-C34-3".
Keeps the D-1 independence-by-isolation story without over-promising the unspecified predicate.

### RC34-06 — minor — §6 F17 row + §1 NOT-list cite "OPA policy on shared partitions" from F-MODE §3; correctly disclaims it, but should name C04/C42 worktree isolation as the actual owner to avoid implying C34 has any F17 role
**Claim.** §6 F17 row: "Out of C34's scope (worktree isolation is C42/C04, native). Noted only because
F-MODE pairs 'OPA policy on shared partitions' with it — C34 does not build that OPA policy (dropped)."
**Evidence.** This is faithful and correct (F-MODE-COVERAGE §3 does pair F17 with "OPA policy on shared
partitions", and OPA is dropped, so the only live F17 mechanism is the native worktree isolation owned by
C42/C04). The disclaimer is right; the nit is purely that listing F17 at all in a C34 spec risks a reader
inferring C34 has a residual F17 duty. Since the row already names C42/C04 as owner and OPA as dropped, this
is the weakest finding — borderline accept-as-is. **Fix (applied, light).** Tightened the row to lead with
"**Not C34 (owner: C42/C04 worktree isolation, native).** Listed only to retire the F-MODE §3 'OPA policy
on shared partitions' pairing: OPA is dropped (SURVIVOR-PASS C42-06), so no C34 (or C42) OPA policy backs
F17", making explicit that the row's only purpose is to close out the dropped-OPA pairing, not to claim a
C34 role.

## Boundary verdict — C34 / C42 / C43 three-way split

**Crisp and faithful — verified against D-13, the inventory, and C42's spec/review.** C34 owns
**enforcement (on-disk realization of the read-isolation policy) + after-the-fact AUDIT + the judge↔worker
independence check**; **C42 PROVIDES** the partition labels / holdout invariant (`scenarios ∉
read_partition(worker)`) that C34 realizes-and-audits; **C43** owns the *distinct* lethal-trifecta
blast-radius bound (G31) that closes the residual broad-tool-access **tool-call-time** read-escape C34's
after-the-fact audit cannot itself prevent; **C30** stores the bytes. C34 does **not** absorb C43's job
(§1 "Explicitly NOT", §2, §6 F31/G31 rows are explicit and correct) and does **not** re-declare C42's
partition (§1, §2). This matches C42's own spec post-RC42-01/02 fix (C42 "provides", C34 "enforces+audits",
C43 "bounds") and the D-13 ledger entry exactly. **No boundary violation found.**

## The BAR (capability-for-principle) — verdict

**Held.** OPA/Rego is explicitly **DROPPED** throughout (§1 NOT-list, §3.1, §4.1, §4.3, §6 F17,
invariant "No-policy-engine", §8.8 acceptance, plan T4-risk/T1/T5/DoD), citing SURVIVOR-PASS C42-06 +
README:425 "later". No custom-MAC, no tool-call-time interceptor is built (explicitly routed to C43). No
model-family-difference enforcer (D-1→FE-1; §1 NOT-list, §6 G08, OQ-C34-4). The KEEP is exactly the
"custom, small" read-audit + independence check (README:173). **No over-build introduced** beyond the
KEEP — the spec actively resists all four temptations the plan §5 names.

## G-coverage (assigned: G10, G21, G08, G28)

- **G21** (detect-vs-prevent) — **surfaced as the load-bearing OQ.** The honest residual ("does `gc`
  PREVENT the out-of-partition read at tool-call time, or permit-with-detect so the audit catches after?")
  is the [AMBIGUITY: G21] block + **OQ-C34-1** (the named top OQ), with Reading A (config+perms+detect)
  picked as the faithful build and Reading B (should-be-hard-control) surfaced as named residual. Correct
  per D-13 (ownership settled; substrate fact open on G11). ✓ (citation tightened — RC34-03.)
- **G10** ("held-out" overstates the guarantee) — acknowledged; status feed carries the "verified-after-the-
  fact, not a hard guarantee" caveat to the register. ✓ (register owner corrected to C57 — RC34-01.)
- **G08** ("model family" undefined; cross-family vs single-Max) — resolved per D-1→FE-1: independence by
  isolation, family rule advisory at C29, FE-1 seam, F48 shared-training-distribution residual surfaced
  "Partial". ✓
- **G28** (several mechanisms, no authority statement) — resolved by the §4.3 one-line authority note (rig
  `read_partition` authoritative declaration / C34 realizes+verifies / C43 bounds / OPA dropped), correctly
  scoped as a note, not a composition stack. ✓ (consistent with C42's parallel §4.3.)

## Verdict

**accept-with-fixes.** Strong, faithful, and well-traced; the D-13 three-way boundary is crisp, the
capability bar is held (OPA/MAC/family-enforcer all correctly out), and G21 is honestly surfaced as the
load-bearing OQ with the prevent-vs-detect residual routed to C43. All six findings are fidelity/citation
fixes, not design changes, and all are applied: the one material one (RC34-01, C35-vs-C57 residual-register
mis-attribution) is corrected to match the inventory and the plan; the rest qualify over-stated claims
(independence-predicate completeness, C41 read-trail ownership, the cross-family attribution clause) and
normalize a G21/G11 citation. **No blockers; nothing deferred** — the architecturally-significant calls
(D-13 ownership, OPA-dropped, D-1 cross-family) are already settled by the binding decisions the spec cites
correctly.
