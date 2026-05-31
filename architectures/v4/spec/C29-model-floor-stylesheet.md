# C29 — Model floor & stylesheet routing  (Spec, Track A)

> Source: README.md Part 4 P6 (lines 183–191), Part 4 OSS-table Fabro row (304), Phase-1 build (420–442); AI-CONTEXT.md §4.1 (Max auth), §6.2 (Fabro / CSS model stylesheet), §6.3 (Kilroy `--force-model` / `modeldb`), §7 Layer-2 table (304 "Cross-family enforcement: None / DIY / Custom model stylesheet rule"), §12 open questions (514 "specific Gas City model stylesheet syntax for judge != coder"); F-MODE-COVERAGE.md §6 F19 (71) + F31 (73), §1 F1/F27/F46/F48 (17/21/24/25); component-inventory.md C29 (maps A11b, A106, B84).
> Inventory ID: C29   Kind: component   Status: sweep-1
> Track: A (faithful). Two readings recorded under [AMBIGUITY] where v4 is contradictory; minimal elaborations flagged [FAITHFUL-FILL].

## 1. Purpose & responsibility

C29 is the **policy artifact + resolution rule** that decides *which concrete model* each workflow node runs on. It fuses two v4 ideas that the inventory binds to one ID:

1. **Model floor declaration (A106 / B84 / F19 / F31).** v4 *declares Claude Code under Max as the explicit capability floor* — the single sanctioned coder adapter. F-MODE-COVERAGE §6 marks F19 ("Model-floor dependency") and F31 ("Substrate safety floor = weakest adapter") **Addressed (by declaration / single-adapter choice)** precisely because there is exactly one adapter, so "the weakest adapter" and "the floor" are the same well-defined thing (FM:71,73,148).
2. **Stylesheet routing (A11b).** A **CSS-like, cost-aware model stylesheet** (transfusion target: Fabro's CSS model stylesheet, AI-CONTEXT §6.2 line 262) holds *routing rules* — selectors over node attributes → a chosen model, with cost-awareness. Onto this same stylesheet v4 hangs the **cross-family enforcement rule**: "judge node must use a different model family than coder node" (README:189,427; AI-CONTEXT:304,514).

**Responsibility:** given a workflow node (its role/attributes) and the stylesheet, **resolve the model to use**, while (a) never resolving below the declared floor for a coder node, and (b) enforcing the cross-family constraint between coder and judge nodes.

**It is explicitly NOT:**
- NOT the agent loop itself (that is C28 Claude Code agent loop) — C29 *selects the model*, C28 *runs the turn*.
- NOT the judge (C32) — C29 only supplies/constrains the judge's model identity; scoring is C32's job.
- NOT the cost *meter* (C46 meta-metrics owns cost-per-satisfaction measurement). C29 is *cost-aware at routing time* but does not compute the satisfaction cost model.
- NOT a model *provider/credential* manager — see §6/§9; the second-family judge provider is an unresolved upstream dependency (G20).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Depends on | **C28** Claude Code agent loop | The floor adapter; the coder node's model. C29 declares C28 as floor and routes coder nodes to it. |
| Depends on (effective) | **C03** Config/feature-flags | The stylesheet is layered TOML; section presence drives whether routing rules are active. `> [FAITHFUL-FILL]` — inventory lists only C28; C03 is the substrate config model all v4 artifacts ride on (README Part 4; inventory C03). Minimal because the stylesheet is "configuration on the Gas City model stylesheet" (README:191) and Gas City config is C03. |
| Consumed by | **C32** Judge harness | Inventory: C32 depends on C29. The judge node reads its constrained (cross-family) model identity from C29. |
| Consumed by | **C05** Sling/dispatch, **C12/C13** formula/molecule nodes | Every node that runs a model resolves it through C29 at dispatch. `> [FAITHFUL-FILL]` (placement) — README:191 says routing is "configuration on the Gas City model stylesheet"; the natural consumer is the dispatch path. |
| Tension with | **C32 / C34** (cross-family) | The load-bearing tension: cross-family requires a non-Claude family (G08/G20) while the floor is a *single* Claude-only adapter (F31, AI-CONTEXT §4.1 "No separate API key"). See §6 and §9. |

## 3. Interfaces / contracts (sweep-1: named + described)

- **`stylesheet` (data, inbound).** The CSS-like rule set: ordered (selector → declaration) rules. A *selector* matches node attributes (role=coder|judge|…, stage, model-family, cost-tier). A *declaration* names a target model (or a `--force-model`-style pin) and may carry a cost-tier preference. Fabro CSS-stylesheet shape (AI-CONTEXT §6.2) is the transfusion source; Kilroy contributes `--force-model` + `modeldb` (per-model registry) shape (§6.3). `> [FAITHFUL-FILL]` — v4 gives the *concept* and source patterns, not concrete syntax; concrete grammar is sweep-2.
- **`resolveModel(node) → modelIdentity` (rule, outbound).** Cascade/specificity resolution (CSS semantics) selecting the winning declaration for a node. Postcondition for a coder node: result ⩾ floor (never a model weaker than the declared Claude Code floor). `> [FAITHFUL-FILL]` — v4 says "floor" but not the comparison operator; "not weaker than floor" is the minimal reading of *floor*.
- **`crossFamilyRule(coderModel) → constraint` (rule, outbound).** Emits the independence constraint used by C32/C34 (README:189,427), carrying the **active judge-independence level**. The policy is *gradable*; the **Phase-0 default is `L1`** (same-provider judge, prompt/role/rig-isolated from the coder). The literal `family(judge) ≠ family(coder)` form (cross-family/cross-provider) is **advisory/relaxed at Phase-0 — active enforcement is FE-1** (see I2); the emitter is the clean FE-1 seam, not a Phase-0 fail-closed gate.
- **`floorDeclaration` (invariant, outbound).** Asserts Claude Code (Max) is the floor; this is what makes F19/F31 "Addressed by declaration" (FM:71,73).

**Key invariants:** (I1) coder nodes never resolve below floor; (I2) `family(judge) ≠ family(coder)` — **relaxed at Phase 0 per D-1/FE-1** (the same-provider judge is the Phase-0 baseline, isolated by rig partitioning + role/prompt rather than family diversity; the literal cross-provider form is FE-1 — see §6/§9); (I3) resolution is deterministic (same node + same stylesheet → same model) so it is lintable/auditable like other v4 deterministic rules (cf. F51 deterministic-first posture).

## 4. Data model / state

C29 owns the **stylesheet artifact** (version-controlled config, not runtime state) and a **model registry** (`modeldb`-shaped: known model identities, their *family* label, and cost tier). It owns no per-run mutable state; resolution is a pure function of (node, stylesheet, registry).

| Datum | Shape (sweep-1) | Owner | Notes |
|---|---|---|---|
| Stylesheet | ordered list of (selector, declaration) | C29 | layered TOML under C03; section presence = active |
| Model registry (`modeldb`) | `{id, family, cost_tier}` per model | C29 | family label is what cross-family compares (G08 — "family" undefined in v4; see §9) |
| Floor pin | `claude-code@max` identity | C29 | the declaration backing F19/F31 |

## 5. Behavior

Resolution flow at node dispatch:
1. Node arrives with attributes (role, stage, …).
2. Match selectors → collect declarations → CSS-cascade by specificity → winning model.
3. If `role=coder`: clamp to floor (I1).
4. If `role=judge`: **(Phase-0, D-1/FE-1)** route to a same-provider judge that is rig/role/prompt-isolated from the coder, emitting the active independence constraint; the literal `family(judge) ≠ family(coder)` cross-provider check is deferred to FE-1 and applies only when a second-provider family is registered (I2, relaxed).
5. Return model identity to dispatch (C05) / agent loop (C28) / judge (C32).

Sequence/state diagrams and the cascade-specificity algorithm are **sweep-2/3**; this sweep fixes only the named flow and invariants above.

## 6. Failure modes & handling

| F-mode | Source | C29's role | Status per v4 |
|---|---|---|---|
| **F19** Model-floor dependency | FM §6:71 | The floor *declaration* is C29's deliverable | Addressed (by declaration) |
| **F31** Substrate floor = weakest adapter | FM §6:73,148 | Single-adapter floor is well-defined *because* C29 declares one floor | Addressed (single-adapter) |
| **F1** Hallucination loop | FM §1:17 | At Phase-0 the active guard is the judge-independence policy at `L1` (prompt/role/rig-isolated same-provider judge); the cross-family strengthening is FE-1 | Addressed (at the v4 level per FM §1; Phase-0 mechanism = L1 isolation) |
| **F27** Circularity / same-model build+validate | FM §1:21 | Phase-0 guard (D-1) is **rig/role/prompt isolation** of the same-provider judge; the cross-provider `crossFamilyRule` is FE-1 | Addressed at Phase-0 isolation level (cross-provider strengthening = FE-1) |
| **F46** Single-model review blindspot | FM §1:24 | Cross-family ensembles enable the strongest form; deferred to FE-1. Phase-0 relies on prompt/role isolation | Partial at Phase-0 (full cross-family addressing = FE-1) |
| **F48** Tacit collusion via shared context | FM §1:25 | Cross-family rule contributes; v4 marks **Partial** (shared training-distribution residual) | Partial |

**Degraded behavior / the load-bearing tension (G08 + G20):** v4's cross-family rule presumes a *second model family* exists, but AI-CONTEXT §4.1 says Max issues *no separate API key* and the only sanctioned coder is Claude Code. So at the floor install there may be **no non-Claude family available to route a judge to**. Faithful handling: C29 *emits the constraint and the family registry*; **sourcing the second family is an upstream dependency (G20), not resolvable inside C29.**

> [AMBIGUITY resolution — D-1 / FE-1] The integrator's ruling **D-1** resolves this tension so the
> cross-family rule is **no longer an unsatisfiable Phase-0 blocker**: the **Phase-0 baseline is the
> same-provider judge** (holdout integrity comes from rig partitioning + role/prompt isolation, not family
> diversity). **The judge-independence policy is *gradable*, and its Phase-0 default is `L1` — a
> same-provider judge that is prompt/role/rig-isolated from the coder; cross-family and cross-provider are
> the stronger (deferred) levels.** D-1 confirms L1 is the correct Phase-0 default. (The frozen optimized
> sibling spells the same gradable ladder out as L0–L3, cf. `spec-optimized/C29-…` §3c — reference only;
> the canonical level set here is "L1 default, cross-family/cross-provider = FE-1".) The literal
> provider-level "judge.family ≠ coder.family" requirement (the README:189 reading) is reclassified as
> **future enhancement FE-1** (`_meta/FUTURE-ENHANCEMENTS.md`), revisited when a second-provider credential
> path exists. **Consequently `crossFamilyRule` (I2/A2) is advisory/relaxed at Phase 0, not fail-closed:**
> a same-provider judge that is *prompt/role/rig-isolated* from the coder is the sanctioned Phase-0 path; it
> does **not** silently un-address F27/F46 because the isolation is structural (separate rig + disjoint
> context), only the *family-diversity* leg is deferred to FE-1. C29 keeps the `family` registry field and
> the constraint emitter as the clean seam FE-1 switches on later.

## 7. Cross-cutting

- **Cost (G32).** v4's only cost anchor is "$200/month Max" (AI-CONTEXT §4.1); the stylesheet is "cost-aware" (Fabro, §6.2) but v4 gives **no cost model** for second-family judge tokens, multi-judge ensembles, etc. C29 carries a *cost-tier* on each registry entry so routing can prefer cheaper tiers, but the cost-per-satisfaction model is **C46's** and is **deferred** here (G32 noted, not resolved — see §9).
- **Security.** Second-family judge needs its own credential path; v4 has no secrets story (G37). Flagged, deferred to upstream/C-secrets.
- **Observability.** Resolution is deterministic → auditable; the chosen model should be recorded per node (ties to C41 attribution / C23 event bus). `> [FAITHFUL-FILL]`.

## 8. Acceptance criteria & test strategy (sweep-1, high level)

- A1: A coder node always resolves to a model ⩾ the declared floor (I1). *Test:* stylesheet with a sub-floor declaration on a coder node → resolution clamps to floor.
- A2: **(Phase-0, per D-1/FE-1)** A satisfaction-measuring judge runs same-provider but **rig/role/prompt-isolated** from the coder; the `family` constraint emitter is exercised but the cross-provider form is **not** required (FE-1). *Test:* a same-provider judge with a disjoint rig + distinct rubric resolves successfully; the emitted `IndependenceConstraint` records the active (Phase-0) level. *(The literal `family(judge) ≠ family(coder)` fail-closed test moves to the FE-1 cross-provider tier.)*
- A3: Resolution is deterministic and reproducible (I3). *Test:* same (node, stylesheet, registry) twice → identical model.
- A4: The floor declaration exists and is the single sanctioned coder adapter (F19/F31). *Test:* registry/declaration names exactly one floor adapter (Claude Code @ Max).
- A5: Cost-awareness is expressible: a node can prefer a cheaper tier among floor-or-above options. *Test:* two above-floor models, cheaper one selected when cost-tier preferred.

Concrete CSS grammar, cascade-specificity tests, and the model-registry schema are **sweep-2**.

## 9. Open questions (→ review-log)

- **[AMBIGUITY: G08 — RESOLVED by D-1/FE-1] "Model family" is undefined.** Reading (a): *family = provider* (Anthropic vs OpenAI vs Google) — implies a second provider, which AI-CONTEXT §4.1 forbids under Max. Reading (b): *family = training-lineage within a provider* (Claude-judge vs Claude-coder allowed). The two readings were left open because F27/F46/F48 want validator-from-builder independence while the Max floor forbids a second provider. **The integrator's ruling D-1 resolves it:** the **Phase-0 baseline is the same-provider judge** — effectively reading (b) for Phase 0, with independence supplied by **rig partitioning + role/prompt isolation** rather than family diversity. The provider-level reading (a) — the literal README:189 cross-provider requirement — is reclassified as **future enhancement FE-1**, not a Phase-0 requirement. C29 still stores `family` as a label so FE-1 can switch on cross-family/cross-provider judging later without re-architecture.
- **[G20 — RESOLVED by D-1/FE-1] The judge model is unsourced.** No named non-Claude provider, budget, or auth path exists in v4 (G20). Per **D-1**, this is **no longer a Phase-0 blocker**: Phase 0 runs the same-provider judge, so no second-provider credential is required to stand up the evaluation tier. Sourcing a second family/provider is **FE-1** (future), revisited when a second-provider credential path exists or same-family judge bias is measured as material.
- **[G32] Cost model deferred to C46.** C29 is cost-*aware* (tiers) but does not own the cost-per-satisfaction model; v4 provides none. Deferred with reason: cost measurement is C46's responsibility per inventory.
- Concrete stylesheet syntax for "judge != coder" is itself flagged as an open question in v4 (AI-CONTEXT §12, line 514) — resolved to a named rule here, concrete grammar at sweep-2.
