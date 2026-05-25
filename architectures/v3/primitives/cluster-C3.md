# Cluster C3 — Scenario storage & holdout (P-08 through P-13)

This file contains the Phase-3.5 buildability sketches for the six primitives in cluster C3, dispatched per the [hybrid (option C) shape](../decisions/auto-001-phase-3.5-dispatch-shape.md#revised-decision) and the [two-part rule](../phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive). One section per primitive, each carrying a contract restatement, construction path (named tool/library + integration sentence), corpus-why citation, research-grade-uncertainty flag, and buildability verdict.

Per the [cluster-subagent rules](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents), this subagent renders **no same-vs-distinct verdicts** on primitives across candidates. P-08 vs P-09 collapse, and P-10 vs the typed-object stores in U-A/U-B/D7-U-1, are explicitly deferred to Phase 4.2 and per-primitive sketches. The sections below are honest per-primitive evidence; whether evidence accumulated here merits collapse is a downstream call.

---

## P-08 — Scenario storage (out-of-tree, holdout-partitioned)

### Contract restatement

An append-only scenario store whose entries are typed objects carrying (a) prose statement, (b) acceptance-criterion shape declaration (point-spec vs. region-spec per [F39](../failure-modes-v3.md)), (c) provenance (operator-authored / generated / codebase-derived), (d) staleness timestamp, (e) `protects: RULE-ID` linkage to invariants, and (f) a **partition tag** that places the scenario into either the *training* (builder-visible) or *holdout* (builder-invisible) subset. The substrate enforces the partition: builder-role credentials cannot read holdout-tagged entries; judge-role credentials read both but cannot rewrite the partition tag. The store is content-addressed and append-only, so a scenario's partition assignment is durable from the moment it is written.

The load-bearing design content is **not** the storage mechanics but **the partition discipline as a substrate-enforced, role-keyed access boundary**. This is what greenfield's D-4 (per [`§1.S2`](../tracks/greenfield-substrate-first.md) of GF-S and [§1.3 / §4 D-4](../tracks/greenfield-methodology-first.md) of GF-M) and brownfield's in-model partition (per [§1 / §4 D-4](../tracks/brownfield-legacy-ingestion-first.md) of BF-L) require to keep [F28 (holdout leakage)](../failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders) from going ambient under [F53 (voluntary-discipline fragility)](../failure-modes-v3.md).

### Construction path

A typed-object store on top of a content-addressed blob backend (Git LFS or an S3-compatible object store with object-versioning enabled) plus an **attribute-based access control (ABAC) policy layer** expressed in OPA Rego. Integration sentence: each scenario object's manifest carries a `partition: train|holdout` field; the Rego policy evaluates incoming reads against the requester's role token (`role=builder` denies reads where `partition=holdout`; `role=judge` allows both), and the policy is itself versioned alongside the store so partition-rule edits are auditable. The substrate need not invent new primitives — OPA's `input.resource.partition` against `input.subject.role` is the canonical Rego shape, and the storage backend supplies content addressing for free.

### Corpus-why citation

[F28 — Holdout leakage / acceptance criteria seen by builders](../failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders) is rated `critical` for greenfield and `high` for brownfield. GF-S [§1.S2](../tracks/greenfield-substrate-first.md) names the partition as the substrate-enforced precondition without which D-4 is methodology-optional and therefore F53-fragile. BF-L [§1 ¶6](../tracks/brownfield-legacy-ingestion-first.md) re-frames the partition for codebase-derived scenarios but preserves the substrate-enforcement requirement.

### Research-grade-uncertainty flag

`none`. Both the storage substrate and the ABAC overlay have widely-deployed off-the-shelf parts.

### Buildability verdict

**`designed-system`.** The index pre-tagged P-08 `commodity (key partition discipline is the design content)`; this sketch surfaces that the partition discipline meets the [working-definitions §Substrate](../phase-3.4-decisions-resolved.md#substrate) criterion that "designed-system substrates… need a more detailed construction path (named tools, named techniques, named prior-art references)" — the storage half is commodity, the partition-enforcement half is a designed integration. Calling the whole primitive `commodity` would understate the load-bearing role of the access-control integration and the F28-criticality of getting it right.

---

## P-09 — Held-out scenario runner

### Contract restatement

A deterministic replay loop that takes a holdout-partitioned scenario reference (resolved against P-08) and the current agent / build artifact, runs the scenario's acceptance check, and returns a typed pass/fail verdict with attached evidence (the trajectory of the replay, the assertion result, any side-effect log). The runner is invoked at gate boundaries (e.g., BF-M stage 7 acceptance per [§1.1 stage 7](../tracks/brownfield-methodology-first.md), or GF-S `§3 step 6` per [`§3`](../tracks/greenfield-substrate-first.md)) and must run with builder credentials *suppressed* — its read credential against P-08 is the judge-role token, not the builder-role token, so the runner can read holdout scenarios but cannot leak their content back into builder context.

### Construction path

A standard test-runner harness (pytest / Bazel / Buck2 / a per-language equivalent) wrapped in a thin orchestrator that fetches the holdout-tagged scenarios from P-08 over the judge-role credential, materialises them into a tmpfs working dir for the duration of the run, and emits a typed verdict envelope to the trajectory store (P-05). Integration sentence: pytest's `pytest_collection_modifyitems` hook supplies the per-scenario test-case yield point, the orchestrator drives selection by `partition=holdout AND protects ∈ {rules-under-test}`, and the runner subprocess inherits the judge-role token via a scoped environment variable that the parent strips before any builder process is forked. Determinism is enforced by pinning the runner image hash, the model snapshot, and the seed — the same scenario, same artifact, same model snapshot must yield the same verdict bit-for-bit.

### Corpus-why citation

BF-M [§1.1 stage 7](../tracks/brownfield-methodology-first.md) names the held-out runner as the load-bearing acceptance gate that contests Jaymin's brownfield-L3 ceiling (per [CTR-A5](../tracks/brownfield-methodology-first.md#21-uc1-mapping-test--lights-out--l5-tension-brief-21)). GF-M [§1.3 / §2.9](../tracks/greenfield-methodology-first.md) treats the runner as the operational realisation of D-4 against [F28](../failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders). BF-L [§1 ¶6](../tracks/brownfield-legacy-ingestion-first.md) requires the runner be "ingestion-aware" so partition discipline survives codebase-derived scenarios.

### Research-grade-uncertainty flag

`none`. Test-runner harnesses are decades-deployed; the only non-trivial integration is the credential scoping, which is OS-level standard.

### Buildability verdict

**`commodity`.** The runner is a thin orchestrator over commodity test-running and credential-scoping infrastructure. (Note: this sketch surfaces *one* honest piece of evidence that may matter at Phase 4.2 collapse discussion — the runner's substantive content is largely "call P-08 with the judge-role token and run the result"; whether that constitutes a distinct primitive vs a read-API on P-08 is the Phase 4.2 question and is not decided here.)

---

## P-10 — Coordination medium (CI-friendly, content-addressed)

### Contract restatement

A shared blob / object medium accessible by both CI workers and agents, addressed by content hash, supporting typed event-log writes for cross-cycle coordination. The medium must be translatable to environments that share only `git` + GitHub issues/comments (per GF-S [§1.S7](../tracks/greenfield-substrate-first.md), explicitly *not* an in-memory mail bus à la Overstory). Read/write semantics: append-only event log + content-addressed artifact store; cycle outputs land as content-addressed blobs and the event log carries pointers to them.

### Construction path

Git's content-addressable object store (the `.git/objects` SHA-256 tree, post-SHA-256-transition) for the artifact half, plus a typed event log on top of Git refs (one ref per event stream, fast-forward-only) or alternatively IPFS for the artifact half with a CRDT log (Automerge) for the event half. Integration sentence: cycle outputs are written as Git blob objects under a `refs/factory/artifacts/<sha256>` namespace; the typed event log is a Git ref `refs/factory/events/<stream>` that the substrate appends to via `git update-ref --create-reflog` (fast-forward-only, signed commits per [F32](../failure-modes-v3.md#f32--mailinjection--unsigned-coordination-messages) HMAC requirement), and CI workers pull events by ref-walking. The Git-only path means GitHub Actions / Buildkite / any standard CI runner already has access without a separate broker.

### Corpus-why citation

GF-S [§1.S7](../tracks/greenfield-substrate-first.md) names this primitive as the substrate's explicit refusal of in-memory mail buses on translatability grounds, citing [Round-2 §5.1](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md): Overstory-style coordination does not survive the move into CI environments that share only `git` + issues/comments. F32 motivates the signing discipline.

### Research-grade-uncertainty flag

`none`. Git's content-addressable store is the canonical example of the shape; IPFS is a drop-in alternative for cross-organisation cases.

### Buildability verdict

**`commodity`.** Construction is well-understood Git plumbing or IPFS-plus-CRDT. (Same-vs-distinct against the typed-object stores P-28 across U-A / U-B / U-C / D7-U-1 is **not** rendered here per the cluster-subagent rules — those are per-primitive sketches addressing that question for their candidate-specific contracts.)

---

## P-11 — Cold-Start Bench (HMAC-signed scenario store)

### Contract restatement

A crypto-signed seed scenario bench, immutable after day-0 sign-off. The bench is the day-0 instance of P-08 (operator-authored, Kaner-shaped, region-spec-flagged), but with two additional substrate properties: (a) every entry carries an **HMAC signature** computed at authoring time against a key the operator controls, so post-hoc tampering is detectable; (b) the bench is **frozen** after the day-0 sign-off event — subsequent writes append to a *different* scenario partition, never to the bench itself. The bench is the "only out-of-distribution signal that exists before code exists" (per GF-C [§1.1 ¶3](../tracks/greenfield-cold-start-first.md)) and is the substrate-side anchor that makes [F1 / F25 / F40 / F41 / F46](../tracks/greenfield-cold-start-first.md#0-axis-declaration-and-defense-pre-respond-to-phase-3-adversarial) tractable on day 0.

### Construction path

P-08's storage substrate (Git LFS / S3-class object store with object-versioning) plus an **HMAC-SHA256 envelope** computed at write time using a Yubikey-held or KMS-held operator key (AWS KMS `GenerateMac` / GCP Cloud KMS `MacSign` / hashicorp Vault Transit's HMAC operation). Integration sentence: at bench-authoring time, each Kaner-shaped scenario is canonicalised (JCS / RFC 8785), MAC-signed by the KMS using `algorithm=HMAC_SHA_256`, and the resulting `{scenario, mac, key-id, timestamp}` envelope is appended to the bench partition; immutability is enforced by an OPA policy that rejects any write to the bench partition after the `bench-frozen` event has been emitted to P-10's event log. Verification at read time is `kms:VerifyMac` — cheap, deterministic, and side-channel-resistant.

### Corpus-why citation

GF-C [§1.1 ¶3](../tracks/greenfield-cold-start-first.md) names the Cold-Start Bench as the day-0 holdout that addresses D-2's vacuousness on day 0, citing Cem Kaner's 2003 scenario-testing tradition ([`followup/09`](../../../research/followup/09-methodology-ancestors.md)). [F32 (mail-injection / unsigned coordination)](../failure-modes-v3.md#f32--mailinjection--unsigned-coordination-messages) motivates the HMAC discipline; GF-C [§1.2 sub-phase B](../tracks/greenfield-cold-start-first.md) explicitly invokes F32 for bench signing. The five critical greenfield F-modes that converge on day 0 ([F1 / F25 / F40 / F41 plus F46](../tracks/greenfield-cold-start-first.md#0-axis-declaration-and-defense-pre-respond-to-phase-3-adversarial)) make the bench's existence load-bearing.

### Research-grade-uncertainty flag

`none`. HMAC-SHA256 + KMS signing + an OPA append-policy gate is uncontroversial cryptographic engineering.

### Buildability verdict

**`commodity`.** HMAC + scenario storage + freeze-policy is straightforward. The substantive content is the *day-0 process* (operator + Council interrogation, bench-construction sub-phase per GF-C [§1.2](../tracks/greenfield-cold-start-first.md)) — that lives at the methodology layer, not the substrate.

---

## P-12 — Deterministic linter framework

### Contract restatement

A rule-engine substrate that hosts deterministic per-cycle checks against typed artifacts (intent blocks, EARS-formed acceptance criteria, change-intent prose, scenario manifests). The framework supplies: (a) a rule-registration API (rules are pure functions over the parsed artifact AST), (b) a per-cycle dispatch surface that runs the registered rule set and emits typed violations, (c) a severity-and-threshold layer that gates the cycle on configured violation counts. The framework itself is **rule-set-agnostic** — it does not ship the INCOSE GtWR R7–R35 rules (that's P-16's content); it ships the engine those rules run on.

### Construction path

A pluggable linter framework such as ESLint's `Linter` class (rule = `{create(context) → visitor}` over an AST), or RuboCop's `Cop` API, or — for prose / requirements artifacts specifically — a thin custom framework built on top of `tree-sitter` (parser) + a simple visitor protocol. Integration sentence: each deterministic check (R7 universal-quantifier ban, R8 superlative ban, R9 vague-term ban, the BF-M F38 mitigation per [§1.1 stage 6](../tracks/brownfield-methodology-first.md)) is implemented as a rule object that exposes a `check(node, context) → violations[]` method; the framework's per-cycle entry point parses the artifact, walks the tree once, dispatches to all registered rules, and emits a typed `{rule-id, severity, location, message}` envelope to P-05 (trajectory) plus a gate-decision bit. ESLint's mature plugin ecosystem and rule-isolation discipline are the named prior art for the engine shape.

### Corpus-why citation

[F38 — Vocabulary lint debt](../failure-modes-v3.md#f38--vocabulary-lint-debt) is rated greenfield-`high`; the F-mode definition itself notes the failure is "authoring-side and deterministically detectable (unlike F36/F37 which are model-capability limits)" — exactly the load this framework is designed to carry. BF-M [§1.1 stage 6](../tracks/brownfield-methodology-first.md) names deterministic linters as the F38 mitigation; GF-S [§1.S8](../tracks/greenfield-substrate-first.md) treats the linter framework as the substrate component of the four-guard mediator. [F51 (Ashby-deficient probabilistic guard)](../failure-modes-v3.md) motivates the "deterministic, not LLM-judge" framing.

### Research-grade-uncertainty flag

`none`. Pluggable linter frameworks are widely-deployed (ESLint, RuboCop, ruff, golangci-lint).

### Buildability verdict

**`commodity`.** The framework half is uncontroversial off-the-shelf engineering. P-16 (the specific INCOSE GtWR R7–R35 rule library that runs on top) is sketched separately as a `designed-system` primitive; this sketch covers only the substrate engine.

---

## P-13 — Maintenance loop (continuous reconciliation)

### Contract restatement

A low-cadence continuous job that compares the substrate's stored model of the system against the system's current reality, emits typed drift events when divergence exceeds a configured threshold, and triggers downstream reconciliation cycles. In the BF-L context (per [§1 ¶4](../tracks/brownfield-legacy-ingestion-first.md)), the maintenance loop re-runs ingestion deltas against the Codebase Model (P-26), reconciles invariants, and refreshes the model's six views. The loop is the brownfield-specific defence against [F34 (cross-layer drift)](../failure-modes-v3.md), [F55 (behavioural drift)](../failure-modes-v3.md#f55--behavioural-drift-self-reference-loop), and [F57 (design-authority erosion)](../failure-modes-v3.md).

### Construction path

A scheduled job runner — cron / systemd timers for single-host deployments, or a managed equivalent (GitHub Actions `schedule:` triggers, Kubernetes `CronJob`, Temporal scheduled workflows) for distributed ones — driving a reconciliation worker that diffs the stored model against a fresh re-ingestion sample. Integration sentence: the cron entry fires the reconciliation worker at the configured cadence (BF-L [§7 OQ-3](../tracks/brownfield-legacy-ingestion-first.md) flags the cadence itself as a tunable open question); the worker calls into P-22 (codebase index) and P-07 (telemetry ingestor) for a fresh snapshot, diffs against the model's stored snapshot using a per-view diff function, and emits drift events to P-10's typed event log when per-view divergence exceeds the per-view threshold. Temporal's durable-execution model is the named prior art for the reconciliation-as-workflow shape; cron + a Python script suffices for a minimal implementation.

### Corpus-why citation

BF-L [§1 ¶4](../tracks/brownfield-legacy-ingestion-first.md) names the maintenance loop as the third of the three loops that define the architecture, citing [F34](../failure-modes-v3.md), [F55](../failure-modes-v3.md#f55--behavioural-drift-self-reference-loop), and [F57](../failure-modes-v3.md). [F34 / F55 / F57](../failure-modes-v3.md) collectively are the cross-cycle drift cluster the loop directly addresses; F20 (maintenance-vs-greenfield asymmetry) is the BF-L-specific corpus problem it operationalises (per [§2.4](../tracks/brownfield-legacy-ingestion-first.md)).

### Research-grade-uncertainty flag

`none`. Cron + reconciliation workers are commodity infrastructure.

### Buildability verdict

**`commodity`.** Construction is cron-plus-diff. The substantive design content is the *per-view diff threshold* policy (a cadence-vs-cost tradeoff per BF-L [§7 OQ-3](../tracks/brownfield-legacy-ingestion-first.md)), which lives at the architecture-configuration layer, not as substrate buildability.

---

## Cluster coda (commodity-cluster framing only)

Per the [Round-2 cluster-subagent rules](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents), only a "this whole cluster is commodity cloud engineering" coda is permitted for pure-commodity clusters; same-vs-distinct verdicts are forbidden.

Five of the six primitives in this cluster (P-09, P-10, P-11, P-12, P-13) land at `commodity` — their construction paths compose off-the-shelf parts (Git plumbing, KMS HMAC, ESLint-class linter frameworks, cron, pytest, OPA). P-08 lands at `designed-system` because the substrate-enforced partition discipline is the load-bearing content; storage mechanics are commodity but the role-keyed access-control integration is the designed part. No primitive in this cluster carries a research-grade-uncertainty flag.
