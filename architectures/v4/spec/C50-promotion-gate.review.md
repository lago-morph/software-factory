# Adversarial review — C50 Promotion gate (canonical track, sweep 1)

Reviewer persona: ADVERSARY / critic-fixer
Target: spec/C50-promotion-gate.md (+ plan-faithful/C50-promotion-gate.md)

Convergence posture: single canonical track; attack = FIDELITY + COMPLETENESS (not design),
PLUS the capability-for-principle bar (the keep must be new 12-principle capability, not hardening
on existing stack capability). Binding decisions in force: D-6, D-15/G09, D-19, XC-3.

## Summary

The spec and plan are unusually faithful and well-cited. Every spot-checked quotation against the
v4 corpus is exact (README:276/280/498/527/269; F-MODE-COVERAGE:63/103/174; AI-CONTEXT:286/362/516;
inventory C50/C48/C46 rows; A72/B61/B78). THE BAR is held cleanly: C50 claims only the multi-metric
+ Goodhart-guarded promotion rule + the default-flip + the recorded/reversible verdict, and
explicitly cedes significance→C48 (D-19), metric defs/cost model→C46, satisfaction recompute→C33,
variant gen→C47, replay→C49, fix-loop numeric policy→C39 (XC-3), and refuses a rollback/experiment
registry engine. The two G18-tagged gates (C50 vs C39) are correctly distinguished and the C39
spec independently confirms it OWNS the numeric termination policy. The cutline-decision-site posture
(D-15/G09) is consistent with C33 §6 and the C53 peer. Findings are dominated by one fidelity
mislabel (RC50-01) and minor citation/scoping polish. No blockers.

## Findings

### RC50-01 — (major) "Held-out(-scenario) signal" presented as a C46 guard metric alongside v4's three named metrics, unlabeled as illustrative
**Claim.** The spec repeatedly lists guard/panel metrics as "cost-per-satisfaction, time-to-threshold,
judge-FP-rate, **and a held-out(-scenario) signal**" (§1 KEEP para; §5 step 2; §6 F47 para "or a
held-out signal"; AC-6 "(e.g. cost-per-satisfaction or held-out)"). v4's named C46 meta-metric set is
exactly **cost-per-satisfaction, time-to-threshold, judge-false-positive-rate** (README:269; inventory
C46). "Held-out-scenario signal" is **not** one of C46's named metrics; it is an inference the spec
introduces while otherwise reciting the v4-named set, with no `[FAITHFUL-FILL]`/illustrative tag.
**Evidence.** README:269 "cost-per-satisfaction, time-to-threshold, judge false-positive rate";
inventory C46 identical three. The spec's §1 "(cost-per-satisfaction, time-to-threshold, judge-FP-rate)"
is faithful; the appended "held-out signal" is not sourced to C46. The *concept* (a variant overfitting
held-out scenarios should not promote — F9, F-MODE-COVERAGE:19) is sound, but F9-resistance flows through
C48's significance verdict over held-out scenario runs, not through a standing C46 "held-out" metric.
**Severity rationale.** Major (not minor): it is the genuine-KEEP paragraph and the Goodhart headline
example; presenting an un-sourced metric as if it were a v4-named one is exactly the "mislabel a fill as
fact" fidelity error the brief targets, and it could mislead the sweep-2 guard-metric freeze (OQ-1).
**Fix (APPLIED).** Re-grounded every guard-metric example to C46's three named metrics, and where the
held-out idea is genuinely useful (the F9 angle) re-expressed it as "a variant that overfits the held-out
scenarios fails C48's significance over held-out runs" rather than as a standing C46 guard metric — i.e.
held-out integrity is enforced via the C48 significance term, not invented as a fourth C46 metric. Left
one explicitly-tagged illustrative mention.

### RC50-02 — (minor) Plan §2 lists C49 under "Must precede C50", overstating a non-edge
**Claim.** plan §2 "Must precede C50" enumerates C49 ("not a direct edge; G19"). C50's inventory deps
are **C48, C12** only; C49 reaches C50 transitively via C48. Listing it under "Must precede" (even
parenthetically annotated) reads as a dependency the inventory does not assert.
**Evidence.** inventory C50 `Depends on: C48, C12`. The spec §2 table correctly rows C49 as
"consumes the result via C48; not a direct edge"; the plan is slightly looser than the spec.
**Severity.** Minor — annotation already present; risk is only a reader treating C49 as a hard C50 prereq.
**Fix (APPLIED).** Reworded the plan §2 C49 bullet to "Reaches C50 only transitively via C48 (NOT a C50
dependency edge; G19) — the hard unsolved invention the whole P12 batch waits on" so it is unambiguous
C49 is not a C50 prerequisite.

### RC50-03 — (minor) C56 autonomy-gate FAITHFUL-FILL is sound but leans on a README line whose scope is human-review-of-builds, not promotion-flip specifically
**Claim.** §1 (NOT-autonomy-ladder bullet) and §6/OQ-4 gate the default-flip on C56 using README:498
("Design review before deployment … Required until P12 is mature and trusted") and :527 (L4/L5). The
[FAITHFUL-FILL] is honestly tagged and the reasoning (don't let the self-optimizer silently re-default
the factory) is the minimal consistent reading. The only fidelity nit: README:498 is literally about
human review of *factory-built components before deployment*, not specifically the promotion-of-a-variant
flip; the spec generalizes it. This is a reasonable generalization, already FAITHFUL-FILL-tagged, and
parity with C39's C56 ship-gate (C39 §3.2 contract 7 — verified on disk) supports it.
**Evidence.** README:498/527 read; C39 §3.2 contract 7 + I4 gate ship-authorization on C56 level.
**Severity.** Minor — already tagged as fill; no overclaim of fact.
**Fix (NOT APPLIED — no change needed).** The FAITHFUL-FILL tag + the OQ-4 deferral + the C39 parity
citation are sufficient. Noted here only so the sweep-2 C50↔C56 seam freeze (OQ-4) carries the
caveat that README:498 is a build-review line generalized to the promotion-flip.

### RC50-04 — (minor) §6 G18 AMBIGUITY block cites a C33-defer chain ("C33 §6") for C50/C53/C39 — verify wording matches C33's actual reading-(b)
**Claim.** The spec leans on C33 routing the cutline to "C50/C53/C39" (C33 §6 reading (b)) in several
places (§1 I2, INV-3, §2, OQ-1). Verified: C33 §6 / INV-3 is threshold-free and explicitly names the
"satisfaction-vs-threshold gate is C50 / C53 / C39" (C33 lines 65, 73–76, 137–138). Faithful.
**Evidence.** spec/C33-satisfaction-metric.md §6 (lines 73–76): "does not own a pass/fail cutline …
the satisfaction-vs-threshold gate is C50 (promotion gate) / C53 / C39".
**Severity.** Minor — this is a confirm, not a defect. Recorded for the audit trail (no change).
**Fix (NOT APPLIED — claim verified correct).**

### RC50-05 — (minor) "G18 stated as self-healing only" tension is handled, but the ambiguities-doc framing is even stronger than the spec lets on — worth a one-line sharpening
**Claim.** ambiguities-and-gaps G18 (line 51) is framed **entirely** as the self-heal loop ("how many
fix attempts before escalation … oscillation … who authorizes a Healer-generated fix to ship at L5") and
mentions promotion **nowhere**; yet the inventory tags C50 with G18. The spec's §6 [AMBIGUITY: G18] block
already chooses reading (b) (G18 generalizes to any unbounded self-modifying loop), scopes it narrowly so
it does not collide with C39's owned numeric policy (XC-3), and justifies why it cannot be reading (a).
This is the correct, honest disposition. The only sharpening: the block could state outright that the
*ambiguities-doc text* names only the fix loop (so the C50 tag rests on the inventory + the gate-by-nature
argument, not on the gap text) — making the inference chain fully explicit.
**Evidence.** ambiguities-and-gaps:51 (no promotion language); inventory C50 Key gaps = G18; C39 spec §6
+ review-log XC-3 confirm C39 owns the numeric policy.
**Severity.** Minor — disposition is already correct and well-argued; this is transparency polish.
**Fix (APPLIED).** Added one clause to the §6 [AMBIGUITY: G18] block noting the gap *text* (ambiguities:51)
is self-heal-only, so C50's G18 tag rests on the inventory tag + C50's gate-by-nature role, with the
*numeric* fix-loop policy unambiguously C39's (XC-3) — i.e. C50 adds the promotion-loop's recorded
stopping rule and nothing of C39's.

## Verdict

**accept-with-fixes.** The spec is faithful, complete for sweep-1, and holds the capability bar cleanly;
the two G18 gates are correctly distinct (confirmed against the on-disk C39 spec + XC-3), the cutline
decision-site posture matches C33/C53, and D-19 (consumes-C48-verdict, runs-no-stats) is airtight. The
one material issue (RC50-01: an un-sourced "held-out" guard metric presented beside v4's three named C46
metrics) is fixed in place by re-grounding to C46's named set and routing the held-out/F9 concern through
the C48 significance term. Remaining findings are minor citation/scoping polish (two applied, two
no-change confirms). No architecturally-significant items deferred. No blockers.
