# C30 — Scenario Authoring & Store (read-isolation)  (Build Plan, canonical track)

> Source / Spec ref: spec/C30-scenario-store.md
> Sources cited in spec: README §"Principle 5" (L164–177), §Phase 2 (L417–442), §Part 7 (L500, L526, L499);
> AI-CONTEXT §1.3 (L35), §6.2 (L294–305), §7 (L373), §11 (L467), §13.3 (L582–608), §12 (L512–513), §15.2
> (L638), §16.4 (L698); F-MODE-COVERAGE §1 (F1/F9/F28), §6 (F55); component-inventory C30 row (deps C17,
> C42; gaps G10, G21, G28; foundational); review-log D-1, D-2, D-6, D-13, D-14; spec/C42-rig-partitioning.md;
> spec/C17-tool-node-abstraction.md.

## 1. Work breakdown

C30 is *adoption (Inspect AI DSL) + a small provider pack + a held-out storage layout* — not authorship of a
DSL or of isolation enforcement, and **not** custom signing (DEFERRED → FE-3/G37 per D-14; Phase-0/2
tamper-evidence is the content-addressed git repo, AI-CONTEXT:236/404). Per D-13, **C30 stores/authors in the
isolated rig**; **C42 provides** the partition and **C34 enforces+audits**. The work is: adopt + pin Inspect
AI, build the `[[service]] type="inspect_ai"` provider pack (as a C17 tool node), establish the separate
scenario repo + `scenarios/<component>/` layout bound to the `scenarios` partition (the git commit history
being the corpus's provenance + tamper-evidence record), and **publish the scenario-path feed C34 audits
against** — then freeze the corpus/layout/feed seams the evaluation tier (C31, C32, C34) builds on.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Adopt & pin Inspect AI | Obtain Inspect AI from `github.com/UKGovernmentBEIS/inspect_ai` (MIT; AI-CONTEXT §15.2); pick + record a version/commit pin. Confirm the Task DSL is the authoring format (AC-1; README:170). | S | — |
| **T2** Scenario-provider pack | Build the small Gas City pack exposing Inspect AI as a scenario provider — the `[[service]] type="inspect_ai"` block + the `inspect_eval` `[[tool]]` subprocess (README:424; AI-CONTEXT §13.3), **wrapped as a C17 tool node** over the C02 ABI. | M | T1, C17/C02 standing |
| **T3** Separate repo + layout | Stand up the **separate scenario git repo** with `scenarios/<component>/` layout (README:171/425; AI-CONTEXT §16.4), filesystem perms read-only-from-implementer. Assert AC-2/AC-6/AC-8 (separate-repo holdout, path-resolvable, versioned). | M | — |
| **T4** Bind to `scenarios` partition / `scenario_authoring` rig | Bind authoring to the `scenario_authoring` rig and storage to the `scenarios` partition C42 provides (AC-3/AC-4; AI-CONTEXT §13.3). **Placement only — enforcement is C34, partition def is C42 (D-13).** | S | T3, **C42** partition published |
| **T5** Corpus integrity via git revision (signing DEFERRED → FE-3/G37) | Establish that each scenario's **git commit identity** is its Phase-0/2 tamper-evidence/provenance record (AC-5; verified by C34/baselining, F7; AI-CONTEXT:236/404). **Custom cryptographic signing is NOT built — it is DEFERRED → FE-3, blocked on G37 (D-14); a plaintext key collapses the assurance (XC-6).** | S | T3 |
| **T6** Scenario-path feed to C34 | Publish the corpus layout/paths (+ git-revision identity) as the feed **C34** enforces+audits actual implementer reads against (AC-7; README:173). **C30 publishes; C34 enforces+audits (D-13).** | M | T3, T4 |
| **T7** Freeze corpus/layout/feed seams | Enumerate + freeze I1–I7 (Task DSL, repo+layout, provider pack, partition/rig binding, git-revision integrity, path-feed, corpus retrieval) + the §4.5 scenario-record schema (OQ-1 RESOLVED) so C31/C32/C34 build against the frozen schema. *(No signature-format seam — signing DEFERRED → FE-3.)* | M | T2–T6 |
| **T8** Scenario-store conformance pack | Build the conformance pack (§8 test strategy) asserting AC-C30-01…AC-C30-08 + E-code negative paths (E-C30-01…E-C30-07); gate C31/C32/C34 on AC-C30-04 + AC-C30-07 green. | M | T7 |

## 2. Dependency graph

- **Upstream of C30:** **C17** (the tool-node abstraction the Inspect AI provider pack is wrapped over —
  spec §2; needed for T2) and **C42** (the `scenario_authoring` rig + `scenarios` partition C30 binds to —
  needed for T4; **C42 provides, C30 does not enforce**, D-13). Inspect AI (external OSS, T1) is the DSL.
  C03 (secrets) is *not* a prereq and not on T5's path: T5 uses the content-addressed git repo (no key);
  **cryptographic signing is DEFERRED → FE-3, blocked on G37/C03 (D-14)** — out of C30's sweep-1 scope.
- **Critical path:** **T1 → T2** (adopt + provider pack) and **T3 → T4** (repo + partition binding) are the
  two gating chains; they converge at **T6** (the C34 path-feed) and **T7** (seam freeze). T4's
  partition-placement (AC-4) is the load-bearing correctness check — it makes the holdout invariant
  `scenarios ∉ read_partition(worker)` (C42) and C34's audit well-defined. C30 does **not** gate on any
  enforcement work (that is C34's, downstream).
- **Downstream gated by T7 (seam freeze):** **C31** (runner → I1 Task DSL + I7 corpus retrieval; also needs
  the Inspect-AI session-id adapter, G25 — *C31's* concern), **C32** (judge → I7 corpus; same-provider per
  D-1), **C34** (holdout enforcement+audit → I6 path-feed + I5 git-revision integrity; **enforcement is C34**), and the
  corpus consumers **C35/C53/C55** (override rules / bootstrap validation / methodology loop → I7).

## 3. Parallelization

C30 fans out into two near-independent storage/provider tracks that converge late:
- **Provider track (T1→T2):** adopt+pin Inspect AI, build the `[[service]] type="inspect_ai"` pack as a C17
  tool node. Independent of the repo track until T7.
- **Storage track (T3→T4→T5):** stand up the separate repo + layout, bind to the `scenarios` partition,
  establish git-revision integrity (T5). T5 (git-revision integrity) and T4 (partition binding) are
  independent of each other once T3 (repo) exists.
- **Convergence (T6, T7):** the C34 path-feed (T6) needs both the layout (T3/T4) and the git-revision identity (T5); the
  seam freeze (T7) needs all of T2–T6.
- **Cross-component:** **C31's** runner design (against the Inspect AI Task DSL + I7) and **C34's**
  enforcement/audit design (against the I6 path-feed + I5 git-revision integrity) can proceed in parallel with C30's
  T3–T6 against the T7-frozen seams + the §4 scenario-record stub — *before* the corpus is populated, since
  they build against stubs. **C42's** partition publication (its M-seam) can proceed fully in parallel with
  C30's provider track.

## 4. Interfaces-first / contract milestones

Freeze early (T7) so dependents build against stubs:
- **M1 — Inspect AI version pin published (after T1):** exact Inspect AI version/commit + "Task DSL is the
  authoring format", so every downstream spec pins the same DSL.
- **M2 — Corpus layout frozen (T3/T7):** the separate-repo + `scenarios/<component>/` path grammar (I2) +
  the corpus retrieval seam (I7) → unblocks **C31** (runner) and **C32** (judge).
- **M3 — Partition/rig binding frozen (T4/T7):** the `scenario_authoring` rig + `scenarios` partition
  binding (I4) — **C42 provides the partition; C30 binds; C34 enforces (D-13)** → confirms the holdout
  placement C34/C42 depend on.
- **M4 — Scenario-path feed + git-revision integrity frozen (T6/T5/T7):** the path/label feed (I6) +
  the git-revision identity (I5) → unblocks **C34** (enforcement+audit) and the F7 baselining path.
  *Cryptographic signing is **not** in this (or any sweep-2) freeze — DEFERRED → FE-3/G37 per D-14.*

## 5. Risks & de-risking order

Retire in this order (highest uncertainty first):
1. **D-13 storage/enforcement seam (top).** The single most load-bearing clarity item: C30 *stores/authors*
   in the isolated rig, **C42 provides** the partition, **C34 enforces+audits**. De-risk by freezing the
   I6 path-feed (T6) and confirming **no enforcement obligation leaks onto C30** (OQ-2). If this seam is
   wrong, C30 either over-builds enforcement (violates D-13) or C34 has nothing to audit against.
2. **Holdout placement correctness (AC-2/AC-3/AC-4).** The corpus *must* land in the separate repo +
   `scenarios` partition / `scenario_authoring` rig so the holdout invariant (C42) and C34's audit are
   well-defined. Spike T3→T4 early. *Per D-1 there is no model-family fallback, so correct placement is the
   load-bearing input to the whole holdout claim* — but enforcement is C34's, not C30's.
3. **Inspect AI wrap + impedance (T2).** "The harder parts are the Inspect AI wrap and the scenario
   isolation policy" (README:442). The *wrap* (provider pack as a C17 tool node) is C30's; the Inspect-AI
   **session-id ↔ Gas City session-id** adapter (AI-CONTEXT §12 L512) is a *runner* (C31) risk, **not
   C30's** — flag the boundary so it doesn't land here.
4. **Signing deferral (FE-3/G37) — confirm, don't build.** Cryptographic signing needs a key; v4 has no
   secrets story (plaintext `city.toml`/env), so a key collapses the assurance (XC-6). Per **D-14** this is
   already settled **optional/deferred → FE-3 (blocked on G37)**; C30's Phase-0/2 corpus integrity is the
   content-addressed git revision (no key, no new uncertainty). Lowest "uncertainty" item — it is a settled
   deferral, not a build risk. *(G37 (secrets) ≠ FE-3 (signing) per D-14.)*
5. **G10/G28 — honest boundary + mechanism authority.** State that "held-out" is a policy intent (C42
   partition) verified after the fact (C34 audit), not a C30 guarantee (G10); and name C30's two
   storage-side mechanisms (separate repo + on-disk layout) with the *authoritative* partition policy being
   C42's and OPA deferred to C34 (G28). Low uncertainty — a wording/ownership discipline, retired by the §6
   resolutions.

## 6. Definition of done

**Per-component DoD (sweep-1 altitude):**
- Inspect AI is adopted + version-pinned; scenarios are authored as **Inspect AI `Task`** artifacts with no
  bespoke DSL (AC-1), exposed via the `[[service]] type="inspect_ai"` provider pack wrapped as a C17 tool
  node (T2).
- The **separate scenario git repo** stands up with the `scenarios/<component>/` layout, read-only-from-
  implementer perms, bound to the **`scenarios` partition / `scenario_authoring` rig** C42 provides; the
  corpus is versioned + append-growing, with **tamper-evidence + provenance from the content-addressed git
  commit history** (custom signing DEFERRED → FE-3/G37, D-14). (AC-2…AC-6, AC-8.) **Resolves
  G10 (honest held-out boundary) and the storage-side of G28 (separate repo + layout, with C42 partition
  authoritative, OPA deferred to C34); routes G21 enforcement to C34 and the broad-tool-access bound to
  C43 (D-13).**
- The **scenario-path feed** (+ git-revision identity) is published so **C34** can enforce+audit actual implementer
  reads against the corpus (AC-7) — **C30 publishes; C34 enforces+audits (D-13); C30 writes no enforcement.**
- The corpus/layout/feed seams (I1–I7) + the §4 scenario-record [FAITHFUL-FILL] are frozen + published so
  C31/C32/C34 build against stubs (M1–M4).

**Per-task DoD:** each Tn meets its mapped acceptance criterion (T1→AC-C30-01, T2→AC-C30-01/I3,
T3→AC-C30-02/AC-C30-06/AC-C30-08, T4→AC-C30-03/AC-C30-04, T5→AC-C30-05, T6→AC-C30-07, T7→M1–M4,
T8→conformance-pack-green) and marks the spec's OQs resolved (OQ-1/OQ-2/OQ-3/OQ-4 RESOLVED by Sweep-2).
**T4 (AC-C30-04: partition placement) + T6 (AC-C30-07: path-feed to C34) are the gating exit criteria** —
they make the holdout boundary well-defined and auditable; C34/C42 depend on them. **DoD explicitly excludes
enforcement/audit work (C34, D-13).** New seam: E-C30-04 handoff to C34 (C30↔C34 trigger contract) left
open for the C34 Sweep-2 author to specify the consumption mechanism.
