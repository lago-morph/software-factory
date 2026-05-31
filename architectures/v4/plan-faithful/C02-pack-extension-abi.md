# C02 — Pack & Tool-Node ABI  (Build Plan, Track A)

> Source / Spec ref: [`spec/C02-pack-extension-abi.md`](../spec/C02-pack-extension-abi.md)

C02 is an **interface/contract** component (no runtime engine of its own — that is C01). "Building" C02
means **specifying and freezing the two contracts** (pack bundle + tool-node ABI), then **conformance-
verifying** them against the real `gc` binary so the ~25 downstream packs can be authored against stable
shapes. The plan is therefore contract-first and verification-heavy, not code-heavy.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Pin pack-bundle layout | Freeze the on-disk pack tree: `pack.toml`, `agents/<name>/prompt.template.md`, tool-node binaries, formulas. | S | C01 install (G11) |
| **T2** Freeze `pack.toml` manifest schema | Concrete schema for `[imports.*]`, `[[tool]]`, hook regs, template refs, `schema_version`, and the reserved discipline keys (`[pack.safety]`, `[pack.derivation]`). | M | T1 |
| **T3** Freeze tool-node ABI (the G29 seam) | Concrete wire contract: arg/`{placeholder}` substitution rules, env, working dir = `work_partition`, output channel, exit-code status (Reading A floor) + optional stdin/stdout-JSON profile (Reading B). | L | T1 |
| **T4** Composition / precedence rule | Specify how imported-pack sections merge with `city.toml`; resolve duplicate-section precedence (spec Reading A: local authoritative). | M | T2 |
| **T5** Conformance suite | Executable checks: Phase-0 minimum loads; a stub subprocess tool node runs and its exit code is read; manifest version-guard rejects incompatible packs. | M | T2, T3, T4 |
| **T6** Reference "hello" pack | A minimal exemplar pack (one `[[tool]]` echo binary + one template) that downstream authors copy. Doubles as T5's fixture. | S | T2, T3 |
| **T7** No-fork invariant doc + license note | Record the boundary beyond which a fork is required (new Provider / modified reconciler / urgent bug fix); confirm `internal/` non-issue (README:288/334). | S | — |
| **T8** Reconcile discipline keys with C43/C57 | Agree exact names/shapes for production-scissors (F44), derivation (F35), RSI (F43) so manifest + governance packs match. | S | T2, C43/C57 specs |

## 2. Dependency graph

```
C01 (gc binary, verified — G11) ──► T1 ──► T2 ──► T4 ──► T5 ──► T6
                                       └──► T3 ──┘        ▲
                                                          │
                          T7 (parallel, no deps)          │
                          T8 (needs T2 + C43/C57) ────────┘
```

- **Critical path:** `C01 verified → T1 → T3 (tool-node ABI) → T5 conformance`. T3 is the longest pole and
  the load-bearing seam (G29); everything downstream that uses a tool node is blocked on it.
- **Upstream gate:** all of C02 is gated on **C01 being obtainable and behaving as described (G11)** — the
  pack-loader and tool-bead executor are C01's, so the ABI cannot be verified until `gc` runs.
- **Downstream gated by C02:** C17 (tool-node abstraction) and every "your work" pack
  (C10/C14/C15/C16/C24/C30–C33/C35/C36–C39/C44/C46–C50).

## 3. Parallelization

Independent workstreams once T1 lands:
- **Stream A (manifest):** T2 → T4 → T8. Owns `pack.toml` + composition.
- **Stream B (ABI):** T3. Owns the subprocess wire contract — the riskiest, give it the strongest author.
- **Stream C (no-fork/license):** T7, fully independent (pure documentation of an existing decision).
Streams A and B converge at **T5 (conformance)** and **T6 (reference pack)**. T8 joins once C43/C57 specs
exist (Batch 4), so it is the natural trailing task.

## 4. Interfaces-first / contract milestones

Freeze in this order so dependents can build against stubs:
1. **`pack.toml` schema (T2)** — unblocks every pack author to start a manifest.
2. **`[[tool]]` declaration + substitution rules (T3, Reading-A floor)** — unblocks C17 and any tool-node
   pack to write a node against a stable arg/exit-code contract *before* the optional JSON profile lands.
3. **Reference "hello" pack (T6)** — the copyable exemplar that turns the frozen contracts into a template.
The optional **JSON tool-node profile (Reading B)** is a *non-breaking superset* — publish it after the
floor so it never blocks the floor's consumers.

## 5. Risks & de-risking order

| Order | Risk | Spike to retire it |
|---|---|---|
| 1 | **G11 — Gas City may not exist / behave as described.** All of C02 rests on `gc`'s real pack-loader + tool-bead executor. | Install `gc`, run the §13.1 Phase-0 minimum, and execute the §13.3 `[[tool]]` subprocess sketch. This single spike validates T1+T3's floor. |
| 2 | **G29 — tool-node I/O channel undocumented.** Reading A vs B picked on inference; wrong guess breaks ~25 packs. | From the same `gc` run, observe what a subprocess node actually receives (args? env? stdin?) and returns (files? stdout? exit code?). Lock T3 to observed behavior, not inference. |
| 3 | **Pack-schema breakage (§3.5, 1–2/quarter).** | Prove the `schema_version` guard (T5) rejects an incompatible manifest, so quarterly churn fails loud. |
| 4 | **Discipline-key drift with C43/C57.** | Defer (T8) but reserve the keys now (T2) so later reconciliation is renaming, not redesign. |

## 6. Definition of done

**Per-component DoD** (ties to spec §8 acceptance criteria):
- The Phase-0 minimum (`[imports.core]` + §13.1 `city.toml` + one template) boots a one-agent city with
  **no custom Go and no fork** (AC-1).
- A subprocess `[[tool]]` node runs end-to-end with `{placeholder}` substitution and its exit code is read
  as status (AC-2), verified by the conformance suite (T5) against the reference pack (T6).
- The **no-fork invariant** is documented and shown to hold across Phases 0–3 (AC-3); the `internal/`
  import block is confirmed irrelevant.
- Manifest declarations (`[[tool]]`/hook/template/formula) compose with `city.toml` under the local-
  authoritative precedence rule (AC-4).
- Discipline keys (F44/F35/F43) parse and are readable by governance checks (AC-5).
- `schema_version` mismatch is rejected, not mis-loaded (AC-6).

**Per-task DoD:** each task closes when its artifact (schema / wire-contract / rule / suite / pack / doc) is
written, cross-referenced to the spec section it realizes, and — for T2/T3/T4 — backed by a passing T5
conformance check. The spec's five open questions (§9) are either resolved by the G11/G29 spike or
explicitly carried to sweep-2 in `_meta/review-log.md`.
