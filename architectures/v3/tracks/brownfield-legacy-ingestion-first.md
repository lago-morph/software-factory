---
based-on-commit: 9a205b6
based-on-date: 2026-05-24
track: brownfield-legacy-ingestion-first
axis: legacy-ingestion-first
mandate-scope: brownfield
---

# Brownfield architecture track — legacy-ingestion-first

**Track role.** One of 9 parallel Phase-2 tracks. Strong on the **legacy-ingestion-first** axis for the **brownfield mandate**. Per the [v3 brief](../00-brief-v3.md) §3 + [D1](../decisions-captured.md#d1--phase-2-fanout-9-parallel-tracks-3--3--3), the other 8 tracks are running independently; this track does not resolve substrate vs. methodology cross-mandate questions and does not attempt unification.

**Thesis in one sentence.** For brownfield, **code archaeology is not a bootstrapping step but a continuously-running substrate process whose output (the *ingestion artifact*) is read by every cycle, by every agent, on every iteration** — and the architecture's load-bearing primitives all hang off the shape and freshness of that artifact.

---

## §0. Glossary, framing, and pre-respond to "ingestion is just bootstrap"

### 0.1 Brief-§0 glossary terms used unchanged

`brownfield`, `substrate`, `methodology`, `harness`, `scaffold`, `lights-out`, `mandate-fit`, `work-unit-class`, `Daemon/Triage/Patrol`, `Atelier-style`, `Refinery-style`, `AGENTS.md`. Defined in the [brief §0](../00-brief-v3.md#0-glossary-defined-terms-used-in-this-brief); used per the brief.

### 0.2 Track-local vocabulary

| Term | Definition (this track only) |
|---|---|
| **Ingestion artifact** | The durable, version-controlled, machine-readable + human-readable representation of "what's in this codebase" that every cycle reads. Not a one-off bootstrap output; a **continuously-refreshed substrate primitive** with its own update protocol, freshness SLO, and freshness watchdog. The artifact's *contents* are deliberately under-specified at this track level; the *primitive position* in the architecture is the load-bearing claim. |
| **Code archaeology** | The set of activities that produces and refreshes the ingestion artifact. Includes: structural mapping (modules, dependency graph), convention extraction (naming, error-handling, test patterns), invariant mining (what the code asserts about itself), hot-path identification (production telemetry, profiles), debt-cluster identification (lint debt, complexity, stale code), runtime characterization (build/deploy reality, observed latency/error envelopes), idiom library, and a *what-changed* delta against the last refresh. |
| **Pace-layer pinning** | Per [Brier followup/12](../../../research/followup/12-brier-pace-layers.md), the ingestion artifact pins each element of the codebase to a pace layer (code / plans / specs / architecture / standards). The pinning is itself a substrate output, and the cycle reads it to decide *which gates apply to a proposed change*. |
| **Ingestion-as-judge-input** | The ingestion artifact is a primary input to the judge layer (in addition to the spec / acceptance criteria). The judge's "is this change consistent with the codebase" check is structurally distinct from "does this change pass the tests." |
| **Re-ingestion trigger** | A substrate-level event that causes a partial or full re-ingestion: a merged PR touching pace-layer 4–5 elements; a dependency upgrade; an observed runtime-envelope drift; a calendar SLO. |
| **Latent invariant** | A property the code *enforces* but does not *declare* (e.g., "all writes to table X go through repository R"; "function F is only called from thread T"). Ingestion surfaces these so cycles can be judged against them. |

**Discipline.** *Code-archaeological* is the brief's contamination-flagged compression of [UC4](../constraints-extracted.md#uc4--users-working-hypothesis-treated-as-falsifiable-not-assumed). Per the brief's [contamination footnote](../00-brief-v3.md#3-working-hypothesis--to-test-not-assume), the underlying claim — "brownfield's architecture is largely fixed by the existing codebase; the factory analyses what is there and grows it" — is what this track tests. The track's view: UC4's underlying claim is **mostly right but understated**. It is not enough to *analyze and grow*; the factory must *continuously re-analyze*, because every cycle and every external change ages the analysis. The label is fine; the under-statement is the issue.

### 0.3 Pre-respond — "ingestion is one-time bootstrap, not an axis"

The strongest objection to this track's framing:

> *"Ingestion is a one-time bootstrap, not an architectural axis. Once you've indexed the codebase you're back to per-cycle work — the cycle is the architecture, the ingestion is a setup script."*

Four-part response, each of which is operationalized in §§2–4:

1. **Ingestion is read on every cycle, not just at bootstrap.** The cycle's planner reads the ingestion artifact to find the right place to make a change; the builder reads it to learn conventions; the judge reads it to detect convention violations; the watchdog reads it to detect cross-layer drift (F34). If the artifact stops getting refreshed, every one of those reads silently degrades. The cycle is not above the ingestion artifact; the cycle *consumes* it.
2. **Brownfield drift makes re-ingestion a recurrent obligation, not a setup task.** Every merged PR (whether from the factory or outside contributors), every dependency upgrade, every runtime-envelope shift, every standards change ages the artifact. The architecture has to declare a *re-ingestion trigger set* and a *freshness SLO*, both substrate-enforced. Without this, F8 (stale-knowledge inversion), F34 (cross-layer drift), F35 (federation-as-family drift), F55 (behavioural drift) compound. See [F-mode treatment](#3-load-bearing-failure-modes-this-track-addresses).
3. **Ingestion is the substrate primitive that distinguishes brownfield from greenfield.** Greenfield's analog would be "domain corpus ingestion" or "exemplar-project ingestion," which is materially different and arguably substrate-shared (Phase 4 question). For brownfield, the ingestion artifact replaces several greenfield primitives at once: it is the durable scenario source (challenging [D-2](../00-brief-v3.md#41-the-defaults)), the latent spec source, the invariant source for the judge, the pace-layer-pinning source, and the convention source for the builder. That is not a setup script.
4. **The "back to per-cycle work" framing presupposes the cycle's primitives are fixed.** They are not. A factory running cycles against a 200kLOC codebase needs different primitives than one running cycles against a 5MLOC codebase or a polyrepo federation. The ingestion artifact *parameterizes the cycle* — what gates run, what context the builder gets, what watchdog cadences fire. Different brownfields require different cycle shapes; the ingestion artifact is how the substrate communicates "what brownfield am I in" to the cycle layer.

The objection collapses ingestion to "indexing a codebase once." The track's claim is that ingestion is a **continuously-running substrate process that produces a durable artifact every cycle depends on** — closer to "trajectory capture" ([D-7](../00-brief-v3.md#41-the-defaults)) or "watchdog" ([D-6](../00-brief-v3.md#41-the-defaults)) in its substrate-primitive role than to a one-shot indexer.

### 0.4 Anticipate Phase-3 adversarial critics

- **Substrate-first critic** ("ingestion is one substrate primitive, not the architecture"): conceded — ingestion is *a* primitive, not *the* architecture. The legacy-ingestion-first axis is not "ingestion is the architecture"; it is "ingestion is the **organizing primitive** the rest of the architecture is downstream of, and the design of every other primitive (judge, scaffold, watchdog, scenario source) is constrained by the ingestion artifact's shape." This is structurally the same move greenfield-cold-start-first tracks make with cold-start.
- **Methodology-first critic** ("you've underweighted the cycle process that consumes the ingestion"): partially conceded. This track deliberately treats the cycle process as downstream of ingestion (§4 sketches cycle primitives but does not specify them) because the brief assigns one of the 3 brownfield tracks to methodology-first. The split is by design. What this track defends: any cycle-process choice — Atelier-style, Refinery-style, or a third shape — has to consume the ingestion artifact, so the ingestion-first track's primitives constrain the methodology-first track's cycle.

---

## §1. Axis defence — why legacy-ingestion-first organizes brownfield

### 1.1 The corpus is brownfield-bench-shaped

The corpus' single deepest empirical benchmark is **SWE-bench Verified** ([report 22](../../../research/22-academic-foundations.md), re-tagged `brownfield-primary` per [CHALLENGE-8](../bias-guards/phase-1/miscategorization-audit.md)). The canonical "nutshell-bench" diagram is **Issue + Codebase → LM → PR → Tests**. Three of the four inputs to the central diagram are *artifacts of an existing system*; the codebase is the largest and the most under-modelled. The factory's first job is to make that input *legible*. Without ingestion, "Issue + Codebase → PR" reads "Issue + opaque-blob → PR," which is exactly the regime the SWE-bench Verified annotation discipline (4-level severity, ensemble-3, 93 developers) was designed to call out.

### 1.2 Compound Engineering's native habitat is brownfield because issues presuppose a system

Per [CHALLENGE-6](../bias-guards/phase-1/miscategorization-audit.md), [report 03](../../../research/03-every-compound-engineering.md) (Compound Engineering) is brownfield-primary: the "queue of issues + accumulating skills + agent panel review" shape presupposes a pre-existing system that has issues. [Followup 11](../../../research/followup/11-compound-knowledge.md) (Compound Knowledge) is the same shape with typed learnings (insight/playbook/correction/pattern) and `kw:confidence`. Both are corpus-popular methodology anchors, and both *consume* a codebase they did not build. Compound Engineering's `docs/solutions/` is the **knowledge-store half** of brownfield's substrate; the ingestion artifact is the **codebase-state half**. Together they form the durable input set for every cycle. Neither one alone is sufficient — and the corpus has under-modelled the codebase-state half because *Compound Engineering's framing assumes the codebase is just there*.

### 1.3 Brier's pace-layers framework already names the substrate

[Followup 12 (Brier)](../../../research/followup/12-brier-pace-layers.md) — flagged `counter-metaphor` (must engage dialectically per [CHALLENGE-14](../bias-guards/phase-1/miscategorization-audit.md)) — provides the strongest argument that brownfield architecture is **already layered**: code (1) / plans (2) / specs (3) / architecture (4) / standards (5), each moving at different speeds, each constraining the layers below. Brier proposes **ARCHITECTURE.md per repo** as the durable invariant store; the factory should respect that.

The dialectical engagement: Brier's framework is the *first half* of what an ingestion artifact does. Brier names pace layers as a *concept the human carries*; this track makes the layer-pinning a *machine-readable substrate output* that the cycle reads. Where Brier disagrees with the factory frame — *"It's a software company, not a software factory"* ([CTR-F1](../contradictions.md)) — this track concedes the disagreement and proposes the ingestion artifact as the bridge: the factory metaphor needs the company's institutional memory to survive lights-out operation, and the ingestion artifact is that memory, encoded.

[F34 (cross-layer drift)](../failure-modes-v3.md#f34--cross-layer-drift), promoted from Brier, is **brownfield-critical**. The ingestion artifact's pace-layer pinning is the substrate-level F34 mitigation — the judge can refuse a change that touches pace-layer 4–5 without an architectural-spec amendment.

### 1.4 The brownfield-critical F-modes cluster around ingestion-shaped failures

Per the [v3 failure-modes catalog](../failure-modes-v3.md), the brownfield-`critical` set is dominated by F-modes the ingestion artifact directly mitigates (or whose mitigations live in the ingestion-refresh protocol):

| F-mode | Brownfield severity | Why ingestion-first matters |
|---|---|---|
| [F20](../failure-modes-v3.md#f20--maintenance-vs-greenfield-asymmetry) — maintenance vs greenfield asymmetry | **critical** | "Survive a living codebase" *is* the ingestion question. |
| [F12](../failure-modes-v3.md#f12--lethal-trifecta--prompt-injection) — lethal trifecta | **critical** | Ingestion artifact carries the typed perimeter (per [F44](../failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default)); cycle can't accidentally compose the trifecta. |
| [F21](../failure-modes-v3.md#f21--context-window-exhaustion--silent-degradation) — context-window exhaustion | **critical** | Ingestion produces *per-cycle context budgets* — the planner picks what to load, not "load the whole codebase." |
| [F27](../failure-modes-v3.md#f27--circularity--same-model-builds-and-validates) — circularity | **high** | Ingestion provides out-of-distribution signal (existing tests, runtime telemetry) that defeats correlated errors. |
| [F33](../failure-modes-v3.md#f33--adversarial-prompt-defeat-of-llm-based-security-analysis) — adversarial-prompt defeat | **critical** | Ingestion-derived deterministic perimeter is the Ashby-adequate guard (see [F51](../failure-modes-v3.md#f51--ashby-deficient-probabilistic-guard)). |
| [F34](../failure-modes-v3.md#f34--cross-layer-drift) — cross-layer drift | **critical** | Pace-layer pinning *is* the F34 mitigation; without ingestion, the slow layers are invisible to the per-cycle judge. |
| [F44](../failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default) — production-scissors default | **critical** | Ingestion identifies which paths *are* production scissors; substrate-default-off uses the ingestion artifact to know what "production" means. |
| [F54](../failure-modes-v3.md#f54--goal-subversion-rsi-prompt-injection-over-cycles) — goal subversion | **critical** | Ingestion captures the *current* goal-frame snapshot; multi-cycle drift detection compares the live frame to the snapshot. |
| [F56](../failure-modes-v3.md#f56--guardrail-bypass-under-stress-replit-class-incident) — guardrail-bypass under stress | **critical** | Ingestion identifies the production-write paths the substrate must default-off (Replit DB wipe class). |

This is not coincidence. Brownfield's critical-severity F-modes are mostly **"the factory did something that violated a property the existing system implicitly held."** The ingestion artifact is the catalog of those properties.

### 1.5 OQ-B4 framing: the unit of work hangs off ingestion

[OQ-B4](../00-brief-v3.md#8-open-questions-surfaced-by-this-brief-deliberate) asks whether brownfield's unit of work is an Atelier-style *issue*, a Refinery-style *change request against a spec*, or a *codebase-evolution proposal*. **All three consume the ingestion artifact**, but each consumes a different slice:

- **Issue** → ingestion provides "what part of the codebase does this issue touch, and what conventions / tests / invariants apply there?"
- **Change request against a spec** → ingestion provides "which pace layer does this change live at, and which slow-layer invariants does it commit to preserving?"
- **Codebase-evolution proposal** → ingestion provides the *current shape* the proposal is evolving *from*.

The ingestion-first axis is **not a vote on OQ-B4**. It is the claim that OQ-B4 is downstream of the ingestion artifact's shape: the artifact you build constrains which units of work the cycle can express.

---

## §2. The ingestion artifact as substrate primitive

### 2.1 Substrate position

The ingestion artifact sits at the **substrate** layer, alongside trajectory capture ([D-7](../00-brief-v3.md#41-the-defaults)), holdout discipline ([D-4](../00-brief-v3.md#41-the-defaults)), cost ceilings ([D-5](../00-brief-v3.md#41-the-defaults)), and watchdog ([D-6](../00-brief-v3.md#41-the-defaults)). It is **not** a methodology concern (which cycle-process to run). Methodologies are free to consume it differently; the substrate guarantees its existence, freshness, and shape.

This positioning is deliberate, and is the track's main bet against the "ingestion is bootstrap" critique. If ingestion is methodology-layer, it can be skipped by an architecture that prefers per-cycle ad-hoc analysis (a real corpus position — see [CTR-C6 Jaymin manifesto](../contradictions.md#ctr-c6--scaffold-as-load-bearing-jaymin-book-vs-scaffold-as-anti-pattern-jaymin-manifesto), *"grep-equipped CLI agents should read the code itself, documentation is a liability because it drifts"*). Putting ingestion at substrate means the methodology layer **cannot opt out**; cycles either read the artifact or the substrate refuses to dispatch them.

The track engages with Jaymin-manifesto / Gas City "bitter lesson" position seriously ([sharpening WEAK-2](../contradictions.md) of CTR-C6). The bitter-lesson argument is that documentation drifts and grep-equipped agents are better. The ingestion artifact's response: **it is not documentation; it is machine-extracted state with a substrate-enforced freshness SLO, regenerated from the code on every refresh trigger.** Drift is the failure mode the substrate is built to detect and remediate. Where Jaymin-manifesto/Gas City says "skip the scaffold," this track says "the scaffold is auto-generated and continuously verified against the code."

### 2.2 Required properties (not contents)

The artifact's *contents* are intentionally under-specified at this track level — Phase-4 substrate-extraction work and Phase-5 ADRs decide the schema. The *required properties*:

1. **Durable.** Survives factory crashes, session resumption, and re-ingestion. Lives in version control.
2. **Versioned.** Carries a commit hash + ingestion timestamp; older versions reconstructible.
3. **Machine-readable + human-readable.** Per [F38 (vocabulary lint debt)](../failure-modes-v3.md#f38--vocabulary-lint-debt) discipline, the human-readable surface follows INCOSE-GtWR-style structural rules to defeat hedge-language drift; the machine-readable surface is the substrate's primary consumer.
4. **Provenance-tagged.** Every claim in the artifact cites the file / commit / telemetry-window / test-run it derives from (per [F14](../failure-modes-v3.md#f14--attribution-collapse) widening to causal-chain reconstruction).
5. **Freshness-tracked.** Carries a *freshness vector* (per-section staleness scores) and a substrate-level SLO; degradation triggers re-ingestion. Patrol-tier (per [D-6](../00-brief-v3.md#41-the-defaults)) watchdog escalates persistent freshness violations.
6. **Diff-able.** Two artifact versions produce a structured delta the cycle can read ("modules added," "conventions shifted," "test pattern changed," "invariant added/removed"). The delta itself is a first-class artifact.
7. **Pace-layer-pinned.** Per Brier (§1.3), every artifact element carries a pace-layer tag (code 1 / plans 2 / specs 3 / architecture 4 / standards 5).
8. **Trifecta-aware.** Per [F12 / F33 / F44](../failure-modes-v3.md#f12--lethal-trifecta--prompt-injection) cascade — production-write paths, secret-store paths, and external-data paths are explicitly catalogued so substrate-default-off has something to default off *from*.
9. **Invariant-explicit.** Latent invariants (§0.2) surfaced and tagged with derivation evidence (tests that enforce them, runtime traces that match them).

### 2.3 What the artifact does NOT do

To avoid scope creep:

- **Not a spec.** The spec (per [D-1](../00-brief-v3.md#41-the-defaults)) is a separate, human-curated artifact; the ingestion artifact is mechanically derived. Per [CTR-B7 (Brier vs Nystrom spec-velocity)](../contradictions.md#ctr-b7--brier-code-is-fashion--free-to-reproduce-vs-nystrom-spec-git-history-is-the-changelog-missed-6), this track sides with Brier on *the ingestion artifact moves at code-pace*, and the spec (separate) sits in pace-layer 3 above it. Whether *the spec* moves at Brier-speed or Nystrom-speed is a methodology-track concern, not this track's call.
- **Not the unit of work.** Per §1.5, the artifact constrains but does not name the unit of work.
- **Not the trajectory.** Trajectories ([D-7](../00-brief-v3.md#41-the-defaults)) capture *what the factory did*; the ingestion artifact captures *what the codebase is*. Both are substrate primitives; they reference each other (trajectories cite ingestion versions; ingestion freshness is partly measured from trajectory rate).

### 2.4 The re-ingestion protocol

The substrate-level protocol for keeping the artifact fresh:

1. **Triggers.** Substrate listens for: merged PRs touching pace-layer 4–5 elements; dependency upgrades; runtime-envelope drift signals from observability (per-deployment latency, error-rate, throughput envelopes); declarative SLO timer expiration; explicit operator-issued re-ingest. Each trigger names its scope (full / module / pace-layer).
2. **Cadence.** Substrate enforces a *base freshness SLO* (e.g., 7 days) regardless of triggers; expired artifact blocks dispatch.
3. **Cost ceiling.** Re-ingestion cost is enforced under [D-5](../00-brief-v3.md#41-the-defaults). Full re-ingest of a 5MLOC codebase is expensive; substrate amortizes via the diff-able property — most re-ingestions are partial.
4. **Atomicity.** A re-ingestion produces a new version atomically; cycles either see the old or the new, never a half-state. Crash-mid-ingest reverts to the prior version.
5. **Diff-on-write.** Every re-ingestion produces the delta against the prior version; deltas are themselves trajectory-captured.
6. **Patrol-tier review.** Persistent freshness-SLO violations escalate to Patrol (per [D-6](../00-brief-v3.md#41-the-defaults)) — the third watchdog tier, hours-cadence, human-escalation.

This protocol is what makes ingestion *load-bearing on every cycle*. Without it, the "one-time bootstrap" critique would be correct.

---

## §3. Load-bearing failure modes this track addresses

Mapping selected F-modes to where the ingestion-first axis bites. **Honoring bias-guard findings:** F30 brownfield critical, F34 brownfield critical, F35 brownfield high (re-rated medium-high greenfield + stays high brownfield), F44 brownfield critical.

### 3.1 F-modes the ingestion artifact directly mitigates

- **[F34 — cross-layer drift](../failure-modes-v3.md#f34--cross-layer-drift) (brownfield critical):** Pace-layer pinning is the mitigation. The judge reads the artifact, identifies which pace layers the proposed change touches, and routes to layer-appropriate gates (a code-layer change runs the test gate; a pace-layer-4 change requires an architectural-spec amendment in the cycle, not after it).
- **[F44 — production-scissors default](../failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default) (brownfield critical):** The artifact's trifecta-aware section identifies production-write paths; substrate defaults these off. R3 (*"do not give it production scissors"*) becomes substrate-enforced not Claw-operator-discipline. Pairs with the [F12](../failure-modes-v3.md#f12--lethal-trifecta--prompt-injection) → [F33](../failure-modes-v3.md#f33--adversarial-prompt-defeat-of-llm-based-security-analysis) → F44 cascade explicitly.
- **[F56 — guardrail-bypass under stress (Replit-class)](../failure-modes-v3.md#f56--guardrail-bypass-under-stress-replit-class-incident) (brownfield critical):** Replit's DB wipe happened because the agent had production-write capability under explicit "do not proceed" instructions. Ingestion-derived substrate default-off makes the *capability* absent, not the *instruction* present. F56's lesson is that instruction-shaped guardrails are probabilistic; ingestion-derived deterministic perimeter is Ashby-adequate (per [F51](../failure-modes-v3.md#f51--ashby-deficient-probabilistic-guard)).
- **[F30 — liability vacuum](../failure-modes-v3.md#f30--liability-vacuum) (brownfield critical):** The ingestion artifact carries an explicit RSI / SB 53 / governance posture per [F43](../failure-modes-v3.md#f43--rsi-board-visibility-gap) framing — the Caremark / [report 31](../../../research/31-caremark-rsi-board-exposure.md) board-visibility primitive becomes a substrate output. Per [Kahana's three-part RSI test](../../../research/31-caremark-rsi-board-exposure.md), the artifact lets the board ask whether durable / compounding / limited-gating apply. Without ingestion, that question has no surface.
- **[F35 — federation-as-family drift](../failure-modes-v3.md#f35--federation-as-family-drift) (brownfield high):** Per [El Kaim Chapter 9](../../../research/24-el-kaim-book-product-line-variability.md), inherited federations claimed-aligned-with a family drift silently. Ingestion makes the family membership and derivation rules executable — the judge can refuse a change that violates derivation rules.
- **[F21 — context-window exhaustion](../failure-modes-v3.md#f21--context-window-exhaustion--silent-degradation) (brownfield critical):** The artifact lets the planner load *only the relevant slice*, defeating the "saturate the window with the whole codebase" failure mode. Per the brief's own line — "brownfield ingestion (codebase + history + traces) saturates context fastest" — the ingestion-first artifact is the planner's index *into* the codebase so the planner never tries to load the whole thing.
- **[F61 — context fragmentation across agents](../failure-modes-v3.md#f61--context-fragmentation-across-agents) (brownfield high):** Multi-agent swarms reading a shared ingestion artifact have a shared frame of reference; per-agent local decisions are anchored to a common index.

### 3.2 F-modes the re-ingestion protocol mitigates

- **[F8 — stale-knowledge inversion](../failure-modes-v3.md#f8--stale-knowledge-inversion):** Freshness SLO + re-ingestion triggers prevent the artifact from rotting. This is the direct substrate response to F8.
- **[F54 — goal subversion (RSI prompt-injection over cycles)](../failure-modes-v3.md#f54--goal-subversion-rsi-prompt-injection-over-cycles) (brownfield critical):** The artifact's diff-on-write captures the codebase-state delta per cycle. If a multi-cycle goal-drift attack tries to shift the goal-frame incrementally, the diff-trajectory makes the drift detectable post-hoc (Patrol-tier escalation).
- **[F55 — behavioural drift / self-reference loop](../failure-modes-v3.md#f55--behavioural-drift-self-reference-loop) (brownfield high):** Ingestion provides out-of-distribution ground truth from production telemetry and existing tests — the factory's outputs are continually anchored against codebase-derived signal, breaking the self-reference loop.
- **[F58 — runtime/design-time compliance split](../failure-modes-v3.md#f58--runtime-design-time-compliance-split) (brownfield high):** Re-ingestion triggers from observability deltas mean runtime-introduced behaviour gets caught in the next cycle's ingestion artifact; compliance-relevant changes surface before the next gate-pass.

### 3.3 F-modes this track does NOT claim to mitigate (and shouldn't pretend to)

- **[F1 / F27 / F46 / F48](../failure-modes-v3.md#f1--hallucination-loop) hallucination/circularity cluster:** Ingestion provides one out-of-distribution signal (the codebase), but the brief's [CTR-D7](../contradictions.md#ctr-d7--anthropic-single-judge-finding-vs-ctr-d4-cross-model-critic-framing-missed-1) registers an unresolved corpus split on whether judge-model-family-diversity is necessary. This track stays neutral on that question — ingestion is *one* signal but not the substitute for judge-diversity.
- **[F40 — last-mile drift](../failure-modes-v3.md#f40--last-mile-drift):** Ingestion doesn't help; this is a per-cycle / methodology problem (release / fit-and-finish bottleneck).
- **[F42 — cognitive-escrow negligence](../failure-modes-v3.md#f42--cognitive-escrow-negligence):** Harness-design concern, orthogonal to ingestion.
- **[F45 — language-as-harness mismatch](../failure-modes-v3.md#f45--language-as-harness-mismatch):** Brownfield gets the language it has; ingestion describes the harness mismatch but doesn't fix it.
- **[F52 — Tempting Wrong Hybrid](../failure-modes-v3.md#f52--tempting-wrong-hybrid-deterministic-wrapping-reflex):** The track must explicitly avoid this — the ingestion artifact must not become a sprawling deterministic wrapper around the LLM that pays for both paradigms while collecting neither. Mitigation: the artifact's *contents* are mechanically derived from code/tests/telemetry (not hand-curated rules); the substrate refuses to accrete operator-discipline workarounds.

### 3.4 F-modes this track creates or sharpens

- **F-NEW-ingestion-drift:** *"The ingestion artifact's pace-layer pinning, invariant catalog, or production-perimeter list silently drifts from the actual codebase state because a re-ingestion trigger was missed or the trigger-set was misconfigured."* Mitigation: the freshness vector + Patrol-tier escalation. This is a methodology-side risk the substrate must enforce against. The track surfaces this as a candidate F-mode rather than asserting it — Phase-3 lead-agent call whether to add to catalog.
- **F35 sharpening:** The ingestion artifact is itself a *family* (in the El Kaim sense): the schema, the derivation rules, the freshness protocol. Per [F35 severity rationale](../failure-modes-v3.md#f35--federation-as-family-drift) (raised to medium-high greenfield, high brownfield), the ingestion-artifact-as-family is itself subject to drift across factory instances. Phase-4 question: do all brownfield factory instances run the same ingestion schema, or does the schema specialize per-codebase?

---

## §4. §4 defaults — accepted vs challenged

Per [D3](../decisions-captured.md#d3--4-invariants-relaxed-to-defaults-with-per-track-acceptchallenge), each [§4 default](../00-brief-v3.md#41-the-defaults) is marked.

### D-1. Specs are the durable, version-controlled, human-curated artifact

**Accepted with justification (qualified).** The spec is durable; per this track, **the ingestion artifact is durable alongside it** — both are substrate-durable, both are version-controlled. The ingestion artifact is mechanically derived (not human-curated); the spec stays human-curated per [D-1](../00-brief-v3.md#41-the-defaults). Adds rather than substitutes: brownfield has *both* artifacts, with the ingestion artifact at pace-layer 1 (code-derived state) and the spec at pace-layer 3 (intent).

Per [CTR-B2 / CTR-B7](../contradictions.md#ctr-b7--brier-code-is-fashion--free-to-reproduce-vs-nystrom-spec-git-history-is-the-changelog-missed-6) — the spec-velocity disagreement (Brier slow / Nystrom changelog-fast) — this track stays neutral on spec velocity; the *ingestion artifact*'s velocity is code-pace (Brier-aligned for the artifact, not the spec).

### D-2. Scenarios live outside the codebase as a holdout set

**Challenged.** This is the brief-flagged fragile default and the brief's pre-respond target. Brownfield's ingestion artifact produces scenarios *from* the codebase:

- **Existing tests** are scenarios. Per [F28 (holdout leakage)](../failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders), the discipline is "withheld from builders," not "outside the codebase" — the substrate enforces holdout by selecting which tests the builder sees on each cycle, not by sourcing scenarios externally.
- **Production telemetry** is scenarios. Observed request/response traces, replay logs, observed envelopes are scenarios with stronger provenance than synthetic ones.
- **Incident replays** are scenarios. Per [report 01 (StrongDM "Tokens are the fuel")](../../../research/01-strongdm-factory.md), StrongDM's own primary pages list *"traces, screen capture, transcripts, incident replays, adversarial use, agentic simulation"* — many necessarily inside the running system. The D-2 default oversimplifies even its primary source ([sharpening WEAK-3 of CTR-B5](../contradictions.md#ctr-b5--scenarios-live-outside-the-codebase-round-1-d-2-vs-brownfield-scenarios-live-inside-fragile-default-flag)).

**The substrate-level invariant brownfield should adopt instead of D-2:** *holdout discipline is enforced at the substrate's scenario-selection layer, not at the scenario-storage location*. The ingestion artifact catalogs scenarios; the substrate's holdout layer decides per-cycle which scenarios the builder can see. This preserves [D-4 (holdout discipline)](../00-brief-v3.md#41-the-defaults) without requiring scenarios to live "outside the codebase."

Per [Anthropic (followup/07)](../../../research/followup/07-evals-deepdive.md), [Husain/Shankar](../../../research/followup/07-evals-deepdive.md) recommend *against* eval-first development for the same reason: writing evals against predicted (not observed) failures anchors them wrong. Ingestion-derived scenarios are observed-failure-anchored.

### D-3. Agent = Model + Harness

**Accepted with justification (qualified).** The vocabulary holds for the individual agent inside a cycle. The track does not propose a graph-node or population shape, so the brief's `flagged fragile` note doesn't bite. Per [CTR-C10 (MISSED-8 report 37 Portuguese-prompt effect)](../contradictions.md#ctr-c10--report-37-portuguese-vs-english-language-effect-on-policy-vs-routerllm-provider-agnosticism-missed-8), there's a corpus-flagged risk that "Agent = Model + Harness" is incomplete (missing natural-language-register as a harness parameter). This track records the risk and stays neutral.

### D-4. Holdout discipline is substrate-enforced, not methodology-optional

**Accepted with justification.** This is the discipline the D-2 challenge above preserves. The substrate's scenario-selection layer is the mechanism. The ingestion artifact catalogs scenarios; substrate decides what the builder sees.

### D-5. Hard cost ceilings are non-optional in CI

**Accepted with justification.** Re-ingestion is the highest-cost substrate operation in this track's design; the cost ceiling discipline applies to it. The diff-on-write amortization (§2.4) is the cost-control primitive. Per [CTR-E1 (Cherny $100K vs $500–$5K/day)](../contradictions.md#ctr-e1--token-spend-per-engineer--cherny-100kmonth-vs-independent-5005000day), no opinion on the ceiling level itself.

### D-6. Tiered watchdog (Daemon / Triage / Patrol) is a substrate primitive

**Accepted with justification (extended).** Daemon checks ingestion-process liveness. Triage detects ingestion stalls vs. legitimate long-running ingestions. **Patrol-tier explicitly extended to ingestion-freshness watchdog** — strategic drift detection across hours, escalating to human on persistent freshness violations or schema-drift across factory instances. The freshness vector (§2.2 property 5) is the Patrol input.

### D-7. Trajectory capture is cheap and production-tested

**Accepted with justification.** Trajectory captures *what the factory did*; the ingestion artifact captures *what the codebase is*. Both are substrate primitives. Trajectory references ingestion versions; cycle-replay reads both. Per [F14 widening](../failure-modes-v3.md#f14--attribution-collapse), forensic-reconstruction debt needs *both* — without the ingestion-version-at-time-of-action, the trajectory is uninterpretable.

**Summary:** 1 challenged (D-2), 6 accepted-with-justification. The D-2 challenge is the brief's expected one and is operationalized as a substrate-level holdout-discipline relocation, not as an abandonment of holdout discipline.

---

## §5. First-encounter with a new codebase (the brownfield analog of cold-start)

The brief makes [§5 cold-start mandatory for greenfield tracks](../00-brief-v3.md#5-greenfield-cold-start--mandatory-dedicated-synthesis-section-per-historian-m4m5). Brownfield doesn't have cold-start in the greenfield sense — by definition there's a codebase — but it has an analog: **first-encounter**, the factory's first cycle on a codebase it has never ingested. This section is worth writing because first-encounter is asymmetric in cost (most expensive ingestion the factory ever runs on this codebase), risk (no prior trajectory data; no prior ingestion to diff against), and informational value (everything observed is novel).

### 5.1 What's available on first-encounter

- The codebase itself (full).
- The repository's git history (commits, PR descriptions, merge messages).
- The existing test suite (passing tests are observed-true scenarios; failing tests are observed-but-tolerated states).
- The CI configuration (the codebase's own build/deploy reality, machine-readable).
- The repository's existing scaffolding (`AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md` per Brier, `README`, `docs/`).
- Production telemetry — *if accessible*. Often gated; first-encounter may have no telemetry signal.
- The dependency graph (lockfiles + package metadata).
- Issue tracker / PR comments (often noisy; lower-quality signal than the above).

### 5.2 What the first-encounter ingestion produces

The first-encounter cycle is *only* an ingestion run — it produces the v1 artifact but does not yet attempt a code-change cycle. This is deliberate: per [F59 (premature decomposition)](../failure-modes-v3.md#f59--premature-decomposition-scout-spec-build-separation-hazard), committing to a work decomposition before discovery is risky. First-encounter discovers the codebase's pace layers, invariants, and conventions before any cycle commits to changing them.

Outputs:

1. **The v1 ingestion artifact** with full pace-layer pinning, invariant catalog (derived from tests + git-blame-on-architecture-files heuristic), perimeter catalog (production-write paths, secrets, external data), convention extraction (naming, error-handling, test patterns).
2. **A first-encounter report** for human review: highest-confidence findings, lowest-confidence findings, paths the ingestion could not classify (escalation candidates), suspected RSI / governance posture (per [F43](../failure-modes-v3.md#f43--rsi-board-visibility-gap)), suspected last-mile bottlenecks (per [F40](../failure-modes-v3.md#f40--last-mile-drift)).
3. **A confidence envelope.** Per [followup 11 `kw:confidence`](../../../research/followup/11-compound-knowledge.md), every claim in the artifact carries a confidence score; the first-encounter envelope is the aggregate distribution. Low aggregate confidence → first cycle runs in heavy-augmentation mode (human review per work unit) regardless of stated lights-out target.
4. **A re-ingestion-trigger seed set** — the substrate's initial guess at what events should trigger re-ingestion in this codebase. Refined cycle-over-cycle.

### 5.3 Why first-encounter is not bootstrap

First-encounter produces *the first version* of the artifact, but the cycle-2-and-after ingestion-refresh protocol (§2.4) is the same substrate process. There is no "first-encounter mode vs steady-state mode" distinction at the substrate; it's all *re-ingestion*, where first-encounter happens to have nothing to diff against. The "ingestion is bootstrap" critique's mistake is treating first-encounter as architecturally distinct from cycle-N ingestion. It isn't; it's just the expensive end of the same distribution.

### 5.4 Per Historian M5 required-reading anchor

The brief names [reports 25, 26, 30, 31 + followup 10](../00-brief-v3.md#51-required-inputs-to-the-cold-start-treatment-per-historian-m5) as cold-start required reading. For first-encounter, the brownfield analog reading is asymmetric:

- **[Report 25 (RE foundations)](../../../research/25-requirements-engineering-foundations.md), [Report 26 (prompt underspecification)](../../../research/26-prompt-underspecification-academic.md)** — both re-tagged `greenfield-primary`. Useful for first-encounter as *vocabulary* (GtWR, EARS, Yang et al.'s instruction-following ceiling, Larbi et al.'s contradictory-prompt-collapse). Brownfield first-encounter doesn't bootstrap a spec from nothing — but the ingestion artifact's human-readable surface uses GtWR discipline to defeat hedge-language drift (§2.2 property 3).
- **[Report 30 (cognitive escrow)](../../../research/30-cognitive-escrow.md), [Report 31 (Caremark RSI)](../../../research/31-caremark-rsi-board-exposure.md), [Followup 10 (governance)](../../../research/followup/10-governance.md)** — `both-primary`. Load-bearing for first-encounter: the first-encounter report (§5.2 output 2) is the substrate's primary surface for governance posture declaration. Per [F43 (RSI board-visibility gap)](../failure-modes-v3.md#f43--rsi-board-visibility-gap), this is the artifact the board reads to decide whether Caremark / SB 53 / SEC IAC reporting obligations attach. Brownfield first-encounter is the latest opportunity to declare this before per-cycle work begins.

---

## §6. Lights-out / L5 / regime treatment (mandatory per OQ-B1)

Per [brief §2.1](../00-brief-v3.md#21-the-lights-out--l5--regime-tension-load-bearing-must-be-addressed) and [OQ-B1](../00-brief-v3.md#8-open-questions-surfaced-by-this-brief-deliberate), every Phase-2 track must treat this. First, the vocabulary mapping test:

### 6.1 Vocabulary mapping test

UC1 "lights-out" and Jaymin's "L5" are **not equivalent for brownfield-with-ingestion-substrate**.

- **L5** (Shapiro, [report 32](../../../research/32-shapiro-completion-chat-agent-claw.md) / [followup 01](../../../research/followup/01-shapiro-five-levels.md)): *"a black box that turns specs into software… humans are neither needed nor welcome."*
- **Lights-out** ([UC1](../constraints-extracted.md#uc1--the-artifact-being-built) per glossary §0): *no human in per-cycle inner loop for automation-eligible work; humans set policy, sample-audit, intervene on watchdog escalation, re-enter on declared trigger conditions.*

The ingestion-first architecture has **explicit re-entry triggers** built into the re-ingestion protocol (§2.4 — Patrol-tier escalation on persistent freshness-SLO violations, on first-encounter report low-confidence findings, on schema drift across instances). These are *exactly* the "watchdog escalation" and "declared trigger conditions" in the lights-out definition. They are **not L5**.

**Conclusion:** lights-out ≠ L5 for this track. CTR-A1 (L5-as-target vs L5-as-anti-pattern) is mostly dissolved for this track — the architecture does not target L5 in Shapiro's sense.

### 6.2 Operating mode (brief §2.1 option c + b)

The track adopts the lead-agent working-stance shape (option c + b) from [brief §2.1](../00-brief-v3.md#21-the-lights-out--l5--regime-tension-load-bearing-must-be-addressed):

- **Option c (regime classification):** Cycle classifies work units against the ingestion artifact. Work units the artifact identifies as touching production-write paths, pace-layer 4–5 elements, or low-confidence regions route to L4-augmented (human review per work unit). Work units in well-understood, well-tested, pace-layer-1-only regions route to L4-lights-out.
- **Option b (lights-out over a defined work-unit-class surface):** The classification is *substrate-enforced* via the ingestion artifact, not methodology-optional. The artifact's perimeter catalog and confidence envelope determine eligibility.

### 6.3 Jaymin-bar position (OQ-B6)

This track does not commit to Jaymin's specific thresholds (K=5 ≥90%, paraphrase 5-of-5, zero medium-or-high safety incidents). [Sharpening WEAK-1 of CTR-A1](../contradictions.md#ctr-a1--l5-as-target-vs-l5-as-anti-pattern) — Jaymin's Ch 9 §7 is itself two-sided (L5 anti-pattern *and* "this time it works") — makes Jaymin's threshold framework unstable as a standalone bar source.

**Track position:** the empirical bar for brownfield-with-ingestion-substrate is *ingestion-derived*. The codebase's existing test suite + production telemetry envelope IS the empirical bar. A cycle's output is automation-eligible if (a) all ingestion-derived gates pass and (b) the runtime envelope post-change matches the pre-change envelope within a substrate-declared tolerance. Defers OQ-B6 to Phase-3 lead-agent triage; offers ingestion-derived bars as one candidate alongside Jaymin's.

---

## §7. Mandate-fit assertion (per D2)

The brownfield-legacy-ingestion-first architecture is **brownfield-only** by design (axis is brownfield-mandate-specific). Per-(work-unit-class) mandate-fit, using the [brief's 5-class illustrative taxonomy](../00-brief-v3.md#6-required-outputs-from-v3-per-d2-schema) — explicitly subject to Phase-2/3/4 revision:

```yaml
mandate-fit:
  initial-spec: n/a                  # greenfield-shaped (cold-start regime)
  refactor: brownfield-fit           # strongest fit; ingestion artifact is exactly what refactor needs
  mvp: n/a                           # greenfield-shaped
  post-mvp-evolution: brownfield-fit # second-strongest fit; pace-layer pinning + invariant catalog directly used
  regression-fix: brownfield-fit     # strong fit; ingestion identifies the regression's blast radius
```

The track makes no claim about greenfield work-unit-classes — those are out of scope for this axis. A both-mandates architecture might extract substrate primitives from this track for use in a unified design (Phase 3/4 question), but the track itself is mandate-specific.

---

## §8. Open questions surfaced by this track

- **Q1.** What is the ingestion artifact's *schema*? (Phase-4 / Phase-5 ADR work. This track deliberately under-specifies contents.)
- **Q2.** Is the schema universal across brownfield factory instances, or codebase-specialized? (Per [F35 sharpening](#34-f-modes-this-track-creates-or-sharpens), the artifact-as-family is itself subject to drift.)
- **Q3.** How does the substrate enforce the re-ingestion trigger set without it becoming the [F52 "Tempting Wrong Hybrid"](../failure-modes-v3.md#f52--tempting-wrong-hybrid-deterministic-wrapping-reflex) — a sprawling deterministic wrapper around the LLM? (Mitigation: triggers are mechanically derived from observability + git events, not hand-curated rules.)
- **Q4.** What is the freshness SLO? (Substrate-policy question; depends on codebase change rate. Default starting point: 7 days for base SLO; immediate for trigger-driven.)
- **Q5.** Is the ingestion artifact's confidence envelope a Phase-4 substrate primitive or a methodology-side concern? (This track puts it at substrate; the methodology-first brownfield track may disagree.)
- **Q6.** How does the architecture handle codebases the ingestion artifact *cannot* fully describe — large monorepos, polyrepo federations, legacy binary blobs, generated code? (First-encounter report flags these as escalation candidates; per-codebase Patrol-tier human review required. Open whether substrate provides a fallback.)
- **Q7.** What is the relationship between the ingestion artifact and the spec? Per [CTR-B7](../contradictions.md#ctr-b7--brier-code-is-fashion--free-to-reproduce-vs-nystrom-spec-git-history-is-the-changelog-missed-6), the corpus is split on spec velocity. The artifact is code-pace; the spec sits above. The contract between them — how spec changes trigger ingestion re-reads, and vice versa — is unspecified here.
- **Q8 (biggest open question).** Does the ingestion artifact generalize to *greenfield with priors* (adjacent domains, exemplar projects, library docs as the "codebase to ingest")? If yes, the legacy-ingestion-first axis collapses into a both-mandates substrate primitive — *priors-ingestion-first*. If no, ingestion is brownfield-specific and Phase 4 splits substrate accordingly. The track leans "yes but with material shape differences" — but defers the call to the no-axis-prescribed tracks per [D1](../decisions-captured.md#d1--phase-2-fanout-9-parallel-tracks-3--3--3).

---

## Closing discipline note

This track is *one* output of nine. It is deliberately strong on its axis and does not attempt to be comprehensive. The substrate-first brownfield track will likely propose a different organizing primitive (the sandbox, the watchdog, or the trajectory store as the substrate organizing element); the methodology-first brownfield track will likely propose the cycle process (Atelier-style queue, Refinery-style change-request, or codebase-evolution-proposal per [OQ-B4](../00-brief-v3.md#8-open-questions-surfaced-by-this-brief-deliberate)) as the organizing element. Phase 3 merges these.

The track honors the Brier counter-metaphor (followup 12) seriously rather than dismissing it: the pace-layer framework is the strongest argument that brownfield architecture is already layered, and this track operationalizes that layering as a substrate-level artifact. Where Brier rejects the factory metaphor outright, the track concedes the disagreement and proposes ingestion as the bridge — the factory needs the company's institutional memory to operate lights-out, and the ingestion artifact is that memory encoded.

*End of brownfield-legacy-ingestion-first.md.*
