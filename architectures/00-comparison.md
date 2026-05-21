---
based-on-commit: c495dc9
based-on-date: 2026-05-10
---

# Software Factory Architecture Options — Comparison and Decision Guide
**Date:** 2026-05-10
**Version:** 2 — post-primary-source-access
**Status:** Companion document to the four architecture specs in this directory
**Purpose:** Compare the four proposed architectures side-by-side, surface the decisions each one resolves differently, and recommend which to pick (or hybridize) for different conditions.

---

## 0. Revision notes (v2)

Changes from v1 driven by the v2 research pass against primary sources:

- **DTU = Digital Twin Universe** (not "Users") throughout. Where this comparison previously referenced DTU implicitly, the term is consistently corrected.
- **Willison's "4 parallel agents" specific number was a v1 fabrication.** The verbatim claim is only that he is "mentally exhausted by 11 a.m." running parallel agents. The cognitive-ceiling row in §2.2 is unchanged in intent but no specific number is cited.
- **Cherny "10–30 PRs/day, 10–15 parallel sessions"** comes from a separate Lenny interview (Feb 19 2026), not the Willison interview. Provenance retagged.
- **Compound engineering canonical loop is four-step** (Plan → Work → Review → Compound), not five. Affects the description of Architecture 2 but not its structure.
- **Self-improving prompts** (Klaassen's frustration-detector, Tedesco's Montaigne) are now documented patterns; Architecture 2's coverage of F8 (stale-knowledge) is *stronger* than v1 suggested.
- **Scenarios are partially agent-generated at StrongDM** (homepage caption confirms a "synthetic scenario curation and shaping interface"). This makes Architecture 4's Predator-driven scenario generation more consistent with prior art than v1 framed it.
- **Simon Willison's "review everything" stance has softened** (May 6 2026 post). The "Tiered: humans for Channel-2 only" framing in §2.2 for Architecture 1 is consistent with this; it remains the appropriate description.
- **The recommended starting path (Atelier as baseline + selective borrows) is unchanged.** The new self-improving-prompts evidence further supports the recommendation.

The four architecture specs each carry their own v0.2 revision notes detailing what changed in each.

---

## 1. The four architectures

| # | Name | Core thesis | Closest existing analog |
|---|---|---|---|
| 1 | **Specification Refinery** | The spec is the product; the implementation is a probe that reveals what the spec did not say | The existing `spec-driven-ai-dev.md`, refined |
| 2 | **Compound Atelier** | Each unit of work makes the next easier — by passing through specialist hands and leaving its lessons behind | Every.to's compound-engineering plugin + Symphony |
| 3 | **Phase-Gated Foundry** | Pre-agile structured methodologies become the right shape when agents make them fast | Waterfall + V-Model + RUP + Cleanroom, at hour cycle time |
| 4 | **Evolutionary Tournament** | The factory does not specify the right answer; it sets up the conditions under which the right answer wins | Genetic algorithms + Willison's "code is cheap" + StrongDM satisfaction-as-judge |

Each is described in full in `architectures/0N-*.md`. This document is the comparison.

---

## 2. Side-by-side decision matrix

### 2.1 Methodology dimensions

| Dimension | 1: Refinery | 2: Atelier | 3: Foundry | 4: Tournament |
|---|---|---|---|---|
| **Spec format** | Layered prose with Given/When/Then ACs | Structured prose with stable IDs | Formal templates (SRS, SAD, DD) | Deliberately under-specified seed |
| **Cycle time** | Days–weeks per layer | Hours per issue | 4–24 hours per cycle | 2–4 hours per generation; days per tournament |
| **Unit of work** | A spec layer | An issue | A six-phase cycle | A population/generation |
| **Dominant agent shape** | Few generic + diagnostic | Many specialized personas | Phase-bound experts | Diverse population + judges |
| **Workflow language** | Prose phases (revelation cycle) | Skill chain with tiered ceremony | Phase contracts with formal artifacts | Tournament bracket + lineage |
| **Knowledge architecture** | Pending buffer + spec history + curator | Flat files + auto-curation + refresh | Phase audit trail + RTM | Genome library + meta-loop curation |
| **Provider strategy** | Agnostic | Persona-aligned where useful | Different provider per phase (V&V independence) | Diversity policy enforces multiple families |

### 2.2 Human role

| Dimension | 1: Refinery | 2: Atelier | 3: Foundry | 4: Tournament |
|---|---|---|---|---|
| **Primary human stance** | Spec author + Channel-2 reviewer | Strategist + queue-driven Operator | Gate chair + scope owner | Geneticist (tunes selection pressure) |
| **What the human reviews** | Probe artifacts + diagnostic proposals | Workpads + synthesized findings + plans | Phase artifacts at gates | Generation summaries + finalist gallery |
| **Time-per-cycle (human)** | Medium (review every cycle) | Low to medium (gates are async) | High (chairs every gate) | Low (per-generation summaries) |
| **Reads code line-by-line?** | Sometimes (Channel 2 review) | Rarely (synthesizer pre-digests findings) | At gates if needed | No (only fitness vectors + walkthroughs) |
| **Solo-friendly?** | Yes, but spec-heavy | Yes | Yes, but heavy gate calendar | Yes, very |
| **Team scale-up natural fit?** | Modest (partition by spec project) | Excellent (queue + workpad scales) | Excellent (phase specialization) | Modest (independent tournaments) |

### 2.3 Cost shape

| Dimension | 1: Refinery | 2: Atelier | 3: Foundry | 4: Tournament |
|---|---|---|---|---|
| **Per-cycle cost** | Medium-high (spec amendments expensive) | Medium (panel reviews add tokens) | High (multiple agents per phase) | Very high (population × generations) |
| **Amortization** | Strong (mature spec runs cheaply for many cycles) | Strong (knowledge store accumulates) | Medium (phase templates reused) | Strong (genome library + meta-loop) |
| **Variance** | Low (deterministic process) | Low-medium (panels predictable) | Low (gates pass/fail) | High (convergence rate varies) |
| **Cost ceiling per cycle** | Soft (Operator time gates spend) | Soft (concurrency cap) | Hard (phase budgets) | Hard (genome sets max generations + budget) |
| **Best when** | High stakes, badly understood domain | Continuous shipping, cross-cutting expertise valued | Regulatory-grade audit trail required | Exploration matters, code is cheap |

### 2.4 Failure mode coverage

Moved to the canonical project-wide index at [`/failure-modes.md`](../failure-modes.md). The per-architecture coverage matrix for F1–F20 lives there now; new failure modes discovered in research, retrospectives, or architecture work are registered against the same file.

---

## 3. When to pick which

A short decision guide:

### Pick 1 (Specification Refinery) when:

- The problem is **high-stakes, badly understood, and likely to surprise you.**
- You can afford weeks of upstream spec work in exchange for cheap downstream implementation.
- The spec quality matters more than implementation throughput.
- You are willing to operate at the edge of your understanding and treat the implementation as a probe.
- Solo or 2-person team; team scale-up requires partitioning.

### Pick 2 (Compound Atelier) when:

- You ship continuously across a stable domain that benefits from cross-cutting expertise (security, performance, accessibility, etc.).
- You value **compounding velocity** — you expect cycle 50 to be much cheaper than cycle 5.
- You can sustain knowledge-store curation discipline.
- Solo or small-team operation; scales to 5–10 people naturally with phase partitioning.
- You are okay with persona-explosion risk and the curation cost it implies.

### Pick 3 (Phase-Gated Foundry) when:

- You operate under **regulatory pressure** (FDA, FAA, ISO 26262, SOC 2 Type II, etc.) requiring audit trails.
- Your defect rate matters more than your speed.
- You want defect-of-origin attribution to drive process improvement.
- You can sustain the gate-review calendar.
- Team scale 2–10; the architecture's phase-specialization makes specialization legible.

### Pick 4 (Evolutionary Tournament) when:

- The implementation shape is genuinely uncertain and **multiple correct answers exist.**
- You operate in adversarial domains (security, reliability, perf-critical) where predator-driven selection is more valuable than spec adherence.
- Token spend is not a binding constraint; quality and diversity matter more.
- You have a **rich scenario corpus** to feed selection pressure.
- Solo Geneticist or independent-tournaments-per-Geneticist; scales by tournament-count, not by per-tournament-team-size.

### Hybrid recommendations

The architectures are not strictly exclusive. Useful hybrids:

- **Refinery seed → Atelier execution.** Use the Refinery's revelation cycle to mature a spec; once stable, hand to the Atelier for ongoing maintenance. The mature spec becomes the Atelier's `STRATEGY.md` analog plus a stable acceptance criteria set.
- **Foundry phases with Atelier reviewers.** Replace the Foundry's gate review boards with the Atelier's persona panels. The phase structure is preserved; the review depth is increased. Best for regulated domains where reviewer breadth matters.
- **Tournament inside a Foundry phase.** Replace the Foundry's single Implementer in Phase 3.5 with a small tournament (e.g., *N* = 4). The winner of the tournament is the artifact that enters Phase 4 V&V. Adds quality at the cost of token spend; preserves audit trail.
- **Refinery layer probing as Tournament generations.** A spec layer probe could itself be a small tournament rather than a single probe. The diversity informs amendment proposals.
- **Atelier knowledge store seeding Tournament genomes.** Compound-Atelier's `docs/solutions/` becomes the genome library for new Tournament problems.

---

## 4. Common substrate

Despite different shapes, the four architectures share a common substrate. If you build infrastructure for any one, you make the others much cheaper to build later.

### 4.1 Shared infrastructure

- **Worktree per unit of work.** All four architectures isolate parallel agents in their own filesystems.
- **Sandboxed agent execution.** All four sandbox implementer agents (capability scoping, network restrictions).
- **Stable ID assignment.** All four use stable identifiers (R/A/F/AE/U/S/K/etc.). The exact letters vary but the discipline is the same.
- **Out-of-construction-tree scenarios.** Three of four architectures use this; the fourth (Foundry) uses an equivalent in its acceptance phase.
- **LLM-judge with model-family independence.** All four require this in some form.
- **Trajectory capture.** All four record per-cycle execution trajectories for review/diagnostic.
- **Manager loop / orchestrator.** All four have a supervisor process that dispatches and monitors agent fleets.
- **Decision log / audit trail.** All four require structured records of decisions made.
- **AGENTS.md / discoverability.** All four require well-known files agents read for project conventions.

A factory infrastructure built around these primitives can run any of the four methodologies with configuration-level differences. **The architecture is the methodology; the infrastructure is shared.**

### 4.2 Shared roles, different emphasis

| Role function | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Strategist | Yes | Yes | Yes | Yes |
| Spec author | Yes (Spec Analyst) | Yes (Brainstormer) | Yes (Requirements Engineer) | Yes (Genome Author) |
| Implementer | Yes | Yes | Yes (Cleanroom-disciplined) | Yes (per-candidate, ×N) |
| Judge / Verifier | Yes (Judge Agent) | Yes (in panel) | Yes (V&V agents, phase-paired) | Yes (Primary + Secondary judges) |
| Reviewer panel | Optional extension | Yes (central) | Yes (gate boards) | No (selection replaces review) |
| Adversarial role | Optional adversarial probe | Named persona | Independent V&V is structurally adversarial | Predator agent (named) |
| Knowledge curator | Yes | Yes (central) | Yes (CM Agent) | Yes (genome curator) |
| Manager / Conductor | Yes | Yes | Yes | Yes |
| Operator (human) | Yes | Yes | Yes (gate chair) | Yes (Geneticist) |

The roles are functionally similar across architectures; the *intensity* and *contract* differ.

---

## 5. The decisions each architecture makes differently

### 5.1 What is the durable artifact?

- **1:** The layered spec. Everything else is instrumentation.
- **2:** The chain of brainstorm + plan + workpad + knowledge documents. The spec is implicit in the brainstorm.
- **3:** The phase artifacts (SRS, SAD, DD) plus the Requirements Traceability Matrix.
- **4:** The genome library. The implementations are throwaway.

### 5.2 What does "the human reviews" mean?

- **1:** Reads diagnostic proposals; classifies failures; approves spec amendments.
- **2:** Reads synthesized findings; disposes residual; approves at `Human Review` gate.
- **3:** Chairs gate boards; signs off on phase exits; resolves Channel-2 outcomes.
- **4:** Reads generation summaries; tunes scoring weights; picks finalist gallery.

### 5.3 What does failure trigger?

- **1:** Failure classified into one of 5 modes (silence/ambiguity/incorrectness/inconsistency/undiscovered preference); spec amended at active layer.
- **2:** Findings synthesized; routed by severity × autofix-class; residual must be disposed before merge.
- **3:** Defect attributed to phase of origin; cycle returns to that phase.
- **4:** Low-fitness candidate excluded from selection; if the population is stuck, scoring weights or scenarios are tuned.

### 5.4 Where does adversarial logic live?

- **1:** Optional adversarial probe extension; otherwise the diagnostic role is reactive.
- **2:** Named adversarial reviewer + named adversarial document reviewer.
- **3:** Independent V&V is structurally adversarial; security/reliability cross-cutters add depth.
- **4:** **Predator agent** (continuously generates new adversarial scenarios) + **selection pressure itself** (high-fitness candidates kill low-fitness candidates).

### 5.5 How is parallelism achieved?

- **1:** Multiple revelation cycles run by the manager loop; each cycle is internally sequential.
- **2:** Multiple issues in parallel via the queue; each issue is internally tiered/sequential.
- **3:** Multiple components run in parallel within Phase 3.5; cycles run sequentially per gate.
- **4:** Population *N* = 8–32 candidates run truly in parallel; tournaments can also run in parallel.

### 5.6 How does the architecture fail when wrongly applied?

- **1:** A simple, well-understood task gets bogged down in upstream spec ceremony; cycle time inflates without benefit.
- **2:** Persona explosion produces a curation burden that exceeds the compounding benefit; the knowledge store rots.
- **3:** Gate calendar consumes the human's attention; gate failures cascade and cycle times grow.
- **4:** Token costs spiral; without a strong scenario corpus, the population converges on irrelevance.

---

## 6. Recommended evaluation sequence

If you want to *try* an architecture before committing, this is the leanest evaluation path:

### To try Architecture 1 — Specification Refinery

Run a manual revelation cycle on a single layer of an existing spec. Don't build any infrastructure. Just write a probe brief, give it to one agent, run a judge separately, and do the structured intake interview by hand. **Goal: validate the discipline produces sharper specs.** Time: 1 day.

### To try Architecture 2 — Compound Atelier

Pick one issue in a real project. Manually run the brainstorm + plan + implement + 4-reviewer-panel + synthesizer + capture chain. Don't build orchestration. **Goal: validate that the persona panel catches things a single reviewer misses.** Time: 1 day.

### To try Architecture 3 — Phase-Gated Foundry

Pick one feature. Manually run Phases 1, 2, 6 (Requirements, Architecture, Acceptance V&V) — skipping construction phases. Acceptance-test the SAD against the SRS using held-out scenarios. **Goal: validate that requirements V&V catches problems before any code is written.** Time: 1 day.

### To try Architecture 4 — Evolutionary Tournament

Pick one small problem (e.g., a refactor with multiple credible approaches). Hand-author a genome with *N* = 4 candidates from 2 different model families. Hand-judge them against 5 scenarios. Pick a gallery winner. **Goal: validate that diversity-of-implementation produces meaningful options the human prefers among.** Time: 1 day.

In each case, the goal is to test the *discipline* before building infrastructure. The infrastructure investment is large; the methodology validation is small.

---

## 7. Recommended path forward

Given the project brief — *general execution environment for agents, scaling from solo to small team* — and the available source signal:

### 7.1 The single recommended starting path

**Pick Architecture 2 (Compound Atelier) as the working baseline.** Reasons:

- It is the only architecture with a fully-realized public reference implementation (Every.to's compound-engineering plugin).
- It has the broadest 20-failure-mode coverage.
- It scales naturally from solo to small team with the queue + workpad model.
- Its knowledge accumulation mechanism is the most concrete in the corpus.
- It has the cleanest interfaces for hybridization (the workpad, the residual gate, the reviewer panel can each be swapped or extended).

### 7.2 Then enhance with selective borrows from the others

Once the Atelier base is operating, layer in:

- **From Architecture 1:** the layered spec discipline for high-stakes greenfield work (use the spec layers as the structure of an issue's `STRATEGY.md`-equivalent).
- **From Architecture 3:** the defect-of-origin attribution practice when post-merge bugs appear (do not just patch; classify which upstream phase made the mistake).
- **From Architecture 4:** small *N* = 3–4 tournaments inside especially uncertain Atelier issues (the gallery winner enters the normal review chain).

### 7.3 Reserve full-architecture adoption for specific contexts

- Adopt the **full Refinery** when undertaking a greenfield spec for a high-stakes, badly-understood domain.
- Adopt the **full Foundry** if the team enters a regulated environment requiring audit trails.
- Adopt the **full Tournament** for designated exploration projects with budget and patience.

### 7.4 Build the shared infrastructure first

The infrastructure layer (§4.1) is the same across all four. Building it well unlocks all four architectures as configuration choices, not engineering forks. Spend infrastructure budget on:

- Worktree-per-unit isolation
- Sandboxed agent execution with capability scoping
- Stable-ID enforcement and a cross-artifact RTM-equivalent
- Out-of-construction-tree scenario storage with held-out access discipline
- Trajectory capture (CXDB-style turn DAG would be the gold standard; cheaper alternatives exist)
- Manager-loop / orchestrator with the 5-state queue or the manager_loop primitive

A factory team that gets the infrastructure right has architectural optionality. A factory team that bakes one methodology into the infrastructure pays to switch later.

---

## 8. What this comparison did not address

These are explicit gaps the four-architecture set leaves. Surfacing them so they're not invisible.

- **MCP / tool ecosystem strategy.** All four assume tooling exists; none specify how the factory exposes tools to agents. Simon Willison's `AGENTS.md` preference is mentioned but not enforced.
- **Multi-codebase coordination.** All four describe single-project work. Cross-project knowledge transfer (from Compound Atelier's solutions across projects, from Tournament genome libraries across problems) is sketched but not formalized.
- **Production observability.** El Kaim's "Healer" / production-trace-to-spec-amendment loop is mentioned in Architecture 1's optional extensions but not centered. None of the four architectures fully integrate production data into their main loop.
- **Cost optimization across architectures.** Each architecture has its own cost shape; none discuss how a team running multiple architectures simultaneously would budget across them.
- **Methodology evolution.** All four say "the methodology is itself an artifact" but none describe a rigorous mechanism for evolving the methodology based on operational experience. Architecture 3's Process Engineer is the closest gesture.
- **Failure of the human role.** What happens when the Operator/Geneticist/Strategist makes a sustained mistake? None of the four architectures have a corrective for human-side drift.

These are starting points for further iteration, not blockers to adoption.

---

## 9. Reading order

For a new reader, the recommended order is:

1. **`research/00-synthesis.md`** — the shared findings, tensions, and failure modes.
2. **This document (`architectures/00-comparison.md`)** — the matrix and decision guide.
3. **One full architecture spec** — pick the one that matches your context; read it end-to-end.
4. **The other three architecture specs** — skim to understand the design space.
5. **`research/01-` through `07-`** — the source-by-source research reports if deeper provenance is needed.
6. **`research/blocked-urls.md`** — to understand which sources should be re-fetched and re-fed for higher-fidelity research.

---

*End of comparison document — `architectures/00-comparison.md` v0.1*
