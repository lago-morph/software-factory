# Doc Templates

Canonical shapes for every per-component artifact. Builders fill these; depth grows sweep over sweep.

---

## Spec doc template — `spec-<track>/<ID>-<slug>.md`

```
# <ID> — <Component Name>  (Spec, Track <A|B>)

> Source: <v4 doc + section refs>
> Inventory ID: <ID>   Kind: <kind>   Status: <sweep-1|sweep-2|sweep-3>
> [Track B only] Deltas: <DELTA-NN list, or "none">

## 1. Purpose & responsibility
What this piece is responsible for; what it explicitly is NOT.

## 2. Context & dependencies
Upstream/downstream pieces (by inventory ID); where it sits in the system.

## 3. Interfaces / contracts
Inbound and outbound interfaces. Sweep 1: named + described. Sweep 2: concrete signatures, schemas,
API contracts, message formats. Pre/postconditions and invariants.

## 4. Data model / state
Owned state, schemas, lifecycle, persistence, consistency requirements.

## 5. Behavior
Key flows, control loops, state transitions. Sweep 2+: sequence/state diagrams (Mermaid),
algorithms/pseudocode (sweep 3).

## 6. Failure modes & handling
Which F-modes apply; detection, mitigation, recovery; degraded behavior.

## 7. Cross-cutting (security / cost / scale / observability / ops)

## 8. Acceptance criteria & test strategy
How we know it's correct. Sweep 2+: concrete test cases.

## 9. Open questions
Unresolved items → mirrored into _meta/review-log.md.
```

---

## Plan doc template — `plan-<track>/<ID>-<slug>.md`

```
# <ID> — <Component Name>  (Build Plan, Track <A|B>)

> Source / Spec ref: spec-<track>/<ID>-<slug>.md

## 1. Work breakdown
Ordered tasks to build this component. Each task: id, description, est. size (S/M/L), prerequisites.

## 2. Dependency graph
Which tasks/components must precede this; which can run concurrently. Call out the critical path.

## 3. Parallelization
What inside this component can be built by independent workstreams simultaneously. Explicit fan-out.

## 4. Interfaces-first / contract milestones
The contracts to freeze early so dependents can build against stubs in parallel.

## 5. Risks & de-risking order
What to prototype/spike first to retire the most uncertainty.

## 6. Definition of done
Per-task and per-component exit criteria, tied to the spec's acceptance criteria.
```

---

## Adversarial review template — `spec-<track>/<ID>-<slug>.review.md`

```
# Adversarial review — <ID> <Component> (Track <A|B>, sweep <n>)

Reviewer persona: <persona>
Target: spec-<track>/<ID>-<slug>.md

## Findings
For each: ID (R<ID>-NN), severity (blocker|major|minor), claim, evidence/reasoning, suggested fix.
Track A reviewers: attack fidelity/completeness only.
Track B reviewers: attack the design (correctness, cost, simplicity, failure handling, scalability).

## Verdict
accept | accept-with-fixes | needs-rework — one line why.
```
