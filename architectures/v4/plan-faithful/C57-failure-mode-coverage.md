# C57 — Failure-mode coverage map & residual-risk register  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C57-failure-mode-coverage.md`](../spec/C57-failure-mode-coverage.md)
> Track: canonical   Status: sweep-1

C57 is a **documentation artifact** (a register/coverage-map), **not running code** — so this is an
**authoring + editorial-integrity** plan, not a software build. The deliverable is a single capstone page
with three tables (coverage map / license-hygiene view / residual-register) plus the honesty invariants that
govern them. The genuine work is **(a)** assembling the corrected 61-mode map (add F15, single status per
mode, counts reconcile to 61, defects shown), **(b)** aggregating C51's license dispositions, and **(c)**
pulling the run's residuals into one honest register with every "Addressed-on-an-unbuilt-mechanism" caveat
attached. C57 is **finalized last** (Batch 5) because it consumes the whole corpus; the dominant risk is
**over-build** (a coverage-enforcement engine / SBOM scanner — DROPPED) and the second is **staleness** (it
trails its owning components). No CI gate, no service, no scanner: hand-maintained under git review.

## 1. Work breakdown

Sizes: S (≤½ day editorial), M (~1–2 days — walks the full corpus). C57 has **no code tasks**; every task is
authoring/reconciliation that *reads* the finished corpus and *records* it.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** | **Freeze the register structure + honesty invariants** — three tables (coverage map / license-hygiene / residual-register), the closed status enum {addressed,partial,gap,caution}, and the §3 invariants (every mode once; single status; counts reconcile to 61; no bare "Addressed"; gaps/cautions named; register-not-resolve; hand-maintained-not-enforced). (Spec §3, §4.1) | S | — |
| **T2** | **Build the corrected 61-mode coverage map** — one row per F1–F61: mechanism + single status + owning C-ID + one-line residual. Walk F-MODE-COVERAGE §1–§9 and each component's spec §6. (Spec §3.1) | M | T1; all component specs' §6 |
| **T3** | **Apply + show the G38/G39/G40 corrections** — add F15 (status TBD, OQ-C57-1); resolve F32/F35/F47 to one status + one owner (Partial+Caution → `caution`, partial noted in residual); re-tally per-status counts to **sum to 61** and **show the arithmetic** (Reading A). (Spec §4.3, §8.1–§8.3) | M | T2 |
| **T4** | **Aggregate the license-hygiene view (C51)** — per (component, exemplar): license fact + `verified?` + `transfusion_mode`, sourced from C51's dispositions over the README:285–306 census; flag any code-port from an unverified/restrictive exemplar. Aggregation only — **no SBOM scanner**. (Spec §3.2, §8.7; C51:OQ-C51-4) | S | T1; C51 dispositions |
| **T5** | **Assemble the residual/caution register** — the 4 cautions (F52/F35/F25/F47); XC-8/D-18 exposure window; prevent-vs-detect (C43/C34); F54/G35 objective-drift audit (**homed at C57, registered UNBUILT**); D-1/FE-1 same-family-judge bias; C49/G19 unsolved replay; FE-1..FE-5 deferrals — each with owner + the caveat that must travel. (Spec §3.3, §6, §8.8) | M | T1; review-log + FE-doc |
| **T6** | **Wire the "no bare Addressed" linkage** — every "Addressed" resting on an unbuilt (twins/C44/C49) or detection-only (XC-8) mechanism links its map-row residual to the register entry (F12/F44/F56 → G31 exposure-window). The honesty discipline made structural. (Spec §3.4, §8.4) | S | T2, T5 |
| **T7** | **Write the 9-gap register block (register-not-resolve)** — G31/G32/G33/G34/G35/G38/G39/G40/G44 each as status + owner + residual **as the run left it**; assert NO resolution not built (esp. G35/F54 = registered unbuilt). (Spec §6) | S | T2, T5 |
| **T8** | **Editorial-integrity self-check + over-build/scope guard** — verify the 10 acceptance criteria (§8): 61 rows incl. F15, single status, counts reconcile-and-shown, no bare Addressed, gaps/cautions named, 9 gaps registered-not-resolved, license aggregated, residuals carried, **no CI gate/engine/scanner**, **not** the repo-level `failure-modes.md`. | S | T2–T7 |
| **T9** | **Resolve / carry the OQs** — OQ-C57-1 (F15 definition ← v3 catalog), -2 (snapshot vs living-doc), -3 (**top** — does F54 audit get a real owner or stay an unbuilt residual?), -4 (re-tally editorial vs per-owner freeze), -5 (integrator-rename vs C57-register for G01/G44/namespace). Record in review-log with owners. | S | T3, T5, T7 |

## 2. Dependency graph

```
ALL component specs §6 ─┐
F-MODE-COVERAGE §1–9  ──┤
                        ▼
        T1 (structure + invariants) ─► T2 (61-mode map) ─► T3 (G38/39/40 corrections, show arithmetic)
                        │                     │
C51 dispositions ──► T4 (license view)        ├──────────► T6 (no-bare-Addressed linkage) ─┐
review-log + FE-doc ► T5 (residual register) ─┘                                            │
                        │                     └──────────► T7 (9-gap register block) ──────┤
                        └──────────────────────────────────────────────────────────────────► T8 (integrity check) ─► T9 (OQs)
```

- **Critical path:** T1 → T2 → T3 (the corrected map is the load-bearing deliverable; G38/G39/G40 are the
  defects C57 exists to fix). T5 (residual register) runs in parallel and joins at T6/T7.
- **Upstream blockers (the whole corpus):** T2 needs **every component's spec §6** finished (C57 is Batch 5,
  finalized last — inventory). T4 needs **C51**'s per-component license dispositions. T5 needs the
  **review-log** residuals + **FE-doc** deferrals. None of these are *code* dependencies — they are
  *finished-corpus* dependencies.
- **Downstream consumers:** the **human reader** (operator / integrator / reviewer) doing go/no-go, security
  risk-tolerance (D-18 confirmation), or audit. No machine consumer; C57 unblocks a *decision*, not a build.

## 3. Parallelization

- **Three tables, three workstreams (after T1).** The coverage map (T2/T3), the license-hygiene view (T4),
  and the residual register (T5) are **disjoint** and can be authored concurrently once T1 freezes the
  structure + invariants. They reconverge only at T6 (linkage) and T8 (integrity check).
- **The map and the register are the two long poles** (both M, both walk the corpus); start them together.
  T4 (license aggregation) is independent and short.
- **The 9-gap block (T7) parallels the residual register (T5)** — both read the same sources (review-log +
  the gap register); author together.
- **No cross-component code parallelism** (C57 builds nothing); the parallelism is *editorial* — different
  authors can own different tables. The one serial join is T6 (needs both T2 and T5) → T8 (needs all).

## 4. Interfaces-first / contract milestones

C57 has no machine interface to freeze; its "contracts" are the **register shape + the honesty invariants**
the human reader and the upstream components rely on (e.g. C43's spec routes its G31 caveat *to C57* — that
seam is the residual-register row format).

| Milestone | Freezes | Unblocks |
|---|---|---|
| **M1 (earliest, load-bearing)** | Register structure + honesty invariants (T1) — three tables, closed status enum, "every mode once / single status / counts reconcile / no bare Addressed / register-not-resolve" | T2/T4/T5 can be authored in parallel against a fixed shape; upstream components know *what to hand C57* (e.g. C43 hands the G31 caveat in the residual-register row format) |
| **M2** | The G38/G39/G40 correction rules (T3) — add F15; one status/one owner per mode; tie-break Partial+Caution → `caution`; counts sum to 61, shown | the corrected coverage base is trustworthy + derivable (no re-import of G39) |
| **M3** | The residual-register row format (T5) — `residual-id · description · owner · travelling caveat` | every component routing a residual *to C57* (C43→G31, C51→license, C39/C56→F54) has a target shape |
| **M4** | The "no bare Addressed" linkage rule (T6) | the security-honesty claim is structural — no consumer can lift an "Addressed" without its caveat |

Freeze **M1 first**: it is the discipline the whole capstone rests on, and it is what lets upstream
components route their residuals to C57 in a known shape. M3 is the seam C43/C51/C39/C56 already point at.

## 5. Risks & de-risking order

1. **(Highest — the bar) Over-build into a coverage-enforcement engine.** The temptation is to make C57 a
   *running* system: a CI gate that fails the build on an unmapped mode, an automated license/SBOM scanner, a
   "residual-risk service" that polls components, or a coverage-enforcement mechanism. **All DROPPED** — none
   is a capability tied to a 12-principle; it is a document doing its job "better" in a non-principle way.
   De-risk by keeping C57 a **hand-maintained Markdown artifact under git review** (like the C51 census it
   aggregates) and checking the §8.9 no-over-build criterion. **When in doubt, DROP** (this is the dominant
   failure mode for a capstone register).
2. **(High) Register-not-resolve discipline slips into claimed-resolution.** The 9 gaps must be **registered
   as the run left them**, not quietly upgraded — especially **G35/F54** (the objective-drift audit is
   **unbuilt**; C57 is its *home*, not its *builder*) and **G31** (lethal-trifecta is "Addressed on paper"
   until twins land). De-risk by making every gap row state status + owner + residual verbatim from the
   source, and by registering F54 explicitly as **unbuilt** (OQ-C57-3). The failure here is a *dishonest
   capstone* — the one thing C57 exists to prevent.
3. **(High) Inheriting F-MODE-COVERAGE's defects (G38/G39/G40).** A capstone that re-imports the missing
   F15, the unreconciled 59≠61 counts, or the F32/F35/F47 double-statuses is worse than none. De-risk via
   T3's **Reading A re-tally** (fresh per-row count over all 61, single-status, arithmetic shown) — do **not**
   adopt the admittedly-unshown 24/20/11/4 headline. Spike T3 early against the finished §6 statuses.
4. **(Medium) Staleness — C57 trails its owners.** Because C57 is finalized last and statuses change in
   their owners (C44 twins shrink the G31 caveat; C49 replay residual moves), the page goes stale. De-risk by
   treating C57 as a **point-in-time snapshot re-authored at integration milestones** (OQ-C57-2), **not** an
   auto-syncing live view (that would be the dropped engine). Date it; name the integration milestone it
   reflects.
5. **(Medium) F15 has no recoverable definition.** T2/T3 add the F15 row to fix the structural drop (G38),
   but its *status* can't be set without the v3 catalog (`architectures/v3/failure-modes-v3.md`, OQ-C57-1).
   De-risk by adding the row with status honestly **TBD** rather than guessing — and flag it as the cheapest
   OQ to retire (read one v3 doc).
6. **(Low) Scope-bleed into the repo-level `failure-modes.md`.** C57 is the **v4-internal** register over
   F1–F61; the repo-level doc is the `0N-*` catalog. De-risk by the §8.10 criterion: C57 does not touch,
   mirror, or supersede it.

## 6. Definition of done

**Per-task:** T1 done when the three-table structure + the §3 invariants are frozen; T2 done when all 61
modes have a row sourced from the corpus; T3 done when F15 is added, F32/F35/F47 resolve to one status/owner
each, and the counts **sum to 61 with the arithmetic shown**; T4 done when every factory-built component has
a C51-sourced license disposition (no scanner); T5 done when every run-wide residual is in the register with
owner + travelling caveat; T6 done when every unbuilt/detection-only "Addressed" links to its residual; T7
done when all 9 gaps are registered (not resolved); T8 done when the 10 acceptance criteria pass; T9 done
when the 5 OQs are in review-log with owners.

**Per-component (tied to spec §8 acceptance criteria):**
- The coverage map has **exactly 61 rows including F15** (§8.1); every mode carries **one status + one
  owner** (§8.2); the counts **reconcile to 61 and the arithmetic is shown** (§8.3).
- **No bare "Addressed"**: every unbuilt/detection-only "Addressed" carries its caveat; F12/F44/F56 link to
  the G31 exposure-window entry (§8.4). Every gap and caution is named with its residual (§8.5).
- The **9 assigned gaps are registered, not resolved** (§8.6) — G35/F54 registered **unbuilt + homed at
  C57** (not claimed-built); G38/G39/G40 corrected in the register structure with the fix shown.
- The **license-hygiene view** aggregates C51's dispositions over the README census; unverified/restrictive
  code-ports flagged (§8.7). The **run-wide residuals** (XC-8/D-18, prevent-vs-detect, F54/G35, D-1/FE-1,
  C49/G19, FE-1..FE-5) are all carried with owner + caveat (§8.8).
- **No over-build:** no CI gate, no coverage-enforcement engine, no automated license/SBOM scanner, no
  residual-risk service — a hand-maintained Markdown artifact (§8.9). C57 does **not** touch the repo-level
  `architectures/failure-modes.md` (§8.10).
- All five OQs are in review-log with owners (OQ-C57-1 F15-def → v3 catalog; OQ-C57-2 snapshot-vs-living →
  integrator; **OQ-C57-3 F54-audit-owner → orchestrator, top**; OQ-C57-4 re-tally-scope → C57/owners;
  OQ-C57-5 integrator-rename-vs-register → integrator).
