---
based-on-commit: c495dc9
based-on-date: 2026-05-10
---

# Architecture 3 — The Phase-Gated Foundry
## A Software Factory Built on Pre-Agile Methodology with Hour-Scale Cycle Times

**Version:** 0.2
**Status:** Draft architecture proposal
**Lineage:** Pre-agile structured methodologies (Waterfall, V-Model, RUP, Cleanroom Software Engineering, Stage-Gate) reconsidered for an environment where agent-driven implementation collapses cycle time from months to hours; refined with findings from `research/00-synthesis.md` (v2)
**Stance in one sentence:** *Formal phases, structured exchanges, and independent verification — rejected by Agile because they were too slow for humans — become the right shape when agents make them fast.*

---

## 0. Revision notes (v0.2)

Changes from v0.1 driven by the v2 research pass:

- **The "looking-the-part hazard"** (Simon Willison, May 6 2026: a repo with 100 commits and tests no longer proves care) is folded into the failure-mode coverage table under F7 (normalization of deviance). This architecture's defect-of-origin attribution and Cleanroom no-debugging discipline are particularly strong defenses against this hazard — surface-quality signals (commits, tests, lint-clean) become *outputs* of the structured process rather than independent proxies for quality.
- **Independent V&V** policy is reinforced by the v2 finding that Simon's stance on human review is eroding under load (May 6 post). The Foundry's independent V&V agents (different model family from construction) are the architectural fix for what would otherwise become normalization-of-deviance drift. The architecture's claim that "V&V on a different model family than construction" is a structural defense is now better supported.
- **No structural changes** to the six-phase cycle, the V-Model pairings, or the role catalog.

---

## 1. Core thesis

Agile methodologies were a response to a specific constraint: human-driven implementation took weeks to months per cycle, so a formal Waterfall phase that consumed two months of requirements work before any code was written was an enormous gamble. If the requirements were wrong (and they almost always were), the cost of discovering it after implementation was catastrophic. Agile's iterative, incremental loop existed to make wrong directions cheap to discover and cheap to correct.

The constraint has changed. With capable coding agents, an entire phase of work — requirements analysis, architecture decisions, detailed design, implementation, verification, validation — can complete in *hours* rather than *months*. The economic argument for Agile (avoid investing months in pre-coding work) no longer applies the same way. What was previously prohibitive (a full-stack waterfall pass before each release) is now affordable.

This architecture takes the structures Agile rejected — formal phases with typed entry/exit criteria, paired verification phases (V-Model), explicit traceability matrices, independent V&V, Cleanroom no-debugging discipline, structured stage-gate reviews — and runs them at hour scale. The bet: **the formal disciplines that produced extremely high quality in life-critical and safety-critical software (avionics, medical devices, nuclear control systems) become broadly applicable when the cycle time is short enough to absorb them.**

It is also the architecture most legible to organizations under regulatory pressure: each phase produces audit-trail-grade artifacts; each gate produces signed verdicts; each defect traces to a phase of origin.

---

## 2. The phase model

The Foundry runs six phases per cycle, executed in order. Each has a defined role, defined input artifacts, defined output artifacts, and a stage-gate review at its exit.

```
PHASE 1 — Requirements           ↔  PHASE 6 — Acceptance V&V
PHASE 2 — Architecture           ↔  PHASE 5 — Integration V&V
PHASE 3 — Detailed Design        ↔  PHASE 4 — Unit V&V
                ↓
            (between 3 and 4: Implementation, the only "construction" phase)
```

The V-Model pairing is structural: every design phase has a corresponding verification phase that runs *against artifacts from the paired design phase*, not against the implementation. This is what makes phase-of-origin defect attribution possible.

### 2.1 Phase 1 — Requirements

**Role:** Requirements Engineer Agent + Strategist (human)
**Input:** Strategy document, problem statement, constraints
**Output:** Software Requirements Specification (SRS)
**Stage-gate review:** Requirements Review Board (RRB) — pass/fail

The SRS is structured (not just prose):

- Functional requirements (FR-N) — what the system shall do
- Non-functional requirements (NFR-N) — performance, security, reliability, usability, etc.
- Interface requirements (IR-N) — external system contracts
- Constraints (C-N) — environmental, regulatory, economic
- Acceptance criteria (AC-N) — the externally observable success conditions, in Given/When/Then form
- Glossary — every domain term defined

Every requirement is **uniquely numbered, individually testable, and cross-references its source.** The Requirements Engineer enforces SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound) and flags any requirement that fails them.

The RRB review checks:
- Completeness (no silent gaps in named scope)
- Consistency (no two requirements contradict)
- Testability (every AC is automatable or has an explicit human-test designation)
- Traceability (every requirement traces to a strategy goal or non-goal)

### 2.2 Phase 2 — Architecture

**Role:** Architect Agent + reviewing humans/agents
**Input:** SRS
**Output:** Software Architecture Document (SAD)
**Stage-gate review:** Architecture Review Board (ARB) — pass/fail/conditional

The SAD captures:

- Component decomposition with explicit interfaces (Component-N, Interface-N)
- Data flow and control flow diagrams (typed nodes/edges)
- Technology choices with rationale and explicit rejected alternatives
- Cross-cutting concerns (logging, monitoring, secrets, deployment)
- A Requirements Traceability Matrix (RTM) — every FR/NFR maps to ≥1 component
- Risk register (known unknowns; mitigations or watch items)

The Architect Agent must produce an explicit Risk Register; arch decisions without risk identification fail the gate.

The ARB review checks:
- Architectural integrity (no circular dependencies; bounded coupling; clear interfaces)
- RTM completeness (no requirement orphaned)
- NFR realizability (the architecture has a credible path to every NFR)
- Risk acknowledgment (high-impact risks have mitigations or explicit acceptance)

### 2.3 Phase 3 — Detailed Design

**Role:** Designer Agent (one per component) + reviewer agents
**Input:** SAD, SRS
**Output:** Detailed Design (DD) per component
**Stage-gate review:** Design Review Board (DRB) — pass/fail per component

The DD captures, per component:

- Component-level data structures, types, schemas
- Algorithms (pseudocode for non-trivial logic)
- Error handling strategy
- Test scenarios per component (categorized: happy path, edge, error, integration)
- Stable Implementation Unit IDs (U-N) per atomic chunk of work
- Local invariants the component must preserve
- Explicit lists of what this component does NOT handle (scope boundaries)

The DD is **not** implementation. It is a contract the implementer must satisfy. Following compound-engineering's discipline: WHAT and the explicit decisions, not exact API signatures or step-by-step shell commands.

The DRB review checks:
- DD covers all component requirements from the SAD
- Test scenarios cover all acceptance criteria
- Error handling is exhaustive (every external interaction has a failure mode)
- Stable IDs are assigned and don't collide

### 2.4 Implementation (between Phase 3 and Phase 4)

**Role:** Implementer Agent (one per U-ID, parallelizable; isolated worktree per unit)
**Input:** DD (component-scoped)
**Output:** Code + unit tests + commit per U-ID
**No stage-gate** — the gate is Phase 4

The Implementer follows **Cleanroom discipline** (Mills/Linger/Hevner, IBM 1980s): the implementer does not run tests during construction. Instead the implementer reads the DD, writes code that mathematically satisfies the contract, and submits. The implementer is *not* allowed to debug. Defects discovered downstream return the work to the appropriate phase, never to a quick patch.

(Cleanroom's original argument was that debugging conditions developers to write defective code, then patch it; the discipline of "code by reasoning, not by trial-and-error" was empirically correlated with order-of-magnitude defect reductions in life-critical systems. With agents, the same logic applies: an agent that can patch will always reach for patches; an agent that cannot patch must reason carefully.)

### 2.5 Phase 4 — Unit V&V (paired with Phase 3 DD)

**Role:** Unit Verifier Agent (independent of Implementer; different model family)
**Input:** Code + DD
**Output:** Unit V&V Report
**Stage-gate review:** Unit Test Readiness Review (UTRR) — pass/fail per U-ID

Independent V&V is structural: the Verifier did not write the code, did not see the Implementer's chain-of-thought, and cannot ask the Implementer questions. It tests the code against the DD's test scenarios and against a corpus of *additional* scenarios it derives from the DD (negative tests, boundary tests, contract tests).

The Verifier produces:
- Pass/fail per scenario per U-ID
- A coverage report (every DD branch / every named test scenario / every named error path covered or explicitly waived)
- A defect report per failure with **phase-of-origin attribution**: did this defect come from Implementation (Phase 3.5), Detailed Design (Phase 3), Architecture (Phase 2), or Requirements (Phase 1)?

A defect attributed to a phase **returns the work to that phase.** No patches; the upstream artifact must be amended and the downstream phases re-run.

The UTRR gate cannot pass with any unwaived defect; waivers require explicit Operator sign-off and are recorded in the cycle's audit trail.

### 2.6 Phase 5 — Integration V&V (paired with Phase 2 SAD)

**Role:** Integration Verifier Agent
**Input:** Multiple components passing UTRR + SAD
**Output:** Integration V&V Report
**Stage-gate review:** Integration Test Readiness Review (ITRR) — pass/fail

Integration testing exercises the **interfaces and contracts** identified in the SAD, not the internals of components. The Integration Verifier tests:
- Every component-to-component interface (correct under normal operation, correct under partner failure)
- Every cross-cutting concern (logging emits as architected; secrets retrieved as architected; etc.)
- The full data flow described in the SAD
- The control flow described in the SAD

Defects attributed to the SAD return work to Phase 2, not Phase 3 or 3.5. (The implementer didn't violate the DD; the SAD was wrong.)

### 2.7 Phase 6 — Acceptance V&V (paired with Phase 1 SRS)

**Role:** Acceptance Verifier Agent + Operator (human, optional but recommended)
**Input:** System passing ITRR + SRS + scenario corpus
**Output:** Acceptance V&V Report
**Stage-gate review:** System Acceptance Review (SAR) — pass/fail

Acceptance testing runs the externally observable behavior against the AC-N criteria from the SRS, plus a separate scenario corpus authored by the human Strategist (held *outside* any tree the design phases could read — same holdout discipline as Architecture 1 and 4).

The Operator participates in the SAR review for any AC-N marked Human-Review-Required (typically presentation/usability concerns). Channel-2 review (the implementation is spec-compliant but not what the user wanted) is an acknowledged outcome of SAR; it returns work to Phase 1.

A defect attributed to the SRS returns work to Phase 1.

---

## 3. The Configuration Management discipline

Each phase produces typed artifacts. The Configuration Management (CM) Agent maintains:

- A version-controlled artifact tree per phase
- A **Traceability Matrix** (RTM) linking every requirement → architecture component → DD → U-ID → commit → test → finding
- A **Defect Database** with phase-of-origin attribution per defect
- An audit trail per cycle showing which artifacts entered each phase, which exited, and which gates passed

The RTM is the **single most important durable artifact** in this architecture. A requirement without a path through the RTM to a passed test is a requirement that has not been delivered. A test without a path back to a requirement is a spurious test. Both states fail the SAR gate.

### 3.1 Defect-of-origin table

Every defect carries an attribution determined by the V&V phase that surfaced it:

| Defect type | Phase of origin | Returns to | Cost ratio* |
|---|---|---|---|
| Code violates DD | Implementation (3.5) | Implementer (3.5) | 1× |
| DD insufficient given SAD | Detailed Design (3) | Designer (3) | 5× |
| SAD violates SRS | Architecture (2) | Architect (2) | 25× |
| SRS does not capture intent | Requirements (1) | Requirements + Strategist | 125× |

*The Cleanroom literature claims a roughly 5× cost multiplier per phase (Boehm and others have measured 10–100× in classical waterfall environments). Whether the ratio holds with agent-driven implementation is open empirical question; the architecture surfaces it as a metric to track.

The cost ratio is a **deterrent against shortcuts.** A team that discovers it spends 80% of its V&V time on Phase-1-attributed defects has a Requirements problem, not a coding problem. The architecture forces that conclusion to be visible.

---

## 4. RUP-style discipline × phase matrix

A pure waterfall has each discipline (requirements, design, implementation, test) confined to its phase. RUP (Rational Unified Process, late 1990s) recognized that disciplines bleed: some requirements work happens in Detailed Design, some test work happens in Architecture, some implementation work happens in Requirements (proof-of-concept code).

The Foundry adopts RUP's matrix view:

|   | Phase 1 (Req) | Phase 2 (Arch) | Phase 3 (DD) | 3.5 (Impl) | Phase 4 (Unit V&V) | Phase 5 (Int V&V) | Phase 6 (Acc V&V) |
|---|---|---|---|---|---|---|---|
| **Req discipline** | █████████ | ███ | █ | — | — | — | █ |
| **Design discipline** | ██ | █████████ | ████████ | █ | — | █ | — |
| **Impl discipline** | █ | █ | ██ | █████████ | █ | █ | — |
| **V&V discipline** | ██ (test plans) | ██ (arch verifications) | ████ (test scenarios) | █ | █████████ | █████████ | █████████ |
| **CM discipline** | ████ | ████ | ████ | ████ | ████ | ████ | ████ |

CM is constant across phases. V&V begins in Phase 1 (writing test plans) and intensifies in Phase 4–6. This is RUP's central insight: **disciplines start before their dominant phase and continue after it.** The agent assignments reflect this:

- The **Requirements Engineer** consults a **V&V Planner** in Phase 1 to ensure ACs are testable.
- The **Architect** consults a **V&V Architect** in Phase 2 to ensure interfaces are testable.
- The **Designer** writes test scenarios alongside the DD in Phase 3.
- The **Implementer** writes unit tests alongside code in Phase 3.5 (these are the V&V harness fodder, not the V&V itself).
- The **V&V Engineers** in Phases 4–6 *run independent tests* derived from upstream artifacts.

---

## 5. Iteration within phases

A phase is not a single linear pass; iterations are allowed within a phase before its gate. RUP names four cycle-level phases (Inception, Elaboration, Construction, Transition) that themselves contain iterations. The Foundry adopts the same idea at the artifact level:

**Within Phase 1 (Requirements):**
1. Initial draft from Strategist intent
2. V&V Planner checks AC testability; flags issues
3. Requirements Engineer revises
4. Repeat until V&V Planner clears
5. RRB gate

**Within Phase 2 (Architecture):**
1. Initial draft from SRS
2. Cross-cutting reviewers (security, reliability, performance) generate findings
3. Architect revises
4. RTM completeness check
5. ARB gate

**Within Phase 3 (Detailed Design):**
1. Component decomposition; one Designer per component
2. Designers run in parallel
3. Cross-component coherence check (interfaces match SAD)
4. DRB gate per component (parallel; not sequential)

**Within Phase 4 (Unit V&V):**
1. Unit Verifier runs against each U-ID's tests
2. Defects classified by phase of origin
3. Returns work to upstream phase if needed
4. Re-runs after upstream phase re-passes
5. UTRR gate

The architecture allows multiple iterations *within* a phase before its gate, but the gate is **all-or-nothing**: a single unwaived defect fails the gate.

---

## 6. Roles

The Foundry has more named roles than the other architectures because each phase has phase-specific responsibilities. Some roles can be filled by the same agent process configured differently; some must be structurally independent.

### 6.1 Construction-side roles

- **Strategist (human)** — owns the strategy document and the initial problem statement
- **Requirements Engineer Agent** — drafts SRS; enforces SMART criteria
- **Architect Agent** — draws decompositions, picks technologies, writes SAD with rationale and risks
- **Designer Agent** — produces DD per component (parallel across components)
- **Implementer Agent** — Cleanroom-disciplined; one per U-ID; isolated worktrees

### 6.2 V&V-side roles (structurally independent — different model family from construction-side)

- **V&V Planner Agent** — works inside Phase 1 to ensure SRS ACs are testable
- **V&V Architect Agent** — works inside Phase 2 to ensure SAD components are testable
- **Unit Verifier Agent** — runs Phase 4
- **Integration Verifier Agent** — runs Phase 5
- **Acceptance Verifier Agent** — runs Phase 6

The independence requirement: the V&V agent must not have read the construction agent's output during construction. It receives the artifact at the gate, with no access to the construction agent's reasoning chain. (This is why the architecture is provider-aligned in policy: V&V always runs on a different model family than construction.)

### 6.3 Cross-cutting roles

- **Configuration Management Agent (CM)** — maintains the RTM, the artifact tree, the defect database, and the audit trail. Runs continuously.
- **Review Board (one per stage gate)** — synthesized from a panel of reviewer agents (correctness, security, performance, reliability, etc.) with a human Operator chairing. Gates produce **signed verdicts**.
- **Risk Manager Agent** — maintains the cycle-level Risk Register; surfaces newly-discovered risks at every gate.

### 6.4 Humans

- **Strategist (human)** — intent, scope, non-goals
- **Operator (human)** — chairs Review Boards; signs off on gate verdicts; resolves Channel-2 outcomes; approves waivers
- **(Optional) Process Engineer (human)** — owns the methodology itself; tunes the phase definitions; reviews defect-of-origin trends

For solo operation, the Strategist and Operator are the same person; the Process Engineer is an occasional self-review session.

---

## 7. Cycle time and tempo

The novelty of this architecture is not the phases (the phases are 1970s-1990s discipline). The novelty is **the cycle time**.

A cycle in classical Waterfall: 6–18 months.
A cycle in the Foundry: target is **4–24 hours**, with 8 hours typical.

The phase budgets, illustratively, for an 8-hour cycle:

| Phase | Time | Notes |
|---|---|---|
| Phase 1 — Requirements | 30–60 min | Strategist sets intent; Requirements Engineer drafts SRS; V&V Planner reviews; iterate |
| RRB gate | 10 min | Operator chairs |
| Phase 2 — Architecture | 30–60 min | |
| ARB gate | 10 min | |
| Phase 3 — Detailed Design | 30–60 min | Parallel across components |
| DRB gate | 10 min | |
| Phase 3.5 — Implementation | 60–180 min | Parallel across U-IDs |
| Phase 4 — Unit V&V | 30–60 min | Parallel across U-IDs |
| UTRR gate | 10 min | |
| Phase 5 — Integration V&V | 30–60 min | |
| ITRR gate | 10 min | |
| Phase 6 — Acceptance V&V | 30–60 min | |
| SAR gate | 10–30 min | Operator + Strategist |

Total: roughly 6–10 hours wall-clock for a moderate feature. The CM Agent and Risk Manager run throughout.

A failed gate adds the time to re-run the upstream phase plus all subsequent phases. Defects attributed to Requirements are the most expensive — they restart the entire cycle. This is by design; the cost ratio enforces the Cleanroom discipline.

---

## 8. Configuration Management as the spine

The CM Agent's traceability matrix is the architecture's spine. It is rebuilt or updated continuously throughout a cycle and signs off as part of every gate.

```
RTM row example:
FR-12 → C-3 (Auth Component) → DD-3-§4.2 → U-7 (token rotation) →
  commit a3f9b1 → unit tests UT-7.1, UT-7.2, UT-7.3 → integration test IT-3.4 →
    AC-12.1 (acceptance) → SAR verdict: PASS
```

Every row of the RTM is *complete* before the SAR gate can pass. Orphaned requirements (no path to a test) and orphaned tests (no path to a requirement) both fail the gate.

The RTM is also the **defect attribution backbone.** A defect found at IT-3.4 traces back through DD-3-§4.2 to FR-12; if the failure is "DD-3 didn't capture an interaction the SAD intended," the defect's phase of origin is Detailed Design. The CM Agent annotates the defect with origin and routes it.

---

## 9. Defenses against the 20 failure modes

| Failure | Defense in this architecture |
|---|---|
| F1 Hallucination Loop | V&V agents are structurally independent (different model family); the policy is non-negotiable |
| F2 Reward hacking | Acceptance V&V runs against scenarios held outside the construction tree; the Acceptance Verifier did not see them during construction |
| F3 Spec-completeness | Requirements V&V Planner enforces SMART criteria; SAD risk register surfaces unstated assumptions; SAR runs against an externally-held scenario corpus |
| F4 Code-quality | Cleanroom discipline (no debugging) raises construction-time quality; Unit V&V exhaustive coverage requirement catches violations |
| F5 Cognitive ceiling | The Operator's role is gate-chairing, not per-agent supervision; gates are time-bounded events |
| F6 Cognitive debt | Phase artifacts are themselves the human-readable record; SAD and DD are written for human comprehension by design |
| F7 Normalization of deviance | Defect-of-origin trend tracked across cycles; rising upstream-defect rates trigger Process Engineer review |
| F8 Stale-knowledge | RTM is regenerated per cycle; cross-cycle knowledge lives in the SAD (architectural decisions) and in published cycle audit trails |
| F9 Spec overfitting | Requirements are written *before* implementation; phase order is enforced; spec amendments require returning to Phase 1 (expensive, deters lazy edits) |
| F10 Findings disappear | Defect database is durable; every finding has an ID and a resolution disposition |
| F11 Renumbering | RTM IDs (FR-N, NFR-N, IR-N, AC-N, U-N, etc.) never renumber by policy enforced by CM Agent |
| F12 Lethal trifecta | Implementation runs in sandboxes with capability whitelisting per Phase 3 DD; security cross-cutter runs in Phase 2 |
| F13 Missing-config blindspot | NFR-N (non-functional requirements) and IR-N (interface requirements) explicitly include configuration concerns; the SRS template requires them |
| F14 Attribution collapse | Every artifact, every defect, every commit is phase-attributed; CM Agent owns the audit trail |
| F15 Single-prompt collapse | Phase 1 has Requirements Engineer + V&V Planner + Strategist; multiple stances per artifact prevents single-prompt narrowing |
| F16 Resume-fidelity decay | Phase artifacts are checkpointable; resume re-runs the most recent phase, not the whole cycle |
| F17 Parallel agents on shared dirs | Worktree isolation per U-ID in Phase 3.5; CM Agent enforces serial merging at integration boundaries |
| F18 Prose-spec rigor | SRS, SAD, DD have structured templates; ACs in Given/When/Then form; RTM is a formal data structure |
| F19 Model-floor dependency | Phase prompts can be tuned per-model; the architecture explicitly supports different models per phase (construction vs. V&V) |
| F20 Maintenance asymmetry | Maintenance cycles run the same six phases; defect-driven cycles enter at Phase 1 (or the failed phase) and run forward |

This architecture is the strongest on F11 (renumbering — RTM is its spine), F14 (attribution — phase-of-origin is structural), and F18 (rigor — formal artifact templates with cross-references). Weaker on F5 because the gate-review tempo is heavier than the other architectures.

---

## 10. Stance on cost and scaling

This architecture is **higher cost than the others per cycle** (more agents, more artifacts, more reviews) and **lower variance** (gate failures cost time but rarely produce silent bad outcomes). It optimizes for **defect-of-origin attribution** and **regulatory-grade audit trails**.

Per-cycle cost (illustrative):

- More agent invocations than Architecture 1 or 2 (each phase has multiple)
- Heavier review process (every gate is a synthesis event)
- More artifact storage (RTM, defect DB, audit trail)

But:

- Lower defect leakage (Cleanroom discipline)
- Better predictability (phases either pass their gate or don't)
- Auditability for free (the artifact tree is the audit trail)
- Scale-up to teams is straightforward (phases parallelize across cycles; one team per cycle)

For solo operation, the architecture works but feels heavy. The Operator chairs every gate; even with agents doing the work, the human's calendar fills with reviews.

For team scale-up, the architecture *shines*. Different team members can specialize in different phases (Strategist, Requirements Engineer, Architect, V&V Lead). Multiple cycles run in parallel without collision because each cycle has its own artifact tree. The RTM is the cross-cycle integration mechanism. This is the architecture that most resembles how an organization with regulatory exposure would actually want to run an agent-based factory.

For domains with **regulatory pressure** (FDA software, FAA software, ISO 26262, SOC 2 Type II evidence requirements, IL-6 compliance), this architecture's audit trail and defect-of-origin attribution are not overhead — they are deliverables.

---

## 11. Implementation roadmap

**Stage 1 — Single-phase pilot.** Run Phase 1 (Requirements) end-to-end with the Requirements Engineer, V&V Planner, and an RRB gate. Produce one SRS for one feature. Goal: validate the artifact template and the gate review process at the smallest scale.

**Stage 2 — V-Model pair (Phase 1 ↔ Phase 6).** Add the Acceptance Verifier and SAR gate. Run requirements all the way to acceptance with no construction in between (acceptance test the SRS by itself, against a scenario corpus). Goal: validate that requirements V&V can be done before any code is written.

**Stage 3 — Add Phase 2 + Phase 5.** Architecture and Integration V&V. Now there's a meaningful cycle without unit-level work yet. Goal: validate the SAD template and the integration-test paradigm.

**Stage 4 — Add Phase 3, 3.5, 4.** Detailed Design + Implementation + Unit V&V. The full six-phase cycle is now operational. Goal: end-to-end cycle in 8 hours.

**Stage 5 — Cleanroom discipline.** Enforce no-debugging in Phase 3.5. Defects must return to upstream phases. Goal: measure the defect-of-origin distribution; expect Phase 1 to dominate initially.

**Stage 6 — RTM + Defect DB.** Add the CM Agent and the formal Configuration Management discipline. Goal: every cycle produces a complete RTM and an attributed defect database.

**Stage 7 — Independent V&V.** Enforce that V&V agents run on different model families from construction agents. Goal: validate that the independence policy catches additional defects (it should).

**Stage 8 — Process Engineer review.** Quarterly or per-N-cycles review of defect-of-origin trends. Adjust phase prompts and gate criteria based on data. Goal: empirical methodology refinement.

The architecture rewards organizations that can sustain the process discipline; it punishes shortcuts. Stage 1–4 take roughly the time-to-first-end-to-end-cycle; Stage 5–8 take the time to mature the process to the point where defects are caught at lowest-cost phase.

---

## 12. What this architecture is not

- **Not classical Waterfall.** Cycle time is 8 hours, not 18 months. The economic argument against Waterfall (months-long pre-coding work) does not apply.
- **Not heavyweight in human-time.** Most of the artifact production is agent-driven. The human spends time at gates, not in artifact authorship.
- **Not the Specification Refinery.** Phase 1's SRS is fixed-format and contract-grade, not a layered iterative artifact. Refinement is by re-running Phase 1 in a new cycle, not by amending in place.
- **Not the Compound Atelier.** Personas are phase-bound; there is no persona panel running on the full artifact at once.
- **Not unmodifiable.** The Process Engineer reviews and tunes the methodology; the gate criteria and phase prompts are themselves artifacts under CM.
- **Not a code factory.** The artifact-of-record is the RTM and the audit trail; code is one of many phase outputs.

---

## 13. Open questions

1. **Phase boundary disputes.** When a defect's phase of origin is debatable (e.g., the SAD said "use a queue" and the DD picked SQS — the queue choice fails NFR; whose fault?), the CM Agent's classification rules need to be unambiguous. The architecture mandates them but doesn't fully specify them.
2. **Iteration within phase versus return to phase.** A defect found in Phase 4 attributed to Phase 1 returns the cycle to Phase 1. But what if the Phase 1 fix is small? The architecture currently re-runs all subsequent phases unconditionally. A "tighter retry" policy might be cheaper at the cost of audit-trail rigor.
3. **Cleanroom in practice.** Cleanroom's empirical claims (10× defect reduction) come from human teams. Whether they hold for agent teams — and which "no debugging" rule actually applies to agents — is open.
4. **Provider strategy.** The architecture takes a strong stance: V&V on a different model family from construction. The exact mapping of model-family-to-phase is unspecified.
5. **Cycle time targets at scale.** 8 hours is illustrative. The right cycle length depends on feature scope, NFR strictness, and team experience. The architecture surfaces cycle time as a metric but doesn't prescribe a target.
6. **RUP discipline matrix discipline.** Knowing *how much* of each discipline runs in each phase is a tuning problem the methodology only sketches.
7. **Stage-gate composition for complex features.** A large feature might need multiple cycles, with cross-cycle coordination that the spec only briefly mentions (the RTM is the integration point, but coordination patterns aren't fully specified).
8. **Maintenance cycles.** A bug in production: does it enter at the RRB (re-run Phase 1) or at the failed-phase boundary? The architecture suggests the latter for speed; the former for rigor. Tradeoff is unresolved.

---

*End of architecture spec — Phase-Gated Foundry v0.1*
