# C01 — Gas City Runtime Substrate  (Build Plan, canonical track)

> Source / Spec ref: spec/C01-gas-city-substrate.md (sweep-2)
> Sources cited in spec: README §Part 4, §Part 6 (Phase 0/1); AI-CONTEXT §2, §3.1–§3.6, §11, §13.1–§13.2, §14; inventory C01 row; gaps G11, G03; D-23 substrate harvest (F1–F12, `lago-morph/gascity-prototype@b14c278`); D-30 prevent-gate; `architectures/v4/_meta/gascity-conformance-check.md`.

## 1. Work breakdown (sweep-2 — concrete tasks)

C01 is *adoption + verification*, not authorship — Phase 0 is "no custom code" (README line 355). The
work is: pin the dependency, stand up the minimum install, **run the conformance check**, and freeze the
substrate seams downstream components build against.

| Task | Description | Size | Prereqs | AC-codes it closes |
|---|---|---|---|---|
| **T1** Source & pin `gc` | Obtain `gc` from `lago-morph/gascity-prototype@b14c278`; confirm Go 1.26.3 via `head -5 go.mod` (go.mod is authoritative — config anchor §1); record the pin in `architectures/v4/_meta/gascity-config-anchor.md` §1. Pre-stage `gc`, `bd`, `dolt`, `node`, `claude` binaries on the host (PLAN items 1–2; sandbox TLS-inspection proxy blocks in-container downloads — F12). **Retires the "pin unknown" half of G11.** | M | Docker host available | AC-C01-3 |
| **T2** Phase-0 install | Author `pack.toml` (`[pack] name`, `schema = 2`, `[imports.core]`), `city.toml` (workspace + one `claude` agent + `[beads] provider="bd"`), and the entrypoint-written `.gc/site.toml` (`[[rig]] name + path`). Set `IS_SANDBOX=1` in `.env`. Pre-populate `~/.claude.json` with the three onboarding pre-acks (PLAN items 7–8). | S | T1 | AC-C01-1, AC-C01-5, AC-C01-7 |
| **T3** Boot single worker | Run `gc start --foreground` (under `tini` in container). Verify `gc status` shows controller running and worker pane in `gc session list`. Execute the minimal stand-up smoke signal: `bd create "conformance-smoke-signal"` from `/workspace/rigs/rig1`. | S | T2, C04 (tmux provider — F7), C28 | AC-C01-1 |
| **T4** Run Gas City conformance check | Execute the full battery at `architectures/v4/_meta/gascity-conformance-check.md` (Tests A–G). **This is the G11 de-risking gate.** Prioritize: Test A (prevent-vs-detect, KEYSTONE → routes D-30), then C (Orders durability → C40 design), then B (twin semantics → C44 design). Record all outcomes in the Results Record table in the conformance-check doc. **No Batch-2 component starts until all tests PASS or outcomes are recorded and consequences are actioned.** | L | T3 | AC-C01-2, AC-C01-6, AC-C01-8 |
| **T5** Freeze substrate seams | Enumerate + freeze the `gc` CLI surface (spec §3.2 table) and the I1–I8 seam descriptions so C02/C04/C05/C12/C18/C19/C23 build against stubs. Publish milestones M1–M4 (see §4). Any `[needs-pinned-gc-run (G11)]` items in spec §3.2 that T4 resolves should be updated in §3.2. | M | T2 (can start concurrently with T3/T4 for docs; finalize after T4) | — |
| **T6** D-30 outcome action | If conformance check Test A = DETECT-ONLY or SILENT: design the D-30 enforcement watcher (blocked on T4 outcome; do NOT design before T4 runs — D-23 decision). If Test A = PREVENT: annotate C34/C43 specs that the bead layer is a real control. Either way, update `auto-001` brief and affected component specs. | M | T4 (gated: ONLY start after Test A outcome is recorded) | AC-C01-8 |
| **T7** Phase-1 turn-on (additive) | Add `[formulas]` + `[[service]]` blocks (langfuse/cxdb/otel) + agent `env` telemetry vars (AI-CONTEXT §13.2). Re-run conformance check AC-C01-5 to assert P3 now delivered (=6 native) and Phase-0 behaviour unchanged. | M | T4; C12, C21, C25 ready | AC-C01-5 (Phase-1 sub-criterion) |
| **T8** No-fork audit | Scan v4 artifact tree for any `github.com/gastownhall/gascity/internal/*` or `.../pkg/*` import paths. Automated check; fails loudly if found. | S | T2 | AC-C01-4 |

## 2. Dependency graph

- **Upstream of C01:** none in v4 — it is the dependency root (Batch 1, inventory line 107). Its *spec*
  references C03 (config semantics) and C04 (session model), but C01's **install** can proceed before
  those specs finalize because the Phase-0 config is fixed verbatim by AI-CONTEXT §13.1.
- **Cycle resolution:** C01↔C03 and C01↔C04 are inventory cycles broken by treating **C01 as root**.
  C01's T1/T2 install proceeds independently; C03/C04 build against the C01 seam contract (M3/M4), not
  the reverse.
- **Critical path:** **T1 → T2 → T3 → T4** is the gating chain. Until T4 passes, every "Native" cell is
  provisional (G11), so T4 blocks *all* Batch-2 work that assumes the substrate. **T1 (sourcing/pinning)
  is the single highest-risk task in the entire program** — if `gc` is unobtainable or non-conformant,
  "the whole plan reorganizes" (README §11). T4 Test A outcome also gates T6 (D-30 action), which affects
  C34/C43 designs.
- **T6 is HARD-GATED on T4 Test A.** Do not begin watcher design until Test A runs (D-23 decision: "don't
  design what we may not need").
- **Downstream gated by T5 (seam freeze):** C02, C04, C05, C12, C13, C17, C18, C19/C20, C23, C41 build
  against the frozen seams.
- **T7** is on the Phase-1 critical path, not Phase-0; it can defer until C12/C21/C25 are ready.

## 3. Parallelization

C01 is small and mostly serial through the critical chain, but some fan-out exists:
- **After T2:** T5 (seam-freeze documentation) and T8 (no-fork audit) can run **concurrently** with T3/T4
  — describing the CLI surface does not require the conformance run to pass; the no-fork audit is a static
  code scan.
- **Within T4:** the seven conformance tests (A through G) are logically independent assertions and may be
  run as parallel workstreams once the minimal stand-up passes. However, **Test A should be prioritized**
  (its outcome gates T6 and shapes C34/C43). Tests B and C should be next (gate C44 and C40 respectively).
- **T6 sub-parts:** if Test A = DETECT-ONLY, the watcher design and the C34/C43 annotation updates are
  independent of each other and can proceed in parallel.
- **T7 sub-parts** (`[formulas]` enablement vs each `[[service]]` block) are independent and parallelizable
  once their respective external services exist.
- **Cross-component:** C03 and C04 specs proceed in parallel with C01's T1–T4 (they describe semantics of
  config/sessions C01 merely hosts).

## 4. Interfaces-first / contract milestones

Freeze early (T5) so dependents build against stubs:
- **M1 — Version pin published (after T1):** the exact `gc` commit (`b14c278`), upstream SDK commit
  (`183897e`), and Go version (1.26.3) — so every downstream spec pins the same substrate.
- **M2 — `gc` CLI surface frozen (T5):** the spec §3.2 table of relied-on subcommands/flags. Exact flag
  syntax confirmed from T4 live run. Unblocks C05, C12, C18.
- **M3 — Seam descriptions frozen (T5):** I3 (pack/tool-node ABI handoff → C02), I4 (provider/session →
  C04), I6 (bead API → C19/C20), I7 (event bus → C23), I8 (reconciler tick → C18).
- **M4 — Phase-0 config canonized (T2):** the ~30-line install is the stub all Batch-1 components assume.
- **M5 — Test A outcome recorded (T4):** the prevent-vs-detect verdict is written into the conformance-check
  Results Record and propagated to C34/C43/D-30. This milestone gates T6 and the P2-readiness decision.

## 5. Risks & de-risking order

Retire in this order (highest uncertainty first):
1. **G11 — does Gas City exist and work as claimed? (blocker).** Spike T1+T3+T4 *before anything else*:
   obtain `gc` at `b14c278`, boot it, run the conformance check. This is the program's top de-risking
   action; a failure here invalidates the architecture's foundation. → OQ-1 in spec; the conformance check
   procedure (`gascity-conformance-check.md`) is the operationalized form.
2. **D-30 prevent-gate (Test A KEYSTONE).** The highest-consequence single test result in the program:
   PREVENT → proceed; DETECT-ONLY / SILENT → watcher must be built before P2. Run as early in T4 as
   possible, and action T6 immediately after.
3. **Migration tail (AI-CONTEXT §3.5/§14).** 1–2 breaking changes/quarter; mitigate by pinning (T1) and
   making T4 a regression gate on version bumps. (E-C01-08)
4. **G03 — native count.** Low-effort: T4 explicitly asserts 5-native at Phase 0 / 6 from Phase 1 via
   AC-C01-5, removing the double-count locally; defer the corpus-wide headline reconciliation to C57.
5. **No-fork drift (INV-2).** T8 static build-graph check prevents accidental `internal/`/`pkg/` imports.
6. **Config-key misplacement (E-C01-06).** PackV2 refuses startup on misplaced keys (F1, F3); AC-C01-7
   explicitly tests the rejection. Author config from the §3.3 table, not from memory.

## 6. E-code → AC-code cross-reference

| E-code | AC-codes that exercise it |
|---|---|
| E-C01-01 (binary unavailable) | AC-C01-1 |
| E-C01-02 (Go version mismatch) | AC-C01-3 |
| E-C01-03 (wrong commit) | AC-C01-3 |
| E-C01-04 (IS_SANDBOX=1 missing) | AC-C01-1 |
| E-C01-05 (claude.json not pre-acked) | AC-C01-1 |
| E-C01-06 (misplaced config key) | AC-C01-5, AC-C01-7 |
| E-C01-07 (conformance check failure) | AC-C01-2, AC-C01-6, AC-C01-8 |
| E-C01-08 (version-pin drift) | AC-C01-3 |
| E-C01-09 (prevent-vs-detect unknown) | AC-C01-8 |
| E-C01-10 (DOLT_REF mismatch) | AC-C01-2 (Test C sub-criterion) |

## 7. Definition of done

**Per-component DoD (sweep-2):**
- A pinned `gc` version (`b14c278`) is recorded; pre-staged binaries on host; the Phase-0 install
  (`pack.toml` + `city.toml` + `.gc/site.toml` entrypoint-written + one template) boots a single Claude
  Code worker with Dolt-backed beads and **no custom code** (AC-C01-1).
- The Gas City conformance check (`gascity-conformance-check.md` Tests A–G) passes: all outcomes recorded
  in the Results Record (AC-C01-2). **Resolves G11 operationally** (the empirical end-to-end gate).
- **Test A outcome actioned** (M5): either D-30 watcher confirmed not needed (PREVENT path) or watcher
  design in progress and P2 blocked until it lands (DETECT-ONLY/SILENT path).
- The no-fork audit (T8) passes: zero `internal/`/`pkg/` Gas City imports (AC-C01-4).
- Phase-0 feature-gating confirmed: `[formulas]` and other optional sections are OFF at Phase-0 config;
  adding `[formulas]` and restarting enables DAG composition without altering Phase-0 behavior (AC-C01-5).
- Attribution end-to-end confirmed: a dispatched work unit produces beads and events with non-null
  `created_by` (AC-C01-6 / conformance check Test E).
- The substrate seams (I1–I8) and the relied-on `gc` CLI surface (§3.2) are frozen and published at
  milestones M1–M5 so C02/C04/C05/C12/C18/C19/C23/C41 can build against stubs.

**Per-task DoD:** each Tn meets its mapped acceptance criterion (T2→AC-C01-1/5/7, T1→AC-C01-3,
T4→AC-C01-2/6/8, T6→D-30 actioned, T7→P3-delivered + Phase-0-unchanged, T8→AC-C01-4) and updates
the spec's Open Questions / conformance-check Results Record / review-log as items close.

## 8. Post-conformance: seam-freeze propagation checklist

After T4 completes and M1–M5 are published, each dependent component must be updated:

| Component | What changes when T4 resolves |
|---|---|
| C34 (holdout integrity) | Test A outcome annotates whether bead layer is PREVENT or DETECT; if DETECT → watcher dependency added |
| C43 (isolation boundary) | Test A outcome: fence is real control (PREVENT) or advisory + watcher needed (DETECT) |
| C40 (Orders durability) | Tests C1/C2/C3 outcomes annotate crash-resume granularity and container-death durability |
| C44 (digital twin) | Test B outcome: `[[service]]` schema confirmed → OQ-4 fields bound; or `[[service]]` not in `gc` → OQ-4 must be re-authored |
| C18 (reconciler) | Test G outcome annotates reconciler convergence as operational or disputed |
| C41 (identity) | Test E outcome annotates `created_by` as bead-schema field (PASS) or unverified (FAIL) |
| C42 (rig partitioning) | Tests D, F outcomes annotate dispatch partition assignment and prefix config as operational or disputed |
| C05 (sling dispatch) | M2 seam freeze confirms `gc sling` subcommand signature for dispatch-policy build |
| C12 (formula format) | M2 seam freeze confirms `gc formula export --format dot` signature; any flag deviation updated in §3.2 |
