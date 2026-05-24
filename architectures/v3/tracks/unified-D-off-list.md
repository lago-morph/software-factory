---
track: unified-no-axis-D-off-list
axis: trust-topology (who-trusts-which-artifact-given-what-evidence; a directed graph of artifact-and-agent trust relationships, not a linear ordering)
mandate-scope: both
based-on-commit: 1127c71
based-on-date: 2026-05-24
---

# Unified Track D (off-list supplement) — Trust-Topology-as-Primary

A unified architecture organized around a **directed graph of trust relationships** between agents and artifacts. Mandate, stakes-tier, pace-layer, and regime are all *projections* of the trust-graph onto different reading orders. The architectural primitive is the **trust edge** (`who trusts what, conditional on what evidence`) — not the layer, not the tier, not the cycle.

This track is the off-list supplementary unified track dispatched per the Phase-2 axis-divergence audit's §6 recommendation, after unified-A and unified-C converged on tier (with strong bias-guard amplification per `anchor-detector.md` CONVERGENCE-3) and unified-B picked the only remaining brief-named alternative (Brier pace-layers). The brief is acting as a soft prompt; this track tests whether an *unprompted* axis is defensible.

---

## §0 — Axis declaration, defense, glossary, falsification-prep

### 0.1 Axis declaration (one sentence)

**Every artifact and every agent in the factory is a node in a directed graph whose edges are *trust relationships* (`subject trusts object | conditional-on evidence-class`); the architecture's primary job is to declare, enforce, audit, and revise this graph — and every other axis (tier, mandate, regime, pace-layer) is a *derived view* of it.**

### 0.2 Glossary (this track's vocabulary)

| Term | Definition (in this track) |
|---|---|
| **Trust edge** | A directed relationship `subject → object [evidence-class, confidence-bound]`. Subjects are agents (builder, judge, classifier, watchdog, operator). Objects are artifacts (spec, code, scenario, prior-cycle output, knowledge-store entry, runtime trace) and other agents. Evidence-class is *what kind of evidence has to be present for the trust to hold* (e.g., `same-model-self-review`, `cross-model-attestation`, `deterministic-rule-pass`, `human-ratification`, `production-trace-replay`, ``derivedFrom``-chain-intact). |
| **Trust topology** | The full directed graph of trust edges in a factory instance at a moment in time. Mandate-agnostic structural object. |
| **Trust boundary** | A cut-set in the topology that no edge crosses without an enumerated evidence-class. Examples: the lethal-trifecta closure surface (Willison), the CaMeL typed perimeter ([followup `08`](../../../research/followup/08-security-primitives.md)), the holdout boundary (D-4), the AILCCP Human Approval Gate. |
| **Provenance chain** | The transitive closure of `derivedFrom` edges from any artifact back to a *trust root* (a human-curated artifact or a deterministic-rule output). El Kaim's `derivedFrom` ([report `14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)) + Beads' `discovered-from` ([report `38`](../../../research/38-gas-systems-substrate.md)) are the corpus' two strongest primitives at this layer. |
| **Trust root** | A node trusted by axiom (not by evidence). Greenfield trust roots: operator-authored intent block, EARS/GtWR rule set, AILCCP control catalog, language compiler. Brownfield trust roots: existing test suite-that-passes, production-trace ground-truth, operator-attested invariant extraction, language compiler. **The set of trust roots differs by mandate; the graph shape does not.** |
| **Evidence-class** | A typed predicate that an edge consults to decide whether the trust holds at this moment (e.g., `cross-model-attestation` requires ≥2 model-family-disjoint judges' agreement). |
| **Adversarial edge** | A trust edge configured to *expect* the object to fail the evidence test — the kevin/carl pattern ([report `34`](../../../research/34-lenny-howiai-personal-harnesses.md)): the critic-agent's trust in the builder-agent is *adversarial* (default = distrust until proven). |
| **Trust-graph mutation** | Any operation that adds, removes, or re-conditions an edge. Mutations are themselves first-class artifacts (they live in the graph as nodes with their own provenance). Mitigates F24 trust creep by making creep observable. |

### 0.3 Off-list confirmation and rejection inventory

**Confirmed off-list.** I considered each prohibited axis from the brief and rejected each before settling on trust-topology:

- *Substrate-vs-methodology split.* Rejected: that is a layer-of-implementation question and the anchor-detector already flagged it as the Round-2 default. Both A and C have it as a *consequence* of their tier axis, not as their primary axis; doing it here would just collapse to the unified-A/C shape with renaming.
- *Regime (Augmentation vs Automation per Jaymin).* Rejected: per brief §2.1 the regime decision is already named as the lead-agent working stance ("(c)+(b)"); picking it as primary is the most brief-compliant move possible.
- *Stakes/risk-tier/blast-radius.* Prohibited; this is the unified-A/C convergence the audit recommended I test against.
- *Work-unit-class (D2 taxonomy).* Rejected: D2 names it as a *secondary dimension* of the mandate-fit matrix; making it primary would smuggle D2 from "matrix dimension" to "architectural primitive" without independent corpus support.
- *Codebase-lifecycle stage.* Rejected as effectively mandate-derived (greenfield = early; brownfield = late). Would collapse to mandate-as-primary.
- *Knowledge-accumulation strategy as primary.* Tempting (Beads `discovered-from`, CK typed-classification, Compound `docs/solutions/` are corpus-strong) but I judged it as overlapping with trust-topology in a way that trust-topology subsumes — provenance chains are *one specific type* of trust edge. Picking trust-topology lets me keep knowledge-accumulation as a derived view; picking knowledge-accumulation as primary would weaken the architecture's coverage of the security/judge/holdout cluster.
- *Judge-architecture choice as primary.* Rejected for the same reason: judge architecture is a *trust-edge configuration* (cross-model vs same-model is just two values of the `evidence-class` parameter on the judge→builder edge). Subsumed.
- *Scaffold-vs-substrate decomposition.* Rejected: this is a CTR-C6/WEAK-2 framing battle; picking it as axis would force me to relitigate that fight rather than build an architecture.
- *Language-as-harness.* Rejected: even report 33 doesn't treat this as architecturally primary; F45 is one F-mode among many.
- *Governance-tier.* Rejected as a special case of stakes-tier (regulatory exposure is one of unified-C's three tier dimensions).
- *Pace-layers (Brier-style).* Prohibited; unified-B's territory.

**Off-list axes I also considered and rejected for this architecture:**

- *Information-flow direction (spec→code vs code→spec vs bidirectional).* Strong candidate — maps onto UC4 directly. Rejected because (i) "code→spec" is just the brief's "code-archaeological" label slightly renamed, smuggling codebase-lifecycle-stage back in as primary; (ii) the unified case under information-flow would be "bidirectional reconciliation" which is a *property of* a trust topology (the spec→code edge and code→spec edge co-exist with conditional evidence) — so info-flow is subsumed by trust-topology too.
- *Coordination shape (single / multi-coop / multi-adv / population).* Rejected because the anchor-detector documents that no Phase-2 track adopted Tournament-style population, suggesting the corpus does not support coordination-shape as architecturally primary; F48/F49 (collusion, [report `37`](../../../research/37-academic-llm-agent-collusion.md)) is the negative evidence here.
- *Memory architecture (stateless / per-session / cross-session / permanent).* Rejected as too narrow; the corpus has thin coverage of memory-class distinctions, and the trajectory-capture / knowledge-store distinction collapses memory questions into provenance questions.
- *Time-horizon (per-cycle / per-session / per-month / per-quarter).* Rejected because it overlaps heavily with Brier pace-layers (the layers are largely time-horizon distinctions), making this near-prohibited.
- *Failure-locus (substrate / methodology / runtime / human).* Tempting because F-modes are diverse, but it is more a *taxonomy of F-modes* than an organizing primitive for an architecture. Rejected.

**Why trust-topology is the survivor.** Reading the §C-bis must-read list (corpus-inventory.md L364–L381) without the brief's candidate-axis list in front of me, the most striking *cross-source* convergence is *trust-shape language*:

- Willison's **lethal trifecta** (private-data × untrusted-content × exfiltration) is explicitly a trust-graph cut ([report `05`](../../../research/05-simon-willison.md), [followup `08`](../../../research/followup/08-security-primitives.md)).
- CaMeL's **PI-SEC formal security game** with NORMAL/STRICT interpreter modes is a formalized trust-graph with typed perimeters ([followup `08`](../../../research/followup/08-security-primitives.md), §3 expanded).
- El Kaim's **`derivedFrom` rule** + **`protects: RULE-ID` linkage** is a typed trust-edge specification at the spec/architecture/evaluation layer ([report `14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)).
- Beads' **`discovered-from` edge** is a typed provenance edge in the knowledge graph ([report `38`](../../../research/38-gas-systems-substrate.md)) — "strictly more expressive than Compound Atelier's flat-file `docs/solutions/`" per the corpus inventory's own framing.
- The **holdout discipline** (Round-2 C13, D-4) is a trust-cut between the builder agent and the acceptance criteria — the *single most-cited substrate primitive across all 9 Phase-2 tracks*.
- The **kevin/carl** cross-model QC pattern ([report `34`](../../../research/34-lenny-howiai-personal-harnesses.md)) is an *adversarial trust edge* between two agents.
- The **AILCCP Human Approval Gate** (followup `10`) + **Caremark-line accountability** ([report `31`](../../../research/31-caremark-rsi-board-exposure.md)) are trust handoffs to humans/boards/regulators.
- F24 **trust creep** is a failure mode named in trust language. F27, F1, F46, F48 are all trust-topology pathologies (same-model-validates-self collapses the trust graph to a single self-loop). F8 **stale-knowledge inversion** is a trust-edge-staleness problem. F58 **runtime/design-time compliance split** is a trust-edge that holds at design time but not at runtime.

The corpus has *trust language scattered everywhere* and **no architecture in any of the unified A/B/C tracks treats trust as the organizing primitive**. They treat trust as one of N concerns, downstream of tier or pace-layer. The off-list constraint forced this re-read; the re-read shows trust is at least as well-supported as tier and is *more* supported than pace-layers (Brier appears in exactly one report; trust appears in 8+).

### 0.4 Defense: why trust-topology is architecturally productive

Four reasons:

1. **It dissolves CTR-A4 (lights-out vs L5 vocabulary mapping) without invoking tier OR pace-layer.** Lights-out (UC1) is a property of the *trust graph's edges that cross the operator boundary*. If no edges cross that boundary during a cycle, the cycle is lights-out. L5 (Jaymin's anti-pattern) is the *forbidden state* where the operator→factory edge has no evidence-class attached (operator trusts factory unconditionally). L4 (Shapiro "I'm here") is the state where the operator→factory edge has `escalation-triggered-presence` as its evidence-class. The vocabulary mapping is structural, not stipulative.

2. **It engages MISSED-3 (El Kaim invariants vs UC4 spec-malleability) without invoking the invariant/body split that anchor-detector flagged as bias-guard-amplified (CONVERGENCE-1).** Under trust-topology, the invariants are *trust roots* (axiomatically trusted, evidence-free); spec body is *non-root* (trusted only via evidence-class chains). UC4 malleability is the property of *non-root* nodes; El Kaim invariants are the property of *root* nodes. The split is between roots and non-roots — not between "invariants vs body" (which is just one specific instance of root-vs-non-root at one specific layer).

3. **It directly attacks F24 (trust creep), F27 (circularity), F46 (single-model review blindspot), F48 (collusion), F1 (hallucination self-reinforcement) as ONE coherent failure-mode cluster** — they are all trust-graph pathologies (cycles, single-node self-loops, missing evidence-class on critical edges, undeclared shared context creating implicit trust edges). Unified-A and unified-C handle these as separate failure modes with separate mitigations; trust-topology handles them with one mechanism (graph-shape constraints + per-edge evidence-class enforcement).

4. **It works identically for both mandates because trust topologies don't care which mandate fills them.** A greenfield factory's day-0 trust graph has operator-authored intent block + library docs + EARS/GtWR rules as trust roots. A brownfield factory's day-0 trust graph has existing-passing-tests + production-trace-ground-truth + operator-attested-invariants as trust roots. **The roots differ; the graph shape, the edge taxonomy, the evidence-classes, and the audit primitives are identical.** This is a different unification claim than tier (which says "mandate is a statistical distribution over tiers") or pace-layer (which says "mandate is per-layer initial state"); it says "mandate is a different *root-set* of the same graph."

### 0.5 Pre-response to Phase-3 unified-mandate-attacker

The attacker has three predictable lines.

**Attack line A — "This is tier in disguise."** The strongest attack. *"Your `evidence-class` parameter on edges is just `tier` renamed; high-stakes edges require cross-model-attestation, low-stakes edges require self-review, and your trust graph is a tier-classifier walking around dressed as a graph."*

Pre-response: structurally, no. Tier is **a linear ordering of work-units by externally-observable consequence**. Trust topology is **a directed graph of relationships between agents and artifacts**. Three concrete differences a tier-classifier cannot represent:

- **The same artifact can have different evidence-classes on different edges.** A spec is trusted by the builder via `derivedFrom-chain-intact` AND by the operator via `human-ratification` AND by the judge via `EARS-lint-pass` — three different evidence-classes, three different consumers, one artifact. Tier collapses this to one tier-value-per-artifact.
- **The graph admits cycles that the architecture must explicitly break.** F27 (circularity / same-model builds and validates) is a literal cycle in the trust graph. Tier-classification cannot represent or detect cycles; cycle-breaking is the trust-topology primitive that addresses F27 by graph-edit, not by per-cycle gate.
- **Trust roots are mandate-derived; trust edges are mandate-agnostic.** This is the unification mechanism. Tier-axis cannot say this because tier doesn't have a notion of "root"; everything is tiered.

The attacker may rephrase: "Okay then your `evidence-class` is just `cross-model-attestation, deterministic-rule-pass, etc.` which is the *same set of mechanisms unified-A and unified-C invoke per-tier*." Concession: yes, the mechanism *set* overlaps substantially — corpus-shaped. But the **selector function** is different: tier-axis selects mechanisms by a scalar tier index; trust-topology selects per edge as a property of the *relationship*, allowing the same agent to use cross-model-attestation against one builder and same-model-review against another in the same cycle. This is not expressible in a tier matrix.

**Attack line B — "This is pace-layers in disguise."** *"Your trust roots are the slow-pace-layer artifacts (standards, invariants); your non-roots are the fast-pace-layer artifacts (code, plans). You've redrawn Brier's diagram as a graph."*

Pre-response: no. Pace-layers is ordered (Standards > Architecture > Specs > Plans > Code). Trust topology has roots that may sit at *any* pace-layer. A production-trace from yesterday is a brownfield trust root that lives at the *Code/runtime* pace-layer, not at Standards. A regulatory standard is a greenfield trust root that lives at Standards. The same graph shape accommodates both; pace-layers cannot accommodate "Code-layer trust roots" without contradiction. Brier's framing requires *direction* (slow trusted, fast contingent); trust-topology requires only *evidence-class*.

**Attack line C — "Trust graphs are unimplementable / not legible to operators."** *"You've just renamed every artifact and every relationship and made the architecture into homework for the operator."*

Pre-response: the corpus already implements partial trust topologies — El Kaim's typed objects with `derivedFrom`, Beads' `discovered-from`, AILCCP's 48 controls (which are trust-edge declarations between regulator and runtime), CaMeL's typed perimeters. The architecture's claim is **make them first-class, audited, and unified**, not invent them. Implementation cost is real — see §7 OQ-D2 for the legibility question and §1.5 for the substrate's role in keeping the graph small enough to be operator-readable.

**Pre-response to the "this is tier/pace-layers in disguise" charge generally.** The single strongest test is the *fundamental theorem*: a tier-classifier is a function `work-unit → tier ∈ {T0..T4}`. A pace-layer assigner is a function `artifact → layer ∈ {Code..Standards}`. A trust-topology is a *labeled directed graph* over `{agents} ∪ {artifacts}`. The latter cannot be reduced to either of the former because cycles and multiple-incoming-evidence-classes are first-class in graphs and absent in linear orderings. If a Phase-3 reviewer collapses the trust graph to a tier classifier they have *thrown information away*. Whether that information is *load-bearing* for the architecture is the falsifiability question; §8 addresses it.

---

## §1 — Architectural sketch

### 1.1 The factory as a maintained trust graph

The factory is a system that maintains a directed graph `G = (N, E)` where:

- **N (nodes):** agents (builder, judge-set, classifier, watchdog, operator, board-reviewer) ∪ artifacts (spec fragments, intent blocks, code commits, scenarios, knowledge-store entries, trajectory traces, ADRs, ARCHITECTURE.md, AGENTS.md, runtime telemetry events).
- **E (edges):** typed trust edges `subject → object [evidence-class, confidence-bound, expiry]`. Edges are *first-class artifacts* — they are themselves nodes in the graph with their own provenance.

A factory cycle is **a graph mutation**: it adds new artifact nodes, adds new edges connecting them to existing nodes via evidence-classes, and may revise existing edges (re-conditioning, expiring, or breaking them).

The architecture has six substrate primitives, six methodology operations, and one invariant.

### 1.2 Substrate primitives (mandate-agnostic, graph-aware)

| # | Primitive | Role | Anchor |
|---|---|---|---|
| **S1** | **Graph store** | Persistent, append-mostly store of nodes and edges. Edges are immutable post-creation; revisions create new edges marking the old as `superseded-by`. Substrate-enforced. | Beads `discovered-from` ([report `38`](../../../research/38-gas-systems-substrate.md)); El Kaim `derivedFrom` ([report `14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)); CK typed-classification ([followup `11`](../../../research/followup/11-compound-knowledge.md)). |
| **S2** | **Evidence-class registry** | A *closed-by-default* enumeration of permitted evidence-classes. Operators may add classes via versioned operator policy; agents may not invent classes mid-cycle. Mitigates F38 (vocabulary lint debt) at the trust-graph layer. | Codex `.rules` Starlark DSL ([report `18`](../../../research/18-openai-codex-substrate.md)); AILCCP 48-controls catalog ([followup `10`](../../../research/followup/10-governance.md)). |
| **S3** | **Edge-evaluator** | Substrate-internal function that, given an edge, computes whether its evidence-class predicate currently holds. Deterministic where possible (compiler-output / test-pass / `.rules` rule-eval); LLM-judged only where evidence-class explicitly names an LLM check (e.g., `LLM-spec-quality-judge`). F51 (Ashby-deficient probabilistic guard) addressed: the *evaluator itself* defaults to deterministic; LLM checks are evidence-class-named, not infrastructure-defaults. | F51 lesson per [report `25`](../../../research/25-requirements-engineering-foundations.md) candidate F39; CaMeL formal PI-SEC game ([followup `08`](../../../research/followup/08-security-primitives.md)). |
| **S4** | **Cycle-detector** | Substrate-internal graph algorithm that runs after every mutation, detecting (a) cycles, (b) single-node self-loops, (c) "trust-creep" patterns (an artifact whose trust path now relies only on artifacts it produced — F24, F27, F55). Cycles trigger Patrol-tier watchdog escalation. | F24 trust creep; F27 circularity; F55 behavioural drift. |
| **S5** | **Trajectory capture** (D-7 retained) | Every node-add and edge-add is a trajectory event; OTEL five-event export ([report `18`](../../../research/18-openai-codex-substrate.md)) tags events with `node-class`, `edge-class`, `evidence-class`. Mandate-agnostic. | D-7; [report `11`](../../../research/11-openhands-substrate-audit.md) OpenHands V1 sub-ms measurement anchor. |
| **S6** | **Tiered watchdog** (D-6 retained) | Daemon (mechanical), Triage (AI-reclassification), Patrol (drift). Patrol layer specifically watches for: cycle-detector escalations, trust-root erosion (a former trust root demoted to non-root without operator ratification), evidence-class expiry cascades. | D-6; F53 voluntary-discipline fragility (substrate-triggers replace voluntary discipline). |

This is a *small* substrate. It does not include: a tier-classifier, a pace-layer assigner, a regime selector, a mandate-feed adapter, or an overlay-matrix. Those constructs are unnecessary because the graph itself encodes the equivalent information.

### 1.3 Methodology operations (mandate-agnostic; six)

A cycle is composed from these six operations:

| # | Operation | Description |
|---|---|---|
| **M1** | **Root-declare** | Operator (or substrate-bootstrap) declares a node as a trust root. Permitted only at session boundary or via versioned operator policy. Greenfield day-0 invokes this heavily; brownfield ingestion uses it to register existing-tests as roots. |
| **M2** | **Derive** | An agent produces a new artifact node from existing nodes, adding `derivedFrom` edges with evidence-classes attached. Evidence-classes are *declared at derivation time* — the agent says what evidence it claims supports the trust. Cannot be retroactively weakened (this prevents F24 trust creep). |
| **M3** | **Attest** | A judge (LLM, deterministic rule, human, runtime) emits an evidence-class verdict on an existing edge. Attestations are themselves nodes (with `attested-by` provenance). Cross-model attestation (kevin/carl) is M3 with two judges of model-family-disjoint provenance. |
| **M4** | **Reconcile** | When two derivation paths produce conflicting artifacts (a greenfield spec→code path produces version X; a brownfield code→spec path produces version Y), the substrate flags the divergence and either operator-ratifies or auto-merges *only* if a `reconciliation-evidence-class` is configured. **This is where bidirectional information-flow lives** (greenfield and brownfield co-existing in one factory). |
| **M5** | **Expire** | Edges have expiry conditions (time, version-of-source, supervening-event); when expiry fires, the edge is removed (with `superseded-by` annotation) and downstream artifacts are flagged as trust-stale until re-attested. F8 (stale-knowledge inversion) is addressed structurally. |
| **M6** | **Cut** | Operator or substrate may impose a *trust boundary* — a cut-set the graph must not cross without an enumerated evidence-class. The lethal-trifecta closure (Willison) is a substrate-default cut. The AILCCP Human Approval Gate is an operator-declared cut for regulated work. |

This is the entire methodology. No issue queue. No `.dot` pipeline. No Refinery layered spec. No Tournament population. **Those v2 architectures are not erased — they reappear as configurations of trust-graph mutations** (an issue queue is a list of M2 derivations pending attestation; a `.dot` pipeline is a fixed mutation-sequence template; Refinery is M2-with-spec-layer-roots; Tournament is parallel M2 + M3 cross-attestation).

### 1.4 The invariant

**Invariant: every artifact's trust path must terminate at a trust root within K hops, where K is operator-policy-set (default K=8).** Artifacts that lack such a path are quarantined (substrate-enforced; trajectory-logged; cycle escalates).

This invariant *is* the architecture's safety floor. It is the trust-topology analog of D-4 (holdout discipline): holdout is the property that the builder's trust graph does not include an edge to the acceptance-criteria node. Generalizing: the safety floor is **trust-graph well-formedness**.

### 1.5 Operator-readability: how the graph stays legible

A trust graph over a year of factory operation could grow to millions of nodes. The architecture keeps it readable via three mechanisms:

- **Forgetfulness by expiry (M5):** stale edges removed automatically; downstream artifacts re-attest or quarantine.
- **Layer-projection (read-only views):** the operator sees the graph projected onto specific lenses (mandate-view, tier-view, pace-layer-view) — proving that the prohibited axes are *useful as views* without being primary.
- **Trust-root dashboard:** operator-facing UI shows the trust roots and the first-hop edges; deeper structure is queried on demand.

This is *not* a graph-database product pitch; it is a claim that the substrate must own legibility as a first-class concern. OQ-D2 names the specific implementation question.

### 1.6 How mandate appears in this architecture

**Mandate is the trust-root set, plus the default derivation polarity.**

- **Greenfield day-0:** trust roots = operator intent block (El Kaim 9-field) + EARS/GtWR rules + adjacent-domain priors-as-`prior-art`-roots + AILCCP control catalog. Default derivation polarity is **spec→code** (specs are derived first, code derives from them via `implements`-class edges).
- **Brownfield day-0:** trust roots = existing-passing-tests + production-trace-ground-truth + operator-attested invariants extracted from codebase + AILCCP control catalog. Default derivation polarity is **code→spec** (the existing code is the root; specs are derived as `extracted-from` artifacts).
- **Mixed (brownfield extending a system):** both polarities are active; M4 (Reconcile) is the cycle's heaviest operation.

The *substrate* (S1–S6) and the *methodology operations* (M1–M6) are identical across mandates. Only the trust-root set and the derivation-polarity default differ.

---

## §2 — Load-bearing concerns

### 2.1 Engagement with CTR-A4 (lights-out↔L5 vocabulary mapping)

**Mapping:**

- **Lights-out (UC1):** every cycle's mutation operations execute without requiring an operator→factory trust edge with evidence-class `operator-in-loop`. The cycle may add such edges (escalating); it may not require them as preconditions.
- **L4 (Shapiro "I'm here"):** the *operator→factory* trust edge exists with evidence-class `escalation-triggered-presence` — the operator is reachable on substrate-triggered escalation.
- **L5 (Jaymin's anti-pattern):** the *operator→factory* edge exists with evidence-class `unconditional` — no evidence required, no escalation path. **This architecture forbids unconditional edges at all trust boundaries by substrate invariant (§1.4).** L5 is structurally unreachable, not policy-prohibited.

This is brief §2.1 option (c)+(b) implemented structurally rather than declaratively. The anchor-detector flagged option (c)+(b) as *brief-implicit anchoring* (CONVERGENCE-4); this track's mapping is brief-compliant but the mechanism (forbid unconditional edges) is corpus-derived (Willison trifecta + AILCCP attestation requirements), not brief-derived.

### 2.2 Engagement with MISSED-3 (El Kaim invariants vs UC4 spec-malleable)

**Reconciliation by trust-root partition.** El Kaim's `invariants` field nodes are *trust roots*. UC4's malleable-spec body nodes are *non-roots* whose trust paths route through the invariants. Spec body mutates freely; invariants do not mutate (they are roots; mutation requires session-boundary ratification).

This is **structurally different** from the invariant/body split that CONVERGENCE-1 documented across six other tracks. Those tracks did the split by *intent-block field membership* (slow fields vs fast fields). This track does it by *graph role* (root vs non-root). The difference matters because:

- The intent-block-field split presupposes the El Kaim 9-field vocabulary; trust-graph split does not.
- The intent-block-field split treats the split as El-Kaim-specific; trust-graph split applies uniformly to *any* artifact (an existing test suite in brownfield is a trust root in exactly the same way as an invariant block in greenfield).
- The intent-block-field split is what bias-guard MISSED-3 explicitly named; the trust-graph split is the *generalization* of which MISSED-3 named one instance.

**Honest concession:** if CONVERGENCE-1's invariant/body split is robust corpus signal (anchor-detector verdict: "largely corpus-signal, but with bias-guard amplifier"), then trust-topology *includes* that split as a special case. The off-list axis is not denying the convergence — it is providing a more general structure that the convergence is a corollary of.

### 2.3 Engagement with F-mode cluster (corpus's trust-shaped F-modes)

The trust-graph framing handles a coherent F-mode cluster with one mechanism:

| F-mode | Trust-graph pathology | Substrate mitigation |
|---|---|---|
| **F1 Hallucination Loop** | Cycle: builder's output becomes its own evidence on next cycle | S4 cycle-detector |
| **F8 Stale-knowledge inversion** | Edge whose evidence-class has expired but is still consulted | M5 expire + edge expiry condition |
| **F12 Lethal trifecta / prompt injection** | Trust boundary cut violated by untrusted-content path | M6 cut + S2 evidence-class registry (CaMeL-class typed perimeter) |
| **F14 Attribution collapse** | Edge present without `attested-by` provenance | S5 trajectory capture of node/edge events |
| **F24 Trust creep** | Edge re-conditioned to weaker evidence-class without operator policy update | M2 monotone evidence; mutation-as-artifact discipline |
| **F27 Circularity / same-model builds & validates** | Single-node self-loop in the trust graph | S4 cycle-detector flags self-loops |
| **F28 Holdout leakage** | Builder-agent → acceptance-criteria edge that should not exist | S6 watchdog enforces the holdout cut |
| **F33 Adversarial-prompt defeat** | Evidence-class `LLM-only` against an adversarial subject | S3 edge-evaluator defaults to deterministic; LLM-only evidence-classes require redundant deterministic backstop |
| **F46 Single-model review blindspot** | Edge `judge → builder` with evidence-class lacking model-family-disjoint requirement | S2 registry distinguishes `same-model-attestation` from `cross-model-attestation`; high-stakes cuts require the latter |
| **F48 Tacit collusion** | Implicit edges between agents via shared context | M2 derivation requires explicit edge declaration; shared-context-as-implicit-trust is detectable by S4 |
| **F51 Ashby-deficient probabilistic guard** | Evidence-class `LLM-judge` on a high-variety disturbance surface | S3 evaluator policy; deterministic checks preferred at high-variety surfaces |
| **F53 Voluntary-discipline fragility** | Operator-attested edges that depend on operator action without substrate trigger | S6 Patrol triggers re-attestation; substrate owns the trigger |
| **F54 Goal subversion** | Trust path that bypasses the original goal-node root | Trust path must terminate at root within K hops (§1.4 invariant) |
| **F55 Behavioural drift / self-reference** | Trust paths increasingly route through agent-produced artifacts | S4 detects trust-creep; trajectory-capture surfaces self-reference fraction |
| **F57 Design-authority erosion (convenience reclassifies stakes)** | Evidence-classes silently relaxed across cycles | M2 monotone evidence + S6 Patrol watches for evidence-class downgrade events |
| **F58 Runtime/design-time compliance split** | Design-time evidence-class diverges from runtime evidence-class | Edges carry both `design-time-evidence` and `runtime-evidence-class` fields; mismatch is a substrate event |

This is **not** "everything is a trust problem so trust solves everything" — it is the observation that the *corpus's most-cited F-modes share a common structural feature* (trust-graph pathologies). The other F-modes (F36 instruction-following ceiling, F40 last-mile drift, F45 language-as-harness, etc.) are *not* trust-shaped and this architecture handles them with the same mitigations the other unified tracks use (scope-discipline, dry-runs, language-floor declaration).

### 2.4 Engagement with D2 (work-unit-class)

Work-unit-class is a *node-class taxonomy* in the trust graph. `initial-spec` work creates spec-class nodes with intent-block roots. `refactor` work creates code-class nodes whose trust paths must terminate at existing test-suite roots. `mvp` work creates code-class nodes whose trust paths terminate at spec-class non-roots which themselves terminate at intent-block roots. Etc.

The five-class taxonomy is preserved; what changes is that each class is defined by *the trust-path-shape* its cycles produce, not by an external label.

### 2.5 Engagement with CTR-C2 (substrate-heavy + thin-methodology vs UC4)

This architecture is **substrate-medium + methodology-medium** — explicitly *not* substrate-heavy. The substrate (S1–S6) is small; the methodology (M1–M6) is also small. Both grow only by adding new evidence-classes to S2's registry (versioned operator policy). The CTR-C2 framing is rejected as a false dichotomy: the right cut is between *substrate that maintains graph well-formedness* and *methodology that performs graph mutations*, both of which are thin if the graph primitive is well-chosen.

The anchor-detector's recommendation that Phase 3 should produce tier-shape AND pace-layer-shape drafts (§5 of audit) **becomes**: Phase 3 should produce tier-shape AND pace-layer-shape AND trust-topology-shape drafts, and the cut between them is a user decision.

### 2.6 Multi-agent / collusion concerns

F48 (tacit collusion, [report `37`](../../../research/37-academic-llm-agent-collusion.md)) and F49 (discussion-as-amplification) are corpus-novel risks the unified-A/C/B tracks treat with restriction (T2/T3 prohibits Tournament-style; T8 doesn't address them deeply). Trust-topology handles them naturally: collusion is the emergence of implicit edges between agents via shared context. The architecture's M2 *requires* explicit edge declaration; an agent reaching consensus with another agent via shared-context-only does not create a trust edge — so the consensus has *no graph-weight* and cannot be the basis for downstream derivation. Multi-agent shapes (Tournament, Council, kevin/carl) are *available* — they just have to declare their edges explicitly. The architecture does not restrict topology shape; it requires topology *legibility*.

---

## §3 — Citations (load-bearing corpus anchors)

The architecture rests on the following corpus anchors. Each cited claim is named with its corpus source.

- **Willison's lethal trifecta** ([report `05`](../../../research/05-simon-willison.md), [followup `08`](../../../research/followup/08-security-primitives.md)) — the corpus' canonical trust-boundary statement. M6 (Cut) is the substrate operation that maintains the trifecta closure; S2's evidence-class registry is the typed-channel mechanism.
- **CaMeL (Google DeepMind + ETH Zürich, arXiv 2503.18813)** — formal PI-SEC trust-graph model with NORMAL/STRICT interpreter modes; the corpus' deepest formalization of typed trust perimeters ([followup `08`](../../../research/followup/08-security-primitives.md) §3 expanded). The architecture's S3 edge-evaluator's deterministic default is corpus-grounded by CaMeL's 7-point AgentDojo utility tax — the cost of safety is named explicitly (engages MISSED-9 / CTR-E6).
- **El Kaim 9-field intent block with `derivedFrom` rules and `protects: RULE-ID` linkage** ([report `14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)) — the corpus' deepest typed-edge specification at the spec layer; directly maps onto S1/M2.
- **Beads `discovered-from` edge** ([report `38`](../../../research/38-gas-systems-substrate.md)) — "the corpus' strongest candidate compounding-of-knowledge primitive at the engine level" per corpus-inventory.md report-38 anchor. S1 graph store extends Beads' edge primitive to all artifact relationships, not just knowledge-store ones.
- **Compound Knowledge plugin** ([followup `11`](../../../research/followup/11-compound-knowledge.md)) — typed four-way classification (insight/playbook/correction/pattern) + first-class `kw:confidence` skill — corpus precedent for typed-evidence-classes on knowledge edges.
- **Codex `.rules` Starlark DSL** ([report `18`](../../../research/18-openai-codex-substrate.md)) — the corpus' canonical auditable-V&V-by-rejection substrate primitive; S2 evidence-class registry inherits this as the deterministic-evaluator path.
- **OpenHands V1 trajectory capture** ([report `11`](../../../research/11-openhands-substrate-audit.md)) — sub-ms per-event persist; S5 inherits unchanged.
- **CJ Hess kevin/carl cross-model QC** ([report `34`](../../../research/34-lenny-howiai-personal-harnesses.md)) — corpus exemplar of adversarial trust edge; M3 (Attest) generalizes the pattern by making cross-model-attestation one named evidence-class among several.
- **Anthropic Auto-Review** ([report `23`](../../../research/23-anthropic-engineering-trilogy.md)) — same-model-different-role attestation as a permitted evidence-class at low-stakes cuts (engages CTR-D7 by making same-model-attestation an explicit evidence-class, not a default).
- **AILCCP 48-controls catalog** ([followup `10`](../../../research/followup/10-governance.md)) — the regulatory-facing edge-declaration set; M6 (Cut) at T3-equivalent governance boundary uses AILCCP control-attestation as its evidence-class.
- **Kahana RSI three-part test** ([report `31`](../../../research/31-caremark-rsi-board-exposure.md)) — the test classifies a factory's *trust-edge to operator/board* as Caremark-exposed; F43 board-visibility gap is the trust-edge missing a regulator-facing evidence-class.
- **Cognitive escrow** ([report `30`](../../../research/30-cognitive-escrow.md)) — the interval is the *recompute window for evidence-class freshness* on operator-facing edges. The anchor-detector flagged cognitive-escrow-as-substrate-primitive as bias-guard-amplified (CONVERGENCE-5); this track does NOT make escrow a top-level substrate primitive — it makes the *general edge-expiry mechanism (M5)* the primitive, of which the escrow interval is one specific case. This is a deliberate dissent from the bias-guard amplification.
- **Husain/Shankar evals findings** ([followup `07`](../../../research/followup/07-evals-deepdive.md)) — "single judge + binary > Likert" maps onto S3 edge-evaluator design: evidence-classes resolve binary (holds / does not hold) per Husain/Shankar's empirics.
- **Schillace Attention Firewall** ([report `28`](../../../research/28-schillace-sunday-letters.md)) — the firewall is a trust boundary between human attention and agent-noise; corpus exemplar of operator-edge engineering.

Anchors I deliberately *do not* lean on:

- **Brier pace-layers** ([followup `12`](../../../research/followup/12-brier-pace-layers.md)) — engaged dialectically only (§0.5 attack line B). Pace-layers is a useful view of the graph; not the organizing primitive.
- **Shapiro Five Levels** ([followup `01`](../../../research/followup/01-shapiro-five-levels.md)) — engaged for vocabulary mapping (§2.1) only.

---

## §4 — §4 defaults: accepted vs challenged

| # | Default | Stance | Justification |
|---|---|---|---|
| **D-1** | Specs are durable, version-controlled, human-curated | **accepted with justification** | Specs are trust roots (greenfield) or first-hop-from-root nodes (brownfield); in both cases human-curated. The version-control is the graph-store's append-mostly property (S1). |
| **D-2** | Scenarios live outside the codebase as a holdout set | **challenged** | Per brief's fragile-default flag and CONVERGENCE-2's seven-track challenge. The graph framing supersedes the location question: scenarios are nodes; the *holdout* is the substrate-enforced absence of an edge from builder to acceptance-criteria, regardless of where the criteria-nodes physically live. D-4 is preserved as the trust-graph property; D-2's location claim is challenged as unnecessary. |
| **D-3** | Agent = Model + Harness | **challenged** | An agent is *also* its set of incoming and outgoing trust edges in the topology. The Model+Harness pair specifies the agent's *internal* implementation; the trust-edge set specifies its *relational* role. Tournament-style population (rejected by all 9 Phase-2 tracks per anchor-detector §3) is admissible under this framing — each population member is an agent with its own edge set. (Note: anchor-detector flagged the D-3 + Natural-Language-Register extension as bias-guard contamination; I do NOT incorporate the Portuguese-vs-English finding as architecturally primary, only as a permitted evidence-class refinement.) |
| **D-4** | Holdout discipline substrate-enforced | **accepted with justification — and generalized** | D-4 is *the* foundational property in this track: the absence of the builder→acceptance-criteria edge is one specific instance of the general substrate property "graph well-formedness." Mandate-agnostic; trust-topology-primary. |
| **D-5** | Hard cost ceilings non-optional in CI | **accepted with justification** | Cost ceilings are per-edge-class properties (an attestation edge requiring cross-model-3-judge has higher cost than same-model-1-judge); per-tier costs become a derived view rather than primary. CTR-E1 ($100K vs $500/day) is explained as different evidence-class profiles in different operator policies. |
| **D-6** | Tiered watchdog Daemon/Triage/Patrol | **accepted with justification** | S6 inherits unchanged; Patrol additionally watches for graph-shape pathologies (trust creep, cycle emergence, root erosion). |
| **D-7** | Trajectory capture cheap and production-tested | **accepted with justification** | S5 inherits; trajectory capture is per-node and per-edge, so the graph's audit history is the trajectory. |

---

## §5 — Cold-start (mandatory per brief §5)

Cold-start in this track is *trust-root declaration* — and **it is symmetric across mandates** in a way the prior tracks could not be.

### 5.1 Day-0 — what trust roots exist

**Greenfield day-0:**
- Operator intent block (El Kaim 9-field; [report `14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)) — `invariants` field flagged as roots.
- EARS canonical guide + INCOSE GtWR R1–R42 ([report `25`](../../../research/25-requirements-engineering-foundations.md)) — registered as deterministic-rule trust roots (the lint rules are evidence-class predicates by themselves).
- AILCCP 48-controls catalog ([followup `10`](../../../research/followup/10-governance.md)) — subset declared in-scope by operator becomes the regulatory-edge evidence-class set.
- Caremark/RSI three-part test ([report `31`](../../../research/31-caremark-rsi-board-exposure.md)) — operator declares whether the factory is RSI-exposed; the declaration is itself a trust root (it sets the evidence-class menu for the operator→board edges).
- Adjacent-domain priors (operator-curated; tagged `prior-art` evidence-class on derived edges).
- Language/compiler ([report `33`](../../../research/33-language-choice-as-harness.md)) — registered as a deterministic-evaluator trust root for type-pass / compile-pass evidence-classes.
- The cognitive-escrow interval ([report `30`](../../../research/30-cognitive-escrow.md)) — operator-policy-set; not a trust root itself but a *policy* governing evidence-class freshness on operator-facing edges.

**Brownfield day-0:** the *roots differ*, the *mechanism is identical*.
- Existing passing tests — registered as runtime-evidence-class trust roots (tests-pass is a deterministic-evaluator predicate).
- Production-trace ground-truth — registered as runtime-evidence-class roots.
- Operator-attested invariants extracted from the codebase via codebase-archaeology agents — the extraction itself is an M2 derivation that the operator then ratifies, converting the extracted-invariant node into a trust root via M1 (Root-declare).
- AILCCP catalog, Caremark/RSI declaration, compiler — same as greenfield.

The architecture's claim: **what differs between greenfield and brownfield day-0 is exactly the trust-root set**. The graph store, evidence-class registry, edge-evaluator, cycle-detector, trajectory capture, and watchdog are identical. The methodology operations (M1–M6) are identical.

### 5.2 Bootstrap protection against silent failure

The cold-start has no track record; the trust graph has minimal structure. Three layered defenses (these are corpus-grounded but I am NOT positioning them as the corpus's only answer — they overlap with anchor-detector's CONVERGENCE-11 which the audit flagged as brief-implicit):

1. **Trust roots are evidence-class-bearing themselves.** EARS/GtWR lint, compiler-passes, AILCCP control-attestations, and existing-tests are *deterministic predicates* — they have signal at day 0 regardless of cycle history. F37 (silent contradictory-prompt collapse, [report `26`](../../../research/26-prompt-underspecification-academic.md) Larbi 73.8%→6.7%) is mitigated by EARS/GtWR contradiction-checks at the M2 step.
2. **Cross-model attestation required on all derivation edges during bootstrap.** Bootstrap-window default: every M2 derivation must carry a `cross-model-attestation` edge from a judge agent of different model-family. F46 (single-model review blindspot) cannot bite. As confidence accumulates (graduation: K=5 ≥70% per Jaymin Augmentation bar — *operator-overridable* per Skeptic #10 / OQ-B6), evidence-class requirements may relax to `same-model-attestation` for low-impact derivations. Bootstrap-window is operator-policy-set; default is 10 cycles or until cycle-detector reports zero trust-creep events for 5 consecutive cycles.
3. **Operator-edge is `escalation-triggered-presence` not `unconditional`.** §2.1: L5 is structurally forbidden. During bootstrap the substrate may set `escalation-triggered-presence` to fire on *any* cycle (i.e., effective L4 throughout bootstrap); as the cycle-detector confirms graph well-formedness over a window, the escalation threshold relaxes.

### 5.3 Trajectory day-0 → day-N

- **Day 0:** trust roots declared via M1; first M2 derivation cycles begin; every derivation cross-model-attested; trajectory capture (S5) populates.
- **Day 0–N1 (bootstrap):** every cycle's M2 → M3 → M4 sequence executes with strict evidence-class requirements; S4 cycle-detector runs after every mutation; S6 watchdog escalates on any anomaly.
- **Day N1–N2 (graduation):** as confidence accumulates, evidence-class requirements may relax per operator policy. Steady state: low-impact derivations may use `same-model-attestation`; high-impact derivations and any derivation crossing an operator-declared cut require `cross-model-attestation` or stronger.
- **Steady state:** factory operates lights-out per §2.1 mapping; operator interacts at policy boundary (registering new evidence-classes, declaring new cuts, ratifying root demotions/promotions).

Cold-start ends when the trust graph has reached operator-policy-set *minimal-shape* properties (default: ≥N trust roots, ≥M derivation-paths-per-root, zero cycle-detector escalations over 30 days). This is operator-tunable.

### 5.4 What cold-start is NOT in this track

Cold-start is *not* a separate architecture, *not* a separate methodology overlay, *not* a tier-pinning regime. It is **the architecture's normal operation with a smaller and operator-attested trust-root set + strict bootstrap-window evidence-class requirements**. The substrate primitives and the methodology operations are unchanged.

This symmetry with brownfield ingestion is deliberate: brownfield ingestion is also "the architecture's normal operation with the trust-root set being initialized from a codebase rather than from operator authorship." The two cases are structurally the same operation with different root-source.

---

## §6 — What this track is NOT trying to be + honest comparison to A, B, C

### 6.1 NOT trying to be

- *Not a tier-shaped architecture.* No T0–T4. No tier-classifier. No tier-indexed cost ceilings (cost is per-evidence-class).
- *Not a pace-layered architecture.* No Code/Plans/Specs/Architecture/Standards stack as primary. Pace-layers are a view, not the spine.
- *Not a substrate-heavy + thin-methodology architecture.* Both substrate (6 primitives) and methodology (6 operations) are small; CTR-C2 is rejected as a false dichotomy.
- *Not a regime-classified architecture.* Regime is the property of operator-facing edges, not a top-level architectural choice.
- *Not a knowledge-accumulation-primary architecture.* The graph store includes knowledge but is not specifically about knowledge.
- *Not denying CONVERGENCE-1 (invariant/body split).* This track *generalizes* the convergence; the split is a corollary of root vs non-root.
- *Not adopting CONVERGENCE-5 (escrow-as-substrate-primitive).* This track makes M5 edge-expiry the primitive; escrow is one specific expiry policy. This is a deliberate dissent from the bias-guard-amplified consensus.
- *Not a multi-codebase coordination story.* Out of scope per brief §7.
- *Not a substrate-stack proposal.* CTR-C5 (Gas City vs OpenHands+Overstory) is deferred to Phase 5; the architecture is substrate-stack-agnostic.

### 6.2 Honest comparison: trust-topology (D) vs tier-axis (A+C) vs pace-layers (B)

| Dimension | Tier-axis (A+C) | Pace-layers (B) | Trust-topology (D) |
|---|---|---|---|
| **Corpus support breadth** | 6+ F-modes severity-graded by production-proximity; Kahana, Shapiro R3, Replit, CodeRabbit, Veracode, METR | 1 primary report (followup 12) + per-layer fits (reports 14, 35) | 8+ reports anchor trust-shape language (5, 8, 14, 23, 31, 34, 38, followup 10, 11) |
| **Corpus support depth** | Strong empirical anchor cluster | Single-author counter-metaphor + per-layer support | Multiple deep formalizations (CaMeL PI-SEC, El Kaim derivedFrom, AILCCP controls) |
| **Independence of selection** | Brief OQ-B7 named "stakes" as candidate; F57 framing presupposes tier — significant bias-guard amplification | Brier explicitly named in candidate axes; selected by 1/3 tracks honestly but brief-anchored | Off-list constraint forced re-read; trust-shape was discovered, not named by brief |
| **Architectural shape novelty** | Substrate + tier-overlays (familiar pattern; resembles operating-system shape) | Stack of concurrent loops (familiar pattern from systems with multiple cadences) | Graph with maintenance operations (less familiar; carries higher implementation-risk) |
| **Resolves CTR-A4 structurally** | Yes (regime-per-tier) | Yes (regime-per-layer) | Yes (regime-per-edge-evidence-class; L5 structurally forbidden) |
| **Resolves MISSED-3** | Tier-graded invariant ratchet (per-tier malleability) | Layer-placement (invariants at Standards, malleable at Specs) | Root-vs-non-root partition (generalizes the other two) |
| **Multi-agent / collusion (F48/F49)** | Restrict to T0/T1 (A); T0/T1 only (C) | Not deeply addressed | Native — collusion is implicit-edge emergence; M2 explicit-edge requirement makes it detectable |
| **Cycles in workflow (F27)** | Per-cycle cross-model judge; not graph-aware | Per-layer judges; not graph-aware | Cycle-detector S4 — first-class |
| **Operator legibility** | Tier matrix is small and readable | Five-layer stack is small and readable | Graph can grow unboundedly; legibility is OQ-D2 |
| **Implementability** | Each primitive corresponds to an existing tool/pattern | Each layer corresponds to an existing artifact discipline | Requires a graph store + cycle-detector + evidence-class registry as new primitives; higher engineering cost |
| **Operator concept-load** | 5-tier matrix + classifier | 5-layer stack + Sentinel | Graph + 6 ops + 6 substrate + evidence-class taxonomy |
| **Falsification surface** | Phase 4 substrate-extraction shows tier mechanisms diverge by mandate → falsified | Brownfield Intake can't extract legible layers → falsified | Graph cannot be kept legible at production scale → falsified (OQ-D2) |

**My honest ranking by strength on the *unified* case specifically:**

1. **Trust-topology (D) — strongest on unified case** because mandate enters at a single locus (the trust-root set) and the entire rest of the architecture is identical across mandates. Tier-axis must invoke mandate-feed adapters or excavation-vs-discovery overlay bifurcation; pace-layers must invoke Cold-Seed vs Intake mandate-specific procedures; trust-topology invokes only "different root set." This is the cleanest unification mechanism.

2. **Tier-axis (A+C) — strongest on empirical-anchor coverage** because the F-mode severity gradient is *genuine* corpus signal (anchor-detector concedes this) and the production-scissors cluster (F12/F33/F44/F56) is the corpus's largest single failure-mode cluster. Tier is the most defensible unified axis *if* you take the F-mode catalog as the primary corpus evidence.

3. **Pace-layers (B) — strongest on artifact-cadence reasoning** because Brier provides a single principled answer to *why* slow artifacts protect fast ones, and the corpus's spec-velocity contradiction (Nystrom fast vs Brier slow, CTR-B7) is resolved with one mechanism. Weakest on multi-mandate symmetry (Cold-Seed and Intake are visibly different procedures).

**On the comparison: is trust-topology genuinely competitive, or is it weaker but defensible, or is this track struggling?**

Genuinely competitive on the *unified* dimension specifically. **Weaker on implementability** (tier-classifier is a Python dict; trust graph is a database). **Weaker on operator legibility at scale** (the OQ-D2 question is real and not glibly answerable). **Stronger on F-mode coverage breadth** (one mechanism for the F1/F24/F27/F46/F48/F55 cluster). **Stronger on resistance to the audit's contamination critique** (the axis was chosen *because* it's off-list, not by anchoring to the brief).

I am not pretending the architecture is dominant. I am claiming it is *defensible as a peer to tier and pace-layers* — and the anchor-detector audit was right to ask for this test, because the corpus does support a third defensible axis when the brief's candidate-list is removed as a soft prompt.

---

## §7 — Open questions

- **OQ-D1.** Cycle-detector (S4) implementation: how does it handle long-range cycles (a five-hop trust path that closes)? Is the algorithm tractable at factory scale? *Next action: Phase-5 ADR on cycle-detector algorithm and complexity bounds; lean-eval brief sized for synthetic graphs of 10K–1M nodes.*
- **OQ-D2.** Operator legibility at scale: the graph could grow to millions of nodes over a year. The Trust-Root Dashboard (§1.5) is plausible but unproven. *Next action: lean-eval brief — operator-readability test on a 100K-node graph after 30 simulated cycles.*
- **OQ-D3.** Evidence-class registry curation: who curates the registry, at what cadence, and how is curation itself trust-graph-modeled (recursive question)? *Next action: Phase-5 ADR on registry governance; operator-policy-versioning model.*
- **OQ-D4.** Bootstrap-window calibration (default 10 cycles, ≥70% K=5): how does this relate to anchor-detector CONVERGENCE-11 (which the audit said was brief-implicit, not robust)? Could the bootstrap-end criterion be derived from cycle-detector quiescence alone, without invoking Jaymin's K=5 bar? *Next action: lean-eval brief — A/B test with-bar vs quiescence-only bootstrap exit.*
- **OQ-D5.** Reconciliation (M4) mechanism for bidirectional information flow: when greenfield-style spec→code derivation and brownfield-style code→spec derivation produce conflicting artifacts, what is the substrate-enforced reconciliation? Auto-merge with cross-attestation? Operator-only? Per-evidence-class? *Next action: Phase-5 ADR on M4 protocols.*
- **OQ-D6.** Substrate-stack mapping: which existing stack (Gas City, OpenHands+Overstory, from-scratch) best implements the graph store + cycle-detector + evidence-class registry? Beads is the closest precedent but is single-purpose (knowledge edges). *Next action: Phase-5 substrate ADR.*
- **OQ-D7.** Does the trust-topology axis defensibly cover the same F-mode coverage as the tier-axis on the *production-scissors cluster* (F12, F33, F44, F56)? §2.3 claims yes via M6 (Cut); the lean-eval should test against a Replit-class incident scenario. *Next action: lean-eval brief — adversarial replay.*

---

## §8 — Falsification reflection (NEW section per dispatch brief)

### 8.1 The dispatch question

The dispatch brief asks: did the off-list constraint find a defensible architecture, or did it confirm tier/pace-layers as the corpus's actual support?

### 8.2 My honest read

**A defensible architecture exists.** Trust-topology is a coherent, corpus-grounded, structurally distinct axis that produces a non-trivial unified architecture. The corpus has rich trust-shape material across at least 8 reports and 4 followups; the axis is not a manufactured artifact of "needing to find something off-list." Multiple primary substrate primitives in the corpus (CaMeL, El Kaim derivedFrom, Beads discovered-from, AILCCP controls, kevin/carl, holdout discipline) are *already* trust-graph primitives that no other architecture treats as a unified primary.

**However.** I will not claim trust-topology dominates tier-axis or pace-layers. Specifically:

- The **F-mode severity-gradient** is genuine corpus signal. It is what makes tier-axis empirically anchored. Trust-topology can re-frame the F-mode cluster (§2.3) but cannot deny the empirical anchor; tier-axis remains the architecture closest to the corpus's largest evidence cluster.
- The **artifact-cadence problem** is also real. Brier's pace-layers is the corpus's only positive treatment. Trust-topology projects pace-layers as a view but does not improve on Brier's analysis at the cadence layer.
- The **implementation cost** of a maintained trust graph is higher than a tier classifier or a layer stack. OQ-D2 is real.

### 8.3 So which is it — contamination or honest signal?

**My verdict: the original A+C convergence was contamination-influenced but not entirely contamination.**

The audit's classification of "mixed → leaning contaminated" (axis-divergence audit §3 aggregate) is accurate. The F-mode severity-gradient genuinely points at production-proximity-as-an-architectural-variable; the brief's OQ-B7 candidate list and F57's framing then amplified this into "tier-classification as the factory's organizing primitive" — which is a *larger* claim than the F-mode evidence alone supports.

The fact that trust-topology *is* defensible from the same corpus indicates the brief's candidate list was indeed acting as a soft prompt. Without the off-list constraint, no Phase-2 subagent would have chosen trust-topology — not because it lacks corpus support but because the brief named easier-to-reach axes. The audit's recommendation to dispatch this track was correct.

But — and this is the honest qualification — **trust-topology is not strictly better than tier or pace-layers**. It is *strictly different*. The three axes carve the corpus differently and each captures something real:

- Tier captures the **empirical severity gradient** (what bites when work goes wrong).
- Pace-layers captures the **artifact-cadence question** (which artifacts protect which others over time).
- Trust-topology captures the **relational structure of trust** (who-trusts-what given what evidence).

The corpus genuinely supports multiple defensible unified architectures. The audit's recommendation to Phase 3 — "produce tier-shape AND pace-layer-shape drafts" — should now be revised to "produce tier-shape AND pace-layer-shape AND trust-topology-shape drafts, and treat the cut between them as a user decision (D-class)."

### 8.4 What would falsify this track specifically

- If OQ-D2 (operator legibility at scale) cannot be satisfied without imposing layer or tier structure on the graph — in which case trust-topology degenerates to one of the other two and the off-list claim collapses.
- If the cycle-detector (S4) cannot run cheaply enough that S5 trajectory capture's cost-budget swallows it — in which case the architecture violates D-5 (cost ceilings).
- If the M4 reconciliation mechanism (OQ-D5) cannot be specified without operator-only intervention at every conflict — in which case lights-out cannot hold for mixed-mandate operation.

### 8.5 The single most important sentence in this report

The corpus admits **at least three** defensible unified architectures (tier, pace-layers, trust-topology). The A+C convergence at *one* of these was substantially the brief's candidate-list working as a soft prompt; it was *also* substantially the F-mode severity gradient working as honest signal. **Both are true; the audit's "mixed verdict" was correct; this track is the empirical confirmation that the third axis exists.**

---

*End of unified-D-off-list.md.*
