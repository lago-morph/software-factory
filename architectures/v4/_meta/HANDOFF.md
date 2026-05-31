# HANDOFF — v4 Spec & Plan run (resume from here)

**Last updated:** 2026-05-31 (Sweep-1 complete).
**Status:** **Sweep-1 is COMPLETE — all 57 components built + adversary-reviewed + integrated** on the single canonical `spec/` + `plan-faithful/` track. Next work is **Sweep 2 (implementation-ready depth)**.
**Working tree:** clean and pushed. The Sweep-1 build is PR #220 on `claude/epic-fermat-LTO4V`.

This file + the other `_meta/` artifacts are sufficient to resume with zero re-grounding. Start with the run summary at [`run-summary.md`](../../../run-summary.md) and the coverage ledger [`STATUS.md`](./STATUS.md).

---

## 1. Where we are: 57 of 57 components built — one canonical track

**One canonical track** — `spec/` + `plan-faithful/`. `spec-optimized/` + `plan-optimized/` are frozen reference. Every component (C01–C57) has `spec/<ID>-<slug>.md` + `plan-faithful/<ID>-<slug>.md` + `spec/<ID>-<slug>.review.md` (**57 / 57 / 57**). All adversary verdicts across the run were **accept-with-fixes** (0 blockers, 0 needs-rework). The live per-component four-axis state (Built / Reviewed / Incorporated / iNtegrated) is in [`STATUS.md`](./STATUS.md) — all 57 are ✓ on all four.

Sweep-1 was produced in batches (build → adversary-review → integrator), each batch's cross-component findings recorded as ledger decisions: **D-1..D-5** (Batch 1 / Integration-Pass-1), **D-6..D-14** (Batch 2), **D-15..D-17** (Batch 3), **D-18..D-19 + XC-3 resolved** (Batch 4), OQ-harvest only (Batch 5). Detail in [`review-log.md`](./review-log.md).

## 2. The bar (operator's — still in force for every sweep)

> *"Does this addition give us MORE CAPABILITY tied to a specific 12-principle? Polish/hardening that does the same thing 'better' in a non-principle way → DROP. Genuine, low-effort custom code where some part of a principle could not be met without it → KEEP. Partial satisfaction by the existing software stack (Gas City + libraries like prometheus / scikit-learn / PyOD / opentelemetry / sigstore / Inspect AI / DSPy / LocalStack / etc.) counts — we don't add custom code to harden what the stack already does."*

When in doubt: DROP. Grounding + worked examples in [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md). This bar held across all 57 — Sweep 2/3 must keep applying it (don't let implementation-depth reintroduce dropped hardening).

## 3. Passes still owed (next runs)

1. **Whole-57 cross-batch integration pass** — integration was done per-batch; a final drift pass over all 57 (esp. seams frozen "→ Sweep-2 joint freeze": C12/C14/C15 loop-DOT encoding D-16; C42/C34/C32 judge read-surface D-17; C36↔C37 population seam; C38↔C39 / C48↔C55 / C46 dep-edge OQ-6).
2. **Sweep 2 (implementation-ready):** concrete signatures, data schemas, API/message contracts, sequence/state diagrams (Mermaid), error taxonomies, concrete acceptance tests — re-enter every component. This is the next work.
3. **Sweep 3 (exhaustive):** pseudocode/algorithms, skeletons, edge-case catalogs, perf/security/ops.
4. **Final cross-cutting pass:** whole-system consistency, critical-path/parallelism analysis, top-level README/index.

## 4. How to resume (Sweep 2)

1. Read [`run-summary.md`](../../../run-summary.md) (what the run did + morning-review items), this file, then [`STATUS.md`](./STATUS.md) (coverage ledger) and [`review-log.md`](./review-log.md) (D-1..D-19 + ~196 harvested OQs — the OQs are the Sweep-2 work list). Do **NOT** read the four v4 source docs into primary context — subagents do that.
2. Resolve the **morning-review items first** (run-summary §"Morning-review"): D-18 (C43 split-sequencing), OQ-C57-3 (F54 ownership), OQ-6 (C46 dep edge) — these shape Sweep-2 dependencies.
3. Use the standing briefs [`BUILDER-BRIEF.md`](./BUILDER-BRIEF.md) + [`ADVERSARY-BRIEF.md`](./ADVERSARY-BRIEF.md) (single-track banners). Dispatch one builder per component at **Sweep 2** depth; concurrency cap ~8; pipeline; subagents persist to disk + return receipts; **primary owns all git**; commit+push every wave.
4. Each component's `spec/<ID>-*.md` already carries its Sweep-1 OQs inline + its `.review.md` — Sweep 2 starts from those, not a blank page.

## 5. Binding decisions (do not relitigate) — detail in [`review-log.md`](./review-log.md)

D-1 same-provider judge (cross-family→FE-1) · D-2 bundle-id namespace `softwarefactory.v4.{beads,trajectory,packs}` · D-3 C20 authors bead schemas / C22 mechanism · D-4 C20→C19 · D-5 C41 hash-chain over C23 · D-6 "canonical track" nomenclature · D-7 node-kind home=C12 · D-8 convoy→C05 / Order→C40 · D-9 F38 vocab-lint=C10 · D-10 modeldb=`{id,family,cost_tier}` · D-11 LangFuse traces-only seam · D-12 two-sink cross-refs · D-13 holdout C34(enforce+audit)/C43(lethal-trifecta) · D-14 G37(secrets)≠FE-3(signing) · D-15 satisfaction holistic (FE-5 deferred) · D-16 loop-DOT encoding=C12 · D-17 judge read-surface · **D-18 (PROVISIONAL — operator confirm)** C43 split-sequencing · **D-19** methodology significance→C48 · **XC-3 RESOLVED** C39 owns G18 numeric policy.

## 6. Deferred capabilities (do not build) — detail in [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md)

FE-1 cross-provider judge · FE-2 portability contracts · FE-3 graduated-mandatory signing (needs G37) · FE-4 multi-seat pool · FE-5 enumerated per-criterion DoD — **resolved by D-15** (holistic satisfaction; revisit only when C46 needs per-criterion diagnosis). Each has a specific external trigger; none pending.

## 7. Key residual risks (carried into Sweep 2 + the C57 register)

- **G11** — every "Native" Gas City claim is still unverified against a real `gc`; Sweep 2 MUST freeze real `gc` schemas (formula/molecule/bead/Order/reconciler) before dependents bind. Touches C01/C12/C13/C14/C18/C40 + the prevent-vs-detect OQ (C43/C34).
- **G18** — **CLOSED in design:** C39 owns the numeric termination policy (N→escalate, F52 oscillation, L5 ship-auth) over C20 slots; C18 owns the loop. (XC-3 resolved.)
- **G31** — lethal-trifecta has a deterministic boundary-typing **design** (C43) but the bound is aspirational until C44 twins land (the XC-8 P0–P3b exposure window); see D-18 (C43 pull-forward, operator-confirm).
- **G19** — counterfactual replay (C49) is **framed honestly, not solved**: deterministic-slice replay is tractable now; full LLM-step counterfactual is deferred (best-effort + human-reviewed). v4's riskiest leaf.
- **F54** — objective-drift audit registered UNBUILT (C57 / OQ-C57-3) — loudest residual after G31 on a self-modifying L5 factory. Operator call.
- **G37** — no secrets store (owned by C03); blocks FE-3 signing; keeps several controls "detect not prevent".

## 8. Artifact map (`architectures/v4/_meta/`)

META-PLAN · TRACK-CHARTERS · DOC-TEMPLATES · BUILDER-BRIEF · ADVERSARY-BRIEF · component-inventory (+ -A/-B raw) · ambiguities-and-gaps · **review-log** (D-1..D-19 + harvested OQs) · INTEGRATION-PASS-1 · SURVIVOR-PASS · FUTURE-ENHANCEMENTS · **RUN-SCOPE-2026-05-31** (this run's scope envelope) · **STATUS** (coverage ledger) · HANDOFF (this). Run summary at repo root: [`run-summary.md`](../../../run-summary.md).

Frozen reference (do not author here): `spec-optimized/` + `plan-optimized/`.
