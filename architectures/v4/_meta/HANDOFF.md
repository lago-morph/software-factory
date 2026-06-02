# HANDOFF — v4 Spec & Plan run (resume from here)

**Last updated:** 2026-06-02 (Sweep-2 spine run #2 merged to `main`; **triangle evaluation invariant adopted — ADR-0069 / D-42 — now the TOP next task; see §0★**).
**Status:** **Sweep-1 COMPLETE** (57/57). **Sweep-2 STARTED**: run #1 (PRs #229–#233, all merged to `main`) delivered the D-23 protocol+harvest, the adversarially-reviewed prevent-gate decision (now **operator-ADOPTED — D-30**, both morning-review items closed), and the evidence/data-substrate depth cluster (C19/C20/C21/C23/C41). **NEXT RUN: author Sweep-2 implementation-ready depth for the 25-component safe-self-build spine, unattended, Gas City + Claude Max integration FIRST.**
**Working tree:** everything through PR #243 is in `main` (the full 25-component spine at Sweep-2 depth). (Historical run reports/prompts now live under [`archive/`](../../../archive/README.md).)

## 0★. NEXT RUN — TOP PRIORITY: implement the spec–scenarios–system triangle (ADR-0069 / D-42)

> Canonical statement: [**ADR-0069**](../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md). Ledger: **D-42** ([review-log.md](./review-log.md)). This is the **#1 next task**, ahead of "Sweep-2 for the remaining 32 components." The eval tier as currently specced is structurally incomplete: it models the judge as a *scorer*, and the operator has established that the judge must be a *diagnostician* over a three-representation triangle. **Read the intent below before touching any spec — the mechanics only make sense in light of it.**

### 0★.1 Why this is the load-bearing task (intent — do not skip)

The factory's purpose is to build components **for itself, unattended**. The hard part is **trust without a human in every loop**. If the agent that writes a component also writes the checks that bless it, the blessing is self-referential — it grades its own homework. The triangle is the structural decomposition that makes the grading independent and the failures diagnosable; **it is the precondition for unattended operation**, not an evaluation nicety.

Every build is **three representations** that must be made to agree:

- **Spec (S)** — what the component must do.
- **hold-out Scenarios (H)** — independent descriptions of using the spec'd system.
- **implemented System (I)** — the built component **and its own unit/integration/e2e tests**.

…joined by **three edges, each verified by a different party with a different trust property**:

| Edge | Must hold | Verified by | Independent of the implementer? |
|---|---|---|---|
| **S ↔ H** | scenarios correctly + completely describe use of the spec'd system | scenario builder **with** spec builder | authoring-side (both) |
| **S ↔ I** | the system faithfully implements the spec | the system's **own** unit/integration/e2e tests | **No** — implementer-written, **gameable** |
| **H ↔ I** | hold-out scenarios pass against the system | the **judge**, evaluated independently | **Yes** — the **anti-gaming check** |

The judge measures **only H↔I**, and a failure there is a **non-specific alarm** — the defect can live in any corner: the **judge** (mis-running/misinterpreting), the **spec** (ambiguity/incompleteness/contradiction), the **scenarios** (incomplete/misrepresenting/ambiguous/contradictory vs the spec), or the **system** (fails the spec; its own tests wrong for the same reasons). The judge's job is to **attribute the root cause** and **recommend a repair mode**:

- **incremental fix** — converge the three representations in place (localized defect); or
- **discard + reimplement** — fix the spec and/or scenarios via the **independent authoring path**, throw away the system, rebuild from the revised spec (structural defect: the system faithfully built the *wrong target*).

**Completion = all three edges aligned.** 100% hold-out pass is *necessary, not sufficient*. The integration bar is 100% hold-out pass **+** tri-alignment **+** human review; the **100% floor never lowers** — what relaxes as the judge earns calibrated trust is the human-review/judge-trust **oversight**, not the pass rate. Because the judge is itself a defect source, **judge calibration** (a human-audited sample before its verdicts are trusted) is a first-class, standing requirement.

### 0★.2 What to change (mechanics — deepen in place, preserve Sweep-2 content)

1. **C32 (judge) — scorer → diagnostician.** Keep `satisfaction_score` (the H↔I signal) + `score_label`. ADD a diagnosis output: (a) per-scenario **misalignment** detail (which scenario(s), and the observed-vs-expected gap); (b) a **root-cause attribution** across `{judge, spec, scenario, system}` with rationale; (c) a **repair_recommendation** ∈ `{incremental_fix, discard_and_reimplement}` with justification. **Contract care:** the `ScoreRecord` is D-39-frozen — add the diagnosis either as *additive optional* fields (bump the bead-type version) **or** as a companion `DiagnosisRecord` keyed to the `ScoreRecord`, so C33/C34/C46 keep consuming cleanly. The seam adversary must verify no downstream breakage.
2. **C53 (go/no-go) — completion = tri-alignment.** `decide()` consumes: (a) **100% hold-out pass** (the H↔I gate at its strictest — every scenario `satisfied`), (b) the judge's **tri-alignment diagnosis** (no unresolved spec/scenario/judge defect), (c) the **human-review** verdict, (d) the **post-deploy factory-integrity** check (does the factory still work after the new component is integrated?). `go` iff all hold. The satisfaction distribution becomes **diagnostic evidence, not the threshold knob**. `MilestoneConfig`: pass-rate pinned at 100%; the relaxable knobs are oversight + the judge-trust precondition. (This realizes `auto-002` option C′ as one edge of the triangle.)
3. **C52 (self-bootstrap) — fail-branch → repair router**, keyed on the judge's attribution + recommendation: judge defect → recalibrate judge, re-eval; system defect vs sound spec → **polish** (patch system + its own tests), re-eval; scenario defect → route to **independent scenario correction** (C30 + spec builder), re-eval; structural spec defect → route to **independent spec correction** (C08/C11), **discard system + reimplement from revised spec**. **Invariant:** spec/scenario correction is performed by the independent authoring path, **never the implementing worker** (this is the anti-gaming property — without it, "fix the spec" becomes "weaken the spec until my output passes"). Bounded attempts (C52:OQ4) + human escalation on exhaustion still apply.
4. **C30 + C08 — correspondence, independence, and the test-kind distinction.** C30: state the **S↔H correspondence duty** (scenarios correctly + completely describe the spec'd system's use), authored by the scenario builder **with** the spec builder in an authoring rig independent of the worker (D-38). C08: state the spec-quality properties the triangle needs (unambiguous, complete, non-contradictory — the very defect classes the judge attributes) and that spec correction runs through the independent authoring path. **Both:** make explicit the distinction now missing from the specs — **in-system tests** (unit/integration/e2e; implementer-written; enforce S↔I; gameable; part of the build deliverable) **vs the hold-out** (C30; independent; enforces H↔I; anti-gaming).
5. **C34 (holdout integrity) — confirm/extend** that it is precisely what makes H↔I a valid anti-gaming check (worker cannot read/author the hold-out), and that the **independent spec/scenario-correction path is also outside the worker's reach**.
6. **Ledger + brief.** D-42 + ADR-0069 are recorded. Update `auto-002` to frame its gate as the H↔I edge within the larger tri-alignment completion criterion. Record any new cross-component contract (e.g., the `DiagnosisRecord` shape) as a numbered ledger decision.

### 0★.3 Scope note — the independent authoring path (capability-bar discipline)

The natural home of the "independent spec/scenario correction" is the **intent crucible (C11)** + **EARS linter (C10)** + scenario authoring (C30). **C10/C11 are non-spine** (not in the 25). Do **not** build the full intent crucible in this pass. Instead: spec the triangle's *contracts* (the judge diagnosis output, the repair router, the independence requirement) and **name the independent-spec-correction path as a seam** to C08 + the future C10/C11, pulling in only the minimal interface needed. This keeps the change disciplined (new capability tied to the triangle invariant; no speculative machinery).

### 0★.4 How to run it (conventions + verification)

Deepen in place per the [Sweep-2 dispatch addendum](./SWEEP2-DISPATCH.md) (depth bar, E/AC codes, verbatim-D-citation, the Mermaid `;`-in-label hazard). **Validate every diagram with the validator tool, not a type-grep.** Suggested wave: (1) **C32 diagnostician first** — it is the keystone and defines the diagnosis contract the others consume; (2) then **C52 router + C53 tri-alignment + C30/C08 + C34** in parallel, pre-briefed with C32's diagnosis-output contract; (3) a **per-product seam adversary**; (4) a **cross-product integration pass** over C32/C52/C53/C30/C08/C34 (the lesson from run #2 — per-cluster reviews miss two-cluster seams); (5) PR. The seam adversary must field-level-verify the `ScoreRecord`/`DiagnosisRecord` contract against every consumer (the run-#2 `satisfaction_score`-vs-`score_value` blocker is the cautionary tale).

## 0. NEXT RUN — Sweep-2 implementation depth for the 25-component spine (LONG, UNATTENDED)

> **✅ §0 DONE — Sweep-2 spine run #2 closed 2026-06-02** (PRs #237–#243, stacked, open for review). All **25 spine components are at Sweep-2 implementation-ready depth**, Gas City + Claude Max first. New cross-component ledger decisions **D-31..D-41** (multi-rig per city; rig-spelling file-split; XC-7/CapabilityDescriptor; command/cmd; C09-vars-from-C05/C13-out; eval-tier CXDB-out + post-hoc scoring + separate judge rig + ScoreRecord-frozen; factory_build status-transition; + 4 panel-found integration fixes). Morning summary at [`overnight-summary.md`](../../../overnight-summary.md); panel verdict at [`panel-sweep2/VERDICT.md`](./panel-sweep2/VERDICT.md); retro at [`retrospective/2026-06-02-242.md`](../../../retrospective/2026-06-02-242.md).
> **CARRIED FORWARD (the next run + the next dispatch prompt MUST pick these up):** (1) **OPERATOR SIGN-OFF OWED** on the C53 first-self-build go/no-go rule shape — decision brief [`auto-002`](./decisions/auto-002-c53-go-no-go-rule-shape.md) (recommend option C′); (2) the **empirical D-23 spike is still owed** (needs Docker) — it gates the unattended face + whether the D-30 watcher is built; (3) **Sweep-2 for the remaining 32 non-spine components** is the next authoring work; (4) adopt the **cross-product integration pass** discipline (retro skill `SKILL-SPEC-de22c313ca` + agents-rule `AGENTS-MD-759e9a22cc`) — it caught 4 build-breakers the per-cluster reviews missed.
>
> The text below was the brief for run #2 (now complete) — kept for context.

> Read this whole §0, then [`STATUS.md`](./STATUS.md), [`review-log.md`](./review-log.md) (ledger D-1..D-30 + harvested OQs = the work list), and **the build order [`implementation-dependencies.md`](../implementation-dependencies.md)** (the authoritative 25-component spine + the 7 products + per-product dependency edges). Do **NOT** read the four v4 source docs into primary context — subagents read targeted sections.

### 0.1 Binding safety gate — D-30 (operator-adopted; DO NOT relitigate)

Unattended operation (P2) / self-modification (P3b) requires the substrate to **BLOCK (prevent at the tool-call/process boundary)** — not merely detect — out-of-boundary access on the relevant blast-radius face. If Gas City does not prevent natively (per the [D-23 spike](./D-23-gas-city-spike-protocol.md)), a **blocking enforcement watcher WILL be added** — sanctioned in principle, but its **DESIGN is deferred until the spike confirms it's needed** (don't design what we may not need; it still passes the bar when built). Until prevention is established, unattended is **blocked**. Per-rig-class autonomy is available but secondary. Full text: [auto-001 brief §Operator adoption](./decisions/auto-001-detect-only-binding-gate.md) + [review-log D-30](./review-log.md). Already annotated on C43/C34/C42/C56/C57.

### 0.2 Scope: the 25-component spine, in product order (Gas City + Claude Max FIRST)

The spine is **25 components across 7 products** (authoritative list + the bold backbone IDs are in [`implementation-dependencies.md` §"The backbone"](../implementation-dependencies.md)). Product build order, and the order to DEFINE them this run:

1. **Gas City (adopt)** — delivers 11 of the 25: **C01, C02, C03, C04, C05, C17, C18, C19, C23, C41, C42**. The "integration" deliverable = the concrete install+config recipe (`city.toml`/`pack.toml`/`.gc/site.toml`), grounded in the working **`lago-morph/gascity-prototype`** (clone it; read its `docs/PLAN.md` + README — the sandbox plumbing, Go 1.26.3 build, `[[rig]]` shapes, etc. are already proven there and harvested in [`D-23-substrate-harvest.md`](./D-23-substrate-harvest.md)), PLUS the **Gas City conformance check** = run the [D-23 spike protocol](./D-23-gas-city-spike-protocol.md) (the prevent-vs-detect / `[[service]]` / Orders-durability tests). **This is the piece the operator starts implementing tonight — define it to the deepest, most actionable detail first.**
2. **Claude Code / Max (adopt) + model-floor (custom)** — **C28** (the `claude` worker under Max that Gas City drives) + **C29** (cost/family routing policy). The **Claude Max integration** deliverable = the provider preset + auth/session plumbing (the `gascity-prototype` proves the sandbox path: `CLAUDE_CODE_OAUTH_TOKEN`, CA-bundle, `IS_SANDBOX=1`, the onboarding-dialog pre-acks) + C29's routing policy. **Second priority — the operator also wants to start this tonight.**
3. **In parallel after Gas City:** **Spec intake** (C08 spec format, C09 prompt binding), **Bead-type schema** (C20 — already at Sweep-2 depth from run #1; refine its seams).
4. **Evaluation tier** (Inspect AI): **C30** scenario store, **C31** runner, **C32** judge scorer, **C33** score reduction.
5. **The fence** (custom, gated on D-30): **C34** holdout integrity, **C43** boundary-typing half (needs only C42; can pull forward). **Bootstrap**: **C51** transfusion predicate, **C52** self-bootstrap, **C53** bootstrap-validation milestone (the apex).

"Everything in, or that needs to be defined for, the spine" = author each spine component to implementation-ready depth, AND define any non-spine dependency a spine component needs (e.g. C24 bridge for CXDB if a spine component reads trajectories).

### 0.3 First actions, in order

1. Ground from §0 + the named docs. Lean HEAVILY on subagents from the start.
2. **Gas City product to implementation depth FIRST** (the 11 components as a single integration product + the conformance check). Land it as its own stacked PR. This unblocks the operator's tonight work.
3. **Claude Code/Max product** (C28 + C29) to implementation depth — its own stacked PR.
4. Then products 3→5 above, one cluster per stacked PR, each closed by a **cross-cluster seam adversary** before integrate.
5. The empirical **D-23 spike is owed** (it decides whether the D-30 watcher is actually built) — run it when a Docker-capable env exists; it does **not** block defining the components.

### 0.4 Depth bar per component (Sweep-2 = implementation-ready)

Concrete signatures, data schemas, API/message/**config** contracts, sequence/state diagrams (Mermaid, valid `stateDiagram-v2`/`sequenceDiagram`), error taxonomies (E-codes), concrete acceptance tests (AC-codes cross-referencing the E-codes). **Use the [C20 spec](../spec/C20-bead-schema.md) as the format exemplar** (per-type field tables Field/Type/Req/Semantics/R-W-by; ownership annotations; E↔AC cross-refs). Deepen **in place** — preserve Sweep-1 content + `[D-23 substrate-verified]` + `[D-30 ADOPTED]` annotations + inline OQs. For Gas City + Claude Max also produce the concrete **integration runbook** (install/config/auth, grounded in the prototype). Cite binding decisions (D-1..D-30) **verbatim**.

### 0.5 Method & unattended discipline (this is the "context is precious" part)

- **Context is precious.** Read only what §0 names; never read the four v4 source docs or a subagent's full output into primary context. Subagents **write deliverables to disk and return ≤15-line receipts**; the orchestrator owns ALL git and **commits + pushes every wave**.
- **Dynamic model choice:** **opus** for planning, decision briefs, and panel synthesis; **sonnet** for general authoring / review / integration. Make the call per task.
- **Standing briefs:** dispatch one builder per component at Sweep-2 depth using [`BUILDER-BRIEF.md`](./BUILDER-BRIEF.md); concurrency cap ~6–8; pipeline.
- **Adversarial review is real subagents, never inline-simulated.** Run a **cross-cluster seam adversary** per product/cluster (it caught a HIGH `event_id` build-breaker in run #1). Cross-component conflicts → record as numbered ledger decisions and propagate (the [`cross-component-decision-ledger`](../../../.claude/skills/cross-component-decision-ledger/SKILL.md) discipline).
- **Panel-of-experts review** (≥5 real adversarial personas, opus) when bringing together a large chunk or making a decision in the operator's absence.
- **Decision briefs** (2 rounds, ≥3 real adversaries each) for genuine operator-judgment forks — don't freeze; write the brief, pick a side, flag it as a morning-review item.
- **Stacked PRs** (operator-directed); at run close write a **plain-language** morning summary (per the [`human-scoped-deliverables`](../../../.claude/skills/human-scoped-deliverables/SKILL.md) skill — idea-first, corpus vocabulary, no hash IDs in body) + a `self-retrospective`.

### 0.6 What run #1 already delivered (context, don't redo)

D-23 protocol+harvest (XC-9/C42:OQ-4/C04:OQ-4 closed; 0 true contradictions); the prevent-gate decision now **adopted (D-30)**; the evidence/data-substrate cluster **C19/C20/C21/C23/C41** at Sweep-2 depth with seam fixes **D-26…D-29**. C20 is the exemplar; the rest of the spine is the new work.

This file + the other `_meta/` artifacts are sufficient to resume with zero re-grounding. Start with the run summary at [`run-summary.md`](../../../archive/PR-220-run-summary.md), the operator decision guide [`decisions-to-make.md`](../../../decisions-to-make.md), and the coverage ledger [`STATUS.md`](./STATUS.md).

---

## 1. Where we are: 57 of 57 built + reviewed + integrated, then wrapped up

**One canonical track** — `spec/` + `plan-faithful/`. `spec-optimized/` + `plan-optimized/` are frozen reference. Every component (C01–C57) has `spec/<ID>-<slug>.md` + `plan-faithful/<ID>-<slug>.md` + `spec/<ID>-<slug>.review.md` (**57 / 57 / 57**). All adversary verdicts across the run were **accept-with-fixes** (0 blockers, 0 needs-rework). The live per-component four-axis state (Built / Reviewed / Incorporated / iNtegrated) is in [`STATUS.md`](./STATUS.md) — all 57 are ✓ on all four.

Sweep-1 was produced in batches (build → adversary-review → integrator), each batch's cross-component findings recorded as ledger decisions **D-1..D-19** (+ XC-3 resolved). Detail in [`review-log.md`](./review-log.md).

**The wrap-up run (after Sweep-1 close) added:**
- **Operator decisions D-20…D-25** adopted and annotated across affected specs — see [`decisions-to-make.md`](../../../decisions-to-make.md) (plain-language) and §5 below. This **resolved every Sweep-1 morning-review item** (D-18, OQ-6, F54 — see §3).
- **Expert-panel review** of the whole corpus — [`VERDICT.md`](./panel/VERDICT.md) + five panelist opinions (`panel/01..05`). The panel's single headline: the whole plan is gated on **D-23** (verify Gas City's "native" claims against a real `gc` *before* building on them), and it argues D-23 should be a **binding go/no-go gate** on D-20, not just a noted spike.
- **Three human-facing guides** (kept in sync): the engineer guide [`architecture-guide-for-engineers.md`](../../../architecture-guide-for-engineers.md), the plain-English build order [`build-order-plain-english.md`](../../../build-order-plain-english.md), and the implementer build order [`implementation-dependencies.md`](../implementation-dependencies.md).
- **The implementer build order now leads with the safe-self-build backbone** (PR #224): the minimum 25-component vertical slice to a first human-reviewed self-build (rings 19→22→25), grouped into six implementation clusters, with a **product→components** table (one Gas City adoption discharges 11 backbone components), dotted-line soft deps, a top-10-next by cost/benefit, and the beads/Gas-City "one install, many components" clarification. Two graph corrections landed there: **C31 scenario-runner is required** (was missing) and **C43 splits per D-20** (boundary-typing now, twin half C44 deferred).
- A whole-57 **consistency pass** report (under `_meta/`) and **C46 dep-edge fix** (D-24).

## 2. The bar (operator's — still in force for every sweep)

> *"Does this addition give us MORE CAPABILITY tied to a specific 12-principle? Polish/hardening that does the same thing 'better' in a non-principle way → DROP. Genuine, low-effort custom code where some part of a principle could not be met without it → KEEP. Partial satisfaction by the existing software stack (Gas City + libraries like prometheus / scikit-learn / PyOD / opentelemetry / sigstore / Inspect AI / DSPy / LocalStack / etc.) counts — we don't add custom code to harden what the stack already does."*

When in doubt: DROP. Grounding + worked examples in [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md). This bar held across all 57 — Sweep 2/3 must keep applying it (don't let implementation-depth reintroduce dropped hardening).

## 3. Sweep-1 morning-review items — ALL RESOLVED by D-20…D-25

The three items the previous handoff said to "resolve first" are now closed:
- **D-18 (C43 split-sequencing)** — **ADOPTED as D-20**: the C43 **boundary-typing half** (needs only C42) is pulled forward as the mandatory precondition before any unattended run; the **twin-isolation half (C44)** is deferred. No longer provisional.
- **OQ-6 (C46 dependency edge)** — **resolved by D-24** (meta-metrics cost signal re-sourced; dep edge corrected).
- **F54 / OQ-C57-3 (objective-drift audit ownership)** — **resolved by D-21**: objective-drift is logged UNBUILT with a cheap human checkpoint while a person still reviews batches; an automated drift detector is a **required precondition for full lights-out** (not built yet — the loudest residual; see §7).

## 4. Passes still owed (next runs)

1. **Sweep 2 (implementation-ready) — the next work.** Concrete signatures, data schemas, API/message contracts, sequence/state diagrams (Mermaid), error taxonomies, concrete acceptance tests — re-enter every component. **First action: the D-23 Gas City reality-check spike** (prevent-vs-detect, Orders durability, `[[service]]` semantics) against a pinned `gc`; the panel wants a *detect-only* outcome to bind a re-evaluation of D-20, not just be noted (VERDICT §6, PF follow-ups).
2. **Whole-57 cross-batch integration drift pass** — integration was done per-batch; a final drift pass over the seams frozen "→ Sweep-2 joint freeze" (C12/C14/C15 loop-DOT encoding D-16; C42/C34/C32 judge read-surface D-17; C36↔C37 population seam; C38↔C39 / C48↔C55 / C46 dep-edge).
3. **Sweep 3 (exhaustive):** pseudocode/algorithms, skeletons, edge-case catalogs, perf/security/ops.
4. **Final cross-cutting pass:** whole-system consistency, critical-path/parallelism analysis, top-level README/index.

## 4b. How to resume (Sweep 2)

1. Read [`run-summary.md`](../../../archive/PR-220-run-summary.md), [`decisions-to-make.md`](../../../decisions-to-make.md) (D-20..D-25 in plain language), this file, then [`STATUS.md`](./STATUS.md) (coverage ledger) and [`review-log.md`](./review-log.md) (D-1..D-19 + ~196 harvested OQs — the OQs are the Sweep-2 work list). Skim [`VERDICT.md`](./panel/VERDICT.md) for the cross-cutting risk ranking + the PF-1..PF-3 follow-ups. Do **NOT** read the four v4 source docs into primary context — subagents do that.
2. **Start with the D-23 Gas City reality-check spike** (it gates the most: every "Native" claim, and whether D-20's fence actually *prevents*). The other operator decisions (D-20..D-22, D-24, D-25) are already adopted and annotated into the specs — do not relitigate.
3. Use the standing briefs [`BUILDER-BRIEF.md`](./BUILDER-BRIEF.md) + [`ADVERSARY-BRIEF.md`](./ADVERSARY-BRIEF.md) (single-track banners). Dispatch one builder per component at **Sweep 2** depth; concurrency cap ~8; pipeline; subagents persist to disk + return receipts; **primary owns all git**; commit+push every wave.
4. Each component's `spec/<ID>-*.md` already carries its Sweep-1 OQs inline + its `.review.md` (+ any D-20..D-25 annotations) — Sweep 2 starts from those, not a blank page.

## 5. Binding decisions (do not relitigate) — detail in [`review-log.md`](./review-log.md) + [`decisions-to-make.md`](../../../decisions-to-make.md)

**Sweep-1 ledger (D-1..D-19):** D-1 same-provider judge (cross-family→FE-1) · D-2 bundle-id namespace `softwarefactory.v4.{beads,trajectory,packs}` · D-3 C20 authors bead schemas / C22 mechanism · D-4 C20→C19 · D-5 C41 hash-chain over C23 · D-6 "canonical track" nomenclature · D-7 node-kind home=C12 · D-8 convoy→C05 / Order→C40 · D-9 F38 vocab-lint=C10 · D-10 modeldb=`{id,family,cost_tier}` · D-11 LangFuse traces-only seam · D-12 two-sink cross-refs · D-13 holdout C34(enforce+audit)/C43(lethal-trifecta) · D-14 G37(secrets)≠FE-3(signing) · D-15 satisfaction holistic (FE-5 deferred) · D-16 loop-DOT encoding=C12 · D-17 judge read-surface · D-18 C43 split-sequencing (**now adopted as D-20**) · D-19 methodology significance→C48 · XC-3 RESOLVED C39 owns G18 numeric policy.

**Operator wrap-up decisions (D-20..D-25 — ADOPTED 2026-05-31):** **D-20** fence (C43 boundary-typing) pulled to a P2 precondition before any unattended run · **D-21** objective-drift (F54) logged-unbuilt + cheap human checkpoint; automated detector required before full lights-out · **D-22** counterfactual replay (C49): ship the deterministic half, keep the LLM-step half experimental (G19 honesty) · **D-23** run the Gas City prevent-vs-detect reality-check spike (G11) as the first Sweep-2 action · **D-24** C46 meta-metrics dependency-edge wiring correction · **D-25** secrets deferred to first-credential + Unleash license version-pin.

## 6. Deferred capabilities (do not build) — detail in [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md)

FE-1 cross-provider judge · FE-2 portability contracts · FE-3 graduated-mandatory signing (needs G37) · FE-4 multi-seat pool · FE-5 enumerated per-criterion DoD — **resolved by D-15** (holistic satisfaction; revisit only when C46 needs per-criterion diagnosis). Each has a specific external trigger; none pending.

## 7. Key residual risks (carried into Sweep 2 + the C57 register)

- **G11** — every "Native" Gas City claim is still unverified against a real `gc`. **D-23 makes the reality-check spike the first Sweep-2 action**; the panel wants a *detect-only* outcome to bind a D-20 re-evaluation. Touches C01/C12/C13/C14/C18/C40 + the prevent-vs-detect OQ (C43/C34). The single highest-leverage unknown.
- **G31** — lethal-trifecta has a deterministic boundary-typing **design** (C43). **D-20 (adopted)** pulls the boundary-typing half forward as the P2 precondition, which closes the documented exposure window *if* the fence actually prevents (depends on D-23). The twin-isolation half (C44) is still future (the XC-8 exposure window narrows but does not vanish).
- **F54 — objective drift:** **D-21 (adopted)** — logged UNBUILT with a human checkpoint; the **automated detector is a required precondition for full lights-out** and is not built. Loudest residual after G31 on a self-modifying L5 factory.
- **G19** — counterfactual replay (C49): **D-22** ships the deterministic-slice half now, keeps full LLM-step counterfactual experimental + human-reviewed. v4's riskiest invention leaf.
- **G37** — no secrets store (owned by C03): **D-25** defers to first-credential need + pins the Unleash license version; blocks FE-3 signing; keeps several controls "detect not prevent".

## 8. Artifact map

**`architectures/v4/_meta/`:** META-PLAN · TRACK-CHARTERS · DOC-TEMPLATES · BUILDER-BRIEF · ADVERSARY-BRIEF · component-inventory (+ -A/-B raw) · ambiguities-and-gaps · **review-log** (D-1..D-19 + harvested OQs) · INTEGRATION-PASS-1 · SURVIVOR-PASS · FUTURE-ENHANCEMENTS · RUN-SCOPE-2026-05-31 (Sweep-1 scope) · **STATUS** (coverage ledger) · **panel/** (VERDICT + 5 opinions) · HANDOFF (this).

**`architectures/v4/`:** **implementation-dependencies.md** (build order — leads with the safe-self-build backbone) · README · AI-CONTEXT · F-MODE-COVERAGE · one-shot-specs-and-research · optimized-differences(+reviews). Frozen reference (do not author here): `spec-optimized/` + `plan-optimized/`.

**Repo root:** [`run-summary.md`](../../../archive/PR-220-run-summary.md) · [`decisions-to-make.md`](../../../decisions-to-make.md) (D-20..D-25 plain-language) · [`architecture-guide-for-engineers.md`](../../../architecture-guide-for-engineers.md) · [`build-order-plain-english.md`](../../../build-order-plain-english.md).
