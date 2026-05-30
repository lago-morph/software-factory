# C02 — Pack & tool-node ABI  (Spec, Track B)

> Source: README Part 4 (lines 107–108, 134–135, 154–202, 253–275 "Gas City pack" / "tool node" rows), README §"Licensing reality" (288, 334, 518), README Phase 0/1 (359–360, 389), §"Bets" (509); AI-CONTEXT §3.3 (vocab table — `pack`), §3.4 (smallest viable install / `pack.toml` `[imports.core]`), §3.5–3.6 (`internal/` paths, Provider extraction surface), §13.1 (`pack.toml`/`city.toml` skeletons), §13.3 (`[[tool]] type="subprocess"` invocation sketch), §11.1/§11.3 ("pack-based extension; no fork" decision); _meta gaps G29 (pack↔Go-library boundary / tool-node protocol undocumented), G06 (undefined vocabulary); F-MODE-COVERAGE F31 (single-provider floor), F44 (Bash/network/fs blast radius).
> Inventory ID: C02   Kind: interface   Status: sweep-1
> Deltas: DELTA-01 (specify the tool-node wire protocol — the undocumented seam G29 names; **define-if-greenfield, conform-or-shim if `gc` already fixes a convention — OQ1/G11**), DELTA-02 (pack bundle manifest = signed, versioned, dependency-declaring artifact, not just a TOML file; signing = **authenticated provenance**, RSI-gating needs a human-held trust root — see §6), DELTA-03 (typed I/O envelope + exit-code taxonomy replaces ad-hoc `{placeholder}`→argv string substitution), DELTA-04 (tool-node capability declaration feeds C43 isolation, not implicit broad access), DELTA-05 (ABI version handshake + compat policy absorbs Gas City's "1–2 breaking pack-schema changes/quarter"), DELTA-06 (language-neutral protocol — Go/Python/any-exec parity, since v4's tool nodes are already Go AND Python), DELTA-07 ("escape valve" fork-trigger criteria made explicit so "no fork" is a falsifiable claim, not a slogan).

## 1. Purpose & responsibility

C02 is the **sole extension surface** of Software Factory v4. v4 adds zero capabilities by importing Gas City as a Go library or forking it; *every* v4-authored capability — spec linter, DOT translator, workflow/discipline linters, the CXDB bridge, anomaly/clustering/diagnosis nodes, twins, A/B routing, the satisfaction aggregator — ships as a **pack** and runs through the **tool-node subprocess protocol**. C02 owns the two halves of that surface:

1. **The pack bundle contract** — what a distributable methodology bundle *is*: a versioned, dependency-declaring artifact carrying (a) config layers (TOML contributed to C03), (b) tool-node binaries/scripts, (c) prompt templates (C09), (d) capability descriptors, (e) a manifest with identity/version/signature.
2. **The tool-node ABI** — the **subprocess input/output protocol** by which Gas City (C01) invokes a tool node and a tool node returns results: how inputs arrive, how outputs/errors/exit codes are returned, the declared capability/isolation envelope, and the ABI-version handshake.

The load-bearing reason C02 exists as its own foundational component: v4's entire "no Go fork" thesis rests on the claim that **packs cover all extension needs** — yet the corpus never specifies the pack/runtime contract the claim depends on (G29). C02 *is* that contract.

What it is **NOT**:
- **Not the config-merge engine.** Packs *contribute* a config layer and declare capability descriptors; **C03** defines layer precedence and validation. C02 defines the bundle that carries the layer, not the merge.
- **Not the workflow node-graph.** A formula (C12) *references* tool nodes by name; C02 defines what a tool node is and how it's invoked, not how the DAG wires them.
- **Not the tool-node abstraction's catalog.** **C17** is the runtime-facing "unified interface for deterministic steps" (Gas City tool beads) and the registry of available nodes; C02 is the *binary↔runtime wire contract and packaging* underneath C17.
- **Not prompt-binding.** **C09** owns spec→template binding; C02 only specifies that templates are a bundle member.
- **Not the agent loop.** Tool *nodes* (C02) are deterministic subprocesses; the LLM *agent* is C28. C02 is explicitly the deterministic-first half of "models only where reasoning is required."
- **Not a Go-library SDK for Gas City internals.** That is precisely the surface C02 exists to make unnecessary (G29 / `internal/` paths).

## 2. Context & dependencies

- **Depends on:** **C01** (Gas City is the process that discovers packs, spawns tool-node subprocesses, and enforces partitions; C02 specifies the contract C01's loader/executor must honor). Reads config via **C03** (a pack is one `LayerSource`). Tool-node capability declarations feed **C43** isolation (DELTA-04).
- **Consumed by (foundational fan-out):** **C17** (tool-node abstraction sits directly on C02 — `Maps from A35,A17`, `Depends on C02`). Through C17/packs, essentially every custom v4 capability: C10 (spec linter), C14 (DOT translator), C15/C16 (workflow/discipline linters), C24 (CXDB bridge — "standalone tool-node binary in a pack"), C31 (Inspect AI wrapped as pack), C33 (satisfaction aggregator Go tool node), C35 (override hooks pack), C36/C37/C38 (Python tool nodes), C44 (per-twin Go binary), C47/C48 (DSPy/Optuna Python nodes, Unleash routing pack), C51 (gene-transfusion *produces* packs). C03 consumes C02's capability-descriptor declaration.
- **Sits at:** the Runtime Substrate, immediately above C01 and beside C03. It is the seam between "third-party runtime we do not modify" and "everything v4 builds." Foundational: a wrong ABI here forces a Go fork and collapses the cost thesis.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete signatures, JSON schemas, and a Mermaid invocation sequence land in sweep 2).

### 3a. Pack bundle contract (packaging surface)

- **`PackManifest`** (DELTA-02) — the bundle's identity record: `{ pack_id, version (semver), abi_version (range it speaks), imports (other pack_ids + version constraints), provides (capability_ids + tool-node names + template paths), tool_nodes (list of ToolNodeManifest), signature, transfused_from (C51 provenance) }`. v4 today only shows `[imports.core]` (a bare import with no version, no identity, no integrity). DELTA-02 promotes the bundle to a first-class versioned/verifiable artifact because packs are the *only* extension path and the supply chain into a self-modifying factory (C52) must be auditable.
- **`ToolNodeManifest`** — per node: `{ name, entrypoint (relative path to binary/script), runtime (native|python|node|wasm-…), abi_version, input_schema_ref, output_schema_ref, declared_capabilities (DELTA-04: fs-read/-write partitions, network egress allowlist, env keys, max wall-clock), deterministic (bool) }`.
- **`CapabilityDescriptor`** (shared seam with C03) — what config section the pack gates and its `requires`/`conflicts_with`; C02 carries it in the bundle, C03 validates it.
- **`PackImport`** — declared dependency on another pack (e.g. `[imports.core]`) with a version constraint; resolved into a load order.

### 3b. Tool-node ABI (the wire protocol — DELTA-01, the core G29 resolution)

The contract by which C01 invokes a node and the node replies. v4 shows only `command="inspect"`, `args=["eval","{scenario_path}","--task","{task}"]` with `{placeholder}` string substitution into argv and a `work_partition` (§13.3). That is a launch recipe, **not** an I/O protocol: it never says how structured inputs reach the node, how results/errors/diagnostics come back, what exit codes mean, or how a node negotiates ABI version. DELTA-01 specifies it:

- **Invocation (runtime → node):** Gas City spawns the entrypoint as a subprocess. Inputs are delivered as a **typed `ToolNodeRequest` envelope** — `{ abi_version, node_name, inputs (schema-validated object), context (bead_id, actor/created_by for C41, work_partition, deadline), capabilities_granted }` — written to **stdin as a single JSON document** (DELTA-03 replaces argv-template substitution as the *primary* path; argv/`{placeholder}` retained as a compatibility shim for trivial nodes). Large/binary inputs are passed **by content-address reference** (CXDB blob id / partition-relative path), never inlined.
- **Result (node → runtime):** a **`ToolNodeResponse` envelope** on **stdout as a single JSON document** — `{ abi_version, status, outputs (schema-validated), diagnostics[], emitted_beads[]?, metrics? }`. **stderr is reserved for human/log diagnostics only** (never the structured result), so a crashing node's stack trace can never be mis-parsed as output.
- **Exit-code taxonomy (DELTA-03):** `0` = success (response valid); `1` = handled tool failure (response carries structured error, workflow may branch on it); `2` = bad request / ABI mismatch (caller error — non-retryable); `3` = transient/retryable (node *advises* retry — **the C18 per-node iteration cap (C01-B DELTA-05) and C40 retry budget are authoritative; a node cannot force unbounded retries, preserving the F52 bound**); `>=124` reserved for runtime-imposed kill (timeout/partition violation). This lets the reconciler (C18) and durable Orders (C40) distinguish "retry" from "branch" from "abort" deterministically instead of guessing from a process exit.
- **ABI-version handshake (DELTA-05):** request carries the runtime's `abi_version`; node manifest declares the range it speaks; a mismatch fails fast as exit-2 with a typed `AbiIncompatible` diagnostic rather than corrupt I/O. Compat policy: additive (new optional fields) within a major; breaking changes bump major and are gated by manifest range — this absorbs Gas City's stated "1–2 breaking pack-schema/formula changes per quarter" (AI-CONTEXT §3.5) at a declared seam instead of silent breakage.
- **Capability grant/enforcement (DELTA-04):** the runtime passes `capabilities_granted` (the intersection of what the node *declared* and what C03/C43 *permit*); the node runs under that envelope (partition-scoped fs, egress allowlist). A node touching outside its grant is killed (exit ≥124) and the violation is an attributable event — **if and only if C43 supplies OS-level enforcement (seccomp/namespace/partition with teeth); absent that, the breach is detected-and-attributed only, not prevented (the G21 detection-vs-prevention trap — see OQ2).** This *threads and declares* the bound that converts F44's broad-access default from implicit to declared at the deterministic-tool layer; the *prevention strength* is owned by C43 (G31), not asserted here.

**Invariants**
- **No-fork invariant (DELTA-07):** any v4 capability expressible as {config layer + subprocess that speaks this ABI + prompt template} MUST be a pack; importing Gas City as a Go library or modifying its source is a *fork-trigger* event, not an extension. The only sanctioned fork-triggers are the three the corpus already names — new runtime `Provider`, modified reconciler, urgent upstream bugfix (README 334, §518; AI-CONTEXT §11.3) — and each MUST be recorded as an explicit escape-valve decision. "No fork" becomes falsifiable, not a slogan.
- **Language neutrality (DELTA-06):** the ABI is JSON-over-stdio + exit codes — no Go-specific calling convention. A Python node (PyOD/HDBSCAN/DSPy) and a Go node (aggregator/twin) are first-class equals. v4 *already* ships both, so a Go-only ABI would itself force per-language glue ≈ a fork by another name.
- **Determinism honesty:** a node manifest-flagged `deterministic=true` MUST be referentially transparent over (inputs, granted capabilities); the discipline linter (C16) and replay (C49) rely on this.
- **Stdout purity:** exactly one JSON `ToolNodeResponse` on stdout; any non-protocol stdout byte is a contract violation (exit-2-class), preventing the classic "a `print()` corrupted my JSON" failure.
- **Integrity:** a pack whose manifest signature fails verification is refused load (DELTA-02); load order respects `imports` topologically.

## 4. Data model / state

C02 is an **interface/contract** component — it owns *formats and protocol*, not a running store. Owned artifacts:

- **Pack bundle on disk:** `pack.toml` (manifest) + `tools/<name>/<entrypoint>` (binaries/scripts) + `templates/*.md` (C09) + packaged TOML config layer. Version-controlled (git), content-addressable; the bundle's identity is `{pack_id, version, content-hash}`.
- **ABI version namespace:** the protocol's own semver, independent of any pack's version and of Gas City's release version (DELTA-05). Three independent version axes — pack version, ABI version, Gas City version — explicitly decoupled so one can move without the others.
- **No durable runtime state.** Per-invocation request/response envelopes are ephemeral; persistence of *what a node did* lives in C19 (beads), C21 (CXDB trajectory), C23 (event bus) via the `context.created_by`/`emitted_beads` fields the ABI threads through (C41 attribution). C02 guarantees attribution is *carried*, not that it's *stored* (that's C41/C19/C23).
- **Capability/grant records** are derived (manifest ∩ C03/C43 policy), computed at load/invocation, not separately persisted.

## 5. Behavior

Two flows (sweep-2 adds Mermaid sequence + the JSON schemas):

**A. Pack load (startup / Phase transition)**
1. C01 discovers declared packs (`[imports.*]` resolved from `city.toml`/`pack.toml`).
2. C02 verifies each `PackManifest` signature + `abi_version` compatibility with the runtime; topologically orders by `imports` (DELTA-02/05).
3. Pack's config layer handed to C03 as a `LayerSource`; capability descriptors registered.
4. Tool-node manifests registered into C17's catalog; declared capabilities reconciled against C03/C43 policy → effective grant per node (DELTA-04).
5. Failure (bad signature, ABI mismatch, unsatisfied import, capability exceeding policy) = fail-closed refuse-load with a typed diagnostic.

**B. Tool-node invocation (per workflow step)**
1. Formula (C12) step names a tool node; sling/reconciler (C05/C18) selects it.
2. C01 builds a `ToolNodeRequest` (inputs schema-validated, context populated with bead_id + `created_by`, deadline, granted capabilities), spawns the entrypoint, writes the envelope to stdin (DELTA-01/03).
3. Node executes within its capability envelope; writes one `ToolNodeResponse` to stdout, diagnostics to stderr, sets an exit code from the taxonomy.
4. C01 validates the response against the node's `output_schema`; maps exit code → {commit outputs / branch on tool-failure / retry (C18/C40) / abort}; records an attributed event (C23) and any `emitted_beads` (C19).
5. Violations (stdout impurity, partition breach, timeout, ABI mismatch) → kill + typed failure + attributed anomaly (feeds C36).

## 6. Failure modes & handling

- **G29 (the seam itself) — primary, resolved.** The undocumented pack/runtime contract is specified in §3b (wire protocol) + §3a (bundle). This *is* the gap C02 closes; everything below is the failure handling that specification enables.
- **F44 (lethal-trifecta / blast radius at the tool layer).** Mitigation: declared capability envelope + runtime enforcement + kill-on-breach (DELTA-04). Residual: enforcement strength depends on C43's mechanism (OS partitions vs. policy); C02 *declares and threads* the grant but does not itself implement the sandbox — noted as a C02↔C43 seam, not claimed solved here.
- **F31 / no-fork pressure.** If a needed capability genuinely can't be expressed as a pack, silent forking would erode the thesis. Mitigation: explicit fork-trigger criteria + escape-valve decision record (DELTA-07) make any fork visible and justified rather than creeping.
- **ABI drift (Gas City "1–2 breaking changes/quarter").** Mitigation: version handshake + additive-within-major compat policy + manifest-declared range (DELTA-05); a runtime upgrade that breaks an old pack fails *fast and typed* at load, not mysteriously at step-time.
- **Malformed node output (the `print()`-corrupts-JSON class).** Mitigation: stdout-purity invariant + stderr-for-diagnostics + schema validation; a node that pollutes stdout is a deterministic exit-2 failure, never silently-wrong output.
- **Supply-chain / self-modification risk.** A self-bootstrapping factory (C52) emits new packs; an unsigned/unverified pack entering the load path is an RSI risk (G35-adjacent). Mitigation: signature + `transfused_from` provenance + fail-closed verify (DELTA-02). **Caveat (G35):** signing provides *authenticated provenance*, not RSI *prevention*. If the factory holds the signing key, a factory-emitted pack is self-signed and the signature only proves "the factory authored this," not "a human reviewed it." To actually gate RSI, the signing trust root MUST be **human-held or the signature gated at the C52/C53 human-review point** — otherwise DELTA-02 is audit, not control. Key custody is DEFERRED to C41 (provenance) + C51 (transfusion) + C57.
- **Cross-language impedance.** A Go-only ABI would silently re-introduce per-language glue. Mitigation: language-neutral stdio/JSON ABI (DELTA-06).
- **Capability over-grant.** A pack declaring more than policy allows must not silently get it. Mitigation: effective grant = declared ∩ permitted; excess = load failure (DELTA-04).

## 7. Cross-cutting

- **Security:** capability declaration + enforcement (DELTA-04) is the deterministic-layer half of the C43 posture; signed bundles (DELTA-02) guard the self-modification supply chain (C52/G35). Secrets reach nodes only as resolved values via the env keys their manifest declares (no plaintext in bundle; aligns with C03 DELTA-03).
- **Cost/scale:** subprocess-per-invocation has spawn cost; the ABI permits content-address-by-reference for large payloads (no inlining), and `deterministic` nodes are cacheable/replayable (feeds C49). No per-token cost — tool nodes are the *cheap, model-free* path (README 154), the structural cost lever against G32/G34.
- **Observability:** every invocation threads `created_by` + bead context and emits an attributed event (C23) + optional metrics; tool-node failures are first-class anomaly inputs (C36).
- **Ops:** three decoupled version axes (pack / ABI / Gas City) give operators independent upgrade control; phase transitions add packs without touching the runtime binary.
- **Parallelizability:** because the ABI is a frozen stdio/JSON contract, every downstream pack (C10/C14/C24/C31/C33/C36–38/C44/C47–48) can be built and tested against a stub runtime in parallel the moment §3 schemas freeze.

## 8. Acceptance criteria & test strategy

1. **Round-trip wire protocol:** a reference node given a `ToolNodeRequest` on stdin returns a schema-valid `ToolNodeResponse` on stdout; harness validates both against the frozen schemas (sweep-2 golden tests).
2. **Exit-code taxonomy:** a node returning each of {0,1,2,3,timeout-kill} drives the runtime into {commit, branch, abort-caller-error, retry, abort-killed} respectively (DELTA-03).
3. **Language parity (DELTA-06):** an identical contract test passes for a Go node and a Python node with no protocol-level difference.
4. **Stdout purity:** a node that writes a stray non-JSON byte to stdout fails as exit-2-class; a node that writes diagnostics to stderr still succeeds.
5. **ABI handshake (DELTA-05):** a node declaring an incompatible `abi_version` range is rejected at load with a typed `AbiIncompatible`, not invoked.
6. **Capability enforcement (DELTA-04):** a node attempting fs/network access outside its granted envelope is killed (exit ≥124) and emits an attributed violation event; a node declaring more than C03/C43 policy permits fails load.
7. **Bundle integrity (DELTA-02):** a pack with a broken signature or unsatisfied `imports` refuses to load; load order is topological.
8. **No-fork falsifiability (DELTA-07):** the three canonical v4 custom capabilities (CXDB bridge C24, satisfaction aggregator C33, a Python anomaly node C36) are each demonstrably expressible as a pack with zero Gas City Go imports — the standing proof that "packs cover all extension needs."
9. **Attribution carriage:** `created_by` present in the request is present on every `emitted_bead`/event the invocation produces (C41 precondition).

## 9. Open questions

- **OQ1 (→ review-log):** Does Gas City's *actual* tool-node mechanism already define a stdin/stdout/exit-code convention C02 must conform to, or is §3b a genuinely new contract we impose? G11 (Gas City unverified) means we cannot confirm the real `[[tool]] type="subprocess"` runtime behavior beyond the §13.3 launch-recipe sketch. If upstream already fixes a different I/O convention, DELTA-01/03 become *conform-or-shim* rather than *define* — and a divergence wide enough to need shimming is itself a soft fork-trigger. **Top open question** — it gates whether the whole "no fork" thesis is even testable. *(Mirrors the verification debt in G11.)*
- **OQ2:** Where does capability *enforcement* live — does C02's declared envelope get teeth from OS-level partitions/sandboxing (C43) or only from Gas City `read_partition`/`work_partition` config (which §13.3 shows but whose enforcement strength is unproven)? Determines whether DELTA-04 is real prevention or detection-only (the same trap G21 flags for holdout isolation).
- **OQ3:** Is the pack signature/verification model (DELTA-02) authored here or owned by C51 (gene-transfusion provenance) / C41 (attribution)? The `transfused_from` field straddles C02↔C51; the signature straddles C02↔C41. Needs an ownership ruling before sweep-2 schemas freeze.
- **OQ4:** ABI for *streaming / long-running* nodes — the single-request/single-response stdio model fits short deterministic steps, but a twin (C44) or a watch-loop bridge (C24, which "watches a directory") is long-lived. Does C24-shaped work use the tool-node ABI at all, or a separate daemon/service contract (`[[service]]`)? The boundary between "tool node" and "service" is undrawn in the corpus. (Mirrored in C17 OQ4.)
- **OQ5 (→ review-log XC-4):** `pack_id` is a fourth reverse-DNS-style identity namespace alongside the unreconciled CXDB/bead bundle-ids (C20 `v4.beads.v1`, C22 `strongdm.factory.v4`, C21 `softwarefactory.trajectory.v1`). As the supply-chain root, C02 should adopt whatever single naming convention the integrator's XC-4 ruling picks, so the factory has one identity scheme, not four. Not a C02-internal defect — flagged for the integrator.
