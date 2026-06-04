# Panel review 05 — the self-bootstrapping / feasibility skeptic

> Reviewer angle: I have watched "the system builds itself" plans fail at exactly the seam
> where an *architecture-of-record* is asserted to be a *buildable* spec. I pressure-test whether
> the recursion actually closes on B12, or whether the conversion step is hand-waved.

## 1. Verdict

**`accept-with-named-amendments`.**

The plan's spine is honest where it counts: it earns the green light before reading it (Gate 1
calibration as a *precondition*), keeps `oversight_level = full` until the judge clears a bar, and
treats `no_go` as an accepted finding, not a failure to hide. That is the opposite of a
magical-recursion plan — why I do not reject. But the recursion does **not** close as cleanly as
Gate 3 asserts, and the plan obscures the seam most likely to break it: the agent-os→C08 conversion
and the gene-transfusion grounding for B12. Three amendments are required before it is safe to run.

## 2. Top 3 named amendments

**A1 — B12 is NOT dependency-free; its DoD reaches into runtime the plan cannot exercise.**
*Problem:* the plan picks B12 as the first real code build on the grounds it is "pure JSON-Schema +
Python, no cluster, no upstream" ([§2 Gate 3](../10-unified-plan.md); grounding
[A0](../00-grounding-and-exemplar.md)). The B12 spec contradicts this: *cited fact* —
`spec-B12.md` §3 lists **HARD upstream A4 (Knative+NATS broker) and B8 (event adapters)**, and
`plan-B12.md` §3.1 marks both `(HARD)`. The "no cluster" claim is true only for the *test tier*
(`spec-B12.md` §8: PyTest yes, Chainsaw/Playwright N/A) — but B12's own acceptance criteria reach
past it: AC-B12-06 ("a published schema is retrievable by an emitter for pre-publish validation and
by an external subscriber") describes runtime contract behavior with A4/B8, not a unit test.
*Fix:* split B12's DoD at Gate 2 into a **clusterless-scoreable core** (REQ-01..05, 09 — the
validators and CI gate, genuinely PyTest-bound) and a **deferred runtime half** (REQ-06 publish,
the B8/emitter contract) explicitly marked twin/cluster-gated, exactly as Gate 5 already does for
B16/B6. Otherwise the first `go` certifies a partial component and the bootstrap bar is quietly
weakened — the precise gaming D-42 exists to prevent.

**A2 — gene-transfusion has no named exemplar for B12, and C51 forbids leaning on the obvious one.**
*Problem:* C52 *requires* C51's predicate to pass before deploy, and C51 mandates ≥1 concrete
external exemplar the build "behaves like" (*cited fact:* `C51-gene-transfusion.md` §1, §3.0; the
≥1-exemplar invariant, B55). For "a CloudEvent schema registry enforcing a closed-namespace +
mint-on-break invariant," the plan names **no exemplar**. Worse, C51 §1 explicitly **excludes
substrate / adopted OSS** from transfusion ("CloudEvents, JSON-Schema … are adopted, not transfused,
and carry no `transfused_from`") — so the natural candidates (a Confluent/Apicurio registry) are
either out-of-discipline or licensing-gated (`check_declaration`, C51 §3.0). *Fix:* Gate 3 must
*name and license-clear* B12's exemplar **before** dispatch, and record what happens when none
exists: per C51 §1 the bet-failure fallback ("factory cannot reliably transfuse *this*") fires —
which means B12 may be the wrong *first* code build, not because it needs a cluster but because it
has no transfusable gene. Pick a first build whose exemplar is real and permissive.

**A3 — the C11→C08 conversion is human-authored, not factory-mechanical; the plan implies otherwise.**
*Problem:* the plan treats "run B12 through the intent crucible (C11) → buildable C08 spec"
([§2 Gate 3](../10-unified-plan.md)) as a mechanical step. *Cited fact:* C11's 9 fields — including
the one anchoring C51's completeness check — are reverse-engineered, and GF-C is undefined
(`C11-intent-intake.md` OQ-1: "the 9 field names are a FAITHFUL-FILL … GF-C itself is undefined …
**the load-bearing ambiguity for C11**"). C51's completeness anchor (named exemplar behaviors) is
*operator-supplied at C11 intake*, not extracted (`C51-gene-transfusion.md` §3.0.1). So a **human**
hand-authors the named-behavior list and DoD the transfusion predicate then grades against. *Fix:*
Gate 3 must state the crucible→C08 step is **human-authored**, and add the named-behavior list to the
Gate-3 evidence bundle — stopping "the factory converted the spec" from masking the narrower true
claim "a human wrote the buildable spec; the factory built against it."

## 3. The single place the recursion is most likely to NOT close

**At the agent-os-spec → C08-DoD conversion, where an architecture-of-record's `[PROPOSED — not in
source]` holes become the C08 Definition-of-Done.** B12 is riddled with them: `spec-B12.md` §4.2
flags the registry layout, schema-id convention, tooling command names, and even the
`platform.capability.changed` payload as `[PROPOSED — not in source]` (R1 "high," R3 "med"). These
are exactly the dimensions the held-out scenarios (`AC-B12-01..06`) score. When the spec's contract
is under-determined, the triangle's `root_cause` will land on **spec** for legitimately ambiguous
reasons — and the plan's own router (C52 §5.0.1 INVARIANT-AG) then forbids the worker from resolving
it, routing every such miss to independent spec correction. The likely failure is not a dramatic
crash but a **`no_go` loop that exhausts `max_attempts`** (C52 §5.0.3, E-C52-08) and triggers the
"factory needs more substrate" exit — when the real defect was that an *architecture* spec was fed
where an *implementation* spec was needed. That fallback is **not actionable as written**: "needs
more substrate" names no missing component, because the missing thing is a human spec-authoring pass,
not a factory capability. Amendment A1+A3 convert this dead-end into a diagnosable one.

## 4. What the plan gets right about feasibility that must be preserved

- **Calibration as a hard precondition, not a smoke test** ([§2 Gate 1](../10-unified-plan.md)):
  the plan refuses to trust `root_cause` until a human-labelled all-five-corners sample measures the
  **false-green rate**. Without this the entire recursion is a confidence trick; keep it load-bearing.
- **The `no_go` branch is a first-class, shipping-blocked terminal** matching C52 §5.0.3 /
  C53 fail-branch — the factory does not deploy under attempt exhaustion. Preserve this exactly.
- **Cost is measured on the *first* build and governs fan-out width** ([§2 Gate 3/5](../10-unified-plan.md)),
  not asserted to amortize — the honest answer to the single-Max-seat multiplicative-judge risk
  (grounding [A6](../00-grounding-and-exemplar.md)).
- **The twin gap is surfaced as the next factory-build empirically**, by the ledger, rather than
  scheduled by faith ([§4](../10-unified-plan.md)). That is the correct way to discover the recursion's
  real boundary.
