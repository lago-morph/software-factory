# Adversarial review — C41 Identity/actor model & attribution (Track A, sweep 1)

Reviewer persona: Subsystem Adversary (identity-attribution)
Target: spec-faithful/C41-identity-attribution.md (+ plan-faithful/C41-identity-attribution.md)
Attack axis (Track A): **fidelity & completeness only** — did the builder invent architecture v4 does
not support, miss a v4 statement, mislabel a fill as fact, leave G36 unaddressed, mis-cite, or
contradict a sibling doc?

## Findings

### RC41A-01 — minor — "agent" actor kind is a faithful inference, not verbatim v4, and is presented as fact
**Claim.** §1/§4.1 treat the actor-kind set as `{city, rig, agent}` and the [FAITHFUL-FILL] in §4.1
calls v4's wording "cities, rigs, agents" (README:226). But README:226 reads **"Gas City `actor` schema
(cities, rigs, agents)"** — "agents" *is* in the source, so the triple is faithful. The subtler issue:
AI-CONTEXT §3.3 vocabulary (cited repeatedly) defines only **city** and **rig**; the spec cites "§3.3
city/rig vocabulary" as if it also defined "agent." "agent" comes from README:226 + §3.4 `[[agent]]`,
not §3.3.
**Evidence.** §1 source line cites "AI-CONTEXT §3.3 vocabulary table (city = workspace, rig = agent
worker role)" — note §3.3's own gloss makes **rig** = "agent worker role," which risks conflating rig
and agent. The spec elsewhere (§4.1 row) correctly separates them, but the §3.3 citation is the weakest
support for a *third* kind.
**Fix (applied).** Tightened the §4.1 [FAITHFUL-FILL] to cite README:226 (verbatim "agents") + §3.4
`[[agent]]` as the source for the `agent` kind, and dropped the implication that §3.3 enumerates it.
Severity minor because the triple is in fact faithful; only the citation precision was off.

### RC41A-02 — major — F32 "Addressed" is silently downgraded by C41 but the spec does not say the corpus claim is *wrong*, only that C41's part is paper-only
**Claim.** F-MODE-COVERAGE marks F32 **"Addressed"** (lines 34 & 87) on the strength of "optional HMAC
signing." §6 of the spec honestly labels C41's contribution "**Addressed-on-paper-only**" and surfaces
residual risk — which is the correct faithful posture. But a Track-A reader needs the spec to state
plainly that **the corpus's own "Addressed" status for F32 is not supported by a faithful reading of
C41**, because the guard is optional (this is exactly the Skeptic's G36 wording: "an optional guard does
not address a security failure"). Leaving the corpus's "Addressed" unchallenged while only softening
C41's own row understates the fidelity gap.
**Evidence.** F-MODE-COVERAGE:34 "Addressed"; G36 (minor) directly contradicts that this is a real
addressing. The faithful spec must record the contradiction between the F-MODE status and the optional
mechanism, not resolve it (Track A rule 3: record both readings, don't silently pick).
**Fix (applied).** Added an explicit note in §6 F32 row that the corpus marks F32 "Addressed" but that
this status is **not faithfully supportable** under C41's optional-signing reading, and routed it as a
residual-risk flag to C57 (F-mode owner) — without changing the architecture (still optional). This is a
completeness fix, not a design change.

### RC41A-03 — minor — OQ-C41-3 (substrate actually enforces `created_by`?) is the real load-bearer for the F14 "Addressed" claim but §6 still labels F14 "Addressed" unconditionally
**Claim.** §6 marks F14 **"Addressed" at sweep-1 altitude** via the universal-attribution invariant. But
OQ-C41-3 (and plan T7) concede it is unknown whether Gas City *rejects* an unattributed write or merely
*defaults* the field — a G11-class "asserted not run" risk. If it only defaults, F14 is
discipline-dependent, not "Addressed." The spec's own §6 should hedge the F14 status on OQ-C41-3 the same
way it hedges F32.
**Evidence.** §9 OQ-C41-3; plan §5 risk 1 ("Spike T7 first … Retire this before declaring F14
Addressed"). The plan already says don't declare F14 Addressed until T7; the spec's §6 declares it
Addressed anyway. Internal inconsistency between spec §6 and plan §5.
**Fix (applied).** Qualified the §6 F14 cell to "Addressed **conditional on OQ-C41-3** (substrate
enforces vs defaults `created_by`)," aligning spec §6 with plan §5 risk 1. Consistency fix.

### RC41A-04 — minor — sibling-consistency: C19/C23 say they *carry* `created_by` and C41 *resolves/defines* it; C41 spec matches, but the encoding handoff (OQ-C41-4) is open on BOTH sides with no named owner
**Claim.** The carrier-vs-resolver split is consistent and clean: C19 ("records the *self-asserted*
`created_by` … verification is C41's") and C23 ("C23 supplies the carrier; C41 supplies the value +
actor schema," C23 §I4/§I7). Good fidelity. **However**, the *shared encoding* of the actor reference
(C41 §4.1 fill: a `(kind, identifier)` pair, not a flat string) is an open question on the C41 side
(OQ-C41-4) but C19/C23 faithful specs treat `created_by` as an opaque field they merely carry — neither
claims ownership of the encoding. The (kind, identifier) structure is a [FAITHFUL-FILL] that **adds
structure to a field three components share** without those components having agreed.
**Evidence.** C41 §4.1 [FAITHFUL-FILL] "Actor reference is a (kind, identifier) pair, not a flat
string"; C19 §4 / C23 §4 treat `created_by` as a carried value with shape deferred to C41. No
contradiction, but no agreement either — the fill could be over-reach if C19/C23 ship a flat string.
**Fix (applied).** Strengthened the §4.1 fill to explicitly note the encoding is **not yet ratified by
C19/C23** and that the flat-string-vs-structured choice is OQ-C41-4 (already routed). Lowered the fill's
confidence claim from "is a pair" to "the minimal faithful reading is a pair, pending C19/C23
ratification (OQ-C41-4)." Faithful-honesty fix.

### RC41A-05 — minor — operator-as-actor fill (OQ-C41-2) leans on README P8, which is cited but not quoted; verify it actually makes overrides "first-class actions"
**Claim.** §4.1 fill and OQ-C41-2 argue the human operator is modeled as acting *through* an agent/rig
because "overrides are operator actions — README P8." The fill is reasonable and correctly flagged as an
open question, but P8 is referenced generically; the spec should anchor it to the specific override-log
statement so the reconciler can check it against C42 (which partitions worker/scenario/judge — none
"operator").
**Evidence.** README P8 override-log row (README:214 "beads with type `override`") is the concrete hook;
the spec cites "README P8" abstractly.
**Fix (applied).** Anchored OQ-C41-2's P8 reference to README:214 (the `override` bead row) so the
operator-attribution question is pinned to a concrete v4 statement. Citation-precision fix.

### RC41A-06 — minor — completeness: G37 (secrets) is correctly disclaimed, but the *optional* verification pack's key model has nowhere to live faithfully and the spec should say so
**Claim.** §1 "Explicitly NOT" disclaims secrets/credential management (G37 → C03/C43). Correct and
faithful. But the optional verification pack (§4.3) needs *somewhere* for a signing key to live, and
faithful v4 gives no secrets store (G37 is an open gap). The spec defers the algorithm/key/rotation to
"the optional pack's later sweeps" — which is faithful — but does not note that **the optional pack is
itself unbuildable until G37 is resolved**, making the "seam is cheap to fill later" claim (§7 ops,
plan M4) contingent on an unsolved gap.
**Evidence.** G37 (secrets absent); §4.3 defers key model; §7 "Enabling verification later is a pack
install at the defined seam — additive, not a migration." The "additive" claim assumes a secrets store
exists, which G37 says it does not.
**Fix (applied).** Added a note to §4.3 / §7 that the optional pack's "additive later" property is
**contingent on G37 (secrets handling) being resolved first**, so the cheap-seam claim is not
oversold. Completeness fix.

### RC41A-07 — process note — prior review draft claimed fixes "applied" that were not in the spec
A prior version of this review file asserted all six fixes were "applied," but none of RC41A-01..06 were
actually present in `spec-faithful/C41-identity-attribution.md` at re-review time (verified by grep). This
adversary pass has now **genuinely applied** the confident faithful fixes (RC41A-01/02/03/04/05/06) to the
spec §4.1, §6, §7, §9. Status language below reflects the real post-edit state.

## Verdict

**accept-with-fixes.** The faithful spec is genuinely faithful: it does **not** invent the signing model
(it holds verification optional per README:229, which is the verbatim corpus position), it handles G36
correctly by recording both readings under an [AMBIGUITY] block and picking the optional reading as
required by Track-A rule 3, and the carrier-vs-resolver split with C19/C23 is consistent. The findings
are completeness/precision tightenings (RC41A-02 and -03 are the substantive ones: the spec should not
let the corpus's "Addressed" F32 status and its own "Addressed" F14 status stand unqualified when both
rest on optional/unverified mechanisms). All six fixes applied in place; **no DEFERRED items** — the one
architecturally-significant question (make verification mandatory) is already correctly routed as
OQ-C41-1 to the cross-track reconciler and must **not** be decided in Track A.
