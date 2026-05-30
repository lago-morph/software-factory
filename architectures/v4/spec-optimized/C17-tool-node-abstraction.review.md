# Adversarial review — C17 Tool-node Abstraction (Track B, sweep 1)

Reviewer persona: Subsystem Adversary (C08/C17)
Target: spec-optimized/C17-tool-node-abstraction.md

Track B attacks the **design**: correctness, hidden coupling, failure handling, cost, simplicity,
scalability, security — and whether each [DELTA] earns its keep against a concrete force, or is gold-plating.
The optimized C17 carries six deltas (DELTA-01..06), the heaviest being DELTA-04 (a result cache). Special
focus per the brief: does C17 layer cleanly on C02-B's wire ABI with no duplication/contradiction of the
tool-node seam (G29)?

## Findings

### RC17B-01 — major — DELTA-04 (the result/memoization cache) is the most expensive delta and rests entirely on a correctness property C17 cannot itself enforce ("determinism honesty"); a single mislabeled `pure` node silently returns stale/wrong results across the whole factory, and the only detection (C49 replay-divergence) runs *after* the bad cache hit has already been served. The cache is a correctness liability disproportionate to its sweep-1 justification.
- **Claim.** §3c/§4/§6 make `invoke` serve cached `NodeResult`s for `pure`/`capability-scoped-deterministic`
  nodes keyed on `(node_id, version, input_hash, granted_caps_hash, abi_version)`. Correctness rests on the
  "determinism-honesty invariant" (§3b) — but C17 explicitly *threads, does not enforce* determinism, and
  §6 + OQ3 concede verification is "passive-on-replay" via C49. So the failure sequence is: node mislabeled
  `pure` → first run caches a result that depended on a hidden clock/file/RNG → every subsequent caller gets
  the *stale* result with no subprocess → C49 *might* later detect divergence *if* that trajectory is
  replayed. Until then the cache poisons every consumer. For a "deterministic-first" substrate whose whole
  value is reproducibility, a silent-wrong-answer cache is a severe failure mode to take on at sweep 1.
- **Reasoning / cheaper-safer alternative.** (a) **Defer the cache** — it is a *performance* optimization,
  not part of the C17 contract; nothing downstream *requires* memoization to function (it's "cheap" already
  because no token cost). Ship C17 as registry + typed descriptor + invocation facade (DELTA-01/02/03/05/06),
  and make the cache a *later, opt-in* component once determinism *verification* exists. (b) If kept, gate
  caching on **active verification, not honesty**: a node may only be cached after an *enrollment* check
  (run twice at load on a probe input, compare) — turning OQ3's "active vs passive" from an open question
  into a precondition. (c) Consider relocating the cache to **C49** (OQ2 already asks this) — replay already
  content-addresses node results, so a separate C17 cache may be duplicate machinery with a second
  correctness surface.
- **Suggested fix (DEFERRED — architectural).** Recommend **demoting DELTA-04 to opt-in + verification-
  gated, or folding it into C49**. This changes C17's scope and touches C49, so it is deferred, not applied.
  Recorded as the top deferred item. (A confident in-place hardening *is* applied — see RC17B-02 — so that
  *if* the cache ships, it fails safe.)

### RC17B-02 — major — Even taking the cache as given, the cache-key omits the node's *capability-scoped inputs themselves* for `capability-scoped-deterministic` nodes: the key uses `granted_caps_hash` (which capabilities were granted) but a cap-scoped node's output depends on the *content* the capability reads (a partition file), not on the grant. Two runs with the same grant but different file contents collide on the key and return a wrong cached result.
- **Claim.** §3c keys cap-scoped nodes on `(node_id, version, input_hash, granted_caps_hash, abi_version)`.
  But §3a defines `capability-scoped-deterministic` as "output is a function of `(inputs, granted
  capabilities' *content*)` — e.g. reads a partition-scoped file." The key hashes the *grant* (`granted_caps_hash`),
  not the *content read under the grant*. If a node reads `partition/foo.json`, gets grant G, and the file
  later changes, the grant hash is unchanged → cache hit → stale result. §3a even says "cacheable keyed on
  capability *content*-hash" — so §3a and §3c contradict each other on the key.
- **Reasoning.** This is an internal inconsistency that, combined with RC17B-01, makes the cache wrong for
  the exact node class it claims to support. The key for cap-scoped nodes must include a **content-hash of
  what was actually read** (captured during the invocation), not the grant — which means the cache entry can
  only be *written* after the read-set is known, and *served* only by re-reading or by trusting a recorded
  read-set. This is materially harder than §3c implies.
- **Suggested fix (APPLIED — corrects the contradiction).** Align §3c's key with §3a: for
  `capability-scoped-deterministic`, the key includes a `read_set_content_hash` (the content-address of the
  bytes the node actually read under its grant), not merely `granted_caps_hash`; and a cap-scoped result is
  cacheable only when the read-set is captured. Note the cost: this requires read-set capture, reinforcing
  RC17B-01's "defer or fold into C49." Applied as a key correction + caveat; the capture *mechanism* is
  sweep-2/DEFERRED.

### RC17B-03 — major — C17-B and C02-B both claim to register tool-node manifests into the registry and both claim to own the invocation, producing a duplicated/contradictory seam: C02-B §5 step B says "C01 builds a `ToolNodeRequest` … spawns … validates the response," while C17-B §3c says C17's `invoke` "builds a `ToolNodeRequest`, spawns via C01, reads the `ToolNodeResponse`." Who actually drives the subprocess is specified twice, differently.
- **Claim.** The brief asks specifically whether C17 layers cleanly on C02. It mostly does (C17-B §1/§3
  repeatedly cedes the wire format + grant to C02 — good), **but the invocation driver is double-owned**:
  - C02-B §5.B: "C01 builds a `ToolNodeRequest` (inputs schema-validated, context populated …), spawns the
    entrypoint, writes the envelope to stdin." → C01 drives, C02 specifies.
  - C17-B §3c/§5.B: "`invoke` … (4) delegates to C02's wire ABI — *building* a `ToolNodeRequest`, *spawning*
    via C01, *reading* the `ToolNodeResponse`, interpreting the exit-code taxonomy."
  Both can't *build* the request and *interpret* the exit code as the primary owner. Either C17.invoke is
  the caller-facing facade that asks C01/C02 to do the spawn+parse (C17 adds typing/cache *around* it), or
  C02/C01 own build+spawn+parse and C17 is a thin pre/post wrapper. The specs assert overlapping ownership
  of the same steps (request-build, response-parse, exit-code mapping).
- **Reasoning.** This is exactly the "duplication/contradiction of the tool-node seam" the brief flags as
  the G29 risk. C02-B already says "Tool-node manifests registered into C17's catalog" (§5.A) and "exit-code
  → caller action mapping is *inherited from C02 §3b*" is what C17-B §3c *also* says — so the *intent* is
  layered, but the prose has C17 re-performing C02/C01's build+spawn+parse rather than calling into it.
- **Suggested fix (APPLIED).** Rewrite C17-B §3c step (4) and §5.B step 4 to make C17 *delegate* rather than
  *re-perform*: C17.invoke validates typed inputs, computes/consults the cache, then **hands the validated
  request to C02/C01's spawn+wire path and receives the `ToolNodeResponse`** (it does not itself spawn or
  parse the wire bytes); it then validates outputs against `output_schema` and surfaces C02's already-mapped
  status as a typed `NodeResult`. This removes the double-ownership while keeping C17's typing/cache value.
  Applied to C17-B only (I may not edit C02).

### RC17B-04 — minor — DELTA-05 (built-in vs pack-node parity through one registry) is sound, but the "native tool beads register through the same path" claim is unverified against Gas City (G11), and OQ1 admits C17 may reduce to "adopt-and-extend" if Gas City already has a registry. The spec should not present `register(NodeInterface, native)` as a thing C17 *defines* for native beads when C01/Gas City may already own that surface.
- **Claim.** §3b/§5.A have C01 calling `register(NodeInterface, native)` into C17's registry. But if Gas
  City's native tool-bead mechanism already maintains its own catalog (plausible — OQ1 flags exactly this),
  C17 doesn't get to define the native registration API; it must *wrap* or *project* Gas City's. The parity
  invariant (good) is achievable either way, but the spec over-commits to C17 owning native registration.
- **Suggested fix (APPLIED — hedge).** Add a clause to §3b/DELTA-05 that native-bead registration is
  *adopt-and-project* if Gas City exposes its own catalog (per OQ1/G11): C17 guarantees parity at the
  `resolve`/`invoke` surface regardless of whether it *owns* or *wraps* the native registry. Keeps the
  parity guarantee, drops the unverifiable ownership claim.

### RC17B-05 — minor — DELTA-06 (`falsifying_scenario_ref` required for guard nodes) is good F52 discipline, but "guard node" is never defined in C17, so the *required-vs-optional* boundary of the field is undecidable: every deterministic node is arguably a "guard" (it gates DAG advancement on its exit code). Without a definition, C16 can't mechanically tell which nodes must carry the ref.
- **Claim.** §3a/§6/DELTA-06 require `falsifying_scenario_ref` "for any node used as a guard" / "required for
  any node used as a guard." But C17 never says what makes a node a guard vs. a plain transform. If the
  predicate is "used as a guard," that's a *graph-position* property (C12 formula) not a *node* property
  (C17 registry) — so the registry field can't be required by the registry alone; C16 must read the formula
  to know which placements are guards. The delta puts the obligation on the registry but the discriminator
  in the graph.
- **Suggested fix (APPLIED).** Clarify: `falsifying_scenario_ref` is *required when a formula (C12) places a
  node in a guard position* (the discriminator is C12's, enforced by C16 reading C12+C17 together); the C17
  registry field is *always present but may be null for non-guard placements*. This makes the obligation
  mechanically checkable and correctly locates the discriminator. (Cross-ref C16/C12 for the guard-position
  definition — DEFERRED for that definition.)

### RC17B-06 — minor — OQ4 (long-running / service-shaped nodes: C24 bridge, C44 twin) is correctly raised but is a real scope hole, not just an open question: C17's entire `invoke` facade is single-shot, yet two of its named consumers (C24 "watches a directory", C44 a stateful twin) are long-lived. If those use a `[[service]]` contract, C17's "single interface over all deterministic steps" claim has an unstated exception.
- **Suggested fix (NOT APPLIED — architectural, cross-component).** Note in the verdict; the tool-node↔service
  boundary straddles C02↔C17↔C44 and must be drawn by the integrator. Flagged, deferred.

## Verdict

**accept-with-fixes.** The optimized C17 is a genuine improvement over "Gas City native — tool beads, stop":
the typed `NodeInterface` (DELTA-02), the registry with parity + fail-closed collision handling
(DELTA-01/05), the three-valued determinism taxonomy (DELTA-03), and the registry-backed F52 discipline
(DELTA-06) are all force-justified and make C17 a real, buildable, parallelizable surface. The design's
serious weakness is **the result cache (DELTA-04)**: it takes on a silent-wrong-answer correctness liability
(RC17B-01) on a determinism property C17 can't enforce, and its key is internally inconsistent for the
cap-scoped node class it claims to serve (RC17B-02). Recommend demoting it to opt-in/verification-gated or
folding it into C49 (DEFERRED); the key contradiction is fixed in place so it at least fails safe. The
**C17/C02 seam** is *mostly* clean — C17 correctly cedes the wire format, grant, and exit-code taxonomy to
C02 — but the **invocation driver is double-owned** (RC17B-03): both specs have someone building the request
and parsing the response. Fixed in place on the C17 side by making C17 *delegate* to C02/C01's spawn path
rather than re-perform it.

**Integrator call (C17/C02 seam consistency):** After the RC17B-03 fix the seam is consistent and non-
duplicative — **C02 owns the wire bytes / packaging / exit-code taxonomy / capability grant; C17 owns the
typed descriptor + registry + invocation *facade* (delegating the actual spawn+parse to C02/C01) + the
optional cache.** No contradiction of the tool-node seam remains *except* the invocation-driver overlap
(now resolved C17-side; C02-B §5.B should be aligned to match by its own author) and the unresolved
tool-node↔`[[service]]` boundary (RC17B-06, straddles C02/C17/C44) — both flagged for the integrator. The
cache ownership (C17 vs C49) is the other deferred cross-component ruling.
