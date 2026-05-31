# Adversarial review — C39 Fix-task generation & loop-closure (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Self-Healing Loop
Target: spec/C39-fix-task-loop-closure.md + plan-faithful/C39-fix-task-loop-closure.md
Charter: canonical (single) track → attack FIDELITY and COMPLETENESS only, not the design; plus the
capability-for-principle bar (flag any KEEP that is hardening-on-existing-capability rather than new
P-tied capability). Binding settled: D-1..D-17 (flag only if violated). Load-bearing check: G18/XC-3
ownership stays at the POLICY layer over C20's bounded slots; flag any C39-built convergence
loop / bead-engine / scheduler. Gaps in scope: G18, G35 only.

## Findings

### RC39-01 — minor — Body cites `attempt_no`/`max_attempts` as frozen C20 field names without the "XC-3-illustrative / C20-sweep-2-not-yet-frozen" caveat the sibling C18 spec carries
**Claim.** §3.2 contract 7, the §5 behavior diagram (`attempt_no < max_attempts?`), the §4 data-model
table, and AC3 all reference **`attempt_no`** and **`max_attempts`** as "C20's `attempt_no`" / "C20's
slot", as though those identifiers are part of C20's frozen schema. **Evidence.** C20's own spec
(`spec/C20-bead-schema.md` §3 contract 5, §4.3, §8 AC-4, OQ-C20-1) defines the boundable slots
**descriptively** — "an attempt count, a terminal-state enum (`resolved`/`escalated`/`abandoned`), and an
escalation marker" — and explicitly defers "the terminal-state enum and registry-vs-store conformance" +
"concrete JSON/TOML field schemas" to **sweep 2**. The literal names `attempt_no`/`max_attempts`/
`escalated`/`closes` originate only in the **XC-3** review-log entry (line 76) as an *illustrative*
parenthetical, not as a C20 freeze. The sibling C18 spec is careful about exactly this — its §3.1
[FAITHFUL-FILL] states "C20 has not yet frozen those exact identifiers; concrete field names are
C20-sweep-2, and `closes` is a chain-edge field rather than a counter." C39's source-banner (line 6) is
correct ("C20's **descriptive** bounded-bead slots"), but the body silently upgrades the illustrative
names to facts — a fill-as-fact mislabel of the kind Track-A review targets. No architectural error (the
*policy* over the slots is unchanged); purely a citation-precision gap. **Fix (applied).** Added a
one-line caveat at §3.2 contract 7 noting the identifiers are XC-3-illustrative, that C20 defines them
descriptively and freezes them at its sweep-2, and that C39 writes whatever C20 freezes — mirroring
C18's discipline. The values/ownership are unchanged.

### RC39-02 — minor — Mis-attribution of inventory critical-path note #2 (it is about the C20 *schema* layer, not C39)
**Claim.** §2 (Context & dependencies) read: "Per the inventory critical-path note #2, G18 makes the
bound a blocker for the self-heal tier **until C39 defines it**." **Evidence.**
`_meta/component-inventory.md` critical-path note **#2** is the **C20** entry: "**C20 Bead schema** (on
C19 bead store) — `override`/`fix_task`/`factory_build_in_progress` types are referenced by override
loop, self-heal, and bootstrap resume; **G17/G18 make this a blocker until defined**." The note frames
G18 as a blocker on **C20's schema definition**, not on C39's policy. C39 paraphrasing it as "until C39
defines it" conflates the schema-slot layer (C20, the actual subject of note #2) with the policy layer
(C39, the subject of XC-3) — a mis-cite. The substantive claim C39 wants (the self-heal tier's bound is
not complete until C39 sets the policy) is *true* and traceable to XC-3, just not to note #2.
**Fix (applied).** Reworded §2 to attribute note #2 to the C20 schema layer verbatim, then separately
state C39 closes G18's *policy* layer over those slots per XC-3 — keeping the two layers distinct and
each correctly sourced.

### RC39-03 — minor — §6 labels the F4/F7 row "Partial (F-MODE-COVERAGE §3)" but F7's source status is "Addressed"; the partiality is C39's contribution, not the mode's status
**Claim.** §6 failure-mode table groups **F4** + **F7** in one row and tags it "**Partial
(F-MODE-COVERAGE §3)**". **Evidence.** F-MODE-COVERAGE §3 rates **F4** "Partial — quality metric
definition is itself a hard problem" but rates **F7** "**Addressed**" (Healer monitors acceptance-
threshold drift; periodic baselining against signed scenarios). Citing the combined row as "Partial
(F-MODE-COVERAGE §3)" misreports F7's catalogued status. The *intended* meaning — that **C39's own
contribution** to F4/F7 is partial (it refuses `resolution` without a positive verdict but does not
baseline the acceptance bar) — is correct and defensible; only the labeling overloads the source's
status word. **Fix (applied).** Reworded the row to attribute the partiality to C39's contribution and
state the source statuses explicitly (F4 "Partial", F7 "Addressed"), clarifying that baselining is the
C30–C34/Healer duty, not C39's.

### RC39-04 — minor (no change) — README:257 literally attributes `fix_task` writing to "the diagnosis agent" (C38), not C39; C39's split is the correct one and is corroborated, but the tension is worth a sentence
**Claim.** C39 owns "fix-task generation" and cites README:257 ("**diagnosis agent writes bead of type
`fix_task`** … your work") as its mandate. **Evidence.** README:257 literally says the **diagnosis
agent** writes the `fix_task` bead — i.e. the *verbatim* text assigns it to C38, not C39. The
architecture splits this: C38's spec (`spec/C38-diagnosis-agent.md` §1 boundary) explicitly disclaims
fix-task generation ("'diagnosis agent writes bead of type `fix_task`' is the *next* node — see boundary
below … the diagnosis→C39 handoff is the seam") and routes it to C39; C39 §1/§2 takes it. So the
*architecture* is internally consistent and both specs agree — this is **not** a contradiction. The only
residual risk is that a reader checking README:257 in isolation sees "diagnosis agent" and not "C39".
C39 already frames README:257 as the "your work" fix-task-generation row and C38 hands off explicitly, so
the split is sound. **No fix applied** — flagging for the record that the C38/C39 boundary rests on an
inferred decomposition of one README row (the row names the *Healer* writing the bead; the architecture
assigns the *write* to C39 and the *diagnosis* to C38). Both sibling specs are mutually consistent; the
decomposition is the minimal faithful reading. Left as-is.

### RC39-05 — minor (no change) — `created_by`/C41 is a T1 prerequisite in the plan and a §3.2 contract field, but C41 is not a hard inventory dependency; correctly handled as ambient
**Claim.** Plan T1 lists **C41** as a prereq and spec §3.2 contract 5 requires every fix/resolution bead
carry `created_by` (C41), yet the inventory deps for C39 are only **C38, C20, C08**. **Evidence.** P9
makes `created_by` "automatic everywhere" (AI-CONTEXT §3.1 row 9 "automatic everywhere"; README P9), and
C20's invariant already mandates "every bead carries `created_by`". So C41 is an **ambient identity
layer**, not a control dependency — C39 "supplies the actor context" and C41 stamps. The spec §2 deps
table correctly omits C41 from the hard-dependency rows and §4 lists it only as the attribution owner.
Listing C41 as a T1 prereq in the plan is defensible (the bead C39 writes must carry `created_by`) and
does not contradict the inventory (which lists *control* deps). **No fix** — consistent as written.

## Verdict
**accept-with-fixes.** Strong, faithful, and tightly scoped. The **load-bearing G18/XC-3 ownership check
passes cleanly**: C39 keeps itself at the *policy* layer (N-attempts→escalate, F52 oscillation detection,
L5 ship-authorization) over C20's bounded slots, consuming C18's **bound-reached** signal and injecting
the per-pass bound C18 enforces — and it explicitly disclaims the convergence loop/scheduler (C18), the
bead schema/slots (C20), the dispatcher (C05), the durable engine (C40), the detector/clusterer/diagnoser
(C36/C37/C38), the verdict engine (C30–C33), the autonomy ladder (C56), and any bespoke OPA-equivalent
governance engine. **No C39-built loop / bead-engine / scheduler exists** anywhere in spec or plan
(plan T2 disclaims it verbatim; the §5 "generate next attempt" edge re-enters via C05/C18, it does not
re-implement convergence). The capability-for-principle bar holds: the three KEEPs (termination/escalation
contract, diagnosis→fix_task→re-entry wiring, proof-gated closure-chain) are exactly the "None/DIY/Small
custom" P11 rows v4 owns (AI-CONTEXT:332/334; README:257/259) — genuine new P11 capability, not hardening
on the existing stack. **G35** is correctly gated on the C56 autonomy level (read-only; never
self-escalated) with the multi-cycle F54 drift audit deferred to C56/C57 — not invented in C39; C56's
spec corroborates the seam. All README / AI-CONTEXT / F-MODE-COVERAGE line citations verified exact, and
the cross-component claims (C18 bound-reached + injected bound; C20 terminal-state enum
`resolved|escalated|abandoned` + closure-chain edges `diagnosed_by`/`produces`/`resolved_by`; C08 AC-5
loop-closure driver; C56 ladder ownership) all match the sibling specs. No binding decision (D-1..D-17)
violated. The four findings are pure citation-precision/labeling fixes (illustrative slot names presented
as frozen, one mis-attributed inventory note, an F7 status-word overload) plus two consistency
confirmations; **all confident fixes applied in place, nothing architectural deferred.**
