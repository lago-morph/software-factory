---
track: brownfield-substrate-first
axis: substrate-first
mandate-scope: brownfield
based-on-commit: 9a205b6
based-on-date: 2026-05-24
---

# Track: Brownfield Substrate-First

*Phase-2 architecture-track output. Strong on the substrate-first axis for the brownfield mandate. Eight peer tracks are in flight; divergence is the design. This track does not resolve cross-mandate questions and does not merge with peers.*

---

## §0 Vocabulary, framing, and the "you don't deserve a different architecture" pre-response

### 0.1 Track-local vocabulary (extends brief §0 glossary)

| Term | Definition |
|---|---|
| **Existing-System Substrate (ESS)** | The set of substrate primitives whose primary input is *the codebase that already exists*: repo-walker, dependency-graph maintainer, change-impact analyzer, runtime-telemetry parser, existing-test-suite ingester, production-log-as-scenario harvester, archaeology cache, issue-history loader. Distinct from the general substrate primitives (sandbox, trajectory capture, judge routing, watchdog, etc.) that this track *inherits without re-deriving*. |
| **Legibility primitive** | A substrate primitive whose only job is to make some property of the existing system *legible* to agents and judges (e.g., "what does this function depend on?", "what production traces hit this module last week?", "what was the operator's stated intent when this file was last touched?"). Legibility primitives produce *typed facts* about the system; they do not produce code. |
| **Codebase-derived scenario (CDS)** | A scenario whose canonical source-of-truth is *inside* the existing system — a production trace, an existing test case, an incident replay, a usage telemetry sample, a fuzz-corpus seed, a runtime invariant inferred from operation. Contrast with the D-2 default (scenarios outside the codebase as holdout). CDS is the brownfield instantiation of StrongDM's own actual practice per CTR-B5 sharpening (Phase-1 WEAK-3): scenarios live *both* inside and outside, and brownfield's natural pull is to the inside. |
| **Archaeology cache** | A typed, append-only, immutable store of *findings about the existing codebase* — symbol graphs, prior-PR rationale, comment-derived invariants, test-fail-pattern signatures, runtime hot-paths. The substrate's answer to F10 (findings disappear into chat) re-cast as "findings about the inherited system disappear into chat". |
| **Production-scissors gate** | The substrate's deterministic refusal point for any write that touches production data, production credentials, or production deployment paths without an explicitly typed elevation. Per F44 (Lethal-Trifecta Production-Scissors Default); default-off, substrate-enforced, not per-cycle operator discipline. |
| **Existing-architecture invariant (EAI)** | A slow-layer pace-layer-4-or-5 constraint of the existing system (Brier framing, F34) — naming conventions, module boundaries, deployment topology, schema contracts, language idioms, performance budgets. EAIs are *inferred from the codebase* by legibility primitives, then *enforced* by judge primitives, not written by humans into a spec. |
| **Cold-substrate / warm-substrate** | Cold-substrate = the substrate has never seen this codebase before (first-encounter). Warm-substrate = the substrate has run ≥N prior cycles against this codebase and the archaeology cache is populated. Brownfield analog of greenfield's cold-start; treated optionally in §5. |
| **Substrate seam** | The boundary between an ESS primitive and the rest of the substrate (e.g., the seam between the dependency-graph maintainer and the judge router). Brownfield's load-bearing fragility hides at seams — the same place CTR-C7 (mail-bus-vs-GitHub-issues) and F31 (substrate floor = weakest adapter) name as substrate-mediated risk. |

### 0.2 Axis defense (substrate-first)

The substrate-first claim, in this track, is that **the brownfield architecture's load-bearing decisions are about what facts about the existing system the substrate makes legible, with what fidelity, at what latency, under what default-off security posture** — and that the methodology layer is downstream of those decisions in a way it is not for greenfield.

Three corroborating reads from the corpus that this track leans on:

1. **Round-2 substrate-heavy thesis** ([`13-round-2-synthesis`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §8): *"Round 2 turned the software-factory project from 'design a methodology' into 'configure a methodology on top of an existing substrate.'"* This track applies that thesis to brownfield specifically: the *existing* in "existing substrate" is doing double duty (the runtime stack and the target codebase), and brownfield needs that duplication to be deliberate.
2. **OpenHands V1 sub-ms persist + 7.4ms replay over 433 SWE-Bench Verified replays** ([`11`](../../../research/11-openhands-substrate-audit.md) §5.2). The corpus' deepest substrate-primitive measurement *was taken on a brownfield benchmark*. SWE-Bench Verified is structurally `Issue + Codebase → PR` (per [`22`](../../../research/22-academic-foundations.md) §4 nutshell-bench diagram); the substrate measurement IS the brownfield measurement.
3. **CTR-B5 sharpening (Phase-1 WEAK-3)**: StrongDM's own pages list *"incident replays, agentic simulation"* as a scenario class. Scenarios live inside the running system in StrongDM's actual practice; the brownfield substrate doesn't invert D-2 — it *reads StrongDM more carefully than the D-2 default did*.

### 0.3 Pre-response to "brownfield substrate is just greenfield substrate plus ingestion"

The Phase-3 critic will say: *"You don't deserve a different architecture. Take greenfield's substrate primitives (trajectory capture, judge router, sandbox, watchdog, cost ceiling, scaffold store), bolt on a repo-walker and an embeddings index, and you're done. Calling it 'brownfield substrate-first' inflates a feature into an architecture."*

Five things are brownfield-load-bearing that don't fall out of greenfield substrate + ingestion:

**(B-1) The security-posture default flips.** Greenfield substrate can plausibly default to *capability-on* (the factory is building its own sandbox; the production-scissors don't exist yet because production doesn't exist yet). Brownfield substrate must default to *capability-off* with explicit typed elevation, because F12, F33, F44 are *constitutively present* on day-0 (per failure-modes-v3 §4 — F33 brownfield critical, F44 brownfield critical, F12 brownfield critical). The Replit DB wipe (1,200 executives' data destroyed during explicit code freeze; [`followup/10`](../../../research/followup/10-governance.md) §3, G1) and the Moltbook breach (1.5M API keys exposed via missing RLS config in 3 days; *ibid* G2) are the empirical anchors. *Inverting a default is not "plus ingestion"; it is a different substrate-level commitment, audited by a different threat model.*

**(B-2) The judge-architecture must be Ashby-adequate against an existing high-variety system, not just an emerging spec.** F51 (Ashby-deficient probabilistic guard) is **critical** for brownfield specifically (per failure-modes-v3 §4a F51 severity rationale): *"brownfield's deterministic perimeter (existing tests, schemas, runtime traces) is the only adequate-variety guard."* This is not a feature on top of greenfield; it's a different regulatory variety. Greenfield's judge can in principle be all-probabilistic because the regulated system is itself still being defined. Brownfield's judge must compose **deterministic perimeter primitives** (typed dependency edges, schema diff checks, existing-test execution, runtime-trace assertions) with probabilistic judges as a *narrower* layer — and the substrate has to ship those perimeter primitives, not delegate them to per-cycle agent code. CTR-D8 (same-model judge legitimacy vs Tournament model-family-diversity) becomes less load-bearing when the substrate provides Ashby-adequate deterministic perimeters; the judge-model-family choice no longer carries the variety load alone.

**(B-3) The scenario surface is constitutively in-tree.** D-2's "scenarios outside the codebase as a holdout set" is flagged fragile for brownfield by the brief itself (§4.1). This track's claim is sharper: in brownfield, the *durable* scenario set is the production-log-as-scenario plus the existing test suite plus incident replays, all of which live inside or are derived from the running system (CTR-B5 + the WEAK-3 sharpening: StrongDM's own page lists incident replays and agentic simulation alongside out-of-tree user stories). This isn't a holdout-set tweak; it's a different substrate-layer commitment about *where canonical truth lives*. The substrate has to provide a holdout-discipline primitive that *partitions in-tree facts* (some scenarios are seen by the builder, some are withheld), which is structurally different from the D-2 default of out-of-tree storage.

**(B-4) Cross-layer drift detection (F34) is the brownfield-critical failure the substrate must own.** F34 brownfield severity is **critical** (existing architecture, conventions, standards as explicit slow-layer invariants; silent violation is the core brownfield risk). Greenfield substrate can defer EAI inference to the methodology layer because the slow-layer reference is itself moving. Brownfield substrate has to *infer EAIs from the codebase* and *enforce them at judge time* — that's a legibility primitive (ESS) plus a judge primitive plus a coordination protocol between them. None of those fall out of greenfield-plus-ingestion.

**(B-5) The substrate has to model the *governance perimeter the existing system already sits inside*.** F30 brownfield severity is **critical** (Replit / Moltbook / Caremark RSI mid-market doctrine; per [`31`](../../../research/31-caremark-rsi-board-exposure.md), [`followup/10`](../../../research/followup/10-governance.md) §3). The substrate must produce *structured board-visible declarations* (RSI status, AILCCP control status, SB 53 reporting status; F43) by reading the existing system's regulatory artifacts, *not* by asking an operator to author them at greenfield-style spec authoring time. This is a *new class of substrate primitive* (governance-declaration emitter) that has no greenfield counterpart at the same severity.

The five together are the brownfield-load-bearing surface this track designs to. *None* of them are a feature on top of greenfield substrate + ingestion; together they re-shape the substrate's default posture, judge composition, scenario semantics, slow-layer detection, and governance interface.

### 0.4 Anti-pattern this track explicitly rejects

The greenfield-imported substrate fantasy: "treat the existing codebase as a really big system prompt, embed it, retrieve top-k, hand to the agent." This pattern survives most of the corpus' vendor reads ([`21`](../../../research/21-tabnine-enterprise.md) §2 makes clear even Tabnine's Context Engine is *RAG plus an agentic graph layer*, not categorically beyond RAG — and Tabnine's posture is conservative). RAG-as-substrate is necessary but radically insufficient against the F12/F33/F34/F44/F51 cascade. This track treats RAG as one *legibility primitive among many*, not as the substrate's load-bearing layer.

---

## §1 The architecture in one paragraph

A brownfield software factory is a layered substrate in which an **Existing-System Substrate (ESS) wedge** — a typed, immutable, event-sourced cache of legibility primitives over the target codebase, its dependency graph, its tests, its runtime telemetry, its issue history, and its deployment topology — sits below the general agent-runtime substrate (sandbox, trajectory capture, judge router, tiered watchdog, cost ceiling, scaffold store, secret store, AGENTS.md/CLAUDE.md discoverability), with a **deterministic-perimeter judge composer** that mediates between ESS facts and probabilistic agent output, a **production-scissors gate** as the substrate's default-off security boundary against the F12/F33/F44 cascade, an **EAI inference + enforcement loop** that derives slow-layer invariants from the codebase and surfaces them to per-cycle judges (F34 mitigation), an **archaeology cache** that promotes per-cycle codebase findings into a durable typed store (F10/F8 mitigation), and a **governance-declaration emitter** that produces board-visible RSI/AILCCP/SB-53 status from the existing system's artifacts (F30/F43 mitigation). The methodology layer — issue queue vs. layered-spec change-request vs. codebase-evolution proposal (OQ-B4) — is downstream of this substrate and can be swapped without re-deriving the substrate.

---

## §2 Primitives (the ESS wedge)

The substrate-first commitment requires naming the primitives. The general agent-runtime substrate (sandbox, watchdog, trajectory, etc.) is inherited from the post-Round-12 corpus consensus and not re-derived here; this section enumerates the *brownfield-load-bearing additions* — the ESS wedge.

### 2.1 Codebase index + symbol graph maintainer

**Inputs:** the target codebase (every commit, by default the default branch HEAD).
**Outputs:** typed symbol table (declarations, definitions, call-edges, type-edges, import-edges) + reverse indexes + per-symbol commit lineage.
**Refresh discipline:** event-sourced on git push; sub-ms persist budget per OpenHands V1 precedent (per [`11`](../../../research/11-openhands-substrate-audit.md) §5.2: event-sourcing is empirically cheap enough that the substrate doesn't need to choose between "capture everything" and "capture some").
**What this is *not*:** an embeddings index. Embeddings are a separate, downstream legibility primitive (§2.2). The symbol graph is *typed and deterministic*; agents can ask "who calls foo()?" and get a closed answer, not a similarity score.
**Why brownfield-load-bearing:** without this, every per-cycle agent re-derives the same graph from scratch via grep, paying F21 (context-window exhaustion, brownfield-critical) every cycle. With this, the per-cycle agent gets typed answers to graph questions in O(lookup) and the context budget goes to *change reasoning*, not *graph discovery*.
**Anti-pattern guarded against:** "the codebase IS the prompt." See §0.4.

### 2.2 Embeddings / RAG index (subordinated)

**Inputs:** files + docstrings + commit messages + PR descriptions + issue bodies.
**Outputs:** vector store; nearest-neighbor retrieval for unstructured prose context.
**Why subordinated:** RAG is the *fallback* legibility primitive when typed graph queries fail. Tabnine's audited reality ([`21`](../../../research/21-tabnine-enterprise.md) §2 "Tabnine's Context Engine **is RAG plus a graph layer on remote repos**") is the corpus-anchored honest framing — RAG is necessary, it is not the load-bearing primitive.
**Composition with §2.1:** the per-cycle agent's query planner prefers typed-graph answers (deterministic, closed) over RAG (probabilistic, open). The substrate exposes both via a uniform legibility API but logs which path served each query — feeding the diagnostic-agent loop (CTR-D4 / §3.3 below).

### 2.3 Dependency-graph maintainer + change-impact analyzer

**Inputs:** symbol graph (§2.1) + the proposed change (diff or planned diff).
**Outputs:** typed *blast-radius* report — which functions / modules / tests / external API consumers are reachable from the change site, with explicit cycles, transitive depth, and known-stable-boundary breakpoints.
**Why brownfield-load-bearing:** the *only* mitigation for F34 (cross-layer drift, brownfield-critical) that the substrate can provide deterministically is "you told us this is a local change; here are the slow-layer surfaces it actually touches." Without this, every per-cycle judge has to re-discover blast radius via probabilistic reading. With it, the judge has a closed list and can apply pace-layer rules deterministically.
**Corpus anchor:** [`followup/12`](../../../research/followup/12-brier-pace-layers.md) (Brier's pace-layers) names ARCHITECTURE.md as the slow-layer reference; the change-impact analyzer is the substrate primitive that lets a per-cycle judge mechanically check "did this diff cross an ARCHITECTURE.md boundary?" without having to read both files into context.

### 2.4 Existing-test-suite ingester + runner

**Inputs:** the existing test suite, its CI configuration, its historical pass/fail signal.
**Outputs:** typed test catalog (per-test: what it asserts, what it covers, when it last ran, its flake history, its runtime cost) + execution adapter that can run any subset against any worktree.
**Why brownfield-load-bearing:** the existing test suite is *the* primary canonical scenario set for a brownfield codebase (CDS, per §0.1). F2 (reward hacking) and F28 (holdout leakage) both demand the substrate withhold *some* scenarios from builder agents; the existing-test-suite ingester is the place where the substrate enforces that withholding — by partitioning the catalog into builder-visible and judge-visible subsets.
**Composition with judge:** the substrate's judge composer (§3.2) consumes the test catalog as one of its Ashby-adequate deterministic perimeter inputs (F51 mitigation).

### 2.5 Runtime-telemetry parser + production-log harvester

**Inputs:** production logs, OpenTelemetry traces, error reports, latency histograms, usage analytics — whatever observability the existing system already emits.
**Outputs:** typed event stream + hot-path catalog + incident-replay corpus (CDS class).
**Why brownfield-load-bearing:** [`18`](../../../research/18-openai-codex-substrate.md)'s OTEL five-event-category export demonstrates the substrate-level pattern (user prompts / tool approvals / tool results / MCP usage / network-proxy decisions); the brownfield-specific extension is that *production OTEL* feeds the *scenario harvester*, not just the agent's own trajectory. Codex's pattern is for the agent's events; the brownfield substrate also ingests the *target system's* events. Reports [`07`](../../../research/07-dark-factory.md) and [`30`](../../../research/30-cognitive-escrow.md) implicitly assume this; this track names it as a first-class primitive.
**Security posture:** all production telemetry is read-only by default; write-back requires the production-scissors gate (§2.9, F44).

### 2.6 Issue-history loader + PR-archaeology cache

**Inputs:** the repo's issue tracker, its PR history with discussion threads, its commit-message corpus.
**Outputs:** typed lookup of "why does this code exist?" — per-symbol-or-region back-references to the issue, the discussion, the rationale, the prior alternative that was rejected.
**Why brownfield-load-bearing:** F9 (spec overfitting), F41 (under-defined-intent debt), and F34 (cross-layer drift) all share a brownfield-specific failure mode: the agent makes a change that locally satisfies a per-cycle prompt but *re-introduces a deliberately-rejected past alternative*. The PR-archaeology cache is the substrate's deterministic answer to "has this been tried before, and why was it abandoned?" — a question no embeddings index reliably answers.
**Anchor:** [`03`](../../../research/03-every-compound-engineering.md) (Compound Engineering)'s `docs/solutions/` is the *methodology-layer* version of this primitive — flat-file, manually-maintained. The substrate-layer version is automated, typed, and read by every judge by default (not just the planner). [`followup/11`](../../../research/followup/11-compound-knowledge.md) (Compound Knowledge plugin) adds the typed four-way classification (insight/playbook/correction/pattern) and `kw:confidence` primitive — the substrate primitive borrows the typing discipline. [`38`](../../../research/38-gas-systems-substrate.md)'s **Beads `discovered-from` edge** is the corpus' strongest engine-level candidate for compounding-of-knowledge expressivity; the PR-archaeology cache adopts the discovered-from edge as its native edge type.

### 2.7 EAI inference + invariant store

**Inputs:** symbol graph (§2.1) + dependency graph (§2.3) + commit history + naming-pattern corpus + the codebase's existing ARCHITECTURE.md / CLAUDE.md / AGENTS.md / linter configs / style rules.
**Outputs:** typed Existing-Architecture-Invariant catalog (module-boundary rules, naming conventions, deprecated-API list, schema contracts, performance-budget assertions, sandboxing posture).
**Why brownfield-load-bearing:** this is the substrate's structural answer to F34 brownfield-critical. The methodology layer cannot enforce slow-layer invariants it doesn't know exist; the substrate must *derive them from the codebase* and *promote them to first-class judge inputs*. The EAI store is what an Ashby-adequate judge (§3.2) consumes alongside test results.
**Methodology-vs-substrate placement (OQ-B9 / CTR-C3):** EAI *inference* is a substrate primitive (it runs once per warm-substrate epoch and incrementally on git push). EAI *enforcement* is a substrate-provided judge primitive that methodology configures (which invariants are blocking vs warning, which are per-work-unit-class waivable).

### 2.8 Governance-declaration emitter

**Inputs:** EAI store (§2.7) + production-telemetry parser (§2.5) + the codebase's existing compliance artifacts (data-classification tags, RLS configs, audit-log infrastructure, SOC2/HIPAA/SOX evidence) + the AILCCP control set ([`followup/10`](../../../research/followup/10-governance.md) §B).
**Outputs:** structured board-visible declaration: RSI status (per [`31`](../../../research/31-caremark-rsi-board-exposure.md) three-part test: durable + compounding + limited-gating), AILCCP control status (Human Approval Gate / sandboxing / immutable logging), SB 53 reporting status.
**Why brownfield-load-bearing:** F30 brownfield-critical and F43 (RSI Board-Visibility Gap). The Caremark mid-market doctrine — *"RSI is not limited to frontier labs"* ([`31`](../../../research/31-caremark-rsi-board-exposure.md) §1) — means any brownfield factory operating on a finance/health/logistics codebase generates board-Caremark exposure on day-1. The substrate emits the declaration as a typed artifact, refreshed per-cycle; no per-cycle agent has to remember to do it.
**This primitive has no greenfield analog at the same severity** (per §0.3 B-5).

### 2.9 Production-scissors gate

**Inputs:** every proposed write (file, network, process, container, deployment) from any agent or sub-agent.
**Outputs:** allow / typed-deny / typed-elevation-required, with a structured audit trail.
**Discipline:** default-off for production data, production credentials, production deployment paths. Elevation requires a typed declaration (which resource, which operation, what scope, what TTL, who/what is authorizing) that is itself audit-logged and watchdog-visible.
**Anchor:** [`32`](../../../research/32-shapiro-completion-chat-agent-claw.md) R3 (*"do not give it production scissors"*) — F44 promotes this from operator-discipline to substrate-default. [`08`](../../../research/followup/08-security-primitives.md) §3 (CaMeL): the gate composes with the CaMeL typed-interpreter boundary; on brownfield, the gate is the deterministic outer layer and CaMeL is the inner closure rule (acknowledging CTR-D5's open question about CaMeL multi-agent generalization).
**Cost-anchor (CTR-E6 acknowledgement):** the CaMeL ~7-point utility tax ([`08`](../../../research/followup/08-security-primitives.md) §3, 77% vs 84% AgentDojo) is the corpus' empirical anchor that *safety has a measurable cost*. This track *accepts the tax explicitly* for brownfield, on the grounds that F12/F33/F44 brownfield-critical severity outweighs a 7-point single-pass utility delta. Cost-ceiling D-5 has to budget for it.

### 2.10 Holdout-partitioning primitive (substrate-enforced)

**Inputs:** the existing-test-suite catalog (§2.4) + the PR-archaeology cache (§2.6) + the production-trace corpus (§2.5).
**Outputs:** typed builder-visible vs judge-visible partition for every CDS.
**Why substrate-not-methodology:** D-4 (holdout discipline) is a Round-2 default; F28 (holdout leakage, brownfield-high) shows methodology-layer enforcement is insufficient. The substrate enforces partition at the *read API* level — builder agents physically cannot read judge-visible scenarios. This is the brownfield instantiation of D-4 with the CDS twist: the partition is *across an in-tree corpus*, not *between in-tree and out-of-tree storage*.

### 2.11 Archaeology cache (general)

**Inputs:** per-cycle findings emitted by builder agents, reviewer agents, judges (typed events).
**Outputs:** durable typed store of findings about *this codebase* — separate from the general scaffold (CLAUDE.md etc.) and from the per-codebase EAI store.
**Why brownfield-load-bearing:** F10 (findings disappear into chat) brownfield-high — *"codebase-archaeological findings about the existing system are scarce and expensive to regenerate."* The archaeology cache is the substrate-level promotion: any agent emitting a typed `archaeology:finding` event has it persisted, indexed, surfaced to future cycles' planners by default.
**Typed-classification discipline:** borrows [`followup/11`](../../../research/followup/11-compound-knowledge.md)'s four-way classification (insight / playbook / correction / pattern) plus the `kw:confidence` first-class primitive plus the no-silent-overwrites rule.

### 2.12 Substrate-inherited primitives (named, not re-derived)

These are inherited from corpus consensus and reframed for brownfield only where the reframing is load-bearing:

- **Trajectory capture** ([`11`](../../../research/11-openhands-substrate-audit.md) §4.2 + Round-2 C16): inherited, no brownfield-specific change.
- **Tiered watchdog (Daemon / Triage / Patrol)** (Round-2 C14): inherited; brownfield-specific note that the *Patrol* tier consumes the EAI store (§2.7) to detect cross-layer drift that the Daemon/Triage tiers structurally cannot see.
- **Judge router (RouterLLM-style)** ([`11`](../../../research/11-openhands-substrate-audit.md) §6): inherited as one judge tactic, *not as the load-bearing F1/F27 mitigation* (per §3.2; the load-bearing brownfield mitigation is deterministic-perimeter composition).
- **Sandbox + Skills closure** ([`23`](../../../research/23-anthropic-engineering-trilogy.md) §3.5): inherited; brownfield-specific note that the Skills "no network access" default ([`23`](../../../research/23-anthropic-engineering-trilogy.md) §3.5) is the *correct* default for brownfield Skills that operate on production data, and the *dreaming* exception (CTR-C9) is gated behind the production-scissors gate (§2.9) with a typed network-access elevation.
- **Cost ceilings as substrate primitive** (Round-2 C15): inherited; brownfield-specific budgeting note in §3.5.
- **Scaffold store (AGENTS.md / CLAUDE.md discoverability)** (Round-2 #9): inherited; CTR-C6 bitter-lesson-vs-scaffold-substrate split engaged in §4 (challenge to D-7 on grounds the EAI store *replaces* much of what AGENTS.md would otherwise carry for brownfield).
- **Secret registry** ([`11`](../../../research/11-openhands-substrate-audit.md) §4.8): inherited; composed with production-scissors gate (§2.9).

---

## §3 Composition — how the primitives interact

### 3.1 The legibility API

Every ESS primitive (§2.1–§2.7, §2.11) exposes a uniform legibility API: agents and judges issue typed queries ("which functions transitively depend on `auth.verify()`?", "what production traces hit module `billing/` last week with status >= 500?", "what was the rationale for not extracting this into a service in PR #1842?") and receive typed answers with provenance.

The API is the substrate's contract; the methodology layer chooses *which* queries to issue and *how* to compose answers. This is the substrate-first commitment: methodology is downstream.

### 3.2 Deterministic-perimeter judge composer (F51 mitigation)

Per §0.3 B-2, the brownfield judge is not a single LLM call; it's a composition. The substrate provides the composer:

1. **Deterministic perimeter (substrate-provided):** existing-test-suite execution (§2.4) over the changed worktree; symbol-graph diff (§2.1) for unauthorized edge introductions; dependency-graph blast-radius check (§2.3) against EAI module-boundary rules (§2.7); schema-diff check; production-telemetry replay (§2.5) for performance-budget assertions.
2. **Probabilistic inner layer (configurable):** LLM-as-judge — model-family-diverse per Tournament/F46 framing, *but the diversity buys less here* because the deterministic perimeter already absorbs the variety. CTR-D7 (Anthropic single-judge finding) and CTR-D8 (Husain/Shankar same-model-judge-is-fine) are *less load-bearing for brownfield* because the deterministic perimeter does the variety-heavy lifting; the LLM-as-judge layer is for the residual probabilistic surface (prose review, intent-vs-implementation alignment, style coherence).
3. **Cross-model critic (per [`34`](../../../research/34-lenny-howiai-personal-harnesses.md) `kevin/carl`):** an optional outer layer for high-blast-radius changes (as scored by §2.3); not the substrate's default.

The composition is what closes F51 in a way no single-layer judge can.

### 3.3 EAI feedback loop (F34 mitigation)

When a per-cycle judge flags an EAI violation, the violation is logged to the archaeology cache (§2.11) with the `correction` type. Periodically (warm-substrate maintenance cadence), the EAI inference job (§2.7) re-runs against the corrections corpus and either (a) ratifies the EAI as load-bearing (raising its enforcement priority) or (b) deprecates it (the codebase has moved past it). The loop is substrate-mediated; no methodology layer has to decide when to re-infer.

### 3.4 Production-scissors composition with secret registry and sandbox

The production-scissors gate (§2.9) is the *outermost* deterministic boundary. The CaMeL typed-interpreter ([`08`](../../../research/followup/08-security-primitives.md) §3) is an *inner* closure rule. The secret registry ([`11`](../../../research/11-openhands-substrate-audit.md) §4.8) is the *credential* primitive that the production-scissors gate consults. Together they form a defense-in-depth that addresses F12 / F33 / F44 *as a cascade* (per failure-modes-v3 F12/F33/F44 cascade notation).

CTR-D5 acknowledged: CaMeL's single-agent closure may not generalize to multi-agent fleets. The production-scissors gate is *fleet-level* by default (every agent's write goes through the gate), which provides an outer-layer guarantee even where CaMeL's inner closure is uncertain.

### 3.5 Cost-ceiling integration

Round-2 D-5 (cost ceilings non-optional in CI) is inherited. Brownfield-specific budget items:

- **ESS refresh cost** (§2.1, §2.3, §2.5, §2.6, §2.7): amortized per-commit, dominated by symbol-graph and dependency-graph maintenance; OpenHands-V1-class sub-ms persist economics ([`11`](../../../research/11-openhands-substrate-audit.md) §5.2) suggest this is sub-token-cost per cycle.
- **Existing-test-suite execution cost**: load-bearing on F34/F51 mitigation; brownfield substrate budgets for full-suite execution per cycle by default, with selective re-execution as an optimization, *not* as the default. (Brownfield's existing suite is the only cheap Ashby-adequate variety source the substrate has.)
- **CaMeL utility tax (~7-point per CTR-E6)**: budgeted explicitly; the substrate doesn't apologize for it.
- **Production-telemetry ingestion cost**: streaming, amortized; bounded by retention policy declared in the governance-declaration emitter (§2.8).

The cost-anchor disagreement (CTR-E1: Cherny $100K+/month vs $500-$5000/day) is one substrate budget away from being a methodology problem; the substrate enforces the ceiling, the methodology chooses how to spend within it.

---

## §4 §4 defaults — accepted vs challenged

Per D3, this track marks each of the seven brief §4.1 defaults.

### D-1. Specs are the durable, version-controlled, human-curated artifact

**Marking: challenged (conditionally) for brownfield substrate-first.**
Rationale: per CTR-B7 (Brier vs Nystrom) and CTR-B4 (Grove vs Willison), the brownfield substrate-first framing puts *the existing codebase + EAI store + archaeology cache* as the load-bearing durable artifacts. A spec exists (for each change request or evolution proposal) but is *not* the most durable artifact — the codebase is, by D-2's own existing-system-as-given logic in UC4 and the F20 mandate framing. The spec is durable *at the cycle scope*; the codebase + EAI + archaeology are durable at the *factory scope*. This track recommends a substrate-level distinction: per-cycle specs are versioned in the issue/PR system (existing primitive); cross-cycle invariants live in the EAI store (§2.7). Surfaced as DECISIONS-PENDING for Phase-3 merge.

### D-2. Scenarios live outside the codebase as a holdout set

**Marking: challenged for brownfield substrate-first.** *(Brief itself flags this as fragile for brownfield.)*
Rationale: per §0.1 (CDS), §0.3 (B-3), §2.4 (existing-test-suite ingester), §2.5 (runtime telemetry as scenario), and CTR-B5 + WEAK-3 sharpening. Brownfield's canonical scenario set is in-tree or derived-from-tree. The substrate-level fix is the holdout-partitioning primitive (§2.10) that *partitions in-tree facts* rather than relying on out-of-tree storage. D-2 should be re-stated for brownfield as: *"scenarios may live inside or outside the codebase; holdout discipline is enforced by substrate-level partition, not storage location."* The reformulation makes brownfield closer to StrongDM's actual practice (per WEAK-3) than D-2's stated default was.

### D-3. Agent = Model + Harness

**Marking: accepted with caveat, for brownfield substrate-first.**
Rationale: this track's primitives don't require graph-node or population shapes, so the C10 fragility (brief §4.1) doesn't bite. However, CTR-C10 (Portuguese-vs-English policy-layer effect) is acknowledged as a real fragility — for brownfield agents operating on multilingual codebases (comments, docs, identifiers in non-English), the harness includes a *natural-language register* that the substrate should make visible in the trajectory. This is a logging extension, not an architecture change; recommend deferring to Phase-5 ADR.

### D-4. Holdout discipline is substrate-enforced

**Marking: accepted with justification.**
The brownfield re-statement (§2.10) is *more demanding* than D-4's original: not only must the substrate enforce holdout, but it must enforce holdout *within an in-tree corpus*. This strengthens D-4 rather than weakening it.

### D-5. Hard cost ceilings are non-optional in CI

**Marking: accepted with justification.**
Budgeting elaborated in §3.5. The CaMeL utility tax (CTR-E6) is the only corpus anchor for safety-has-a-measurable-cost; brownfield accepts that cost explicitly. The Cherny-vs-noosphr cost disagreement (CTR-E1) is one substrate budget away from being a methodology choice.

### D-6. Tiered watchdog (Daemon / Triage / Patrol)

**Marking: accepted with brownfield-specific extension.**
Patrol tier consumes the EAI store (§2.7); without this extension, Patrol can't detect cross-layer drift (F34 brownfield-critical). The extension is a reading-only addition to the watchdog API.

### D-7. Trajectory capture is cheap and production-tested

**Marking: accepted with justification.**
The OpenHands V1 measurement (sub-ms persist, 7.4ms median crash recovery over 433 SWE-Bench Verified replays — *a brownfield benchmark*) is the corpus' strongest empirical anchor and it lives in our mandate's native test bed. The brownfield ESS refresh cost (§3.5) is in the same economic neighborhood; this default holds with high confidence for brownfield.

### Note on scaffold (CTR-C6 bitter-lesson split)

Not a §4 default, but called out by brief §0 vocabulary and Phase-1 WEAK-2. This track sits on the *scaffold-substrate* side of the bitter-lesson cleavage *for brownfield*, on the grounds that brownfield codebases already have scaffolds (AGENTS.md, CLAUDE.md, ARCHITECTURE.md, READMEs, contribution guides) and the EAI store (§2.7) *infers EAIs from those scaffolds*. The bitter-lesson camp (Jaymin manifesto / Gas City) is correct that grep-as-substrate works for greenfield-ish situations where the codebase is small enough; for brownfield at scale (100k+ LOC), the EAI store + symbol graph + archaeology cache replace what grep alone cannot deliver at acceptable latency under the F21 context-window budget.

---

## §5 Warm-start / first-encounter-with-a-codebase

**Brief permits omission; this section is included because there is a brownfield-specific phenomenon worth naming.**

Brownfield substrate has a *cold-substrate* state (the substrate has never seen this codebase) and a *warm-substrate* state (the ESS wedge is populated for this codebase). The cold→warm transition is the brownfield analog of greenfield cold-start, but with fundamentally different shape:

- **Inputs at cold-substrate:** the codebase, its tests, its issue tracker, its CI history, its production telemetry retention, its compliance artifacts, its team's existing scaffold (AGENTS.md etc.).
- **No design choices to make.** Cold-substrate is *ingestion-bounded*, not *spec-authoring-bounded* (the greenfield cold-start failure shape, per brief §5).
- **Failure modes during cold-substrate:** ingestion is incomplete (some private deps, some test environments unreachable); EAI inference produces false positives that have to be deprecated through the §3.3 loop; archaeology cache starts empty so the first N cycles get less F8/F10 mitigation than steady-state.
- **Trajectory cold → warm:** dominated by ESS refresh wall-clock, not by cycles. A 1M-LOC codebase with 10-year history needs hours-to-days of initial symbol-graph + dependency-graph + EAI inference; the substrate accepts this as the brownfield onboarding cost. Production-telemetry corpus warms with operational time, not factory-cycle time.
- **Bootstrap protection:** because the substrate's deterministic perimeter (existing tests) is available from the first cycle, the substrate has *Ashby-adequate variety from day 1 against the existing system's own definition of correctness* — the cold-substrate factory is not flying blind in the way a cold-start greenfield factory is. F1/F27 mitigation through existing-test-suite execution is available before the EAI store is mature.

This asymmetry is precisely why "brownfield substrate is just greenfield substrate plus ingestion" misreads the situation (§0.3): brownfield's day-1 trust foundation is the existing system's own behaviour, not a spec the factory just wrote.

---

## §6 What this track does *not* decide

Per discipline rule 4 (don't resolve cross-mandate questions) and rule 5 (don't merge with other tracks):

- **Unit of work shape (OQ-B4).** Issue-from-queue vs change-request-against-spec vs codebase-evolution-proposal is a methodology choice; the substrate supports all three (the legibility API is shape-agnostic). The brief mandates Phase-2 brownfield tracks treat this; this track's answer is *the substrate is choice-agnostic; the methodology layer picks*. Whether *that* is a valid answer is for Phase-3.
- **Operating-mode (OQ-B1 lights-out / L5 / regime).** Per §0.3 and §2.8 (governance-declaration emitter), this track can deliver structured evidence about *which* control regime is in effect, but doesn't pick option (a)–(e) of brief §2.1. Recommend the F30/F43 governance posture (option c — regime classification scheme) but defer to Phase-3.
- **Human re-entry mechanism (OQ-B3).** The production-scissors gate provides typed-elevation-required as the canonical re-entry trigger; *who* the human is and *what* the protocol is, methodology.
- **Provider-property requirements (OQ-B8).** RouterLLM is one tactic among several; this track doesn't take a position on whether RouterLLM is the right abstraction level — the substrate exposes the judge composer (§3.2), the methodology configures the routing.
- **Methodology-evolution placement (OQ-B9).** This track says EAI *inference* is substrate and EAI *enforcement* is substrate-provided / methodology-configured (§2.7); the broader question of whether *all* methodology evolution is substrate-mediated is left open.
- **Greenfield substrate sharing.** Phase-4 decides which ESS primitives have greenfield counterparts and which are brownfield-only. This track's prediction is that §2.1 (symbol graph), §2.11 (archaeology cache), and §2.12 (inherited primitives) plausibly share; §2.3 (change-impact), §2.4 (existing-test-suite), §2.5 (production-telemetry), §2.6 (PR-archaeology), §2.7 (EAI), §2.8 (governance-declaration) are brownfield-load-bearing in ways that may not translate.

---

## §7 Phase-3 adversarial anticipation

The brownfield critic's strongest moves and this track's pre-responses.

### 7.1 "You overweight greenfield-imported substrate primitives that don't match brownfield's reality."

This is the brief's named adversarial challenge for this track. Pre-response:
- The inherited primitives (§2.12) are explicitly named as inherited and reframed only where brownfield demands.
- The brownfield-load-bearing primitives (§2.1–§2.10) are derived from brownfield-specific failure-mode severities (F12 / F30 / F33 / F34 / F44 / F51 all critical for brownfield) and brownfield-specific corpus anchors (SWE-Bench Verified as Issue+Codebase→PR, Tabnine Context Engine on-prem, Compound Engineering's `docs/solutions/` as the methodology-layer twin, Beads' `discovered-from` edge).
- §0.3's five-item list (B-1 through B-5) names what specifically doesn't fall out of greenfield-plus-ingestion. The critic has to attack those five, not the substrate-first framing.

### 7.2 "Your ESS wedge is just RAG with a graph layer; you're describing Tabnine Context Engine and calling it an architecture."

Pre-response:
- Per §2.2 and §0.4, RAG is subordinated to typed symbol-graph queries, not the load-bearing primitive.
- The Tabnine audit ([`21`](../../../research/21-tabnine-enterprise.md)) itself shows that the *governance posture* (P&A non-overridability, air-gapped attribution DB, per-repo opt-in advanced indexing, admin-set Context Engine User, ephemeral processing) is what makes Tabnine governance-rather-than-advice. This track adopts the non-overridability discipline (production-scissors gate is non-overridable), the per-repo / per-scope opt-in (EAI enforcement priorities are typed), the typed identity (Context Engine User → typed agent identity in the secret registry).
- ESS includes §2.5 (production telemetry), §2.6 (PR archaeology with discovered-from edge), §2.7 (EAI inference), §2.8 (governance-declaration), §2.10 (in-tree holdout partition) — none of which Tabnine ships and none of which are "RAG with a graph layer."

### 7.3 "You accept the CaMeL utility tax but don't account for the cumulative cost of all these primitives."

Pre-response: §3.5 explicitly budgets ESS refresh + existing-test-suite execution + CaMeL tax + telemetry ingestion. The corpus cost-anchor (CTR-E1) is one substrate-budget knob; this track doesn't claim the brownfield substrate is cheaper than greenfield, only that its costs are budgetable and the F-mode severities justify them.

### 7.4 "Your EAI inference is hand-wavy and probably hallucinates invariants that don't exist."

Pre-response: §3.3 (EAI feedback loop) is the substrate's answer — every flagged EAI violation feeds back to either ratify or deprecate. The substrate produces *candidate* invariants from inputs that include *existing human-authored scaffold* (ARCHITECTURE.md, linter configs, style rules); the inference is grounded, not free-form. False positives are expected; the loop is designed for them. Acknowledged open question: what's the right cadence for re-inference, and is there a substrate-level guard against an EAI inference loop that converges on a hallucinated invariant? (See §8.)

### 7.5 "Production-scissors gate as a substrate default-off is operationally infeasible — brownfield agents need write access to ship value."

Pre-response: typed-elevation-required is not "no writes ever"; it's "every write is authorized through a declared, audit-logged, watchdog-visible path." The Replit empirical anchor ([`followup/10`](../../../research/followup/10-governance.md) §3 G1) — 1,200 executives' data destroyed *during an explicit code freeze* the agent ignored — is the corpus' strongest argument that operator-discipline-as-control fails and substrate-default-off is required. The infeasibility framing is the F44 production-scissors framing the failure-mode catalog explicitly names as a constitutive brownfield critical risk.

### 7.6 "Your D-1 challenge (specs not the most durable artifact for brownfield) breaks Phase-3's unified synthesis ability."

Acknowledged risk. The challenge is conditional ("durable at cycle scope vs factory scope" — both true at different granularities); recommend Phase-3 treat as a *layering decision* rather than a contradiction.

### 7.7 "You haven't engaged the Brier counter-metaphor (CTR-F1)."

The brownfield substrate-first framing is closer to Brier's *software-company* (codebase-as-organizational-artifact, EAI-as-standards-layer, archaeology-as-culture) than to the StrongDM Ford-factory. The pace-layer mapping is direct: EAI store ≈ Brier's standards layer; ARCHITECTURE.md ≈ Brier's architecture layer; per-cycle issue ≈ Brier's plans layer; diff ≈ Brier's code layer. The substrate-first framing for brownfield is *more* compatible with the pace-layer mental model than with the factory metaphor. Per Phase-1 MISSED-10 (Notion/Boxy ratifying "factory" internally even while Boxy is the day-to-day name), this isn't a metaphor war the substrate-first track has to win — it's a framing the track is comfortable with both metaphors of.

---

## §8 Open questions this track raises

- **OQ-T1.** What's the right cadence for EAI re-inference (§2.7 / §3.3), and is there a substrate-level guard against an EAI inference loop that converges on a hallucinated invariant?
- **OQ-T2.** Does the production-scissors gate (§2.9) compose cleanly with multi-agent fleets given CTR-D5's open question about CaMeL fleet-generalization?
- **OQ-T3.** The PR-archaeology cache (§2.6) borrows Beads' `discovered-from` edge; what happens when the substrate substitutes a different engine? (See [`38`](../../../research/38-gas-systems-substrate.md) substrate-vs-application split.)
- **OQ-T4.** The governance-declaration emitter (§2.8) consumes the existing system's compliance artifacts; what happens when the existing system has *none* (brownfield in an undisciplined codebase that was supposed to be in scope but is itself ungoverned)?
- **OQ-T5.** Does the in-tree holdout-partitioning primitive (§2.10) survive an adversarial codebase author who deliberately structures tests to be unsplittable? (Likely a methodology problem in disguise; flagged for Phase-3.)
- **OQ-T6.** Are there ESS primitives this track missed that are brownfield-load-bearing? (Candidate: per-file blame-derived "ownership" graph, deployment-topology-derived blast-radius extension into infra. Both arguably collapse into §2.3 and §2.7.)

---

*End of brownfield-substrate-first.md*
