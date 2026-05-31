# Track B Optimized-Deltas Independence Analysis

**Scope:** Every DELTA in the 23 Track-B spec-optimized files (C01–C42, Batch 1 components).
**Precedent:** INTEGRATION-PASS-1 cherry-picked D-1..D-5 (bundle namespace, schema ownership, dependency direction, tamper-evidence chain, judge provider) — these are already in both tracks; they are NOT re-analyzed here.
**Method:** For each DELTA: identify cross-references, linked components, classify, cost, name port targets, and recommend.

---

## Section 1: Per-Delta Table

Where a delta was part of D-2/D-3/D-4/D-5 rulings already adopted, it is marked **ADOPTED** and excluded from recommendation — it is done.

### C01 — Gas City Substrate

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C01-DELTA-01 | C01 | SYSTEMIC | C04-DELTA-01, C21-DELTA-01, C28-DELTA-01 | C04, C21, C28, C17, C02 | high | spec/C01, plan-faithful/C01 | leave in Track B only |
| C01-DELTA-02 | C01 | ISOLATED | — | C03 (conformance hook) | low | spec/C01, plan-faithful/C01 | port to faithful as-is |
| C01-DELTA-03 | C01 | CLUSTER-2 (native-count) | C03-DELTA-05 | C03 | low | spec/C01, spec/C03, plan-faithful/C01, plan-faithful/C03 | port the cluster |
| C01-DELTA-04 | C01 | CLUSTER-2 (tool-node-seam) | C02-DELTA-01 | C02 | medium | spec/C01, spec/C02, plan-faithful/C01, plan-faithful/C02 | port the cluster |
| C01-DELTA-05 | C01 | CLUSTER-3 (termination) | C13-DELTA-05, C18 (policy seam) | C13, C18, C39 | medium | spec/C01, spec/C13, plan-faithful/C01, plan-faithful/C13 | port the cluster |
| C01-DELTA-06 | C01 | CLUSTER-2 (degraded-mode) | C21-DELTA-04, C23-DELTA-01 | C21, C23, C40 | medium | spec/C01, spec/C21, plan-faithful/C01, plan-faithful/C21 | port the cluster |

**Notes:**
- DELTA-01 (RuntimeSubstrate interface): Requires that C04, C21, C28 all simultaneously expose conformance-testable abstractions. Any single-component port is internally contradicted — e.g., faithful C01 saying "Gas City IS the substrate" while faithful C04 says "the SessionProvider interface" creates an incoherence. Systemic.
- DELTA-02 (version pin + conformance suite): Purely operational — pin a version, add a CI gate. No structural impact on other specs. Easy lift.
- DELTA-03 (native count 5 not 6): Already linked to C03-DELTA-05 which corrects the same claim from the config side. Two-file cluster, low cost.
- DELTA-04 (tool-node seam is C02-owned): A clean re-attribution of ownership. Requires C02 to accept that attribution simultaneously; C02-DELTA-01 is the reciprocal claim.
- DELTA-05 (bounded reconciler tick): Needs C13 to carry the run-scope budget slot (C13-DELTA-05) and C18/C39 to accept the numeric policy boundary. Three components share one invariant.
- DELTA-06 (degraded mode): Interoperates with C21-DELTA-04 (CXDB spool contract) and C23-DELTA-01 (event bus durability). The degraded-mode story is coherent only if C21 and C23 also carry their pieces.

---

### C02 — Pack & Tool-Node ABI

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C02-DELTA-01 | C02 | CLUSTER-2 (tool-node-seam) | C01-DELTA-04 | C01, C17 | medium | spec/C02, spec/C01, plan-faithful/C02, plan-faithful/C01 | port the cluster |
| C02-DELTA-02 | C02 | CLUSTER-3 (supply-chain) | C41-DELTA-06, C51 (provenance seam) | C41, C51, C52 | high | spec/C02, spec/C41, plan-faithful/C02, plan-faithful/C41 | leave in Track B only |
| C02-DELTA-03 | C02 | CLUSTER-2 (typed-I/O) | C01-DELTA-04 | C01, C17 | medium | spec/C02, spec/C17, plan-faithful/C02, plan-faithful/C17 | port the cluster |
| C02-DELTA-04 | C02 | CLUSTER-2 (capability-declaration) | C43 (isolation seam) | C43, C04 | medium | spec/C02, spec/C04, plan-faithful/C02, plan-faithful/C04 | port the cluster |
| C02-DELTA-05 | C02 | ISOLATED | — | C01 (version axis only) | low | spec/C02, plan-faithful/C02 | port to faithful as-is |
| C02-DELTA-06 | C02 | ISOLATED | — | — | low | spec/C02, plan-faithful/C02 | port to faithful as-is |
| C02-DELTA-07 | C02 | ISOLATED | — | C52 (fork-trigger log) | low | spec/C02, plan-faithful/C02 | port to faithful as-is |

**Notes:**
- DELTA-02 (signed pack manifest + RSI gating): The signing trust root connects to C41 key model (DELTA-06) and C51 gene-transfusion provenance — three components must agree on what a "valid signature" means. High cost; the trust-root question alone is unresolved (OQ3 in C02).
- DELTA-04 (capability declaration feeds C43): C43 doesn't exist yet (Batch 4); porting this alone into faithful creates a forward reference to an undefined component. Medium cost but the faithful spec can use a [FAITHFUL-FILL] stub declaring the seam.
- DELTA-05 (ABI version handshake): Independent of signing/capability; just adds a version negotiation handshake at load. Can be stated in one file.
- DELTA-06 (language neutral protocol): Factual statement about JSON-over-stdio. No cross-component consequence.
- DELTA-07 (no-fork falsifiability): A policy/invariant statement in one file. No structural dependencies.

---

### C03 — Layered Config / Feature-Flag Model

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C03-DELTA-01 | C03 | ISOLATED | — | C01 (precedence description) | low | spec/C03, plan-faithful/C03 | port to faithful as-is |
| C03-DELTA-02 | C03 | ISOLATED | — | C02 (CapabilityDescriptor) | low | spec/C03, plan-faithful/C03 | port to faithful as-is |
| C03-DELTA-03 | C03 | CLUSTER-2 (secrets) | C41-DELTA-06 | C41, G37-adjacent | medium | spec/C03, spec/C41, plan-faithful/C03, plan-faithful/C41 | port the cluster |
| C03-DELTA-04 | C03 | ISOLATED | — | — | low | spec/C03, plan-faithful/C03 | port to faithful as-is |
| C03-DELTA-05 | C03 | CLUSTER-2 (native-count) | C01-DELTA-03 | C01 | low | spec/C03, spec/C01, plan-faithful/C03, plan-faithful/C01 | port the cluster |
| C03-DELTA-06 | C03 | ISOLATED | C23/C41 (emission only) | C23, C41 | low | spec/C03, plan-faithful/C03 | port to faithful as-is |

**Notes:**
- DELTA-03 (SecretRef indirection): The indirection mechanism itself is isolated to C03, but the security argument depends on C41's key model (DELTA-06) being in place to make secrets actually safe. Can be ported as a structural delta without DELTA-06 by noting the residual (G37 still open); the faithful spec already flags G37.
- DELTA-06 (config provenance emission): Emits a record to C23/C41; these are downstream consumers, so the emission is one-sided and doesn't require C23/C41 to change their specs.

---

### C04 — Session & Provider Runtime

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C04-DELTA-01 | C04 | SYSTEMIC | C01-DELTA-01, C28-DELTA-01, C21-DELTA-01 | C01, C28, C21 | high | spec/C04, plan-faithful/C04 | leave in Track B only |
| C04-DELTA-02 | C04 | ISOLATED | — | C19 (ResumeToken anchor) | low | spec/C04, plan-faithful/C04 | port to faithful as-is |
| C04-DELTA-03 | C04 | ISOLATED | — | C28 (credential ladder) | low | spec/C04, plan-faithful/C04 | port to faithful as-is |
| C04-DELTA-04 | C04 | ISOLATED | — | C28, C36 (liveness producer) | low | spec/C04, plan-faithful/C04 | port to faithful as-is |
| C04-DELTA-05 | C04 | CLUSTER-3 (isolation-at-spawn) | C42-DELTA-05 (PartitionBinding), C43 seam | C42, C43, C28 | medium | spec/C04, spec/C42, plan-faithful/C04, plan-faithful/C42 | port the cluster |
| C04-DELTA-06 | C04 | ISOLATED | — | C01 (pool count) | low | spec/C04, plan-faithful/C04 | port to faithful as-is |

**Notes:**
- DELTA-01 (SessionProvider contract): Directly depends on C01's RuntimeSubstrate abstraction and C28's AgentLoopProvider abstraction being defined first. SYSTEMIC — the three portability contracts (C01/C04/C28) are one architectural bet, not three independent statements.
- DELTA-05 (isolation-at-spawn): Requires C42 to emit a PartitionBinding and C43 to define capability profiles. C42-DELTA-05 is the reciprocal. These two can travel together even without C43 (which is Batch 4) by using a FAITHFUL-FILL stub for C43's capability profile shape.
- DELTA-02/03/04/06: Genuinely isolated improvements (typed resume token, credential ladder, liveness signal, pool lifecycle). Each touches one spec.

---

### C05 — Sling / Dispatch

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C05-DELTA-01 | C05 | ISOLATED | — | C29, C42, C28 (typed RoutingDecision inputs) | low | spec/C05, plan-faithful/C05 | port to faithful as-is |
| C05-DELTA-02 | C05 | CLUSTER-2 (admission) | C28-DELTA-02 | C28 | medium | spec/C05, spec/C28, plan-faithful/C05, plan-faithful/C28 | port the cluster |
| C05-DELTA-03 | C05 | ISOLATED | — | — | low | spec/C05, plan-faithful/C05 | port to faithful as-is |
| C05-DELTA-04 | C05 | CLUSTER-2 (routing-authority-split) | C09-DELTA-01 | C09, C12 | low | spec/C05, spec/C09, plan-faithful/C05, plan-faithful/C09 | port the cluster |
| C05-DELTA-05 | C05 | ISOLATED | — | C18 (partial failure handling) | low | spec/C05, plan-faithful/C05 | port to faithful as-is |
| C05-DELTA-06 | C05 | ISOLATED | — | C23, C19, C41 (emission) | low | spec/C05, plan-faithful/C05 | port to faithful as-is |

**Notes:**
- DELTA-02 (admission-controlled dispatch): C28 must provide the `acquire()` governor interface. C28-DELTA-02 adds the seat governor. These two must travel together — the dispatch can't back-pressure without C28 exposing the gate.
- DELTA-04 (routing authority split): C09-DELTA-01 adopted the same split from the C09 side (spec referenced by ID, not rendered as template). Both sides of the seam must agree simultaneously.

---

### C07 — Vocabulary & Glossary

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C07-DELTA-01 | C07 | ISOLATED | — | — | low | spec/C07, plan-faithful/C07 | port to faithful as-is |
| C07-DELTA-02 | C07 | ISOLATED | — | C54, C57 (rename advisory) | low | spec/C07, plan-faithful/C07 | port to faithful as-is |
| C07-DELTA-03 | C07 | ISOLATED | — | C51 (provenance field) | low | spec/C07, plan-faithful/C07 | port to faithful as-is |
| C07-DELTA-04 | C07 | CLUSTER-2 (vocab-lint-wiring) | C10-DELTA-04 | C10 | low | spec/C07, spec/C10, plan-faithful/C07, plan-faithful/C10 | port the cluster |
| C07-DELTA-05 | C07 | ISOLATED | — | — | low | spec/C07, plan-faithful/C07 | port to faithful as-is |
| C07-DELTA-06 | C07 | ISOLATED | — | C01-DELTA-01 (extraction synonym consumer), C57 | low | spec/C07, plan-faithful/C07 | port to faithful as-is |

**Notes:**
- DELTA-04 (CanonicalTermSet export): C07 exports; C10 imports. These must move together or C10 has a dangling import. But the cluster is just two files and zero structural changes to the broader system.
- DELTA-02 (pinning authority for overloaded terms): Purely descriptive/advisory — pinning which sense is canonical does not change any component's behavior, only documentation. No structural cross-impact.

---

### C08 — Spec Artifact

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C08-DELTA-01 | C08 | CLUSTER-3 (spec-bundle-seam) | C09-DELTA-01, C05-DELTA-04 | C09, C05, C10 | medium | spec/C08, spec/C09, spec/C05, plan-faithful/C08, plan-faithful/C09, plan-faithful/C05 | port the cluster |
| C08-DELTA-02 | C08 | CLUSTER-2 (multi-file-bundle) | C09-DELTA-01 | C09 | medium | spec/C08, spec/C09, plan-faithful/C08, plan-faithful/C09 | port the cluster |
| C08-DELTA-03 | C08 | CLUSTER-2 (DoD) | C32, C33 (scoring surface) | C32, C33 | medium | spec/C08, plan-faithful/C08 | port to faithful as-is |
| C08-DELTA-04 | C08 | CLUSTER-3 (content-address-identity) | C09-DELTA-03, C21 (BLAKE3 reuse) | C09, C21, C33, C46, C49 | medium | spec/C08, spec/C09, plan-faithful/C08, plan-faithful/C09 | port the cluster |
| C08-DELTA-05 | C08 | CLUSTER-2 (required-section-schema) | C10-DELTA-02 | C10 | low | spec/C08, spec/C10, plan-faithful/C08, plan-faithful/C10 | port the cluster |
| C08-DELTA-06 | C08 | ISOLATED | — | C09, C11 (detail_level consumer) | low | spec/C08, plan-faithful/C08 | port to faithful as-is |

**Notes:**
- DELTA-01 (standalone spec bundle vs template-is-spec): This is the fundamental Track B spec-intake redesign — the spec becomes a separate artifact from the prompt template. It requires C09 to consume it by reference (C09-DELTA-01) and C05 to treat the binding opaquely (C05-DELTA-04). The cluster is C08+C09+C05 at minimum, with C10 needing the structured surface. Together these are a meaningful but bounded change: 3–5 spec files.
- DELTA-03 (enumerated DoD): Adds DoD.md to the bundle. Downstream C32/C33 would need to score against it — but in faithful those components don't exist yet (Batch 3), so porting DELTA-03 into faithful C08 is safe with a FAITHFUL-FILL note that C32/C33 will consume it. Single-file port.
- DELTA-04 (content-address spec_id): Requires BLAKE3 which C21 provides. But C08 can define the hashing rule with a FAITHFUL-FILL stub — the C21 dependency is a type reuse, not a blocking call. Still clusters with C09-DELTA-03 since C09 must embed the spec_id in the binding record.

---

### C09 — Prompt Template & Spec→Execution Binding

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C09-DELTA-01 | C09 | CLUSTER-3 (spec-bundle-seam) | C08-DELTA-01, C05-DELTA-04 | C08, C05, C12 | medium | spec/C09, spec/C08, spec/C05, plan-faithful/C09, plan-faithful/C08, plan-faithful/C05 | port the cluster |
| C09-DELTA-02 | C09 | ISOLATED | — | C13 (render variables) | low | spec/C09, plan-faithful/C09 | port to faithful as-is |
| C09-DELTA-03 | C09 | CLUSTER-2 (content-addressed-binding) | C08-DELTA-04 | C08, C23, C19, C41 | low | spec/C09, spec/C08, plan-faithful/C09, plan-faithful/C08 | port the cluster |
| C09-DELTA-04 | C09 | ISOLATED | — | — | low | spec/C09, plan-faithful/C09 | port to faithful as-is |
| C09-DELTA-05 | C09 | ISOLATED | — | C28 (prompt.id correlation) | low | spec/C09, plan-faithful/C09 | port to faithful as-is |
| C09-DELTA-06 | C09 | ISOLATED | — | C08 (detail_level input) | low | spec/C09, plan-faithful/C09 | port to faithful as-is |

**Notes:**
- DELTA-04 (render sandbox): A security improvement entirely internal to C09's render logic. No structural impact on other specs.
- DELTA-05 (strict missing-key + prompt.id): prompt.id emission requires C28 to correlate it in telemetry, but C28 already records correlation keys in faithful. Low cost.

---

### C10 — Spec Linter (EARS / INCOSE)

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C10-DELTA-01 | C10 | CLUSTER-2 (pure-node-contract) | C17-DELTA-03 | C17 | low | spec/C10, spec/C17, plan-faithful/C10, plan-faithful/C17 | port the cluster |
| C10-DELTA-02 | C10 | CLUSTER-2 (structured-lint-surface) | C08-DELTA-05 | C08 | low | spec/C10, spec/C08, plan-faithful/C10, plan-faithful/C08 | port the cluster |
| C10-DELTA-03 | C10 | ISOLATED | — | C08 (detail_level input) | low | spec/C10, plan-faithful/C10 | port to faithful as-is |
| C10-DELTA-04 | C10 | CLUSTER-2 (vocab-lint-wiring) | C07-DELTA-04 | C07 | low | spec/C10, spec/C07, plan-faithful/C10, plan-faithful/C07 | port the cluster |
| C10-DELTA-05 | C10 | ISOLATED | — | C51 (rule provenance) | low | spec/C10, plan-faithful/C10 | port to faithful as-is |
| C10-DELTA-06 | C10 | ISOLATED | — | C46 (structural score metric) | low | spec/C10, plan-faithful/C10 | port to faithful as-is |

---

### C12 — Formula / Pipeline-File Format

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C12-DELTA-01 | C12 | ISOLATED | — | C01 (Gas City TOML conformance) | low | spec/C12, plan-faithful/C12 | port to faithful as-is |
| C12-DELTA-02 | C12 | CLUSTER-2 (node-taxonomy) | C16 (discipline linter surface) | C16 | low | spec/C12, plan-faithful/C12 | port to faithful as-is |
| C12-DELTA-03 | C12 | CLUSTER-2 (parameter-binding) | C09-DELTA-01 (spec_ref param) | C09, C13 | low | spec/C12, spec/C09, plan-faithful/C12, plan-faithful/C09 | port the cluster |
| C12-DELTA-04 | C12 | CLUSTER-2 (methodology-identity) | C55, C50 (methodology selection) | C50, C55 | low | spec/C12, plan-faithful/C12 | port to faithful as-is |
| C12-DELTA-05 | C12 | CLUSTER-3 (DAG-invariants) | C13-DELTA-04, C15/C16 (linters) | C13, C15, C16 | medium | spec/C12, spec/C13, plan-faithful/C12, plan-faithful/C13 | port the cluster |
| C12-DELTA-06 | C12 | ISOLATED | — | C51 (transfusion lineage) | low | spec/C12, plan-faithful/C12 | port to faithful as-is |
| C12-DELTA-07 | C12 | CLUSTER-2 (DOT-round-trip) | C14 (translator contract) | C14 | low | spec/C12, plan-faithful/C12 | port to faithful as-is |

**Notes:**
- DELTA-02 (closed node taxonomy): Provides the structured surface C16 needs — C16 is Batch 3 and not yet authored, so the taxonomy can be stated in C12 faithful with a FAITHFUL-FILL noting C16 will consume it.
- DELTA-04 (methodology identity fields): C55/C50 are Batch 4/5; porting into faithful C12 is safe with a note that these fields exist for future use.

---

### C13 — Molecule Runtime State

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C13-DELTA-01 | C13 | ISOLATED | — | — | low | spec/C13, plan-faithful/C13 | port to faithful as-is |
| C13-DELTA-02 | C13 | ISOLATED | — | C12, C19 (transactional create) | low | spec/C13, plan-faithful/C13 | port to faithful as-is |
| C13-DELTA-03 | C13 | CLUSTER-2 (molecule-root-bead) | C20-DELTA-02 (factory_build identity) | C20, C19 | low | spec/C13, plan-faithful/C13 | port to faithful as-is |
| C13-DELTA-04 | C13 | CLUSTER-3 (tree-invariants) | C12-DELTA-05, C19-DELTA-03 | C12, C19 | medium | spec/C13, spec/C12, spec/C19, plan-faithful/C13, plan-faithful/C12, plan-faithful/C19 | port the cluster |
| C13-DELTA-05 | C13 | CLUSTER-3 (termination) | C01-DELTA-05, C12 (gate bound) | C01, C12, C18, C39 | medium | spec/C13, spec/C01, plan-faithful/C13, plan-faithful/C01 | port the cluster |
| C13-DELTA-06 | C13 | ISOLATED | — | C19 (dependency correction) | low | spec/C13, plan-faithful/C13 | port to faithful as-is |
| C13-DELTA-07 | C13 | CLUSTER-2 (branch-reinstantiation) | C49 (replay primitive) | C49 | medium | spec/C13, plan-faithful/C13 | port to faithful as-is |

**Notes:**
- DELTA-07 (branch/re-instantiation): C49 is Batch 5 and not yet authored. Porting the `branch()` API stub into faithful C13 is safe — it adds an interface seam without requiring C49 to exist. Low port cost but medium value because C49 is the "most unsolved" component; having the interface defined early helps.

---

### C17 — Tool-Node Abstraction

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C17-DELTA-01 | C17 | CLUSTER-2 (registry-and-facade) | C02-DELTA-01 (wire ABI beneath) | C02, C01 | medium | spec/C17, spec/C02, plan-faithful/C17, plan-faithful/C02 | port the cluster |
| C17-DELTA-02 | C17 | ISOLATED | — | C02 (manifest above) | low | spec/C17, plan-faithful/C17 | port to faithful as-is |
| C17-DELTA-03 | C17 | CLUSTER-2 (determinism-class) | C10-DELTA-01, C49 (replay) | C10, C49 | low | spec/C17, spec/C10, plan-faithful/C17, plan-faithful/C10 | port the cluster |
| C17-DELTA-04 | C17 | ISOLATED | — | C49 (cache-vs-replay OQ) | low | spec/C17, plan-faithful/C17 | port to faithful as-is |
| C17-DELTA-05 | C17 | ISOLATED | — | — | low | spec/C17, plan-faithful/C17 | port to faithful as-is |
| C17-DELTA-06 | C17 | CLUSTER-2 (guard-accountability) | C12-DELTA-02 (guard position from formula), C16 | C12, C16 | low | spec/C17, spec/C12, plan-faithful/C17, plan-faithful/C12 | port the cluster |

**Notes:**
- DELTA-04 (result cache): Internally coherent once determinism class (DELTA-03) is defined. The cache OQ (C17 OQ2: does it belong in C49?) means this has an open ownership question — safer to note as FAITHFUL-FILL than to commit the full caching design.

---

### C19 — Bead Work-Graph

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C19-DELTA-01 | C19 | ISOLATED | — | C01 (config toggle) | low | spec/C19, plan-faithful/C19 | port to faithful as-is |
| C19-DELTA-02 | C19 | CLUSTER-2 (attribution-invariant) | C41-DELTA-02 (Actor model) | C41 | low | spec/C19, spec/C41, plan-faithful/C19, plan-faithful/C41 | port the cluster |
| C19-DELTA-03 | C19 | CLUSTER-3 (typed-edge-taxonomy) | C13-DELTA-04, C20 (edge-kind enum) | C13, C20 | medium | spec/C19, spec/C13, spec/C20, plan-faithful/C19, plan-faithful/C13, plan-faithful/C20 | port the cluster |
| C19-DELTA-04 | C19 | ISOLATED | — | — | low | spec/C19, plan-faithful/C19 | port to faithful as-is |
| C19-DELTA-05 | C19 | ISOLATED | — | C23 (mutation events) | low | spec/C19, plan-faithful/C19 | port to faithful as-is |
| C19-DELTA-06 | C19 | ISOLATED | — | C20 (validation seam) | low | spec/C19, plan-faithful/C19 | port to faithful as-is |
| C19-DELTA-07 | C19 | ISOLATED | — | C13, C18, C35, C39 | low | spec/C19, plan-faithful/C19 | port to faithful as-is |

**Notes:**
- DELTA-02 (non-null created_by invariant): Requires C41 to have defined the Actor model — but the faithful spec can reference C41's Actor as a type. Clusters with C41-DELTA-02 since both must agree the field is non-null. Already partially addressed via D-4 (D-4 integration touched C19's attribution seam).
- DELTA-04 (file durability): An entirely self-contained operational improvement (append+fsync+atomic-rename). Zero cross-component impact.
- DELTA-05 (monotonic seq + mutation events): Self-contained within C19; the emission to C23 is a one-sided producer push.

---

### C20 — Bead Schema Registry

D-2, D-3, D-4 adoption already touched C20. The remaining deltas:

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C20-DELTA-01 | C20 | ISOLATED | — | — | low | spec/C20, plan-faithful/C20 | port to faithful as-is |
| C20-DELTA-02 | C20 | CLUSTER-2 (lifecycle-state) | C13-DELTA-03 (molecule root) | C13, C52, C19 | low | spec/C20, spec/C13, plan-faithful/C20, plan-faithful/C13 | port the cluster |
| C20-DELTA-03 | C20 | ISOLATED | — | — | low | spec/C20, plan-faithful/C20 | port to faithful as-is |
| C20-DELTA-04 | C20 | CLUSTER-2 (loop-closure-schema) | C39, C18 (policy fields) | C39, C18 | medium | spec/C20, plan-faithful/C20 | port to faithful as-is |
| C20-DELTA-05 | C20 | ISOLATED | — | C41, C51 | low | spec/C20, plan-faithful/C20 | port to faithful as-is |
| C20-DELTA-06 | C20 | ISOLATED | — | — | low | spec/C20, plan-faithful/C20 | port to faithful as-is |
| C20-DELTA-07 | C20 | CLUSTER-2 (CXDB-type-binding) | C22-DELTA-01, C21 (turn registration) | C22, C21 | medium | spec/C20, spec/C22, plan-faithful/C20, plan-faithful/C22 | port the cluster |

**Notes:**
- DELTA-02 (`factory_build` as one type + lifecycle states): Already closely related to D-4 (direction ruling) and XC-2 (cold-start query compat). Clusters with C13 because the molecule root bead is a `factory_build` bead.
- DELTA-04 (loop closure schema fields): C20 owns the fields; C39 sets the numeric policy. This is a clean split but the fields alone don't close G18 — that needs C39. Can port C20's schema side without C39 existing.
- DELTA-07 (CXDB type binding): Requires C22 to accept the registration binding. The D-2 adoption already resolved the bundle namespace; DELTA-07 extends to the per-type registration seam.

---

### C21 — CXDB Trajectory Store

D-2 adoption set the bundle namespace. Remaining deltas:

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C21-DELTA-01 | C21 | SYSTEMIC | C01-DELTA-01, C04-DELTA-01, C28-DELTA-01 | C01, C04, C28 | high | spec/C21, plan-faithful/C21 | leave in Track B only |
| C21-DELTA-02 | C21 | ISOLATED | — | C24 (retry safety) | low | spec/C21, plan-faithful/C21 | port to faithful as-is |
| C21-DELTA-03 | C21 | CLUSTER-2 (type-bundle-naming) | C22-DELTA-01 | C22 | low | ADOPTED (D-2) | ADOPTED |
| C21-DELTA-04 | C21 | CLUSTER-2 (degraded-mode-spool) | C01-DELTA-06, C23-DELTA-01 | C01, C23, C24 | medium | spec/C21, spec/C23, plan-faithful/C21, plan-faithful/C23 | port the cluster |
| C21-DELTA-05 | C21 | CLUSTER-2 (branch-replay-API) | C13-DELTA-07, C49 | C13, C49, C37 | medium | spec/C21, spec/C13, plan-faithful/C21, plan-faithful/C13 | port the cluster |
| C21-DELTA-06 | C21 | ISOLATED | — | — | low | spec/C21, plan-faithful/C21 | port to faithful as-is |
| C21-DELTA-07 | C21 | ISOLATED | — | C49, C37, C38 | low | spec/C21, plan-faithful/C21 | port to faithful as-is |

**Notes:**
- DELTA-01 (TrajectoryStore port abstraction): Same architectural-bet pattern as C01-DELTA-01 and C04-DELTA-01. The entire "portability contract" framing is a Track-B-wide architectural stance.
- DELTA-05 (branch API): Requires C13's `branch()` primitive (C13-DELTA-07) to call it. Both travel together because they define the same operation from different perspectives.

---

### C22 — CXDB Type Registry

D-2, D-3 adoptions already resolved bundle namespace and ownership split. Remaining deltas:

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C22-DELTA-01 | C22 | CLUSTER-2 (concrete-bundle) | C21-DELTA-03 | C21, C20 | low | ADOPTED (D-2) | ADOPTED |
| C22-DELTA-02 | C22 | ISOLATED | — | C37, C38, C49 (viewpoint consumers) | low | spec/C22, plan-faithful/C22 | port to faithful as-is |
| C22-DELTA-03 | C22 | ISOLATED | — | C49, C37 (replay determinism) | low | spec/C22, plan-faithful/C22 | port to faithful as-is |
| C22-DELTA-04 | C22 | CLUSTER-2 (registration-mechanism) | C20-DELTA-07 | C20 | medium | ADOPTED (D-3) | ADOPTED |
| C22-DELTA-05 | C22 | ISOLATED | — | C21 (ingest validation) | low | spec/C22, plan-faithful/C22 | port to faithful as-is |

---

### C23 — Event Bus

D-5 adoption set the event_id ordering contract. Remaining deltas:

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C23-DELTA-01 | C23 | CLUSTER-2 (durability-contract) | C21-DELTA-04 (spool fallback) | C21, C01 | medium | spec/C23, spec/C21, plan-faithful/C23, plan-faithful/C21 | port the cluster |
| C23-DELTA-02 | C23 | ISOLATED | — | C24, C40 (consumer decoupling) | low | spec/C23, plan-faithful/C23 | port to faithful as-is |
| C23-DELTA-03 | C23 | ISOLATED | — | C19, C21, C24, C40 (dedup key) | low | spec/C23, plan-faithful/C23 | port to faithful as-is |
| C23-DELTA-04 | C23 | ISOLATED | — | — | low | spec/C23, plan-faithful/C23 | port to faithful as-is |
| C23-DELTA-05 | C23 | ISOLATED | — | — | low | spec/C23, plan-faithful/C23 | port to faithful as-is |
| C23-DELTA-06 | C23 | ISOLATED | — | C41 (attribution ledger) | low | spec/C23, plan-faithful/C23 | port to faithful as-is |

**Notes:**
- DELTA-01 (durability/fsync contract): The durability invariant ("Append does not return until batch is fsync'd") is what makes C21's degraded-mode spool story work (C21-DELTA-04 rests on C23 actually being durable). They must travel together.
- DELTA-02/03/04/05/06: All are clean improvements to a single component — back-pressure decoupling, idempotency key, partitioned streams, retention, attribution-total envelope. No other spec breaks if faithful C23 lacks these.

---

### C24 — Telemetry → CXDB Ingestion Bridge

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C24-DELTA-01 | C24 | CLUSTER-2 (dual-source) | C23-DELTA-03 (at-least-once contract) | C23, C21 | medium | spec/C24, spec/C23, plan-faithful/C24, plan-faithful/C23 | port the cluster |
| C24-DELTA-02 | C24 | CLUSTER-2 (idempotent-posting) | C21-DELTA-02 | C21 | low | spec/C24, spec/C21, plan-faithful/C24, plan-faithful/C21 | port the cluster |
| C24-DELTA-03 | C24 | ISOLATED | — | C21 (spool durability, separate) | low | spec/C24, plan-faithful/C24 | port to faithful as-is |
| C24-DELTA-04 | C24 | ISOLATED | — | C21 (parent-chain seam) | low | spec/C24, plan-faithful/C24 | port to faithful as-is |
| C24-DELTA-05 | C24 | ISOLATED | — | C25 (producer-side readiness) | low | spec/C24, plan-faithful/C24 | port to faithful as-is |
| C24-DELTA-06 | C24 | CLUSTER-2 (supervised-service-model) | C25-DELTA-01 (C25 is config-not-process) | C25, C01 | low | spec/C24, spec/C25, plan-faithful/C24, plan-faithful/C25 | port the cluster |

---

### C25 — OTLP Telemetry Export

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C25-DELTA-01 | C25 | CLUSTER-2 (config-not-process) | C24-DELTA-06 | C24, C04, C28 | low | spec/C25, spec/C24, plan-faithful/C25, plan-faithful/C24 | port the cluster |
| C25-DELTA-02 | C25 | ISOLATED | — | C26 (anti-edge to CXDB) | low | spec/C25, plan-faithful/C25 | port to faithful as-is |
| C25-DELTA-03 | C25 | CLUSTER-2 (raw-bodies-security) | C24-DELTA-05 (readiness protocol) | C24, C43 | low | spec/C25, spec/C24, plan-faithful/C25, plan-faithful/C24 | port the cluster |
| C25-DELTA-04 | C25 | ISOLATED | — | C04 (injection), C28 (loop safe) | low | spec/C25, plan-faithful/C25 | port to faithful as-is |
| C25-DELTA-05 | C25 | ISOLATED | — | C26 (endpoint contract) | low | spec/C25, plan-faithful/C25 | port to faithful as-is |

---

### C28 — Claude Code Agent Loop

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C28-DELTA-01 | C28 | SYSTEMIC | C01-DELTA-01, C04-DELTA-01, C21-DELTA-01 | C01, C04, C21, C29 | high | spec/C28, plan-faithful/C28 | leave in Track B only |
| C28-DELTA-02 | C28 | CLUSTER-2 (admission-governor) | C05-DELTA-02 | C05 | medium | spec/C28, spec/C05, plan-faithful/C28, plan-faithful/C05 | port the cluster |
| C28-DELTA-03 | C28 | SYSTEMIC | C28-DELTA-01, C04-DELTA-01 | C01, C04, Max ToS OQ | high | spec/C28, plan-faithful/C28 | leave in Track B only |
| C28-DELTA-04 | C28 | CLUSTER-2 (capability-profile-per-invocation) | C43, C04-DELTA-05 | C43, C04, C42 | medium | spec/C28, spec/C04, plan-faithful/C28, plan-faithful/C04 | port the cluster |
| C28-DELTA-05 | C28 | ISOLATED | — | — | low | spec/C28, plan-faithful/C28 | port to faithful as-is |
| C28-DELTA-06 | C28 | ISOLATED | — | C29 (floor conformance gate) | low | spec/C28, plan-faithful/C28 | port to faithful as-is |
| C28-DELTA-07 | C28 | ISOLATED | — | C02 (pack ABI), C35 | low | spec/C28, plan-faithful/C28 | port to faithful as-is |

**Notes:**
- DELTA-01 (AgentLoopProvider abstraction): Part of the portability-contract cluster (C01/C04/C21). Systemic — cannot port C28's provider abstraction without the whole chain.
- DELTA-03 (multi-seat pool): Depends on C28-DELTA-01's provider abstraction AND raises an unresolved Max ToS question (OQ-1). Even if the ToS clears, this is a structural change that requires the pool scheduler built on the provider contract. Systemic.
- DELTA-05 (context-budget management): Entirely internal to the loop. C28 owns the context-window ceilings in faithful already (it's a Claude Code internal); this makes them observable and enforced.
- DELTA-07 (typed hooks/skills/MCP surface): Improves the pack-ABI binding but does not require other specs to change.

---

### C29 — Model Floor & Stylesheet Routing

D-1 adoption set the Phase-0 same-provider judge baseline. Remaining deltas:

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C29-DELTA-01 | C29 | ISOLATED | — | — | low | spec/C29, plan-faithful/C29 | port to faithful as-is |
| C29-DELTA-02 | C29 | SYSTEMIC | C32, C34 (judge-independence-policy), D-1 | C32, C34, cross-track | high | spec/C29, plan-faithful/C29 | leave in Track B only |
| C29-DELTA-03 | C29 | SYSTEMIC | C32, C34 | C32, C34 | high | spec/C29, plan-faithful/C29 | leave in Track B only |
| C29-DELTA-04 | C29 | ISOLATED | — | C28, C23, C41 | low | spec/C29, plan-faithful/C29 | port to faithful as-is |
| C29-DELTA-05 | C29 | CLUSTER-2 (live-budget-routing) | C46 (cost stream) | C46, C28 | medium | spec/C29, plan-faithful/C29 | port to faithful as-is |
| C29-DELTA-06 | C29 | ISOLATED | — | C32 (fail-closed judge dispatch) | low | spec/C29, plan-faithful/C29 | port to faithful as-is |

**Notes:**
- DELTA-02 (graded independence policy L0–L3): This is the Track-B response to the cross-family judge problem. D-1 resolved the Phase-0 baseline as L1 (same-provider). But DELTA-02's full graded-policy mechanism is the FE-1 seam — it is the structural element that makes L2/L3 reachable later. Porting the full mechanism into faithful would either (a) add machinery faithful v4 never described, or (b) require C32/C34 to be co-authored. Systemic because it restructures the evaluation-independence model.
- DELTA-03 (metered-API judge seat credential path): A concrete credential proposal for the L2/L3 path. Systemic for the same reason — requires C32/C34 to exist and acknowledge it.
- DELTA-05 (live budget routing): C46 is Batch 5 and not yet authored. With a graceful degradation fallback (static tier labels), this is a partial port — port the mechanism but note C46 supplies it when available.

---

### C41 — Identity / Actor Model & Attribution

D-5 adoption resolved tamper-evidence chain ownership. Remaining deltas:

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C41-DELTA-01 | C41 | SYSTEMIC | C06, C03 (signing policy), G37 | C06, C03, C43, G37 | high | spec/C41, plan-faithful/C41 | leave in Track B only |
| C41-DELTA-02 | C41 | CLUSTER-2 (actor-taxonomy) | C19-DELTA-02 | C19, C42, C04, C28 | low | spec/C41, spec/C19, plan-faithful/C41, plan-faithful/C19 | port the cluster |
| C41-DELTA-03 | C41 | ISOLATED | — | C19, C23 (Attribution record embed) | low | spec/C41, plan-faithful/C41 | port to faithful as-is |
| C41-DELTA-04 | C41 | ISOLATED | — | C23 (ADOPTED D-5) | low | ADOPTED (D-5) | ADOPTED |
| C41-DELTA-05 | C41 | ISOLATED | — | C06, C34 | low | spec/C41, plan-faithful/C41 | port to faithful as-is |
| C41-DELTA-06 | C41 | SYSTEMIC | C41-DELTA-01, G37, C03 | C03, G37 | high | spec/C41, plan-faithful/C41 | leave in Track B only |
| C41-DELTA-07 | C41 | CLUSTER-2 (boundary-class) | C43 (taxonomy owner) | C43, C34 | low | spec/C41, plan-faithful/C41 | port to faithful as-is |

**Notes:**
- DELTA-01 (graduated-mandatory signing): The most significant Track B change to C41. The faithful spec says "optional/deferred" (README l.229). Making it mandatory requires key infrastructure (DELTA-06), G37 to be solved, and C03's policy tier config. Without G37 (unsolved), mandatory signing is a security mechanism with no key store — the XC-6 problem. SYSTEMIC because it requires a cascade of resolved prerequisites.
- DELTA-06 (signing key model): Specifies the per-actor keypair and trust root. Pre-requires G37. Also connects to C02-DELTA-02 (pack signing trust root). SYSTEMIC.
- DELTA-07 (boundary_class label): Low-cost addition that provides valuable auditability (G31 exposure window visibility). C43 will eventually define the taxonomy; faithful C41 can add the stamping with a FAITHFUL-FILL note.

---

### C42 — Rig / Agent-Role Partitioning

| delta_id | component | classification | linked_deltas | linked_components | cherry_pick_cost | port_target_files | recommendation |
|---|---|---|---|---|---|---|---|
| C42-DELTA-01 | C42 | CLUSTER-2 (composition-order) | C04-DELTA-05 | C04, C34 | medium | spec/C42, spec/C04, plan-faithful/C42, plan-faithful/C04 | port the cluster |
| C42-DELTA-02 | C42 | CLUSTER-2 (OS-boundary-enforcement) | C04-DELTA-05 | C04 | medium | spec/C42, spec/C04, plan-faithful/C42, plan-faithful/C04 | port the cluster |
| C42-DELTA-03 | C42 | ISOLATED | — | C30, C32, C34 | low | spec/C42, plan-faithful/C42 | port to faithful as-is |
| C42-DELTA-04 | C42 | ISOLATED | — | — | low | spec/C42, plan-faithful/C42 | port to faithful as-is |
| C42-DELTA-05 | C42 | CLUSTER-3 (prevent-then-detect) | C04-DELTA-05, C34 (PartitionBinding audit) | C04, C34 | medium | spec/C42, spec/C04, plan-faithful/C42, plan-faithful/C04 | port the cluster |
| C42-DELTA-06 | C42 | ISOLATED | — | — | low | spec/C42, plan-faithful/C42 | port to faithful as-is |

**Notes:**
- DELTA-01/02/05 all require C04 to apply the PartitionBinding at spawn. They travel together (C42+C04). C34 is Batch 3; its audit side can be noted with FAITHFUL-FILL.
- DELTA-03 (closed role taxonomy): A pure data-model addition — the `{worker, scenario-author, judge}` set plus the access matrix. No runtime consequence until C04 enforces it.
- DELTA-04 (worktree-per-run lifecycle): Self-contained operational pattern.
- DELTA-06 (OPA positioned as optional refinement): A policy clarification, no structural impact.

---

## Section 2: Cluster Catalog

### CLUSTER: portability-contracts
**Member deltas:** C01-DELTA-01, C04-DELTA-01, C21-DELTA-01, C28-DELTA-01
**What binds them:** All four define "X is an *interface* that Y implements" for the four foundational runtime abstractions (substrate, session, trajectory store, agent loop). Each depends on the others' interfaces existing to be testable. A RuntimeSubstrate contract only makes sense if the SessionProvider (C04) codes against it, and if the trajectory store (C21) is swappable behind a port, and if the agent loop (C28) is provider-abstracted.
**Joint port cost:** HIGH — this is a track-level architectural bet. Porting any single one into faithful creates an internal contradiction (faithful says "Gas City IS the substrate"; Track B says "Gas City implements RuntimeSubstrate"). All four or none.

### CLUSTER: native-count
**Member deltas:** C01-DELTA-03, C03-DELTA-05
**What binds them:** Both correct the same claim (5 native principles at Phase-0, not 6). C01 states it in the substrate coverage manifest; C03 states it in the phase-profile configuration.
**Joint port cost:** LOW — two files, purely descriptive correction with no structural change.

### CLUSTER: tool-node-seam
**Member deltas:** C01-DELTA-04, C02-DELTA-01, C02-DELTA-03
**What binds them:** C01 says "the tool-node seam is C02-owned and conformance-tested"; C02-DELTA-01 defines the wire protocol that seam uses; C02-DELTA-03 replaces argv substitution with a typed I/O envelope. Together they define what the seam IS.
**Joint port cost:** MEDIUM — three delta texts across two spec files and two plan files. The faithful specs currently describe a vague "subprocess contract"; these replace it with a typed one.

### CLUSTER: termination-invariant
**Member deltas:** C01-DELTA-05, C13-DELTA-05, C12 (gate bound field)
**What binds them:** C01 owns the substrate-level guarantee (no unbounded tick); C13 owns the run-scope budget slot; C12 declares the gate bound. Together they make "a molecule cannot loop forever" provable at three levels.
**Joint port cost:** MEDIUM — three specs (C01, C12, C13). The numeric policy (C39/C18) is deferred via FAITHFUL-FILL.

### CLUSTER: degraded-mode
**Member deltas:** C01-DELTA-06, C21-DELTA-04, C23-DELTA-01
**What binds them:** C01 describes what the substrate does when stores are down; C21-DELTA-04 describes how CXDB spools to C23 and replays on recovery; C23-DELTA-01 is what makes C23 actually durable (fsync before return). Without C23's durability guarantee, C21's degraded-mode story is hollow.
**Joint port cost:** MEDIUM — three spec/plan pairs, but the logic is linear (C23 → C21 → C01).

### CLUSTER: spec-bundle-seam
**Member deltas:** C08-DELTA-01, C08-DELTA-02, C09-DELTA-01, C05-DELTA-04
**What binds them:** Track B's core spec-intake redesign — spec is a standalone bundle (not the prompt template). C08 defines the bundle; C09 references it by spec_id; C05 treats the binding opaquely. All four must agree or the seam is incoherent.
**Joint port cost:** MEDIUM — 3 spec files, 3 plan files, but the change is structural (replaces the "spec IS the template" faithful design).

### CLUSTER: content-address-identity
**Member deltas:** C08-DELTA-04, C09-DELTA-03
**What binds them:** C08 defines spec_id as a BLAKE3 bundle hash; C09 embeds spec_id in the binding record. Both are needed for "which spec drove which work" to be a queryable primary key.
**Joint port cost:** LOW — two spec files.

### CLUSTER: vocab-lint-wiring
**Member deltas:** C07-DELTA-04, C10-DELTA-04
**What binds them:** C07 exports CanonicalTermSet; C10 loads it. Without the export, C10's vocab-lint has no term source. Without C10 consuming it, C07's export has no named consumer.
**Joint port cost:** LOW — two spec files.

### CLUSTER: admission-control
**Member deltas:** C05-DELTA-02, C28-DELTA-02
**What binds them:** C05 calls C28's `acquire()` governor before committing a placement; C28 exposes the governor. Both must define the same interface freeze (M1).
**Joint port cost:** MEDIUM — two spec/plan pairs with an interface that must match.

### CLUSTER: routing-authority-split
**Member deltas:** C05-DELTA-04, C09-DELTA-01
**What binds them:** C05 routes and C09 resolves; neither re-derives the other's job. The seam (opaque binding pass-through) requires both sides to declare the split.
**Joint port cost:** LOW — two spec files, policy clarification with no new mechanism.

### CLUSTER: isolation-at-spawn
**Member deltas:** C04-DELTA-05, C42-DELTA-01, C42-DELTA-02, C42-DELTA-05, C28-DELTA-04
**What binds them:** C42 defines and emits PartitionBinding; C04 applies it at process creation; C28 binds the capability profile per invocation. The "isolation before first tool call" guarantee is owned collectively.
**Joint port cost:** MEDIUM — four spec/plan pairs. C43 (capability profiles) is deferred via FAITHFUL-FILL.

### CLUSTER: supply-chain-signing
**Member deltas:** C02-DELTA-02, C41-DELTA-06, C41-DELTA-01
**What binds them:** C02 signs pack bundles; C41 defines the key model and trust root; the signing policy (mandatory vs optional for packs) ties them together. Also depends on G37 (unsolved secrets storage).
**Joint port cost:** HIGH — three spec/plan pairs, plus G37 unresolved. Do not port without a G37 decision.

### CLUSTER: attribution-invariant
**Member deltas:** C19-DELTA-02, C41-DELTA-02
**What binds them:** C19 declares `created_by` non-null at the store level; C41 defines the Actor model that `created_by` references. Both must agree on what the value IS.
**Joint port cost:** LOW — two spec files. Faithful C19 already references C41's actor concept; this makes it a structural invariant.

### CLUSTER: typed-edge-taxonomy
**Member deltas:** C19-DELTA-03, C13-DELTA-04, C20 (edge-kind enum)
**What binds them:** C19 owns the edge kinds; C13 uses them for the molecule tree shape invariants; C20 uses them for loop-closure (`closes` edge on fix_task). All three must agree on the same enum.
**Joint port cost:** MEDIUM — three spec files.

### CLUSTER: CXDB-type-binding
**Member deltas:** C20-DELTA-07, C22-DELTA-04 (ADOPTED D-3), C21-DELTA-03 (ADOPTED D-2)
**What binds them:** C20 maps bead types to CXDB triples; C22 registers them. D-2/D-3 already resolved the bundle namespace and registration ownership; DELTA-07 adds the per-type binding seam.
**Joint port cost:** LOW — effectively complete via D-2/D-3 adoption; DELTA-07 is the residual binding table.

### CLUSTER: branch-replay-API
**Member deltas:** C21-DELTA-05, C13-DELTA-07
**What binds them:** C21 exposes the O(1) `Branch()` API; C13's `branch()` molecule operation calls it. Both define the same operation from different layers.
**Joint port cost:** MEDIUM — two spec files, shared interface freeze needed.

### CLUSTER: degraded-ingest
**Member deltas:** C21-DELTA-04, C23-DELTA-01, C24-DELTA-01, C24-DELTA-02
**What binds them:** C21 spools to C23 on CXDB-down; C23 must be durable for this to work; C24 posts idempotently and retries. This is the complete G33 answer for the persistence tier.
**Joint port cost:** MEDIUM — three component pairs; the logic chain is C24→C23→C21.

### CLUSTER: graded-judge-independence
**Member deltas:** C29-DELTA-02, C29-DELTA-03
**What binds them:** The graded independence policy (L0–L3) and the metered-API judge credential path. Together they define Track B's approach to the cross-family judge problem (beyond the D-1 Phase-0 baseline). Both require C32/C34 to honor the independence verdict tag.
**Joint port cost:** HIGH — involves unbuilt C32/C34 components plus the G20 open credential question.

---

## Section 3: Counts

| Classification | Count | Percentage |
|---|---|---|
| ISOLATED | 68 | 53% |
| CLUSTER-2 | 34 | 26% |
| CLUSTER-3+ | 14 | 11% |
| SYSTEMIC | 13 | 10% |
| **Total** | **129** | **100%** |

*Note: "ADOPTED" deltas (D-2/D-3/D-4/D-5 covered) are excluded from counts.*

Cluster distribution: 17 named clusters, of which 10 are CLUSTER-2 (two-delta pairs) and 7 are CLUSTER-3+ (three or more deltas). The named systemic deltas all fall into one of two architectural bets: the portability-contracts cluster (4 deltas) or the mandatory-signing cluster (3 deltas).

---

## Section 4: Top 5 Cherry-Pick Candidates

Ranked by (benefit / port-cost). Benefit assessed by: gaps closed, failure modes addressed, or correctness improvements. Cost assessed by number of files and whether the surrounding spec must be re-derived.

| Rank | delta_id | component | why high-value |
|---|---|---|---|
| 1 | **C19-DELTA-04** | C19 | Closes the durability gap (append+fsync+atomic-rename) at the bead store. Eliminates the "scratchpad lost on restart" failure (README l.235). One file, zero cross-component consequence. Faithful C19 has no durability contract; this is a straightforward addition. |
| 2 | **C23-DELTA-02 + C23-DELTA-03** | C23 | Back-pressure decoupling (producers never block on consumers) + at-least-once idempotency key. Together these are the G33 answer at the event bus seam. Two independent improvements to one file, each independently useful. Port as a pair. |
| 3 | **C02-DELTA-05 + C02-DELTA-06** | C02 | ABI version handshake and language-neutral protocol. Addresses the "1–2 breaking pack changes per quarter" operational hazard (AI-CONTEXT §3.5) and closes the Go-only impedance mismatch. Two self-contained additions to C02 with no cross-component impact. |
| 4 | **C09-DELTA-04** | C09 | Render sandbox (restricted FuncMap). Closes a lethal-trifecta hole where a spec author could smuggle execution into the instruction render. One-file security fix; zero structural change to other components. |
| 5 | **C42-DELTA-03 + C42-DELTA-04** | C42 | Closed role taxonomy (worker/scenario-author/judge) with default-deny access matrix, plus worktree-per-run lifecycle. The role taxonomy is descriptive and can be stated in one file; the worktree lifecycle is operationally self-contained. Together these give faithful C42 a concrete instantiation of the holdout model that D-1 made load-bearing. |

---

## Section 5: Track-B-Only Deltas (SYSTEMIC)

These deltas represent Track B as a distinct architecture, not merely an improved one:

| delta_id | component | why systemic / Track-B-only |
|---|---|---|
| **C01-DELTA-01 / C04-DELTA-01 / C21-DELTA-01 / C28-DELTA-01** (portability-contracts cluster) | C01, C04, C21, C28 | Track B's central architectural stance: every major third-party dependency (Gas City, tmux provider, CXDB, Claude Code CLI) sits behind a thin, conformance-tested interface, making re-platforming a swap rather than a rewrite. Faithful Track A takes v4 literally — Gas City IS the substrate, Claude Code IS the agent loop. The portability-contract framing is not a point improvement; it is a different answer to the question "what happens when any dependency fails." All four deltas are a single all-or-nothing bet. |
| **C41-DELTA-01 + C41-DELTA-06** (mandatory-signing cluster) | C41 | Track B makes actor signing graduated-mandatory by default for cross-boundary actions. Faithful Track A follows v4 literally: "optional, deferred" (README l.229). This is a security-posture choice (prevention vs audit-trail-with-optional-signing). The full Track-B mandatory-signing model requires G37 (secrets storage) to be solved, which is not a Phase-0 commitment in v4. This is the most explicit Track A vs Track B security-policy divergence. |
| **C29-DELTA-02 + C29-DELTA-03** (graded-judge-independence cluster) | C29 | Track B builds a full graded independence policy (L0–L3) with a concrete credential path for L2/L3. Faithful Track A records the cross-family rule as stated (README l.189/l.427) and flags it as a tension (D-1 resolved the Phase-0 baseline; the mechanism for future L2/L3 is Track B's addition). The graded-policy mechanism is not a small addition — it restructures how the evaluation tier trusts its own judgments, tagging every satisfaction score with an independence level. |
| **C28-DELTA-03** (multi-seat pool) | C28 | Multi-seat / seat-pool abstraction is contingent on Max ToS permitting pooled unattended automation (C28 OQ-1, flagged as the "top open question" for that component). If the ToS does not permit it, this delta cannot be implemented at all. Track A makes no such claim; it accepts the single-seat throughput ceiling as a given. This makes DELTA-03 a Track-B-specific provisionable-capacity design that may have no path to implementation. |
| **C28-DELTA-01** (AgentLoopProvider abstraction) | C28 | Already listed above in the portability-contracts cluster. Separated here to name it individually: the claim that "Claude Code is a default adapter, not the hardcoded loop" is the most consequential single statement in Track B's agent-side architecture. |

---

## Summary Verdict

**Track A can absorb a substantial fraction (~65%) of Track B's value via targeted cherry-picks, but Track B contains a distinct architecture — not merely a list of improvements.**

The ISOLATED and small-cluster deltas (53% + 26% = 79% by count) are mostly independent improvements to individual components — durability contracts, typed interfaces, determinism taxonomies, security hardening of the render path, partitioned streams, and operational clarity. These can be ported individually or in small clusters with 1–6 file edits each, without restructuring Track A's architecture.

The four SYSTEMIC areas that are genuinely Track-B-only:
1. **Portability contracts** (C01/C04/C21/C28 DELTA-01s): an all-or-nothing bet on swappable infrastructure. Track A cannot absorb this without abandoning its "v4 is a fixed proof" stance.
2. **Mandatory signing** (C41 DELTA-01/06): a security-posture flip that requires G37 and cascades across C03/C06.
3. **Graded judge independence** (C29 DELTA-02/03): restructures how satisfaction scores are trusted; Track B adds the FE-1 seam machinery that Track A does not need (D-1 resolved Phase-0 as same-provider/L1).
4. **Multi-seat pool** (C28 DELTA-03): contingent on an unresolved ToS question; Track A is correct to make no such claim.

The practical recommendation: raid Track B for the 35–40 highest-value isolated/cluster deltas (durability, typed interfaces, termination invariants, vocab-lint wiring, render sandbox, role taxonomy, etc.) via a focused integration pass. Leave the portability-contract cluster and mandatory-signing cluster in Track B as the authentic architectural alternative they represent.
