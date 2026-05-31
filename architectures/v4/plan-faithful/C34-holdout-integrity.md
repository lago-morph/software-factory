# C34 — Holdout integrity & isolation enforcement  (Build Plan, canonical track)

> Source / Spec ref: [C34 spec](../spec/C34-holdout-integrity.md)
> Track: canonical   Status: sweep-1

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

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** | **Freeze the read-isolation policy object** — the enforced invariant `scenarios ∉ read_partition(worker)` (from C42) + its on-disk realization (perms read-only-from-implementer + separate scenario repo). Owns *realization correctness*, not the declaration. (Spec §3.1, §4.1) | S | C42 partition labels frozen (C42 M1); C30 scenario layout |
| **T2** | **Freeze the holdout-audit contract (the custom KEEP)** — inputs (scenario paths from C30 + per-actor read trail) → per-run/per-scenario `clean|leak` verdict + leak finding. Detection, not prevention (README:173). (Spec §3.2, §4.2) | M | T1; read-event source (OQ-C34-2) |
| **T3** | **Freeze the independence-check contract (D-1)** — judge↔worker pairing (from C32) → role/prompt-isolation predicate → `independent|violation` + finding. Independence by isolation, not family (D-1) / not a registry field (D-10). (Spec §3.3, §4.2) | M | C32 pairing seam; OQ-C34-3 (predicate + judge partition) |
| **T4** | **Freeze the status + findings feed** — per-run holdout + independence status + findings-as-beads, consumable by C33 (gate/annotate score), C35 (override/why), C57 (residual register). (Spec §3.4) | S | T2, T3 |
| **T5** | **Write the one-line G28 authority note + G10 caveat** — rig `read_partition` (C42) authoritative; C34 realizes (perms/repo) + verifies (audit); OPA dropped; blast-radius is C43's. A sweep-1 clarification, **not** a composition stack. (Spec §4.3) | S | T1 |
| **T6** | **Author the audit pack + exemplars** — the Gas City pack tool node (README:177) that runs the read-trail-vs-scenario-paths scan + the isolation predicate; clean and leak/violation negative examples. | M | T2, T3 |
| **T7** | **Resolve substrate prevent-vs-detect OQ (G21/OQ-C34-1)** — spike: does `gc` *prevent* the worker subprocess's out-of-partition read at tool-call time, or only permit-with-detect so the audit catches it after the fact? Feeds the C43 hand-off. | M | T1; G11-class `gc` availability |
| **T8** | **Resolve read-trail completeness OQ (OQ-C34-2)** — confirm the read-event source (Gas City event bus / OTLP raw bodies / CXDB / C41 attribution) and whether it captures *filesystem* reads (not just tool calls), which is what makes the audit sound against a broad-tool-access worker. | M | T2 |
| **T9** | **Resolve independence-predicate + FE-1 OQs** — OQ-C34-3 (exact isolation predicate + judge partition, with C42 OQ-C42-3), OQ-C34-4 (does the family-difference check move into C34 at FE-1 or stay advisory in C29?). | S | T3 |

## 2. Dependency graph

```
C42 (partition labels) ─┐
C30 (scenario layout) ──┼─► T1 ─► {T2, T5}
                        │        T2 ─► {T4, T6, T8}
C32 (judge pairing) ────┴─► T3 ─► {T4, T6, T9}
                              T1 ─► T7 (spike) ──► C43 hand-off
                              T3 ─► T9 (OQs) ────► review-log / C29(FE-1) / C42
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

| Milestone | Freezes | Unblocks |
|---|---|---|
| **M1 (earliest, load-bearing)** | Read-isolation policy object + the enforced invariant (T1) — `scenarios ∉ read_partition(worker)` realized by perms+repo backing C42's labels | The audit + independence checks (what "the policy" is) |
| **M2** | Holdout-audit contract (T2) — reads-vs-scenario-paths → `clean|leak` + finding | C57 residual register; the audit pack (T6) |
| **M3** | Independence-check contract (T3) — judge↔worker isolation predicate → `independent|violation` | C32 ↔ C34 boundary on the pairing; F1/F27/F46/F48 independence claim |
| **M4** | Status + findings feed (T4) — beads consumable by C33/C35/C57 | C33 (gate/annotate score), C35 (override/why), C57 (register) |
| **M5** | One-line G28 authority note + G10 caveat (T5) | C57 (residual-risk register). *(Not "what C43 must enforce" — the lethal-trifecta blast-radius bound is C43's; C34 owns enforcement+audit per D-13.)* |

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
