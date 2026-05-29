# V4 — failure-mode coverage analysis

Maps each of the 61 catalogued failure modes (F1-F61, source: `architectures/v3/failure-modes-v3.md`) to its treatment in the v4 plan. Per-mode: which principle / layer / mechanism addresses it, what residual risk remains, and any cautions where v4 might *worsen* the failure rather than mitigate.

Three classifications:
- **Addressed** — v4 has a concrete mechanism that mitigates the failure
- **Partial** — v4 reduces but doesn't eliminate the failure
- **Gap** — v4 has no mechanism; failure stands
- **Caution** — v4's design choices could *worsen* this failure if not actively guarded

---

## 1. F-modes addressed by Layer 2 (P5 + P6 — scenarios + judge)

| F# | Name | v4 mechanism | Status |
|---|---|---|---|
| F1 | Hallucination Loop | Cross-family judge enforcement (P6 component); held-out scenarios (P5) | Addressed |
| F2 | Reward hacking | Probabilistic satisfaction over scenario population (P6); not gate-pass | Addressed |
| F9 | Spec overfitting | Cryptographically signed scenarios at day-0 (gene transfusion from GF-C pattern) | Addressed |
| F18 | Prose specs lack rigor | EARS-style spec linter (P1 component) + satisfaction-not-test-pass (P6) | Partial — fundamental prose ambiguity remains |
| F27 | Circularity / same-model build+validate | Cross-family enforcement at judge nodes | Addressed |
| F28 | Holdout leakage | Scenario storage with read-isolation (P5 component: file permissions + OPA + rig partition) | Addressed |
| F37 | Silent contradictory-prompt collapse | Multi-model paraphrase divergence (gene transfusion from GF-M pattern, runnable as pack on v4) | Partial — multi-model has its own ceiling |
| F46 | Single-model review blindspot | Cross-family judge ensemble (P6 component) | Addressed |
| F48 | Tacit collusion via shared context | Cross-family judge + independence auditor (gene transfusion from D7-U-1 pattern) | Partial — shared training distribution residual |

## 2. F-modes addressed by Layer 3 (P8 + observability)

| F# | Name | v4 mechanism | Status |
|---|---|---|---|
| F10 | Findings disappear into chat | Override log discipline (P8 component); content-addressed trajectory store (P10/CXDB) | Addressed |
| F14 | Attribution collapse | P9 (attribution) — Gas City's native strongest match; every bead, event, action carries actor | Addressed |
| F16 | Resume-fidelity decay | CXDB trajectory replay + Gas City session resume | Partial — KV cache loss inherent |
| F32 | Mail-injection / unsigned coordination | P9 attribution + optional HMAC signing layer | Addressed |
| F42 | Cognitive-Escrow Negligence | Layer 3 observability + re-engagement surface design (Honeycomb BubbleUp-style transfusion) | Partial — operator-side discipline still required |
| F50 | Architecture/spec confusion in typed objects | CXDB type registry with viewpoint tagging on bundles | Addressed |

## 3. F-modes addressed by Layer 4 (P11 — self-healing)

| F# | Name | v4 mechanism | Status |
|---|---|---|---|
| F4 | Code-quality teardown | Anomaly detection on quality metrics; Healer agent recognizes degradation patterns | Partial — quality metric definition is itself a hard problem |
| F7 | Normalization of deviance | Healer monitors acceptance-threshold drift; periodic baselining against signed scenarios | Addressed |
| F22 | Zombie agents | Anomaly detection on session liveness (PyOD on telemetry); Tracker-style diagnosis | Addressed |
| F23 | Stalled-vs-thinking ambiguity | Tracker `Diagnose`/`Audit`/`Doctor` APIs as gene transfusion source for Healer | Addressed |
| F24 | Trust creep | Healer monitors gate-relaxation patterns over time; surface to operator | Addressed |
| F40 | Last-mile drift | Healer monitors shipping rate vs project-start rate; flag stalls | Partial — need explicit shipping definition |
| F57 | Design-authority erosion | Healer monitors classification-threshold drift; surface to operator | Partial — values question; can detect drift, cannot decide |

## 4. F-modes addressed by Layer 5 (P7 — digital twins)

| F# | Name | v4 mechanism | Status |
|---|---|---|---|
| F12 | Lethal trifecta | Twins reduce production exposure; boundary typing (CaMeL pattern); scenarios use twins not production | Addressed |
| F33 | Adversarial-prompt defeat of LLM-judge | Deterministic boundary typing as primary guard (P4); LLM-judge as secondary; twins remove the deploy-to-production vector | Addressed |
| F44 | Lethal-Trifecta Production-Scissors Default | Substrate default: twins for everything; production scissors require explicit declaration per pack | Addressed |
| F56 | Guardrail-bypass under stress (Replit-class) | Twins isolate the agent from production entirely; stress-induced compliance failure has bounded blast radius | Addressed |

## 5. F-modes addressed by Layer 6 (P12 — self-optimization)

| F# | Name | v4 mechanism | Status |
|---|---|---|---|
| F47 | Visible-metric drift / Goodhart | Meta-metric definition is values-question; variant testing measures multiple metrics simultaneously; no single visible target | Partial — Goodhart applies recursively to meta-metrics |
| F60 | Parallel-cycle compounding error | Aggregate-rate tracking in meta-metric set (1 − (1−p)ⁿ explicit); A/B harness reports aggregate not single-cycle | Addressed |

## 6. F-modes addressed by foundational principles (Phases 0-1)

| F# | Name | v4 mechanism | Status |
|---|---|---|---|
| F11 | Renumbering breaks references | Content-addressed storage (CXDB BLAKE3) makes references immutable | Addressed |
| F19 | Model-floor dependency | v4 declares Claude Code as floor explicitly | Addressed (by declaration) |
| F26 | Telephone / sustained inter-agent chain | Pipeline-file (P3) controls handoff patterns; chain length is a formula property, visible and lintable | Addressed |
| F31 | Substrate safety floor = weakest adapter | v4 uses only Claude Code via Gas City tmux runtime; floor is well-defined and stable | Addressed (by single-adapter choice) |
| F38 | Vocabulary lint debt | EARS-style spec linter (P1 component); deterministically detectable | Addressed |
| F43 | RSI Board-Visibility Gap | P9 attribution + audit trail + bead history; pack-author declares RSI status in pack.toml | Partial — declaration discipline still operator-required |
| F51 | Ashby-deficient probabilistic guard | P4 (deterministic-first) — deterministic boundary typing is the primary guard; LLM-judge is secondary | Addressed |
| F53 | Voluntary-discipline fragility | Substrate-triggered structural controls (Gas City hooks, formula checks) replace operator-voluntary discipline | Addressed |
| F55 | Behavioural drift / self-reference loop | External grounding: signed scenarios + twins as external truth; held-out scenarios from human-authored corpus | Partial — drift in synthetic scenarios still possible |
| F61 | Context fragmentation across agents | Shared CXDB trajectory store; multi-agent reads through bead query | Partial — agents still take local decisions |

## 7. F-modes that gene-transfusion patterns address (Phase 3+ factory-built)

| F# | Name | v4 mechanism | Status |
|---|---|---|---|
| F8 | Stale-knowledge inversion | Healer's anomaly detection includes knowledge-store freshness; periodic curation pack | Addressed |
| F17 | Parallel agents on shared dirs lose data | Gas City worktree isolation per session (native); OPA policy on shared partitions | Addressed |
| F32 | Mail-injection (revisit) | HMAC signing on mail bus (gene transfusion: any signed-message protocol) | Addressed |
| F34 | Cross-layer drift | Drift detector pack (gene transfusion from U-B pattern); cross-layer invariants made explicit | Partial |
| F35 | Federation-as-Family Drift | Pack governance pack: derivation-rule check at pack adoption time | Partial — discipline-required |
| F39 | Point-spec / region-mismatch | Inspect AI region scoring (multiple acceptable trajectories); satisfaction distribution over region | Addressed |
| F41 | Under-defined-intent debt | Intent Crucible pack (gene transfusion from GF-C) — 9-field structured intake | Addressed |
| F45 | Language-as-Harness Mismatch | v4 stack uses Go (strongly typed); Inspect AI uses Python; bounded scopes | Partial — Python sections inherit risk |
| F54 | Goal subversion (RSI prompt-injection over cycles) | CXDB content-addressed history + Healer anomaly detection on objective shift | Partial — significant residual; requires audit discipline |
| F58 | Runtime/design-time compliance split | Continuous observability + meta-metric tracking provides runtime evidence | Partial — depends on regime-specific requirements |

## 8. Cautions — F-modes v4 might *worsen* if not actively guarded

| F# | Name | Why v4 might worsen | Guard |
|---|---|---|---|
| F52 | Tempting-Wrong-Hybrid (deterministic-wrapping reflex) | v4's emphasis on Layer 4 self-healing + Layer 6 self-optimization is exactly the "more controller patches" trap Schillace names. P4 (deterministic-first) could become discipline-without-purpose. | **Explicit discipline**: every deterministic guard must point at a specific scenario it catches, with measurable false-positive rate. No guard without a falsifying scenario. Counts of catches per guard reviewed monthly. |
| F35 | Federation-as-Family Drift | v4's pack architecture creates exactly this risk if pack governance is not explicit. Packs claimed managed-family, instances drift, no derivation-rule check. | **Pack discipline**: derivation-rule check as Phase 1 component; pack adoption requires passing the check. Audit periodic. |
| F25 | Design starvation | v4's principle-bound runtime is high-throughput; if operator can't spec faster than factory consumes specs, you're in design starvation by construction. | **Honest staffing**: v4 doesn't claim to solve design starvation. Document the operator-throughput requirement. |
| F47 | Goodhart on visible metrics | v4's meta-metric layer creates explicit visible metrics. Goodhart applies. | **Multi-metric mandatory**: no single visible target; P12 always tracks aggregate of multiple metrics; promotion gate requires multiple metrics moving together. |

## 9. Gaps — F-modes v4 does not address

These are failure modes v4 does not have a mechanism for. Some are inherent limits; some are intentional scope choices; some are residual gaps that should be revisited.

| F# | Name | Why v4 doesn't address |
|---|---|---|
| F3 | Spec-completeness fallacy | Fundamental: specs cannot enumerate everything that should not happen. Twins (P7) and scenarios (P5) partially compensate by checking against environment-wide behavior. Residual gap. |
| F5 | Cognitive ceiling | Operator-side; v4 mitigates via L4-L5 batching (no per-cycle review) but if the operator is in the per-cycle loop, F5 remains. v4 explicitly targets out-of-loop. |
| F6 | Cognitive debt | Operator-side; v4 deliberately delegates the model of the system to the factory. Operator mental-model erosion is an accepted cost of L4-L5 operation. |
| F13 | Missing-config blindspot | Twins (P7) partially address by exercising environment; but the unspecified environment surface is fundamentally larger than any test set. Residual gap. |
| F20 | Maintenance vs greenfield asymmetry | v4 deliberately does not pick a mandate. Both greenfield and brownfield methodologies can run on the runtime. Mandate-specific behavior is methodology-level, not runtime-level. |
| F21 | Context-window exhaustion | Methodology-level concern (pack chooses context-management strategy). Runtime provides observability to detect exhaustion but doesn't prevent it. |
| F29 | Talent pipeline depletion | Systemic; v4 doesn't claim to solve. Pack-author skill level becomes a constraint v4 should document. |
| F30 | Liability vacuum | Systemic / regulatory; v4 doesn't address regulatory framework gaps. Pack-author declares regulatory regime. |
| F36 | Instruction-following ceiling | Inherent model limit (Yang et al. 19-requirement ceiling). v4 mitigates via spec-chunking (P1 component: small focused specs) but the limit persists per chunk. |
| F49 | Discussion-as-Amplification | Empirical instability of safety prompts; v4 substitutes substrate-level controls (P4 deterministic-first) for prompt-level safety. Residual: prompts still carry instructions. |
| F59 | Premature decomposition | Methodology-level concern. The runtime supports either spec-then-implement or discovery-during-implementation; pack authors choose. v4 doesn't impose either. |

---

## 10. Summary by status

Of the 61 catalogued failure modes:

| Status | Count | Percentage |
|---|---|---|
| Addressed | 24 | 39% |
| Partial | 20 | 33% |
| Gap | 11 | 18% |
| Caution | 4 | 7% |
| Addressed (by Phase 3+ factory-built components, with gene-transfusion sources identified) | 10 | overlap with above |

Net: **~72% of catalogued failure modes have some v4 mechanism** (addressed or partial); **~18% remain as gaps** (mostly inherent limits or systemic constraints v4 cannot solve); **4 modes carry active cautions** because v4's design choices could worsen them without explicit discipline.

The gap set is dominated by inherent model limits (F3, F36, F49) and operator-side failures (F5, F6, F25, F29) that no substrate can fully address. The cautions (especially F52 — the Tempting-Wrong-Hybrid trap) are real and warrant explicit discipline in v4's implementation.

---

## 11. Strongest matches and weakest matches

**Strongest v4 matches** (single mechanism cleanly addresses):
- **F14** (Attribution collapse) — Gas City's native attribution is the corpus's strongest principle match
- **F11** (Renumbering breaks references) — CXDB content-addressing makes references inherently stable
- **F31** (Substrate safety floor = weakest adapter) — single-adapter choice (Claude Code only) defines the floor
- **F50** (Architecture/spec confusion in typed objects) — CXDB type registry enforces viewpoint separation
- **F53** (Voluntary-discipline fragility) — substrate-triggered controls replace operator-voluntary discipline

**Weakest v4 matches** (real residual risk):
- **F36** (Instruction-following ceiling) — inherent model limit
- **F49** (Discussion-as-Amplification) — empirical instability of safety prompts
- **F54** (Goal subversion) — multi-cycle objective drift is structurally hard to detect
- **F55** (Behavioural drift / self-reference loop) — external grounding helps but synthetic scenarios drift
- **F58** (Runtime/design-time compliance split) — depends on regulatory regime

**v4's distinctive contributions** (modes v4 addresses better than v3 candidate-shaped approaches):
- **F52** (Tempting-Wrong-Hybrid): v4's explicit principle-grounding of every guard prevents controller-patch accretion
- **F25** (Design starvation): v4's runtime separation makes the operator-throughput requirement visible
- **F60** (Parallel-cycle compounding): meta-metric tracking forces aggregate-rate awareness

---

## 12. Recommendations for the v4 plan

Based on the coverage analysis:

1. **Add F52 discipline as a Phase 0 requirement.** Every deterministic guard added in Phases 0-1 must point at a specific scenario it catches. No guard without a falsifying scenario. This is the explicit guard against the Tempting-Wrong-Hybrid trap.

2. **Add F35 governance to Phase 1.** Pack-derivation-rule checks should ship with the initial pack infrastructure, not as a later add-on. Pack governance prevents Federation drift before it accumulates.

3. **Make F47 multi-metric mandatory.** No single visible target in P12; promotion gate requires multiple metrics moving coherently. Goodhart applies and v4 should not pretend otherwise.

4. **Document the F25 honest constraint.** v4 does not solve design starvation. Operator throughput is a real constraint and pack-author skill is a real input. Document this so adopters set expectations correctly.

5. **Plan an F54 audit pack.** Goal subversion (multi-cycle objective drift) is the weakest v4 mechanism. Build an explicit audit pack: regular goal-statement comparisons across cycles, escalation on detected drift.

6. **Honest scoping of residual gaps.** F3 (spec-completeness), F36 (instruction-following ceiling), F49 (discussion amplification) are inherent. v4 should not claim to solve them; documentation should make the residual risk visible.

---

*Document created: 2026-05-29. Source: `architectures/v3/failure-modes-v3.md` (61 F-modes catalogued). Last updated: 2026-05-29.*
