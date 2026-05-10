# Architecture 1 — The Specification Refinery
## A Software Factory Built Around Iterative Specification Refinement

**Version:** 0.1
**Status:** Draft architecture proposal
**Lineage:** Refines `spec-driven-ai-dev.md` v0.1 with findings from `research/00-synthesis.md`
**Stance in one sentence:** *The specification is the product; everything else is instrumentation.*

---

## 1. Core thesis

Every cycle of agent-driven implementation reveals what the specification did not say. That information has more value than the code itself. A factory that systematically *captures* this information and *folds* it back into the spec — under discipline that prevents over-fitting to whatever the AI happened to build — produces a mature specification that other agents can implement without supervision.

This architecture adopts the existing baseline (`spec-driven-ai-dev.md`) wholesale and refines it in five directions:

1. **Scenarios become a sibling artifact.** End-to-end user stories are versioned outside the implementation tree as an ML-style holdout set, judged by an LLM separate from the implementer.
2. **Stable identifiers chain through every artifact.** R/A/F/AE/U/S-IDs survive renumbering, splitting, and deletion so traceability never silently rots.
3. **A knowledge store closes the loop between cycles.** Failures classified in cycle *n* become discoverable context for cycle *n+1*.
4. **The judge is structurally independent.** Different model family or different scaffold; never the same brain that wrote the implementation.
5. **A manager loop multiplies the operator.** A supervisor process observes many concurrent revelation cycles and surfaces only the ones that need a human's attention.

The original baseline defined *why* this loop should exist (the inversion of scarcity from implementation cost to specification cost). This architecture defines *how to run it at scale without overfitting.*

---

## 2. Artifact stack

The refinery has nine durable artifact classes. All are version-controlled. Volatility decreases from top to bottom — strategy is rarely amended; trajectories are produced every cycle.

| Tier | Artifact | What it is | Who writes it | Read by |
|---|---|---|---|---|
| 1 | **Strategy** | 1–2 page anchor: diagnosis, guiding policy, coherent action; explicit non-goals | Human (Strategist role) | Every downstream agent |
| 2 | **Spec (layered)** | The 5-layer document from the baseline (Domain → Behavioral → Integration → Quality → Presentation) | Human + Spec Analyst Agent | Implementer, Judge, Reviewer |
| 3 | **Scenarios** | End-to-end prose user stories with R/A/F/AE-IDs traced from the spec | Human (Scenario Designer) | Judge only — *not* the Implementer |
| 4 | **Pending observations buffer** | Out-of-layer feedback held until that layer is active | Spec Analyst Agent | Spec Analyst Agent |
| 5 | **Plan (per-cycle)** | The probe brief: active layer, scoped acceptance criteria, explicitly-excluded constraints | Spec Analyst Agent | Implementer |
| 6 | **Implementation probe** | The artifact built to exercise the active layer | Implementer Agent | Judge, Reviewer, Diagnostic |
| 7 | **Decision log** | Per-implementation structured record of every decision encountered and how it was resolved | Implementer Agent | Diagnostic Agent |
| 8 | **Trajectory** | Captured execution path with intermediate states | Auto-recorded by the harness | Diagnostic, Knowledge Curator |
| 9 | **Knowledge document** | Captured learning with YAML frontmatter, deduplication-checked | Knowledge Curator Agent | Spec Analyst Agent (next cycle's grounding) |

**The spec is the *only* artifact whose history is "the project's history."** Everything else is instrumentation, kept because it might be useful to read, but not the source of truth.

### 2.1 Stable identifier discipline

| Tier | ID prefix | Origin | Flows into |
|---|---|---|---|
| Requirements | `R-N` | Spec Layer 1–2 | Plan, scenarios |
| Actors | `A-N` | Spec Layer 1 | Spec, scenarios |
| Key flows | `flow:F-N` | Spec Layer 2 | Plan, implementation units |
| Acceptance examples | `AE-N` | Spec Layer 2–3 | Scenarios, decision log |
| Implementation units | `U-N` | Plan | Decision log, knowledge |
| Scenarios | `S-N` | Scenario set | Trajectory, judge output |
| Findings | `finding:F-N` | Diagnostic / Reviewer | Pending buffer, knowledge |
| Knowledge | `K-N` | Knowledge Curator | Spec Analyst grounding |

**Rule:** never renumber. Splits keep the original ID; deletions leave gaps. A pending-buffer observation tagged `K-12 ↔ R-7 ↔ Layer-2` is durable; a "see issue #14" reference is not.

### 2.2 Why scenarios sit outside the implementation tree

The Implementer Agent must not be able to read the scenario corpus during a cycle. Reasons:
- **Reward hacking (failure F2):** if the Implementer can read scenarios, it will hardcode their inputs.
- **Hallucination Loop (F1):** if the same agent constructs both code and tests, blind spots are shared.
- **Spec overfitting (F9):** if scenarios are inside the spec tree, they get amended together with the spec, ratifying whatever the AI happened to do.

Scenarios live in a separate repo (or a separate branch protected from agent reads) and are mounted into the Judge's environment only.

---

## 3. Roles

The architecture defines six agent roles and three human roles. Roles are not personas; they are *responsibility contracts*. Multiple roles may run on the same model; the constraint is that the **Judge** must be a different model family or scaffold from the **Implementer**.

### 3.1 Agents

- **Spec Analyst Agent** — process owner. Generates probe briefs, conducts observation interviews, classifies failures into the five modes, proposes spec amendments, runs consistency checks, manages the pending buffer. *Does not write business logic.*
- **Implementer Agent** — builds probes from probe briefs. Owns its own loop (per Attractor's argument: don't reuse the SDK's `generate()` tool loop). Produces decision logs.
- **Judge Agent** — evaluates trajectories against scenarios, probabilistically. Returns a *satisfaction score* per scenario plus a *failure-class hint* per low-scoring trajectory. Constraint: different model family or scaffold from the Implementer.
- **Diagnostic Agent** — analyzes Channel-1 failures. Maps automated test failures + decision log + trajectory into a proposed spec amendment classified by failure mode.
- **Knowledge Curator Agent** — captures durable learnings, deduplicates against the existing store (5-dimensional overlap check), enforces discoverability via `AGENTS.md`, and runs periodic refresh cycles.
- **Manager Loop Agent (Conductor)** — supervises a fleet of concurrent revelation cycles. Observes events, scores progress, surfaces escalations to the human. Does not steer cycles; only escalates.

### 3.2 Humans

- **Strategist** — owns the strategy document and the long-arc choice of what to build.
- **Scenario Designer** — authors and curates the scenario corpus. *This role is non-negotiable;* scenarios written by an agent against a spec the agent also read defeat the holdout property.
- **Operator** — receives manager-loop escalations, runs Channel-2 (completeness) reviews, approves spec amendments. The day-to-day human in the loop.

For solo operation all three roles are the same human in different stances. For team scale, the Strategist and Scenario Designer can be different people; the Operator role can rotate.

---

## 4. The revelation cycle (refined)

The baseline's seven-phase cycle is preserved and extended. New material is marked **[+]**.

### Phase 1 — Probe commissioning

The Spec Analyst confirms the active layer, surfaces pending-buffer observations belonging to it, and generates a probe brief.

**[+]** The probe brief now includes:
- The relevant **subset of scenarios** that exercise the active layer (the Judge will run these; the Implementer will not see them)
- A list of **knowledge docs** (`K-N`) the Implementer is *allowed* to consult, surfaced from the curator's index
- A **token budget** and a **cost ceiling** that the Manager Loop will enforce
- An **independence flag** declaring which model family the Judge is using for this cycle

### Phase 2 — Implementation and trajectory capture

The Implementer builds the probe and records a decision log. The trajectory is captured by the harness (CXDB-style turn DAG with branch-from-any-turn).

**[+]** A **sandbox** wraps the Implementer (Codespace, Docker, or chroot — the architecture is agnostic). YOLO mode is on inside the sandbox; never on outside it. This addresses F12 (lethal trifecta).

### Phase 3 — Automated judging

The Judge runs the scenarios against the probe and produces:
- A **satisfaction score** per scenario (probabilistic)
- A **failure class hint** per low-scoring scenario
- A **divergence narrative** (not a diff) describing where the trajectory left the expected behavior

The Judge's output is the basis of Channel-1 review. *The Judge does not produce code-quality opinions* — those are out of scope for compliance review.

### Phase 4 — Diagnostic analysis

The Diagnostic Agent receives spec + decision log + trajectory + judge output. For each low-satisfaction scenario it produces a proposed spec amendment classified into one of:

- **Silence** — the spec did not address the decision point. Fix: add coverage.
- **Ambiguity** — the spec addressed it, in language permitting multiple valid interpretations. Fix: add precision.
- **Incorrectness** — the spec stated something the author did not mean. Fix: correct the statement.
- **Inconsistency** — two spec statements cannot both be satisfied. Fix: reconcile.
- **Undiscovered preference** — the implementation was compliant; the user discovered a preference they didn't know they had. Fix: add the preference (Channel 2).

**[+]** The Diagnostic Agent now also flags:
- **Scenario gap** — if the failure suggests the scenario set itself does not cover an important behavior, route to the Scenario Designer.
- **Reward hacking signature** — if the trajectory hits scenarios via shortcuts not in the spirit of the spec (`return true` patterns, hardcoded inputs, rewriting tests), flag for the Operator with a confidence score.

### Phase 5 — Channel-2 review (human)

The Operator reviews:
- Probe artifact (what was built)
- Trajectory narrative (what the agent did to build it)
- Judge output (where compliance failed)
- Diagnostic proposals (recommended amendments)

**[+]** Review uses a **structured intake interview** (preserved from baseline) with one addition: the Operator must explicitly answer **"Was the spec edited because I disagreed with the implementation, or because I disagreed with what I asked for?"** The first answer is a fix; the second is an undiscovered preference. Conflating the two is the spec-overfitting failure mode.

### Phase 6 — Amendment drafting + consistency check

Active-layer amendments are drafted, reviewed, and approved. The consistency check runs across the full spec.

**[+]** Two new checks:
- **Stable-ID integrity:** no amendment renumbered an ID; every cross-reference still resolves.
- **Discoverability:** if the amendment introduces a new pattern, `AGENTS.md` must surface where the future Implementer will find it. This addresses F8 (knowledge invisible) and the compounding-decay risk.

### Phase 7 — Knowledge capture and cycle close

**[+]** New phase. The Knowledge Curator runs:
- For amendments tagged "ambiguity" or "silence," create a `K-N` document if the pattern is reusable.
- Five-dimensional overlap check against existing `K-*` docs; update rather than duplicate.
- Frontmatter validation (`module`, `tags`, `problem_type`, `confidence`, `last_updated`).
- Update the Manager Loop's index of knowledge docs the next cycle's Implementer is allowed to consult.

The Spec Analyst produces the cycle summary: layer stability, surprise rate, knowledge captured, residual buffer state.

---

## 5. Layer stability and exit conditions

Preserved from baseline:

- A layer is **stable** when successive probes produce no new Channel-1 failures and Channel-2 observations are limited to undiscovered preferences.
- The spec is **mature** when all layers are stable and a full-stack probe produces no surprises.
- The spec is **implementation-ready** when all acceptance criteria are either automatable or explicitly designated for human review.

**[+]** New stability signals:
- **Knowledge-store growth slows.** Mature specs produce few new knowledge docs per cycle; immature specs produce many. The Curator's growth rate is a stability proxy.
- **Reward-hacking signals decrease.** As the scenarios mature, the Implementer has fewer shortcuts; trajectory shapes converge.
- **Independence preserved.** Cycles where the Judge and Implementer used the *same* model family are flagged retroactively as suspect; their stability claims discounted.

---

## 6. Human leverage at scale

The architecture targets a single Operator running 4–8 concurrent revelation cycles. The Manager Loop is the leverage point.

### 6.1 The manager loop

A supervisor process observes all active cycles every *n* seconds (default 30s). For each cycle it computes:
- **Cycle health:** is it advancing? (token spend / wall time / progress signal)
- **Escalation level:** none / informational / decision-required
- **Resource pressure:** token budget remaining, time budget remaining

It surfaces to the Operator only:
1. Cycles requesting Channel-2 review (the highest priority)
2. Cycles flagged with reward-hacking signals
3. Cycles approaching budget exhaustion
4. Cycles producing inconsistency check failures

Everything else, including routine Channel-1 amendments, runs without the Operator. The Operator's inbox is a sortable list of "needs human attention." Symphony's 5-state queue (`Backlog → Todo → In Progress → Human Review → Merging → Done`) is the operational analog.

### 6.2 Pyramid summaries for survey reading

Drawn directly from StrongDM. When the Operator opens a cycle's Channel-2 review queue, the Manager Loop emits multi-resolution summaries:

- **2-word level:** "Auth broken." / "Pagination edge."
- **8-word level:** "Token expiration handler skips refresh on 401s."
- **Full level:** the diagnostic narrative.

The Operator scans 8-word summaries across all queued reviews and drills into only those that warrant. This is how 30 cycles' worth of Channel-2 reviews compress into a 5-minute scan.

### 6.3 Showboat-style trajectory artifacts

For Channel-2 review, the trajectory is rendered as a **walkthrough document** — note / exec / image entries showing what the agent did, not just what it produced. The Operator reviews the *narrative*, not just the diff. This is Simon Willison's pattern transplanted as a first-class artifact.

### 6.4 Cost telemetry as a first-class metric

Per-cycle: tokens, wall-clock, dollar cost, model usage breakdown. Per-day: aggregate spend versus budget envelope. The dashboard exposes the StrongDM-style "$1k/day/engineer" benchmark *and* a soft floor (under-spending suggests under-utilizing). The architecture takes no position on what the right number is; it surfaces it.

---

## 7. Defenses against the 20 failure modes

| Failure | Defense in this architecture |
|---|---|
| F1 Hallucination Loop | Judge is structurally independent (different model family); Scenario Designer is human |
| F2 Reward hacking | Scenarios outside repo; trajectory pattern detector; Operator confirms suspicious shortcuts |
| F3 Spec-completeness | Layered spec exposes silence-as-failure-mode; pending buffer routes out-of-layer surprises |
| F4 Code-quality | Reviewer panel for Channel-2 (added in §8); not the central focus of this architecture |
| F5 Cognitive ceiling | Manager Loop reduces operator's surface to escalation-only |
| F6 Cognitive debt | Walkthrough-style trajectory artifacts; layered specs the Operator wrote remain authoritative |
| F7 Normalization of deviance | Surprise rate tracked across cycles per layer; rising drift triggers explicit Operator review |
| F8 Stale-knowledge | Curator runs refresh cycles; discoverability gate at amendment time |
| F9 Spec overfitting | Classify-before-amend discipline; "did I disagree with implementation or with what I asked?" question; pending-buffer keeps out-of-layer observations from leaking into active-layer amendments |
| F10 Findings disappear into chat | Pending-buffer + decision-log + structured intake interview |
| F11 Renumbering | Stable-ID rule (never renumber) enforced by the Spec Analyst |
| F12 Lethal trifecta | Sandboxed Implementer; capabilities scoped via tool whitelisting |
| F13 Missing-config blindspot | Layer 4 (Quality and Constraints) explicitly includes operational/configuration concerns; the Spec Analyst flags their absence |
| F14 Attribution collapse | Decision log ties every choice to a model+prompt+spec section; trajectory ties every artifact to a cycle ID |
| F15 Single-prompt collapse | Probe briefs commissioned with explicit constraints; the Implementer is given divergent ideation only when the layer is in active probe |
| F16 Resume-fidelity decay | Trajectory checkpoints are first-class; resume reduces fidelity for one hop only |
| F17 Parallel agents on shared dirs | Each cycle runs in its own worktree; the Manager Loop merges serially |
| F18 Prose-spec rigor | Acceptance criteria in Given/When/Then form; the Judge runs them probabilistically rather than pretending they're proofs |
| F19 Model-floor dependency | Surfaced explicitly: an "assumed model capability" section in the spec ages the design |
| F20 Maintenance asymmetry | The methodology applies equally to greenfield and maintenance; specs evolve via amendment, not rewrite |

The architecture covers 20/20 in some form, though F4 (code quality) and F18 (rigor) get partial coverage.

---

## 8. Optional extensions

Three extensions can be bolted onto the core architecture without disturbing it:

### 8.1 Reviewer panel for code-quality (F4)

A small panel of named reviewers (correctness, security, maintainability) runs after the Judge and before Channel-2. These produce *advisory* findings, not gates. The Operator can promote any to a spec amendment.

### 8.2 Adversarial probe (F1, F2)

A second Implementer Agent — same brief, different model family — runs in parallel and produces a *competing* probe. The Judge runs both. Disagreements between the two probes' satisfaction scores are amplified into Channel-2 review items: the spec is doing something different to two faithful implementers.

### 8.3 Healer loop (F20)

For long-lived systems, a continuous diagnostic loop watches production trajectories (CXDB-style) and clusters anomalies. Each cluster becomes a Channel-2 candidate the next time a cycle is commissioned. This closes the long-loop feedback that El Kaim's "dark factory" foregrounds.

---

## 9. Stance on cost and scaling

This architecture is *expensive at the spec-construction phase and cheap thereafter.* A mature spec with stable layers may run dozens of zero-amendment cycles producing implementations with no human attention. A young spec produces many amendments and consumes significant Operator time.

The cost curve is the inverse of agile: you pay heavily for spec maturity up front, and reap the savings during the long tail of implementation. This is the right shape for **high-stakes, long-lived, badly-understood domains.** It is the wrong shape for **throwaway prototypes** and **well-understood replication** (a CRUD admin panel doesn't need a revelation cycle).

For team scale-up: each Operator runs their own spec project. The Strategist coordinates across specs; the Scenario Designer rotates. The architecture does not naturally support multiple Operators on the *same* spec — you'd need to partition by layer or by use case to avoid amendment collisions.

---

## 10. Implementation roadmap

A staged implementation plan for someone wanting to adopt this architecture from scratch.

**Stage 1 — Manual revelation cycle.** Operator runs the seven phases by hand, with one Implementer Agent and one Judge (different model). No knowledge store, no manager loop. Goal: validate that the discipline produces stable specs at all.

**Stage 2 — Spec Analyst + Diagnostic.** Add the Spec Analyst Agent to manage the spec document, the pending buffer, and the cycle summary. Add the Diagnostic Agent for failure classification. Goal: take the cognitive load of process discipline off the Operator.

**Stage 3 — Knowledge store.** Add the Knowledge Curator. Begin capturing learnings. Run a refresh cycle every *n* cycles. Goal: cycle *n+1* should be measurably cheaper than cycle *n* on the same layer.

**Stage 4 — Manager loop.** Run multiple cycles in parallel. Add the supervisor process and the pyramid summary surface. Goal: scale to 4–8 concurrent cycles.

**Stage 5 — Adversarial probe / Healer.** Add the optional extensions for cross-checking and long-loop healing.

Each stage should be operated for at least 5 revelation cycles before moving to the next. Stage 1 is the gate to all subsequent stages — if the manual process doesn't produce stable specs, no automation will.

---

## 11. What this architecture is not

- **Not a one-shot specification tool.** The spec is iterative by design.
- **Not a replacement for human judgment about what is wanted.** The Operator and Strategist remain authoritative.
- **Not a high-throughput code factory.** The throughput unit is a *stable spec layer*, not a feature.
- **Not StrongDM-style automated judgment.** The Judge produces a satisfaction score; the Operator produces the verdict on whether amendment is appropriate.
- **Not an attempt to scale to many humans on one spec.** Multiple operators on one project requires layer partitioning, which is unsupported in this version.

---

## 12. Open questions

These are points where the architecture acknowledges uncertainty and invites probes of itself.

1. **Scenario authorship at scale.** Scenarios must be human-authored to preserve holdout independence. Is there a co-author Agent that *proposes* scenarios for human ratification without reading the spec? Worth exploring.
2. **Independence of judge from implementer.** "Different model family" is the default; "different scaffold" or "different prompt" might be enough for some failure modes. The architecture does not formalize the spectrum.
3. **Stable-ID collisions.** R/F naming collides between requirements and key flows. The architecture mandates prefixed cross-references (`req:R-7`, `flow:F-3`) but doesn't enforce a global ID registry.
4. **Curation cadence.** How often the Curator's refresh runs is unspecified. Too frequent: thrash. Too infrequent: stale knowledge inverts compounding.
5. **Provider strategy.** This architecture is provider-agnostic. Attractor's stance — provider-aligned profiles, not unified — would change how the agents are configured. Not addressed.

---

*End of architecture spec — Specification Refinery v0.1*
