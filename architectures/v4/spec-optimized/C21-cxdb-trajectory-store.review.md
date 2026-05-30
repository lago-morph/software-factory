# Adversarial review — C21 CXDB Trajectory Store (Track B, sweep 1)

Reviewer persona: Subsystem Adversary — Persistence & Memory
Target: spec-optimized/C21-cxdb-trajectory-store.md
Charter: Track B → attack the DESIGN hard (correctness, coupling, failure handling, cost, scale,
security, simplicity). Are the [DELTA]s justified against concrete forces, or unsupported taste?

## Findings

### RC21B-01 — blocker — Bundle-id namespace collision: DELTA-03 picks `softwarefactory.trajectory.v1`, colliding with three other foundational specs (XC-4)
**Claim.** DELTA-03 names + CI-pins the v4 CXDB bundle `softwarefactory.trajectory.v1`. **Evidence.**
The same `{bundle_id,type,version}` namespace is independently named in three sibling foundational
specs with *four different values*: C20-B `v4.beads.v1` (DELTA-07, bead→CXDB binding), C22-A
`softwarefactory.v4`, C22-B `strongdm.factory.v4` (DELTA-01, one registry for both bead+trajectory
types). C22-B's DELTA-04 explicitly claims a **single registry serving both bead-type and
CXDB-payload-type namespaces** — so C22-B intends `strongdm.factory.v4` to be the bundle C21's turns
also register under, directly contradicting C21-B's `softwarefactory.trajectory.v1`. Since C22 *is*
the type registry C21 stores triples into (C21 §3 outbound: "Type-triple resolution from C22"), C21
cannot pick its own bundle-id independently of C22 — the two must agree or every `AppendTurn`
validation (C21 AC-6) fails to resolve. This is review-log XC-4, unresolved, and it is a build
blocker for the whole Persistence subsystem. **Fix (DEFERRED — needs integrator ruling).** C21-B must
NOT unilaterally pin a bundle-id that conflicts with C22. Recommended canonical ruling below. Added a
DELTA-03 caveat in the spec flagging the collision and deferring the literal value to XC-4.

### RC21B-02 — major — DELTA-04 (durable spool to C23) creates a circular ordering dependency the spec half-admits but doesn't resolve
**Claim.** DELTA-04: when C21 is down, ingestion spools to C23 (event bus) as the durable source, and
"a turn is 'real for the loop' once its source event is sequenced on C23." **Evidence.** This makes
C23 the linearization point for trajectory durability — but C21's *primary writer* is C24 (the
raw-API-bodies bridge, AI-CONTEXT §5.4 #2 path), whose input is NOT the event bus. Raw API bodies are
conversation payloads that do **not** exist on C23 (C23 carries action events, not model request/
response bodies — see C23-A §6 G27). So "spool to C23 on C21-down" only works for the C23→C21 feed
path; for the raw-bodies→C21 path (the one v4 actually builds, README/AI-CONTEXT §11), there is no
event-bus record to spool — the body file is the only durable copy, and that durability is C24's
on-disk spool (OQ2 concedes this). DELTA-04 therefore answers G33 for one of the two ingest paths and
*assumes away* the path v4 prioritizes. **Fix (applied).** Scoped DELTA-04 in the spec to the
C23-sourced event class and cross-referenced C24's client-side spool (G26/G27) for the raw-bodies
path, so the G33 answer doesn't over-claim coverage of an input that never touches C23.

### RC21B-03 — major — DELTA-01 `TrajectoryStore` port is likely infeasible-thin; the spec's own OQ1 says so, but DELTA-01 still claims it "retires the G11/G33 single-vendor bet"
**Claim.** DELTA-01 wraps CXDB behind a thin swappable `TrajectoryStore` port, claiming this "retires
the G11/G33 single-vendor bet." OQ1 then admits "a faithful-but-thin port may be infeasible,
degrading DELTA-01 to 'document the lock-in + keep the fork option.'" **Evidence.** CXDB's value *is*
its idiosyncratic BLAKE3-CAS + turn-DAG + O(1)-branch semantics (AI-CONTEXT §5.3/§5.5). A port thin
enough to be a genuine abstraction would have to re-expose exactly those semantics, so any second
implementation must reimplement CXDB's hardest parts — the port abstracts almost nothing. Claiming the
single-vendor bet is "retired" by a port whose feasibility is an open question is overstated; the real
mitigation is the Apache-2.0 fork option (which exists regardless of the port). **Fix (applied).**
Softened DELTA-01's claim from "retires the bet" to "bounds the blast radius / preserves the fork
option; port thickness is OQ1," so the delta is justified by the force it actually addresses
(swap-cost containment) rather than an over-claim.

### RC21B-04 — major — `AppendTurn` idempotency key (DELTA-02) folds `attribution` into the TurnRef, which breaks dedup and can double-count
**Claim.** DELTA-02: `TurnRef` is "a deterministic function of `(parent_ref, blob_hash, type_triple,
attribution)`." **Evidence.** Including `attribution` (`created_by`) in the idempotency key means two
*byte-identical* turns differing only in actor produce different TurnRefs — fine. But it also means the
same logical turn re-delivered by a *retry from a different actor context* (e.g. C24 bridge restarts
under a different process/actor id, or a replay-on-recovery drains under the recovery actor rather than
the original) yields a NEW TurnRef → a duplicate turn. The DELTA-04 replay-on-recovery path
(AppendTurn under recovery context) is exactly this case. The idempotency guarantee that "C24 can
retry safely" (the whole point of DELTA-02) is undermined if the retrying actor differs from the
original. **Fix (applied).** Noted in the spec that the idempotency key must be invariant under the
*retrying* actor — `attribution` should be recorded on the turn but the dedup identity should key on
`(parent_ref, blob_hash, type_triple)` (the content+position), with attribution as recorded metadata,
not part of the dedup key. Flagged the precise key composition as a sweep-2 freeze item.

### RC21B-05 — minor — DELTA-06 mark-and-sweep GC vs immutability/audit (F54) is an unresolved tension, not just an OQ
**Claim.** DELTA-06 adds mark-and-sweep compaction of "unreachable" blobs after a retention window;
turns "retained per policy (default = keep)." **Evidence.** Branch provenance (DELTA-05) and F54
RSI-drift audit (§6) require the full immutable history; but GC of "unreachable" blobs can reclaim a
blob still referenced by an *un-walked* branch or by a future audit query, and "reachable-from-turn"
reachability is expensive over a TB-scale turn-DAG. The interaction of windowed blob-GC with the
keep-turns-forever audit requirement is real (a turn whose payload blob was swept is a dangling
reference). OQ5 raises the policy but not this referential-integrity hazard. **Fix (applied).** Added
an invariant to the spec: GC may never sweep a blob reachable from any retained turn (including all
branch heads), making "retained turns ⇒ retained blobs" a hard rule so the audit trail can't develop
dangling payload refs.

### RC21B-06 — minor — Performance contract restated as an acceptance "gate" while §8 also calls it "measured evidence" — pick one
**Claim.** §3 invariant says perf is "an acceptance target, not an assumption"; AC #8 calls it "a
*measured* gate, recorded as evidence." **Evidence.** A "gate" blocks the build if missed; "evidence
recorded against the asserted claim" does not. For an *adopted* third-party store the factory can't fix,
a hard gate is the wrong instrument (you can't fail-build CXDB for being slow; you'd fork or accept).
**Fix (applied).** Reworded AC #8 to "measured and recorded as a de-risking datum; a miss is an
integrator finding (fork/accept/tune), not a hard build gate," consistent with the Track-A framing.

## Verdict
**accept-with-fixes** (one DEFERRED blocker). The DELTA set is mostly well-motivated by real forces
(G33 durability, G11 vendor risk, G17 typing). The serious issues: the **bundle-id collision (XC-4)**
is a genuine cross-spec blocker and must go to the integrator; DELTA-04's G33 answer over-claims for the
raw-bodies path; and the DELTA-02 idempotency key is mis-composed (attribution in the dedup key breaks
retry-safety). Fixes applied for everything except the namespace value, which is deferred.
