---
track: unified-no-axis-A
axis: escrow-interval-as-substrate
mandate-scope: unified
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
based-on-date: 2026-05-24
---

# Unified-A — Escrow-Interval-as-Substrate

A single architecture for both greenfield and brownfield, organised around the **escrow interval** — the named interval (Kahana, [report 30](../../../research/30-cognitive-escrow.md)) between when an instruction leaves human possession and when its consequences return. The interval is treated as a first-class, *substrate-level* primitive: every cycle is a journey through one or more escrow intervals; the substrate enforces *what happens in each interval* (gates, attestations, reflection prompts, cross-model judges, immutable logging); the methodology layer above chooses *which intervals exist*. Lights-out lives in the *inner* per-cycle intervals; humans live at *boundary* intervals where the substrate has structurally invited them in.

---

## §0 Axis declaration and defense

**Chosen axis:** the architecture is organised around the **escrow interval** as the substrate's load-bearing primitive. Concretely: every transition where a human (or earlier-cycle artifact) hands off intent to a machine *and where the machine's action is not yet observable* is a named, typed `EscrowInterval` object; the substrate enforces gate, log, reflection, and judge behaviour *inside* that object; the architecture (whether greenfield or brownfield) is the *graph of escrow intervals* and the policies on each node.

**Why this axis, and why for unified.** Five reasons, pre-responding to Phase-3 adversarial:

1. **It dissolves the lights-out/L5 tension without redefining lights-out.** Kahana names the interval; he does not abolish it. Lights-out (per brief §0) means *no human in the per-cycle inner loop for automation-eligible work units*; an interval-as-substrate frame says *the substrate, not the operator, occupies the interval* — gates, judges, immutable logs, AILCCP controls all live inside the interval ([report 31 §5](../../../research/31-caremark-rsi-board-exposure.md)). Re-entry intervals (OQ-B3) are *also* `EscrowInterval` instances; they differ only in the policy on the node. This is consistent with brief §2.1 option (c)+(b) (regime classification + bounded operating mode).

2. **It is corpus-grounded as both phenomenon and design site.** Report 30 names the interval; F42 catalogs the failure mode; the AILCCP framework supplies the control surface (followup/10 §A/§B/§C). Schillace's Attention Firewall (report 28 §6), Codex `.rules` DSL + OTEL stack (report 18 §4.3–§4.4), Anthropic's Auto-Review subagent ([report 23 §3.5](../../../research/23-anthropic-engineering-trilogy.md)) and CJ Hess's `kevin`/`carl` (report 34 §6.2) all *already* operate inside the interval — the corpus has been groping toward the abstraction the axis names.

3. **It is mandate-symmetric in a way that artifact-axis (spec/code) and lifecycle-axis (cold-start/legacy-ingestion) are not.** Both mandates produce escrow intervals; what changes is *which intervals* and *what their policies say*. Greenfield's cold-start is `EscrowInterval{kind: bootstrap, priors: out-of-tree}` (brief §5); brownfield's RSI cycle is `EscrowInterval{kind: refactor, priors: in-tree codebase + traces}` (report 31 §1). The substrate is the same; the graph differs.

4. **It addresses Kahana's "discipline fragility" finding (F53) at substrate level.** Voluntary-cognitive-discipline patterns (STIR, Willison three-tier review, BCG intent-thinking, EARS/GtWR cadence) are corpus-canonical *and* corpus-flagged as fragile because they assume operator-budget-at-the-moment ([report 30 §3](../../../research/30-cognitive-escrow.md)). Organising the architecture around intervals where the substrate fires the discipline structurally (not voluntarily) is the only mitigation that survives Kahana's critique. Other axes (spec-driven, queue-of-issues, pace-layers, substrate-vs-methodology) leave discipline at the methodology layer and inherit F53.

5. **It pre-responds to the Brier "factory is the wrong metaphor" attack ([followup/12](../../../research/followup/12-brier-pace-layers.md), CTR-F1).** Brier's complaint is that Ford-style variance-elimination misframes software production. The escrow-interval frame is neither a factory nor a company metaphor — it is a *process-control* frame: variability is permitted *inside* the interval; the interval's boundary is what is enforced. Brier's five-layer pace-stack collapses naturally into a graph of intervals annotated by pace-layer (a fast-layer code interval has different gates than a slow-layer architecture interval), without committing to either Ford or Warhol vocabulary.

**Anticipated Phase-3 adversarial attacks and pre-responses:**

- *"This is just Cognitive Escrow rebranded as architecture."* No: Kahana names a phenomenology; this track promotes it to a substrate-typed object with mandatory primitives (gate / log / judge / reflection-trigger / pace-layer tag) that every architecture in v3 either has or lacks. The novelty is *making the interval a typed object*, not naming it.
- *"You're smuggling the substrate-vs-methodology boundary (OQ-B2) by putting everything in the substrate."* Acknowledged. The position is *the interval object itself is substrate; the graph of intervals is methodology*. That answers OQ-B2 unambiguously: substrate carries the typed primitive; methodology composes graphs of primitives. Other tracks may take other positions.
- *"This is greenfield-flavoured because cold-start fits the bootstrap-interval framing too cleanly."* Counter: the brownfield F-mode set (F12 critical, F20 critical, F30 critical, F33 critical, F44 critical, F56 critical, F58 high) maps point-for-point onto interval-policy choices (sandboxing, Human Approval Gate, immutable logging — AILCCP three controls per [report 31 §5](../../../research/31-caremark-rsi-board-exposure.md)). The brownfield mandate's defining constraints land *in* the interval, not outside it.
- *"You've made the escrow interval do too much work."* Acknowledged risk; surfaced in §7 as the load-bearing open question (interval-granularity). The axis claim is only that the interval is *one* load-bearing primitive, not the only one.

---

## §1 Architecture sketch

**Name:** Escrow-Graph Factory.

**Unit of work:** a *cycle* is a directed graph of `EscrowInterval` nodes, from initial intent through to artifact-and-receipt. Each node carries:

```yaml
EscrowInterval:
  id: stable-uuid
  kind: bootstrap | refactor | regression-fix | spec-author | review | merge | deploy | dream | re-entry | ...
  pace-layer: code | plans | specs | architecture | standards   # Brier, followup/12
  priors:
    out-of-tree: [scenarios, exemplars, adjacent-domains, operator-knowledge]
    in-tree: [codebase, tests, runtime-telemetry, prior-cycle-artifacts]   # may be empty (greenfield bootstrap)
  policies:
    gate: deterministic | LLM-judge | cross-model-judge | none
    log: append-only | OTEL-export | none      # AILCCP immutable-logging when high stakes
    sandbox: container | bwrap+seccomp | none  # AILCCP sandboxing
    approval-gate: required | sample | none    # AILCCP Human-Approval-Gate
    reflection-trigger: STIR | success-criterion | similar-prior-prompt | delegation-confirm | none
    judge-diversity: same-model | different-role | different-family   # CTR-D4/D7/D8 cleavage
  classifier:
    work-unit-class: initial-spec | refactor | mvp | post-mvp-evolution | regression-fix
    automation-eligibility: lights-out | sample-audit | escalate | human-required
  artefacts:
    inputs: [content-addressed handles]
    outputs: [content-addressed handles]
    trajectory: pointer to OpenHands-style sub-ms event log    # D-7 default
```

**Five substrate primitives, all interval-anchored:**

1. **Interval object store.** Content-addressed, append-only; every interval is a durable record. Trajectory capture (D-7) is the inside-the-interval event stream; the interval object is its envelope.
2. **Policy mediator.** Reads `policies` from the interval, fires the gates and judges in order, refuses to close the interval unless all enforced policies passed. *Substrate, not methodology.*
3. **Classifier.** Decides `automation-eligibility` and `work-unit-class` (D2 schema) for each interval at *open* time, on the basis of pace-layer + priors + kind. The classifier itself is interval-bracketed (its decision is logged, audit-able, and overrideable at a re-entry interval).
4. **Judge router.** Routes to same-model / different-role / different-family judge per policy. Default: cross-model judge for stakes ≥ "modifies state outside sandbox" (F46, [report 34 §6.2](../../../research/34-lenny-howiai-personal-harnesses.md)); same-model-different-role permissible elsewhere ([report 23 §3.5](../../../research/23-anthropic-engineering-trilogy.md), CTR-D4/D7).
5. **Re-entry registrar.** Holds the protocol for human re-entry per OQ-B3: which conditions promote a `sample-audit` interval to `escalate`; who decides; what the substrate-level handoff looks like. Substrate exposes the registrar; the architecture supplies the policies; the registrar fires deterministically.

**Methodology layer (kept thin per CTR-C2):** the methodology supplies *graphs* of intervals — declarative DAGs whose nodes are interval-kinds and whose edges are content-handle dependencies. A "Compound Atelier" methodology is one graph shape; an "Attractor `.dot` pipeline" ([report 27](../../../research/27-dotfile-pipelines-as-product.md)) is another; a "Tournament" methodology is a graph with a `select` interval at the end. The *substrate* doesn't know which methodology it's running.

**How the same architecture serves both mandates.**
- **Greenfield day-0** runs a single `kind: bootstrap` interval with `priors.in-tree: []` and `priors.out-of-tree: [adjacent-domains, exemplars, operator-curated]`. The bootstrap interval's policies are the *strictest* (cross-model judge mandatory; human-approval-gate sample-rate 100%; reflection-trigger STIR cascade), reflecting the F1/F15/F27/F36/F37/F41/F55 critical-severity stack on greenfield specs.
- **Brownfield ingestion** runs an `kind: archaeology` interval with `priors.in-tree: [codebase, history, traces, tests]` and `priors.out-of-tree: []`. The archaeology interval feeds a populated `change-request` interval graph; subsequent intervals reuse in-tree priors and *invert* D-2 (scenarios from codebase, per CTR-B5).
- **Steady-state** for both is the same: a graph of intervals, with the classifier promoting routine work to `lights-out` and rare/high-stakes work to `escalate`. F57 (design-authority erosion) is mitigated structurally because the classifier itself runs inside an interval and is audited.

**What this is not.** It is not a Ford-style production line (variability *is* permitted within each interval); not an Attractor-style DOT pipeline (intervals are typed objects, not graph nodes in a single global graph); not a Compound Atelier (no queue-as-primary; the queue is one possible methodology graph). It absorbs primitives from each — the durable-artifact discipline of Refinery, the knowledge-accumulation of Compound, the parallelism of Atelier, the pipeline-as-spec idea of Attractor — but reduces them to *graph-construction choices on a shared interval substrate*.

---

## §2 How this addresses each load-bearing concern

### Lights-out / L5 tension (brief §2.1, OQ-B1)

The architecture takes option (c) + (b) from brief §2.1: **regime is per-interval**, not per-architecture. The classifier assigns `automation-eligibility` per interval at open time; lights-out applies to intervals classified `lights-out`. The vocabulary-mapping test (CTR-A4) is *also* per-interval: each interval declares what regime it operates under, eliminating the global lights-out↔L5 collision. Jaymin's empirical bars ([report 09 §2c](../../../research/09-jaymin-book-harnesses-practices-mental-models.md), CTR-A1) become per-interval-class thresholds: a `bootstrap` interval may require Automation-Mode-equivalent thresholds (5-of-5 paraphrase robustness, ≥90% K=5) before promotion to `lights-out`; a `regression-fix` interval may run at Augmentation-Mode bars. **The mandate (UC1) is preserved**: the factory runs lights-out for the intervals classified that way; the corpus' L5-anti-pattern findings are honoured by *not* classifying greenfield-bootstrap or brownfield-deploy intervals as `lights-out` at day 0 ([report 09 §7](../../../research/09-jaymin-book-harnesses-practices-mental-models.md), CTR-A1, CTR-A5).

### UC4 working hypothesis (spec-malleable vs. code-archaeological)

UC4 is *falsified for this architecture's domain* in the precise sense brief §3 names: a single architecture works for both, because mandate-difference shows up as *graph-shape and per-node policy*, not as substrate. Greenfield's spec-malleability is `EscrowInterval{kind: spec-author, pace-layer: specs}` runs that are revisable (the *graph* has back-edges; the substrate permits supersession); brownfield's existing-architecture-as-given is `pace-layer: architecture | standards` intervals with frozen-by-default policies (Brier's slow layers, followup/12 §4). El Kaim's 9-field intent block (CTR-B6) is a *specific policy* for `kind: spec-author` intervals — a Phase-5 ADR knob, not a substrate commitment. The architecture does not have to take a side on Brier-vs-Nystrom spec velocity (CTR-B7): each interval declares its own velocity.

### Cold-start (mandatory; full treatment in §5)

The cold-start problem is the bootstrap interval (singular). It is the architecture's *day-0* shape; §5 dedicates the full treatment.

### OQ-B2 (greenfield/brownfield boundary)

**Resolution stance:** the boundary falls at the *methodology layer* (graph shape and per-node policy), not the substrate. Substrate primitives (interval object store, policy mediator, classifier, judge router, re-entry registrar) are shared.

### OQ-B3 (human re-entry mechanism)

**Resolution stance:** re-entry is a typed `EscrowInterval{kind: re-entry}` node; the re-entry registrar substrate primitive holds the protocol. Conditions (watchdog escalation per C14 Daemon/Triage/Patrol tiers; cost-ceiling breach per D-5; severity-class trigger per Jaymin's safety-incident taxonomy); decider (substrate-default operator-of-record; methodology may override); handoff (substrate freezes the in-flight interval graph, emits a re-entry summary derived from the trajectory + AILCCP immutable log, awaits explicit close).

### OQ-B4 (brownfield unit-of-work)

**Resolution stance:** *all three* (issue / change-request / codebase-evolution-proposal) are valid graph-shapes over the shared interval substrate. The architecture does not pick; the methodology layer does. Compound-Atelier-flavoured graphs have `kind: issue-intake` as their entry interval; Refinery-flavoured graphs have `kind: spec-delta` entry intervals; codebase-evolution-proposal graphs have `kind: archaeology + proposal` entry pair.

### OQ-B6 (empirical bars)

**Resolution stance:** per-interval-class threshold matrix (not a global bar). Jaymin's K=5/paraphrase/safety-severity bars are *one* candidate set ([report 09 §5.5](../../../research/09-jaymin-book-harnesses-practices-mental-models.md)); SWE-bench Verified ([report 22](../../../research/22-academic-foundations.md), brownfield-primary) supplies another for refactor/regression-fix intervals; AttractorBench (report 27) supplies a third for pipeline-conformance intervals. The substrate enforces "an interval cannot be classified `lights-out` until its kind has cleared a declared bar"; the bar source is a Phase-5 ADR per interval-kind.

### OQ-B8 (provider-property requirements)

**Resolution stance:** the judge router is the abstraction; provider-property requirements (diversity, long-context, vision, tool-calling-latency) are declared at the *policy* layer of the interval, not globally. RouterLLM-style abstraction (CTR-C4) is permitted for *intra-family* routing (latency/cost optimisation); cross-family routing (the F46 mitigation) is mandatory at high-stakes intervals and is explicitly *not* unified with intra-family routing — answering Attractor's "do not unify" objection ([report 02](../../../research/02-strongdm-attractor.md), CTR-C4).

### OQ-B9 (methodology evolution)

**Resolution stance:** methodology evolution is a graph-shape change, captured as a `kind: methodology-delta` interval. Whether *that* interval runs at `lights-out` or `human-required` is itself the question — substrate does not pre-decide. F35 (federation-as-family drift) and F55 (behavioural drift / self-reference loop) are mitigated by requiring methodology-delta intervals to have `judge-diversity: different-family` by default.

### F-mode coverage (illustrative; not comprehensive)

- F1 / F27 / F46 / F48 (correlated-error / collusion cascade): judge router with `judge-diversity` policy is the primitive control surface; cross-family by default for stakes-bearing intervals.
- F12 / F33 / F44 (lethal-trifecta cascade): sandbox and approval-gate policies on every interval that touches production state; substrate-default-off per F44.
- F36 / F37 / F39 (instruction-following ceiling / silent-contradictory-prompt / point-spec-region-mismatch): the `kind: spec-author` interval policy mandates EARS/GtWR lint (deterministic) + cross-model contradiction-detection judge ([report 26](../../../research/26-prompt-underspecification-academic.md)) + complexity-diagnosis field at open.
- F42 (cognitive-escrow negligence): foundational; the architecture's *axis* is the mitigation.
- F43 (RSI board-visibility gap): AILCCP three-controls coverage is per-interval-policy and aggregated to a board-quarterly report by the substrate's policy mediator ([report 31 §7](../../../research/31-caremark-rsi-board-exposure.md)).
- F53 (voluntary-discipline fragility): substrate-fired reflection-triggers (STIR cascade, success-criterion articulation per [report 30 §4](../../../research/30-cognitive-escrow.md)) at the interval boundary — discipline is structural, not voluntary.
- F54 (goal subversion / RSI prompt-injection over cycles): immutable logging policy plus methodology-delta intervals having `judge-diversity: different-family`.
- F56 (Replit-class guardrail-bypass under stress): deterministic policy mediator refuses interval close; LLM-shaped guardrails do not run alone in a `production-deploy` interval.
- F57 (design-authority erosion / convenience reclassifies stakes): classifier decisions are themselves intervals; the audit trail of classifier drift is structurally available.
- F59 (premature decomposition): graph back-edges permitted; substrate does not enforce graph-shape frozen-at-bootstrap.

---

## §3 Citations and grounding

| Load-bearing claim | Primary citation |
|---|---|
| Escrow interval is a named phenomenological state with no current governance vocabulary | [Report 30 §1](../../../research/30-cognitive-escrow.md) (Kahana, *Cognitive Escrow*, Stanford CodeX 2026-03-07) |
| Voluntary-discipline patterns (STIR, Willison three-tier, EARS/GtWR, intent-thinking) are fragile | [Report 30 §3](../../../research/30-cognitive-escrow.md); F53 in [failure-modes-v3.md §5a](../failure-modes-v3.md) |
| RSI three-part test (durable + compounding + limited-gating) reaches the corpus' subject matter | [Report 31 §1](../../../research/31-caremark-rsi-board-exposure.md) (Kahana, *Ungovernable Machine* 2026-03-17) |
| Three AILCCP controls (Human Approval Gate / sandboxing / immutable logging) map to interval-policy slots | [Report 31 §5](../../../research/31-caremark-rsi-board-exposure.md); followup/10 §A/§B/§C |
| Lights-out is per-cycle-inner-loop, compatible with policy/audit/re-entry | [Brief §0 glossary](../00-brief-v3.md), UC1 |
| L5 as 2026 empirical anti-pattern (CodeRabbit 1.4× / Veracode 45% / METR 19%) | [Report 09 §2c / §7](../../../research/09-jaymin-book-harnesses-practices-mental-models.md); CTR-A1 |
| Jaymin's Augmentation/Automation threshold matrix (K=5, paraphrase, safety-severity) | [Report 09 §5.5](../../../research/09-jaymin-book-harnesses-practices-mental-models.md); OQ-B6 |
| Shapiro self-positions at L4 ("I'm here"); L5 is *other* people | [Followup 01](../../../research/followup/01-shapiro-five-levels.md); CTR-A2 |
| Brier counter-metaphor: software *company*, not factory; pace-layers stack | [Followup 12](../../../research/followup/12-brier-pace-layers.md); CTR-F1, CTR-B3, CTR-B7 |
| Substrate-heavy + thin-methodology is the Round-2 thesis to test | Round-2 §8; CTR-C2 |
| Trajectory capture is cheap (sub-ms persist, 7.4ms recovery, 433 SWE-Bench replays) | [Report 11 §6](../../../research/11-openhands-substrate-audit.md); D-7 default |
| Codex `.rules` Starlark DSL + OTEL five-event-category export = partial substrate of interval policies | [Report 18 §4.3–§4.4](../../../research/18-openai-codex-substrate.md) |
| Anthropic Auto-Review subagent = same-model-different-role judge primitive | [Report 23 §3.5](../../../research/23-anthropic-engineering-trilogy.md); CTR-D4/D7 |
| Cross-model judge (`kevin`/`carl`) catches same-model self-review blindspot | [Report 34 §6.2](../../../research/34-lenny-howiai-personal-harnesses.md); F46 |
| Attractor: do-not-unify provider profiles; per-family agents | [Report 02](../../../research/02-strongdm-attractor.md); CTR-C4 |
| RouterLLM is one substrate-routing abstraction (cited as measurement only, not normative) | [Report 11 §6](../../../research/11-openhands-substrate-audit.md); brief §0 |
| Schillace Attention Firewall = first concrete interval-as-design-site exemplar | [Report 28 §6](../../../research/28-schillace-sunday-letters.md) |
| Yang et al. instruction-following ceiling 98.7→85.0% over 1→19 reqs; Larbi 73.8→6.7% on contradictory prompts | [Report 26 §3.4, §6.1–6.2](../../../research/26-prompt-underspecification-academic.md); F36, F37 |
| INCOSE GtWR / EARS / Complexity Primer principle-12 (point-spec/region-mismatch) | [Report 25](../../../research/25-requirements-engineering-foundations.md); F38, F39 |
| Caremark spine (Marchand mission-critical / Boeing / Hughes / McDonald's officer-Caremark / SolarWinds framing rule) | [Report 31 §2](../../../research/31-caremark-rsi-board-exposure.md); [followup 10 §3](../../../research/followup/10-governance.md) |
| Replit prod-DB wipe under explicit code freeze (1,200 execs / 1,190 cos) | [Followup 10 §3 (G14)](../../../research/followup/10-governance.md); F56 |
| Greenfield = "no pre-existing implementation," priors permitted | Brief §0 (Skeptic finding #6 revision) |
| Cold-start required reading per Historian M5 | Brief §5.1 (reports 25, 26, 30, 31; followup 10) |

---

## §4 §4 defaults: accepted vs challenged

| # | Default | Stance | Justification |
|---|---|---|---|
| D-1 | Specs are the durable, version-controlled, human-curated artifact | **accepted with justification** | Specs *are* durable artifacts in this architecture, but they are *one of many* interval-output content-handles. Spec-author intervals produce specs; refactor intervals do not. The default holds as long as "spec" is read per-interval, not globally. Anchored in [00-synthesis §2.1](../../../archive/synthesis-v1-v2/00-synthesis.md); D-1 in brief §4.1. |
| D-2 | Scenarios live outside the codebase as a holdout set | **challenged** | The interval substrate is mandate-symmetric on this point: greenfield-bootstrap intervals have `priors.out-of-tree: [scenarios, exemplars]`; brownfield-archaeology intervals have `priors.in-tree: [tests, traces]` and the methodology layer is *expected* to invert D-2 (CTR-B5, CTR-G2). Substrate enforces holdout-vs-builder *separation* (D-4) regardless of which side of the tree scenarios live on. Per [report 01 §1](../../../research/01-strongdm-factory.md) (StrongDM "Tokens are the fuel" already includes in-runtime sources per WEAK-3 sharpening). |
| D-3 | Agent = Model + Harness | **challenged** | The interval substrate doesn't require this decomposition. A graph-node agent (Attractor-style, CTR-F3) or a population (Tournament-style) is encoded as *interval-kind* + policy, not as a Model+Harness decomposition. Round-2 §2.2 already retired the persona-vs-graph-node disagreement at the methodology layer. Additionally CTR-C10 ([report 37 §5](../../../research/37-academic-llm-agent-collusion.md)) suggests "Agent = Model + Harness + Natural-Language-Register" — the interval substrate's `policies` slot is the natural home for the third term. |
| D-4 | Holdout discipline is substrate-enforced, not methodology-optional | **accepted with justification** | This architecture is uncompromising on this point: the substrate's policy mediator refuses to close a `kind: judge` interval if acceptance-criteria handles leaked into the upstream builder interval's inputs. F28 mitigation. Anchored in Round-2 C13. |
| D-5 | Hard cost ceilings are non-optional in CI | **accepted with justification** | Cost-ceiling breach is a substrate-fired re-entry trigger (per the re-entry registrar). The default is preserved; the addition is *where the breach fires the gate* (at the interval boundary, not at the workflow boundary). CTR-E1 ($100K vs $500-5000/day) is the open question; substrate enforces *whatever ceiling the operator declared*, not a corpus-derived number. |
| D-6 | Tiered watchdog (Daemon / Triage / Patrol) is a substrate primitive | **accepted with justification** | The three watchdog tiers map directly onto interval-policy enforcement: Daemon = liveness check on the in-flight interval (heartbeat / resource); Triage = AI reclassification of `lights-out` → `escalate` per F22/F23; Patrol = strategic drift detection across interval histories, feeding the AILCCP board-quarterly report (F43 mitigation). Round-2 C14. |
| D-7 | Trajectory capture is cheap and production-tested | **accepted with justification** | OpenHands V1's sub-ms per-event persist ([report 11 §6](../../../research/11-openhands-substrate-audit.md)) is the substrate measurement anchor; trajectory is the *inside-the-interval* event stream. The interval object envelopes the trajectory; the architecture pays the C16 / D-7 cost as already-priced. Generalisation caveat: the OpenHands measurement is on its own benchmark; substrate selection is a Phase-5 ADR. |

---

## §5 Cold-start (mandatory)

### 5.1 Cold-start is the bootstrap interval

On day 0, the factory has *one* `EscrowInterval{kind: bootstrap, priors.in-tree: [], pace-layer: standards}`. There is no codebase, no issue queue, no `docs/solutions/`, no prior cycles. The bootstrap interval's *job* is to produce the seed graph of subsequent intervals (a methodology DAG) plus the seed artifact set (an `EvaluationSuite` per El Kaim, a `Frontier AI Framework` per SB 53 if applicable, an `ArchitectureSpecification` typed object, an initial `AGENTS.md` scaffold). All of these are content-addressed handles stored in the interval object store.

### 5.2 Available priors (per brief §0 greenfield definition)

Priors permitted (and expected):

- **Adjacent-domain exemplars.** El Kaim's 9-field intent block ([report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)); Notion's `agent specs/` Markdown layout ([report 35](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)); Codex `.rules` DSL templates ([report 18](../../../research/18-openai-codex-substrate.md)).
- **RE/SE foundations.** EARS five patterns + INCOSE GtWR R7–R35 + Complexity Primer principle-12 — the cold-start required reading ([report 25](../../../research/25-requirements-engineering-foundations.md)) supplies the spec-authoring discipline plus deterministic lint at the bootstrap interval's `gate`.
- **Academic empirical anchors.** Yang et al. (instruction-following ceiling at 10–20 requirements; redundancy 65.2%) and Larbi et al. (silent contradictory-prompt collapse) ([report 26](../../../research/26-prompt-underspecification-academic.md)) supply the threshold-bar for promotion from bootstrap to next-interval and the cross-model-judge requirement.
- **Governance scaffolding.** AILCCP 37 principles / 48 controls ([followup/10 §A/§B](../../../research/followup/10-governance.md)) supply the policy templates for `approval-gate` / `sandbox` / `log` per interval-kind; the Caremark-line / SB 53 / SEC IAC framing ([report 31](../../../research/31-caremark-rsi-board-exposure.md)) supplies the board-visibility primitive the bootstrap must produce.
- **Operator-curated knowledge.** The operator's `AGENTS.md` / `CLAUDE.md` scaffold (Round-2 C11), prior-run skill libraries (transferable across operator-instances of the substrate), Compound-Knowledge-style insight/playbook/correction/pattern typed learnings ([followup 11](../../../research/followup/11-compound-knowledge.md)) when the operator brings them.

The greenfield-vs-brownfield asymmetry here is *only* in `priors.in-tree`: brownfield bootstrap has tests + traces + codebase, greenfield does not. *Everything else is shared.*

### 5.3 Bootstrap interval policies (strictest defaults)

Because the bootstrap interval is the regime with the largest unspecified surface (F3 critical, F36 critical, F37 critical, F39 critical, F41 critical, F55 critical for greenfield), its policies are the strictest:

- **gate:** deterministic EARS/GtWR lint (F38 mitigation) + LLM-judge with `judge-diversity: different-family` (F36/F37/F46 mitigation) + complexity-diagnosis field at open (F39 mitigation).
- **log:** AILCCP immutable logging on; full trajectory + decision-log retention (F43, F54).
- **sandbox:** all interval-bound activity in bwrap+seccomp or container; substrate-default-off production-access ([report 32 §8.2](../../../research/32-shapiro-completion-chat-agent-claw.md), F44).
- **approval-gate:** required at 100% sample rate (sample-audit graduates only when interval-kind clears Jaymin Automation-Mode thresholds, OQ-B6).
- **reflection-trigger:** STIR cascade ([report 30 §4](../../../research/30-cognitive-escrow.md)) + delegation-confirm + success-criterion articulation; F42, F53 mitigation.
- **classifier.automation-eligibility:** `escalate` at bootstrap; cannot be set to `lights-out` for the bootstrap interval itself, full stop. (This is the architecture's hardest constraint and pre-responds to the Jaymin / Shapiro / El Kaim / Replit-incident cold-start evidence: no system clears the lights-out bar at day 0.)

### 5.4 Day-0 → day-N trajectory

The factory transitions from cold-start to steady-state when:

1. The bootstrap interval has produced a non-empty methodology DAG with at least one `kind: routine-cycle` interval-class whose policies have been declared and whose declared threshold-bars (per OQ-B6) have been *measured* (K=5 ≥90%; 5-of-5 paraphrase robustness; zero medium-or-high safety incidents over a declared window).
2. The classifier's interval-class taxonomy has been audited at a re-entry interval; the operator has confirmed which interval-classes graduate to `automation-eligibility: lights-out` and which remain `escalate` / `sample-audit`.
3. The board-visibility apparatus per F43 mitigation (AILCCP three-controls coverage + SB 53 applicability + IAC three-question response) has produced its first quarterly report and the operator has acknowledged it.

Until those three conditions hold, every interval is at minimum `sample-audit`. There is no "lights-out greenfield" until the factory has measured itself against its declared bars, and the measurement is itself an interval.

### 5.5 Silent-failure protection

Per brief §5.2's "how is the bootstrap protected against silent failure" question:

- **The bootstrap interval cannot self-judge.** Its `gate.judge-diversity` is mandatorily `different-family`; the architecture refuses to allow same-family or same-model bootstrap-judging (F1 critical, F27 critical, F46 high on greenfield).
- **Behavioural drift (F55) is checked at every methodology-delta interval.** Methodology evolution intervals (OQ-B9) must score against the *original* bootstrap-interval acceptance criteria; drift triggers escalation.
- **No track record yet** is itself a fact the substrate carries: a `track-record-depth` field on the interval-class taxonomy that the classifier must consult before promoting a class to `lights-out`. Until N successful sample-audit cycles exist (N is a Phase-5 ADR; corpus-default per Jaymin K=5 is 5), promotion is refused.

### 5.6 What the bootstrap *outputs*

A typed product, content-addressed:
- An `EvaluationSuite` (per El Kaim's `protects: RULE-ID` linkage, [report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)).
- An `ArchitectureSpecification` typed object with `derivedFrom` rules.
- A methodology DAG (graph-of-intervals).
- A scaffold set (`AGENTS.md`, skills directory, policy templates).
- A `Frontier AI Framework` (if SB 53 applicable; [report 31 §3](../../../research/31-caremark-rsi-board-exposure.md)) or its sub-threshold equivalent (RSI-three-part-test declaration).
- A first board-quarterly draft (F43 mitigation surface).

All of these are *artifacts produced by an interval whose `automation-eligibility = escalate`*. The operator authored them with substrate support. Day-1 onward, the substrate fires them automatically per the gates the operator declared.

---

## §6 What this track is NOT trying to be

- **Not a substrate-stack recommendation.** The architecture is agnostic between OpenHands+Overstory and Gas City (CTR-C5). Either can carry the interval primitive; Phase-5 ADRs pick.
- **Not a Methodology-vs-substrate-boundary ruling for all of v3.** This track answers OQ-B2 *for this architecture* (boundary at the methodology layer). Other unified tracks (B, C) and the 6 mandate-specific tracks may answer differently.
- **Not a falsification of UC4.** It is a *defensible unified architecture* per D1's brief, claiming the spec-malleable / code-archaeological tension is per-interval-policy-shaped, not per-architecture-shaped. UC4 may still hold for *other* architectures.
- **Not a count-of-architectures claim.** The v3 set may include this *plus* mandate-specific architectures; the comparison matrix (D2) will show per-(architecture × work-unit-class) fit. This track claims `both` only for the unified architecture itself.
- **Not a defence of any specific provider, model family, or vendor.** Provider properties are interval-policy-declared (OQ-B8).
- **Not a verdict on the factory-vs-company metaphor.** The frame is process-control (intervals as state-machine nodes), neutral on Brier's metaphor war (CTR-F1).
- **Not an answer to F36/F37 numbering** (resolved by lead agent per brief §0; this track only consumes the resolved numbers).

---

## §7 Open questions surfaced by this track

1. **Interval-granularity.** At what cadence is an interval an `EscrowInterval`? Every send/receive pair? Every cycle? Every gate-boundary? The axis works at multiple granularities; choosing one is a Phase-5 ADR. **Most load-bearing open question this track surfaces.**
2. **Classifier accountability.** The classifier itself is the architecture's most powerful actor (it decides automation-eligibility per interval). F57 (design-authority erosion via convenience-reclassifies-stakes) is *amplified* by giving so much weight to one substrate primitive. Audit discipline on the classifier's decision history is necessary but corpus-light on detail.
3. **Re-entry registrar protocol completeness.** OQ-B3 is answered in shape (re-entry is a typed interval) but not in protocol (what does the substrate hand to the human at re-entry; how does the human commit a graph-state change back; how is partial re-entry — human acknowledges but does not redirect — represented?). Phase-5 ADR.
4. **Cross-interval correlation against F48 (tacit collusion via shared context).** If many intervals share access to the same trajectory store or scenario library, the F48 multi-agent collusion surface may re-emerge at the substrate layer. Whether interval-object-store *itself* needs partition discipline is unresolved.
5. **Multi-codebase intervals.** Brief §7 scopes v3 to single-codebase-per-factory; the interval substrate accepts the constraint, but several primitives (Codex Spaces, [report 19](../../../research/19-github-copilot-cloud-agent.md)) suggest interval policies could be team-or-org-scoped. Future work.
6. **Cost model for full immutable logging at high parallelism.** F43 + AILCCP immutable logging demands grow with interval count; CTR-E6 ([followup 08 §3](../../../research/followup/08-security-primitives.md)) names the CaMeL ~7-point utility tax as the corpus' empirical anchor for substrate-safety having a cost. Combined cost of immutable logging + cross-family judge + STIR-cascade reflection across high-parallelism interval graphs is not corpus-measured. Substrate-cheap thesis (Round-2 / D-7) may not survive this combination.
7. **Whether "interval" is itself a contaminating label.** Per D5/D7 (bias-guard discipline), the chosen axis name carries downstream framing weight. A blind-axis test (D7) on this track is appropriate if two other unified subagents also converge on interval/escrow framing.

---

*End of unified-A.md.*
