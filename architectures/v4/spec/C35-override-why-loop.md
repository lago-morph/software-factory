# C35 — Override → pattern → rule loop  (Spec, canonical track)

> Source: README §"Principle 8 — 'Why am I doing this?'" (L206–218: the 5-row component table — *Manual override detection* → Claude Code `PreToolUse`/`PostToolUse` hooks; *"Why" field prompting* → hook handler; *Override log storage* → "Gas City beads with type `override`"; *Periodic pattern surfacing* → "Custom SQL/duckdb query pack"; *Rule conversion* → "Manual review + new Inspect AI rubric"), §"Phase 3a — P8" (L457: "factory builds the override-detection Claude Code hooks + the periodic-surfacing pack. Transfusion sources: AWS CloudTrail audit log shape, git reflog conventions. Small scope."); AI-CONTEXT §3.1 row 8 (L38: "Manual overrides surface as new validation rules"), §6 "Layer 3 — observability + 'why'" (L306–319: *Manual override logging / "Why" field capture / Pattern surfacing* = "None [purpose-built] / DIY / Small custom"), §8 Layer-3 transfusion sources (L400–401: override pattern ← AWS CloudTrail, GCP Audit Logs, auditd, git reflog; pattern surfacing ← Honeycomb BubbleUp, Datadog Watchdog); F-MODE-COVERAGE §2 (L31: F10 "Findings disappear into chat" → "Override log discipline (P8 component)").
> Inventory ID: C35   Kind: control-loop   Status: sweep-1
> Maps from: A38, A39, A40, A41, A42, B09, B67, B68. Depends on: C28, C20, C30. Key gaps: G43.
> Binding decisions obeyed: **D-3** (C20 *authors* the `override` bead-type schema; C35 *logs* `override` beads using it, and does not define the schema). **D-6** (canonical track; no Track-A/B framing). *Contextual (not implemented by C35):* **D-1** governs the *judge* that later consumes a C35-emitted Inspect-AI rubric (same provider/family as coder); C35 itself neither invokes the judge nor chooses a provider, so D-1 only frames the downstream of the §3 rule-conversion handoff.

## 1. Purpose & responsibility

C35 is the **"why" discipline control-loop** (P8): the mechanism by which an **operator override of the system becomes institutional knowledge**. It closes the loop *override → why → bead → pattern → rule*: it (1) **detects** when an operator bypassed/overrode what the factory would have done, (2) **prompts for the "why"**, (3) **logs** the override + rationale as a durable `override` bead, (4) **surfaces recurring override patterns** across the accumulated log, and (5) **converts a recurring pattern into a new validation rule** — v4's named sink is a new Inspect-AI rubric (C30, README L216); spec-/workflow-structural classes are faithfully inferred to feed the spec linter (C10) / workflow linter (C15) (§3 contract 6) — so the same class of override stops being necessary.

This is the genuine P8 capability — *institutional learning from human corrections* — that no piece of the stack delivers on its own. README L208 states the thesis verbatim: "If you can articulate why something looks wrong, you've described a validation rule. Capture overrides, surface patterns, convert to rules." C35 is the orchestration that wires the stack's parts (Claude Code native hooks for detection, C20 `override` beads for storage, a query/clustering pack for surfacing) into that loop and carries the small custom glue between them.

It is responsible for:
- **Override detection** via Claude Code **native** `PreToolUse` / `PostToolUse` hooks registered as a Gas City pack (README L212). The hook is the trigger; C35 owns the *override-recognition predicate* (what counts as "operator bypassed the system") and the handler that fires on it.
- **"Why" capture** — the hook handler forces a structured rationale for the override (README L213 "Forces structured explanation").
- **Override logging** — writing an `override` bead (type + payload **defined by C20**, D-3) carrying the rationale and a reference to the overridden action (README L214).
- **Pattern surfacing** — a periodic pack that reads the `override` log and finds *recurring* overrides (README L215 "Reviews log for recurring overrides"; AI-CONTEXT L401 transfuses the surfacing pattern from Honeycomb BubbleUp / Datadog Watchdog).
- **Rule conversion** — turning a surfaced recurring pattern into a **new validation rule**. v4 (README L216) names exactly **one** conversion target — a "new Inspect AI rubric" (the C30 scenario store) — so that is the v4-grounded sink. Where an override class is *spec-structural* or *workflow-structural* rather than satisfaction-shaped, the minimal faithful reading routes it to the C10 (spec linter) / C15 (workflow linter) rule sets (those linters are where such "validation rules" live in the system, per README L208's generic "you've described a validation rule") — see the [FAITHFUL-FILL] in §3 contract 6; these two are an **inference**, not a v4-named sink.

**What it is explicitly NOT:**
- NOT the **`override` bead-type schema author** — the `type="override"` payload shape (the "why"/rationale field, the overridden-action reference) is **C20's** (binding **D-3**; C20 spec §4.2). C35 is a *writer/reader* of that type, not its definition.
- NOT the **hook framework** — detection rides Claude Code's **native** `PreToolUse`/`PostToolUse` surface exposed by C28 (C28 §3 "Hooks", C28 AC3: "override-detection surface for C35"). C35 registers a handler; it does **not** build a custom hook engine. (Any custom hook-dispatch machinery would be flagged and dropped — see §7.)
- NOT the **bead store / work-graph** — durability, querying, and `created_by` attribution of the `override` beads belong to C19/C20/C41. C35 transitions/writes beads; it does not own the ledger.
- NOT a **clustering/embedding engine** — recurring-pattern surfacing reuses existing query/clustering capability (DuckDB/SQL for the simple case per README L215; the C37 trajectory-clustering / sklearn-HDBSCAN territory for the semantic case). C35 does not reinvent clustering.
- NOT the **linter engines** — C35 *emits a new rule/rubric* into C10 / C15 / C30; it does not execute spec-linting or workflow-linting itself (those are C10/C15's loops).
- NOT a **silent auto-shipper of rules** — rule conversion is operator-gated (README L216 "Manual review", "Operator workflow"); C35 *proposes* a rule, it does not unilaterally promote one to enforced at L5 (see §6, F-mode F52/G35 caution).
- NOT the **self-heal loop** (C36–C39) — that loop reacts to *anomalies/failures*; C35 reacts to *operator overrides*. They share the bead-chain idiom but are distinct loops with distinct triggers.

## 2. Context & dependencies

| Direction | Piece | Relationship |
|---|---|---|
| Upstream (detection surface) | **C28** Claude Code agent loop | Provides the native `PreToolUse`/`PostToolUse` hook surface C35's handler registers on (C28 §3, AC3). C35 is the first named consumer of that surface. |
| Upstream (schema) | **C20** Bead schema registry | **Authors** the `override` bead type + payload (D-3); C35 logs against it. C20 §2 lists C35 as the downstream consumer of `override`. |
| Dependency **and** rule sink (Inspect-AI rubric) | **C30** Scenario store | Dual relationship: C35 **depends on** C30 (inventory) because C30 owns the **Inspect-AI rubric schema** C35's conversion must target, **and** C35 **emits a new rubric into** C30 (a downstream sink) when a surfaced override class is about work-satisfaction (README L216 — the one v4-named conversion target). C30's read-isolated rig owns rubric authoring; C30 §2 lists C35 as a downstream consumer. |
| Upstream (store/attribution) | **C19 / C41** | C19 persists the `override` work-graph; C41 stamps `created_by` on every override record (P9). |
| Downstream (rule sinks) — **inferred, not v4-named** | **C10** spec linter, **C15** workflow linter | *Faithful inference* (see §3 contract 6 [FAITHFUL-FILL]): v4 names only the Inspect-AI rubric (C30) as a conversion target (README L216); routing spec-structural / workflow-structural override classes to C10/C15 is the minimal reading of L208's generic "validation rule", since those linters are where such rules live. C35→C10/C15 is a rule-registration handoff, not a code dependency, and **C10/C15 are not listed as C35 dependencies** in the inventory. |
| Lateral (reuse) | **C37** trajectory clustering | For *semantic* recurring-pattern surfacing, C35 reuses C37's embedding/clustering rather than its own (the simple case stays SQL/DuckDB per README L215). |
| Lateral (operator) | **Operator workflow** | The human-in-the-loop review that approves a surfaced pattern → enforced rule (README L216). |

C35 is **not foundational** (inventory) and lands in **Batch 3 / Phase 3a** (README L457) — it depends on C28's hook surface and C20's schema both existing first.

## 3. Interfaces / contracts (sweep-1: named + described)

**Inbound:**
1. **Override-detection hook binding** — a pack-registered `PreToolUse`/`PostToolUse` hook (Claude Code native, via C28) whose handler is C35's **override-recognition predicate**. Input: the hook's tool-call context (proposed/observed tool call, decision, actor/session id). The predicate decides "was this an *operator override* of the system?" (e.g. an operator-initiated deny/edit/force that contradicts what a gate/linter/formula would have done). *Sweep-1: named + described; the exact predicate definition and the hook event payload fields are sweep-2.*
2. **"Why" capture contract** — when the predicate fires, the handler **elicits a structured rationale** from the operator (a required "why" field). Precondition: an override was detected. Postcondition: a non-empty rationale is bound to the pending `override` record (or the override is flagged un-explained — see §6).
3. **Override-log read contract** — the periodic surfacing pack reads the accumulated `override` beads via Gas City `gc bd` / CXDB query (README L242 "Query interface", C20-owned schema).

**Outbound:**
4. **Override-logging contract** — C35 writes a bead of `type="override"` using **C20's** payload schema (D-3): the captured "why"/rationale + a reference to the overridden action, with `created_by` (C41). Invariant: **every** detected override produces exactly one `override` bead (no silent overrides — that is the entire point of P8; F10).
5. **Pattern-surfacing contract** — the periodic pack emits a **recurring-override report**: clusters/groups of `override` beads that recur (by overridden-action class + rationale similarity), above a recurrence threshold. Simple case = SQL/DuckDB grouping (README L215); semantic case = reuse C37 clustering. Output consumed by the operator-review step.
6. **Rule-conversion / rule-emission contract** — for an operator-approved recurring pattern, C35 emits a **new validation rule** to the appropriate sink:
   - work-satisfaction class → a new **Inspect-AI rubric** in **C30** (README L216) — **the v4-named sink**,
   - spec-structural class → a new **C10** (EARS/INCOSE) rule *(inferred sink — see FAITHFUL-FILL)*,
   - workflow-structural class → a new **C15** (Mammoth) rule *(inferred sink — see FAITHFUL-FILL)*.
   *Sweep-1: the handoff is named (what sink, what triggers it). The rule-encoding format per sink is sweep-2 and is constrained by each sink's own rule schema.*
   > [FAITHFUL-FILL] **Only the Inspect-AI rubric (C30) is a v4-named conversion target.** README L216's "Rule conversion" row names exactly one sink: "Manual review + **new Inspect AI rubric**". v4 names no C10 or C15 conversion path for overrides, and the component-inventory C35 row lists dependencies as **C28, C20, C30** only (not C10/C15). The minimal faithful elaboration of README L208's *generic* thesis ("If you can articulate why something looks wrong, you've described a validation rule") is that a *spec-structural* override class becomes a C10 (EARS/INCOSE) rule and a *workflow-structural* one a C15 (Mammoth) rule, because those linters are the system's home for exactly those rule kinds (inventory C10/C15). This is an **inference about which existing sink a rule lands in**, not a new component or a v4-stated handoff; it invents no rule-conversion *mechanism* (still operator-gated, I4). If the orchestrator rules the override loop targets *only* the Inspect-AI rubric, drop the C10/C15 rows — nothing else in C35 depends on them.

**Invariants:**
- **I1 (totality):** every override the predicate detects is logged as exactly one `override` bead — no override disappears into chat (F10; README L208 "Capture overrides").
- **I2 (why-completeness):** an `override` bead carries a non-empty rationale, or is explicitly marked `why_missing` for follow-up (degraded path, §6) — a logged override without a captured "why" is a defect, not a silent success.
- **I3 (schema deference, D-3):** C35 never defines or extends the `override` payload; it writes only fields C20's schema declares. A needed new field is a **change request to C20**, not a local extension.
- **I4 (no auto-enforce):** a converted rule is *proposed* and reaches "enforced" only through the operator-review gate (README L216) — C35 cannot silently promote a rule into C10/C15/C30 enforcement (G35/F52 guard).
- **I5 (native-hooks-only):** detection uses only Claude Code's native hook surface (via C28); C35 introduces no custom hook framework.

## 4. Data model / state

C35 owns **almost no durable state of its own**; it is a control-loop over state owned elsewhere.

| State | Owner | C35's relationship |
|---|---|---|
| `override` beads (type + payload) | **C20** schema / **C19** store | C35 **writes and reads** them; owns neither the schema nor the ledger. |
| `created_by` attribution on each override | **C41** | Stamped by the identity layer; C35 supplies the actor context from the hook. |
| Hook registration (`.claude/` + pack) | **C02 pack / C28** | Declarative, version-controlled; C35 contributes the handler, not the hook engine. |
| Recurring-pattern report | **transient** (query output) | Re-derivable from the `override` log on each periodic run; C35 holds it only across one surfacing→review cycle. (May be persisted as a bead at sweep-2; not owned-state in sweep-1.) |
| Converted/proposed rules | **C30** (v4-named rubric sink); **C10 / C15** (inferred sinks, §3 contract 6) | Once emitted, the rule lives in the sink's own store; C35 keeps only a provenance back-reference (which `override` cluster produced which rule). |

The **override-recognition predicate** and the **recurrence threshold** are C35's two pieces of genuine policy/config (carried in C03 / the pack), but they are configuration, not a persistent store. The loop is otherwise **stateless between runs** — its memory *is* the C20 `override` log.

## 5. Behavior

**The loop (one override → rule cycle):**
1. **Detect.** During a C28 agent run, an operator override occurs (operator denies/edits/forces a tool call against what a gate/linter/formula would do). The native `PreToolUse`/`PostToolUse` hook fires; C35's handler runs the **override-recognition predicate**.
2. **Prompt "why".** If the predicate says "this is an operator override," the handler forces a structured rationale (the required "why" field). (README L213.)
3. **Log.** C35 writes one `override` bead — C20's schema, C41 `created_by` — carrying the "why" + the overridden-action reference. (README L214.) *(I1, I2.)*
4. **Surface (periodic, not per-override).** A scheduled pack reads the `override` log and groups recurring overrides (SQL/DuckDB for exact/structural recurrence; reuse C37 clustering for semantic recurrence). Clusters above the recurrence threshold become a **recurring-pattern report**. (README L215; AI-CONTEXT L401.)
5. **Operator review.** The report goes to the operator, who decides whether a recurring pattern *is* a latent validation rule (README L208 thesis; L216 "Manual review", "Operator workflow"). *(I4.)*
6. **Convert.** For an approved pattern, C35 emits a new rule to the right sink — a **C30 Inspect-AI rubric** (satisfaction-class; the v4-named sink, README L216) or, by the §3 contract-6 faithful inference, a C10 (spec-structural) / C15 (workflow-structural) rule. The rule then prevents/flags that override class going forward, closing the loop.

**Cadence:** steps 1–3 are **synchronous** with each override (hook-driven). Steps 4–6 are **periodic + human-gated** (README L215 "Periodic pattern surfacing"; L457 "periodic-surfacing pack"). C35 is therefore a *slow* control-loop: it does not act on a single override, only on *recurrence*.

**Degraded behavior:** see §6.

> [FAITHFUL-FILL] v4 lists C35 as five table rows and a one-line thesis; it does not give the loop as a numbered sequence. The above is the minimal faithful assembly of exactly those five rows (detect → why → log → surface → convert) in the order README L208 states them. No step is invented; the only addition is making the *cadence* (synchronous log vs periodic surfacing) explicit, which README L215/L457 already imply by calling surfacing "periodic".

## 6. Failure modes & handling

| F-mode | Applies how | Handling per v4 |
|---|---|---|
| **F10** Findings disappear into chat | The override (a finding about what's wrong) could be lost in conversation instead of captured | **Directly addressed** — F-MODE-COVERAGE L31 names "Override log discipline (P8 component)" + content-addressed trajectory store as the F10 mechanism. C35's I1 (every override → one bead) *is* this guard. |
| **F52** "More controller patches" / runaway loop *(faithful analogy — see note)* | Rule conversion that auto-shipped could spawn rules that cause further overrides (oscillation) — the self-modifying-control trap | Mitigated by **I4 + operator gate** (README L216): conversion is human-reviewed, not auto-promoted, so the loop cannot silently feed itself. |

> **F-mode mapping note.** **F10** is the *v4-stated* mapping for the P8 component (F-MODE-COVERAGE L31: "Override log discipline (P8 component)") — that row is grounded directly in v4. **F52** is applied here by **faithful analogy**: v4 maps F52 to the *self-healing* loop ("more controller patches", F-MODE-COVERAGE §8), and C35's auto-shippable-rule-conversion step is structurally the same self-modifying-control trap, so the same guard (operator gate, I4) is the right one. The canonical F-mode→component mapping is owned by **C57**; C35 surfaces the F52 risk on its conversion seam rather than asserting a v4-stated F52→C35 mapping.

**Loop-specific failure handling:**
- **Un-explained override (why missing/refused):** if the operator dismisses the "why" prompt, the override is still logged (I1) but marked `why_missing` (I2 degraded path) so it is visibly incomplete and re-promptable — an override is never *dropped* just because the rationale wasn't given.
- **Predicate false-positive / false-negative:** the override-recognition predicate is heuristic; an over-broad predicate floods the log, an over-narrow one misses overrides. Faithful mitigation: the predicate is **tunable config** (§4) and recurring false-positive *clusters* are themselves visible in the surfacing report (so the predicate can be corrected via the same loop). *Quantified thresholds → sweep-2.*
- **Surfacing on an empty/sparse log:** before enough overrides accumulate, surfacing yields nothing; this is correct (no spurious rules) and is why the loop is periodic, not eager.

> [AMBIGUITY: G43] **P8 maturity is stated inconsistently across the v4 docs — does C35 ship a working "why" loop, or only the detection+logging half?**
> Reading A (strong): AI-CONTEXT §3.1 row 8 (L38) flatly asserts the P8 outcome — "Manual overrides **surface as new validation rules**" — i.e. the *full* detect→surface→convert loop is in scope and delivered.
> Reading B (weak): AI-CONTEXT §6 Layer-3 (L317–319) rates override-logging / "why"-capture / pattern-surfacing each as "**None [purpose-built] / DIY / Small custom**", README Phase-0 "What's delivered" omits P8 entirely, and P8 only lands in **Phase 3a** (README L457) as a *factory-built* component — so at Phase 0 the loop is **absent**, and even at 3a the *rule-conversion* end is "Manual review + Operator workflow" (README L216), not an automated converter.
> **Chosen (most consistent with v4):** **C35's automatable scope is detect → "why" → log → surface; rule *conversion* is explicitly operator-gated, not automated** (README L216; I4). This reconciles both readings: §3.1's "surface as new validation rules" is the loop's *purpose/outcome*, achieved **with a human in the conversion step**, not a claim that conversion is autonomous. C35 is therefore correctly a *small, mostly-discipline* component (README L218 "P8 is mostly a discipline + small tooling") whose automated portion is detection+logging+surfacing and whose conversion step is an operator workflow. The "P8 delivered at Phase 0" impression from F-mode F10 is the doc inconsistency itself: **F10's override-log guard is real only from Phase 3a onward**, and any Phase-0 reliance on P8 (e.g. F10) is overstated until C35 ships. *This is a deferral of the maturity-timeline reconciliation to the review-log, plus a concrete scope ruling (conversion = human-gated).* 

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security:** the override hook sees operator tool-call decisions and rationales — `override` beads carry `created_by` (C41, P9) so every logged override is attributable and non-repudiable (modulo the optional-signing gap G36, owned elsewhere). The "why" rationale is operator-authored free text → treat as untrusted input at the rule-conversion seam (no rationale string is executed; it only informs a human-reviewed rule). C35 adds **no** new tool/network/fs surface of its own.
- **Cost:** negligible by construction — detection is a hook callback (no extra model call required for the predicate; "why" capture is a prompt, not an inference); surfacing is a periodic SQL/DuckDB query or a reuse of C37's already-budgeted embeddings. README L218: "small tooling". No second model seat. *(If semantic surfacing routes through C37 embeddings, that token cost is C37's, not new here.)*
- **Scale:** the `override` log grows with operator-override frequency, which is **low-volume** (human-in-the-loop events), not trajectory-volume — so the store and the periodic query scale trivially relative to CXDB/trajectory data.
- **Observability:** C35 is itself part of the observability/"why" tier (AI-CONTEXT §6 Layer 3). Its own actions (override logged, pattern surfaced, rule proposed) are beads/events → visible in the same stores it feeds.
- **Ops:** entirely **declarative + pack-shaped** — the hook handler + the periodic-surfacing query ship as a Gas City pack (README L212, L215, L457; transfusion from CloudTrail/git-reflog log shape, AI-CONTEXT L400). No Go fork. The recurrence threshold + predicate are config (C03).

**What the capability-bar dropped (non-principle polish):** a bespoke override-clustering/embedding engine (→ reuse C37 / DuckDB), a custom hook-dispatch framework (→ Claude Code native hooks via C28), a real-time per-override alerting/dashboard (not tied to a principle; surfacing is *periodic* by design), and any auto-promote-rule-to-enforced path (dropped on the F52/G35 safety bar — conversion stays human-gated). What is **kept** as genuine custom code is the small glue the principle requires: the **override-recognition predicate** (no stack component knows what "operator overrode the system" means for *this* factory) and the **rule-conversion handoff** wiring to the rule sink(s) — the C30 Inspect-AI rubric (v4-named) and, by the §3 contract-6 faithful inference, C10/C15.

## 8. Acceptance criteria & test strategy (sweep-1, high level)

- **AC1 (detect + log):** an operator override during a C28 run fires the registered `PreToolUse`/`PostToolUse` hook, the recognition predicate identifies it as an override, and exactly one `override` bead is written using C20's schema with `created_by` set. (README L212, L214; I1.)
- **AC2 (why capture):** the override bead carries a non-empty operator-supplied rationale; an override where the operator declines to explain is logged and marked `why_missing`, never dropped. (README L213; I2.)
- **AC3 (surfacing):** given an `override` log containing a recurring override class above threshold, the periodic surfacing pack groups it into a recurring-pattern report; given a log with no recurrence, it reports none. (README L215.)
- **AC4 (rule conversion handoff):** an operator-approved recurring pattern is converted into a new rule registered in the correct sink — a **C30 Inspect-AI rubric** (satisfaction-class; the v4-named sink, README L216) or, per the §3 contract-6 inference, a C10 (spec-structural) / C15 (workflow-structural) rule — and the conversion is reachable **only** through the operator-review gate. (README L216; I4.)
- **AC5 (schema deference):** C35 writes only C20-declared `override` fields; introducing a new field is a change request to C20, verified by C20's bead-schema validation rejecting unknown fields (D-3).
- **AC6 (native-hooks-only):** detection uses Claude Code's native hook surface via C28 with no custom hook engine present (I5).
- **AC7 (F10 closure):** no detected override exists only in conversation/chat — every one is retrievable from the bead store by type. (F-MODE-COVERAGE L31.)

**Test strategy (sweep-1):** unit-test the recognition predicate against override vs non-override tool-call fixtures; integration-test the hook→bead write against a C28 hook + C20 schema stub; test surfacing against a seeded `override` log (recurring and non-recurring); contract-test the rule-emission handoff against C10/C15/C30 rule-registration stubs; assert the operator gate is mandatory on the conversion path. (Concrete cases → sweep-2.)

## 9. Open questions (→ review-log)

- **OQ1 (G43, top):** The four v4 docs disagree on P8 maturity (§3.1 "surfaces as rules" vs §6 "DIY/None" vs README Phase-0 omits P8 vs Phase-3a builds it vs F10 leans on it). Spec rules: automated scope = detect→why→log→surface, conversion = operator-gated. **Needs review-log confirmation** that F10's "Addressed" status is only valid from Phase 3a, and that no earlier phase silently depends on the override loop.
- **OQ2:** What precisely counts as an "operator override of the system"? The recognition predicate is the load-bearing custom piece and v4 never defines its boundary (operator-initiated tool deny? edit-against-a-gate? force past a failing linter? all of these?). Predicate definition + the hook event-payload fields it reads → sweep-2.
- **OQ3:** Is the recurring-pattern report itself persisted as a bead (a new C20 type) or kept transient/re-derivable? Sweep-1 treats it as transient; a persisted "pattern" type would be a C20 change request (D-3).
- **OQ4:** Rule-conversion encoding per sink — and **which sinks are in scope**. v4 names only the **C30 Inspect-AI rubric** (README L216); the **C10 (EARS/INCOSE) and C15 (Mammoth)** sinks are a faithful inference (§3 contract-6 [FAITHFUL-FILL]), not v4-named, and are not C35 inventory dependencies. **Confirm with the orchestrator whether the override loop converts to C10/C15 at all, or only to the Inspect-AI rubric.** If retained, C35 targets up to three different rule schemas (each owned by its sink); confirm each handoff format at sweep-2.
- **OQ5:** Recurrence threshold + false-positive policy for the predicate (how many recurrences = a pattern; how predicate false-positives are pruned) — unquantified by v4; sweep-2.
