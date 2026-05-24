---
track: greenfield-methodology-first
axis: methodology-first
mandate-scope: greenfield
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
based-on-date: 2026-05-24
---

# Greenfield, methodology-first

## §0 Axis declaration and defense

**Axis.** Methodology — the per-cycle process — is the primary organizing
principle. The substrate is whatever the chosen cycle shape *requires*; the
substrate is downstream, not upstream. For greenfield specifically, the
question is: *what cycle shape stays productive while the spec is still
moving?* Everything else in this track derives from that question.

**Why methodology-first for greenfield (and not the other way round).**
Greenfield's defining property per UC4 is that the architecture moves
during spec refinement. The substrate cannot be sized, scoped, or
configured until the cycle shape is fixed, because the cycle shape decides
what state has to persist, what gets held out, what gets diffed, what gets
re-tried, and where the human re-enters. Substrate-first greenfield tracks
risk pre-committing to primitives (event-sourced trajectory, RouterLLM,
mail bus, holdout store) before the cycle has decided whether it needs
them. CTR-C2 (substrate-heavy + thin-methodology vs methodology-dominates,
[`13-round-2-synthesis`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md)
§8 vs UC4) is the named tension; this track sits on the methodology-dominates
side of it for greenfield. Brownfield may sit on the other side; that is
not this track's argument.

**Pre-response to anticipated Phase-3 adversarial passes.**

- *"This is just Compound Atelier renamed."* No. Compound Atelier's unit of
  work is *an issue from a queue against an accumulating knowledge base*
  ([`research/03`](../../../research/03-every-compound-engineering.md)) —
  it presupposes a system that has issues and accumulated solutions, which
  greenfield day-0 lacks. The cycle proposed here (§1) is shaped for the
  spec-malleable regime where the unit of work is *a reversible commitment
  against a still-discovering intent*, not an issue. The Phase-1 inventory
  re-tag of report 03 to `brownfield-primary` (CHALLENGE-6) is consistent
  with this.
- *"You're ignoring CTR-A1 / Jaymin's empirical anti-pattern claim against
  L5."* See §2. This track adopts brief §2.1 option (c)+(b): lights-out
  *over a defined work-unit-class surface*, with explicit regime
  classification per cycle phase. The track's cycle defaults to L4
  (operator setting policy, sample-auditing, on watchdog escalation
  only) and explicitly *names* the cycle phases that escalate to L3
  augmentation. This is not a hand-wave; it is a per-phase declaration.
- *"Methodology-first is the contaminated v2 framing under a new name."*
  No. The v2 architectures (Atelier / Refinery / Foundry / Tournament)
  were each methodology-first in some sense but none was built around the
  *spec-malleable phase as a first-class regime*. The cycle here is novel:
  it treats the malleable phase as a distinct work-unit class
  (`initial-spec` per D2) with different gates, different judges, and a
  different exit criterion than the steady-state phase that follows.
- *"You'll just be re-asserting D-1 (spec is the durable artifact) and
  calling it a methodology."* The spec is durable, but in greenfield the
  spec *is itself being authored* and the question is what the cycle does
  *before* the spec is durable enough to anchor anything. That question is
  what the cold-start section (§5) and the cycle shape (§1) actually
  answer. D-1 holds at steady-state; this track names the phase before
  steady-state and gives it a shape.
- *"You're treating the substrate as an afterthought; F31 (substrate
  safety floor) and F44 (production-scissors default) bite regardless."*
  Agreed. §1.4 lists what the substrate *must* provide for the cycle to
  function. This is a *requirement* on the substrate, not a design of it.
  Phase 4 decides whether those requirements are met by a substrate
  shared with the brownfield mandate or by a greenfield-specific one;
  this track does not pre-decide that.

---

## §1 Architecture sketch

The greenfield mandate is split into **two regimes** the cycle treats
differently. The split is the architecture.

### 1.1 Regime A — *Spec-discovery* (the malleable phase)

**Operating mode.** L3 augmentation by default (per CTR-A1 / CTR-H10
cluster). Lights-out is *not* claimed here, because the dominant failure
modes (F36 instruction-following ceiling, F37 silent contradictory-prompt
collapse, F41 under-defined-intent debt, F39 point-spec/region-mismatch)
are model-capability limits with empirically inadequate LLM-judge
mitigation (Larbi MCC ≤ 0.55 for contradiction detection, report
[`26`](../../../research/26-prompt-underspecification-academic.md) §6.1).
The cycle's contract is to *make the spec converge fast enough that
Regime B can run lights-out*, not to itself run lights-out.

**Unit of work.** A *reversible commitment*. Not an issue (no queue
yet), not a PR (no codebase to PR against yet), not a change request
(no spec to change yet). A reversible commitment is a hypothesis-shaped
artifact pair: (a) an intent block in El Kaim's 9-field shape (report
[`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md))
with `invariants` populated, and (b) a paired scenario in Kaner's
out-of-tree shape (followup
[`09`](../../../research/followup/09-methodology-ancestors.md)) that
operationalizes the intent. Both are versioned. Both are explicitly
labelled `reversible` until promoted.

**Cycle shape.** Four phases per cycle:

1. **Intent draft** — operator dictates intent in natural prose;
   substrate produces an EARS-constrained acceptance-criteria block
   (report [`25`](../../../research/25-requirements-engineering-foundations.md)
   §2.2) and a structured 9-field intent block. Deterministic lint
   against GtWR R7/R8/R9 (mitigating F38 vocabulary lint debt) runs at
   this gate; failures are returned to the operator, not silently
   rewritten by an agent.
2. **Paraphrase divergence** — the intent is restated by *N* independent
   model-family agents (cross-model per F46) into *N* candidate scenarios
   and *N* paraphrased intents. If the *N* paraphrases disagree
   semantically (judged at the level of which post-condition is being
   asserted, not at the surface-text level), the intent is flagged as
   *underspecified* (Yang et al., report 26 §1) and returned to the
   operator. **This is the cycle's defense against F37**: rather than
   relying on a single LLM judge to detect a contradiction (Larbi MCC ≤
   0.55), the cycle detects contradiction by *behavioural disagreement
   across paraphrasers*. The bar is K=5 prompt-paraphrase robustness 3-of-5
   in this regime ([`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5
   Augmentation bar; not the Automation bar — this is L3).
3. **Tiny probe** — one (and only one) candidate scenario is realized in
   the smallest possible working artifact (Schillace fidelity-1 sense,
   followup [`05`](../../../research/followup/05-klaassen-siblings.md)).
   The probe is *not* the system being built; it is a probe of the
   spec. If the probe surfaces an intent ambiguity the paraphrase step
   missed (e.g., the operator says "obvious, you should have known"
   when seeing the result), the cycle returns to phase 1 and the
   commitment is reversed.
4. **Promote or reverse** — if the probe satisfies the operator's
   reaction (a deliberately *thick*, AI-judge-resistant signal per F51
   Ashby), the intent + scenario pair is promoted from `reversible` to
   `durable`; otherwise both are reversed (deleted, not amended).
   *Reversal is cheap by design; this is what makes "spec-malleable"
   productive rather than paralytic.*

**Exit condition for Regime A.** When the cumulative set of durable
intents covers a coherent slice of the system (criterion: at least one
end-to-end scenario passes through the slice without an intent gap),
the cycle transitions the slice to Regime B. Different slices transition
at different times; Regime A and Regime B run concurrently after the
first slice transitions.

### 1.2 Regime B — *Spec-anchored execution* (the steady-state phase)

**Operating mode.** L4 lights-out for `regression-fix` and
`post-mvp-evolution` work units on *promoted* slices. L3 for any work
unit that touches a still-`reversible` intent. (This is the per-cycle
mandate-fit declaration that D2 asks for.)

**Unit of work.** A scenario from the durable scenario set (Kaner-shaped,
out-of-tree per D-2, with the holdout discipline of D-4 substrate-enforced).
The scenario is the queue item; durable intents are the spec.

**Cycle shape.** Standard Compound-Engineering-like loop
(plan → work → review → compound, report
[`03`](../../../research/03-every-compound-engineering.md)) with one
explicit modification: the review panel is **cross-model** (per F46
single-model review blindspot; CJ Hess `kevin/carl` pattern, report
[`34`](../../../research/34-lenny-howiai-personal-harnesses.md) §6.2),
*not* same-model — this contradicts CTR-D7 (Anthropic's "same model fine"
finding from followup
[`07`](../../../research/followup/07-evals-deepdive.md)) on the
specific grounds that greenfield has no out-of-distribution ground truth
(failure-modes-v3.md §7 force #1).

### 1.3 The methodology→substrate derivation (what the cycle *requires*)

Reading off Regime A + Regime B, the substrate must provide:

- **Reversibility primitive.** Cheap commit-and-reverse on intent
  artifacts. *Substrate consequence:* event-sourced storage of intent /
  scenario versions (D-7 trajectory capture, report
  [`11`](../../../research/11-openhands-substrate-audit.md) §6,
  sub-ms persist makes this affordable). Note this is a *methodology-driven*
  reason to need D-7, not a substrate-inherited one.
- **Paraphrase divergence primitive.** N model-family-diverse paraphrasers
  callable in parallel. *Substrate consequence:* multi-provider routing
  (the OQ-B8 abstraction layer, contested in CTR-C4). This track requires
  the *capability* (model-family diversity); it is agnostic on
  RouterLLM-vs-provider-aligned-profiles.
- **Holdout enforcement.** Scenarios must be unreadable by builder
  agents (D-4, mitigating F28). *Substrate consequence:* a sandboxed
  filesystem partition with substrate-enforced read masking, not
  agent-discipline-enforced.
- **Tiered watchdog.** Daemon / Triage / Patrol per C14 (Round-2
  consensus, [`13-round-2-synthesis`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md)
  §1.1) — the Regime A → Regime B regime change is exactly the kind of
  drift Patrol catches.
- **Cost ceiling.** D-5 — non-optional in CI, with the Phase-A
  paraphrase fan-out cost as a known multiplier (~Nx single-cycle
  cost; this is the methodology's explicit cost-vs-correctness trade
  per UC5).
- **Cognitive escrow primitive.** The Phase-1 and Phase-4
  operator-touchpoints are exactly the moments where Kahana's escrow
  interval is load-bearing (report
  [`30`](../../../research/30-cognitive-escrow.md) §4). The substrate
  must surface reflection prompts in the interval, not minimize it
  (mitigating F42, F53).

### 1.4 What is NOT in this architecture

- No tournament population (the cycle uses *paraphrase divergence* at
  the spec layer, not candidate divergence at the implementation
  layer; CTR-D3 explicitly bites tournament-shaped greenfield).
- No graph-DAG pipeline (the cycle is two regimes with explicit
  transition; Attractor's `.dot` shape per report
  [`02`](../../../research/02-strongdm-attractor.md) is one valid
  realisation of Regime B but is not load-bearing).
- No same-model judge pool (per F46 / CTR-D7 split — this track sits
  on the cross-model side for the named greenfield reason).
- No `docs/solutions/` knowledge accumulation in Regime A (greenfield
  day-0 has nothing to accumulate; the directory makes sense only
  after Regime B has been running long enough to produce repeatable
  patterns — and even then, F55 behavioural drift / F8 stale knowledge
  inversion gate its use).

---

## §2 How this addresses each load-bearing concern

### 2.1 Lights-out / L5 tension (brief §2.1; OQ-B1)

This track adopts **option (c)+(b)** per brief §2.1: lights-out *over a
defined work-unit-class surface*, with explicit regime classification.

**Vocabulary mapping (CTR-A4).** This track maps UC1 *lights-out* to L4
("I'm here," Shapiro followup
[`01`](../../../research/followup/01-shapiro-five-levels.md)), not L5.
The operator is upstream (intent dictation, Regime A reflection
touchpoints) and downstream (sample auditing, watchdog escalation), but
not in the per-cycle inner loop for Regime B work units. This makes
CTR-A1 (L5-as-anti-pattern) mostly dissolve for this track (per
CTR-H10's WEAK-4 sharpening: Round-2's ceiling claim is L5-anti, not
L3-only; L4 lights-out is compatible).

**Regime A explicitly does not claim lights-out.** It claims L3
augmentation with K=5 prompt-paraphrase robustness 3-of-5 as the
empirical bar (Jaymin Augmentation Mode, report
[`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5).
The paraphrase-divergence step *is* the threshold-check mechanism — it
operationalises the bar in the cycle, not as a separate audit.

**Regime B claims L4 with K=5 consistency ≥90% as the empirical bar.**
The cross-model review panel produces the K=5 signal continuously
(every cycle's review is itself a K-sample); architectures that cannot
sustain ≥90% are caught in-cycle, not at audit time. This is option (a)
under brief §2.1 (clears Jaymin's Automation bar by the named
mechanism), reinforced by option (c) (regime classification).

### 2.2 UC4 working hypothesis

This track *accepts* UC4 for greenfield: spec-malleability is real and
constitutive. But it does not accept the implicit framing that
spec-malleability makes the cycle *paralytic*. The cycle is productive
in the malleable phase because **commitments are reversible by design
and cheap by substrate**. The methodology is shaped *for* malleability,
not *despite* it.

The CTR-B6 sharpening (El Kaim's intent-block as upstream stability vs
UC4 spec-malleable) is reconciled here by treating El Kaim's
`invariants` field as the **only** stable subfield within an otherwise
reversible intent. The invariant is what makes reversal possible
(you know what cannot change); the rest of the intent block is
deliberately fluid in Regime A.

### 2.3 Cold-start (greenfield) — see §5 (mandatory section).

### 2.4 OQ-B3 (human re-entry mechanism)

The Regime A → Regime B transition is a *declared* re-entry trigger:
the operator approves the slice promotion. Watchdog escalations (C14
Patrol tier) re-trigger human entry on drift; the substrate-level
protocol is the slice rollback (reverse the most recent N promotions to
the last-known-coherent slice). This is more concrete than the brief's
reframe asks for and is methodology-derived, not substrate-derived.

### 2.5 OQ-B4 (unit of work shape)

The unit of work is *neither* issue *nor* change-request-against-spec.
In Regime A it is a *reversible commitment*; in Regime B it is a
*scenario from the durable set*. The shape is regime-specific. This is
the cleanest answer this track has to OQ-B4 for greenfield.

### 2.6 OQ-B6 (empirical bars)

This track adopts Jaymin's bars (K=5 / paraphrase) as the per-regime
declared bars, with the cycle itself producing the K-sample at no extra
cost. The CTR-A1 WEAK-1 sharpening (Jaymin Ch9 §7 is two-sided) is
absorbed: Jaymin is the source of both the bars and the
"this time it works" framing, and the track does not need to resolve
that tension to use the bars operationally.

### 2.7 OQ-B7 (other organizing axes)

Methodology-first is itself the axis answer for this track. Regime
(Regime A vs Regime B), stakes (reversible vs durable), and
synchronicity (operator-in-loop vs lights-out) all surface as
*derived* organizing axes within the methodology, not as competing
top-level organizing principles.

### 2.8 OQ-B9 (methodology evolution)

In this track, methodology evolution is *per-architecture* (the cycle
shape itself is the architecture). The substrate provides primitives
(trajectory, holdout, watchdog); the methodology composes them. The
self-improving-prompts pattern (Klaassen, report
[`03`](../../../research/03-every-compound-engineering.md)) is
permitted in Regime B as a methodology concern, not as a substrate
primitive — and gated by F55 (behavioural drift in self-reference
loops).

### 2.9 Failure-mode coverage highlights

- **F36 (instruction-following ceiling)**: Regime A's intent-block
  decomposition + chunked verification keeps simultaneous-requirement
  load per cycle below the 10–20 ceiling.
- **F37 (silent contradictory-prompt collapse)**: paraphrase
  divergence is the in-cycle detector; LLM-judge is *not* relied on
  (Larbi MCC ≤ 0.55 is treated as disqualifying).
- **F39 (point-spec/region-mismatch)**: paraphrase divergence + tiny
  probe surfaces region-vs-point mismatches behaviourally.
- **F41 (under-defined intent debt)**: Regime A's exit criterion
  *is* intent-discipline. No promotion without paraphrase agreement +
  probe satisfaction.
- **F25 (design starvation)**: explicitly *not* solved — Regime A's
  throughput is operator-bound by design. Mitigation is that Regime B
  runs in parallel for already-promoted slices, so the factory is
  not idle waiting for Regime A.
- **F40 (last-mile drift)**: addressed in Regime B's promotion
  criterion (end-to-end scenario must pass before slice is promoted);
  not addressed in Regime A by design.
- **F44 (lethal-trifecta production-scissors)**: substrate-level
  default-off required (§1.3); methodology does not relax it.
- **F52 (tempting-wrong-hybrid)**: this track has *only one*
  deterministic wrapper (the GtWR linter at Phase 1) and one
  cross-model check (paraphrase divergence). Everything else is the
  cycle itself. This is a deliberate guard against control-layer
  accretion.
- **F53 (voluntary-discipline fragility)**: STIR-style discipline is
  baked into the cycle (paraphrase step, probe step, promote/reverse
  gate); none of it is operator-voluntary.

---

## §3 Citations and grounding

Primary load-bearing citations for this track:

- **UC1, UC4** ([`constraints-extracted.md`](../constraints-extracted.md)) — the mandate and the malleability claim.
- **D-1, D-4, D-5, D-6, D-7** (brief §4.1) — accepted defaults; see §4.
- **D-2, D-3** (brief §4.1) — accepted with track-specific scope; see §4.
- **CTR-A1, CTR-A4, CTR-C2, CTR-D7, CTR-H10** ([`contradictions.md`](../contradictions.md)) — the operating-mode and substrate-vs-methodology tensions this track sits on a specific side of.
- **CTR-B6** — El Kaim invariants vs UC4 malleability, resolved here by treating `invariants` as the only stable subfield.
- **F36, F37, F38, F39, F40, F41, F46, F52, F53, F55** ([`failure-modes-v3.md`](../failure-modes-v3.md)) — the failure-mode core this track's cycle is shaped against.
- **Report 25** (EARS / GtWR), **Report 26** (Yang underspecification; Larbi contradiction collapse), **Report 14** (El Kaim 9-field intent), **Report 30** (Kahana cognitive escrow), **Report 31** (Kahana RSI/Caremark), **Followup 10** (governance / Replit incident) — the cold-start required reading (brief §5.1).
- **Report 09** §5.5 — K=5 consistency and prompt-paraphrase robustness bars used in §2.1.
- **Report 34** §6.2 — CJ Hess `kevin/carl` cross-model QC, cited for the Regime B review panel design (and against F46).
- **Followup 09** — Kaner scenario-testing primary anchor for the out-of-tree scenario primitive.
- **Followup 05** — Klaassen fidelity-1 framing for the tiny-probe step in Regime A.
- **Report 11** §6 — OpenHands sub-ms persist, cited as evidence that reversible-commitment cost is affordable.

---

## §4 §4 defaults: accepted vs challenged

**D-1 (specs are the durable, version-controlled, human-curated artifact)** —
**accepted with justification.** True at steady-state. In Regime A the spec
is partially `reversible` (not yet durable); D-1 applies the moment an
intent is promoted from `reversible` to `durable`. The promotion event
*is* the moment D-1 attaches. Justified by report 14 (El Kaim intent
authorship) + report 35 (Nystrom Markdown-spec-in-repo as AFIS strategy-3
industrial anchor).

**D-2 (scenarios live outside the codebase as a holdout set)** —
**accepted with justification.** Strongly applicable for greenfield:
there is no codebase to inherit scenarios from (CHALLENGE noted as
fragile for brownfield only). Greenfield must author scenarios
out-of-tree from day 0; CTR-B5 / CTR-G2 (the fragility flag) does not
bite greenfield. Kaner-shaped per followup
[`09`](../../../research/followup/09-methodology-ancestors.md).

**D-3 (Agent = Model + Harness)** — **accepted with justification.** The
cycle here uses harness-shaped agents (paraphrasers, builders, reviewers)
with explicit prompts and tool surfaces; the population-shaped and
graph-node-shaped fragility flags do not bite (this track is neither
tournament nor graph-pipeline). The CTR-C10 sharpening (natural-language
register as a third axis, report 37) is *acknowledged*: the paraphrase
step explicitly varies natural-language register, which extends D-3
operationally without contradicting it.

**D-4 (holdout discipline is substrate-enforced)** — **accepted with
justification.** F28 (holdout leakage) is critical for greenfield (per
[`failure-modes-v3.md`](../failure-modes-v3.md) F28); substrate
enforcement is the only credible mechanism given F53 (voluntary
discipline fragility). This is *required* in §1.3.

**D-5 (hard cost ceilings non-optional in CI)** — **accepted with
justification.** Regime A's paraphrase fan-out is the primary cost
multiplier; D-5 caps it. The CTR-E6 sharpening (CaMeL's measurable
utility tax) is acknowledged: substrate safety primitives have non-zero
cost, and the cost ceiling must explicitly admit them.

**D-6 (tiered watchdog substrate primitive)** — **accepted with
justification.** Patrol tier is exactly the drift-detection layer needed
for the Regime A → Regime B transition (F34 cross-layer drift, F55
behavioural drift). Daemon and Triage handle F22 / F23.

**D-7 (trajectory capture cheap and production-tested)** — **accepted
with justification.** The reversibility primitive in §1.3 *requires*
cheap event-sourcing; D-7's evidence (OpenHands sub-ms persist) is the
warrant that the cycle is implementable. Note this is a
methodology-driven need for D-7, not a substrate-default inheritance.

*All 7 defaults marked. None challenged.* This is itself a finding:
the methodology-first greenfield axis happens to be compatible with all
7 Round-1/Round-2 defaults, which is informative — the contention with
the defaults lives in the brownfield, population, and graph-node
architectures, not here.

---

## §5 Cold-start (MANDATORY for greenfield)

### 5.1 Day-0 state

A greenfield factory at day 0 has:
- An operator with a domain idea (prose-shaped).
- Adjacent-domain priors (per brief §0 glossary revision per Skeptic #6):
  exemplar projects, framework / library docs, operator-curated knowledge
  from *other* factory runs. Permitted and expected.
- No scenarios, no issue queue, no `docs/solutions/`, no prior runs of
  *this* factory.
- Substrate primitives per §1.3 (assumed available; Phase 4 decides
  their concrete realisation).

### 5.2 The bootstrap protocol

Day 0 starts in **Regime A only**. Regime B does not run until at least
one slice has been promoted. The bootstrap sequence:

1. **Operator dictates the first intent** in prose. The substrate runs
   the EARS / GtWR lint (report
   [`25`](../../../research/25-requirements-engineering-foundations.md))
   on the resulting acceptance-criteria block. Lint failures return to
   the operator. *Day-0 priors are used here*: adjacent-domain exemplars
   inform what the intent should plausibly look like, but the cycle does
   not auto-import them.
2. **Paraphrase divergence** runs against the first intent. **This is
   the most important day-0 step.** It surfaces F37 (silent
   contradictory-prompt collapse) and F41 (under-defined intent debt)
   before any code is written. Day-0 is the regime where these failure
   modes bite hardest (per failure-modes-v3.md severity ratings:
   F37 critical, F41 critical for greenfield).
3. **First tiny probe**. Fidelity-1 (followup
   [`05`](../../../research/followup/05-klaassen-siblings.md)) — the
   smallest possible working artifact. The probe's job is to surface
   what the paraphrase step missed.
4. **First promote-or-reverse**. If promoted, this is the seed of the
   durable spec. Even a single promoted intent + scenario pair is enough
   to start a *minimal* Regime B for that slice. *The transition is
   not gated on having a "complete" spec — it is gated on a coherent
   slice.*

### 5.3 Bootstrap protection against silent failure

The bootstrap-phase architecture has no track record to evaluate itself
against. The protections are:

- **Paraphrase divergence is its own protection.** It is a same-cycle
  K=5 (or K=N) test that does not depend on any external ground truth.
  This is the day-0 analog of the K=5 consistency bar (report 09 §5.5).
- **Tiny probes are cheap to throw away.** Reversal is by design (§1.1
  step 4); a bad bootstrap is detectable because the probe surfaces
  operator dissatisfaction *as the cycle's defined exit signal*, not
  as a separate audit.
- **Patrol watchdog (D-6) runs from day 0**, watching for the kind of
  silent drift Kahana's RSI/Caremark framing names (report
  [`31`](../../../research/31-caremark-rsi-board-exposure.md) §1 three
  RSI failure modes). The cold-start period is exactly when behavioural
  drift (F55) is hardest to detect on the cycle's own outputs because
  there are few outputs.
- **No `docs/solutions/`-style knowledge accumulation in the
  cold-start phase.** Self-referential drift (F55) is most acute at
  cold-start because all "knowledge" is from a tiny number of cycles.
  Accumulation begins only after Regime B has produced enough cycles
  to be evaluable.
- **Cognitive escrow primitive (report
  [`30`](../../../research/30-cognitive-escrow.md)) is active from
  cycle 1.** The Regime A operator touchpoints (intent dictation,
  promote/reverse decision) are escrow-interval design sites; the
  substrate surfaces reflection prompts (F42 mitigation).
- **Governance scaffolding from day 0** per Kahana RSI/Caremark
  (report 31) and followup
  [`10`](../../../research/followup/10-governance.md). Even at
  cold-start, the factory's outputs are subject to RSI three-part test
  exposure once the cycle is running over multiple iterations; the
  bootstrap protocol logs immutably (AILCCP control) and gates
  material self-modification behind operator promotion (Human Approval
  Gate). The Replit-incident anchor (followup 10 §3, G14) is the
  reason F56 (guardrail-bypass under stress) requires substrate-
  default scissors, not operator-discipline scissors.

### 5.4 Trajectory from day 0 to day N

- **Day 0 to day ~T₁ (first slice promoted)**: Regime A only. Cycle
  time dominated by operator reflection and paraphrase fan-out.
  Throughput low by design (mitigates F25 design starvation by
  *not* spawning busy-work; the design starvation failure mode is
  re-cast as a *property of the regime*, not a failure).
- **Day T₁ to day ~T₂**: Regime A + Regime B run concurrently;
  Regime B picks up promoted slices while Regime A continues to
  expand the durable spec. The factory's productive output (Regime B
  artifacts) ramps up as more slices promote.
- **Day T₂ onward**: Steady-state. Regime A continues for new slices
  (post-MVP evolution per D2 work-unit-class) but the dominant
  throughput is Regime B. Knowledge accumulation can begin once
  enough Regime B cycles exist to provide evaluable patterns; F8 / F55
  apply.
- **Regime transition trigger.** The transition is not time-based; it
  is *slice-coherence-based*. A slice promotes when an end-to-end
  scenario passes through it. This is the methodology's answer to
  "when is the spec ready" — not when complete, but when a slice is
  end-to-end coherent.

### 5.5 What the cold-start does NOT do

- Does not attempt to derive the full spec before any code is written
  (refutes the phase-gated Foundry shape for greenfield).
- Does not attempt to spawn N parallel candidate implementations from
  the first intent (refutes Tournament for cold-start; F60 parallel-
  cycle compounding error is acute when cycle-error-rate is unknown).
- Does not auto-import adjacent-domain exemplars into the durable
  spec (they inform the operator, not the cycle).
- Does not accumulate knowledge in `docs/solutions/` until Regime B
  has been running long enough to evaluate the knowledge against
  outcomes (F8 / F55).

---

## §6 What this track is NOT trying to be

- **Not a substrate design.** §1.3 *requires* substrate properties; it
  does not design them. Phase 4 decides whether the substrate is
  greenfield-only or shared with brownfield.
- **Not a brownfield architecture.** Brownfield's existing-codebase
  anchor (UC4 second clause) changes the cycle shape fundamentally
  (issue-shaped queue per OQ-B4, scenarios inherited from codebase per
  CTR-B5). This track does not try to address that.
- **Not a unified architecture.** This is the greenfield methodology
  axis. The 3 both-mandates tracks per D1 have the unified mandate;
  this track does not.
- **Not comprehensive on the corpus.** This track is strong on the
  methodology-first axis for greenfield. Whole sub-corpora (Gas City
  substrate, OpenHands V1 substrate audit, language-as-harness) are
  cited only where the cycle requires them; their fuller substrate
  implications are for other tracks (substrate-first) and Phase 4.
- **Not a tournament, attractor, or compound-atelier rebrand.** The
  cycle is novel in treating Regime A as a first-class regime with its
  own gates, judges, and exit criteria. The closest corpus analog is
  El Kaim's intent→decision→spec→control→feedback chain (report 14)
  with the spec-malleability dimension added.

---

## §7 Open questions surfaced by this track

- **OQ-T1.** *Slice coherence as the Regime A → Regime B transition
  criterion is operationally underdefined.* "End-to-end scenario
  passes through the slice without intent gap" is a verbal criterion;
  a substrate-implementable check is open. Candidate: the paraphrase-
  divergence test re-run at slice scope must agree across N
  paraphrasers; if it does, the slice is coherent. This needs
  empirical calibration.

- **OQ-T2.** *Paraphrase fan-out cost vs cost ceiling (D-5)
  interaction is concrete and unresolved.* If Regime A's per-cycle
  cost is Nx the single-cycle cost (where N is the paraphrase fan-out),
  and D-5 caps the budget, then the cycle's throughput is sharply
  bounded. CTR-E1 (Cherny $100K+/month vs $500–$5000/day) gives a
  10× range with no methodology-side resolution. This track's
  paraphrase-divergence step exacerbates the cost question by making
  it methodology-load-bearing, not optional.

- **OQ-T3.** *The Regime A → Regime B handoff requires a substrate
  protocol that does not exist in the corpus.* The closest analog is
  C16 trajectory replay (Round-2), but slice-promotion is a
  spec-layer transition, not a runtime replay. Phase 4 substrate
  decision: does this need a new primitive, or can it be expressed
  on top of trajectory + holdout?

- **OQ-T4.** *Cross-model paraphrase divergence (per F46) presumes
  multi-provider access; how does this interact with OQ-B8 (provider
  abstraction)?* The track requires *capability*, not a specific
  abstraction. But if the corpus' RouterLLM-vs-provider-aligned-
  profiles cleavage (CTR-C4) resolves toward per-provider profiles,
  the paraphrase step's cost rises (separate harnesses per provider).

- **OQ-T5.** *The two-regime split is itself a falsifiable design
  claim.* A single-regime greenfield architecture might exist that
  carries spec-malleability through the whole cycle without the
  promote/reverse distinction. This track *asserts* the split is
  productive; a Phase-3 adversarial pass could attack on grounds that
  the malleable phase should not have a defined exit (continuous
  Regime A only). Counter-argument: F40 last-mile drift is critical for
  greenfield exactly because nothing ever transitions to "shipped"; the
  split is the answer to F40.

- **OQ-T6.** *The "biggest" open question this track surfaces:* whether
  paraphrase divergence is actually adequate as the F37 (silent
  contradictory-prompt collapse) defense, or whether the underlying
  empirical anchor (Larbi MCC ≤ 0.55) generalises to the multi-
  paraphraser case in ways the corpus does not yet measure. If
  paraphrase divergence has its own MCC ceiling for contradiction
  detection, the cycle's central defense fails and Regime A's exit
  criterion is unsafe. This is empirically testable but currently
  unmeasured in the corpus; flagged for Phase-8 lean-evaluation.

---

*End of greenfield-methodology-first.md.*
