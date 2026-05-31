# C38 — Diagnosis Agent (Healer)  (Build Plan, canonical track)

> Source / Spec ref: spec/C38-diagnosis-agent.md

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Diagnosis prompt/role (the transfused Tracker discipline).** Author the Claude Code **diagnosis-role prompt** that reproduces Tracker's `Diagnose`/`Audit`/`Doctor` *discipline*: investigate a failure cluster's trajectories and produce a **structured, evidence-bound, JSON-serializable failure report** (root cause + evidence refs + confidence + proposed remedy), not free prose (README:256,462; AI-CONTEXT:276). **Pattern-transfusion by default** (legal regardless of Tracker license, G30). This is C38's primary deliverable. | M | C37 (cluster shape), C21 (CXDB query tools), C28 (agent loop) |
| T2 | **Cluster + CXDB read-tool wiring.** Wire the diagnosis role's **read-only** access to a C37 cluster (members/exemplars) and the cluster's CXDB trajectory turn-DAGs (query tools, I3) — no write tools on the trajectories it diagnoses. | S | C37, C21, C17 |
| T3 | **Diagnosis-model binding (C29/D-1).** Consume `resolveModel(diagnosis/healer node)` and run the role as the **Claude Code** investigator (same provider, Phase-0, D-1) — a distinct *role*, not a distinct provider. | S | C29, C28 |
| T4 | **`diagnoseCluster(clusterRef) → Diagnosis` core.** Bind (cluster + its CXDB context) into one investigation run → one structured `Diagnosis`. The genuine custom glue C38 adds beyond the stack (the engine is C28; the *focused work* is this + T1). | M | T1, T2, T3 |
| T5 | **`Diagnosis` emission (→ C39).** Emit one structured, attributed (C41) `Diagnosis` per cluster — `{cluster_id, root_cause, evidence_refs[], confidence, proposed_remedy}` — to a bead/CXDB turn for **C39** to mint a `fix_task`. (Build-time `transfused_from` provenance is on C38's `factory_build` bead per T7, NOT a field of this runtime record — C20/C51, D-3.) **C38 stops at the diagnosis; it does NOT write `fix_task` (I2, XC-3→C39).** | M | T4, C41, C19/C21 |
| T6 | **Degraded / inconclusive paths.** Diagnosis-model-unavailable or CXDB-evidence-miss → undiagnosed + bead/gate event; insufficient signal → explicit **low-confidence/inconclusive** verdict; never a fabricated cause (I4/I5). | S | T4, T5 |
| T7 | **Provenance + license flag (G30, framework C51).** Stamp `transfused_from = Tracker Diagnose/Audit/Doctor` + the **pattern-vs-code** flag; default pattern-only until Tracker license is verified permissive (AI-CONTEXT:625). Route the license-clearance *framework* + correctness *predicate* to **C51** (G07/G30); do not build them here. | S | T1, C51 (records into) |
| T8 | **Healer scenario hook (G07 acceptance seam).** Leave the seam by which C38 is evaluated against the **adversarial Healer scenario set** — "manually-clustered failure trajectories; ensure its diagnoses match the human" (README:499) — scored by the evaluation tier (C30–C33). C38 supplies the diagnosis-under-test; the bar/threshold is C53/C51's, not C38's. | S | T5, C30–C33 (consume) |

## 2. Dependency graph

Critical path: **C37 (failure cluster) + C21 (CXDB context) + C29 (diagnosis model) → T1 → T4 → T5 →
`Diagnosis` consumable by C39**.
- T1 (the diagnosis prompt) is the load-bearing deliverable; T4 joins prompt + cluster + CXDB into the
  first real diagnosis; T5 is the handoff C39 consumes.
- **Must precede C38:** **C37** (the failure clusters — the *unit* of diagnosis), **C21** (CXDB trajectory
  store + query tools), **C28** (the Claude Code agent loop the role runs in), **C29** (diagnosis-role
  model identity), **C41** (attribution). C38 is sequenced **last among C36–C39** in v4 ("save the
  diagnosis agent for after the substrate is proven", README:466) — build C36→C37 first.
- **Built concurrently with C38:** **C39** (consumes the `Diagnosis` to mint `fix_task` + owns
  termination/escalation — depends on the *`Diagnosis` schema*, not C38 internals), **C40** (the durable
  Order that may *drive* a diagnosis run — couples to the run, not to C38's reasoning), **C51** (the
  transfusion correctness predicate + license framework C38 *records into*).

## 3. Parallelization

After T1 (prompt) + T2/T3 (cluster/CXDB/model wiring) land, three independent workstreams fan out:
- **WS-A (diagnosis core):** T4 + T5 — investigate→`Diagnosis`→emit. The spine; produces the record C39
  consumes.
- **WS-B (robustness):** T6 — degraded/inconclusive paths. Independent of the happy path once the
  `Diagnosis` shape (T5) is frozen; the no-fabricated-cause guarantee (I4/I5).
- **WS-C (transfusion + evaluation governance):** T7 (provenance/license flag) + T8 (Healer-scenario
  seam). Governance/correctness; independent of A/B once the record carries `transfused_from` — and both
  *route their frameworks out* (license → C51, correctness bar → C51/C53), so C38 builds the seam, not the
  framework.

T5 (the `Diagnosis` schema) is the **freeze-early join point** — **C39** builds against it (to mint a
`fix_task`) and a **human reviewer** reads it (README:466), so it gates the most downstream work (see §4).

## 4. Interfaces-first / contract milestones (freeze early)

1. **`Diagnosis` schema** (T5) — the single most load-bearing contract: **C39** binds to it to mint a
   `fix_task` and carry loop-closure; a **human** reviews it (README:466). Freeze first so C39 builds
   against a stub in parallel. Must carry: `cluster_id`, `root_cause`, `evidence_refs[]` (CXDB turn/span),
   `confidence`, `proposed_remedy`, `transfused_from`. Pin against the **verified Tracker `Diagnose`/
   `Audit`/`Doctor` field shape** (AI-CONTEXT:276; `[FAITHFUL-FILL]`, OQ4).
2. **`diagnoseCluster(clusterRef) → Diagnosis`** (T4) — the agent entry point; freeze so a C40 Order (or any
   batch caller) can launch a diagnosis run against the contract.
3. **Cluster-to-diagnose contract** (T2, *consumed from C37*) — what a "failure cluster" is (id, members/
   exemplars, shared-failure signal). Freeze C38's *consumption* shape so C37 and C38 evolve independently
   (C37 owns the cluster schema; C38 consumes it).
4. **Diagnosis→C39 handoff** (T5) — does C39 *poll* `Diagnosis` beads, or does C38 *hand* the `Diagnosis`
   to a C39 entry? Freeze C38's *emit* shape so C39 builds the `fix_task` minting + termination against it
   (the numeric policy is C39's, XC-3). (OQ1 — the C38/C39 *ownership split* is confirmed on disk by
   [`spec/C39-fix-task-loop-closure.md`](../spec/C39-fix-task-loop-closure.md) §1/§3.1; only the *handoff
   mechanism* — poll vs hand-off — is the open sweep-2 detail.)

## 5. Risks & de-risking order

1. **Diagnosis quality — do the LLM's diagnoses match a human's? (T1/T8), highest.** The whole P11 value
   rests on the diagnosis being *right* (G07). De-risk with the **adversarial Healer scenario set** early —
   "feed it failure trajectories the team manually clustered, ensure its diagnoses match" (README:499) —
   before trusting the loop. This is the make-or-break of the diagnosis agent; spike the prompt against
   labelled clusters first. (Correctness *predicate/bar* is C51/C53's; C38 spikes the *capability*.)
2. **Tracker license verdict (T7, G30).** Confirm Tracker's actual license (likely MIT, "verify",
   README:292) so C38 can decide **pattern-vs-code** transfusion. De-risk by **building pattern-first** (the
   JSON-failure-report *discipline* is legal regardless) — code-port is an *upgrade* iff verified permissive.
   Never block the build on the license; route the *framework* to C51.
3. **Evidence-binding discipline (T1/T4, I1).** Prove the LLM reliably *cites CXDB evidence refs* for its
   root cause rather than emitting a plausible prose opinion — this is what makes the diagnosis checkable by
   C39 and a human, and is the core of the Tracker transfusion. Spike: reject any `Diagnosis` with an empty
   evidence set (AC3) and measure how often the model produces grounded evidence.
4. **C38↔C39 seam (OQ1) — *mechanism* only; split confirmed.** README reads as "diagnosis agent writes
   `fix_task`" but the inventory splits C38/C39, and that split is now **confirmed on disk** by
   [`spec/C39-fix-task-loop-closure.md`](../spec/C39-fix-task-loop-closure.md) §1/§3.1 (C39 consumes the
   diagnosis and mints the `fix_task`; C39 owns the numeric termination policy, XC-3). The residual risk is
   narrower than "wrong split": freeze the handoff *transport* (does C39 poll `Diagnosis` beads, or does C38
   hand the `Diagnosis` to a C39 entry?) with the C39 author before sweep-2 so the emit shape and the
   `fix_task`-minting intake agree.
5. **Shared-seat cost/throughput (OQ5, with C28 G13/G34, G32).** An LLM root-cause investigation **per
   cluster** competes with build + judge calls for the single Phase-0 Max seat. Per-cluster (not
   per-trajectory) is the natural rate-limiter (clustering, C37, is *upstream* for this reason). Quantify a
   diagnosis token-budget probe → review-log; do **not** design horizontal scale on the canonical track.

## 6. Definition of done

- **Per spec ACs:** AC1 (one attributed, evidence-bound `Diagnosis` per cluster, consumable by C39), AC2
  (diagnoses **match the human** on the held-out Healer scenario set — the G07 acceptance, bar owned by
  C53/C51), AC3 (evidence-bound, not free prose — empty-evidence diagnosis rejected), AC4 (inconclusive is a
  first-class low-confidence verdict, never a fabricated cause), AC5 (**diagnose-don't-fix** — no `fix_task`/
  deploy side-effect; that is C39's, XC-3), AC6 (read-only over trajectories), AC7 (transfusion recorded;
  **pattern-by-default** absent a verified-permissive Tracker license), AC8 (no silent/fabricated diagnosis
  on model-unavailable / CXDB-miss).
- **Per-task DoD:** each artifact (the diagnosis prompt/role, the read-tool wiring, the `Diagnosis` record,
  the provenance stamp) is version-controlled in a **"Specialized Gas City agent pack"** (C02/C17, README:256)
  and exercised by at least one real diagnosis run with the `Diagnosis` captured on a bead/CXDB turn.
- **Component DoD:** a real **failure cluster** (C37) is diagnosed end-to-end by the **Claude Code diagnosis
  role** over its CXDB trajectories, emitting an attributed, evidence-bound `Diagnosis` that **C39 can mint a
  `fix_task` from** and a **human can review** (README:466); the diagnoses **match the human** on the
  adversarial Healer scenario set (README:499) above the C53/C51 bar; and the deferred edges have written
  findings in `_meta/review-log.md` — **G30** (Tracker license verdict → C51 framework; pattern-by-default
  meanwhile), **G07** (general transfusion-correctness predicate → C51; C38 supplies match-the-human
  acceptance), **OQ1** (C38↔C39 `fix_task` seam), **OQ5** (per-cluster cost). **C38 builds NO fix-task
  minting, NO loop-closure/termination policy (C39), NO clustering (C37), NO investigation engine / CXDB
  query tooling (C28/C21), and NO transfusion correctness/license framework (C51)** — closed by routing, not
  silent assumption.
