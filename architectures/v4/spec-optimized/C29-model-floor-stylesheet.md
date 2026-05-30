# C29 — Model floor & stylesheet routing  (Spec, Track B)

> Source: README.md Part 4 P6 (183–191 "Cross-family enforcement … Custom policy on the model stylesheet … Gas City model stylesheet rule"), Phase-1 build (420–442 "rule in Gas City model stylesheet — judge node must use different model family than coder node"), OSS-table Fabro row (304 "CSS model stylesheet is the transfusion target"); AI-CONTEXT.md §4.1 (139–145 Max auth, "No separate API key issued"), §4.2 (149–153 Agent-SDK June-15 credit), §6.2 (260–262 Fabro CSS-like cost-aware model stylesheet, "Strongest v4 transfusion target"), §6.3 (266–268 Kilroy `model stylesheet + --force-model + modeldb`), §7 Layer-2 table (304 "Cross-family enforcement | None | DIY | Custom model stylesheet rule"), §12 open questions (514 "specific Gas City model stylesheet syntax for judge != coder"), §14 risk register (624 "Claude Code Max policy changes … have API-key fallback path ready"); F-MODE-COVERAGE.md §6 F19 (71 "Model-floor dependency … Addressed (by declaration)"), F31 (73/148 "Substrate safety floor = weakest adapter … Addressed (by single-adapter choice)"), §1 F1/F27/F46/F48 (hallucination loop / circularity / single-model review blindspot / tacit collusion); component-inventory.md C29 row (Agent Loop, component, foundational, maps A11b/A106/B84, depends C28, gaps G08/G20/G32); _meta gaps G08 ("model family" undefined; cross-family vs single-adapter tension), G20 (judge model unsourced — no provider/budget/auth), G32 (cost essentially unmodeled).
> Inventory ID: C29   Kind: component   Status: sweep-1
> Deltas: DELTA-01 (**`model-family` is a *first-class declared registry field with an explicit independence axis*, not an undefined word** — resolves G08 by defining family as "shared-weights lineage" and adding an orthogonal `independence_class` so cross-family policy is checkable, not hand-wavy); DELTA-02 (**cross-family rule generalised to a configurable `judge_independence_policy` with graded enforcement levels L0–L3**, because the strict "different provider" reading has *no satisfiable path under Max* — Track B confronts this head-on; **per ruling D-1 the L1 same-provider default is the Phase-0 baseline and L2/L3 cross-family/cross-provider are future-enhancement FE-1**, with this graded policy serving as the FE-1 `judge_family` seam); DELTA-03 (**explicit credential-path proposal for a second judge family** — the metered-API "judge seat" — turning G20 from an unsourced gap into a costed, gated dependency C29 owns the policy hook for); DELTA-04 (**routing is a compiled, deterministic decision function with a conformance/lint pass**, not loose CSS text — selectors, cascade, and the floor clamp are version-pinned and testable; closes the F19/F31 "by declaration" loophole); DELTA-05 (**cost-tier becomes a *live budget-aware* input** wired to C28's seat governor and C46's cost stream — the stylesheet routes on *measured remaining budget*, not a static tier label, addressing G32 at routing time); DELTA-06 (**fail-closed-by-default with an auditable `degraded_eval` escape valve** — when no compliant judge family is registered, satisfaction-measuring dispatch is refused unless an operator explicitly accepts a named, logged degradation, so F27/F46 cannot be silently un-addressed).

## 1. Purpose & responsibility

C29 is the factory's **model-selection policy engine**: the single deterministic authority that, given a workflow node, decides **which concrete model/adapter that node runs on**, subject to two hard constraints — a **capability floor** (no coder runs below Claude Code @ Max) and a **judge-independence policy** (the satisfaction judge must be sufficiently independent of the coder). It fuses two v4 ideas the inventory binds to one ID, and Track B sharpens each:

1. **Model floor (A106 / B84 / F19 / F31).** v4 *declares* Claude Code @ Max as the capability floor. Track B keeps the declaration but makes it **enforced**: the floor is a clamp in a compiled decision function plus a conformance gate (co-owned with C28 DELTA-06), so "floor by declaration" becomes "floor by test" (DELTA-04).
2. **Stylesheet routing (A11b, Fabro/Kilroy).** A **CSS-like, cost-aware** rule set — selectors over node attributes → a target model, with cascade/specificity — transfused from Fabro's CSS model stylesheet (AI-CONTEXT §6.2) and Kilroy's `--force-model`/`modeldb` registry (§6.3). Track B compiles it to a deterministic, lintable function (DELTA-04) and makes its cost input *live budget* rather than a static label (DELTA-05).

Onto this engine v4 hangs the **cross-family enforcement rule** ("judge.family ≠ coder.family", README:189/427). Track B's central move (DELTA-02/03) is to confront the fact that **this rule has no satisfiable path under Max** — the only sanctioned coder is Claude, and Max issues no second-provider key — and replace the binary rule with a **graded, configurable independence policy plus a concrete second-family credential path**.

**Responsibility:** for any node, **resolve `{adapter, model, family, cost_class}`**, guaranteeing (a) coder nodes never below floor, (b) judge nodes satisfy the configured independence level against the coder, (c) resolution is deterministic, lintable, and attributable, and (d) when (b) is unsatisfiable, dispatch **fails closed** (DELTA-06) unless an explicit, logged degradation is accepted.

**It is explicitly NOT:**
- **Not the agent loop (C28).** C29 *selects*; C28 *runs the turn*. C28 consumes a `model_selection` from C29 per invocation. The two co-design the selection contract (§3a).
- **Not the LLM client / provider transport.** OAuth/HTTP/LiteLLM transport is the client layer (README:119) under C04/C28; C29 names *which* model, not how bytes move.
- **Not the judge (C32) or holdout enforcement (C34).** C29 supplies and *constrains* the judge's model identity and emits the independence constraint; C32 scores, C34 enforces read-isolation. C29 owns the *family-independence* half of the cross-family requirement; C34 owns *data*-independence (holdout). (ID-mapping note: the "cross-family enforcement" cell README:189 is split — *model-family* independence → C29; *holdout/read* isolation → C34. Same C-IDs, clarified seam.)
- **Not the cost meter (C46).** C46 owns cost-per-satisfaction *measurement*; C29 *consumes* a live budget signal to route (DELTA-05) but does not compute the satisfaction cost model.
- **Not a secrets manager.** C29 *declares the requirement* for a second-family credential and the gate that blocks dispatch without it (DELTA-03); the secret store itself is a security-substrate concern (G37, deferred).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Depends on | **C28** Claude Code agent loop | The floor adapter; coder model. C29 declares C28 as floor, routes coder nodes to it, and reads C28's `AgentLoopProvider` conformance result so it never selects a sub-floor adapter (DELTA-04). C29 also reads C28's seat-governor utilization for live cost routing (DELTA-05). |
| Depends on | **C03** Config/feature-flags | The stylesheet + `model_registry` + `judge_independence_policy` level are layered TOML under C03; section presence gates whether routing/independence enforcement is active. |
| Depends on | **C46** Meta-metrics (cost stream) | Supplies live remaining-budget / cost-per-class signal that the cost-tier selector reads (DELTA-05). At Phase 0/1, before C46 exists, the input degrades to a static tier label (graceful). |
| Consumed by | **C32** Judge harness | Inventory: C32 depends on C29. The judge reads its constrained, independence-checked model identity from C29. |
| Consumed by | **C34** Holdout integrity | Reads C29's family-independence verdict as one input to its overall isolation audit (the other input is read-partition, C42). |
| Consumed by | **C05** Sling/dispatch; **C12/C13** formula/molecule nodes; **C28** agent loop | Every node that runs a model resolves `{adapter, model}` through C29 at dispatch; C28 receives it as `model_selection`. |
| Writes to | **C23** Event bus / **C41** attribution | Each resolution emits an auditable record (node, winning rule, model, family, independence verdict) so routing is reconstructable (DELTA-04/06). |
| Hard tension with | **C32 / C34** (cross-family) | The load-bearing G08/G20 tension: cross-family presumes a non-Claude family; the floor is a single Claude-only adapter with no second key (AI-CONTEXT §4.1). DELTA-02/03 confront this directly (§6/§9). |

Placement: **Agent Loop** subsystem (C28, C29), Batch 1/2 of the build order — foundational, started once C01/C03 shape is fixed, co-designed with C28.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete CSS grammar, the registry JSON schema, the cascade-specificity algorithm, and a Mermaid resolution sequence land in sweep 2). The defining Track-B move is that selection is a **compiled deterministic function over typed inputs** (DELTA-04), not a text policy interpreted ad hoc.

### 3a. `resolveSelection(node, ctx) → ModelSelection` — the selection contract

Inbound `node`: `{ role (coder|judge|tool|diagnose|…), stage, formula_id, required_family?, attrs… }`. Inbound `ctx`: `{ coder_selection? (for judge nodes), live_budget (from C46/C28, DELTA-05), independence_policy_level }`.
Outbound `ModelSelection`: `{ adapter, model, family, independence_class, cost_class, floor_satisfied: bool, independence_verdict, winning_rule_id }`.

Pre/post:
- **Pre:** the `model_registry` is loaded and every referenced model has a `family` + `independence_class` + `cost_tier`. Lint (DELTA-04) rejects a stylesheet referencing an unregistered model.
- **Post (I1, floor):** `role=coder ⇒ floor_satisfied ∧ capability(model) ⩾ capability(floor)`. A rule resolving a coder below floor is **clamped to floor** and the clamp is logged.
- **Post (I2, independence):** `role=judge ⇒ independence_verdict satisfies judge_independence_policy` against `ctx.coder_selection` — else dispatch **fails closed** (DELTA-06).
- **Post (I3, determinism):** same `(node, registry, stylesheet, policy_level)` ⇒ identical `ModelSelection` (auditable/lintable, like all v4 deterministic rules).

### 3b. `model_registry` — the `modeldb`-shaped catalog (DELTA-01)

Per model: `{ id, adapter, family, independence_class, cost_tier, capability_rank, status (conformance-passed|candidate|disabled) }`.
- **`family`** = *shared-weights lineage* (e.g. `claude-3.x`, `gpt-4.x`). This is the concrete definition G08 leaves undefined (DELTA-01). Two checkpoints of the same base model are the *same* family.
- **`independence_class`** = orthogonal axis answering "how independent of the coder is this validator?": `same-family` (different prompt, same weights) < `cross-family-same-provider` < `cross-provider`. Cross-family policy is expressed against *this* axis, not a vague word.
- **`capability_rank`** = the floor comparator basis (I1). Floor pin = the Claude-Code@Max entry's rank.

### 3c. `judge_independence_policy` — graded enforcement (DELTA-02)

A single configured level (C03 TOML) the judge resolver enforces:

| Level | Requirement on judge vs coder | Satisfiable under pure Max? | When used |
|---|---|---|---|
| **L0 `off`** | none | yes | bootstrap/dev only; satisfaction numbers marked untrusted |
| **L1 `prompt-independent`** | same family, *disjoint context + different rubric/persona* (no shared conversation) | **yes** | Phase 0/1 default — the only path that runs with zero second-provider credential |
| **L2 `cross-family`** | `independence_class ⩾ cross-family-same-provider` | only if a 2nd family is registered | **FE-1 (future)** — when a second Anthropic-or-other family is available |
| **L3 `cross-provider`** | `independence_class = cross-provider` (the literal README:189 reading) | only with a 2nd-provider key (DELTA-03 seat) | **FE-1 (future)** — the strong-isolation eval tier; not a Phase-0 requirement (D-1) |

This is the **head-on confrontation** the brief demands: the literal v4 rule is **L3**, which is **unsatisfiable under Max alone**. C29 makes the level explicit and **defaults to L1**, the strongest *satisfiable* level under the Max floor, while keeping L2/L3 reachable the instant a second-family credential exists (DELTA-03). The factory therefore *always* runs at a defined, honest independence level instead of either lying ("L3 addressed") or silently routing judge=coder.

> **Ruling D-1 / FE-1 (adopted).** The integrator's decision **D-1** ratifies this: the **Phase-0 baseline is the same-provider judge** — **L1 is the correct Phase-0 default** (holdout integrity comes from rig partitioning + role/prompt isolation, not family diversity). The **cross-family (L2) / cross-provider (L3)** judge is **future enhancement FE-1** (`_meta/FUTURE-ENHANCEMENTS.md`), **not a Phase-0 requirement**. The graded-policy seam (L0–L3) + the judge-seat credential hook (DELTA-03) is exactly the clean `judge_family` seam FE-1 asks for, so L2/L3 can be switched on later without re-architecture. L2/L3 remain spec'd but are flagged FE-1, not blocking.

### 3d. `requireJudgeFamily()` / credential gate (DELTA-03)

For L2/L3, C29 exposes a gate: a satisfaction-measuring formula requesting L≥2 must resolve to a registry entry whose adapter has a **valid second-family credential** (the proposed **metered-API "judge seat"** — a small pay-as-you-go API key used *only* for judge tokens, never the Max OAuth token, isolated per AI-CONTEXT §4.1's "OAuth never leaves Claude Code"). If absent, the gate triggers DELTA-06 fail-closed. This converts G20 from "unsourced" into a **named, costed, isolatable dependency** with a single enforcement point.

### 3e. Outbound constraint emitters
- **`crossFamilyConstraint(coder) → IndependenceConstraint`** — consumed by C32/C34; carries the active policy level + the required `independence_class`.
- **`floorDeclaration`** — the invariant asserting the single sanctioned floor adapter (backs F19/F31), now paired with the C28 conformance result (DELTA-04).

## 4. Data model / state

C29 owns **config artifacts**, not per-run mutable state; resolution is a pure function of `(node, registry, stylesheet, policy_level, live_budget)`.

| Datum | Shape (sweep-1) | Owner | Notes |
|---|---|---|---|
| Stylesheet | ordered `(selector, declaration)` list, compiled to a decision function | C29 | layered TOML under C03; compiled + linted (DELTA-04) |
| `model_registry` (`modeldb`) | `{id, adapter, family, independence_class, cost_tier, capability_rank, status}` | C29 | family + independence_class resolve G08 (DELTA-01) |
| `judge_independence_policy` | one of L0–L3 | C29 (set via C03) | default **L1** (DELTA-02) |
| Floor pin | `claude-code@max` id + capability_rank | C29 | F19/F31 declaration, conformance-gated (DELTA-04) |
| Judge-seat credential ref | handle/alias only (never the secret) | C29 declares; secrets store owns | DELTA-03; absence ⇒ fail-closed for L≥2 |
| Resolution record (emitted, not stored) | `{node, winning_rule_id, model, family, independence_verdict, clamp?}` | → C23/C41 | makes routing auditable (DELTA-04/06) |
| `live_budget` (read-through) | remaining cost / per-class budget | C46/C28 supply | static fallback label when absent (DELTA-05) |

## 5. Behavior

Resolution at node dispatch (sweep-1 prose; Mermaid sequence + cascade algorithm in sweep 2):

1. Node arrives with attributes (role, stage, formula_id, …).
2. Match selectors → collect declarations → **CSS-cascade by specificity** → candidate model.
3. **Cost selection (DELTA-05):** among floor-or-above candidates, pick the cheapest class that meets the node's capability need, reading `live_budget`; if budget is tight, downshift within the allowed band (never below floor for coders).
4. **`role=coder`:** clamp to floor (I1); log any clamp.
5. **`role=judge`:** look up `ctx.coder_selection.family`; evaluate `independence_verdict` against `judge_independence_policy` (§3c). For L≥2, run the credential gate (§3d). If the level is unmet:
   - **fail closed (DELTA-06):** refuse dispatch and emit a `judge_unroutable` record — *unless* the formula carries an explicit, operator-signed `degraded_eval` acceptance, in which case route at the highest satisfiable level (≥L1), mark the resulting satisfaction scores `independence_degraded`, and log the named acceptance. (This is the auditable escape valve, not a silent fallback.)
6. Emit the resolution record (C23/C41); return `ModelSelection` to dispatch (C05) / agent loop (C28) / judge (C32).

**Degraded flows:**
- *No second family registered, policy=L1 (default):* normal operation; judge runs prompt-independent same-family; scores trusted at L1.
- *Policy=L3, no judge-seat credential:* fail-closed; satisfaction-measuring dispatch refused; surfaced to operator (the honest "you asked for cross-provider but have no second provider" signal).
- *C46 budget stream down:* cost selector falls back to static `cost_tier` labels (DELTA-05 graceful degradation); floor + independence invariants unaffected.

## 6. Failure modes & handling

| F-mode | Source | C29 (Track-B) handling | Status |
|---|---|---|---|
| **F19** Model-floor dependency | FM §6:71 | Floor is a *compiled clamp + C28 conformance gate* (DELTA-04), not just a sentence | Addressed (by test, strengthened) |
| **F31** Substrate floor = weakest adapter | FM §6:73,148 | Any adapter must be `conformance-passed` in the registry before it can win a coder rule; the floor is the *enforced* minimum | Addressed (single-/conformed-adapter) |
| **F1** Hallucination loop | FM §1 | Judge-independence policy (≥L1) breaks builder==validator self-confirmation | Addressed at active level |
| **F27** Circularity (same-model build+validate) | FM §1 | `judge_independence_policy` is the guard; fail-closed (DELTA-06) prevents silent judge=coder | Addressed at L≥1; **honest about the L1 ceiling** |
| **F46** Single-model review blindspot | FM §1 | Independence axis enables judge ensembles across `independence_class` | Addressed when L≥2 family available |
| **F48** Tacit collusion via shared context | FM §1 | L1 already forbids *shared context* (disjoint conversation), not just same model; L≥2 adds weight independence | Partial→stronger (L1 closes the context-sharing leg; shared-training residual remains until L2/L3) |

**The load-bearing tension confronted (G08 + G20) — explicit DELTA.** v4's literal cross-family rule ("judge must be a *different model family*", README:189/427) is **L3 (cross-provider)** and is **unsatisfiable under Max alone** because (a) the only sanctioned coder is Claude and (b) Max issues no second-provider API key (AI-CONTEXT §4.1). Faithful Track-A handling could only "emit the constraint and fail closed." Track B resolves the contradiction three ways at once:

1. **Relax the requirement into a graded policy (DELTA-02).** L1 (`prompt-independent`, same family, disjoint context, different rubric) is the **strongest independence level satisfiable on the pure-Max floor** and becomes the default. This is an honest, runnable guard against F1/F27/F48's *context-sharing and prompt-coupling* failure legs — which are the legs a single subscription can actually defend — while being explicit that it does **not** defend the *shared-weights* leg.
2. **Propose a credential path (DELTA-03).** A metered-API **judge seat** (a tiny pay-as-you-go key used only for judge tokens, credential-isolated from the Max OAuth token) unlocks L2/L3. C29 owns the gate that requires it; the cost is small because judges run on cheap models over short trajectories and only at eval time. This is the concrete answer to G20.
3. **Scope the eval tier accordingly (DELTA-06).** Satisfaction scores are *tagged with the independence level that produced them* (`L1`/`L2`/`L3`/`independence_degraded`). The promotion gate (C50) and meta-metrics (C46) can then *require* L≥2 for high-stakes promotions while permitting L1 for routine in-loop checks — the eval tier's trust is scoped to its actual independence, not asserted uniformly.

This turns F27/F46 from "Addressed (on an impossible premise)" into "Addressed at a *declared, satisfiable* level, with a costed upgrade path and tagged trust."

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Cost (G32) — addressed at routing time (DELTA-05).** v4's only anchor is "$200/month Max" with no cost model. C29 carries a `cost_tier` per registry entry *and* reads C46/C28's live budget so routing prefers the cheapest floor-or-above option and downshifts under budget pressure. The judge-seat (DELTA-03) is the one new spend line; because it is metered and judge-only, C29 can cap it per formula. The *cost-per-satisfaction* model itself stays C46's; C29 supplies the routing lever and the per-resolution cost class. (G32 partially closed here, fully owned by C46.)
- **Security.** The judge-seat credential is the only second-provider secret; it is referenced by handle only and isolated from the Max OAuth token (AI-CONTEXT §4.1). C29 *requires* it via the gate but does not store it (G37 — secrets store deferred; the *requirement and isolation rule* are specified here).
- **Scale.** Routing cheap classes off the floor (DELTA-05) directly relieves the single-Max-seat ceiling (G34, fully owned by C28's seat governor) by not spending floor capacity on work that does not need it.
- **Observability.** Every resolution emits an auditable record (winning rule, model, family, independence verdict, clamp) to C23/C41 — routing decisions are reconstructable and the active independence level is queryable per satisfaction score.
- **Ops.** Stylesheet + registry + policy level are version-pinned config (C03); the compile+lint pass (DELTA-04) is a CI gate; changing independence level (L1→L2) is config + a registered judge family, not a rebuild.

## 8. Acceptance criteria & test strategy

Sweep-1 (high level; concrete cascade/grammar/registry-schema cases in sweep 2):

1. **Floor clamp (I1, DELTA-04).** A stylesheet placing a sub-floor model on a coder node resolves to the floor and logs the clamp; an adapter not `conformance-passed` can never win a coder rule.
2. **Graded independence (I2, DELTA-02).** With policy=L1 and only Claude registered, a judge node resolves successfully (same family, disjoint context, distinct rubric) and the score is tagged `L1`. With policy=L3 and no second-provider entry, the judge node **fails closed** (`judge_unroutable`) — not judge=coder.
3. **Credential gate (DELTA-03).** A formula requesting L≥2 with no valid judge-seat credential is refused at the gate; supplying the credential + a registered cross-family entry makes the same formula resolve and tags the score `L2`/`L3`.
4. **Degraded escape valve (DELTA-06).** A formula with an operator-signed `degraded_eval` acceptance routes at the highest satisfiable level, tags scores `independence_degraded`, and the acceptance is logged; absent the acceptance, dispatch is refused.
5. **Determinism (I3).** Same `(node, registry, stylesheet, policy)` twice ⇒ identical `ModelSelection`; the resolution is replayable from the emitted record.
6. **Cost routing (DELTA-05).** Given two above-floor candidates, the cheaper is selected when budget is tight; with the C46 stream absent, the static `cost_tier` fallback selects the same way without violating the floor.
7. **Tagged trust (DELTA-06).** Every satisfaction score carries the independence level that produced it, and C50/C46 can filter on it.

## 9. Open questions (→ review-log)

- **OQ-1 (RESOLVED by D-1 for Phase-0; residual for FE-1):** Is **L1 `prompt-independent` (same-weights, disjoint-context) judging trustworthy enough** to gate routine in-loop satisfaction? **D-1 rules yes for Phase-0:** the same-provider judge is the baseline (L1 default), with holdout integrity from rig partitioning + role/prompt isolation. L2/L3 are **FE-1**, not Phase-0 — so the judge-seat (DELTA-03) is **not mandatory** for Phase-0. Residual (FE-1 trigger): the minimum independence level per high-stakes decision class is revisited when a second-provider credential path exists or same-family bias is measured as material.
- **OQ-2 (DELTA-03, G20/G37 — deferred to FE-1):** Is a metered-API **judge seat** compatible with the project's "no second API key under Max" posture, and where does its credential live (secrets store is G37, unspecified)? Per **D-1/FE-1** this is **not a Phase-0 question** — the seat is the FE-1 cross-provider path; its admissibility gates L2/L3, which are future. Revisit with FE-1.
- **OQ-3 (DELTA-01, G08):** Is **`independence_class = cross-family-same-provider`** (e.g. a hypothetical second Anthropic family) materially more independent than same-family, or does shared training distribution collapse L2 toward L1 (the F48 "shared-distribution residual")? Determines whether L2 is a real tier or just L1 with extra cost.
- **OQ-4 (DELTA-04, C28 seam):** The floor `capability_rank` comparator depends on C28's conformance suite (DELTA-06 there). The two specs must agree on the capability metric so "⩾ floor" is well-defined — co-design item with C28.

> [DELTA-01]…[DELTA-06] indexed in the header. ID mapping: C29 keeps its single ID; the README:189 "cross-family enforcement" cell is *split by concern* — model-family independence (C29) vs holdout/read isolation (C34) — with no new IDs introduced.
