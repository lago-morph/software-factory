# Adversarial review — C23 Event Bus (Track B, sweep 1)

Reviewer persona: Subsystem Adversary — Persistence & Memory
Target: spec-optimized/C23-event-bus.md
Charter: Track B → attack the DESIGN hard. Are the [DELTA]s justified, or hidden coupling / over-build?

## Findings

### RC23B-01 — major — DELTA-01 "gap-free monotonic seq" + DELTA-04 "single-writer per stream" is a real constraint that conflicts with "all actors are producers" (§2)
**Claim.** DELTA-01 promises a **gap-free** per-stream `seq`; DELTA-04 partitions streams per-`run_id`/
actor and relies on "single-writer-per-segment (no global lock)." §2 lists producers as C19, C20, C28,
C35, C41 "and in principle every component that takes an action." **Evidence.** Gap-free `seq` is only
cheaply achievable with a *single writer* per stream. But a per-`run_id` stream has *many* concurrent
actor-producers (the agent loop C28, the bead store C19 emitting `BeadMutationEvent`, C41 attribution,
overrides C35) all appending to the same run's stream. So either (a) the stream is per-`run_id` and gap-
free `seq` requires a per-stream lock/sequencer (re-introducing the contention DELTA-04 claims to avoid),
or (b) the stream is per-*actor* (truly single-writer) but then a *run's* total order is lost (you can't
replay "what happened in run R in order" without merging N actor streams, breaking the C21 replay and
C40 trigger model that assume a run-ordered stream). DELTA-04's "single-writer-per-segment" and DELTA-01's
"gap-free per `run_id`" are in tension. **Fix (applied).** Flagged the tension in the spec: either drop
gap-free to *monotonic-but-possibly-gapped* under a per-run multi-writer sequencer, or make the
partition granularity per-actor and define an explicit run-order merge for replay. Tied to OQ1 (which
already raises granularity but not this specific gap-free-vs-multi-writer conflict).

### RC23B-02 — major — DELTA-03 resolves C19-OQ1 and C21-OQ2 *for* those components — a Track-B spec deciding sibling components' open questions is a cross-spec overreach
**Claim.** DELTA-03 states "**resolves C19-OQ1 and C21-OQ2** by making the bus at-least-once and pushing
dedup to content-addressed consumers." §3/§6 repeat this. **Evidence.** C19 and C21 are separate
components with their own adversary passes; C23 unilaterally closing *their* open questions in *its* delta
header is a coupling/authority overreach — C19's "event-bus-down policy" (C19-OQ1) and C21's spool
ordering (C21-OQ2) are decisions those specs (and the integrator) must ratify, not ones C23 can declare
resolved. The *substance* (at-least-once + idempotency key) is good and the right call; the *framing*
("resolved") is wrong — it should be "C23 *offers* at-least-once + `event_id` so C19/C21 *can* resolve
their OQs this way, pending their confirmation." **Fix (applied).** Reworded DELTA-03 and §6 from
"resolves C19-OQ1/C21-OQ2" to "*provides the mechanism that lets* C19/C21 close those OQs, subject to
their confirmation" — keeping the delivery semantics, dropping the unilateral-resolution claim.

### RC23B-03 — major — DELTA-01 "fsync on every Append before return" vs DELTA-02 "Append latency independent of consumers" is fine, but fsync-per-event on the hottest path has no throughput budget
**Claim.** DELTA-01: the record is "fsync-durable … before the call returns"; §8 AC-1 tests this under N
concurrent appends. **Evidence.** Every bead mutation, every agent action, every override, every
attributed action calls `Append` (§2 "record every action") — and each does a synchronous fsync. fsync
per event on a busy run is a well-known throughput cliff (hundreds–low-thousands/s per device without
group-commit). The spec mandates per-Append fsync durability (load-bearing for C21's G33 fallback) but
gives no group-commit / batched-fsync story, and §7 only says "per-stream throughput ceiling … must be
sized in sweep-2." For "the cheapest, most durable store" that three other components fall back to, the
durability/throughput tradeoff is the central design question and is deferred. **Fix (applied).** Added a
group-commit allowance to DELTA-01: durability is "fsync-durable before return, with group-commit
batching permitted so long as `Append` does not return until the batch is on stable storage" — preserving
the C21-fallback durability guarantee while not mandating one-fsync-per-event. Sized in sweep-2.

### RC23B-04 — major — DELTA-05 retention low-water-mark = `min(committed_seq)` over consumers creates an unbounded-disk DoS via one dead consumer; OQ4 raises it but the default is unsafe
**Claim.** DELTA-05: prune below `min(committed_seq)` over *registered durable consumers*, so "the bus
never prunes data a registered consumer hasn't ingested." **Evidence.** This means a *single* stuck/dead
registered consumer (a crashed C24 bridge, a wedged Order) pins the low-water-mark forever and the log
grows without bound until disk fills — a cascading failure *worse* than the G33 case DELTA-02 claims to
solve (one dead consumer now stalls the whole factory via disk exhaustion). OQ4 flags the max-age-vs-
durability knob but the spec's *default* (`min(committed_seq)`, no max-age escalation wired) is the unsafe
one. **Fix (applied).** Made the retention contract explicitly two-bounded: prune at
`max(min(committed_seq), head − max_age_or_size_bound)` — i.e. a dead consumer cannot pin the log past a
hard age/size ceiling; crossing it emits a `consumer-lag` alarm AND prunes (accepting that a permanently-
dead consumer loses un-ingested tail, which is correct vs. filling disk and stalling everything). Tied
the escalation (page vs degrade) to C56/C57 per OQ4.

### RC23B-05 — minor — `EventBus` port + file-only fallback (DELTA-01 / AC-8) duplicates the C21 DELTA-01 port pattern; justify or it's speculative generality
**Claim.** §3 offers an `EventBus` port so "the Gas City native and a file-only fallback satisfy the same
contract"; AC-8 tests port-swappability. **Evidence.** C23 *is* the Gas City event-bus primitive
(adopted, AI-CONTEXT §3.2). A second "file-only" implementation is plausible (the storage is just JSONL),
but the port adds a layer whose only justification is "swap Gas City out" — the same G11 vendor-risk
mitigation as C21 DELTA-01. For an MIT primitive that is *already* plain JSONL on disk, the fork/replace
cost is low without a formal port; the port may be speculative generality. **Fix (applied).** Added a
one-line justification requirement: the port is warranted only if it stays thin (it likely does here,
since the contract is small — append/read/cursor); flagged "don't let the port re-implement Gas City's
internals" as the same OQ1-class risk C21 carries.

### RC23B-06 — minor — Bundle-id / XC-4: C23 stays correctly out of the namespace, but DELTA-06's `type` field overlaps the CXDB type system
**Claim.** DELTA-06 envelope carries a `type` field (`BeadMutationEvent`, `SchemaChangeEvent`, …).
**Evidence.** This is a *flat string* event type, distinct from CXDB's `{bundle_id,type,version}` triple
— correct, C23 is pre-CXDB. But when C24 bridges a C23 record into C21, that flat `type` must map to a
CXDB `{bundle_id,type,version}` (C22), and the canonical bundle-id is the XC-4 ruling. The spec doesn't
note that the C23 `type` ↔ CXDB type-triple mapping is a C24/C22 seam. **Fix (applied).** Added a note at
DELTA-06/§4 that the flat C23 `type` is mapped to a CXDB type-triple at the C24 bridge (C22 namespace,
XC-4 ruling), so C23's `type` enum and CXDB's bundle are not conflated.

## Verdict
**accept-with-fixes.** This is a strong, ambitious spec that correctly recognizes C23 as the load-bearing
durability/ordering substrate three siblings lean on — and that recognition is right. The serious design
issues: (1) **gap-free seq vs single-writer vs multi-actor-per-run** is an unresolved internal tension;
(2) **fsync-per-event** has no throughput budget; (3) **retention low-water-mark lets one dead consumer
fill disk** (a self-inflicted cascading failure). All three are fixed in place with bounded contracts.
Plus a cross-spec-authority trim (C23 must not unilaterally "resolve" C19/C21's OQs). No DEFERRED
blockers — C23 is correctly outside the XC-4 namespace fight.
