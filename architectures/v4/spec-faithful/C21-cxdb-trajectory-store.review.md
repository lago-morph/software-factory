# Adversarial review — C21 CXDB Trajectory Store (Track A, sweep 1)

Reviewer persona: Subsystem Adversary (Persistence & Memory)
Target: spec-faithful/C21-cxdb-trajectory-store.md

Track A = attack **fidelity & completeness only**, not the design.

## Findings

### RC21A-01 — major — Upstream repo URL is asserted, not cited; risks fact-vs-fill mislabel
**Claim.** §1 states CXDB is `github.com/strongdm/cxdb`, Apache 2.0. The source-trace header
cites AI-CONTEXT §15.2 line 635 for "repo". But the inventory (C21 row) and the gap analysis
(G11) explicitly flag that *every* CXDB attribute — including the repo URL — is an **unverified
upstream assumption** (G11: "the repo URL … is asserted, not verified"). The spec presents the
URL and "Apache 2.0 … mature for purpose" as fact in §1/§2 without the G11 "unverified" caveat
attached at the point of assertion.
**Evidence.** ambiguities-and-gaps G11; inventory line 123 "No exemplar for the v4-specific type
bundle". §6 does carry the G11 thread, but §1/§2 read as settled fact.
**Fix (applied).** Added an "unverified upstream" caveat marker to the §1 repo/license assertion
pointing at OQ-3/§6, so the fact-vs-assumption boundary is explicit where the claim is made.

### RC21A-02 — major — BLAKE3 + msgpack serialization is stated as fact but is a faithful fill
**Claim.** §1, INV-1, and the ingest flow assert payloads are "msgpack-serialized" then BLAKE3-keyed.
AI-CONTEXT §5.3 names BLAKE3 Blob CAS and the `{bundle_id,type,version}` model, but the precise
"msgpack of the payload bytes, then BLAKE3 of the msgpack" pipeline is the spec's own elaboration.
It is presented as upstream fact, not flagged.
**Evidence.** AI-CONTEXT §5.3 ("Blob CAS … BLAKE3"); the msgpack-is-the-hashed-representation
chaining is not stated verbatim in v4.
**Fix (applied).** Annotated INV-1 with a `[FAITHFUL-FILL]` note that the *serialization-then-hash
ordering* is the minimal faithful reading, while BLAKE3 CAS itself is v4-stated.

### RC21A-03 — major — Performance contract numbers ("p50 < 1ms", "sub-ms TB-scale") cited as AC, traceable but under-qualified
**Claim.** AC-6 and §7 lift "p50 append < 1ms for 10KB payloads" and "sub-ms retrieval over
TB-scale" from AI-CONTEXT §5.5 and make them acceptance criteria. These are *upstream marketing
claims* in v4, not measured facts; G11 explicitly lists "p50<1ms, sub-ms TB-scale retrieval" as
unverified. Making them pass/fail ACs without the "measure-the-upstream-claim" framing risks a
builder treating the number as a guaranteed property.
**Evidence.** G11; the spec's own OQ-3 concedes "every branching/perf claim is provisional".
**Fix (applied).** AC-6 reworded to "**measure and record** p50/retrieval against the pinned
binary (de-risk the upstream §5.5 claim)" rather than asserting the number as a contract to meet.

### RC21A-04 — minor — G33 AMBIGUITY resolution is sound but quietly imports a Track-B-shaped obligation
**Claim.** §6 [AMBIGUITY: G33] chooses fail-open and places the durability obligation on C24,
asserting C21 "MUST be idempotent on replayed writes (BLAKE3 content-addressing makes re-posting
… a no-op — INV-1)". Idempotent-replay-as-a-store-contract is a reasonable faithful inference, but
"a buffering bridge needs it" is a forward design assumption about C24 that v4 never states.
**Evidence.** G26 places back-pressure at the bridge; v4 says nothing about store-side idempotency
guarantees being a *requirement* (it is a consequence of CAS, not a stated obligation).
**Fix (not applied — kept).** The reading is the smallest consistent one and already flagged as an
AMBIGUITY + OQ-2. Left as-is; noted here for the integrator. No change needed.

### RC21A-05 — minor — Bundle-id namespace not surfaced (cross-spec, see ruling below)
**Claim.** §3 I7 / §4 give the registry example as `mycompany.agents.v1` and defer the v4 bundle to
C22, but never names what C21 expects the v4 trajectory bundle to be. C21-B (optimized) names it
`softwarefactory.trajectory.v1`; C22-A names `softwarefactory.v4`; C22-B `strongdm.factory.v4`;
C20-B `v4.beads.v1`. The faithful C21 is silent, which is *defensible* (C22 owns the bundle) but
leaves a reader unable to detect the XC-4 collision from C21-A alone.
**Evidence.** review-log XC-4; C20/C21-B/C22 specs.
**Fix (applied).** Added a one-line pointer in §3 (I7 row note) to XC-4 / the canonical-namespace
ruling, so C21-A explicitly defers naming to the integrator rather than silently omitting it.

### RC21A-06 — minor — Second-pass: §5 step-4 and §7 still called perf numbers a "contract" after RC21A-03 only fixed AC-6 (Subsystem Adversary pass)
**Claim.** RC21A-03 reworded AC-6 to "measure, don't assume" but left §5 "Ingest a turn" step 4 and
§7 Scale still asserting "**Performance contract: p50 < 1ms**" as a hard guarantee — an internal
inconsistency (the spec calls the same number both "unverified upstream claim" at AC-6 and "contract"
at §5/§7). **Evidence.** Lines 170, 244 vs AC-6/G11. **Fix (applied).** Reworded §5 step-4 and §7
Scale to "Performance *claim* (upstream, unverified — measured at AC-6)", matching AC-6's framing.

## Verdict
**accept-with-fixes.** Faithful, well-traced, and the C21/C22 G17 split + G33 fail-open reading are
the correct minimal readings. The only real fidelity defects are *under-qualified upstream claims*
(BLAKE3/msgpack pipeline, perf numbers, repo/license) presented as settled fact where G11 marks
them unverified — all fixed in place by adding the missing "unverified / measure-this" framing.
Nothing architectural deferred.
