# C01 — Gas City Runtime Substrate  (Build Plan, Track A)

> Source / Spec ref: spec-faithful/C01-gas-city-substrate.md
> Sources cited in spec: README §Part 4, §Part 6 (Phase 0/1); AI-CONTEXT §2, §3.1–§3.6, §11, §13.1–§13.2, §14; inventory C01 row; gaps G11, G03.

## 1. Work breakdown

C01 is *adoption + verification*, not authorship — Phase 0 is "no custom code" (README line 355). The
work is: pin the dependency, stand up the minimum install, **prove the Native claims**, and freeze the
substrate seams downstream components build against.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Source & pin `gc` | Obtain `gc` from `github.com/gastownhall/gascity`; select a version satisfying all Phase-0/1 Native claims given two in-flight migrations (AI-CONTEXT §3.5); record commit+version pin (INV-1). **Retires G11.** | M | — |
| **T2** Phase-0 install | Author `pack.toml` (`[imports.core]`), `city.toml` (workspace + one `claude` agent + `[beads] provider="file"`), one `agents/worker/prompt.template.md` (AI-CONTEXT §13.1). | S | T1 |
| **T3** Boot single worker | Run one Claude Code session via the substrate; execute one trivial unit of work end-to-end (AC-1). | S | T2, C04, C28 |
| **T4** Native-conformance pack | A conformance suite (shape transfused from `runtimetest/conformance.go`, AI-CONTEXT §3.6) asserting AC-2 (P1,P2,P4,P9,P10 at Phase 0), AC-3 (pin reproducible), AC-4 (no-fork), AC-5 (feature-gating), AC-6 (attribution). **The G11/G03 de-risking gate.** | L | T3 |
| **T5** Freeze substrate seams | Enumerate + freeze the `gc` CLI surface (`gc bd`, `gc formula export`, `gc converge resume`, …) and the I1–I8 seam descriptions so C02/C04/C05/C12/C18/C19/C23 build against stubs. | M | T2 |
| **T6** Phase-1 turn-on (additive) | Add `[formulas]` + `[[service]]` blocks (langfuse/cxdb/otel) + agent `env` telemetry vars (AI-CONTEXT §13.2); re-run conformance to assert P3 now delivered (=6 native) and Phase-0 behaviour unchanged. | M | T4; C12, C21, C25 ready |

## 2. Dependency graph

- **Upstream of C01:** none in v4 — it is the dependency root (Batch 1, inventory line 107). Its *spec*
  references C03 (config semantics) and C04 (session model), but C01's **install** can proceed before
  those specs finalize because the Phase-0 config is fixed verbatim by AI-CONTEXT §13.1.
- **Critical path:** **T1 → T2 → T3 → T4** is the gating chain. Until T4 passes, every "Native" cell is
  provisional (G11), so T4 blocks *all* Batch-2 work that assumes the substrate. **T1 (sourcing/pinning)
  is the single highest-risk task in the entire program** — if `gc` is unobtainable or non-conformant,
  "the whole plan reorganizes" (README §11).
- **Downstream gated by T5 (seam freeze):** C02, C04, C05, C12, C13, C17, C18, C19/C20, C23, C41 build
  against the frozen seams.
- **T6** is on the Phase-1 critical path, not Phase-0; it can defer until C12/C21/C25 are ready.

## 3. Parallelization

C01 is small and mostly serial through the critical chain, but some fan-out exists:
- **After T2:** T5 (seam-freeze documentation) can run **concurrently** with T3/T4 — describing the CLI
  surface and seams does not require the conformance run to pass.
- **Within T4:** the six AC checks (AC-1…AC-6) are independent assertions and can be authored in parallel
  by separate workstreams once T3 boots the worker.
- **T6 sub-parts** (`[formulas]` enablement vs each `[[service]]` block) are independent and parallelizable
  once their respective external services exist.
- **Cross-component:** C03 and C04 specs proceed in parallel with C01's T1–T4 (they describe semantics of
  config/sessions C01 merely hosts).

## 4. Interfaces-first / contract milestones

Freeze early (T5) so dependents build against stubs:
- **M1 — Version pin published (after T1):** the exact `gc` version/commit, so every downstream spec
  pins the same substrate.
- **M2 — `gc` CLI surface frozen (T5):** enumerated subcommands/flags v4 relies on (I1) → unblocks C05,
  C12, C18.
- **M3 — Seam descriptions frozen (T5):** I3 (pack/tool-node ABI handoff → C02), I4 (provider/session →
  C04), I6 (bead API → C19/C20), I7 (event bus → C23), I8 (reconciler tick → C18).
- **M4 — Phase-0 config canonized (T2):** the ~30-line install is the stub all Batch-1 components assume.

## 5. Risks & de-risking order

Retire in this order (highest uncertainty first):
1. **G11 — does Gas City exist and work as claimed? (blocker).** Spike T1+T3+T4 *before anything else*:
   obtain `gc`, boot it, run the conformance pack. This is the program's top de-risking action; a failure
   here invalidates the architecture's foundation. → OQ-1 in spec, top of review-log.
2. **Migration tail (AI-CONTEXT §3.5/§14).** 1–2 breaking changes/quarter; mitigate by pinning (T1) and
   making T4 a regression gate on version bumps.
3. **G03 — native count.** Low-effort: T4 explicitly asserts 5-native at Phase 0 / 6 from Phase 1, removing
   the double-count locally; defer the corpus-wide headline reconciliation to C57.
4. **No-fork drift (INV-2).** AC-4 build-graph check prevents accidental `internal/`/`pkg/` imports.

## 6. Definition of done

**Per-component DoD (sweep-1 altitude):**
- A pinned `gc` version is recorded and the Phase-0 install (`pack.toml` + `city.toml` + one template)
  boots a single Claude Code worker with file beads and **no custom code** (AC-1).
- The Native-conformance pack passes AC-2…AC-6 against the pinned `gc`: P1,P2,P4,P9,P10 delivered at
  Phase 0; P3 delivered after Phase-1 `[formulas]` turn-on; attribution end-to-end; feature-gating by
  section-presence; no-fork invariant; reproducible install. (**Resolves G11 operationally; resolves G03
  locally.**)
- The substrate seams (I1–I8) and the relied-on `gc` CLI surface are frozen and published so C02/C04/C05/
  C12/C18/C19/C23/C41 can build against stubs (M1–M4).

**Per-task DoD:** each Tn meets its mapped acceptance criterion (T2→AC-1/AC-5, T1→AC-3, T4→AC-2/4/5/6,
T6→P3-delivered + Phase-0-unchanged) and updates the spec's Open Questions / review-log as items close.
