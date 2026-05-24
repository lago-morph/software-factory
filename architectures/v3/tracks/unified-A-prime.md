---
based-on-commit: 5c4deeb
based-on-date: 2026-05-24
track: unified-no-axis-A-prime
axis: verification-topology (judge-graph + ground-truth provenance) as primary; mandate as a derived view via ground-truth source
mandate-scope: both
prior-track-superseded: unified-A
---

# Track unified-A-prime — The Verification-Topology Factory

## §0. Axis declaration, prohibition acknowledgment, glossary, and pre-response

### 0.1 Chosen axis: verification topology (judge-graph + ground-truth provenance)

**Primary organizing axis.** The factory is organized around the **verification topology** — the graph of who/what produces ground truth, who/what closes the loop on each artifact, and how *independence* between producer and verifier is mechanically established. Concretely the axis has three typed properties per work item:

1. **GT-source** — where the ground truth comes from for *this* cycle: `scenarios-out-of-tree` / `existing-tests-in-tree` / `production-traces` / `invariant-pack` / `human-ratified-spec` / `none-yet` (cold-start).
2. **Judge-graph shape** — `none` / `same-model-different-role` (Anthropic Auto-Review per CTR-D7) / `cross-model-pair` (`kevin`/`carl` per F46) / `cross-vendor-triad` / `deterministic-perimeter` (CaMeL-class) / `human-in-loop`.
3. **Closure rule** — what *closes* the cycle: `gate-passed` / `holdout-mediator-clears` / `escrow-elapsed-without-objection` / `human-ratifies`.

A work item's verification topology is **declared at intake** (not classified by stakes/risk). The mandate determines only *which GT-sources are available* (greenfield: invariant-pack + scenarios + cold-seed priors; brownfield: existing-tests + production-traces + invariant-pack-extracted-from-codebase). The same architecture runs for both.

### 0.2 Acknowledgment of the prohibition, and defense of this axis as the strongest remaining alternative

**Prohibited axes (Phase-2 axis-divergence audit, [`axis-divergence-audit.md`](../bias-guards/phase-2/axis-divergence-audit.md)):** tier-based / risk-tier / stakes-tier / blast-radius (used by unified-A and unified-C — flagged contaminated by F57's tier-presupposing definition + brief OQ-B7's named-list bias + missing-FM audit's "stakes / risk tier" language); Brier pace-layers (used by unified-B).

**Why verification topology is the strongest remaining axis:**

1. **It is the corpus' deepest unresolved cleavage.** Five of the eight CTR-D contradictions (CTR-D3, D4, D5, D7, D8, plus D1's F36/F37 collision-now-resolved) sit on judge-graph questions. The corpus' deepest substrate-vendor (Anthropic, via Husain/Shankar) and the corpus' deepest harness-practice voice (CJ Hess `kevin`/`carl`) *empirically disagree* about whether judge-model independence is necessary. No track has yet made this the primary axis; A and C absorbed it as a *property of tier*; B absorbed it as a *property of layer*. The corpus signal points here as much as it points at tier.

2. **It dissolves CTR-A1 / CTR-A4 (lights-out vs. L5) without smuggling tier-classification.** Lights-out is permitted exactly when the verification topology *can close the loop without a human*. That is a structural property (judge-graph + closure-rule), not a stakes property. The CodeRabbit 1.4× / Veracode 45% / METR 19% empirics (CTR-E3) become an *attack on specific judge-graph shapes* (single-LLM review; no holdout-mediator; no cross-model critic), not a blanket anti-L5 claim. This is the same logical move A/C make at the tier layer, but performed at the layer where the empirics were actually measured.

3. **It engages MISSED-3 (El Kaim invariants vs. UC4 spec-malleability) without resorting to tier or pace-layer.** The invariant-pack is a GT-source; spec-malleable artifacts are work-items whose GT-source is *the invariant-pack* + scenarios — they are reversible at the artifact layer because the verification topology re-runs cheaply. Invariants are non-negotiable not because they sit at a higher layer or a higher tier, but because *no other GT-source can override them in the closure rule*.

4. **It honors UC4's mandate-difference at the right grain.** UC4 says greenfield is spec-malleable, brownfield is code-archaeological + existing-architecture-as-given. Under verification-topology, this becomes a difference in *which GT-sources are populated*: greenfield bootstraps with `invariant-pack` + `cold-seed-scenarios` + `none-yet`; brownfield bootstraps with `existing-tests` + `production-traces` + `invariant-pack-extracted`. The architecture is the same; the GT-source distribution differs. This is the substrate-heavy / thin-methodology pattern (CTR-C2) made concrete *without* a tier classifier.

5. **It engages CTR-D4 / D7 / D8 head-on by making judge-graph a first-class declaration, not a derived setting.** The Husain/Shankar finding (same-model-different-role is fine) and the `kevin`/`carl` finding (cross-model is necessary) are both *true* — for different judge-graph shapes. They were contradictory only under the implicit assumption that there is one judge-graph; once judge-graph is a typed declaration per work item, both findings ship.

6. **It is genuinely competitive with tier and pace-layer on corpus citations.** Per-axis citation count (lead-agent tally of `both-primary`/`both-secondary` reports directly load-bearing on the axis): tier-axis ≈ 8 (reports 09, 31, 32, followup 10, 12, F44/F56/F57 mode-cluster). Pace-layer axis ≈ 4 (followup 12, reports 14, 35, F34). Verification-topology axis ≈ 9 (reports 11, 18, 23, 28, 34, 38, followup 07, 08, 11; F1/F27/F33/F44/F46/F48/F51 mode-cluster; CTR-D1..D8 contradictions). The corpus does not point uniquely at tier — it points at *several* defensible axes, and verification-topology has the broadest cross-cutting support among them.

**Why not the other candidates:**
- *Substrate-vs-methodology* (lead-agent stance): answers boundary-question, not shape-question. Verification-topology decides *which side of that boundary each judge-graph primitive lives on*, which is more discriminating.
- *Work-unit-class (D2 taxonomy)*: shape-based, not closure-based. Each class has a typical verification topology; topology is the deeper variable.
- *Regime (Jaymin Augmentation vs. Automation)*: regime is *derived* from verification topology (Automation-eligible iff judge-graph + closure-rule can close without human). Making regime primary forces a tier-shaped classifier; making topology primary lets regime fall out.
- *Knowledge-accumulation strategy*: a substrate property under any axis; not shape-giving on its own.
- *Language-as-harness*: F45 is real but mostly affects single substrate selection; not architecture-axis sized.
- *Dotfile-pipelines-as-product* (report 27): a strong candidate; honored in this track as the *intake-time declaration mechanism* (the `.dot` file declares the work item's verification topology) — but the pipeline-as-data is a mechanism, not the organizing axis.

### 0.3 Verdict on unified-possibility (under the prohibition)

**Unified case is genuinely possible** under verification-topology. The same architecture serves both mandates; the substrate primitives are mandate-agnostic; the methodology differs only in *which GT-sources the intake stage marks available* and *which judge-graph shape is the default for a given GT-source-set*. The hypothesis UC4 ("no single architecture works best for both") is **partially falsified** — falsified for the unified shape; preserved for per-cell mandate-fit (D2 matrix), where the GT-source-distribution per mandate × work-unit-class still favors one mandate's defaults.

**Honest falsification check:** if the corpus genuinely forced tier-classification (the F57 framing), I'd have to admit defeat. It does not. F57's mechanism *describes* tier-classification as the operative scheme but cites G6 (El Kaim governance attribution) which is itself about design-authority erosion — *erosion of who closes the loop*, not erosion of tier boundaries. Reframed without F57's presupposition, the failure mode is naturally a verification-topology drift (the closure rule loosens; the judge-graph collapses to single-LLM). F57 is *more naturally* a verification-topology failure than a tier-classification failure. **The corpus pointed here; F57's framing pulled the early tracks toward tier.**

### 0.4 Pre-response to Phase-3 unified-mandate-attacker

**Attack A (against greenfield):** *"At cold-start, GT-source is `none-yet` for everything. Your verification topology collapses to `human-in-loop` for every cycle. You haven't built a unified architecture; you've built a tautology: 'lights-out when verification works.'"*

Pre-response: §5 cold-start treats GT-source as **deliberately seeded, not absent**. The invariant-pack is populated from operator-curated priors (report 25 EARS+GtWR templates; report 14 El Kaim 9-field intent blocks; followup 10 AILCCP governance controls). Cold-seed scenarios come from adjacent-domain exemplars + report 26 prompt-underspecification academic empirics. The first ~N cycles run with a `cross-model-pair + invariant-pack + escrow-elapsed-without-objection` topology — that's lights-out under a deliberately *over-built* verification graph, which graduates downward as cycles accumulate (production-traces become available; existing-tests come into being). The architecture does not require GT-source to magically appear; it requires the operator to declare what counts as ground truth at day 0, which is exactly what the brief §5 mandates.

**Attack B (against brownfield):** *"Brownfield's `existing-tests` are a Veracode-45%-style mess — they're the very GT-source that's already been measured as failing. Your topology trusts them and inherits the rot."*

Pre-response: existing-tests are *one* GT-source, never the sole one — the judge-graph for brownfield T-bumping work declares at least `existing-tests-in-tree + production-traces + invariant-pack-extracted` and the closure rule requires *consensus* across them. CTR-B5 (scenarios outside vs. inside codebase) is resolved by **Holdout Mediator** brokering which signals are visible to which agent — D-2 fragility flagged for brownfield is converted into a substrate primitive, not papered over. Where the brownfield codebase has no usable existing-tests, the architecture *declines* lights-out for that subsystem (the verification topology cannot close; regime falls to L4 by structural necessity, not by tier).

**Attack C (the philosophical one):** *"Verification topology is just risk-tier in different vocabulary — production-touch GT-source = high tier, sandbox GT-source = low tier. You're contaminated too."*

Pre-response: the cleavage is real. Tier-axis classifies *the work* by potential consequence; topology-axis classifies *the verification graph* by structural properties. The same work item can have multiple legitimate verification topologies (e.g., a refactor can be verified by existing-tests OR by scenarios OR by cross-model critique); tier-axis assigns one answer. The same verification topology can serve work items of vastly different stakes (e.g., `cross-model-pair + invariant-pack` serves both a T0 sandbox cycle and a T3 production cycle if the GT-sources are populated). The axes overlap statistically (high-stakes work tends to demand richer topology) but they are not the same axis — and the *architectural primitives* the two axes demand differ: tier-axis demands a classifier; topology-axis demands a topology-declaration parser + a mediator. **No tier classifier appears in this track.**

### 0.5 Glossary (track-local vocabulary)

| Term | Meaning |
|---|---|
| **Verification topology** | The 3-tuple (GT-source-set, judge-graph-shape, closure-rule) declared per work item at intake. |
| **GT-source** | A typed source of ground truth: `scenarios-out-of-tree` / `existing-tests-in-tree` / `production-traces` / `invariant-pack` / `human-ratified-spec` / `none-yet`. |
| **Judge-graph** | The directed graph of judge agents (nodes) and judging relationships (edges) for a cycle. Shapes are typed (see §0.1). |
| **Closure rule** | The substrate-enforced condition that ends a cycle. Always one of a fixed enum. |
| **Holdout Mediator** | Substrate primitive (S2) brokering GT-source visibility — which agent sees which signal under which topology. Resolves D-2 / CTR-B5. |
| **Topology declaration** | A `.topo` artifact (per work item, version-controlled) inspired by report 27's `.dot`-as-product framing. Declares (GT-sources, judge-graph, closure-rule). |
| **Invariant pack** | The El Kaim 9-field intent block + AILCCP controls + GtWR rules. A GT-source, not a tier. |
| **Topology graduation** | The transition (per work-unit-class, per codebase) from a richer to a sparser topology as evidence accumulates that the sparser one suffices. Substrate-mediated; trajectory-captured. |

---

## §1. The architecture in one paragraph

The factory is a **substrate-heavy stack** whose central primitive is the **Topology Declaration Parser** that ingests a per-work-item `.topo` artifact and configures the cycle: which GT-sources the Holdout Mediator exposes, which judge-graph shape the Judge Router instantiates, and which closure rule the Cycle Closer enforces. The same substrate (sandbox, trajectory capture, watchdog, cost ceiling, Holdout Mediator, Judge Router, Cycle Closer, Topology Parser, Topology Graduation Ledger) runs both mandates. Mandate determines only (a) which GT-sources Intake populates at bootstrap, (b) the default judge-graph priors per work-unit-class. Methodology is thin: cycles are dispatched against a topology declaration; agents build; judges judge per their declared graph; the closer closes per its declared rule; trajectory is captured; the graduation ledger accumulates evidence about which (GT-source-set, judge-graph) pairs reliably close lights-out. The architecture is the same for greenfield and brownfield; the data flowing through it differs.

## §2. The five core substrate primitives

### S1 — Topology Declaration Parser
- **Role:** Reads the `.topo` artifact (one per work item; checked into the repo alongside the work item; report 27 `.dot`-as-product framing). Validates the declared (GT-sources, judge-graph, closure-rule) against the substrate's allowed enums. Rejects topology declarations that the substrate cannot enforce (e.g., declaring `none-yet` GT-source with `escrow-elapsed-without-objection` closure is rejected — no signal to escrow against).
- **Mandate behaviour:** identical.
- **Anchors:** report [`27`](../../research/27-dotfile-pipelines-as-product.md) (dotfile-pipelines-as-product); report [`18`](../../research/18-openai-codex-substrate.md) (`.rules` Starlark DSL — same family of substrate-DSL primitive).
- **F-modes addressed:** F50 (typed-object architecture/spec confusion — `.topo` is typed); F51 (Ashby-deficient guard — substrate rejects under-specified topologies up front rather than letting an LLM-judge mis-classify under requisite-variety pressure).

### S2 — Holdout Mediator
- **Role:** Brokers which GT-source signals are visible to which agent under which topology. Builder agents never see holdout GT-sources directly; judge agents see only the GT-sources their declared role requires.
- **Mandate behaviour:** identical; what differs is *which* GT-sources are routable (greenfield: scenarios + invariant-pack; brownfield: + existing-tests + production-traces).
- **Anchors:** Round-2 D-4 (holdout discipline as substrate primitive); CTR-B5 / WEAK-3 (brownfield-scenarios-inside-codebase fragile-default — resolved here by mediation rather than location).
- **F-modes addressed:** F2 (reward hacking — builder cannot see holdout); F27 (circularity — judge cannot see builder's GT-source if same-model topology); F60 (parallel-cycle compounding — mediator throttles holdout exposure across parallel cycles).

### S3 — Judge Router
- **Role:** Instantiates the declared judge-graph shape: `none` / `same-model-different-role` / `cross-model-pair` / `cross-vendor-triad` / `deterministic-perimeter` / `human-in-loop`. Per CTR-C4 resolution: declares provider-property requirements (model-family diversity, long-context, vision) per shape; does NOT prescribe a single router-as-substrate (sidesteps OpenHands-RouterLLM-vs-profile dispute). Cross-vendor-triad explicitly requires three model families per F46.
- **Mandate behaviour:** identical.
- **Anchors:** F46 (single-model review blindspot); CTR-D4/D7/D8 (the corpus' three-way judge contradiction); report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5 (Anthropic Auto-Review = `same-model-different-role`); report [`34`](../../research/34-lenny-howiai-personal-harnesses.md) (CJ Hess `kevin`/`carl` = `cross-model-pair`); followup [`08`](../../research/followup/08-security-primitives.md) (CaMeL = `deterministic-perimeter`).
- **F-modes addressed:** F1 (hallucination loop); F27 (circularity); F33 (adversarial-prompt judge defeat); F46 (single-model blindspot); F48 (tacit collusion — declared-graph diversity bounds the failure surface).

### S4 — Cycle Closer
- **Role:** Enforces the declared closure rule. `gate-passed` (default for sandboxed cycles); `holdout-mediator-clears` (default when scenarios or production-traces are in the GT-source-set); `escrow-elapsed-without-objection` (cognitive escrow per report [`30`](../../research/30-cognitive-escrow.md) — interval is declared, not LLM-judged); `human-ratifies` (for `human-in-loop` graph shape, or for invariant-pack diffs).
- **Mandate behaviour:** identical.
- **Anchors:** report [`30`](../../research/30-cognitive-escrow.md) (cognitive escrow as interval-as-design-surface); F42 (cognitive escrow negligence).
- **F-modes addressed:** F42; F56 (Replit-class guardrail bypass — the closer is substrate-enforced, NOT instruction-shaped, so the failure mode that defeats prompt-level guardrails has no surface here).

### S5 — Topology Graduation Ledger
- **Role:** Trajectory-capture extended: records per (GT-source-set, judge-graph-shape, work-unit-class, codebase) cell the historical close-rate, escape rate, post-merge sample-audit verdict, and human-re-entry rate. Operators (not agents) propose graduations: "for work-unit-class X in codebase Y, topology Z has closed N times without human re-entry — propose graduating to topology Z' (sparser)." Graduation is **human-ratified**, never automatic. Anti-F57 by construction.
- **Mandate behaviour:** identical; the ledger fills differently per mandate (brownfield fills faster because existing-tests give more signal-per-cycle).
- **Anchors:** D-7 (trajectory capture); F57 (design-authority erosion — explicitly addressed: graduation requires explicit human ratification, the *opposite* of convenience-driven reclassification).
- **F-modes addressed:** F57 (the central design); F55 (loop-corruption — graduation ledger has out-of-distribution audit slots required at fixed intervals); F7 (normalisation of deviance — operator sees the graduation history).

**Shared substrate also consumed (mandate-agnostic, topology-agnostic):** sandbox; cost-ceiling enforcement (D-5); tiered watchdog Daemon/Triage/Patrol (D-6); secret store; coordination via git+GitHub-issues (CTR-C7); OTEL five-event export (report 18); `.rules` Starlark DSL.

## §3. How the loop runs (work-cycle walkthrough)

A work item arrives (from issue queue, scheduled task, or `.dot`-pipeline trigger per report 27):

1. **Intake.** Topology Declaration Parser (S1) reads the work item's `.topo` artifact. Validates against substrate enums. Rejects under-specified topologies (F51 mitigation: substrate is Ashby-adequate for the declared variety; topologies declaring more variety than the substrate can support are rejected at intake, not silently degraded).
2. **GT-source population.** Holdout Mediator (S2) determines which GT-sources are *available* for this codebase (mandate-derived) and *required* by the declared topology. Mismatch → topology rejected, work item flagged for re-declaration.
3. **Builder dispatch.** Cycle launches with builder agent(s) seeing only non-holdout context.
4. **Judge dispatch.** Judge Router (S3) instantiates the declared judge-graph. Per CTR-D4 / D7 / D8 resolution: shape is declared, not router-chosen; same-model-different-role is permitted (Anthropic Auto-Review) when GT-source-set excludes production-touch signals; cross-model-pair is required when production-traces are in the GT-source-set; cross-vendor-triad is required when invariant-pack diffs are in scope.
5. **Closure.** Cycle Closer (S4) evaluates the declared closure rule. Lights-out passes proceed; `human-ratifies` cycles route to a human queue.
6. **Trajectory + Ledger.** D-7 trajectory captured; Topology Graduation Ledger (S5) updates the cell for (this topology, this work-unit-class, this codebase).

**Regime mapping (CTR-A4 engagement):** lights-out runs whenever the closure rule resolves without human-in-loop AND the substrate's Daemon+Triage watchdog tiers do not escalate. Shapiro L4 (`human-in-loop`) and L5 (`gate-passed` / `holdout-mediator-clears` / `escrow-elapsed-without-objection`) are *substrate-mechanical* declarations of where the human sits, not regime classifications layered on top. CTR-A1 (L5-target vs. L5-anti-pattern) is resolved by recognising that the CodeRabbit / Veracode / METR empirics were measured on a specific (poor) verification topology — single-LLM review, no holdout, no cross-model critic. The factory's lights-out cycles run *richer* topologies than the ones in those studies.

## §4. §4 defaults: accepted vs. challenged

- **D-1 (specs as durable artifact):** **`accepted with justification`** — specs are one GT-source. Invariant-pack and intent-block specs (report 14) are durable; lower-layer specs are work-item artifacts. Both mandates.
- **D-2 (scenarios live outside codebase as holdout):** **`challenged`** — per CTR-B5 / WEAK-3. Resolved by Holdout Mediator (S2): location of GT-sources is mandate-and-topology-dependent; the *discipline* is substrate-enforced via mediation, not via physical location. Greenfield scenarios out-of-tree; brownfield includes in-tree existing-tests and production-traces brokered by the mediator.
- **D-3 (Agent = Model + Harness):** **`accepted with justification`** — builders and judges in this architecture are all Model + Harness. Population-shaped architectures (Tournament) are *allowed as a declared judge-graph shape*, but each population member is itself Model + Harness; the decomposition holds. CTR-C1 fragile-flag does not bite because populations sit *inside* the judge-graph declaration.
- **D-4 (holdout discipline substrate-enforced):** **`accepted with justification`** — central to this architecture; S2 Holdout Mediator is the named primitive.
- **D-5 (hard cost ceilings in CI):** **`accepted with justification`** — declared per topology; cross-vendor-triad costs more than `none` and the topology declaration carries the cost estimate.
- **D-6 (tiered watchdog substrate primitive):** **`accepted with justification`** — Daemon/Triage/Patrol exists regardless of topology; topology declaration sets the Patrol's drift-detection signal-set (which GT-source signals are watched for drift).
- **D-7 (trajectory capture cheap and production-tested):** **`accepted with justification`** — extended to the Topology Graduation Ledger (S5).

## §5. Cold-start (mandatory, per brief §5)

The greenfield cold-start question: how does a factory bootstrap on day 0 with no scenarios, no issue queue, no `docs/solutions/`, no prior runs? Required-reading inputs: reports [`25`](../../research/25-requirements-engineering-foundations.md), [`26`](../../research/26-prompt-underspecification-academic.md), [`30`](../../research/30-cognitive-escrow.md), [`31`](../../research/31-caremark-rsi-board-exposure.md), and followup [`10`](../../research/followup/10-governance.md).

### 5.1 Day 0 — deliberately over-built verification topology

The architecture's day-0 default topology for every cycle is **maximally over-built**: GT-sources = `invariant-pack + cold-seed-scenarios + human-ratified-spec`; judge-graph = `cross-model-pair + deterministic-perimeter`; closure rule = `human-ratifies` for cycles touching the invariant pack, `escrow-elapsed-without-objection` (interval = 24h) for everything else. This is the verification-topology analogue of A's cold-start tier-pinning, but the pin is on *topology shape*, not on tier.

### 5.2 Cold-seed GT-source population

- **Invariant pack** (slow-changing, human-ratified, GT-source for everything else): seeded from report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md) 9-field intent block + report [`25`](../../research/25-requirements-engineering-foundations.md) INCOSE GtWR R1–R35 rules + followup [`10`](../../research/followup/10-governance.md) AILCCP 37/48/43/10/18 control catalog + report [`31`](../../research/31-caremark-rsi-board-exposure.md) Kahana RSI three-part test (if RSI-relevant per operator declaration).
- **Cold-seed scenarios** (out-of-tree, brokered by S2): operator-curated from adjacent-domain exemplars; the report [`26`](../../research/26-prompt-underspecification-academic.md) empirics (Pass@1 98.7%→85.0% as specs scale; 73.8%→6.7% on contradictory prompts) inform the *minimum scenario count* — bootstrap requires ≥N scenarios where N is set such that F36 (Yang instruction-following ceiling) is bounded by chunking.
- **Human-ratified spec**: the day-0 spec is necessarily human-authored; downstream cycles operate under it.
- **Production-traces / existing-tests**: explicitly `n/a` for day 0; populated as the system runs.

### 5.3 Bootstrap-against-silent-failure (brief §5.2 question)

The Topology Graduation Ledger (S5) explicitly logs `none-yet` cycles. Until a topology cell has accumulated ≥M close-events without re-entry, S5 *forbids graduation* — silent failure is detectable because the ledger refuses to certify lights-out for any topology cell whose evidence base is thin. This is the structural answer to "the architecture has no track record yet to evaluate it against": the architecture *knows it has no track record* and structurally requires human ratification until the track record exists. The cognitive escrow interval (report [`30`](../../research/30-cognitive-escrow.md)) is the interval during which silent failure is *expected* to surface — escrow is the bootstrap-period silent-failure detector.

### 5.4 Trajectory day-0 → day-N

- **Day 0–~7:** every cycle topology = day-0 default (above). Closure mostly `human-ratifies`. Ledger fills.
- **Day ~7–~30:** topologies relax per-work-unit-class as Ledger evidence accumulates. First lights-out cycles (likely `regression-fix` + `refactor` classes) admitted when their cell has cleared the M-event bar AND post-merge sample-audit confirms zero high-severity incidents (Jaymin Automation-mode bar from report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5 applied to *the topology cell*, not the whole factory — OQ-B6 partial resolution).
- **Day ~30+:** steady-state. Different work-unit-classes graduate at different rates. The factory is *never* uniformly lights-out; it is lights-out *per topology cell that has earned it*.

### 5.5 Brownfield cold-start (the inverse problem)

Brownfield's day-0 problem is not absent GT-sources but *untrusted* GT-sources (Attack B in §0.4). The cold-start procedure is a **time-boxed Intake** that: (a) extracts an invariant-pack from the existing codebase using AFIS strategy-3 (report 25); (b) classifies existing-tests by trust level via test-quality heuristics (production-trace agreement, mutation testing sample); (c) catalogs production-trace availability and access controls. The Intake's output is itself a `human-ratified` artifact; lights-out cycles do not begin on the brownfield codebase until the Intake's outputs are human-approved. Where Intake produces low-confidence GT-sources for a subsystem, the architecture declines lights-out for that subsystem until Intake re-runs.

## §6. Mandate-fit per D2 work-unit-class

| Work-unit-class | Greenfield fit | Brownfield fit | Driver |
|---|---|---|---|
| `initial-spec` | both | both | GT-source = human-ratified-spec + invariant-pack; topology = `human-in-loop`. Same for both mandates by construction. |
| `refactor` | both | both-strong | GT-source set richer in brownfield (existing-tests + production-traces); topology graduates faster. |
| `mvp` | both-strong | both | Greenfield's natural class. Cold-seed scenarios drive verification. |
| `post-mvp-evolution` | both | both-strong | Brownfield's natural class. Production-traces are the load-bearing GT-source. |
| `regression-fix` | both | both-strong | Existing-tests + production-traces define ground truth structurally; brownfield's natural class. |

Architecture-fit is `both` for all five classes; mandate-fit "strength" varies by which GT-sources are typically populated.

## §7. F-mode coverage matrix (selected; full pass in Phase 3 merge)

| F-mode | Mitigation in this architecture | Mandate notes |
|---|---|---|
| F1 (hallucination loop) | Judge Router enforces declared judge-graph; cross-model-pair or higher required when GT-source-set lacks ground-truth signals. | Same for both. |
| F12 (lethal trifecta) | Topology declaration explicitly enumerates production-touch GT-sources; `deterministic-perimeter` (CaMeL-class) required in judge-graph when production-traces are GT-source. | Brownfield more often hits this; same primitive. |
| F27 (circularity) | Holdout Mediator (S2) prevents builder/judge GT-source overlap when same-model topology declared. | Same. |
| F33 (adversarial-prompt judge defeat) | F33 specific instance of F51; mitigated by S1 (substrate-rejection of under-specified topologies) + cross-vendor-triad requirement for sensitive GT-sources. | Same. |
| F34 (cross-layer drift) | Topology Graduation Ledger tracks invariant-pack diffs as a special signal; any cycle touching invariants forces `human-ratifies` closure. | Brownfield's invariant-pack-extracted is the riskier surface. |
| F44 (production-scissors default) | `deterministic-perimeter` is a substrate-supported judge-graph node; production-touch GT-sources cannot route without it. | Brownfield exposure higher; primitive same. |
| F46 (single-model review blindspot) | Judge Router refuses `same-model-different-role` when GT-source-set includes production-touch signals. | Same. |
| F48 (tacit collusion) | Judge-graph declaration must include model-family diversity for ≥2-node graphs touching production. F48/F49 bounded to topologies the architecture explicitly admits the failure-surface for. | Same. |
| F51 (Ashby-deficient guard) | S1 rejects topologies declaring more variety than the substrate enforces; the substrate's variety is the floor. | Same. |
| F55 (loop corruption from prior-runs) | Topology Graduation Ledger requires out-of-distribution audit slots at fixed intervals. | Greenfield more vulnerable; primitive same. |
| F56 (Replit-class guardrail bypass) | Cycle Closer is substrate-enforced, not instruction-shaped — Replit's bypass surface doesn't exist here. | Brownfield critical; substrate handles. |
| F57 (design-authority erosion) | **Central design** — Topology Graduation Ledger requires explicit human ratification for every graduation; convenience cannot reclassify. | Same. |
| F59 (premature decomposition) | Topology declaration does not require scout-spec-build separation; `.topo` admits implementation-discovers-spec patterns. | Greenfield high; primitive same. |
| F60 (parallel-cycle compounding) | Cost ceiling + Holdout Mediator throttle parallel exposure to the same GT-source. | Brownfield high. |
| F61 (context fragmentation across agents) | Judge-graph declaration is per-cycle (not per-fleet); fragmentation is a declared structural property, not emergent. | Same. |

## §8. Open questions, candidate ADRs, and Phase-3 attack surfaces

### 8.1 Open questions

- **OQ-Ap1.** What is the exact M-event graduation threshold per work-unit-class? Lead-agent placeholder: M=30 with zero high-severity incidents (Jaymin Automation-mode K=5 ≥90% applied to topology cells). *Next action: Phase-5 ADR on graduation thresholds; lean-eval brief to measure.*
- **OQ-Ap2.** Is the topology declaration parser itself an F51 Ashby-deficient guard? Mitigation: parser is deterministic and rejects on schema violation, never on semantic judgment. *Next action: Phase-5 ADR on `.topo` schema; lead-agent owns.*
- **OQ-Ap3.** How does the architecture interact with multi-codebase coordination (deferred per brief §7)? *Next action: out of scope; flag for v4.*
- **OQ-Ap4.** Where does F45 (language-as-harness) live? Lead-agent placeholder: a *property of the codebase*, declared at Intake, that modulates the cost ceiling and the judge-graph defaults. *Next action: Phase-5 ADR.*

### 8.2 Pre-response to Phase-3 adversarial personas

- **Skeptic:** "Your axis is judge-architecture in disguise; the brief literally named judge-architecture as a candidate." Response: judge-architecture is *part* of verification topology (the judge-graph leg); the axis is the 3-tuple (GT-source, judge-graph, closure-rule). Judge-architecture alone underspecifies; the GT-source leg is what makes mandate-fit fall out, and the closure-rule leg is what makes regime fall out. The brief naming judge-architecture is corpus signal, not contamination — the axis-divergence audit (§3.4) did not flag judge-architecture as a contaminated frame.
- **Historian:** "v2 architectures already varied judge architecture (Tournament's diversity-as-defense vs. Atelier's senior-reviewer-as-judge); this is renaming v2." Response: v2 *varied* judge architecture as a top-level architectural choice; this track makes it a *per-work-item declaration* under a unified substrate. The unification is in S1–S5; v2 had no Topology Declaration Parser, no Holdout Mediator, no Topology Graduation Ledger.
- **CFO:** "Cross-vendor-triad is expensive; the cost-ceiling will refuse." Response: cost ceiling is per-topology (D-5 fragility addressed); operators choose which topology cells to enable; OQ-Ap4 lives here. The architecture does not promise that *every* topology is affordable — it promises the cost is *declared and enforced*.
- **On-call:** "When a graduated topology cell regresses (post-merge sample-audit finds a defect), what happens?" Response: substrate-mediated topology *de-graduation* — the cell reverts to the previous (richer) topology automatically; the regression is logged; a Patrol-tier watchdog event escalates to the operator. CTR-A5 (brownfield ceiling) is engaged here: brownfield topology cells de-graduate faster because production-trace signal density is higher.
- **Naive newcomer:** "I don't understand why I should write a `.topo` file." Response: most work items inherit a default topology by class; the `.topo` is explicit only when overriding. The discoverability primitive (AGENTS.md per Round-2) carries the default-topology table for each repo.
- **Phase-3 unified-mandate-attacker:** see §0.4.

### 8.3 Candidate Phase-5 ADRs

- ADR: `.topo` schema (S1).
- ADR: Holdout Mediator interface (S2; resolves D-2 / CTR-B5).
- ADR: Judge Router shape enum + provider-property declarations (S3; resolves CTR-D4 / D7 / D8 / C4).
- ADR: Closure rule enum (S4).
- ADR: Topology Graduation Ledger schema + ratification protocol (S5; resolves F57 design-authority erosion).
- ADR: Cold-start over-built-topology default + day-0 GT-source seeding procedure (§5).
- ADR: Brownfield Intake protocol + Intake's GT-source-trust-classification (§5.5).

---

*End of unified-A-prime.md.*
