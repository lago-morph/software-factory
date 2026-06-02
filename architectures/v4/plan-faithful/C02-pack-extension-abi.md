# C02 — Pack & Tool-Node ABI  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C02-pack-extension-abi.md`](../spec/C02-pack-extension-abi.md)

C02 is an **interface/contract** component (no runtime engine of its own — that is C01). "Building" C02
means **specifying and freezing the two contracts** (pack bundle + tool-node ABI), then **conformance-
verifying** them against the real `gc` binary so the ~25 downstream packs can be authored against stable
shapes. The plan is therefore contract-first and verification-heavy, not code-heavy.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Pin pack-bundle layout | Freeze the on-disk pack tree: `pack.toml`, `agents/<name>/prompt.template.md`, tool-node binaries, formulas, `.claude/skills/`. Already specified in spec §4.2. | S | C01 install (G11) |
| **T2** Freeze `pack.toml` manifest schema | Concrete field-table for `[pack]`, `[imports.*]`, `[[tool]]`, `[[hook]]`, `[pack.safety]`, `[pack.derivation]`, `schema_version`. Specified at spec §4.1. | M | T1 |
| **T3** Freeze tool-node ABI (the G29 seam) | Concrete wire contract: Reading-A floor (args + files + exit code; spec §3.2.1), optional Reading-B profile (structured stdin/stdout JSON; spec §3.2.2), env-var set `[needs G11]`, placeholder substitution grammar `[needs G11]`. Already frozen at floor level; residual is the G11 spike. | L | T1 |
| **T3b** G11 spike: observe real `gc` tool-node invocation | Run the prototype's `[[tool]]` subprocess against the pinned `gc` binary; capture argv, env vars passed, stdin connectivity, working-dir path form, stdout handling. Resolves the `[needs G11 verification]` items in §3.2.1. | M | G11 Docker spike |
| **T4** Composition / precedence rule | Specify how imported-pack sections merge with `city.toml`; resolve duplicate-section precedence (spec Reading A: local authoritative). Sweep-2 needs `gc` confirmation (G11 / OQ-2). | M | T2 |
| **T5** Conformance suite | Executable checks: Phase-0 minimum loads (AC-C02-01); schema mismatch rejected (AC-C02-02); subprocess invoked with substituted args (AC-C02-03); non-zero exit surfaced (AC-C02-04); duplicate import rejected (AC-C02-05); import-placement rule (AC-C02-06); namespace check (AC-C02-07); declaration-discipline keys parse (AC-C02-08). See spec §8.1. | M | T2, T3, T4 |
| **T5b** Reading-B conformance | Conformance checks for JSON profile: AC-C02-09 (JSON round-trip), AC-C02-10 (malformed JSON → failure). | S | T3, T5 |
| **T6** Reference "hello" pack | Minimal exemplar pack: one `[[tool]]` echo binary + one prompt template + one `[[hook]]` PreToolUse + `.claude/skills/hello.md`. Doubles as T5 fixture. Satisfies no-fork invariant (AC-C02-01). | S | T2, T3 |
| **T7** No-fork invariant doc + license note | Record the boundary beyond which a fork is required; confirm `internal/` non-issue (README:288/334). | S | — |
| **T8** Reconcile discipline keys with C43/C57 | Agree exact names/shapes for `[pack.safety] production_scissors` (F44), `rsi` (F43), `[pack.derivation] from` (F35) so manifest + governance packs match. | S | T2, C43/C57 specs |
| **T9** Claude Code extension registration contract | Confirm `[[hook]]` field shape, MCP `[[service]] protocol = "mcp"` field, and `.claude/skills/` auto-registration against pinned `gc` and Claude Code docs (spec §3.3; OQ-6/C28:OQ-4). Requires G11 spike. | M | T3b, C28 spec |
| **T10** XC-7 ruling response | Once orchestrator rules on CapabilityDescriptor ownership (XC-7), apply the result: either carry a `capability_id` ref field in §4.1 (if C03 owns the registry) or no action. | S | Orchestrator ledger ruling |

## 2. Dependency graph

```
C01 (gc binary, G11 spike needed) ──► T1 ──► T2 ──► T4 ──► T5 ──► T6
                                        └──► T3 ──┤        ▲
                                                   └──► T5b ┘
                     T3b (G11 spike) ────────────────► T3 (residual fills)
                                     └───────────────► T9 (ext. registration)
                     T7 (parallel, no deps)
                     T8 (needs T2 + C43/C57) ─────────► T5 (discipline-key ACs)
                     T10 (awaits orchestrator ruling)
```

- **Critical path:** `C01 verified (T3b G11 spike) → T3 (ABI wire bytes frozen) → T5 conformance`. T3
  floor is already frozen (Reading A); T3b fills the `[needs G11]` wire details.
- **Upstream gate:** all wire-level claims rest on **C01 (gc) being obtainable and behaving as described**
  (G11). The Reading-A floor can be partially tested with a stub; the complete contract requires T3b.
- **Downstream gated by C02:** C17 (tool-node abstraction) and every "your work" pack.

## 3. Parallelization

Independent workstreams once T1 lands:
- **Stream A (manifest):** T2 → T4 → T8. Owns `pack.toml` schema + composition.
- **Stream B (ABI floor):** T3. Owns the subprocess wire contract floor — already frozen at Reading A.
- **Stream B2 (ABI spike):** T3b. Owns the G11 validation run — the riskiest, needs Docker.
- **Stream C (no-fork/license):** T7, fully independent.
- **Stream D (extension surfaces):** T9, depends on T3b + C28 spec.

Streams A, B, B2 converge at **T5 (conformance)** and **T6 (reference pack)**. T8 and T10 join last.

## 4. Interfaces-first / contract milestones

Freeze in this order so dependents can build against stubs:
1. **`pack.toml` schema (T2)** — unblocks every pack author to start a manifest. Now done at spec §4.1.
2. **Reading-A floor (T3, already frozen)** — unblocks C17 and any tool-node pack to write a node against
   the args/exit-code contract *before* G11 verification lands.
3. **Reference "hello" pack (T6)** — the copyable exemplar that turns the frozen contracts into a template.
4. **G11 spike result (T3b)** — fills in the `[needs G11 verification]` wire-byte details (env vars,
   stdin, substitution grammar) so downstream packs can rely on precise behavior.
5. **Optional Reading-B profile (T5b)** — non-breaking superset; publish after the floor so it never
   blocks the floor's consumers.

## 5. Risks & de-risking order

| Order | Risk | Spike to retire it |
|---|---|---|
| 1 | **G11 — Gas City may not exist / behave as described.** All of C02 rests on `gc`'s real pack-loader + tool-bead executor. | T3b: install `gc`, run the §13.1 Phase-0 minimum, execute the §13.3 `[[tool]]` subprocess sketch. This single spike validates T1+T3's floor and resolves OQ-1's residual G11 items. |
| 2 | **G29 residual — env-var set, stdin, placeholder grammar.** Reading A is frozen; the wire bytes are inferred. | T3b: observe what a subprocess node actually receives. Lock §3.2.1 to observed behavior. |
| 3 | **OQ-6 / C28:OQ-4 — extension-surface registration field shapes.** `[[hook]]`, MCP `[[service]] protocol`, `.claude/skills/` auto-registration are all `[inferred — needs G11]`. | T9: confirm against pinned `gc` run and Claude Code pack documentation. |
| 4 | **Pack-schema breakage (§3.5, 1–2/quarter).** | T5: prove schema mismatch (AC-C02-02) is rejected, so quarterly churn fails loud. |
| 5 | **Discipline-key drift with C43/C57.** | Defer (T8) but reserve the keys now (T2) so later reconciliation is renaming, not redesign. |
| 6 | **XC-7 CapabilityDescriptor ruling.** | T10: await orchestrator; no canonical-track impact until ruled. |

## 6. Definition of done

**Per-component DoD** (ties to spec §8 / §8.1 acceptance criteria):
- The Phase-0 minimum (`[imports.core]` + §13.1 `city.toml` + one template) boots a one-agent city with
  **no custom Go and no fork** (AC-C02-01).
- A subprocess `[[tool]]` node runs end-to-end with `{placeholder}` substitution and its exit code is read
  as status (AC-C02-03/04), verified by the conformance suite (T5) against the reference pack (T6).
- The **no-fork invariant** is documented and shown to hold across Phases 0–3 (AC-C02-01 + T7); the
  `internal/` import block is confirmed irrelevant.
- Manifest declarations (`[[tool]]`/hook/template/formula) compose with `city.toml` under the local-
  authoritative precedence rule (AC-C02-03 + T4).
- Discipline keys (F44/F35/F43) parse and are readable by governance checks (AC-C02-08).
- Schema mismatch is rejected, not mis-loaded (AC-C02-02).
- Transitive-import deduplication is enforced (AC-C02-05), import-placement rule is enforced (AC-C02-06).
- D-2 namespace is enforced by the conformance suite (AC-C02-07).
- E-code taxonomy (§6.1, E-C02-01..08) covers all load/ABI/registration failure paths.

**Per-task DoD:** each task closes when its artifact (schema / wire-contract / rule / suite / pack / doc)
is written, cross-referenced to the spec section it realizes, and — for T2/T3/T4 — backed by a passing T5
conformance check. The spec's OQs (§9) are either resolved by the G11/T3b spike or explicitly carried
with `PARTIAL (needs-G11)` status.

## 7. Sweep-2 depth added summary

| Item | Count / description |
|---|---|
| Signatures / typed params | 8 (tool-node invocation inputs: argv[0], argv[1..N], cwd, env, stdin, stdout, stderr, exit-code) |
| Schema tables (Field/Type/Req/Semantics/R-W-by) | 1 (spec §4.1 pack manifest field table, 16 fields) |
| Diagrams | 1 sequenceDiagram (spec §5.1: host → tool-node subprocess → result) |
| E-codes | 8 (E-C02-01..08, spec §6.1) |
| AC-codes | 10 (AC-C02-01..10, spec §8.1) |
| E↔AC cross-refs | 6 (AC-02, 04, 05, 06, 10 each reference an E-code; AC-07 references D-2 namespace) |
| OQs resolved | OQ-1 (G29 floor — RESOLVED at Reading A; PARTIAL G11 residual named) |
| OQs still open | OQ-2 (precedence), OQ-3 (XC-7 deferred), OQ-4 (discipline keys), OQ-5 (long-lived tool nodes), OQ-6 (C28:OQ-4 extension registration) |
