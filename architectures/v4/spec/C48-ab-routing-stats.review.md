# Adversarial review — C48 A/B routing & statistical comparison (canonical track, sweep 1)

Reviewer persona: ADVERSARY / critic-fixer (single canonical track — fidelity + completeness, not design; plus the capability-for-principle bar)
Target: spec/C48-ab-routing-stats.md + plan-faithful/C48-ab-routing-stats.md

## Method

Verified every load-bearing citation against source: README:269/273/275/276/278/320–324/470/512, AI-CONTEXT:143/286/358/360/361/364/420–422/652, F-MODE-COVERAGE F47 (63/103/174) + F60 (64). All verified accurate. Verified the binding decisions D-6/D-15/D-19 and gap G32. Cross-checked the seams against the on-disk dependency/consumer specs: C47 (variant production + `depends on C46`, no cycle), C46 (cost-model ownership / G32 / significance→C48 / no promotion), C50 (`depends on C48`; consumes the verdict; owns promotion + the multi-metric Goodhart guard), C55 (significance-consultation seam), and C33 (significance→C48 boundary). The bar (Unleash/MABWiser + scipy/statsmodels/Evidently are off-the-shelf; keep = wiring + binding + verdict contract) is correctly honored — no custom routing or stats engine is proposed, INV-5 + AC-7 + the §6 "what got DROPPED" note explicitly refuse both.

## Findings

### RC48-01 — C48 over-claims that it *routes among C55's methodology candidates* — major

**Claim.** The spec repeatedly frames C55 as a *source of a variant set that C48 routes among*, not merely a *consumer of the significance verdict*. Specifically: §1 (L42) "Given a set of candidate variants (C47's prompt/hyperparameter variants; **or C55's methodology candidates**), C48 decides which variant serves a given unit of work"; §1 Responsibilities I1 (L64) "Bind a candidate variant set (**from C47/C55**) to a routing strategy"; §3 I1 (L145) "Bind a candidate variant set (**C47/C55**) to a routing strategy … decide … which arm serves it"; §4 (L184) "Which variant set (**C47/C55**) is under test, the routing strategy (flag split or bandit)"; §5 Stand up (L207) "configured with the variant set under test (from C47, **or C55's methodology candidates**)".

**Evidence / reasoning.** This contradicts C55's own spec and the binding decision D-19:
- **C55 owns and drives its experiment run itself.** spec/C55 §I3 (L151): "For each (candidate formula × work_type): run the candidate over the same held-out C30 scenarios through the same judge … **C55 orchestrates; C31 runs, C32 judges, C33 aggregates**." C55's candidates are run through the **eval tier (C30→C31→C32→C33)**, *not* through C48's traffic router. C55 §INV-4 (L168) and §1 (L82) state C55 only "consults" C48 for significance.
- **C55 explicitly disclaims being routed by C48 in the way the C48 spec implies, and v4 keeps the two functions distinct.** spec/C55 §1 boundaries (L111): "A/B *traffic routing* is **C48**" is listed as something C55 does NOT do — but nowhere does C55 (or README/AI-CONTEXT) say C48 *routes traffic among C55's methodology candidates*. C55 produces its distributions via the eval tier and hands C48 only the comparison.
- **D-19 scopes the C55↔C48 seam to significance only.** review-log D-19: "C55 … computes per-(methodology × work-type) satisfaction distributions **via the existing eval tier (C30/C32/C33)** but does NOT perform statistical significance testing — routed to C48 … C55 names the seam." The seam is a *significance consultation*, not a *routing* relationship.

So C48's **routing** function (live A/B traffic via Unleash flag / MABWiser bandit) applies to **C47's variants only**. For C55, C48 supplies **only the significance verdict** (I3/I4) over distributions C55 already produced. Listing C55 as a routing-input/variant-set source mislabels the seam and contradicts a sibling spec + a binding decision — a fidelity defect, and a (mild) violation of the D-19 bar ("verify C48 is the single significance home … and that C55's consultation seam is mirrored"): the verdict-consumer half is mirrored correctly (I4, §2 downstream, OQ-4), but the routing-input half is an over-reach D-19 does not license.

**Suggested fix (APPLIED).** Scope C55 to the **significance-verdict consumer** role throughout: C47 (and live A/B traffic) is the routing-input/variant-set source for I1; C55 enters only at I4 (it poses a candidate-vs-candidate comparison over its own eval-tier distributions and consults the verdict). Remove "C55" from the routing-input/variant-set framing in §1 (L42), §1 I1 (L64), §3 I1 (L145), §4 (L184), §5 (L207). The verdict-consumer references (§2 downstream row, I4, §5 wiring "upstream of C50/C55", §8 AC-8, OQ-4) are correct and unchanged.

### RC48-02 — bandit (MABWiser / Vowpal Wabbit) miscited to README:273 — minor

**Claim.** Four sites cite **README:273** as support for the multi-armed bandit: §1 (L44) "multi-armed bandit (MABWiser / Vowpal Wabbit) for adaptive exploration (**README:273**; AI-CONTEXT:358/361; A69/A72c)"; §1 I1 (L65) "adaptive bandit (MABWiser, **README:273**? — paired with the Unleash:273 cite)"; §6 the-bar (L312) "MABWiser/Vowpal Wabbit (**README:273**; AI-CONTEXT:361)"; §8 AC-2 (L353) "via a bandit (MABWiser) for adaptive exploration (**README:273**; AI-CONTEXT:361)".

**Evidence / reasoning.** README:273 (the P12 capability table "A/B test routing" row) names **only "Unleash, GrowthBook, Flagsmith"** — it does **not** name a bandit. The multi-armed bandit (MABWiser / Vowpal Wabbit) is named only in **AI-CONTEXT:361** ("Multi-armed bandit | Vowpal Wabbit, MABWiser | BSD/Apache 2.0 | Mature narrow domain") and AI-CONTEXT:422, and in the per-track inventory as **A72c**. So pairing "bandit (MABWiser)" specifically with "README:273" is a miscitation. The *capability* is faithfully v4-named (AI-CONTEXT:361/422 + A72c) — only the README line ref is wrong. Where README:273 is cited for the **flag** (Unleash) it is correct (e.g. §3 I1 "fixed-split feature flag (Unleash, README:273)" stays). The combined routing-engine row at §2 (L121, "README:273; AI-CONTEXT:358/361") is acceptable because it spans both flag + bandit.

**Suggested fix (APPLIED).** At the four sites where README:273 is cited *specifically for the bandit*, drop the README:273 ref for the bandit and rely on AI-CONTEXT:361 (+ A72c); keep README:273 only where it backs the Unleash flag.

### RC48-03 — Unleash license string conflicts with README's own license table — minor, NO FIX (faithful citation of a v4 contradiction)

**Claim.** The §Source block (L4) quotes README:273 verbatim — Unleash/GrowthBook/Flagsmith licenses "**MIT / MIT / commercial-with-OSS-core**" — while the same block (L11–12) also quotes README's license table (L322 "Unleash | **Apache 2.0**"; L323 GrowthBook MIT; L324 Flagsmith BSD-3) and AI-CONTEXT:358 ("Apache 2.0/MIT/BSD-3/CNCF spec"). README:273's license string is internally inconsistent with README's own license table on Unleash (commercial-with-OSS-core vs Apache 2.0) and Flagsmith (MIT-position vs BSD-3).

**Evidence / reasoning.** This is **v4's own internal inconsistency**, not a builder error: the builder faithfully cited *both* the table row and the capability-table string, and asserts no license of its own in C48's prose (no §-body line states an Unleash license). Per the bar, a faithful spec should not silently "correct" a source contradiction; it should preserve it and route it to the version-pin/license step. §7 Ops already says "Pin scipy/statsmodels/Evidently and the router versions" and §License hygiene is C57's register.

**Suggested fix.** None applied. Optionally, a one-clause parenthetical could flag that README:273's Unleash license string conflicts with README:322 (Apache 2.0) and that the pin/license census (C57) resolves it — but this is polish, not a fidelity fix, so left for the sweep-2 version-pin/OQ rather than asserted now.

## Items checked and found SOUND (no finding)

- **The bar (capability-for-principle).** No custom router and no custom stats engine. INV-5, AC-7, and the §6 "what got DROPPED" enumeration explicitly refuse both; the keep is correctly limited to significance-determination wiring + routing-strategy binding (incl. the G32 cost-aware bandit reward) + the verdict contract. Nothing is hardening-on-existing-capability dressed as new capability.
- **D-19 significance home.** C48 is correctly specced as the single significance home consumed by **C50** (verified: spec/C50 consumes the verdict, owns promotion + Goodhart guard, `depends on C48`) **and C55** (verdict-consumer half mirrored). Only the routing-input over-reach (RC48-01) violated the seam; with it fixed, D-19 is honored.
- **G32 cost.** Reading (b) (C46 owns the cost *model*; C48 wires the *signal* and degrades-with-declaration when absent — INV-6) is consistent with spec/C46 (C46 names the cost model as its core G32 deliverable; defers significance to C48; makes no promotion decision) and with C29/C37/C55's repo-wide "cost model → C46" deferral. C48 does **not** reinvent the cost model. Sound.
- **No dependency cycle.** Inventory: C48 `depends on C47, C46`; C47 `depends on C46`; C50 `depends on C48`; C55 (Batch 4) consults C48 (Batch 5) without blocking. C48 §2 correctly treats C49 as "related, not a dependency edge." Sound.
- **Citations.** README:269/273/275/276/278/320–324/470/512, AI-CONTEXT:143/286/358/360/361/364/420–422/652, F-MODE F47(63/103/174)+F60(64), and the "C55 INV-2 / README:31" fairness cite — all verified accurate (modulo RC48-02's bandit→README:273 mis-pairing).
- **A/B-mapping.** A69/A71/A72c/B60/B63 matches the inventory C48 row. Sound.
- **Plan.** plan-faithful tasks T1–T7, critical path (T1 verdict contract → T4 significance → T7), and the WS-A/WS-B parallelization are coherent and tie to the spec's ACs/INVs. The plan inherits the same C55 framing only lightly (it lists C55 as a verdict *consumer*, which is correct) — no plan edit required.

## Verdict

**accept-with-fixes.** One major fidelity defect (RC48-01: C55 mislabeled as a routing-input source — contradicts C55 §I3/INV-4 + D-19) and one minor miscitation (RC48-02: bandit→README:273), both fixed in place. One minor (RC48-03) is a faithful citation of a v4-internal license contradiction — correctly left unaltered. The component's scope, the bar, the G32 stance, and D-19 are otherwise sound; with the C55 routing over-reach removed, C48 is a faithful sweep-1 spec.
