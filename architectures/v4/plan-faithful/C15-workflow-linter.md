# C15 — Workflow linter (Mammoth 21-rule) (`workflow-linter`)  (Build Plan, canonical track)

> Source / Spec ref: spec/C15-workflow-linter.md
> Track: canonical (single track; D-6). Sweep: 1 (architecture altitude — plan names the workstreams and the contracts to freeze; the per-rule Mammoth-21 fixtures land at sweep 2/3).

## 1. Work breakdown

Ordered tasks. Size S/M/L. Prerequisites by task id / component id.

| id | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Freeze C15 I/O contract** as a C17 deterministic tool node over the C02 ABI: declared input (`formula_dot` — the C14 DOT export — + rule config) → status (exit code) + declared output (findings report). | S | C17, C02 ABI frozen |
| T2 | **Define the findings-report schema** (`rule_id`, `severity`, `location`, `message`); `location` is graph-shaped (node id / edge / cycle path). **Share the schema with C10** (same report shape); defer JSON/SARIF serialization to sweep 2 (OQ-4). Stub it so dependents can read it. | S | T1 |
| T3 | **Pin the DOT-surface contract with C14** (OQ-2, the top open question): the node/edge graph C14 exports must carry stable **node ids**, the **edge set**, and **loop-construct markers** (so a bounded loop is distinguishable from a raw back-edge). C14 **is specced at sweep-1** (`spec/C14-formula-dot-translator.md` §3.1 names node ids / `kind=` attr / edges), but its **attribute-level encoding is C14 sweep-2** and the **loop-marker encoding is C14:OQ-2** — so this task pins the attribute contract C15 needs against C14 sweep-2. | M | C14 §3.1 surface (specced); C14:OQ-2 / C12:OQ-2 loop encoding; C12 §3/§4 node/edge + acyclicity model |
| T4 | **Author the rule-set definition** (the in-pack rule table): the **21 Mammoth structural rules**, each as `rule_id` + default severity + structural class (cycle / reachability / entry-exit / dangling / chain-bound). Fixed table, **not** a pluggable registry. (Sweep-2 deepens to per-rule detectors from the Mammoth source.) | M | spec §3.3; T3 |
| T5 | **Implement structural detectors** over the parsed graph: cycle/acyclicity (back-edge vs. bounded-loop), reachability/orphan, entry/exit well-formedness, dangling-edge, chain-length/fan-out bound. Textbook DAG algorithms — independently writable (de-risks G30 license fallback). | L | T2, T3, T4 |
| T6 | **Graph front-end** — parse the C14 DOT export into the node/edge model all detectors consume; clean-fail on un-parseable DOT (single high-severity finding). | M | T3 |
| T7 | **Blocking/advisory disposition** wiring to C03 config (INV-3): default advisory (zero exit + report); per-rule-class opt-in to blocking (nonzero exit). Mirror C10's disposition mechanism. | S | T1, C03 |
| T8 | **Package as a Gas City pack** with a `[[tool]] type="subprocess"` declaration (C02) so it places as a C17 deterministic node; record `transfused_from` = Mammoth (gene-transfusion, C51) — code-port or pattern-reimplement per the G30 license outcome (T0-license). | M | T1, T5 |
| T9 | **Test corpora + acceptance suite** (AC-1…AC-8): positive DAG corpus, one negative formula per malformation class, the **boundary corpus** (structurally-sound-but-wrong-kind → zero C15 findings, proving the C15/C16 split, AC-4), determinism (run-twice diff), blocking-config matrix. | M | T5–T7 |
| T0-license | **Verify Mammoth's license** (G30 / OQ-3) — README:134 states MIT, README:301/§508/§551 say "verify". Decide **code-port vs. pattern-reimplement** before T4/T8 finalize. Spike-priority (§5). | S | — (do first) |

## 2. Dependency graph

**Must precede C15 (external):**
- **C14** formula↔DOT translator — the DOT export surface C15 lints (inventory `Depends on → C14`). **C14 is
  specced at sweep-1** (`spec/C14-formula-dot-translator.md`): the named `export` surface (node ids, `kind=`
  attr, directed edges) exists, but its **attribute-level DOT encoding is C14 sweep-2** and the **loop-marker
  encoding is C14:OQ-2** — so the T3 attribute contract is the load-bearing blocker; until C14 freezes those
  at sweep-2, C15 builds against a *stub DOT* matching the T3 contract.
- **C12** formula format — the node/edge + acyclicity/loop model the rules reason about — must be frozen
  (it is: `spec/C12-formula-pipeline-file.md` exists).
- **C17 / C02** tool-node abstraction + ABI (declared input → status + output) — frozen.
- **C03** config layering (the optional-enable + blocking disposition) — shape known.

**Critical path:** C14 DOT-surface contract (**T3**, gated on C14's *sweep-2* attribute encoding + C14:OQ-2
loop markers) → **T1** (I/O contract) → **T2** (report schema) → **T4** (rule table) → **T5/T6** (detectors +
front-end) → **T8** (pack) → **T9** (acceptance). **T0-license** runs in parallel from the start and must land
before T4/T8 finalize. The single biggest schedule risk is **C14**: T3 cannot fully freeze until C14's
attribute-level DOT surface + loop encoding (C14:OQ-2) land at sweep-2, so stub-against-contract early.

**Can run concurrently with C15:** **C16** discipline linter (sibling on the same formula, disjoint concern)
and **C14** itself (C15 consumes C14's output but the two can be built in parallel against the frozen T3
contract).

## 3. Parallelization

Once **T1–T4 (I/O + report schema + DOT-surface contract + rule table)** are frozen, the detector
implementations fan out cleanly because each structural rule is an independent, stateless function over the
same parsed graph:

- **Workstream A:** T5 cycle/reachability detectors (the DAG-algorithm core).
- **Workstream B:** T5 entry-exit / dangling-edge / chain-bound detectors (further splittable rule-by-rule —
  each of the 21 `rule_id`s is an independent detector against the frozen report schema).
- **Workstream C:** T6 the DOT graph front-end (the shared parse layer all detectors consume — freeze its
  node/edge output shape early so A/B build against a stub).
- **Workstream D (off the critical path, do first):** T0-license verification + T3 C14-contract negotiation —
  the two external unknowns; resolving them unblocks A/B/C.

T7 (config), T8 (packaging), T9 (tests) gather the streams. The natural fan-out unit is **one detector per
rule_id** — the rule table (T4) is the contract that lets the 21 detectors be authored in parallel.

## 4. Interfaces-first / contract milestones

Freeze these first so dependents and parallel streams build against stubs:
1. **C14 DOT-surface contract (T3):** stable node ids + edge set + loop-construct markers. **The top
   milestone** — C15's whole input depends on it; C14 is specced at sweep-1 but its **attribute-level
   encoding + loop markers are C14 sweep-2 / C14:OQ-2**, so pin the attribute contract C15 needs against
   that surface (OQ-2). Lets C15 build against a stub DOT before C14's sweep-2 encoding freezes.
2. **C15 tool-node I/O contract (T1):** declared input (`formula_dot`, config) → exit-code status +
   findings-report output, in the C17/C02 vocabulary. Lets C15 be *placed in a formula* before any detector
   exists.
3. **Findings-report schema (T2):** `rule_id`/`severity`/`location`/`message`, **shared with C10**. Every
   detector and every consumer (author loop, C39 fix-task, C46 meta-metric) reads this — freeze before T5.
4. **Rule-table definition (T4):** the 21 enumerated rule ids + default severities. The contract the parallel
   detector streams divide along.

## 5. Risks & de-risking order

Spike in this order to retire the most uncertainty:
1. **T0-license / G30 (Mammoth license + the 21 rules)** — highest leverage and an external unknown.
   README:134 says MIT but v4 itself flags "verify" (README:301/§508/§551). Verify *first*; if non-permissive,
   commit to **pattern-reimplementation** (the structural rules are textbook DAG algorithms — see risk 3),
   recording `transfused_from` as pattern-only. Also document the **exact 21 rules** (AI-CONTEXT §509 open
   item), since the rule table (T4) and `transfused_from` record depend on it.
2. **OQ-2 / C14 DOT surface** — the load-bearing dependency. C14 **is specced at sweep-1** (named surface:
   node ids, `kind=` attr, edges), but its **attribute-level encoding is C14 sweep-2** and the
   **loop-vs-back-edge marker is C14:OQ-2**; confirm the DOT export will carry the node ids, edges, and the
   loop-vs-back-edge distinction C15's cycle rule needs. If C14's round-trip is lossy on that topology, fall
   back to reading the C12 AST directly. Spike against a hand-written DOT export of a real formula early.
3. **Re-implementability of the 21 rules** — prototype 3–4 representative rules (cycle detect, reachability,
   chain-length) to confirm they are mechanically detectable from topology alone (they are — standard graph
   algorithms). This both sizes T5 *and* de-risks the G30 license fallback (proving C15 is buildable without
   Mammoth's Go).
4. **OQ-1 blocking-vs-advisory** — confirm with C03/integrator whether any structural class (e.g. a true
   cycle) hard-gates by default, given C01's loader is the real execution gate. Drives T7 and the AC-6
   expectation. Spec picks advisory-by-default; validate before building blocking semantics.

## 6. Definition of done

**Per-component (sweep-1 exit):**
- C15 places as a C17 deterministic tool node via the C02 ABI, no model call (AC-7, AC-2).
- The Mammoth 21-rule structural set (cycle / reachability / entry-exit / dangling / chain-bound) runs over a
  formula's DOT export and emits the structured findings report (AC-1, AC-5).
- Deterministic, read-only, and **structure-only** — no kind/discipline findings (C16's), no vocabulary
  findings (C10/F38, D-9) (AC-2, AC-3, AC-4).
- Advisory-by-default with config-gated blocking wired to C03 (AC-6).
- Test corpora (positive / negative-per-malformation / **boundary** / determinism / blocking-matrix) pass
  (AC-1…AC-8).
- `transfused_from` = Mammoth recorded (code-port or pattern-reimplement per G30 outcome) — C51 discipline,
  with the license verification (T0-license) completed (AC-8).

**Per-task:** each Txx exits when its acceptance slice passes — e.g. each detector (T5) ships with its
positive+negative fixture; T6 with the un-parseable-DOT clean-fail case; T9 with the boundary corpus proving
the C15/C16 split.

**Carried to sweep 2:** the per-rule (21× `rule_id`→detector+severity) table from the Mammoth source
(OQ-3), findings serialization choice shared with C10 (OQ-4), the frozen C14 DOT-surface contract once C14's
sweep-2 attribute encoding + C14:OQ-2 loop markers land (OQ-2), the sequence diagram, and concrete
rule-by-rule fixtures.
