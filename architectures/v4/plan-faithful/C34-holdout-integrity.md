# C34 — Holdout integrity & isolation enforcement  (Build Plan, canonical track)

> Source / Spec ref: [C34 spec](../spec/C34-holdout-integrity.md)
> Track: canonical   Status: sweep-2

C34 is the **enforcement + after-the-fact audit** of the holdout boundary (D-13). It is not a service or a
policy engine: it (1) **owns the read-isolation policy** — the holdout invariant `scenarios ∉
read_partition(worker)` and its on-disk realization (filesystem perms + separate repo) backing **C42's**
partition labels, (2) runs the **custom after-the-fact audit** — "log audit checking agent reads vs scenario
paths" (README:173), the one genuine custom KEEP, and (3) runs the **independence check** that delivers
judge↔worker independence by **rig/role/prompt isolation** now that model-family diversity is deferred
(**D-1** → FE-1). **OPA is out of scope** (SURVIVOR-PASS C42-06); enforcement is perms + C42 partitions +
audit, nothing more. The plan is correspondingly small; the load-bearing work is **freezing the audit +
independence + findings contracts** that C33/C35/C57 build against and **retiring two uncertainties** — the
substrate prevent-vs-detect question (G21/OQ-C34-1) and the read-trail completeness that makes the audit
sound (OQ-C34-2).

## 1. Work breakdown

**Sweep-2 depth added:** T1–T5 now carry concrete deliverables (schemas, signatures, diagrams); OQ-C34-3
is resolved (D-38); T8/T9 are partially resolved. New task T10 added for the C30 MANIFEST seam.

| Task | Description | Size | Prereqs | Sweep-2 status |
|---|---|---|---|---|
| **T1** | **Freeze the read-isolation policy object** — the enforced invariant `scenarios ∉ read_partition(worker)` (from C42) + its on-disk realization (perms read-only-from-implementer + separate scenario repo). Spec §4.1 field table frozen (R/W-by annotated). | S | C42 partition labels frozen (C42 M1); C30 scenario layout | DONE — §4.1 field table complete |
| **T2** | **Freeze the holdout-audit contract (the custom KEEP)** — `run_holdout_audit(manifest, read_trail, run_id) → HoldoutAuditResult`. `HoldoutAuditRecord` bead schema frozen (§4.2). E-C34-01/03 defined. AC-C34-01/02/03 cover the test vectors. | M | T1; T10 (manifest seam); OQ-C34-2 (source named) | DONE (signatures + schemas frozen; trail completeness sub-question stays OQ-C34-2) |
| **T3** | **Freeze the independence-check contract (D-1, D-38)** — `check_independence(score_record, worker_actor, worker_partition, judge_partition) → IndependenceCheckResult`. Four-predicate spec frozen. `IndependenceAuditRecord` + `IndependenceViolationFinding` schemas frozen (§4.2). E-C34-02/04 defined. AC-C34-04/05/06 cover the test vectors. | M | C32 ScoreRecord schema frozen (D-39); D-38 (OQ-C34-3 resolved) | DONE — OQ-C34-3 RESOLVED (D-38) |
| **T4** | **Freeze the status + findings feed** — per-run `HoldoutAuditRecord` + `IndependenceAuditRecord` beads written to C19, consumable by C33/C35/C57. Sequence diagram (§5.1) shows publish path. AC-C34-09 covers the C33 gate seam. | S | T2, T3 | DONE — §5.1 sequence diagram + §4.2 schemas complete |
| **T5** | **Write the one-line G28 authority note + G10 caveat** — rig `read_partition` (C42) authoritative; C34 realizes (perms/repo) + verifies (audit); OPA dropped; blast-radius is C43's. (Spec §4.3) | S | T1 | DONE — §4.3 authority note unchanged (Sweep-1 resolution sufficient) |
| **T6** | **Author the audit pack + exemplars** — the Gas City pack tool node (README:177) that runs the `load_scenario_manifest` + `run_holdout_audit` + `check_independence` pipeline; clean and leak/violation exemplars (against §3.1/§3.2/§3.3 signatures). | M | T2, T3, T10 | PENDING (Sweep-3 / build time) |
| **T7** | **Resolve substrate prevent-vs-detect OQ (G21/OQ-C34-1)** — spike: does `gc` prevent the worker subprocess's out-of-partition read at tool-call time? Feeds the C43 hand-off. Per D-30: detect+audit path (T2) is built now regardless; watcher design is deferred pending spike. | M | T1; G11-class `gc` availability | OPEN — D-23 spike (detect+audit path complete; prevent path awaits spike) |
| **T8** | **Resolve read-trail completeness OQ (OQ-C34-2 completeness sub-question)** — confirm whether C23/C25 trail captures raw filesystem reads (Bash `cat` etc.) against a broad-tool-access worker. Sources are named (§3.2). | M | T2; D-23 spike / C43 | PARTIALLY RESOLVED (sources named: C23/C25/C41; raw-filesystem sub-question open; E-C34-03 handles incomplete trails) |
| **T9** | **Independence predicate + FE-1 forward seam** — OQ-C34-3 resolved (§3.3, D-38); OQ-C34-4 FE1_cross_family_gate seam named (§3.3) but not built (D-1). | S | T3 | OQ-C34-3 RESOLVED; OQ-C34-4 OPEN (FE-1 seam named) |
| **T10** | **Freeze C30 MANIFEST consumption seam** — `load_scenario_manifest(manifest_path, scenario_repo_root) → ScenarioManifest`; `created_by` validation (E-C34-05); staleness check (E-C34-06). Closes the C30→C34 deferred seam. | S | C30 §3.3 manifest schema frozen | DONE — §3.1 seam closed (Sweep-2) |
| **T11** | **Confirm anti-gaming structural property (§1.1)** — state explicitly that H↔I is a valid anti-gaming check because `scenarios ∉ read_partition(worker)` (D-13) and the worker cannot author the hold-out (D-38); without this the judge's verdict is self-referential for unattended operation. Cite D-13 + D-38 verbatim. | S | T1; D-13 + D-38 (already adopted) | DONE — §1.1 authored (Sweep-2) |
| **T12** | **Freeze repair-path independence duty (§1.2)** — state that the independent spec/scenario-correction path (C08/C30 + future C10/C11 seam) is also outside the worker's reach; C34 audits correction-request provenance; E-C34-09 on worker-originated request. Cite D-42 + D-43 verbatim. | S | T11; D-42 + D-43 (adopted) | DONE — §1.2 + E-C34-09 authored (Sweep-2) |
| **T13** | **Freeze DiagnosisRecord audit contract (§3.4 + §4.5)** — `audit_diagnosis(diagnosis, judge_rig_names, current_scenario_set_version) → DiagnosisAuditResult`; `audit_correction_request_provenance(...) → ProvenanceAuditResult`; `DiagnosisAuditRecord` bead schema (§4.5); E-C34-07/08/09/10 defined; AC-C34-11..14 cover the test vectors. **D-44/D-45 seam-integration edit (2026-06-02):** `audit_correction_request_provenance()` extended to cover `{Spec,Scenario}CorrectionRequest.requested_by` (D-45 canonical enforcement); C08 E-C08-07 and C30 E-C30-08 are defense-in-depth; AC-C34-15 (worker-rig `requested_by` on `SpecCorrectionRequest` fails) and AC-C34-16 (non-worker `requested_by` passes) added. | M | T3 (independence-check); C32 §3.2a schema frozen (D-43) | DONE — §3.4 + §4.5 + E-codes + AC-codes authored (Sweep-2); D-44/D-45 extension authored (2026-06-02) |
| **T14** | **Validated anti-gaming + repair path diagram (§5.2)** — Mermaid flowchart of the H↔I structural property + repair path independence; validated by tool (PASS). | S | T11, T12, T13 | DONE — §5.2 validated diagram (Sweep-2) |

## 2. Dependency graph

```
C42 (partition labels) ─┐
C30 MANIFEST (§3.1) ────┼─► T10 ─► T1 ─► {T2, T5}
                        │          T2 ─► {T4, T6, T8}
C32 ScoreRecord (D-39) ─┴─► T3 ─► {T4, T6, T9}
                              T1 ─► T7 (spike) ──► C43 hand-off
                              T3 ─► T9 (OQs) ────► review-log / C29(FE-1)
                              T10 (DONE — seam closed)

D-13 + D-38 ────────────────► T11 (anti-gaming structural property)
D-42 + D-43 + T11 ──────────► T12 (repair-path independence)
C32 §3.2a (D-43) + T3 ──────► T13 (DiagnosisRecord audit contract)
T11 + T12 + T13 ────────────► T14 (validated diagram §5.2)
T13 ────────────────────────► T4 (extended: DiagnosisAuditRecord beads also published)
```

- **Critical path:** T1 → (T2 + T3) → T4. These freeze the read-isolation policy, the audit, the
  independence check, and the findings feed that C33/C35/C57 all consume. T6 (the pack) hangs off T2+T3.
- **Upstream blockers:** T1 needs **C42's** partition labels frozen (C42 milestone M1) and **C30's**
  scenario layout; T2 needs the read-event source resolved (OQ-C34-2); T3 needs **C32's** judge↔worker
  pairing seam and the independence predicate (OQ-C34-3, entangled with C42's OQ-C42-3 judge partition). T7's
  spike is gated on `gc` being runnable end-to-end (the same G11 assumption that blocks C01/C42).
- **Downstream consumers waiting on these freezes:** C33 (gate/annotate a tainted satisfaction score), C35
  (override/why on a leak/violation finding), C57 (residual-risk register — so "held-out" is not
  over-trusted, G10), C43 (bounds the residual broad-tool-access blast radius — the distinct lethal-trifecta
  boundary, D-13).

## 3. Parallelization

- **Independent once T1 lands:** T5 (authority note) is disjoint from the audit/independence path and can be
  authored immediately after T1.
- **The two verification paths fan out:** T2 (holdout audit) and T3 (independence check) are independent
  workstreams off T1/C32 respectively and can be built concurrently; they re-converge at T4 (findings feed)
  and T6 (the pack).
- **The OQ workstreams run in parallel with the contracts:** T8 (read-trail completeness) only needs T2's
  shape; T9 (predicate + FE-1) only needs T3; both can run alongside the T4/T6 build.
- **The one serial spike:** T7 (substrate prevent-vs-detect) is the long pole and gates the C43 hand-off;
  start it as soon as T1's policy is frozen and `gc` is available — do not let it block T2/T3/T4.
- **Cross-component parallelism:** because C34 is Batch-3 alongside C30/C31/C32, C33 and C35 can build
  against **stubbed** holdout/independence verdicts the moment T4 freezes, before T7/T8 resolve.

## 4. Interfaces-first / contract milestones

| Milestone | Freezes | Status (Sweep-2) | Unblocks |
|---|---|---|---|
| **M0 (new — C30 seam)** | C30 MANIFEST consumption seam (T10) — `load_scenario_manifest` signature + E-C34-05/06 + `created_by` validation | DONE | M1; audit `protected_paths` |
| **M1 (load-bearing)** | Read-isolation policy object + enforced invariant (T1) — §4.1 field table frozen | DONE | The audit + independence checks |
| **M2** | Holdout-audit contract (T2) — `run_holdout_audit` signature + `HoldoutAuditRecord`/`LeakFinding` schemas (§3.2/§4.2) | DONE | C57 residual register; audit pack (T6) |
| **M3** | Independence-check contract (T3) — four-predicate `check_independence` + `IndependenceAuditRecord`/`IndependenceViolationFinding` schemas (§3.3/§4.2); OQ-C34-3 RESOLVED (D-38) | DONE | C32 ↔ C34 pairing; F1/F27/F46/F48 independence claim |
| **M4** | Status + findings feed (T4) — `HoldoutAuditRecord` + `IndependenceAuditRecord` beads to C19; sequence diagram §5.1 | DONE | C33 (gate score), C35 (override/why), C57 (register) |
| **M5** | One-line G28 authority note + G10 caveat (T5) | DONE (Sweep-1; unchanged) | C57 residual register |
| **M6 (PENDING)** | Audit pack tool node (T6) — Gas City pack running the pipeline against real `gc` | PENDING — Sweep-3 / build | End-to-end AC-C34-01..14 pass |
| **M7 (new — Sweep-2)** | Anti-gaming structural property + repair path independence (T11+T12) — §1.1 + §1.2 state the H↔I anti-gaming argument; D-13 + D-38 + D-42 + D-43 cited verbatim | DONE | C52/C53/C57 can discover C34's correction-path enforcement duty |
| **M8 (new — Sweep-2)** | DiagnosisRecord audit contract (T13) — `audit_diagnosis` + `audit_correction_request_provenance` signatures; `DiagnosisAuditRecord` schema (§4.5); E-C34-07/08/09/10; AC-C34-11..14. **D-44/D-45 (2026-06-02):** `audit_correction_request_provenance()` extended to `{Spec,Scenario}CorrectionRequest.requested_by` (D-45 canonical enforcement); AC-C34-15/16 added. | DONE | C52 blocks on `failed` DiagnosisAuditRecord; C53 blocked from using stale/inconsistent `tri_alignment`; C08/C30 defense-in-depth guards backed by C34 canonical enforcement (D-45) |
| **M9 (new — Sweep-2)** | Validated anti-gaming diagram (T14) — §5.2 Mermaid flowchart, tool-validated PASS | DONE | Diagrams available for integration review |

Freeze M1 first: it is the policy the audit and independence checks rest on. M2/M3/M4 let C33/C35/C57 start
without waiting on the T7 substrate spike. M3 is the seam C32 needs to expose its judge↔worker pairing.

## 5. Risks & de-risking order

1. **(Highest) The audit is detect-only, and the read trail may be incomplete (G21/OQ-C34-1/OQ-C34-2).** Per
   **D-1** there is no model-family fallback, so a **detect-only** audit over a possibly-incomplete read
   trail is the *sole* holdout integrity guarantee. **De-risk first via T7 + T8**: (T7) establish whether
   `gc` *prevents* the out-of-partition read or only permits-with-detect; (T8) establish whether the
   read-event source captures *filesystem* reads, not just tool calls — an audit that misses a `cat
   scenarios/...` via Bash is unsound. If detect-only over a partial trail, the residual must be loud in
   C57/C35. *(Ownership of the prevention seam is **settled by D-13**: C34 owns enforcement + audit; the
   broad-tool-access read-escape is **C43's** distinct lethal-trifecta blast-radius bound. The residual
   *substrate* question — prevent vs permit-with-detect (G11) — stays for the spike.)*
2. **`gc` partition primitive may not exist as described (G11-class).** T1/T7 assume C42's `[[rig]]`
   `read_partition` and the perms/repo realization are real Gas City behavior (AI-CONTEXT §13.3 / README:171),
   but this is asserted-not-run. Spike `gc` early (T7) — the same uncertainty that blocks C01/C42.
3. **Independence predicate is underspecified for a same-provider judge (OQ-C34-3, D-1).** "Independence by
   isolation" needs a concrete predicate (distinct rig + prompt + partition + no shared context) and the
   judge's partition is itself open (C42 OQ-C42-3). De-risk via T3/T9 with C42/C32 before C33 trusts an
   `independent` verdict.
4. **Over-build temptation: an OPA / policy-engine enforcement layer.** The inventory and AI-CONTEXT §6.2
   name "OPA + file permissions composition", which invites building a Rego policy engine or a custom MAC
   layer. **De-risk by holding the line** (T1/T5): OPA is **dropped** (SURVIVOR-PASS C42-06; README:425
   "later"); enforcement is perms + C42 partitions + the after-the-fact audit only. Flag any OPA/MAC/
   tool-call-interceptor creep at review.
5. **Cross-family scope creep (G08).** The inventory says "cross-family + independence enforcement", which
   invites building a model-family-difference enforcer that v4 cannot source under same-Max (AI-CONTEXT
   §4.1). **De-risk via D-1**: family difference is relaxed/advisory (C29) and deferred to **FE-1**; C34
   delivers independence by isolation only. T9 records the FE-1 boundary.

## 6. Definition of done

**Per-task:** each contract task (T1–T5) is done when its spec section is frozen and a downstream consumer
(C33/C35/C57/C43) can build a stub against it; T6 is done when the audit pack + clean/leak/violation
exemplars exist; T7/T8/T9 are done when the OQ is answered in review-log (or explicitly carried forward with
owner + reason).

**Per-component (tied to spec §8 acceptance criteria):**
- The read-isolation policy is realized (perms + repo) and the holdout invariant enforced; a realization
  where the worker can read scenario paths despite the declared partition is surfaced as a defect (§8.1).
  The substrate prevent-vs-detect *strength* is recorded (T7); the broad-tool-access read-escape is C43's
  blast-radius bound — the split is **settled by D-13** (C34 owns enforcement+audit; C42 provides; C43
  bounds).
- The holdout audit yields `leak` on a worker-rig read inside `scenarios` and `clean` otherwise, raising a
  leak finding (§8.2, the custom KEEP, README:173) — detection, not prevention.
- The independence check yields `violation` on a judge sharing the worker's rig/prompt/context and
  `independent` otherwise (§8.3), by isolation (D-1), not family (G08) and not a registry field (D-10).
- Cross-family is relaxed and recorded as FE-1; C34 does not block on a second-provider credential and the
  F48 shared-training-distribution residual is surfaced "Partial" (§8.4).
- C33/C35/C57 can consume C34's status + findings feed to gate/annotate a tainted score and surface the
  residual (§8.5).
- The G28 one-line authority note (OPA dropped) + the G10/G21 detect-after-the-fact caveat are explicit and
  discoverable by C30/C42/C43/C57 (§8.6, §8.7).
- **No OPA / policy-engine / custom-MAC over-build** is present; enforcement is perms + C42 partitions +
  audit (§8.8, SURVIVOR-PASS C42-06).
- All four OQs are in review-log with owners (OQ-C34-1 → reconciler/C43 + G11; OQ-C34-2 → C34 + event-source
  owner C23/C25/C41; OQ-C34-3 → C34 + C42 + C32; OQ-C34-4 → C29/FE-1).
- **Sweep-2 additions (T11–T14):**
  - The anti-gaming structural property (§1.1) is stated with D-13 + D-38 cited verbatim; the H↔I verdict
    trustworthiness argument for unattended operation is explicit.
  - The repair-path independence duty (§1.2) is stated with D-42 + D-43 cited verbatim; E-C34-09 covers the
    worker-originated correction-request violation.
  - `audit_diagnosis()` + `audit_correction_request_provenance()` signatures and the `DiagnosisAuditRecord`
    bead schema (§3.4 + §4.5) are frozen; E-C34-07/08/09/10 and AC-C34-11..14 cover the surface.
  - **D-44/D-45 (2026-06-02):** `audit_correction_request_provenance()` is the canonical enforcement owner
    for worker-rig `requested_by` checks on both `SpecCorrectionRequest` (C08 route) and
    `ScenarioCorrectionRequest` (C30 route); E-C34-09 extended; AC-C34-15 (worker-rig fails) and
    AC-C34-16 (non-worker passes) added; C08 E-C08-07 and C30 E-C30-08 are explicitly defense-in-depth.
  - The §5.2 anti-gaming + repair path diagram is validated (PASS) and in the spec.
