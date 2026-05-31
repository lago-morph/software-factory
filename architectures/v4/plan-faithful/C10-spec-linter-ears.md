# C10 — Spec linter (EARS / INCOSE) (`spec-linter-ears`)  (Build Plan, Track A)

> Source / Spec ref: spec/C10-spec-linter-ears.md
> Track: A (faithful). Sweep: 1 (architecture altitude — plan names the workstreams and the contracts to freeze; per-rule fixtures land at sweep 2/3).

## 1. Work breakdown

Ordered tasks. Size S/M/L. Prerequisites by task id / component id.

| id | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Freeze C10 I/O contract** as a C17 deterministic tool node over the C02 ABI: declared inputs (`spec_path`, term-registry path, rule config) → status (exit code) + declared output (findings report). | S | C17, C02 ABI frozen; C08 §3.2 lint contract |
| T2 | **Define the findings-report schema** (`rule_id`, `severity`, `location`, `message`) and pick serialization (defer JSON/SARIF choice to sweep 2 per OQ-4); stub it so dependents can read it. | S | T1 |
| T3 | **Author the rule-set definition** (the in-pack rule table): enumerate the EARS patterns + INCOSE R7–R35 rules, each as `rule_id` + default severity + mechanically-checkable flag. (Sweep-2 deepens to per-rule detectors.) | L | spec §3.3 |
| T4 | **Implement EARS pattern conformance detectors** (ubiquitous / event `When` / state `While` / unwanted `If…then` / optional `Where`; single actor; measurable "shall" response). | L | T3 |
| T5 | **Implement INCOSE R7–R35 structural detectors** (active voice, vague-term list, escape clauses, compound and/or, defined-terms, pronouns, units, negation). Mechanically-checkable rules first; heuristic/best-effort rules flagged. | L | T3 |
| T6 | **Implement the F38 vocab-lint rule** against C07's TOML term registry: load registry, flag undefined terms / non-canonical aliases; graceful skip-with-warning if registry absent. *DEFERRED — orchestrator decision (review RC10-01): SURVIVOR-PASS C10 #04 drops "vocab-lint wired to C07", but F-MODE:74 + C07's frozen spec assign F38 ownership to C10. T6 stays planned as-authored pending that ruling; if DROP #04 is upheld literally, T6 (and Workstream C, AC-4) are removed. Recommended: keep T6, scope the drop to the C07 content-hash machinery only.* | M | C07 §3.2 registry; T2 |
| T7 | **Requirement-statement extraction** over free-form Markdown (heuristic per spec §3.3 / OQ-3): identify candidate requirement sentences/list-items; warn (not error) on un-parseable prose. | M | T1 |
| T8 | **Blocking/advisory disposition** wiring to C03 config (INV-3): default advisory (zero exit + report); per-rule-class opt-in to blocking (nonzero exit). | S | T1, C03 |
| T9 | **Package as a Gas City pack** with a `[[tool]] type="subprocess"` declaration (C02) so it places as a C17 deterministic node; record `transfused_from` (gene-transfusion of an existing EARS implementation, C51). | M | T1, T4–T6 |
| T10 | **Test corpora + acceptance suite** (AC-1…AC-7): positive EARS corpus, one negative spec per anti-pattern, in/out-of-registry vocab corpus, determinism (run-twice diff), blocking-config matrix. | M | T4–T8 |

## 2. Dependency graph

**Must precede C10 (external, Batch 1):**
- **C08** spec-artifact format (the input surface; lint contract C08 §3.2) — must be frozen.
- **C07** term registry §3.2 (the F38 allow-list data) — registry format frozen.
- **C17 / C02** tool-node abstraction + ABI (declared inputs → status + outputs) — frozen.
- **C03** config layering (the optional-enable + blocking disposition) — shape known.

**Critical path:** C08+C07+C17/C02 frozen → **T1** (I/O contract) → **T2** (report schema) → **T3** (rule
table) → **T4/T5/T6** (detectors, parallel) → **T9** (pack) → **T10** (acceptance). T1→T2→T3 is the serial
spine; everything else fans out.

**Can run concurrently with C10:** C09 (prompt binding), C11 (intent intake) — sibling Spec-Intake
components that share C08 but do not depend on C10.

## 3. Parallelization

Once **T1–T3 (contracts + rule table)** are frozen, the detector implementations fan out cleanly because
each rule is an independent, stateless function over the same parsed input:

- **Workstream A:** T4 EARS pattern detectors.
- **Workstream B:** T5 INCOSE R7–R35 structural detectors (further splittable rule-by-rule — each Rxx is an
  independent detector against the frozen report schema).
- **Workstream C:** T6 F38 vocab-lint (only this stream touches C07; isolatable).
- **Workstream D:** T7 requirement-statement extraction (the shared parse front-end all detectors consume —
  freeze its output shape early so A/B/C build against a stub).

T8 (config), T9 (packaging), T10 (tests) gather the streams. The natural fan-out unit is **one detector per
rule_id** — the rule table (T3) is the contract that lets N detectors be authored in parallel.

## 4. Interfaces-first / contract milestones

Freeze these first so dependents and parallel streams build against stubs:
1. **C10 tool-node I/O contract (T1):** declared inputs (`spec_path`, registry, config) → exit-code status
   + findings-report output, expressed in the C17/C02 vocabulary. This is what lets C10 be *placed in a
   formula* before any detector exists.
2. **Findings-report schema (T2):** `rule_id`/`severity`/`location`/`message`. Every detector and every
   consumer (author loop, C39 fix-task, C46 meta-metric) reads this — freeze it before T4–T6.
3. **Rule-table definition (T3):** the enumerated EARS + Rxx rule ids + default severities. The contract the
   parallel detector streams divide along.
4. **Parsed-input / requirement-extraction shape (T7 output):** the front-end shape detectors consume —
   stub early so A/B/C don't block on D.

## 5. Risks & de-risking order

Spike in this order to retire the most uncertainty:
1. **OQ-1 blocking-vs-advisory** (highest leverage): confirm with C03/integrator whether the linter ever
   hard-gates or is always advisory. Drives T8 and the AC-6 expectation. Spec picks advisory-by-default;
   validate before building blocking semantics.
2. **OQ-2 / R7–R35 mechanical checkability:** prototype 3–4 representative INCOSE rules to confirm how many
   are mechanically detectable vs. require best-effort heuristics — this sizes T5 and the "heuristic finding"
   degrade path. Biggest unknown in the rule set.
3. **OQ-3 requirement extraction over free-form Markdown:** spike T7 against the real one-shot-specs corpus
   (one-shot Part 1 examples) to see whether heuristic statement-extraction is good enough without a required
   spec structure (depends on C08 OQ-2). De-risks false-positive/negative rate.
4. **Gene-transfusion source (C51):** identify the EARS/INCOSE implementation to transfuse from
   (README:108 "any EARS-rule implementation") early, since it shapes T3–T5 and the `transfused_from` record.

## 6. Definition of done

**Per-component (sweep-1 exit):**
- C10 places as a C17 deterministic tool node via the C02 ABI, no model call (AC-7, AC-2).
- EARS + INCOSE R7–R35 + F38 vocab rules run over a C08 spec body and emit the structured findings report
  (AC-1, AC-4, AC-5).
- Deterministic and read-only (AC-2, AC-3).
- Advisory-by-default with config-gated blocking wired to C03 (AC-6).
- Test corpora (positive / negative-per-anti-pattern / vocab / determinism / blocking-matrix) pass (AC-1…7).
- `transfused_from` recorded (C51 discipline).

**Per-task:** each Txx exits when its acceptance slice passes — e.g. each detector (T4/T5) ships with its
positive+negative fixture; T6 with in/out-of-registry fixtures; T7 with the un-parseable-prose warn case.

**Carried to sweep 2:** per-rule Rxx→detector+severity table (OQ-2), findings serialization choice (OQ-4),
sequence diagram, and concrete rule-by-rule fixtures.
