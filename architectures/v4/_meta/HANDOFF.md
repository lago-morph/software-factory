# HANDOFF — v4 Spec & Plan run (resume from here)

**Last updated:** 2026-06-01 (Sweep-2 run #1 — D-23 + first depth cluster — complete; see §0).
**Status:** **Sweep-1 COMPLETE** (57/57 built+reviewed+integrated) + **wrap-up COMPLETE** (D-20…D-25 adopted, panel VERDICT, guides, products-first build order). **Sweep-2 has STARTED** (this run): the **D-23 Gas City reality-check is done as protocol + harvest** (no live run, per operator), the pivotal **auto-001 decision is settled** (2 rounds / 6 adversaries), and the **first Sweep-2 depth cluster (C19/C20/C21/C23/C41) landed**. **2 operator morning-review items are open** (D-20 re-adoption; per-rig-class autonomy) — see [`overnight-summary-2026-06-01-sweep2.md`](../../../overnight-summary-2026-06-01-sweep2.md) §6.
**Working tree:** the Sweep-2 run #1 work is in stacked PRs **#229→#232 + wrap** (NOT yet merged to `main` at run close). Prior state: everything through #228 is in `main`.

## 0. Sweep-2 run #1 (2026-06-01) — what landed + what's next

**Done this run (stacked PRs #229–#232 + wrap):**
- **D-23 (protocol + harvest):** [`D-23-gas-city-spike-protocol.md`](./D-23-gas-city-spike-protocol.md) (runnable prevent-vs-detect / `[[service]]` / Orders-durability checklist) + [`D-23-substrate-harvest.md`](./D-23-substrate-harvest.md) (12 facts from the real `gascity-prototype@b14c278`). Closed **XC-9, C42:OQ-4, C04:OQ-4**; **0 true contradictions** (3 flagged, all reclassified NEW-INFO). 13 specs annotated `[D-23 substrate-verified]`.
- **auto-001 decided** (the [detect-only binding-gate brief](./decisions/auto-001-detect-only-binding-gate.md)): detect-only ⇒ binding gate on unattended P2, as a **policy rubric** (descope-to-L4 default; prevent layer NOT pre-blessed; per-rig-class middle; fail-closed). Resolved **OQ-C41-4** via D-29.
- **Sweep-2 depth cluster** (evidence/data substrate): **C19, C20, C21, C23, C41** at implementation depth. Seam adversary found + fixed a HIGH `event_id` drift → ledger **D-26…D-29**.

**MANDATORY FIRST ACTIONS for the next session (in order):**
1. **Resolve the 2 morning-review items** ([summary §6](../../../overnight-summary-2026-06-01-sweep2.md)): (a) re-adopt D-20 as conditional-on-prevention? (b) accept per-rig-class autonomy? Until (a) is answered, do NOT wire the auto-001 rubric into specs.
2. **If (a) re-adopted:** wire the auto-001 rubric into **C43/C34/C42/C56/C57** (the deferred spec edits) as its own PR.
3. **The empirical D-23 spike is still owed** (needs a Docker-capable env; prototype + protocol ready) — prevent-vs-detect (C34:OQ-C34-1 ≡ C43:OQ-C43-1) stays OPEN until then; it gates the auto-001 rubric's actual outcome.
4. **Continue Sweep-2 depth** on the remaining ~52 components. Suggested next clusters: **workflow-engine** (C04/C05/C12/C13/C18/C40) and **eval/holdout** (C30/C31/C32/C33/C34/C42 — note holdout depth is partly gated on item 1). Use the [`BUILDER-BRIEF`](./BUILDER-BRIEF.md) at Sweep-2 depth, the C20 spec as the format **exemplar**, and a cross-cluster seam adversary per cluster.

This file + the other `_meta/` artifacts are sufficient to resume with zero re-grounding. Start with the run summary at [`run-summary.md`](../../../run-summary.md), the operator decision guide [`decisions-to-make.md`](../../../decisions-to-make.md), and the coverage ledger [`STATUS.md`](./STATUS.md).

---

## 1. Where we are: 57 of 57 built + reviewed + integrated, then wrapped up

**One canonical track** — `spec/` + `plan-faithful/`. `spec-optimized/` + `plan-optimized/` are frozen reference. Every component (C01–C57) has `spec/<ID>-<slug>.md` + `plan-faithful/<ID>-<slug>.md` + `spec/<ID>-<slug>.review.md` (**57 / 57 / 57**). All adversary verdicts across the run were **accept-with-fixes** (0 blockers, 0 needs-rework). The live per-component four-axis state (Built / Reviewed / Incorporated / iNtegrated) is in [`STATUS.md`](./STATUS.md) — all 57 are ✓ on all four.

Sweep-1 was produced in batches (build → adversary-review → integrator), each batch's cross-component findings recorded as ledger decisions **D-1..D-19** (+ XC-3 resolved). Detail in [`review-log.md`](./review-log.md).

**The wrap-up run (after Sweep-1 close) added:**
- **Operator decisions D-20…D-25** adopted and annotated across affected specs — see [`decisions-to-make.md`](../../../decisions-to-make.md) (plain-language) and §5 below. This **resolved every Sweep-1 morning-review item** (D-18, OQ-6, F54 — see §3).
- **Expert-panel review** of the whole corpus — [`VERDICT.md`](./panel/VERDICT.md) + five panelist opinions (`panel/01..05`). The panel's single headline: the whole plan is gated on **D-23** (verify Gas City's "native" claims against a real `gc` *before* building on them), and it argues D-23 should be a **binding go/no-go gate** on D-20, not just a noted spike.
- **Three human-facing guides** (kept in sync): the engineer guide [`architecture-guide-for-engineers.md`](../../../architecture-guide-for-engineers.md), the plain-English build order [`build-order-plain-english.md`](../../../build-order-plain-english.md), and the implementer build order [`implementation-dependencies.md`](../implementation-dependencies.md).
- **The implementer build order now leads with the safe-self-build backbone** (PR #224): the minimum 25-component vertical slice to a first human-reviewed self-build (rings 19→22→25), grouped into six implementation clusters, with a **product→components** table (one Gas City adoption discharges 11 backbone components), dotted-line soft deps, a top-10-next by cost/benefit, and the beads/Gas-City "one install, many components" clarification. Two graph corrections landed there: **C31 scenario-runner is required** (was missing) and **C43 splits per D-20** (boundary-typing now, twin half C44 deferred).
- A whole-57 **consistency pass** report (under `_meta/`) and **C46 dep-edge fix** (D-24).

## 2. The bar (operator's — still in force for every sweep)

> *"Does this addition give us MORE CAPABILITY tied to a specific 12-principle? Polish/hardening that does the same thing 'better' in a non-principle way → DROP. Genuine, low-effort custom code where some part of a principle could not be met without it → KEEP. Partial satisfaction by the existing software stack (Gas City + libraries like prometheus / scikit-learn / PyOD / opentelemetry / sigstore / Inspect AI / DSPy / LocalStack / etc.) counts — we don't add custom code to harden what the stack already does."*

When in doubt: DROP. Grounding + worked examples in [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md). This bar held across all 57 — Sweep 2/3 must keep applying it (don't let implementation-depth reintroduce dropped hardening).

## 3. Sweep-1 morning-review items — ALL RESOLVED by D-20…D-25

The three items the previous handoff said to "resolve first" are now closed:
- **D-18 (C43 split-sequencing)** — **ADOPTED as D-20**: the C43 **boundary-typing half** (needs only C42) is pulled forward as the mandatory precondition before any unattended run; the **twin-isolation half (C44)** is deferred. No longer provisional.
- **OQ-6 (C46 dependency edge)** — **resolved by D-24** (meta-metrics cost signal re-sourced; dep edge corrected).
- **F54 / OQ-C57-3 (objective-drift audit ownership)** — **resolved by D-21**: objective-drift is logged UNBUILT with a cheap human checkpoint while a person still reviews batches; an automated drift detector is a **required precondition for full lights-out** (not built yet — the loudest residual; see §7).

## 4. Passes still owed (next runs)

1. **Sweep 2 (implementation-ready) — the next work.** Concrete signatures, data schemas, API/message contracts, sequence/state diagrams (Mermaid), error taxonomies, concrete acceptance tests — re-enter every component. **First action: the D-23 Gas City reality-check spike** (prevent-vs-detect, Orders durability, `[[service]]` semantics) against a pinned `gc`; the panel wants a *detect-only* outcome to bind a re-evaluation of D-20, not just be noted (VERDICT §6, PF follow-ups).
2. **Whole-57 cross-batch integration drift pass** — integration was done per-batch; a final drift pass over the seams frozen "→ Sweep-2 joint freeze" (C12/C14/C15 loop-DOT encoding D-16; C42/C34/C32 judge read-surface D-17; C36↔C37 population seam; C38↔C39 / C48↔C55 / C46 dep-edge).
3. **Sweep 3 (exhaustive):** pseudocode/algorithms, skeletons, edge-case catalogs, perf/security/ops.
4. **Final cross-cutting pass:** whole-system consistency, critical-path/parallelism analysis, top-level README/index.

## 4b. How to resume (Sweep 2)

1. Read [`run-summary.md`](../../../run-summary.md), [`decisions-to-make.md`](../../../decisions-to-make.md) (D-20..D-25 in plain language), this file, then [`STATUS.md`](./STATUS.md) (coverage ledger) and [`review-log.md`](./review-log.md) (D-1..D-19 + ~196 harvested OQs — the OQs are the Sweep-2 work list). Skim [`VERDICT.md`](./panel/VERDICT.md) for the cross-cutting risk ranking + the PF-1..PF-3 follow-ups. Do **NOT** read the four v4 source docs into primary context — subagents do that.
2. **Start with the D-23 Gas City reality-check spike** (it gates the most: every "Native" claim, and whether D-20's fence actually *prevents*). The other operator decisions (D-20..D-22, D-24, D-25) are already adopted and annotated into the specs — do not relitigate.
3. Use the standing briefs [`BUILDER-BRIEF.md`](./BUILDER-BRIEF.md) + [`ADVERSARY-BRIEF.md`](./ADVERSARY-BRIEF.md) (single-track banners). Dispatch one builder per component at **Sweep 2** depth; concurrency cap ~8; pipeline; subagents persist to disk + return receipts; **primary owns all git**; commit+push every wave.
4. Each component's `spec/<ID>-*.md` already carries its Sweep-1 OQs inline + its `.review.md` (+ any D-20..D-25 annotations) — Sweep 2 starts from those, not a blank page.

## 5. Binding decisions (do not relitigate) — detail in [`review-log.md`](./review-log.md) + [`decisions-to-make.md`](../../../decisions-to-make.md)

**Sweep-1 ledger (D-1..D-19):** D-1 same-provider judge (cross-family→FE-1) · D-2 bundle-id namespace `softwarefactory.v4.{beads,trajectory,packs}` · D-3 C20 authors bead schemas / C22 mechanism · D-4 C20→C19 · D-5 C41 hash-chain over C23 · D-6 "canonical track" nomenclature · D-7 node-kind home=C12 · D-8 convoy→C05 / Order→C40 · D-9 F38 vocab-lint=C10 · D-10 modeldb=`{id,family,cost_tier}` · D-11 LangFuse traces-only seam · D-12 two-sink cross-refs · D-13 holdout C34(enforce+audit)/C43(lethal-trifecta) · D-14 G37(secrets)≠FE-3(signing) · D-15 satisfaction holistic (FE-5 deferred) · D-16 loop-DOT encoding=C12 · D-17 judge read-surface · D-18 C43 split-sequencing (**now adopted as D-20**) · D-19 methodology significance→C48 · XC-3 RESOLVED C39 owns G18 numeric policy.

**Operator wrap-up decisions (D-20..D-25 — ADOPTED 2026-05-31):** **D-20** fence (C43 boundary-typing) pulled to a P2 precondition before any unattended run · **D-21** objective-drift (F54) logged-unbuilt + cheap human checkpoint; automated detector required before full lights-out · **D-22** counterfactual replay (C49): ship the deterministic half, keep the LLM-step half experimental (G19 honesty) · **D-23** run the Gas City prevent-vs-detect reality-check spike (G11) as the first Sweep-2 action · **D-24** C46 meta-metrics dependency-edge wiring correction · **D-25** secrets deferred to first-credential + Unleash license version-pin.

## 6. Deferred capabilities (do not build) — detail in [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md)

FE-1 cross-provider judge · FE-2 portability contracts · FE-3 graduated-mandatory signing (needs G37) · FE-4 multi-seat pool · FE-5 enumerated per-criterion DoD — **resolved by D-15** (holistic satisfaction; revisit only when C46 needs per-criterion diagnosis). Each has a specific external trigger; none pending.

## 7. Key residual risks (carried into Sweep 2 + the C57 register)

- **G11** — every "Native" Gas City claim is still unverified against a real `gc`. **D-23 makes the reality-check spike the first Sweep-2 action**; the panel wants a *detect-only* outcome to bind a D-20 re-evaluation. Touches C01/C12/C13/C14/C18/C40 + the prevent-vs-detect OQ (C43/C34). The single highest-leverage unknown.
- **G31** — lethal-trifecta has a deterministic boundary-typing **design** (C43). **D-20 (adopted)** pulls the boundary-typing half forward as the P2 precondition, which closes the documented exposure window *if* the fence actually prevents (depends on D-23). The twin-isolation half (C44) is still future (the XC-8 exposure window narrows but does not vanish).
- **F54 — objective drift:** **D-21 (adopted)** — logged UNBUILT with a human checkpoint; the **automated detector is a required precondition for full lights-out** and is not built. Loudest residual after G31 on a self-modifying L5 factory.
- **G19** — counterfactual replay (C49): **D-22** ships the deterministic-slice half now, keeps full LLM-step counterfactual experimental + human-reviewed. v4's riskiest invention leaf.
- **G37** — no secrets store (owned by C03): **D-25** defers to first-credential need + pins the Unleash license version; blocks FE-3 signing; keeps several controls "detect not prevent".

## 8. Artifact map

**`architectures/v4/_meta/`:** META-PLAN · TRACK-CHARTERS · DOC-TEMPLATES · BUILDER-BRIEF · ADVERSARY-BRIEF · component-inventory (+ -A/-B raw) · ambiguities-and-gaps · **review-log** (D-1..D-19 + harvested OQs) · INTEGRATION-PASS-1 · SURVIVOR-PASS · FUTURE-ENHANCEMENTS · RUN-SCOPE-2026-05-31 (Sweep-1 scope) · **STATUS** (coverage ledger) · **panel/** (VERDICT + 5 opinions) · HANDOFF (this).

**`architectures/v4/`:** **implementation-dependencies.md** (build order — leads with the safe-self-build backbone) · README · AI-CONTEXT · F-MODE-COVERAGE · one-shot-specs-and-research · optimized-differences(+reviews). Frozen reference (do not author here): `spec-optimized/` + `plan-optimized/`.

**Repo root:** [`run-summary.md`](../../../run-summary.md) · [`decisions-to-make.md`](../../../decisions-to-make.md) (D-20..D-25 plain-language) · [`architecture-guide-for-engineers.md`](../../../architecture-guide-for-engineers.md) · [`build-order-plain-english.md`](../../../build-order-plain-english.md).
