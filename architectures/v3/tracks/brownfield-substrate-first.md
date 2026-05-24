---
track: brownfield-substrate-first
axis: substrate-first
mandate-scope: brownfield
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
based-on-date: 2026-05-24
---

# Brownfield, Substrate-First

A Phase-2 architecture track. Strong on one axis (substrate-first) for one
mandate (brownfield); deliberately not comprehensive. The seven other
parallel Phase-2 tracks are the divergence; merging happens in Phase 3.

---

## §0 Axis declaration and defense

**Axis.** Substrate is the primary organizing principle for the brownfield
mandate. The brownfield factory's design begins from the substrate
primitives that ingest the existing codebase, its tests, its dependency
graph, its runtime telemetry, and its issue/PR history — and treats those
ingestion-and-maintenance primitives as the load-bearing investment. The
methodology layer is a thin overlay that consumes substrate-produced views
of the existing system; it does **not** own the reading-and-indexing
discipline.

**Why substrate, not methodology, for brownfield.** Three substrate-first
reasons specific to this mandate:

1. **The pre-existing implementation is the primary input** (UC2; UC4's
   "analyzing what is there and growing it"). Whatever methodology a
   brownfield factory runs, every cycle's first operation is *reading the
   system as it currently exists.* That read is non-trivial: it requires a
   codebase index, a dependency graph, a tests-and-coverage view, a
   runtime-telemetry surface, and a history-of-prior-changes record. If
   these are methodology-owned, every cycle re-implements them. If they
   are substrate-owned, the methodology layer becomes a consumer of a
   well-known set of queries — and *that* is what makes "different
   methodologies on shared substrate" tractable for the unified D1 search.
2. **The brownfield codebase is itself the scenario holdout** (CTR-B5,
   CTR-G2; D-2 fragile-default). When scenarios live in the existing
   system (production traces, existing tests, observed behavior), the
   substrate is the only place to enforce holdout discipline (D-4): an
   in-codebase scenario can leak to a builder agent if the substrate does
   not partition reads by role. Methodology-only enforcement of holdout
   on in-codebase scenarios is structurally impossible.
3. **The lethal-trifecta is constitutive of brownfield**, not optional
   (F12 brownfield-critical; F33 brownfield-critical; F44
   brownfield-critical; F56 brownfield-critical). Brownfield agents
   necessarily touch production data, production credentials, deploy
   paths, and live tests. Per F44, the perimeter must be substrate-default
   (production-scissors-off, read/write asymmetric), not per-Claw
   discipline. F53 (voluntary-discipline fragility) generalizes the
   argument: any control assumed to be operator-applied or methodology-
   applied breaks under the time-pressure conditions where it is most
   needed. The trifecta closure has to be in the substrate.

**Pre-respond to Phase-3 adversarial pass (anticipated attacks).**

- *"Substrate-first reifies a particular substrate vendor (Gas City /
  OpenHands / Codex). UC6 explicitly archived those recommendations."*
  Response: this track names substrate **primitives the brownfield factory
  must have**, not substrate *implementations.* The corpus offers
  candidate implementations (CTR-C5: OpenHands+Overstory vs. Gas City) and
  the v3 work is explicit that the choice is a Phase-5 ADR. What is
  load-bearing here is the *primitive set*, not the chosen vendor.
- *"You're smuggling Round-2 'substrate-heavy + thin-methodology' as
  given."* Response: CTR-C2 explicitly contests this for both-mandates
  search; this track is brownfield-only and the corpus' brownfield-
  specific signals (F20 brownfield-critical, F34 brownfield-critical, F35
  brownfield-high, F58 brownfield-high, F61 brownfield-high) converge on
  invariant-preservation and integration-discipline failures that
  per-cycle methodology cannot catch. Substrate-heavy is the brownfield-
  specific conclusion, not a Round-2 inheritance.
- *"You're ignoring methodology-first brownfield possibilities — Compound
  Engineering's `docs/solutions/` is the corpus' strongest brownfield
  methodology anchor."* Response: this track does not exclude Compound-
  Engineering-shaped methodologies; it requires that Compound's knowledge
  store, its `discovered-from` edges (report 38 Beads anchor), and its
  panel-review topology run *on top of* a substrate that owns the
  codebase index, dependency graph, holdout enforcement, and trifecta
  closure. Compound-as-methodology is compatible with this track;
  Compound-as-the-whole-design is what this track rejects.
- *"Substrate-first means upfront-heavy and a slow brownfield bootstrap."*
  Response: the brownfield "bootstrap" is reading the existing system, and
  the substrate does that work *once per codebase* (incrementally
  maintained thereafter). Per-cycle methodology cost is reduced. This is
  the brownfield analog of the greenfield cold-start problem (CTR-G3);
  this track explicitly does *not* treat them as symmetric — see §5.
- *"You're rejecting Schillace's 'Tempting-Wrong-Hybrid'
  warning — wrapping LLMs in deterministic controls is the trap."*
  Response: F52 names the trap as accreting *control-layer* wrappers
  around the LLM to escape randomness. This track's substrate does not
  wrap the LLM's reasoning; it owns *non-LLM* facts about the codebase
  (the dependency graph is a graph, not an LLM judgment) and *frames* what
  the LLM reads. That is harness-and-perimeter discipline, not the
  hybrid F52 warns against.

**Defended sub-axis.** Within "substrate-first for brownfield," the
specific sub-axis is **codebase-and-runtime as primary substrate inputs**.
This sub-axis rejects two alternative framings: (a) spec-as-primary-input
(which is greenfield-shaped per UC4 and F39); (b) issue-queue-as-primary-
input (which is one valid methodology overlay per OQ-B4 but presupposes
the codebase has already been read once to make the issues actionable).

---

## §1 Architecture sketch

A brownfield substrate-first architecture has **five substrate primitive
classes** the methodology layer consumes, plus a **thin methodology
overlay** that picks a per-cycle work unit and composes substrate queries
into a change.

### 1.1 Substrate primitive classes (the load-bearing layer)

**S-1. Codebase Index (incremental).** A queryable, incrementally
maintained representation of the existing code: symbols, definitions,
references, call graph, module boundaries, type information where
available. Updated on every commit; queryable by agent tools. Without
this, every cycle's agent re-greps. The brownfield F21 (context-window
exhaustion, brownfield-critical) is unavoidable without a substrate-side
index that returns *just the relevant slice*; agents that try to ingest
the codebase whole saturate context (F61, brownfield-high).

**S-2. Dependency-and-Impact Graph.** Per-symbol and per-module
dependency edges; per-change blast-radius computation. Required to make
F34 (cross-layer drift, brownfield-critical) and F35
(federation-as-family drift, brownfield-high) addressable: an agent
proposing a change must surface "what else does this touch" before
shipping. Methodology cannot enforce this without the substrate having
the graph; substrate cannot help unless it owns the graph.

**S-3. Runtime/Telemetry Ingestor.** Production traces, observed
behavior, OpenTelemetry events, error rates per module, hot paths. This
is the corpus' canonical answer to "brownfield's scenarios live inside
the codebase" (CTR-B5, CTR-G2). The substrate exposes these as
*queryable* by agent tools but *partitioned by role* — builder agents
cannot read holdout telemetry; only the V&V agent role can. This is
substrate-enforced holdout discipline (D-4) generalized to telemetry-
as-scenario.

**S-4. Change-History/Attribution Store.** Per-commit, per-PR, per-issue
attribution; per-agent and per-model attribution for prior cycles (F14,
widened to forensic reconstruction). Required for F35 (federation drift),
F43 (RSI Board-Visibility Gap, brownfield-high), F54 (goal subversion,
brownfield-critical), and F58 (runtime/design-time compliance split,
brownfield-high). The store is append-only and signed (mitigating F32
mail-injection / unsigned coordination).

**S-5. Perimeter / Trifecta-Closure Layer.** Production-scissors default
off (F44); read/write asymmetric (R1 per report 32 hardening rules);
sandboxed (followup 08 CaMeL-class typed-interpreter boundary, with the
~7-point utility tax accepted per CTR-E6); cross-model judge available
(F46, F1 brownfield-high); guard-bypass detection (F56). All trifecta
closures are substrate-default rather than per-Claw discipline. F53
(voluntary discipline fragility) is the explicit argument against putting
these closures in methodology.

Plus the universal substrate primitives the brief assumes will land in
Phase 4 (sandbox runtime, trajectory capture per D-7, cost ceilings per
D-5, watchdog tiers per D-6 — see §4 on §4 defaults).

### 1.2 Methodology overlay (the thin layer)

The methodology layer **does not own**: code indexing, dependency
analysis, telemetry ingestion, attribution, or perimeter enforcement.
What it owns:

- **Work-unit selection.** Picks one of the OQ-B4 shapes — issue,
  change-request-against-spec, or codebase-evolution proposal — and
  frames the cycle. This track is mandate-strong but axis-agnostic on
  OQ-B4: the substrate supports all three shapes; the architecture
  chooses per-deployment.
- **Per-cycle composition.** Composes substrate queries into a change
  plan: "given S-1's view of these symbols, S-2's blast radius, S-3's
  hot-path telemetry, S-4's prior-change context — propose a change."
- **Per-cycle V&V.** Runs the cross-model judge (F46), checks the
  proposed diff against S-2's impact predictions, checks acceptance
  against the substrate-partitioned holdout slice of S-3 (D-4
  generalized).
- **Knowledge promotion.** Decides what becomes a persistent skill /
  pattern / knowledge entry (Compound-Knowledge-shaped, followup 11
  brownfield-primary; Beads `discovered-from` edges from report 38).

### 1.3 Cycle shape

A single brownfield cycle:

1. Substrate maintains S-1..S-4 continuously (incremental on every push).
2. Methodology picks a work unit (S-4 issue store; or human-injected).
3. Methodology queries S-1 for relevant code, S-2 for blast radius, S-3
   for relevant telemetry partitioned by builder-role.
4. Builder agent (in S-5 sandbox, with substrate-typed perimeter)
   proposes a diff.
5. Cross-model judge (F46 mitigation) reviews; substrate enforces same-
   change cannot be its own judge (F1, F27, F48 brownfield-high).
6. Methodology checks diff against S-2's predicted blast radius;
   discrepancies escalate.
7. Substrate logs to S-4 with per-agent, per-model attribution.
8. Knowledge-promotion step decides what to persist (Beads
   `discovered-from` edge to S-4 record).

---

## §2 How this addresses load-bearing concerns

### 2.1 Lights-out / L5 tension (brief §2.1, OQ-B1)

Brownfield substrate-first does **not** assert architecture-wide L5. It
adopts the brief's option (c) + (b) combination: lights-out is declared
*per work-unit-class* rather than uniformly. Substrate-first makes this
declaration cleanly possible because the substrate's S-2 (impact graph)
and S-3 (telemetry) provide *measurable per-cycle inputs* to a
classification: a change with small blast radius, in-distribution
telemetry, and prior-cycle precedent in S-4 is automation-eligible;
a change crossing module boundaries, hitting cold-path telemetry, or
violating S-2's predicted-blast-radius is escalation-required.

Per CTR-A5 (Jaymin's brownfield L3 ceiling): this track accepts that the
*default* brownfield work-unit-class operates around L3-L4 (matching
brownfield-critical severities of F12/F33/F56) and the substrate is what
makes L4 reachable for the specific work-unit-classes where S-2/S-3 give
confident inputs.

The vocabulary mapping (CTR-A4): this track treats "lights-out" per
glossary §0 (no human in per-cycle inner loop for automation-eligible
work units), not as identical to Jaymin's L5. CTR-A1 dissolves under the
glossary definition for the work-unit-classes where substrate evidence
clears the bar; remains undissolved (and thus operates at L3-L4) for the
classes where it does not.

### 2.2 UC4 hypothesis (brownfield as code-archaeological)

This track is the *substrate-side restatement* of UC4. UC4 names code-
archaeology as the brownfield discipline; this track says: code-
archaeology cannot be a methodology — it requires the substrate to
maintain the index, graph, telemetry, and history that "analyzing what
is there" presupposes. CTR-G4 (code-as-opaque vs. code-as-readable
archaeology) is decided by the substrate owning the readability
(S-1 + S-2).

### 2.3 OQ-B4 (unit of work)

Issue (Atelier), change-request-against-spec (Refinery), or codebase-
evolution proposal (novel shape): the substrate supports all three. The
substrate's S-4 (attribution + change history) is the issue store; S-2 +
S-3 are the spec-evidence base for change-request shapes; S-1 + S-2
together support codebase-evolution proposals that read the system as
graph. *The architecture defers OQ-B4 to per-deployment methodology
choice.*

### 2.4 OQ-B6 (empirical bars)

This track accepts Jaymin's K=5 and prompt-paraphrase bars as one
candidate set (per glossary §0, threshold definitions). The substrate's
S-2 / S-3 evidence is the per-cycle input that lets the methodology
*compute* whether a specific work unit clears the bar for automation,
rather than declaring it architecturally.

### 2.5 OQ-B8 (provider-property requirements)

CTR-C4 (RouterLLM vs. provider-aligned profiles): this track requires the
substrate to declare *provider-property requirements* (model-family
diversity for the cross-model judge in step 5 — F46 mitigation) without
mandating a router-style abstraction. The judge slot needs a different-
family model; the builder slot may be configured per-deployment. This
satisfies F1/F27 mitigation at the architectural level (CTR-D4 cross-
model topology side) without committing to RouterLLM as substrate.

### 2.6 OQ-B9 (methodology evolution)

CTR-C3 (self-improvement as methodology pattern vs. substrate primitive):
in this track, methodology evolution is **methodology-owned**. The
substrate owns the *records* (S-4) and the *knowledge store*
(Compound-Knowledge-style, followup 11) but the rules for promoting,
retiring, and reorganizing methodology patterns live in the methodology
layer. This is consistent with the substrate-thin-methodology stance
applied carefully: substrate owns durable facts; methodology owns
durable practices that change.

### 2.7 OQ-B10 (Phase-7 generosity)

Process discipline; no architectural commitment here.

### 2.8 Brownfield-specific F-modes

| F-mode | brownfield-severity | substrate primitive that addresses it |
|---|---|---|
| F12 (lethal trifecta) | critical | S-5 |
| F20 (maintenance asymmetry) | critical | the whole architecture, by being brownfield-shaped |
| F21 (context exhaustion) | critical | S-1 (return only relevant slice) |
| F33 (LLM-judge defeat) | critical | S-5 deterministic perimeter; cross-model judge in cycle step 5 |
| F34 (cross-layer drift) | critical | S-2 (impact graph surfaces architecture/standards layer violations) |
| F44 (production-scissors default) | critical | S-5 (substrate-default closure) |
| F54 (goal subversion across cycles) | critical | S-4 (per-cycle attribution; immutable signed log) |
| F55 (behavioural drift / self-reference) | high | S-3 (production telemetry as out-of-distribution ground truth) |
| F56 (guardrail-bypass under stress / Replit) | critical | S-5 substrate-default (not instruction-guardrail) |
| F58 (runtime/design-time compliance split) | high | S-4 + S-3 together provide runtime compliance evidence |
| F60 (parallel-cycle compounding error) | high | S-2 substrate-enforced parallelism cap by overlapping impact |
| F61 (context fragmentation across agents) | high | S-1 + S-2 as shared canonical views |

### 2.9 Specific contradictions this track takes a position on

- **CTR-B5 / CTR-G2** (scenarios inside vs. outside codebase): inside,
  substrate-partitioned-by-role. D-2 default is challenged for brownfield
  (see §4).
- **CTR-C2** (substrate-heavy vs. UC4 methodology-deep): substrate-heavy
  is the brownfield-specific answer; track is silent on whether this
  scales to a unified architecture (that's the D1 unified tracks' job).
- **CTR-C4** (RouterLLM vs. provider-aligned): provider-property
  *requirements* declared, abstraction *not* assumed. Avoids choosing.
- **CTR-D4 / CTR-D7 / CTR-D8** (judge diversity): cross-model judge for
  F1/F27/F46 mitigation; Anthropic same-model-fine claim acknowledged but
  not adopted as architectural default given F46 + CTR-D8's Tournament-
  spec corpus support.
- **CTR-F1** (factory vs. company / Brier counter-metaphor): this track
  is factory-shaped because the substrate's read-graph-perimeter
  primitives are factory-shaped infrastructure. Brier's pace-layer
  framing is absorbed as the substrate's **layered fact store** (S-1
  fastest, S-2 medium, S-3 medium-slow, S-4 slow, S-5 enforced
  invariants slowest) — pace-layer-as-substrate, factory-as-methodology.
- **CTR-G4** (code-as-opaque vs. code-as-archaeological): code-as-
  archaeological; substrate owns the reading.
- **CTR-H13** (Schillace code-review-as-firing-offense vs. substrate-
  vendor Auto-Review): adopt the substrate-vendor side (Anthropic Auto-
  Review, Codex Auto-Review) as the cross-model judge in cycle step 5.

---

## §3 Citations and grounding

Per the brief and contradictions.md citation discipline, citations target
underlying corpus material, not bias-guard `WEAK-N` / `MISSED-N` IDs.

**User constraints anchoring this track:** UC1 (lights-out), UC2
(brownfield co-equal), UC4 (code-archaeological framing).

**Contradictions this track engages:** CTR-A1, CTR-A4, CTR-A5
(L5/lights-out cluster); CTR-B5, CTR-G2 (scenarios inside codebase);
CTR-C2 (substrate-heavy vs. methodology-deep); CTR-C4 (RouterLLM vs.
provider profiles); CTR-D4, CTR-D7, CTR-D8 (judge diversity); CTR-E6
(CaMeL utility tax); CTR-F1 (factory vs. company); CTR-G1, CTR-G3, CTR-G4
(brownfield asymmetries); CTR-H13 (Schillace vs. substrate-vendor
auto-review).

**F-modes load-bearing for this track** (sourced from
failure-modes-v3.md): F1, F12, F14, F20, F21, F27, F32, F33, F34, F35,
F44, F46, F48, F52, F53, F54, F55, F56, F58, F60, F61.

**Reports cited (corpus-inventory.md anchors):**

- Report [`01`](../../../research/01-strongdm-factory.md) — software-factory anchor; no-human-review posture this track positions against for brownfield specifically.
- Report [`03`](../../../research/03-every-compound-engineering.md) — Compound Engineering methodology; brownfield-primary per inventory; this track allows Compound-as-methodology-overlay.
- Report [`05`](../../../research/05-simon-willison.md) — lethal-trifecta framing (F12 anchor).
- Report [`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) — Jaymin's threshold matrix; brownfield-L3-ceiling claim (CTR-A5); F21/F22/F23/F24/F25/F26 anchors.
- Report [`11`](../../../research/11-openhands-substrate-audit.md) — trajectory capture (D-7); RouterLLM as one provider-routing example (CTR-C4); not a normative dependency.
- Report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) — typed spec objects + ArchitectureSpecification (slow-pace-layer in S-2/S-5 architecture-invariant region).
- Report [`18`](../../../research/18-openai-codex-substrate.md) — `.rules` DSL, OTEL five-event export, Auto-Review subagent (S-4 + S-5 + cycle-step-5 anchors).
- Report [`22`](../../../research/22-academic-foundations.md) — SWE-bench Verified as brownfield-shaped (per inventory CHALLENGE-8); V&V baseline.
- Report [`23`](../../../research/23-anthropic-engineering-trilogy.md) — Claude Code sandboxing; Skills schema (S-5 + scaffold); Auto-Review subagent (CTR-H13).
- Report [`28`](../../../research/28-schillace-sunday-letters.md) — F52 (Tempting-Wrong-Hybrid) pre-respond; Amplifier internals as substrate-component reference.
- Report [`30`](../../../research/30-cognitive-escrow.md) — F42, F53 (voluntary-discipline fragility — central to substrate-default argument).
- Report [`31`](../../../research/31-caremark-rsi-board-exposure.md) — F43 (board-visibility), F54 (goal subversion), F55 (behavioural drift); brownfield-critical for the S-4 attribution requirement.
- Report [`32`](../../../research/32-shapiro-completion-chat-agent-claw.md) — five hardening rules (R1-R5) operationalizing S-5; F44 anchor.
- Report [`34`](../../../research/34-lenny-howiai-personal-harnesses.md) — F46 cross-model review (kevin/carl); cycle-step-5 anchor.
- Report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md) — Boxy / CI-as-substrate-bottleneck; Stripe 1,300 PRs/week brownfield industrial-scale anchor; supports the substrate-first conclusion at industrial scale.
- Report [`38`](../../../research/38-gas-systems-substrate.md) — Beads `discovered-from` edge as candidate S-4 knowledge primitive; substrate-vs-application split as one concrete substrate-first instantiation (CTR-C5 acknowledged; choice deferred).
- Followup [`08`](../../../research/followup/08-security-primitives.md) — CaMeL paper-body, ~7-point utility tax (CTR-E6 accepted); S-5 anchor.
- Followup [`10`](../../../research/followup/10-governance.md) — AILCCP, BCG Five Pillars, Replit prod-DB wipe (F56 anchor); brownfield-relevant.
- Followup [`11`](../../../research/followup/11-compound-knowledge.md) — Compound Knowledge plugin (brownfield-primary per inventory CHALLENGE-7); typed knowledge classification supports methodology-side knowledge promotion.
- Followup [`12`](../../../research/followup/12-brier-pace-layers.md) — pace-layer absorption into substrate fact-store layering; counter-metaphor engaged (CTR-F1).

---

## §4 §4 defaults: accepted vs challenged

Per D3, every Phase-2 track marks all 7 defaults.

- **D-1 (Specs are durable, version-controlled, human-curated)** —
  **accepted with justification**. For brownfield, "spec" includes the
  existing codebase (UC4) plus any intent layer the operator chooses to
  maintain. The durable-version-controlled-human-curated property
  applies; the *content* differs (report 14 typed spec objects on top of
  S-1's view of the existing code). Cites report 14, report 35 (Markdown
  specs as AFIS strategy-3 industrial anchor).
- **D-2 (Scenarios live outside the codebase as a holdout set)** —
  **challenged**. Brownfield's scenarios live *inside* the codebase
  (CTR-B5, CTR-G2): existing tests, production traces, runtime telemetry
  (S-3). The default-as-stated does not apply; the underlying *holdout
  discipline* (D-4) does apply but is enforced by substrate role-
  partitioning of S-3 reads rather than by file-system location. Cites
  CTR-B5, CTR-G2; failure-modes F20 / F34 / F35 reasoning.
- **D-3 (Agent = Model + Harness)** — **accepted with justification**
  *with a flag*. The brownfield architecture decomposes cleanly into
  model + harness for builder / judge / scout agents. CTR-C10 (natural-
  language-as-harness-parameter from report 37) is acknowledged as a
  fragility but not architecturally consequential at the substrate-first
  level (substrate doesn't model NL register; methodology may add it
  later). Cites Round-2 C10 corpus; CTR-C10 caveat.
- **D-4 (Holdout discipline is substrate-enforced, not methodology-
  optional)** — **accepted with justification**, and *expanded*. In this
  track, holdout discipline applies to telemetry-as-scenario (S-3 read
  partitioning), not just file-system scenario directories. Substrate
  enforcement is exactly the point. Cites F28 (holdout leakage).
- **D-5 (Hard cost ceilings non-optional in CI)** — **accepted with
  justification**. Brownfield's parallelism (Stripe 1,300 PRs/week per
  report 35; Cherny $100K/month per CTR-E1) makes cost ceilings load-
  bearing. The substrate's perimeter (S-5) is the enforcement point.
- **D-6 (Tiered watchdog: Daemon/Triage/Patrol)** — **accepted with
  justification**. F22 (zombie agents, brownfield-high), F23 (stalled-
  vs-thinking, brownfield-medium), F56 (guardrail-bypass under stress,
  brownfield-critical) all require the tiered watchdog. Substrate-owned.
- **D-7 (Trajectory capture is cheap and production-tested)** —
  **accepted with justification**. The S-4 attribution store *requires*
  trajectory capture as substrate (per OpenHands V1 measurement context
  cited in glossary §0, not as normative dependency). CTR-E4 largely
  resolved.

---

## §5 Cold-start

**Brownfield: not mandatory per brief.** Stated explicitly: cold-start
(per brief §5) is a *greenfield* concern.

However, the brownfield analog is **legacy-ingestion** (CTR-G3) — day-0
bootstrapping of the substrate's S-1 through S-4 against an unfamiliar
existing codebase. This track names legacy-ingestion as a substrate-side
operation:

- **S-1 build:** index the codebase. One-time bulk pass; incremental
  thereafter.
- **S-2 build:** derive the dependency-and-impact graph. May require
  human-curated "module boundary" hints for codebases without clean
  module boundaries.
- **S-3 build:** connect to existing telemetry / observability pipeline.
  If none exists, the factory's first work-unit-class becomes
  *adding telemetry* — a self-bootstrap step.
- **S-4 build:** ingest git history; tag pre-factory commits as
  unattributed. From day 0 forward, attribution is substrate-enforced.
- **S-5 build:** declare the trifecta perimeter (production-scissors
  off; sandbox configuration; cross-model judge slot). This is *upfront
  policy* and applies before the first cycle.

CTR-G3 explicitly: this track does **not** claim legacy-ingestion is
symmetric to greenfield cold-start. Legacy-ingestion is a substrate
*setup* (one-time, bounded); greenfield cold-start is a methodology
*problem* (recurring, ill-defined, per brief §5). The two are different
shapes.

---

## §6 What this track is NOT trying to be

- **Not a unified architecture.** Greenfield is *not* in scope; this
  track does not address spec-malleability, cold-start, day-0 priors
  beyond the legacy-ingestion analog. The D1 unified tracks have that
  brief.
- **Not a methodology proposal.** OQ-B4 (issue / change-request /
  codebase-evolution) is explicitly deferred to methodology overlay
  choice; substrate supports all three.
- **Not a substrate-vendor recommendation.** CTR-C5 (OpenHands+Overstory
  vs. Gas City) is unresolved; this track names the primitive set, not
  the implementation. Phase-5 ADRs choose.
- **Not a regime declaration for brownfield as a whole.** Per §2.1, the
  lights-out / L4 / L3 classification is *per work-unit-class*, computed
  per-cycle from substrate evidence — not a track-level declaration.
- **Not a comprehensive failure-mode-mitigation catalog.** Phase-2
  discipline: strong on axis, not comprehensive. F-modes that don't
  intersect substrate-first brownfield (F29 talent pipeline; F35 in its
  greenfield-rarity reading; F50 architecture/spec confusion at greenfield)
  are not addressed here.
- **Not a refutation of Compound Engineering, Refinery, or Atelier as
  methodologies.** Any of them can run on this substrate; the track is
  silent on which is best for which deployment.

---

## §7 Open questions surfaced by this track

- **OQ-T1 (substrate-vendor choice for brownfield).** Per CTR-C5, the
  corpus has two substrate candidates (OpenHands+Overstory; Gas City)
  and the brief is explicit that vendor choice is operator-time. But
  the brownfield S-1/S-2 primitives are not equally well-served by both
  candidates: OpenHands measurement context is single-cycle replay; Gas
  City's Beads `discovered-from` edge is closer to S-4 needs.
  Substrate-first analysis suggests the brownfield-fit vendor evaluation
  is *different* from the greenfield-fit one. Phase-5 work.
- **OQ-T2 (S-2 dependency-graph maintenance for polyglot codebases).**
  S-2 is straightforward for single-language codebases with strong
  static analysis; harder for polyglot codebases without unified
  semantics (corpus does not directly address). Per F45 (Language-as-
  Harness Mismatch), the language choice for new code interacts with
  S-2's maintainability. Brownfield codebases generally cannot change
  language; the architecture has to accept S-2 fidelity will vary.
- **OQ-T3 (the "telemetry doesn't exist yet" failure mode for S-3).**
  Many brownfield codebases (especially mid-market per Kahana report
  31) lack production telemetry. The substrate's self-bootstrap step
  (add telemetry as first work-unit-class) needs to be safe to run at
  L3 (operator-gated), but the cycle that adds telemetry has none of
  the S-3 evidence to clear an L4 threshold. The substrate's perimeter
  must accept a degraded-S-3 starting condition.
- **OQ-T4 (cross-model judge availability and cost).** F46 requires a
  different-family model in cycle step 5. The substrate's provider-
  property declaration (per OQ-B8 / CTR-C4) makes this a requirement,
  but the cost (per CTR-E1's $100K/month anchor; CTR-E6's 7-point
  utility tax) compounds. Cross-model-judge-for-every-cycle is the
  default; whether sample-rate cross-model judging satisfies F1/F27
  mitigation is an empirical question the corpus does not answer.
- **OQ-T5 (what if D-2 challenge cascades to D-4?).** D-2 is challenged
  for brownfield; D-4 is accepted-and-expanded. But if scenarios are
  inside the codebase and holdout is enforced by substrate read
  partitioning, the substrate is now load-bearing for something
  Round-2 promoted as a methodology discipline. This may surface
  substrate-vs-methodology boundary issues for Phase 4 that the
  current track frames optimistically.
- **OQ-T6 (legacy-ingestion as bounded one-time or as continuous).**
  §5 frames legacy-ingestion as bounded substrate setup. But brownfield
  codebases that absorb large external dependencies (vendored libraries,
  acquired-company code) face *recurring* legacy-ingestion events. The
  architecture has not declared whether these re-trigger the full S-1..
  S-4 bootstrap or are handled incrementally.

---

*End of brownfield-substrate-first.md.*
