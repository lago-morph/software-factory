# HANDOFF — v4 Spec & Plan run (resume from here)

**Last updated:** 2026-05-31.
**Status:** Tracks converged to one canonical `spec/`. Apply pass complete (no spec edits needed; faithful already had the keeps in minimal form). 34 components remain unbuilt — that is the next work.
**Working tree:** clean and pushed. PR #218 contains the convergence work.

This file + the other `_meta/` artifacts are sufficient to resume with zero re-grounding.

---

## 1. Where we are: 23 of 57 components built; **one canonical track**

**Track convergence (2026-05-31):** the run used to author both `spec/` (formerly `spec-faithful/`) and `spec-optimized/` in parallel. As of 2026-05-31 there is **one canonical track** — `spec/` + `plan-faithful/`. `spec-optimized/` and `plan-optimized/` are frozen reference (per-directory READMEs explain). The four architectural bets in the optimized track are parked as FE-1..FE-4 in [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md); rationale in [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md).

**DONE (23) on the canonical track** — each has `spec/<ID>-<slug>.md` + `plan-faithful/<ID>-<slug>.md`:
C01 C02 C03 C04 C05 C07 C08 C09 C10 C12 C13 C17 C19 C20 C21 C22 C23 C24 C25 C28 C29 C41 C42

- **Batch 1 (C01,02,03,07,08,17,19,20,21,22,23,41)** — built → adversarially reviewed (`.review.md`) → Integration Pass 1 applied D-1..D-5 ([`INTEGRATION-PASS-1.md`](./INTEGRATION-PASS-1.md)). Gold standard.
- **Batch 2 partial (C04,05,09,10,12,13,24,25,28,29,42)** — built; **NOT yet adversary-reviewed** on the canonical track.

**NOT BUILT (34)** — id [slug] — build in this batch order:

| Batch | Components (id [slug]) |
|---|---|
| 2 tail | C26 [otel-collector], C27 [langfuse-traces] |
| 3 | C06 [agent-messaging], C11 [intent-intake], C14 [formula-dot-translator], C15 [workflow-linter], C16 [discipline-linter], C18 [reconciler-convergence], C30 [scenario-store], C31 [scenario-runner], C32 [judge-harness], C33 [satisfaction-metric], C34 [holdout-integrity], C35 [override-why-loop], C40 [durable-orders] |
| 4 | C36 [anomaly-detection], C37 [trajectory-clustering], C38 [diagnosis-agent], C39 [fix-task-loop-closure], C43 [isolation-boundary], C44 [digital-twin], C45 [twin-fidelity], C51 [gene-transfusion], C52 [self-bootstrap], C53 [bootstrap-validation], C54 [phase-plan], C55 [methodology-experiment], C56 [autonomy-ladder] |
| 5 | C46 [meta-metrics], C47 [variant-identification], C48 [ab-routing-stats], C49 [counterfactual-replay], C50 [promotion-gate], C57 [failure-mode-coverage] |

(Full descriptions, dependencies, and per-component gap IDs are in [`component-inventory.md`](./component-inventory.md).)

## 2. The bar (operator's, from convergence session)

Every spec/plan claim, fill, and addition must pass:

> *"Does this addition give us MORE CAPABILITY tied to a specific 12-principle? Polish/hardening that does the same thing 'better' in a non-principle way → DROP. Genuine, low-effort custom code where some part of a principle could not be met without it → KEEP. Partial satisfaction by the existing software stack (Gas City + libraries like prometheus / scikit-learn / PyOD / opentelemetry / sigstore / etc.) counts — we don't add custom code to harden what the stack already does."*

This bar is *stricter* than faithful's original "elaborate v4 with minimal fills" charter. When in doubt: DROP. Scope creep is the dominant failure mode to avoid. Grounding + worked examples in [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md).

## 3. Then: passes still owed

1. **Build sweep-1 specs + plans for the 34 unbuilt components** on the canonical track, in the batch order above, under the bar in §2.
2. **Adversary review wave** for Batch 2 already-built (C04,05,09,10,12,13,24,25,28,29,42) — never done on the canonical track.
3. **Adversary review** for Batches 2-tail / 3 / 4 / 5 as each is built.
4. **Integration Pass 2+:** re-run integrator after each batch to catch new cross-component drift.
5. **Sweep 2 (implementation-ready):** concrete signatures, schemas, sequence/state diagrams, error taxonomies, acceptance tests — re-enter every component once Sweep-1 breadth is complete.
6. **Sweep 3 (exhaustive):** pseudocode, skeletons, edge-case catalogs, perf/sec/ops.
7. **Final cross-cutting pass:** whole-system consistency, critical-path/parallelism analysis, top-level README/index.

## 4. How to resume (exact procedure)

1. Read this file, then [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md) (apply outcome + the bar), then [`META-PLAN.md`](./META-PLAN.md) (process — but note the two-track sections are superseded), then [`component-inventory.md`](./component-inventory.md) (backbone). Do **NOT** read the four v4 source docs into primary context — subagents do that.
2. Use the standing briefs: [`BUILDER-BRIEF.md`](./BUILDER-BRIEF.md), [`ADVERSARY-BRIEF.md`](./ADVERSARY-BRIEF.md). Both carry a convergence banner: **dispatch single-track only** — file paths to write are `spec/<ID>-<slug>.md` + `plan-faithful/<ID>-<slug>.md`. Ignore Track A/B legacy text below the banner.
3. Dispatch one builder per component with a tiny prompt: id+slug+one-liner, sweep level, and the bar in §2.
4. **Concurrency cap is ~8** (platform rate-limits beyond that). Pipeline at width 6–8; let it drain to ~2 then dispatch the next chunk.
5. **Subagents never run git.** Primary commits + pushes between waves. Retry push with backoff.
6. After each batch builds, run the adversary wave, then the integrator to apply any new rulings.

## 5. Binding decisions already made (do not relitigate) — detail in [`review-log.md`](./review-log.md)

- **D-1** same-provider judge baseline; cross-provider judge → FE-1.
- **D-2** one namespace: `softwarefactory.v4.{beads,trajectory,packs}` (no vendor `strongdm.*`).
- **D-3** C20 authors bead-type schemas; C22 = registration mechanism + CXDB-turn types only.
- **D-4** C20 depends on C19 (co-foundational; M1 interface freeze + no-op `validate` stub).
- **D-5** C41 owns the provenance hash-chain over C23-provided ordered `event_id`s.

## 6. Deferred capabilities (do not build now) — detail in [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md)

- **FE-1** cross-provider/cross-family judge — needs a second-provider credential.
- **FE-2** substrate portability contracts — only if a concrete second-vendor plan exists.
- **FE-3** graduated-mandatory signing — needs G37 secrets store AND a threat model that warrants it.
- **FE-4** multi-seat pool — needs concurrency outgrowing manual management AND Max ToS clarity.
- **FE-5** enumerated per-criterion DoD inside spec artifact — decide when C32/C33 are authored.

Nothing in this list is pending action right now; each has a specific external trigger.

## 7. Key risks the Skeptic flagged (still true; must be designed for in the unbuilt components)

- **G11** — entire plan assumes Gas City exists/behaves as described; every "Native" claim unverified. Sweep 2 must freeze real `gc` schemas (formula/molecule/bead) before dependents bind. Hits C12/C13/C14/C15.
- **G18** — self-healing loop (C36–C39) needs a termination bound + fix-authorization contract; schema slots exist (C20) but the numeric policy is owed by **C39** (unbuilt).
- **G31** — lethal-trifecta isolation window; C04/C42 shrink it at spawn but the real fix is **C43** (unbuilt).

## 8. Artifact map (`architectures/v4/_meta/`)

META-PLAN · TRACK-CHARTERS · DOC-TEMPLATES · BUILDER-BRIEF · ADVERSARY-BRIEF · component-inventory (+ -A/-B raw) · ambiguities-and-gaps · review-log · INTEGRATION-PASS-1 · **SURVIVOR-PASS** (convergence apply) · **FUTURE-ENHANCEMENTS** (deferred FE-1..5) · STATUS · HANDOFF (this).

Frozen reference (do not author here): `spec-optimized/` + `plan-optimized/` (each carries a `README.md` pointing back to the canonical track).
