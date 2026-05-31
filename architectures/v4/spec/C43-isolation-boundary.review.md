# Adversarial review — C43 Isolation & lethal-trifecta boundary (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Security & Governance (lethal-trifecta / isolation)
Target: spec/C43-isolation-boundary.md + plan-faithful/C43-isolation-boundary.md
Charter: canonical-track Adversary → attack **fidelity and completeness** (not the design), **plus** the
capability-for-principle bar (HANDOFF §2): flag any addition that is hardening on existing-stack capability
rather than new capability tied to a 12-principle. Binding decisions D-1..D-17 are SETTLED — flagged only if
violated.

Cross-checked against: spec/C34-holdout-integrity.md, spec/C42-rig-partitioning.md, spec/C44-digital-twin.md,
F-MODE-COVERAGE.md (F12/F33/F44/F51/F56/F31 rows verified verbatim), README (L152–162 P4, L193–204 P7, L468
Phase 3c verified), review-log (D-13/D-14, XC-8), ambiguities-and-gaps (G31/G35/G37).

## Findings

### RC43-01 — minor — "CaMeL pattern" / "boundary typing" phrase is over-attributed across F-MODE rows
**Claim.** §1 (L48), the Responsibilities bullet (L88), the §4.3 table (L266), and the §6 G31 AMBIGUITY (L326)
cite the phrase **"boundary typing (CaMeL pattern)"** as if it spans **F12/F33/F51** (L48) / **F12/F33** (L88,
266) / **F12/F44** (L326). **Evidence.** In F-MODE-COVERAGE the literal string **"CaMeL pattern" appears in
exactly one row — F12** (L54: "Twins reduce production exposure; boundary typing (CaMeL pattern); scenarios
use twins not production"). **F33** (L55) and **F51** (L76) say "**deterministic** boundary typing" with **no
"CaMeL"**; **F44** (L56) is "Substrate default: twins for everything; production scissors require explicit
declaration per pack" — it contains neither "boundary typing" nor "CaMeL". So the CaMeL-pattern phrase is
F12-only, and "boundary typing" as a phrase is F12-only; F33/F51 independently corroborate the *deterministic*
typing as primary guard, but not under the "CaMeL pattern" label, and F44 corroborates the scissors default,
not the typing. **Fix (applied).** Re-scoped the citations so "CaMeL pattern" is attributed to **F12** only,
and the F33/F51 support is cited as "deterministic boundary typing is the primary guard" (their actual words),
and F44 is cited only for the scissors default — no claim that F44 names "boundary typing". The substantive
reading (deterministic typing is the P4 primary guard, twins+scissors are the P7 routing) is unchanged and
sound; only the per-row attribution is tightened.

### RC43-02 — minor — C44 listed in BOTH the Upstream and Downstream rows of §2; "bidirectional at the seam" muddles the declared dep direction
**Claim.** §2's dependency table lists **C44** twice: once correctly as **"Upstream (declared dep)"** (L154,
"C43 `depends on C44`") and again as **"Downstream (binds twins) … (also a dep — bidirectional at the seam)"**
(L157). **Evidence.** The inventory edge is one-directional: **C43 `depends on C42, C44`** (component-inventory
L55); **C44 `depends on C17`** only (L56) — C44 has **no** dependency on C43. C44's own spec confirms the
direction: it lists C43 as a *consumer* and states "C43 depends on C44" (C44 §2, L89). So C44 is **strictly
upstream** of C43; calling the seam "bidirectional" and giving C44 a Downstream row risks implying a
dependency cycle that the inventory does not have. The *content* of the downstream row (the `twin` type is the
signal a surface routes to a C44 twin) is correct and useful — it is just mis-placed as a "downstream/also-a-
dep" relationship. **Fix (applied).** Removed the duplicate "Downstream (binds twins)" C44 row and folded its
one load-bearing sentence (the `twin` type is the routing signal that resolves to the C44 twin) into the
existing Upstream C44 row, and dropped the "bidirectional at the seam" gloss. C44 now appears once, as the
upstream declared dep it is. (C45 and C57 remain correctly downstream.)

### RC43-03 — minor — the third boundary type `isolated` is a FAITHFUL-FILL but the "closed set" is asserted with near-fact firmness in places that don't carry the fill tag
**Claim.** The boundary-type set **{`twin`, `isolated`, `production`}** is treated as a **closed set** and the
basis of the deterministic-typing invariant in §1, §3.1, §3 invariants, §4.1, §5, §8, and the plan (T1/M1).
**Evidence.** v4 names **`twin`/`production`** explicitly (F44 scissors default fixes that two-way split);
**`isolated` is the builder's synthesis** — correctly tagged `[FAITHFUL-FILL]` in §4.1 (L237) and openly
questioned in **OQ-C43-3** (is `isolated` just a *label* on the C42/C04 worktree boundary, or a distinct C43
sandbox — the latter would be an over-build the bar drops). That handling is good. The fidelity risk is only
that several *downstream* mentions (e.g. the §3 "Blast-radius bound" invariant, §8.3, the plan's M1 freeze)
state the three-element closed set without re-flagging that one of the three is a fill whose very existence as
a *type* (vs a label) is unresolved (OQ-C43-3). A reader could lift "closed set of three types" as a v4 fact.
**Fix (applied).** Added a one-clause back-reference at the first invariant use (§3 "Deterministic typing" /
§4.1) noting `isolated` is the faithful third type pending OQ-C43-3 (label-on-C42/C04 vs distinct sandbox), so
the closed-set framing is not read as fully v4-anchored. The closed-set *treatment* is retained (the
deterministic-typing invariant does need a closed set to be well-defined — the spec's own justification, which
is correct), just explicitly marked as resting on the fill for the third element.

### RC43-04 — minor — §6 F31 row attributes the single-adapter floor to "C29/C28" as if established; F-MODE names no owner
**Claim.** §6's F31 row (L318) says F31 is "**Adjacent (owner: C29/C28 single-adapter choice)**." **Evidence.**
F-MODE-COVERAGE's F31 row (L73) reads only "v4 uses only Claude Code via Gas City tmux runtime; floor is
well-defined and stable" — **Addressed by single-adapter choice**, naming **no component**. Assigning the
owner to C29/C28 is a reasonable faithful inference (C29 = model stylesheet / adapter floor; C28 = the agent
loop), but it is presented as settled fact, not inference. This is the same class of nit RC23A-style reviews
flag: an inferred owner stated as established. Low stakes — F31 is only listed to *disambiguate* that C43 is
the blast-radius boundary, not the adapter-floor declaration, which is the correct and important point. **Fix
(applied).** Softened to "owner: the single-adapter choice (C29/C28 adapter floor) — *not C43's mechanism*",
marking the C29/C28 attribution as the faithful read it is rather than a v4 statement. The disambiguation
(C43 ≠ adapter floor) is unchanged.

### RC43-05 — minor (examined, no change) — the "deterministic boundary typing" KEEP clears the capability-for-principle bar, but only because it is scoped as a DECLARATION, not a built control
**Claim/scrutiny.** The bar's sharpest question for a security component (HANDOFF §2; the plan itself names
this risk #2): with the **capability-grant engine DROPPED (C02-04)**, **spawn-time OS jail DROPPED (C04-05)**,
**OPA DROPPED (C42-06)**, and **`boundary_class` tags DROPPED (C41-07)** — is there any residual C43
*capability*, or is "deterministic boundary typing" just hardening/relabeling of declarations that C44's
`[[service]]` block + C02 pack config + C34's audit already carry? **Evidence / verdict.** It clears the bar,
and the spec is careful about *why*: v4 **explicitly names** "boundary typing (CaMeL pattern)" as a distinct
F12 mechanism and the "production scissors require explicit declaration per pack" default as a distinct F44
mechanism — these are a **named P4/P7 capability** (a deterministic typing/routing *declaration*) that no
single stack component provides as such. The spec repeatedly and correctly scopes the keep as a *named
deterministic declaration + the default-twin routing rule*, explicitly **not** a control plane (§1 FAITHFUL-
FILL, §3.5, §4.3 scope note, the "No-enforcement-engine" invariant), and routes the actual *prevention* to
OQ-C43-1 (does the loader reject vs permit-with-review) and the *realized bound* to C44. That is the smallest
faithful form. **No fix.** Recorded so the integrator sees the bar was applied to the load-bearing case and
the keep survives *as a declaration*; if a later sweep tries to grow C43 a runtime enforcement mechanism, that
crosses into the dropped scope (the plan's risk #2 already guards this — good).

### RC43-06 — (verification, no change) — D-13 three-way split is crisp and mutually consistent across C34/C42/C43; no absorption
**Claim/scrutiny.** The orchestrator's top ask: verify C43 **bounds** the broad-tool-access blast radius
(deterministic typing + twin-by-default routing) and does **not** absorb C34's holdout-audit or C42's
partition-provision, and that the split is crisp. **Evidence / verdict.** Verified — and it is the strongest
part of the doc. C43 §1 states "C42 PROVIDES the role partition, C34 ENFORCES+AUDITS the holdout
read-isolation, and C43 BOUNDS the broad-tool-access blast radius" and carries explicit "Explicitly NOT C34"
(holdout audit, L111–117) and "Explicitly NOT C42" (partition, L118–121) bullets. Cross-checks hold both ways:
**C34 §1/§6** says "C43 owns the Bash/network/filesystem security posture … a distinct boundary from holdout
read-isolation; C34 *detects* a leak after the fact, C43 *bounds* the escape that makes it physically
possible"; **C42 §1** says "C42 declares the partitions; C43 bounds the trifecta blast radius." The invariant
"Distinct-from-holdout (D-13)" (§3) nails it. **No fix.** D-13 is honored, not violated. **Boundary verdict:
crisp and consistent — no absorption, no contradiction.**

### RC43-07 — (verification, no change) — THE BAR drops (OPA / OS-jail / capability-grant / `boundary_class`) are all present and correctly attributed
**Claim/scrutiny.** Verify OPA, spawn-time OS jail/seccomp, capability-grant engine, and `boundary_class` tags
were DROPPED, with the keep being only the deterministic boundary-typing design. **Evidence / verdict.**
Verified across §1 FAITHFUL-FILL (L67–80), §3 "No-enforcement-engine / no-OS-jail" invariant (L213–216), the
§4.3 "(dropped)" table row (L270), §7 security, §8.7, and the plan's risk #2 + DoD "No over-build". Each drop
cites the correct ruling: capability-grant → **C02-04**, OS jail → **C04-05**, OPA → **C42-06**,
`boundary_class` → **C41-07**. The mechanical isolation is correctly attributed to the stack (C04/C42
process/worktree boundaries + C44 twins). **No fix.** The bar is applied correctly and loudly.

### RC43-08 — (verification, no change) — the aspirational-until-twins HONESTY caveat is flagged loud, not falsely claimed realized
**Claim/scrutiny.** Verify the lethal-trifecta bound is flagged **aspirational** until C44 twins land (the
Phase 0→3b exposure window / XC-8), not falsely claimed fully realized. **Evidence / verdict.** Verified and
prominent: §1 (L56–59, "Addressed on paper"), the §3 "Aspirational-until-twins" invariant (L217–220), §6 F12
leads with the caveat (L313), the [AMBIGUITY: G31] block picks **Reading A** (own the typing/routing *design*
now; realization waits on C44) with the exposure-window residual routed **loud to C57** (L334–343), §7
security, and AC §8.6 ("G31 residual-exposure caveat is discoverable"). XC-8 is cited correctly as the
"detection-only at Phase 0 / sequence-C43-earlier" decision (OQ-C43-2). The C44 sibling spec agrees from its
side (C44 §6 G31: "Until C43 lands, twins are available but isolation is detection/opt-in only"). The two
seam-halves are consistent (C43 waits on C44 for the twin to route to; C44 waits on C43 for the enforcement) —
not a contradiction. **No fix.**

### RC43-09 — (verification, no change) — prevent-vs-detect OQ surfaced and correctly mirrored to C34's OQ; G37→C03 deferred per D-14
**Claim/scrutiny.** (a) Verify C43's OQ — does the pack/`gc` loader *prevent* a production-typed surface at
load, or permit-with-review — is surfaced and mirrors C34's OQ (gated on G11). (b) Verify G37 secrets→C03 is
deferred per D-14. **Evidence / verdict.** (a) **OQ-C43-1** (L415–423) is exactly this question and explicitly
states "**Same enforcement-strength uncertainty as C34's OQ-C34-1**" and "gated on **G11**" — verified against
C34's OQ-C34-1, which is the identical prevent-vs-permit-with-detect substrate question. The §4.4 and §5
config-load-time text both route the prevent/permit choice to OQ-C43-1/G31. Correctly mirrored. (b) **G37** is
deferred to **C03** in §1's "NOT a secrets store" bullet (L135–139) and §6's G37 row (L321), both citing
**G37 (not FE-3)** per **D-14** — correct. **No fix.**

### RC43-10 — (completeness, no change) — G35 blast-radius/objective-drift split is faithful and anchored; G31/G35/G37 all covered
**Claim/scrutiny.** Verify the three assigned gaps (G31, G35, G37) are each addressed, and only those.
**Evidence / verdict.** **G31** — core gap, owned + honest residual (RC43-08). **G35** — §6 row (L320) splits
the **blast-radius** dimension (C43: twin-by-default caps what an L4/L5 agent can touch) from the
**objective-drift / fix-ship-authorization** dimension (routed to **C39 + C56 + C35** + "the audit-pack the
docs recommend"), matching the gap text (G35 names the guard as a Phase-3+ "audit pack … not built"). Faithful,
not absorbed. **G37** — deferred to C03 (RC43-09). All three covered; no out-of-scope gap pulled in. **No fix.**

## Verdict

**accept-with-fixes.** This is a strong, faithful, well-traced spec — the load-bearing asks all pass: the
**D-13 three-way split (C42 provides / C34 enforces+audits / C43 bounds) is crisp and mutually consistent**
with C34 and C42 (RC43-06); **THE BAR drops** (OPA / OS-jail / capability-grant / `boundary_class`) are all
present and correctly cited, with the keep scoped to a *deterministic typing/routing declaration*, not a
control plane (RC43-05/07); the **aspirational-until-C44 honesty caveat** is loud and routed to C57 (RC43-08);
the **prevent-vs-detect OQ** is surfaced and correctly mirrored to C34's, and **G37→C03 is deferred per D-14**
(RC43-09); and **G31/G35/G37** are all covered without scope creep (RC43-10). No blockers; nothing
architecturally significant deferred to the orchestrator. The four applied fixes are all "tighten an
over-attributed citation or a muddled dependency-direction / fill-firmness" — they do not change the design or
the readings: (RC43-01) scope "CaMeL pattern" to F12 only; (RC43-02) list C44 once as the upstream dep it is,
drop the spurious "bidirectional" downstream row; (RC43-03) mark the `isolated` third type as the
OQ-C43-3-pending fill it is at the invariant sites; (RC43-04) mark the F31 C29/C28 owner as inference.
