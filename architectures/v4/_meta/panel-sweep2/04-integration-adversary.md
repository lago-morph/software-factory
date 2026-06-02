# Panel Sweep-2 — 04 · Cross-Product Integration Adversary

**Reviewer angle.** I do not care whether any single component is good. I care whether the 25
components COMPOSE: does each hand-off contract match on BOTH sides (field names, types,
ownership, AND temporal ordering), or do the seams between the 7 products hide contradictions
that only surface at integration? The eval-tier seam adversary already caught one
field-name blocker (`satisfaction_score` vs `score_value`). My job: find the ones that survived
the cluster reviews because each cluster reviewer only saw its own side of the seam.

**Sources read (targeted):** the five cluster seam-reviews
([gascity](../gascity-cluster-seam-review.md), [claudemax](../claudemax-cluster-seam-review.md),
[specintake](../specintake-cluster-seam-review.md), [evaltier](../evaltier-cluster-seam-review.md),
[fence-bootstrap](../fence-bootstrap-cluster-seam-review.md)); ledger decisions **D-31..D-40**
in [review-log.md](../review-log.md); and spot-checks of the actual specs on the critical path:
`C05`, `C09`, `C20`, `C31`, `C32`, `C33`, `C41`, `C42`, `C52`, `C53`.

---

## VERDICT: `right-idea-change-X-before-building`

The seam discipline is real and the cluster reviews did good work: the
`satisfaction_score`/`score_value` blocker is genuinely fixed corpus-wide; the C31→C32
TrajectoryLog chain closes with a version-pin guard; D-29 `created_by` wire-type is consistent;
the D-36 "C33 writes to C19 beads not CXDB" boundary holds; D-31 multi-rig propagated into
C42/C01/C03/anchor. **The intra-cluster seams are largely sound.**

But the cluster decomposition created exactly the blind spot it was designed to risk: **seams
that cross TWO cluster reviews fell between the chairs.** Each reviewer verified its own side and
trusted the other. I found **four uncaught cross-cluster contradictions**, two of which are
build-blockers, and one of which is a runtime **deadlock at the apex go/no-go (C53)** — the
single most consequential decision in the whole bet-#3 recursion. None of these appear in any of
the five cluster reviews or the other four panel opinions. They are correctable without
architectural change, but they MUST be corrected before building, because each is the precise
class of silent-failure the eval-tier blocker was.

---

## Findings

### INT-1 — BLOCKER — C52↔C53 is a circular hand-off; the bootstrap go/no-go chain does NOT close

This is my sharpest objection. The fence-bootstrap review's RFB-SEAM-03 fix added a
`RubricResult` type alias so that "C52 references a type C53 never defines" became typed. It
verified the **type name** matched. It never traced the **temporal ordering**, which is
mutually contradictory:

- **C52 → C53 dependency.** C52's mandatory deploy gate `submit_for_review(...)` takes
  `c53_rubric_result: RubricResult` as an input parameter (C52 §3.4 line 139; §5 step 6 line
  272: "The gate consumes (a) C51's verdict and (b) C53's `RubricResult`"). So **C53.decide()
  must run BEFORE C52's review gate** to produce the RubricResult.
- **C53 → C52 dependency.** C53's `decide()` takes a `GoNoGoInput` whose **`ReviewVerdict`
  field is "From C52 (human design-review record)"** (C53 §3.1 lines 207-209), and every
  `GoNoGoInput` field is required — "missing any → E-C53-02 (insufficient-evidence)." The
  go/no-go predicate's **Term 3 is `ReviewVerdict == "approve"`** (C53 §3.2 line 259). So
  **C52's review must run BEFORE C53.decide()**.

**C52.submit_for_review needs C53's RubricResult → C53.decide needs C52's ReviewVerdict → … .**
Neither can run first. The chain dead-locks. This is not a paraphrase or readability gap — it is
two `func` signatures each declaring the other's output as its required input.

**Why both reviews missed it:** RFB-SEAM-03 checked `RubricResult == GoNoGoDecision` (a type
identity) and declared the seam "logically coherent." It is type-coherent and ordering-incoherent
at the same time. The cluster review's lens was field-name/type drift; ordering cycles are
invisible to that lens.

**Impact:** C53 is "the apex point of bet #3" (C53 §3.1) and C52:542 calls the bootstrap-
validation prompt "the most consequential thing you write in the first month." If this ships as
specced, the first self-build cannot produce a go/no-go — the two functions wait on each other.

**Change before building:** Split the ordering explicitly. The coherent reading is a
**two-phase** decision: (Phase A) C53 evaluates the *objective* terms it CAN compute pre-review —
Term 0 (scenario-set present), Term 1 (C51 `TransfusionVerdict == pass`), Term 2 (C33
satisfaction bar) — and emits a *provisional* RubricResult with `ReviewVerdict` UNSET; (Phase B)
C52's `submit_for_review` consumes that provisional result, runs the human gate, and the human
*approve* is the final Term-3 conjunct applied either by C52 at gate-close or by a second
C53 call. Pick one and make `GoNoGoInput.ReviewVerdict` optional-until-Phase-B. Freeze the
ordering as a joint C52/C53 Sweep-2 contract. (The substrate-realist's "state ordering as a hard
gate" finding is about *build* sequence; this is a *runtime data-flow* cycle — distinct.)

---

### INT-2 — BLOCKER — `factory_build` status is `completed` in three places and `closed` in C20's own envelope state machine

The fence-bootstrap RFB-SEAM-01 fix added the D-40 `status enum{in_progress, completed}` to
C20 §4.5.3 without reconciling it against C20's **pre-existing universal envelope** status enum.
The result is a flat contradiction inside C20 itself, propagated to C52:

- **C20 envelope (§4.1 line 304):** `status enum{open, in_progress, closed}` — the status field
  EVERY bead carries. **`completed` is not a member.**
- **C20 envelope state machine (§5.1 line 414 + note line 427):** `in_progress --> closed_build :
  build completes (factory_build)`, and explicitly "`closed_build` … carries envelope
  **`status=closed`**." So per C20's own state diagram a finished build is `status=closed`.
- **C20 factory_build extension (§4.5.3 line 343):** `status enum{in_progress, completed}`;
  `advance_to_completed` sets `status=completed`.
- **C52 (§4.1 line 211; §5 state diagram lines 241/247):** writes **`status=completed`**.
- **D-40 verbatim:** transition is "`status: in_progress → completed`".

So C52 writes `status=completed`, a value **illegal under the envelope enum** and **absent from
the envelope state machine** (which terminates finished builds at `closed`). A C34 audit or C54
Phase-3 gate that queries the envelope contract for finished builds (`status=closed`, or any of
the envelope enum) will **never match** the `status=completed` beads C52 writes — a silent query
miss at the bootstrap apex, structurally identical to the `score_value` blocker (a reader looking
for a value the writer never emits).

**Why the review missed it:** RFB-SEAM-01 was scoped to "add the D-40 fields"; it added the new
enum but did not diff it against the envelope enum two sections up in the same file. The
fence-bootstrap reviewer flagged the *type-flip vs status-transition* tension (RFB-SEAM-07) but
not the *enum-value collision* on the shared `status` field.

**Change before building:** Reconcile to ONE lifecycle vocabulary. Either (a) `factory_build`
terminal state IS the envelope `closed` with a `verdict`-style sub-slot distinguishing
`completed` from `abandoned` (matching the existing `closed_build`/`resolved`/`escalated`
pattern at C20 line 427), OR (b) extend the envelope enum to include `completed` and update the
§5.1 state diagram's `closed_build` node + the line-427 note. D-40's verbatim text says
`completed`, so (b) is the lower-friction path — but the envelope state machine and §4.1 enum
MUST be edited in the same pass, or the contradiction just moves.

---

### INT-3 — MAJOR — C09↔C05 disagree on call direction and on when the `DispatchRequest` exists (D-35 fix is half-wired)

The spec-intake review's D-35 fix (RSI-SEAM-02) correctly routed C09's `{{.BeadId}}`/
`{{.CreatedBy}}` render variables to come FROM the C05 `DispatchRequest` instead of a C13 fetch.
But it only touched C09's field table / data model / one sequence-diagram note. It left C09's and
C05's **call-ordering models mutually contradictory**, and left C09 internally self-contradictory:

- **C05's model (gas-city cluster, C05 §5.1 lines 204-206):** `C18 ->> C05: dispatch(DispatchRequest{...})`
  FIRST, then `C05 ->> C09: resolve routing key`, `C09 -->> C05: RoutingKey`. Here C05 is the
  entry point and **C05 calls C09 mid-dispatch**; the DispatchRequest already exists when C09 is
  consulted. C05 §3.4 (lines 140-142): "C09 writes (resolved role); C05 reads."
- **C09's model (spec-intake cluster, C09 §5.1 lines 219, 242-244):** `C12 ->> C09:
  bind_and_render(...)` FIRST; C09 does all the work; only at the end `C09 -->> C05:
  RoutingKey`, then `C05 ->> C05: dispatch(DispatchRequest with RoutingKey)`. Here **C09 is the
  entry point and hands a complete DispatchRequest to C05**; the DispatchRequest is built AFTER
  C09 runs (line 244). AC-C09-10 (line 307) confirms this ordering.

These cannot both hold. And the D-35 fix makes C09 contradict *itself*: line 234 says C09
"extract BeadId from DispatchRequest.bead_id" (DispatchRequest pre-exists), but line 244 builds
the DispatchRequest *after* C09 emits the RoutingKey (DispatchRequest does not exist yet). **If
C09 runs first, there is no DispatchRequest to read `bead_id`/`created_by` from** — which is
exactly what D-35 says C09 must do. The fix is logically valid ONLY under C05's ordering
(DispatchRequest-first), but C09's own sequence diagram encodes the opposite ordering.

**Why both reviews missed it:** spec-intake verified D-35 in isolation (the variable *source*),
gas-city verified C05↔C04 and C05↔C41 and treated C05↔C09 as settled by OQ-1 (an *ownership*
split, not an *ordering* contract). Ownership was reconciled; ordering was never cross-checked.

**Change before building:** Freeze ONE ordering. The only ordering consistent with D-35 is:
**C18/C12 assembles the `DispatchRequest` (with `bead_id`, `created_by`) → C05.dispatch is
invoked → C05 calls C09 to resolve the routing key AND C09 reads `bead_id`/`created_by` from the
already-present DispatchRequest for rendering.** Rewrite C09 §5.1's sequence diagram (lines
219-247) and AC-C09-10 to match C05 §5.1. This is a joint C05/C09 Sweep-2 contract.

---

### INT-4 — MINOR-to-MAJOR — C41 actor-kind enum `{city, rig, agent}` does not admit the `tool:` kind that C17/C32 emit

D-29's wire format is `"kind:id"`, and the gas-city review (RGC-SEAM-04) verified C17/C05 emit
the *string* form correctly. But it checked the *format*, not the *kind vocabulary*:

- **C41 (§3 line 118):** `resolve_actor(created_by) → ActorRef = { kind: "city" | "rig" |
  "agent", id }` — a **closed 3-value enum**. C41 §1 (line 30) calls these "the actor kinds
  (city, rig, agent) that may legitimately appear in a `created_by`."
- **C17 `ToolNodeResult.CreatedBy`** (gas-city review evidence, line 109 of that review):
  example `"tool:inspect_eval"` — kind **`tool`**. The eval tier's `score_record` and trajectory
  artifacts are produced by tool-nodes (C17), so their native `created_by` carries `tool:`.

A `"tool:inspect_eval"` wire value fed to C41's `resolve_actor` would fail — `tool` is not in
C41's closed vocabulary. So either C41's enum is too narrow (it must admit `tool`), or C17 is
emitting an out-of-vocabulary kind. C41 OWNS the vocabulary (D-29 parses to C41's `ActorRef`),
so this is C41's enum to widen — but it is currently a contract mismatch: the attribution
authority does not recognize a kind its own substrate emits.

**Change before building:** Either add `tool` (and confirm whether `pool`/`service` are also
emitted) to C41's `ActorRef.kind` enum, OR have C17 attribute tool-node output under a `rig:` or
`agent:` kind. This is a one-line enum decision but it is load-bearing: C41 is the "cross-cutting
load-bearer that touches nearly everything," and an unresolvable `created_by` breaks the
universality invariant (every action attributable) that F14 depends on.

---

## The 10 ledger decisions (D-31..D-40): mutually consistent? mostly — two propagation gaps

I checked the 10 decisions against each other and against corpus application:

- **Mutual consistency: PASS.** D-31 (multi-rig) ↔ D-32 (rig-spelling file-split) ↔ D-38
  (separate judge rig) compose cleanly: D-38's worker-rig ≠ judge-rig is the canonical instance
  of D-31's N-rigs-per-city, and D-32's `city.toml` array-of-tables spelling is the mechanism.
  D-36/D-37/D-39 (eval tier) are internally consistent and consistent with D-15/D-1. D-40 is
  self-consistent. No decision contradicts another.
- **Propagation gap 1 (D-40):** D-40's verbatim "C20 owns … the `status` slot" was applied as
  a NEW enum value (`completed`) without reconciling C20's pre-existing envelope enum and state
  machine → **INT-2**. D-40 propagated to C52/C53 but left C20 internally inconsistent.
- **Propagation gap 2 (D-35):** D-35 ("C09 vars from C05 DispatchRequest") propagated into C09's
  field table but NOT into C09's sequence-diagram ordering, leaving the seam half-wired →
  **INT-3**.
- D-31/D-32/D-33/D-34 verified present in C42/C01/C03/anchor and C02/C03. D-36/D-37/D-38/D-39
  verified present and applied in C30/C31/C32/C33. The `score_record`/`satisfaction_metric` C22
  registration seams (D-3, eval-tier) propagated correctly into C20's bundle (RFB-SEAM-02 fix
  landed).

## Chains that DO close (credit where due)

- **C31 → C32 TrajectoryLog:** closes. Schema fields match; the REV-SEAM-02 version-pin guard
  (`inspect_version` validated → E-C32-02) is now in C32 §3.1/§7. Sound.
- **C32 → C33 ScoreRecord:** closes post-fix. `satisfaction_score` is canonical in BOTH; the
  12-field D-39 schema maps onto C33's consumed subset (REV-SEAM-09). `trajectory_ref` matches.
- **C33 → C53 SatisfactionDistribution:** the *data* contract closes — C53 reads
  `{n, mean, p10, p50, p90, std_dev}` and the field names match C33 §3.4 exactly (C53 §3.1 line
  240). (The *ordering* problem is at the C52/C53 seam, INT-1, not here.)
- **C09 → C05 RoutingKey, C05 → C04 handoff, C05 → C41/C23 attribution:** the ownership splits
  are clean (OQ-1 resolved); only the C09/C05 *ordering* is broken (INT-3).

## Seams DEFERRED to non-spine components — do any block the spine?

- **C34:OQ-C34-4 / FE-1** (claudemax review): deferred to C34 + FE-1. Does NOT block — C29 emits
  the `cross_family_required` signal; enforcement is a future-enhancement, not Phase-0.
- **C30→C34 E-C30-04 handoff** (eval review REV-SEAM-07): deferred to C34 builder. Does NOT
  block the spine — C30 ships publishing both surfaces; C34 is the next product.
- **C52 OQ5 / G14 class-level fallback → C54** (fence review RFB-SEAM-08): deferred to C54
  phase-plan. Does NOT block the *build* of the spine; it is a hedge for *transfusion
  reliability* (bet #3 risk), legitimately a C54 sequencing question.
- **C13 (molecule):** correctly kept OUT of the spine by D-35; the only risk was C09 pulling it
  in for render vars, which D-35 closed. No spine block.

None of the non-spine deferrals block the spine. The blocking issues (INT-1, INT-2) are all
*inside* the spine, at seams the cluster reviews split across two reviewers.

---

## Sharpest objection (one sentence)

**The bootstrap go/no-go — the apex of bet #3 — is specced as a deadlock: C52's deploy gate
takes C53's RubricResult as input while C53's decision takes C52's review-approve as input, so
neither function can run first, and the fence-bootstrap review's "fix" verified the type name
matched without ever checking that the two signatures each require the other's output (INT-1).**

## Change-before-building (ranked)

1. **INT-1 (BLOCKER):** Break the C52↔C53 cycle with an explicit two-phase ordering; make
   `GoNoGoInput.ReviewVerdict` optional-until-Phase-B. Joint C52/C53 Sweep-2 freeze.
2. **INT-2 (BLOCKER):** Reconcile the `factory_build` status vocabulary — `completed` must
   either join the envelope enum + state machine (D-40-faithful) or collapse to `closed` + a
   verdict slot. Edit C20 §4.1, §4.5.3, AND §5.1 in one pass.
3. **INT-3 (MAJOR):** Freeze ONE C09↔C05 call ordering (DispatchRequest-first, the only ordering
   D-35 is consistent with); rewrite C09 §5.1 + AC-C09-10 to match C05 §5.1.
4. **INT-4 (MINOR→MAJOR):** Widen C41's `ActorRef.kind` enum to admit `tool` (and audit for
   `pool`/`service`), or re-attribute C17 tool-node output to an existing kind.
