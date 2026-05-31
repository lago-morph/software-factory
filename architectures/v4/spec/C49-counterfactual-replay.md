# C49 — Counterfactual Replay Driver  (Spec, canonical track)

> Source: README §"Principle 12 — Self-optimization" capability table (line 274 "Counterfactual replay | Re-run from trajectory midpoint | **CXDB** O(1) branching | Apache 2.0 | **Bridge + driver**") + placement summary (line 278 "P12 is the most ambitious and the most research-flavored … the **driver is your most significant invention**. Build last, after Layers 1-5 are solid"); README §Part 6 Phase 1 (line 397 "CXDB substrate ready for P11 anomaly clustering and **P12 counterfactual replay**") + Phase 3d (line 470 "factory builds the meta-metric pack, the variant identification pack … the A/B routing pack …, **the counterfactual replay driver**. This is the **highest-risk layer; heaviest human review**"); AI-CONTEXT §5.5 (line 237 "**O(1) trajectory branching → counterfactual replay** essential for self-healing investigations and self-optimization variant tests"), §10 capability table (line 359 "Counterfactual replay | CXDB branching + driver | Apache 2.0 + DIY | **Primitive exists; driver yours**"; line 357 "Auto variant — methodology/topology | None | DIY | Research frontier"), §10 multi-capability table (line 375 "CXDB | … + **L6 counterfactual primitive** | Apache 2.0"), §10 exemplar list (line 423 "Counterfactual replay: **git cherry-pick mechanics, Temporal workflow replay (closest analogs; no LLM-specific exemplar)**"), §12 open technical questions (line 515 "**Counterfactual replay driver: no good exemplar; design problem largely unsolved**"); component-inventory C49 row (line 61 "Re-runs a trajectory from a midpoint via CXDB O(1) branching for variant tests; the 'most significant invention', largely unsolved"; maps A70/B62; depends C21; gap G19; foundational no) + critical-path note (line 127 "the single hardest, admittedly-unsolved invention (G19); the self-optimization batch (C46–C50) cannot close without it. **Highest-risk leaf on the critical path**") + Batch-5 placement (line 115); ambiguities-and-gaps **G19** (line 53 "The counterfactual-replay driver (P12) is admitted unsolved … zero interface, zero contract, zero acceptance scenario — yet P12 is counted in the '12 principles delivered' framing"); spec/C21 §3 (I5 "Branch / fork (O(1))" line 102 "The primitive C49 builds on"; I6 "Replay / trajectory retrieval" line 103 "C36/C37/C38/C49 consume"), §3 INV-3 (O(1) branch — no history copy), §1 (line 61 "NOT the counterfactual-replay driver … the driver … is **C49**"), §2 (line 80 C49 downstream consumer "most significant invention"); spec/C44 §1 (twin "holds the dependency's state across a session" — stateful + record/replay + OpenAPI mock); spec/C43 §1 (deterministic twin-by-default routing + lethal-trifecta blast-radius bound); review-log **D-6** (canonical track — no "Track A/B" framing), **D-13** (C43 owns blast-radius/twin isolation; C44 provides the twin; G31).
> Inventory ID: C49   Kind: component   Status: sweep-1
> Track: canonical (single-track per D-6)

## 1. Purpose & responsibility

C49 is the factory's **counterfactual-replay driver**: the component that, given a stored trajectory and a
**midpoint turn** within it, **re-runs the trajectory forward from that midpoint under a variant** (a changed
prompt, model, hyperparameter, or workflow step) and **makes the variant's outcome comparable to the
original's** (README line 274 "Re-run from trajectory midpoint"). It is the **driver half** of v4's "**Bridge +
driver**" entry for counterfactual replay (README line 274): the **bridge/primitive** — content-addressed
turns + **O(1) trajectory branching** — is owned by **C21 (CXDB I5/I6, INV-3)**; **C49 is the orchestration
glue that drives that primitive** to answer "what would have happened from turn T if we had changed X?"
(AI-CONTEXT §5.5 line 237; §10 line 359 "**Primitive exists; driver yours**").

C49 is the **keystone of P12 (self-optimization)** and v4 names it the system's "**most significant
invention**" (README line 278), to be "**built last, after Layers 1-5 are solid**" and given the "**heaviest
human review**" (README lines 278, 470). It is also **the riskiest leaf on the critical path**
(component-inventory line 127): the self-optimization batch (C46–C50) "**cannot close without it**." Its
value is that it lets the optimization loop test a variant **against the real situations the system already
encountered** — replaying from a recorded decision point — rather than only against synthetic scenarios or
fresh live traffic.

> **G19 is the defining fact of this spec.** v4 *admits this component is largely unsolved* — "**no good
> exemplar; design problem largely unsolved**" (AI-CONTEXT §12 line 515), with "**zero interface, zero
> contract, zero acceptance scenario**" in the source corpus (ambiguities-and-gaps G19). This spec's job at
> Sweep 1 is therefore **not to pretend a solution**. It is to (a) **name the capability and a contract**
> honestly, (b) **name precisely why it is hard**, and (c) **partition the problem into a tractable-now slice
> and an explicitly-deferred research slice** — so the integrator knows what can be built when C46–C50 land
> and what remains an open research bet. Over-claiming a general solution here would be the single most
> dangerous form of architectural dishonesty in v4. The genuine KEEP is **the branch-from-midpoint replay
> *driver* over CXDB** + the **honest open-problem framing** + the **tractable/deferred split**.

**Responsibilities (what C49 is the spec-of-record for):**
- **Select a midpoint** — given a trajectory (a path in C21's turn-DAG) and a selector, identify the **turn T**
  to branch from (the decision point under counterfactual study). Selection *policy* (which midpoints are
  worth testing) is upstream (C47 variant-identification / a self-healing investigation); C49 owns the
  *act of branching at the chosen T*.
- **Branch at the midpoint via CXDB O(1) fork** — invoke **C21 I5** to create a new head pointer rooted at T
  with **no history copy** (C21 INV-3). The branch shares the original's prefix (turns ≤ T) by construction;
  this is the primitive that makes "re-run from a midpoint" *storage-tractable* (AI-CONTEXT §5.5 line 237).
- **Apply the variant** — inject the change-under-test at the branch point: a different prompt/template
  (C09), model/route (C29), hyperparameter, or workflow step (C12). C49 owns the *binding of a variant onto
  the branch*; it does not author variants (that is C47).
- **Re-run forward from T under the variant** — drive the continuation: produce the post-T turns on the new
  branch by re-executing the workflow from the branched state. **This is the hard, only-partially-solvable
  step** (§5, §6) — it requires reconstructing the executable state as of T, which LLM non-determinism and
  external-dependency state defeat in general.
- **Make outcomes comparable** — produce a **counterfactual result record** pairing (original branch outcome,
  variant branch outcome) over the same midpoint, in a shape C48 (statistical comparison) and the evaluation
  tier (C32/C33 satisfaction) can score. C49 produces the *paired replay*; it does **not** decide
  significance (C48) or promotion (C50).
- **Scope and label replay fidelity honestly** — every replay carries a **fidelity/mode tag** declaring
  whether it was a **deterministic-tool-node replay** (tractable, high-fidelity) or a **counterfactual
  re-execution involving LLM/external-effect steps** (best-effort, fidelity-bounded). A consumer must never
  treat a best-effort replay as ground truth (§6, INV-3).

**Explicitly NOT (boundaries):**
- **NOT the branching primitive / the store.** O(1) fork, content-addressing, the turn-DAG, replay
  retrieval are **C21's** (I5/I6, INV-1/INV-3). C49 *calls* them; it stores no trajectories of its own
  (README line 274 "Bridge + driver" — C49 is the driver; the bridge/primitive is CXDB; README line 500
  "factory builds the orchestration glue, not the foundations").
- **NOT variant identification.** *What* prompt/hyperparameter/topology to try is **C47** (DSPy/Optuna);
  C49 replays a variant C47 (or an investigator) hands it. (inventory C47.)
- **NOT statistical comparison or promotion.** "Was the variant better?" is **C48** (scipy/Evidently);
  "does it become the default?" is **C50** (promotion gate). C49 yields the **paired counterfactual
  outcomes**; the verdict and the gate are downstream (inventory C48/C50; README lines 275–276).
- **NOT the meta-metric definition.** *What "better" means* (cost-per-satisfaction, time-to-threshold,
  judge-FP-rate) is **C46** (README line 269). C49 produces replays whose outcomes feed those metrics; it
  does not define them.
- **NOT the satisfaction/judge scorer.** Scoring a replayed outcome is **C32/C33**. C49 hands the variant
  trajectory to the eval tier; it does not judge.
- **NOT the digital twin or the isolation boundary.** Reconstructing **external-dependency** state for a
  replay is served by **C44 twins** (the stateful clone that "holds the dependency's state across a session",
  spec/C44 §1); bounding a replay's **blast radius** (a re-execution must not touch production) is **C43**'s
  deterministic twin-by-default routing (spec/C43 §1; D-13). C49 **runs its re-executions behind C43/C44**;
  it neither builds twins nor owns isolation. **These two mitigate, but do not solve, the midpoint-state
  reconstruction problem** (§6).
- **NOT a general time-travel debugger for arbitrary trajectories.** v4 scopes the use to **self-optimization
  variant tests** and **self-healing investigations** (AI-CONTEXT §5.5 line 237). C49 is not a user-facing
  "rewind any session and edit it" tool; that breadth is out of scope.
- **NOT a guarantee of deterministic reproduction.** C49 explicitly does **not** claim that re-running an
  LLM step from a midpoint reproduces the original (it cannot — §6). It claims only *branch-and-continue with
  an honest fidelity label*.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Dependency (sole, inventory) | **C21** CXDB trajectory store | Provides the **O(1) branch** (C21 I5, INV-3 "no history copy") and **replay/retrieval** (C21 I6) primitives C49 drives, plus the turn-DAG/content-addressing the midpoint lives in. C21 §1/§2 already name **C49 as the downstream consumer** of these. Inventory C49 "Depends on: C21". |
| Midpoint-state: external deps | **C44** Digital twin | Supplies the **reconstructable external-dependency state** for a replay — the stateful/record-replay clone that "holds the dependency's state across a session" (spec/C44 §1). A replay that hits an external service hits its **twin**, not production. *Mitigates the external-state half of G19; does not solve it.* |
| Midpoint-state: blast radius | **C43** Isolation & lethal-trifecta boundary | A counterfactual re-execution is a *speculative* run; C43's **deterministic twin-by-default routing** (production-scissors-by-declaration; D-13) ensures a replay's side effects are bounded to twins/isolated surfaces and **never reach production**. C49 re-executes **behind C43**. |
| Upstream (what to replay) | **C47** Variant identification | Hands C49 the **variant** to test (prompt via DSPy, hyperparameter via Optuna) — and, with the investigation, the **midpoint** of interest. C49 executes the counterfactual; C47 chooses it. (inventory C47; Batch 5.) |
| Downstream (verdict) | **C48** A/B routing & statistical comparison | Consumes C49's **paired counterfactual outcomes** to decide whether the variant was actually better (scipy/Evidently). C49 produces the comparison *inputs*, not the test. (inventory C48; Batch 5.) |
| Downstream (gate) | **C50** Promotion gate | Uses C48's verdict (over C49's replays + live A/B) to promote a variant to default. (inventory C50; Batch 5.) |
| Scoring | **C32/C33** Judge + satisfaction | Score a replayed variant trajectory's outcome (the same eval tier used for live runs). C49 hands off the variant trajectory; the scorer is unchanged. (inventory C32/C33.) |
| Variant surfaces (what gets changed) | **C09** prompt-template, **C29** model-floor/stylesheet, **C12** formula | The injectable change-under-test attaches to one of these surfaces at the branch point. C49 binds a variant onto them; it does not own them. |
| Packaging host | **C02/C17** Pack & tool-node ABI | C49 is delivered as a Gas City pack / tool node(s) in Phase 3d (README line 470 "factory builds … the counterfactual replay driver"). |
| Closest analogs (no exemplar) | git cherry-pick mechanics; Temporal workflow replay | The **nearest prior art**, explicitly flagged as **analogs with no LLM-specific exemplar** (AI-CONTEXT §10 line 423). Inform the *deterministic-replay* slice; neither solves the LLM-step counterfactual. |

**Position in the system.** C49 is **Batch 5** (component-inventory line 115), **Phase 3d** (README line 470):
the **last** thing built, after the substrate (P0–P1), the eval tier (P5/P6), self-healing (P11), twins (P7),
and the rest of self-optimization (C46–C48, C50) are in place. It is **not foundational** (inventory C49):
nothing else contracts against it; it is a leaf consumer of C21's primitive feeding C48/C50. It is, however,
**the highest-risk leaf on the critical path** (component-inventory line 127) and is **feature-gated with the
self-optimization layer** (it exists only when P12 is enabled). v4's own posture — "build last … heaviest
human review … highest-risk layer" (README lines 278, 470) — is the binding sequencing constraint.

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete signatures, the variant-injection schema, the
counterfactual-result record shape, and the fidelity-tag taxonomy defer to sweep 2 (and the branch/replay
wire to C21, the variant schema to C47, the comparison contract to C48).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Replay request (trajectory + midpoint + variant)** | inbound | Accept a request: a source trajectory (C21 turn-DAG path), a **midpoint turn T**, and a **variant spec** (what to change at T). The entry point for a counterfactual. | C49 (this); variant spec from **C47** |
| I2 | **Branch-at-midpoint** | outbound (write) → C21 | Invoke **C21 I5** to fork a new head at T (**O(1)**, no history copy — C21 INV-3). Returns a branch handle whose prefix (turns ≤ T) is shared with the original. | **C21** (primitive), C49 (caller) |
| I3 | **Variant binding** | internal | Bind the variant onto the branch: substitute the prompt (C09), model/route (C29), hyperparameter, or workflow step (C12) that the post-T continuation will use. | C49 (this) |
| I4 | **Counterfactual re-execution (forward from T)** | internal + outbound | Drive the continuation from the branched state under the variant, producing post-T turns on the new branch. **Runs behind C43 isolation, against C44 twins for external deps.** *The fidelity-bounded step — see I6, §6.* | C49 (this); **C43/C44** (boundary/state) |
| I5 | **Paired-outcome result record** | outbound | Emit a **counterfactual result**: (original-branch outcome, variant-branch outcome) over midpoint T, in a shape C48 can compare and C32/C33 can score. Carries the fidelity tag (I6). | C49 (this); consumed by **C48**, **C32/C33** |
| I6 | **Replay fidelity / mode tag** | internal/state (stamped on I5) | Declare the replay's fidelity class — **`deterministic-tool-replay`** (re-run touches only deterministic tool nodes / twin-served deps → high-fidelity, reproducible) vs **`counterfactual-reexecution`** (re-run involves LLM steps and/or non-twinned effects → best-effort, fidelity-bounded). A consumer **MUST** honor this label (INV-3). | C49 (this) |
| I7 | **Pack/tool-node lifecycle** | inbound (ops) | Delivered + invoked as a Gas City pack / tool node(s) in Phase 3d; feature-gated with the self-optimization layer. | C02/C17 (ABI), C49 (config) |

**Invariants C49 must uphold:**
- **INV-1 (driver, not store — branch is O(1) and copy-free):** C49 creates a counterfactual *only* by
  branching an existing turn via C21 I5 (C21 INV-3 — no history copy); it never duplicates or mutates stored
  turns and owns no trajectory storage. Re-running from a midpoint is storage-tractable **because** the
  prefix is shared, not copied (AI-CONTEXT §5.5 line 237).
  > [FAITHFUL-FILL] v4 states the *mechanism* ("re-run from midpoint via O(1) branching", README line 274) but
  > gives C49 no interface. "Branch via C21 I5 + re-execute forward" is the minimal faithful realization of
  > exactly that sentence — it adds no storage and no primitive beyond what C21 already exposes and already
  > names C49 as the consumer of (C21 I5/I6). Anything more (a C49-owned store, a custom branch implementation)
  > would duplicate C21 and is DROPPED.
- **INV-2 (variant isolated to the branch):** the variant is applied **only on the new branch**; the original
  trajectory and all other branches are unaffected (a counterfactual must not corrupt the factual record).
  Guaranteed by C21's copy-free branch semantics (INV-1) — branches are independent (C21 INV-2/INV-3).
- **INV-3 (fidelity is labeled, never assumed — the honesty invariant):** every replay result (I5) carries a
  fidelity tag (I6); a **`counterfactual-reexecution`** result is **best-effort** and a downstream consumer
  (C48/C50) **MUST NOT** treat it as a deterministic reproduction of the original. This is the contract that
  keeps G19's open problem from being silently laundered into a false certainty.
  > [FAITHFUL-FILL] v4 does not specify a fidelity contract (G19: "zero contract"). But v4 *does* admit the
  > problem is "largely unsolved" (AI-CONTEXT §12 line 515) — so the minimal faithful contract is one that
  > **surfaces** that unsolvedness at the interface (a fidelity label) rather than hiding it. This is the
  > smallest honest contract; it claims nothing v4 doesn't already concede.
- **INV-4 (no production side effects):** a counterfactual re-execution (I4) is speculative; it runs **behind
  C43** (twin-by-default routing) and hits **C44 twins**, never production. A replay that *cannot* be routed
  to a twin/isolated surface for some external effect **must fail closed** (refuse to replay that step) rather
  than touch production. (D-13; spec/C43 §1.)
- **INV-5 (deterministic-replay slice is exactly reproducible):** when a replay's post-T continuation touches
  **only deterministic tool nodes and twin-served dependencies**, re-execution reproduces the original
  post-T outcome on the original branch and yields a clean variant comparison (this is the `deterministic-
  tool-replay` class, I6). This slice is the **tractable-now** deliverable (§6).

## 4. Data model / state

C49 owns *driver/run state*; the **branch + turns** are C21's, the **variant spec** is C47's, the **twin
state** is C44's. State C49 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Replay job** | One counterfactual: {source trajectory ref, midpoint turn T, variant spec ref, branch handle, fidelity class, status}. Transient orchestration state. | C49-local (or a `factory_build`/experiment bead — see OQ). | C49; bead-type → **C20** if persisted |
| **Branch handle** | The C21 head pointer returned by the O(1) fork at T (I2). | **CXDB** (C21 owns the branch); C49 holds the reference. | **C21** |
| **Counterfactual result record** | The paired (original, variant) outcome over T + fidelity tag (I5/I6); the artifact C48/C32-C33 consume. | Emitted to C48 / persisted as a trajectory-or-bead (OQ). | C49 (shape); **C48** (consumer) |
| **Variant binding** | The concrete change-under-test mapped onto the branch (prompt/model/hyperparam/step). | Derived from C47's variant spec; transient. | **C47** (spec), C49 (binding) |
| **Replayed turns (post-T)** | The new turns produced on the branch by re-execution. | **CXDB** (turns are C21's; C49 appends via the normal turn path). | **C21** |
| **Pack/tool-node config** | C21 endpoint, twin/isolation wiring (C43/C44), feature-gate, replay bounds. | Pack TOML (C02/C03 model). | C02/C03 (model), C49 (binding) |

> [FAITHFUL-FILL] v4 gives C49 *no* state model (G19). The minimal faithful set is just the **replay job** +
> **branch handle** + **result record** — the smallest state needed to "branch at T, run the variant, pair the
> outcomes" (README line 274). C49 introduces **no new store**: branches and turns live in CXDB (C21), variant
> specs come from C47, twin state from C44. Whether a replay job/result is **persisted as a bead** (a new
> `factory_build`/experiment slot → C20 change request) or kept **transient + the variant trajectory itself is
> the durable artifact in CXDB** is **OQ-2** (the latter is the leaner default — the replay's evidence already
> survives as a CXDB branch). On-disk formats are sweep-2.

**Consistency / lifecycle.** C49 stands up **last (Phase 3d)** once C21 (primitive), C43/C44 (boundary/state),
and C47/C48 (variant in/verdict out) exist. Its state is **derived/transient**: the durable evidence of a
counterfactual is the **CXDB branch** (turns ≤ T shared, post-T variant turns appended) — re-derivable and
attributable via C21. C49 is therefore a *stateless-ish driver over CXDB's branch primitive*; if it dies
mid-replay, the partial branch survives in CXDB and the job can be re-issued (a half-run branch is harmless —
it is just an unfinished variant trajectory).

## 5. Behavior

**Stand up (Phase 3d).** The pack is installed last, after Layers 1–5; C49 is wired to C21 (:9010/:9009 for
branch/replay), to C43/C44 (the replay runs behind isolation against twins), and to C47 (variant in) / C48
(verdict out). Feature-gated with the self-optimization layer. Heaviest human review (README line 470).

**Counterfactual replay path (the contract).**
1. **Request** (I1): receive {trajectory, midpoint T, variant} from C47 / an investigation.
2. **Branch** (I2): invoke C21 I5 to **fork a new head at T** — O(1), no history copy (C21 INV-3). The branch
   shares turns ≤ T with the original by construction (INV-1).
3. **Bind variant** (I3): map the change-under-test onto the branch (prompt/model/hyperparam/step).
4. **Re-execute forward from T** (I4) — **behind C43, against C44 twins** (INV-4):
   - If the post-T continuation touches **only deterministic tool nodes / twin-served deps** → the
     **`deterministic-tool-replay`** path: re-execution is reproducible (INV-5); the variant comparison is
     clean. **This is the tractable-now slice.**
   - If the continuation involves **LLM steps and/or non-twinned external effects** → the
     **`counterfactual-reexecution`** path: re-execution is **best-effort, fidelity-bounded** (§6); C49 stamps
     the result accordingly (I6) and **does not claim reproduction**. If an external effect cannot be routed
     to a twin, the step **fails closed** (INV-4).
5. **Pair & emit** (I5): produce the (original, variant) outcome record over T + fidelity tag; hand to C48 for
   comparison and the eval tier (C32/C33) for scoring. C49 makes **no** better/worse or promotion decision.

> The variant-injection mechanism, the counterfactual-result record schema, the fidelity-tag taxonomy, the
> deterministic-vs-LLM step classification rule, the fail-closed external-effect detection, and sequence/state
> diagrams (Mermaid) are **sweep-2+**, and the deepest (LLM-step) parts are **research-deferred** (§6, OQ-1).
> The branch/replay wire is **C21**; the variant schema is **C47**; the comparison contract is **C48**.

## 6. Failure modes & handling

C49 owns **G19** — and G19 is not a bug to be handled but an **admitted open research problem to be framed
honestly and partitioned**. This section is the core of the spec.

**G19 (major) — the counterfactual-replay driver is admitted largely unsolved. FRAMED + PARTITIONED HERE
(not "resolved").**
> [AMBIGUITY: G19] v4 simultaneously (a) **counts P12 among the "12 principles delivered"** and lists
> counterfactual replay with a concrete mechanism ("Re-run from trajectory midpoint via CXDB O(1) branching",
> README line 274), and (b) **admits the driver is "largely unsolved … no good exemplar"** (AI-CONTEXT §12
> line 515; §10 line 359 "driver yours"), with **no interface / contract / acceptance scenario** in the corpus
> (G19). The two readings: **(a)** treat it as buildable now (over-claim a solution); **(b)** treat it as a
> framed open problem with a tractable slice carved out and the rest deferred. **Chosen: (b)** — it is the only
> reading consistent with v4's own words ("largely unsolved", "build last", "highest-risk layer; heaviest human
> review", README lines 278, 470). Pretending (a) would contradict AI-CONTEXT §12 directly. **C49 therefore
> ships an honest contract (§3) + the following partition, not a claimed general solution.**

**Why it is hard (named precisely — the load-bearing analysis):** "Re-run a trajectory from a midpoint" requires
**reconstructing the executable state as of turn T** and then continuing under a variant. Two forces defeat
faithful reconstruction in the general case:
- **(1) LLM non-determinism.** A model step is **not a pure function** of its inputs — sampling, provider-side
  changes, and context-sensitivity mean re-running the same prompt from T does **not** reproduce the original
  turn, and a *variant* prompt's effect is confounded with that intrinsic variance. The CXDB branch
  reconstructs the *recorded conversation prefix* (turns ≤ T) **exactly** (content-addressed, C21 INV-1) — but
  re-executing the *model* from there is inherently stochastic. **CXDB's O(1) branch solves trajectory-state
  reconstruction; it does not solve model-execution reconstruction.** This is the irreducible core of G19.
- **(2) External-dependency state.** A continuation from T may call external services whose state has since
  changed (or which cannot be safely re-hit). **C44 twins** reconstruct a *clone* of that dependency's state,
  and **C43** routes the replay to the twin (never production) — **this mitigates external state** for twinned
  dependencies. But it is **bounded by twin fidelity (G22/C45)** and **only covers dependencies that have a
  twin**; un-twinned or imperfectly-twinned effects remain a fidelity gap.

**The honest partition — what's tractable now vs deferred:**

| Slice | Fidelity | Status | Why |
|---|---|---|---|
| **TRACTABLE NOW — `deterministic-tool-replay`** | High / reproducible (INV-5) | **Buildable in Phase 3d** | When the post-T continuation touches **only deterministic tool nodes and twin-served dependencies**, re-execution is a *pure* function of the branched state: CXDB reconstructs the prefix exactly (C21 INV-1), C44 reconstructs external state, and there is **no LLM in the replayed segment**. Variant tests over **deterministic workflow steps / hyperparameters affecting deterministic nodes** are genuinely comparable. This is the analog of git cherry-pick / Temporal workflow replay (AI-CONTEXT §10 line 423) — the prior art that *does* exist. **This is the real, low-risk KEEP.** |
| **DEFERRED — `counterfactual-reexecution` (full LLM-step counterfactual)** | Best-effort, fidelity-bounded (INV-3) | **Open research bet → OQ-1** | Re-running **LLM steps** from a midpoint under a variant is the unsolved core (force 1). C49 ships it **labeled best-effort** with mitigations (multiple re-runs to estimate variance; twin-served deps; fail-closed on non-twinned effects) but **claims no deterministic reproduction**. v4's "heaviest human review" (README line 470) applies *here*. Quantifying when a best-effort LLM-counterfactual is *trustworthy enough* to feed C48/C50 is **the open question** (OQ-1). |

**Other failure cases.**
- **Midpoint turn invalid / not in DAG** → reject the replay request (C21 has no such turn); do not branch.
- **External effect with no twin** (INV-4) → **fail closed**: refuse to replay that step rather than touch
  production; surface as a fidelity limitation on the result. *[FAITHFUL-FILL]: v4 gives no rule; fail-closed
  is the only safe choice given C43's production-scissors posture (D-13).*
- **Variant trajectory diverges unboundedly** (the variant takes a wildly different path) → the replay is
  still a valid counterfactual *observation*, but comparability degrades; the fidelity tag + C48's stats must
  account for it. C49 bounds re-execution (max turns/cost) like any agent run. *[FAITHFUL-FILL].*
- **Confounded comparison from LLM variance** (force 1) → mitigated, not eliminated, by repeating the
  counterfactual N times to estimate the variance band (so C48 compares *distributions*, not single runs);
  N + the trust threshold are **deferred** (OQ-1). *[FAITHFUL-FILL].*
- **CXDB down** → no branching possible; C49 is a Phase-3d optimization layer and **degrades cleanly** (the
  factory's build/heal loops do not depend on C49); inherits C21's fail-open posture (C21 AC-7).

> F-mode applicability is owned by C57 (coverage map). C49 underwrites the P12 self-optimization principle's
> counterfactual capability **contingent on the partition above** — and C57 is precisely where the **honest
> residual** ("full LLM-step counterfactual is best-effort, not solved") must be registered, not buried. C49
> surfaces the class (G19 unsolved-core, twin-fidelity-bounded external state) and defers the canonical F-mode
> mapping + residual-risk entry there.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** A counterfactual re-execution is a **speculative agent run** and is the sharpest case for
  C43's lethal-trifecta boundary: it **must not** mutate production (INV-4) — it runs behind C43's
  twin-by-default routing against C44 twins, and **fails closed** on any non-twinnable external effect (D-13).
  This is *why* C49 is gated behind twins+isolation and built **after** them (Phase 3d, after P7/C43).
- **Cost.** Re-execution **spends model tokens** (each LLM-step counterfactual is a fresh run; estimating
  variance multiplies that by N). v4 gives **no cost model** for replay; cost-per-counterfactual feeds the
  meta-metrics (C46) and is a real budget concern on a single Max seat (shared with C28's token-budget OQs).
  The `deterministic-tool-replay` slice is cheap (no model spend); the LLM-counterfactual slice is the
  expensive, deferred one. **OQ-3.**
- **Scale.** The **branch** is O(1) (C21 INV-3) — replay does not stress storage. The cost ceiling is
  **re-execution compute/tokens**, not branching. "Thousands of replays" is bounded by model throughput +
  twin throughput (C44), not by CXDB.
- **Observability.** Each replay's lineage is fully attributable in CXDB (the branch records turns ≤ T shared
  + post-T variant turns, with `created_by`, C21 turn model); the **fidelity tag** (I6) is the key
  signal telling a consumer/operator how much to trust a result. C49's own health = replay success/fail rate,
  fail-closed count, variance bands.
- **Ops.** Built **last**, **heaviest human review** (README lines 278, 470) — the operator posture is that
  C49's outputs (especially LLM-counterfactuals) are **reviewed**, not auto-trusted, until the trust question
  (OQ-1) is settled. Pin C21/C44 versions so branch/twin behavior is reproducible.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2). **Note (honesty):** the acceptance criteria are
split to match the partition — the deterministic slice has *hard* criteria; the LLM-counterfactual slice has a
*labeling/best-effort* criterion, **not** a reproduction criterion (claiming the latter would violate G19's
honest framing).

1. **AC-1 (branch-at-midpoint — I2/INV-1):** given a trajectory and a turn T, C49 creates a CXDB branch rooted
   at T via C21 I5 with **no history copy** (C21 INV-3 / AC-4); the branch shares turns ≤ T with the original.
2. **AC-2 (variant isolated — INV-2):** applying a variant on the branch leaves the original trajectory and
   sibling branches byte-identical (the factual record is uncorrupted).
3. **AC-3 (deterministic-tool replay reproduces — INV-5, the tractable slice):** for a post-T continuation
   touching **only deterministic tool nodes + twin-served deps**, re-execution **reproduces** the original
   post-T outcome (and a variant change produces a *clean, attributable* difference). This is the load-bearing
   "it actually works for the tractable slice" test.
4. **AC-4 (no production side effect — INV-4):** a replay routes all external calls to **C44 twins** (never
   production); a step with a non-twinnable external effect **fails closed**, not through to production.
5. **AC-5 (fidelity labeled — INV-3, the honesty AC):** every result (I5) carries a fidelity tag (I6); a replay
   involving LLM steps is tagged **`counterfactual-reexecution`** (best-effort) and is **never** emitted as
   `deterministic-tool-replay`. A consumer can mechanically tell a high-fidelity replay from a best-effort one.
6. **AC-6 (paired comparable output — I5):** C49 emits a (original, variant) outcome record over T in a shape
   **C48 can statistically compare** and **C32/C33 can score** — without C49 itself deciding better/worse.
7. **AC-7 (best-effort LLM-counterfactual is bounded, not claimed — INV-3, addresses G19 honestly):** for an
   LLM-step counterfactual, C49 produces a result **with a variance estimate** (repeat-N) and the best-effort
   tag; the AC verifies the result is **labeled and bounded**, and explicitly **does NOT** assert
   reproduction. *(This is the AC that encodes "framed, not solved.")*
8. **AC-8 (clean degradation — Phase-3d leaf):** with C49 disabled or CXDB/twins unavailable, the factory's
   build/heal loops are unaffected (C49 is a self-optimization leaf; nothing foundational depends on it).

**Test strategy.** A **counterfactual-replay integration pack** that, against pinned C21 + a C44 twin behind
C43: (1) drives AC-1/AC-2 (branch + isolation of the variant) — purely the C21-primitive path, low-risk;
(2) drives AC-3 over a **deterministic-tool-only** trajectory (the *real* correctness proof of the tractable
slice); (3) drives AC-4 (fail-closed production guard) — the security de-risker; (4) drives AC-5/AC-7 (the
**fidelity-labeling** and best-effort-bounding tests — the proof the unsolved part is *honestly surfaced*, not
hidden). The LLM-counterfactual trust threshold (when AC-7's best-effort result is good enough to feed C48/C50)
is **explicitly out of the Sweep-1 acceptance set** and deferred to the research bet (OQ-1). This suite gates
nothing else (C49 is the last leaf) but is itself the **heaviest-human-review** artifact (README line 470).

## 9. Open questions

- **OQ-1 (→ review-log, top): the unsolved core of G19 — when is an LLM-step counterfactual trustworthy?**
  The `deterministic-tool-replay` slice is tractable (AC-3); the **full LLM-step counterfactual** is the
  admitted-unsolved part (AI-CONTEXT §12 line 515). What makes a best-effort `counterfactual-reexecution`
  result (variance-estimated over repeat-N) **trustworthy enough** to feed C48's comparison and C50's gate —
  what N, what variance bound, what judge-FP guard (C46/C32)? Is the honest Phase-3d posture **"deterministic
  slice automated + LLM slice human-reviewed-only"** until this is answered? *This is the riskiest open
  question in v4* (component-inventory line 127) and the one the "heaviest human review" (README line 470) is
  for. **Frame, don't pretend to close.**
- **OQ-2 (→ review-log): replay-job/result persistence.** Is a replay job/result persisted as a **bead** (a new
  `factory_build`/experiment slot → C20 change request) or kept **transient** with the **CXDB variant branch
  as the durable artifact** (the leaner default)? Freeze sweep-2 with C20/C48.
- **OQ-3 (→ review-log): replay cost model + budget.** v4 gives no cost model for counterfactual re-execution
  (token spend × repeat-N × variants). Quantify cost-per-counterfactual (feeds C46) and the per-seat budget
  ceiling (shared with C28's token/throughput OQs) before any "thousands of replays" claim. Sweep-2.
- **OQ-4 (→ review-log): variant-injection seam + result-record schema.** The exact mechanism for binding a
  variant (prompt C09 / model C29 / hyperparam / step C12) onto a branch at T, and the **counterfactual-result
  record** shape C48 consumes + C32/C33 score. Freeze jointly sweep-2 with C47 (variant spec) + C48 (comparison
  contract).
- **OQ-5: twin-fidelity dependence (G22 inherited).** The external-state half of a replay is only as good as the
  C44 twin's fidelity (G22/C45). For which dependencies must a twin exist before a counterfactual touching them
  is admissible, and how does twin-fidelity (C45) bound the replay's fidelity tag? Joint sweep-2 with C44/C45.
