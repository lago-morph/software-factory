# Adversarial review — C56 Autonomy ladder (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Security & Governance
Target: spec/C56-autonomy-ladder.md (+ plan-faithful/C56-autonomy-ladder.md)
Charter: canonical track (faithful posture) → attack FIDELITY and COMPLETENESS only, not the design;
PLUS the capability-for-principle bar (flag any addition that is hardening on existing stack capability
rather than new capability tied to a 12-principle). Binding decisions in force: D-1..D-17 (relevant: D-6).

## Findings

### RC56-01 — minor — §3 contract 3 coins an opaque label ("monotone-not-assumed") that reads as if it contradicts the named "Authorization monotonicity" invariant
**Claim.** §3 interface 3 (Current-authorized-level read) prefixes the fail-safe rule with the self-coined
term **"monotone-not-assumed"**: *"Operator-set, monotone-not-assumed: a consumer that cannot read it … MUST
treat the level as the safe default (≤ L4, i.e. not L5)."*
**Evidence/reasoning.** Two problems, both fidelity/clarity (not design): (1) the **§3 invariant block**
separately defines an **"Authorization monotonicity"** invariant ("autonomy only *adds* out-of-loop authority
going up the ladder"). A reader hitting "monotone-not-assumed" two paragraphs earlier reasonably reads it as
*denying* that invariant, when the intent is the opposite — it is trying to say "do not assume an
unread/garbled value sits at a high rung." (2) The label is not a v4 term and is never defined; it is a fill
phrase dressed as a defined property. What the sentence actually states is just the **fail-safe default**,
which the spec already names cleanly in the §3 invariant "Fail-safe default", §4.3, and the §6 "Unset/garbled"
row. The coined label adds confusion, not precision. **Fix (applied).** Dropped the "monotone-not-assumed"
label; reworded interface 3 to state the fail-safe directly ("a consumer that cannot read it, or reads an
undefined/garbled value, MUST treat the level as the safe default (≤ L4 — never L5)"), and added a one-clause
pointer to the §3 Fail-safe-default invariant so the rule has a single named home. No semantic change — the
fail-safe behavior is identical; only the misleading label is removed.

### RC56-02 — minor — README ladder citation oscillates between ":81–86" and ":81–87"; harmless but worth pinning
**Claim.** The spec cites the six level *names* as "README:81–86" in most places (§1, §3.1, §4.1) but
"README:81–87" in the §3 invariant and §8.1.
**Evidence/reasoning.** Verified against README: the mermaid **node** declarations `L0[L0 Manual]` … `L5[L5
Dark]` are exactly lines **81–86**; line **87** is the order edge `L0 --> L1 --> … --> L5`. So *both*
citations are technically correct (81–86 = the names; 81–87 = names + the ordering arrow that backs the order
invariant), and the spec uses the wider span precisely where it asserts the **order** (the invariant + AC1).
This is internally defensible, not a miscite — flagged only so a later sweep does not "tidy" them to a single
span and lose the names-vs-order distinction. **Fix.** None applied (the split is correct as-is); recorded so
the divergence is known-good rather than mistaken for an error.

## Verdict

**accept-with-fixes.** This is a high-fidelity, faithful spec+plan; the one applied fix is cosmetic
(an opaque coined label), and the second finding is a confirmation that an apparent inconsistency is in fact
correct. Substantively the doc holds the line exactly where the bar demands:

- **THE BAR (no enforcement engine) — PASS, exemplary.** C56 is kept as a pure governance/policy artifact:
  ladder definition + per-level authorization boundary + declared current level + L4-default + the *named*
  F54 audit obligation. The autonomy *enforcement engine* / central interceptor is explicitly DROPPED in §1
  ("Explicitly NOT"), §6 [AMBIGUITY: G35] Reading A, §7 over-build flag, AC8, and the plan's §5 risk #1 —
  with the correct capability-for-principle reasoning (enforcement is *more machinery without a new
  principle*; it already lives at C43/C34/C39 and would duplicate their frozen specs). No central gate, no
  interceptor, no control plane. Every "action blocked" guarantee is attributed to a consumer.
- **G35 split — PASS, consistent on disk.** C56 = ladder + which-level-may-auto-ship + L4-default + F54
  audit obligation; **C43** = blast radius (verified: C43 §1/§2/line 160 — "blast-radius bound is what makes
  higher autonomy rungs (L4/L5) survivable"; "C43 caps the damage; it does not decide autonomy level");
  **C39** = per-fix ship-gate (verified: C39 §1, §3 contracts 4 & 7, I4 — "C39 reads the current authorized
  level; it does not define or set the ladder"); **C57** = objective-drift residual-risk register + the
  deferred F54 audit pack (verified: inventory C57 gaps include G35; C57 is Batch-5/unbuilt, which the spec
  correctly states in OQ-3). C35's override-loop and C34's holdout enforcement are correctly excluded from
  C56's scope. The split matches every reciprocal spec; no contradiction.
- **C39 seam (C56 = read-only level source) — PASS.** C39 on disk treats C56 exactly as the spec claims: a
  level it *reads* (contract 4 "Current-autonomy-level read (C56 → C39)") and gates on (contract 7 / I4),
  *not* a dependency that gates C39, and *not* an inventory hard-dep (C39's deps are C38/C20/C08; the C39↔C56
  tie is the G35 disposition seam). The L4-batched / L5-auto-ship / below-L4-per-fix branch and the
  downgrade-mid-flight re-read all match C39 §5 + edge cases. C53's deploy-gate seam and C52's
  "C56 sets the gate's strictness" framing also match their on-disk specs.
- **G15 — ADDRESSED faithfully.** Recorded as a documented operator-capacity *precondition* for sustained
  L4/L5 (not a runtime mechanism), citing F-MODE F25's "honest staffing / document it" guard verbatim (§6,
  §8.7, OQ-1, plan T6). This is exactly the gap's prescribed disposition; C56 does not over-reach by
  designing a throughput mechanism.
- **Fidelity — clean.** Every load-bearing citation was checked against source and is exact: README ladder
  names/order (81–87), README:90 (L4-L5 out-of-loop), README:248 (ship without human intervention),
  README:498 (design review until P12 trusted), README:527 (no L5 commitment, L4 default); AI-CONTEXT:56
  (Five-Levels ladder + "L3 HITL (the trap)"); AI-CONTEXT:335 (`Healer governance | OPA`); F-MODE-COVERAGE
  §9 F5/F6 (accepted cost of L4-L5), §11/§12 + line 178 (F54 audit pack — "the weakest v4 mechanism …
  goal-statement comparisons across cycles, escalation on detected drift"). FAITHFUL-FILLs are honestly
  tagged as fills (L0–L2 semantics by the named Five-Levels reading; the §4.2 boundary table as the
  operational reading of v4 prose with only the two v4-stated thresholds load-bearing; the C03 config home
  as sweep-2/OQ-2; the C23/C41 attribution of level-changes as a P9-consistent fill). No fill is mislabeled
  as a v4 fact; no contradiction with C39/C43/C52/C53/C57; **D-6** obeyed (canonical-track framing, no live
  Track-A/B). Inventory row (deps C52; gaps G15/G35; A13/B10; not foundational; Batch 4) matches.

Nothing architecturally significant deferred; no DEFERRED items. The open questions (OQ-2 level
representation, OQ-3 G35-split/F54-home confirmation with the unbuilt C57, OQ-4 machine-checkable L5
promotion) are correctly scoped as sweep-2 / cross-component confirmations, not sweep-1 fidelity gaps.
