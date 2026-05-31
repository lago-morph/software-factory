# C57 — Failure-mode coverage map & residual-risk register  (Spec, canonical track)

> Source: F-MODE-COVERAGE.md (the whole doc — the 61-mode catalog F1–F61 with per-mode mechanism +
> status: §1 Layer-2/P5+P6, §2 Layer-3/P8+obs, §3 Layer-4/P11, §4 Layer-5/P7, §5 Layer-6/P12, §6
> foundational/Phases-0-1, §7 Phase-3+ gene-transfusion, §8 **Cautions** (F52/F35/F25/F47), §9 **Gaps**
> (F3/F5/F6/F13/F20/F21/F29/F30/F36/F49/F59), §10 summary-by-status counts, §11 strongest/weakest matches,
> §12 recommendations); README Part 5 "License census" (L285–306 — per-source SPDX + "Verify before
> adopting" gating) + Part 8 "the bets" (L508–512); component-inventory C57 row (subsystem Security &
> Governance; kind **cross-cutting**; "Canonical 61-mode → mechanism mapping (addressed/partial/gap/caution);
> **owns license hygiene + the honest residual/caution register**"; maps `A100, A102, A104, A109, A110-A169,
> B58, B74, B75-79`; **depends on C51, C43**; gaps **G31, G32, G33, G34, G35, G38, G39, G40, G44**;
> foundational: no; **Batch 5 — "finalized last … can only be finalized once all mechanisms exist"**);
> ambiguities-and-gaps **G31/G32/G33/G34/G35** (cross-cutting risks) + **G38/G39/G40** (the coverage-doc's own
> count/cross-reference defects) + **G44** (El Kaim 10-of-11 / 12-principle bookkeeping); FUTURE-ENHANCEMENTS
> **FE-1..FE-5** (the deferred-by-decision register); review-log **XC-8** (Phase-0 capability enforcement is
> detection-only until C43 isolation lands — "prevention" claims are really detection), **D-18** (C43
> split-sequencing; the boundary-typing half pulls forward to a Phase-2 entry precondition, the twin half
> stays Phase-3c — the exposure window), **D-1** (same-provider judge for Phase 0 — cross-family is FE-1, so
> F1/F27/F46 "Addressed" and F48 "Partial" carry the same-family-bias residual), the prevent-vs-detect
> cross-component OQ (C43:OQ-C43-1 ≡ C34:OQ-C34-1), **C51:OQ-C51-4** (license census authority shared with
> C57 — C57 owns the census aggregation + verification workflow), **C52:OQ6 / C56:OQ-3 / C39:OQ3** (the F54
> goal-subversion / objective-drift audit register is homed at **C57**, unbuilt, Batch 5), **C54:OQ-1** (G01
> architecture-wide layer-vocabulary rename routes to integrator/C57), **C56:OQ-1** (G15 design-starvation
> constraint routes to C57 + review-log), and the run-wide residual on **C49** counterfactual replay (G19,
> "largely unsolved").
> Inventory ID: C57   Kind: cross-cutting (documentation artifact — a register/coverage-map, **not running
> code**)   Status: sweep-1
> Track: canonical

## 1. Purpose & responsibility

C57 is the **capstone artifact** of Software Factory v4: a **documentation register**, not a running
component. It is the **canonical 61-mode → v4-mechanism coverage map** (every catalogued failure mode F1–F61
mapped to the mechanism that addresses it, with a status of **addressed / partial / gap / caution**, the
**owning component**, and the **honest residual**), it **owns license hygiene** (the consolidated view of
C51's per-component license dispositions over the README:285–306 census), and it is the **honest
residual/caution register** that pulls the run's known residuals into one place so no "Addressed" status is
ever read without its caveat. C57 *consumes the whole corpus* — it is the integration ledger that can only
be finalized once every other mechanism exists (inventory: Batch 5, "finalized last").

The load-bearing word is **honest**. F-MODE-COVERAGE today is the v4 corpus's coverage claim, and it is
*defective in exactly the ways a coverage doc must not be*: it silently **drops F15** (G38 — 60 distinct
F-numbers, not 61), its **summary counts do not reconcile** with the rows (G39 — 24+20+11+4 = 59 ≠ 61), and
it **double-counts F32/F35/F47** across sections with **conflicting statuses** (G40 — a mode that is both
"Partial" and "Caution" has no single status). A capstone register that inherited those defects would be
worse than none. So C57's genuine deliverable is twofold: **(a) the register structure** — a single table
where every one of the 61 modes appears **exactly once** with a **single deterministic status**, an owning
component, and a one-line residual; and **(b) the honesty discipline** — every gap and caution is *named,
not hidden*; every "Addressed" that rests on an unbuilt mechanism (twins, C43, C49) carries its
exposure-window caveat; and the count/cross-reference defects (G38/G39/G40) are **corrected and the
correction shown**, not silently re-stated.

> [FAITHFUL-FILL] **C57 = a register/coverage-map DOCUMENT + the honesty discipline; NOT a
> coverage-enforcement engine.** Per the capability-for-principle bar, the over-build to flag and reject is a
> *running* coverage system: a CI gate that fails the build if a mode is unmapped, an automated SBOM/license
> scanner, a "residual-risk service" that polls components for live status, or a mechanism that *enforces*
> coverage. None of that is a capability tied to a 12-principle — it is a documentation artifact doing its
> job "better" in a non-principle way, which the bar **DROPS** (when in doubt, DROP). The genuine KEEP is the
> *artifact itself*: the mapping (every mode → mechanism/status/owner/residual, each mode once, single
> status), the **honesty discipline** (gaps/cautions named; unbuilt-mechanism caveats loud; the
> count/cross-reference defects fixed and the fix shown), and the **license-hygiene aggregation** (the
> consolidated per-component view of C51's dispositions over the README census). C57 is *maintained by hand
> under git review* — the same way the license census it aggregates already is (C51 §9: "not an automated
> SBOM tool"). It records; it does not run.

**Responsibilities**
- **Own the canonical 61-mode coverage map (the register structure, G38/G39/G40).** A single table over
  the **full F1–F61 catalog** where each mode appears **exactly once** with: the v4 mechanism, a **single**
  status ∈ {addressed, partial, gap, caution}, the **owning component** (C-ID), and a one-line **residual**.
  This is the corrected successor to F-MODE-COVERAGE: it **adds the missing F15** (G38), **reconciles the
  counts to 61** (G39), and **resolves the F32/F35/F47 double-counts to one status each** (G40) — and shows
  the reconciliation arithmetic so the totals are derivable from the rows.
- **Own license hygiene (C51 aggregation, C51:OQ-C51-4).** The consolidated, hand-maintained view of every
  factory-built component's **license disposition** — per (component, exemplar): the license fact, the
  `verified?` flag, and the chosen `transfusion_mode` (code-port vs pattern-reimplement) — sourced from
  **C51**'s per-component records over the **README:285–306 census**. C57 owns the *census aggregation +
  verification-status view*; C51 owns the per-component decision and the build-blocking gate. (Confirmed
  C51:OQ-C51-4: C57 owns the census; adding an exemplar's license is a *pre-transfusion* step in C51; **no
  Phase-0 SBOM scanner**.)
- **Own the honest residual/caution register (the run-wide residuals).** The single home for the residuals
  surfaced across the whole run, each with its owning component and the caveat that must travel with it:
  the **4 cautions** (F52/F35/F25/F47 — modes v4's own design could *worsen*); the **XC-8 / D-18
  exposure window** (lethal-trifecta "Addressed" is detection-only until C43 isolation + C44 twins land —
  the most dangerous class is "Addressed on paper" for the period it is actually exposed); the
  **prevent-vs-detect** residual (C43:OQ-C43-1 ≡ C34:OQ-C34-1 — does the stack *prevent* at tool-call time or
  *detect* after); the **F54 / G35 objective-drift audit** (homed at C57 per C52:OQ6 / C56:OQ-3 / C39:OQ3 —
  **unbuilt, Batch 5**); the **same-family-judge bias** residual (D-1 / FE-1); the **C49 counterfactual-replay
  unsolved** residual (G19); and the **FE-1..FE-5** deferred-by-decision items.
- **Register the 9 assigned gaps honestly — register, do NOT resolve (G31/G32/G33/G34/G35/G38/G39/G40/G44).**
  For each, record the status, the owning component, and the residual exactly as the run left it. C57 is the
  *honest ledger* of these gaps, not their fix (§6).
- **State the run-wide honesty invariants (§3).** The rules every consumer relies on: every mode mapped
  once; single status per mode; no bare "Addressed" without its residual; counts reconcile to 61; license
  hygiene is current; this is a hand-maintained artifact, not an enforcement engine.

**Explicitly NOT**
- **NOT a coverage-enforcement engine / CI gate (DROPPED, bar).** C57 does not *fail a build* when a mode is
  unmapped, does not *enforce* that every component declares its F-modes, and does not run as a service. It
  is a document. The enforcement of any individual mode's mechanism is that mode's **owning component**
  (e.g. C43 enforces the boundary typing, C51 enforces the license-mode gate); C57 *records* their status.
- **NOT an automated license/SBOM scanner (DROPPED, C51 §9).** License hygiene is the **aggregation** of
  C51's hand-maintained dispositions over the README census; it is not an SPDX-parsing tool, a dependency
  crawler, or a CVE feed. (C51:OQ-C51-4: "no Phase-0 SBOM scanner".)
- **NOT the resolver of the 9 gaps.** C57 **registers** G31/G32/G33/G34/G35/G38/G39/G40/G44 with status +
  owner + residual; it does **not** build twins (C44), a cost model (the G32 owners), a stack-degradation
  design (the G33 owners), a throughput scheduler (FE-4), the F54 audit-pack mechanism (unbuilt), or fix the
  El Kaim bookkeeping (G44 is a corpus-arithmetic note). Registering ≠ resolving (§6).
- **NOT the repo-level `architectures/failure-modes.md`.** That is a *different artifact* — the failure-mode
  catalog for the `0N-*` repo-level architecture alternatives. C57 is the **v4-internal** residual-risk
  register over the v4 F1–F61 catalog (F-MODE-COVERAGE). C57 does not touch, mirror, or supersede the
  repo-level doc. (Per the BUILDER brief SCOPE clause.)
- **NOT the owning component of any mode it maps.** C57 names the owner (C01–C56) for every addressed/partial
  mode and the residual for every gap/caution; it does not *implement* any mechanism. It is the ledger, not
  the work.
- **NOT a model-floor / autonomy / security mechanism itself.** The F31 floor is C29/C28's; the L4/L5
  autonomy posture is C56's; the lethal-trifecta bound is C43/C44's. C57 records that these exist and their
  residual; it adds no new control.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (declared dep) | **C51** Gene-transfusion discipline | C51 supplies the **per-component license disposition** (per-exemplar license fact + `verified?` + `transfusion_mode`) that C57 **aggregates** into the license-hygiene view. C51 owns the per-build decision + the build-blocking gate; C57 owns the consolidated census view + verification status. C57 `depends on C51`. (C51 §1/§9; C51:OQ-C51-4.) |
| Upstream (declared dep) | **C43** Isolation & lethal-trifecta boundary | C43 supplies the **F12/F44/F56/F33/F51 mechanism** (deterministic boundary typing + twin-by-default routing) **and** the **G31 exposure-window residual** (aspirational-until-C44-twins; XC-8/D-18). C57 records both — the mechanism *and* the caveat. C57 `depends on C43`. (C43 §1 names C57 as the residual recorder.) |
| Upstream (the whole corpus) | **C01–C56** (every component) + **F-MODE-COVERAGE** + **README/AI-CONTEXT** | C57 "consumes the WHOLE corpus" (brief). Every mode's owning component, every per-component OQ that became a residual, and the F1–F61 catalog itself feed the register. C57 is the integration ledger; these are **not** declared inventory edges (the inventory declares only C51 + C43) but are the de-facto inputs — > [FAITHFUL-FILL]: the inventory critical-path note already calls C57 "the integration/residual-risk ledger, finalized last" that "touches nearly everything". |
| Upstream (deferral register) | **FUTURE-ENHANCEMENTS.md** (FE-1..FE-5) | The deferred-by-decision items (cross-family judge, substrate-portability contracts, graduated signing, multi-seat automation, enumerated DoD) are residuals-by-choice; C57 records them as deferred (not gap, not addressed) with their revisit trigger. |
| Downstream (the human reader) | **Operator / integrator / reviewer** | C57's consumer is a **person** doing go/no-go, security risk-tolerance, or audit. C57 is the single page they read to know "what is actually covered, what is paper, what is deferred, and where the residual lives." No machine consumer; no API. |

C57 is **not foundational** (inventory: no) and is in **Batch 5** — built **last**, because (inventory
critical-path) it "can only be finalized once all mechanisms exist." It is a **cross-cutting load-bearer that
touches nearly everything but is not on a single linear path**: it does not gate any build, but it is the
artifact the whole-system **honesty** claim rests on — if C57 inherits F-MODE-COVERAGE's count/double-count
defects, the system's coverage claim is unfalsifiable. C57's correctness is *editorial integrity*, not
runtime behavior.

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described** as *document sections + invariants* (C57 is an artifact, so its
"interfaces" are the register's shape and the honesty rules its readers rely on). The concrete table schema
(column set, status enum encoding), the license-hygiene aggregation format, and the residual-register row
format are sweep-2 deliverables.

1. **The 61-mode coverage map (the register structure).** A single table over the full F1–F61 catalog, one
   **row per mode**, columns: `F-id` · `name` · `mechanism` · `status ∈ {addressed, partial, gap, caution}`
   · `owning component (C-ID)` · `residual (one line)`. **Every mode appears exactly once with exactly one
   status.** This is the corrected successor to F-MODE-COVERAGE §1–§9: the missing **F15 is added** (G38);
   the **F32/F35/F47 double-counts are resolved to one status each** (G40); the **counts reconcile to 61**
   (G39, §4.3). Read by a person; no machine contract.
2. **License-hygiene view (C51 aggregation).** A consolidated, hand-maintained table: per factory-built
   component, the exemplar(s), the license fact, the `verified?` flag, and the chosen `transfusion_mode`
   (code-port / pattern-reimplement) — sourced from C51's per-component records over the README:285–306
   census. C57 owns the *aggregate + verification-status view*; the per-build decision + gate is C51's.
3. **Residual/caution register.** A table of the run-wide residuals, columns: `residual-id` · `description`
   · `owning component / decision-ref` · `caveat that must travel with the status`. Holds the 4 cautions
   (F52/F35/F25/F47), the XC-8/D-18 exposure window, the prevent-vs-detect residual, the F54/G35 objective-
   drift audit (unbuilt), the D-1/FE-1 same-family-judge bias, the C49/G19 unsolved-replay residual, and the
   FE-1..FE-5 deferrals.
4. **The "Addressed-with-caveat" linkage.** For each "Addressed" status that rests on an **unbuilt or
   detection-only** mechanism (F12/F44/F56 → twins+C43; the Phase-0 capability controls → XC-8 detection-
   only), the register row's `residual` column **links to** the residual-register entry, so a reader can
   never lift the bare status. This linkage *is* the honesty discipline made structural.
5. **Reconciliation note (G39).** A short shown-arithmetic note: how the per-status counts sum to 61 after
   adding F15 and de-duplicating F32/F35/F47. The summary is **derivable from the rows**, not asserted.

**Invariants (the honesty discipline — load-bearing)**
- **Total coverage.** Every mode in the **full F1–F61 catalog** appears in the map **exactly once**. A
  catalog of 61 has 61 rows. (Fixes G38 — F15 is present.)
- **Single status.** Each mode carries **exactly one** status ∈ {addressed, partial, gap, caution}. No mode
  is both "Partial" and "Caution" (fixes G40 — F35/F47 resolved to one status each; F32 to one owner).
- **Counts reconcile.** The per-status counts **sum to 61** and the summary is **derivable from the rows**,
  with the reconciliation shown (fixes G39).
- **No bare "Addressed".** An "Addressed" status whose mechanism is **unbuilt** (twins, C44, C49) or
  **detection-only** (XC-8) **must** carry its exposure-window/prevent-vs-detect caveat in the `residual`
  column. A status without its required caveat is an invalid register entry. (This is the run's loudest
  honesty rule — it is why C43's spec routes the G31 caveat *to C57*.)
- **Gaps and cautions named, not hidden.** Every gap (status `gap`) and caution (status `caution`) is in the
  register with its residual; none is silently dropped or upgraded. (The capstone honesty bar.)
- **Register, not resolve (for the 9 assigned gaps).** C57's entry for G31/G32/G33/G34/G35/G38/G39/G40/G44
  records status + owner + residual **as the run left it**; C57 does not assert a resolution it did not
  build. (§6.)
- **License hygiene current.** Every factory-built component in the license-hygiene view has a license
  disposition sourced from C51; a component that code-ported from an unverified/restrictive exemplar is a
  **flagged residual** (it should have been blocked by C51's gate — C57 records if it was not). (G30 surface
  shared with C51.)
- **Hand-maintained, not enforced (bar).** C57 is a document under git review; it contains **no CI gate, no
  scanner, no service, no coverage-enforcement engine**. Updated by a human when a mechanism or its status
  changes.

## 4. Data model / state

C57 owns **no instance state and no store**. It is a versioned Markdown artifact. Its "data model" is the
shape of its three tables + the closed status enum + the reconciliation rule. The underlying facts live in
their owners (mode statuses in each component's spec §6; license dispositions on C51's `factory_build`
beads; residuals in review-log / FE-doc); C57 is the **consolidated, human-readable view** of them.

### 4.1 Coverage status (the closed enum)

| Status | Meaning (from F-MODE-COVERAGE preamble legend, lines 6–9, verbatim intent) | Honesty rule |
|---|---|---|
| `addressed` | v4 has a concrete mechanism that mitigates the failure | must name the owning component; if the mechanism is unbuilt/detection-only, must carry the caveat (§3 invariant) |
| `partial` | v4 reduces but does not eliminate the failure | must state the residual (what remains) |
| `gap` | v4 has no mechanism; the failure stands | must state why (inherent / operator-side / systemic / deferred) |
| `caution` | v4's design choices could *worsen* this failure if not actively guarded | must state the required discipline + its owner |

> [FAITHFUL-FILL] **Status set = {`addressed`, `partial`, `gap`, `caution`}, taken verbatim from
> F-MODE-COVERAGE's preamble legend (lines 6–9; the doc has no numbered §0 — sections run §1–§12).** v4
> already defines exactly these four; C57 adopts the closed set unchanged so the
> map is a faithful successor. The single-status invariant (§3) is what makes the set *closed per mode* —
> the defect C57 fixes is that F-MODE-COVERAGE let three modes hold two statuses at once (G40), not the enum
> itself.

### 4.2 The three tables (named; concrete schemas → sweep-2)

- **Coverage map** — one row per F-id (§3.1).
- **License-hygiene view** — one row per (component, exemplar) (§3.2), aggregating C51.
- **Residual/caution register** — one row per residual (§3.3).

Concrete column encodings, the status-enum on-disk form, the C51→C57 aggregation field mapping, and the
residual-id scheme are **sweep-2**.

### 4.3 Count reconciliation (G38/G39/G40) — the corrected base

The faithful correction C57 applies to F-MODE-COVERAGE's §10 summary (which reads Addressed 24 / Partial 20
/ Gap 11 / Caution 4 = **59**, with F15 absent and F32/F35/F47 double-counted):

| Defect | F-MODE-COVERAGE state | C57 correction (sweep-1 policy; exact per-row tally → sweep-2) |
|---|---|---|
| **G38** F15 missing | 60 distinct F-numbers; F15 has no row | **Add F15** as a row with a single status + owner + residual (status TBD pending the F15 definition — itself an OQ, §9). The catalog is 61; the map has 61 rows. |
| **G39** counts ≠ 61 | 24+20+11+4 = 59 | After adding F15 and de-duplicating, **the per-status counts are recomputed to sum to 61** and the arithmetic is **shown** (derivable from rows). The headline percentages are recomputed against 61, not an unreconciled base. |
| **G40** F32/F35/F47 double-counted with conflicting status | F32 §2+§7; F35 §6/§7 "Partial" + §8 "Caution"; F47 §5 "Partial" + §8 "Caution" | **Each resolved to ONE status + ONE owner.** Faithful tie-break rule: a mode that is *both* reduced (Partial) *and* could-be-worsened (Caution) is recorded as **`caution`** with the partial-mechanism noted in its residual — because the *caution* is the load-bearing honest signal (the design could worsen it), and a single status is required (§3). F32's two mechanisms (P9 attribution + HMAC on mail bus) collapse to **one owner** (C41, attribution) with the HMAC noted as the FE-3-deferred secondary. (The exact resolved status per mode is recorded in the sweep-2 row tally; the *rule* is fixed here.) |

> [AMBIGUITY: G39/G40] **Is the corrected base derived by re-tallying every row (sweep-2), or by adopting
> F-MODE-COVERAGE's headline 24/20/11/4 and patching only the three defects?** Reading A (re-tally): the
> only honest base is a fresh per-row count over all 61 (incl. F15, single-status), since F-MODE-COVERAGE's
> own §10 admits "the arithmetic is never shown" (G39) — so the headline numbers are not trustworthy inputs.
> Reading B (patch the headline): cheaper, but it builds the capstone on a base the gap register calls
> unreconciled. **Pick: Reading A — re-tally over 61 with single-status, show the arithmetic.** The whole
> point of C57 is that the coverage claim becomes *derivable and honest*; adopting an admittedly-unshown
> total would re-import G39. Sweep-1 fixes the **rule** (add F15; one status per mode; tie-break Partial+
> Caution → caution; counts sum to 61, shown); the **exact resolved per-mode status table** is the sweep-2
> deliverable (it requires walking all 61 rows, which is below sweep-1 altitude). This is "register the
> defect + fix the rule now, tally at sweep-2", not "leave it broken."

### 4.4 Persistence & consistency

C57 holds **no state of its own**. The coverage statuses are owned by each mode's component (their spec §6);
the license dispositions are C51's bead facts; the residuals are review-log/FE-doc entries. C57's only
consistency requirement is the **honesty invariants** (§3): the map is a faithful, single-status,
fully-reconciled, caveat-complete *view* of those owned facts. Staleness is the operative risk — because
C57 is finalized last and maintained by hand, a status that changes in its owning component must be
propagated to C57 (an editorial discipline, not an automated sync — the sync-vs-snapshot question is
OQ-C57-2, §9).

## 5. Behavior

C57 has **no control loop and no runtime behavior** — it is a document. Its "behavior" is **editorial**, at
two moments:

- **Finalization (Batch 5, once per major integration).** When all mechanisms exist, C57 is authored/updated
  to reflect them: walk the F1–F61 catalog, record each mode's mechanism + single status + owner + residual;
  aggregate C51's license dispositions; pull the run's residuals into the register; apply the
  G38/G39/G40 corrections and show the reconciliation. The output is the consolidated capstone page.
- **Maintenance (on status change).** When a mode's status changes in its owning component (e.g. C44 twins
  ship and F12/F44/F56's exposure-window caveat can shrink; or C49's replay residual moves), the owner
  updates their spec and C57 is **edited by hand** to match. C57 does not poll, subscribe, or auto-derive;
  the propagation is a review-time editorial step (OQ-C57-2).

(No sequence/state diagrams — C57 is an artifact, not a process. The "flow" is authoring discipline, not a
runtime control loop.)

## 6. Failure modes & handling — the 9 assigned gaps (REGISTER, not resolve)

C57's relationship to its assigned gaps is **register, not resolve**: for each, C57 records the status, the
owning component, and the residual **as the run left it**. C57 does not build the missing mechanism. The
table below is the sweep-1 register entry for each.

| Gap | One-line statement | C57 register entry (status · owner · residual) |
|---|---|---|
| **G31** (blocker) | Lethal-trifecta "Addressed" but the mechanism (twins) is unbuilt and last; Phase 0→3b the factory runs with Bash/net/fs and no twin isolation. | **status `addressed`-with-caveat · owner C43 (+C44 twins)** · *Residual:* the bound is **aspirational until C44 twins ship**; D-18 pulls C43's boundary-typing half forward to a Phase-2 entry precondition but the twin half stays Phase-3c, so a real exposure window remains. **This is the run's loudest "no bare Addressed" entry** — F12/F44/F56's map rows link here. **Register-not-resolve:** C57 records the window; C43/C44 close it. |
| **G32** (major) | Cost is essentially unmodeled; "cost-per-satisfaction" is the headline P12 metric with no cost model for scenario runs / multi-judge / A/B replays / embeddings / second-family judge. | **status `gap` (cost model) · owner C46 (meta-metrics, defines the cost model) / C29 (model-floor routing)** · *Residual:* no token-budget math anywhere in the corpus; "$200/month Max" is the only figure. The second-family-judge token cost is moot at Phase 0 (D-1 same-provider) but returns with FE-1. **Register-not-resolve:** C57 names the missing model + its owner; it does not build a cost model. |
| **G33** (major) | No story for partial/cascading failure of the OSS stack (CXDB/LangFuse/Python tool-nodes down mid-run); no degradation/retry/circuit-breaker design. | **status `gap` (stack-degradation) · owner C40 (durable Orders, partial) / C24 (bridge back-pressure, partial)** · *Residual:* "Gas City Orders survive crashes" is claimed for Gas City only; the Python-tool-node / CXDB-outage degradation design does not exist. C40 + C24:OQ-4 (inbox-capacity bound) cover slices; the holistic story is a gap. **Register-not-resolve:** C57 records the gap + the partial owners. |
| **G34** (major) | Single-Max-seat throughput ceiling; the rate-limit relief (twins) is on the *dependency* side, but the coder/judge still hit Max limits. | **status `partial` · owner C04/C05/C28 (concurrency) + FE-4 (seat-pool, deferred)** · *Residual:* P7 twins relieve the *dependency* side, not the *agent* side; the agent-side ceiling under one Max seat is real and **deferred to FE-4** (multi-seat automation, blocked on Max ToS clarity). **Register-not-resolve:** C57 records the ceiling + the FE-4 deferral. |
| **G35** (major) | RSI / goal-subversion is the weakest acknowledged control on a self-modifying L5 factory (F54 guard = "audit pack", not built). | **status `partial` / `caution` · owner split:** blast-radius half → **C43**; per-fix ship-gate → **C39**; ladder/which-level-auto-ships → **C56**; **the F54 multi-cycle objective-drift audit register is homed at C57 itself — UNBUILT, Batch 5** (C52:OQ6 / C56:OQ-3 / C39:OQ3). · *Residual:* the objective-drift audit mechanism does not exist; C57 is its declared home but registers it as unbuilt. **Register-not-resolve:** C57 owns the *home* for the F54 residual but **does not build the audit** — that is the most important honesty line in this row. |
| **G38** (major) | F15 missing entirely from the 61-mode coverage. | **status: corrected in the register structure (§4.3)** · owner C57 · *Residual:* F15's *status* (addressed/partial/gap) cannot be set until F15's definition is recovered from the v3 catalog source — itself **OQ-C57-1**. **Register-not-resolve:** C57 *adds the row* (fixes the structural drop) but honestly marks F15's status TBD pending its definition. |
| **G39** (major) | Summary counts don't reconcile (24+20+11+4 = 59 ≠ 61). | **status: corrected in the register structure (§4.3)** · owner C57 · *Residual:* the exact resolved per-mode tally is a sweep-2 deliverable (Reading A, §4.3); sweep-1 fixes the rule (sum to 61, shown). **Register-not-resolve:** C57 fixes the arithmetic rule + commits to a shown re-tally; it does not paper over the unshown base. |
| **G40** (major) | F32/F35/F47 each double-counted across sections with conflicting status. | **status: corrected in the register structure (§4.3)** · owner C57 · *Residual:* the Partial+Caution→`caution` tie-break (§4.3) is a *faithful editorial rule*; if an owner disputes a resolved status that is a sweep-2 reconciliation item. **Register-not-resolve:** C57 enforces one-status-per-mode + one-owner-per-mode; it records the tie-break rule, not a silent re-statement. |
| **G44** (minor) | El Kaim "10 of 11" arithmetic vs "12 working principles" — the +1/−1 bookkeeping yields 11 unless something is uncounted. | **status `gap` (corpus-arithmetic note) · owner integrator / C54 (phase-plan principle accounting)** · *Residual:* the working set is "10 original-minus-1 + 1 new (self-optimization) = 11", but the corpus asserts 12; the El Kaim P11↔P12 split is the unreconciled bookkeeping. **Register-not-resolve:** C57 records the discrepancy as an honest note; it does not re-derive the principle count (that is an architecture-wide editorial call, C54:OQ-1 sibling). |

**The run-wide residuals C57 also carries (beyond the 9 gaps):**

| Residual | Owner / decision-ref | Caveat that must travel |
|---|---|---|
| **4 cautions** (F52 Tempting-Wrong-Hybrid; F35 Federation-drift; F25 design-starvation; F47 Goodhart) | F-MODE-COVERAGE §8; F52→C16/C18 discipline; F35→C51 pack-governance; F25→C56 (G15); F47→C50 promotion gate | each is a mode v4's design **could worsen**; the required discipline + owner travels with it (status `caution`). |
| **XC-8 / D-18 exposure window** | C43 + integrator | "prevention" claims for Phase-0 capability breach are **detection-only** until C43 isolation lands; D-18 (provisional, operator-confirm) pulls the boundary-typing half forward but the twin half stays Phase-3c. |
| **prevent-vs-detect** (C43:OQ-C43-1 ≡ C34:OQ-C34-1) | C43 + C34, gated on G11 | does `gc`/the loader **prevent** an out-of-partition read / production-typed surface at tool-call time, or **permit-with-detect**? Settles whether typing is a control or a declaration. Unresolved without real `gc`. |
| **F54 / G35 objective-drift audit** | **C57 (home) — UNBUILT, Batch 5** | the multi-cycle goal-comparison audit does not exist; C57 is its declared register home (C52:OQ6/C56:OQ-3/C39:OQ3) but registers it unbuilt. |
| **same-family-judge bias** (D-1) | C32/C34; FE-1 trigger | Phase-0 judge shares the coder's provider/family; F1/F27/F46 "Addressed" and F48 "Partial" carry the shared-distribution residual until FE-1 (cross-family) is triggered. |
| **C49 counterfactual replay unsolved** (G19) | C49 | the "most significant invention" is "largely unsolved" — zero interface/contract/acceptance scenario; P12's self-optimization completeness rests on it. |
| **FE-1..FE-5 deferred-by-decision** | FUTURE-ENHANCEMENTS.md | cross-family judge (FE-1), substrate-portability contracts (FE-2), graduated signing (FE-3, blocked on G37 secrets), multi-seat automation (FE-4), enumerated DoD (FE-5) — each with its revisit trigger. Recorded as *deferred*, distinct from `gap`. |

> [AMBIGUITY: G35] **Is C57's ownership of the F54/objective-drift audit an obligation to *build* the audit,
> or only to *register* it as unbuilt and homed here?** Reading A (register-only): C52:OQ6/C56:OQ-3/C39:OQ3
> route the F54 *residual home* to C57 so it is "explicitly homed, not assumed-covered"; the audit mechanism
> itself is "unbuilt, Batch 5" and C57 is a documentation artifact, so C57 owns the *ledger entry*, not the
> mechanism. Reading B (build it): C57 could be read as the place the audit-pack lives. **Pick: Reading A —
> C57 registers the F54 residual as unbuilt + homed; it does not build the audit-pack.** C57 is explicitly a
> register/coverage-map *artifact* (brief; inventory kind cross-cutting/documentation), and the bar DROPS a
> coverage-enforcement engine — an objective-drift *audit* is a running mechanism, not a register. The
> faithful move is: C57 is the **honest home** for the F54 residual (so no one assumes it covered), and the
> *audit mechanism* is a separate unbuilt Batch-5 component / pack the register points at. Building it inside
> C57 would conflate the ledger with the work and exceed the artifact's scope.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C57 is the **security honesty surface**: it is where the lethal-trifecta exposure window
  (G31/XC-8/D-18), the prevent-vs-detect residual (C43/C34), and the RSI/objective-drift weakness
  (G35/F54) are recorded so the whole-system security claim is *honest about what is paper*. C57 adds no
  control; it ensures no security "Addressed" is read without its caveat. The single most important security
  function of the capstone is the **"no bare Addressed"** invariant (§3).
- **Cost.** C57 is cheap (a Markdown artifact under git review). It also *registers* the cost gap (G32) —
  the absence of a cost model is one of the residuals it carries; C57 does not build the model (C46/C29
  own it).
- **Scale.** C57 has no scale concern of its own (it is a document). It *registers* the throughput ceiling
  (G34) + the FE-4 deferral. The register grows only with the catalog (61 modes); it does not grow with
  runtime volume.
- **Observability.** C57 *is* the consolidated observability of coverage + license + residual status — the
  one page that makes "what is covered, what is paper, what is deferred" auditable for a human. It aggregates
  but does not collect; the underlying telemetry is the owning components'.
- **Ops.** C57 is **hand-maintained under git review** (like the C51 census it aggregates). The operative
  ops risk is **staleness** (it is finalized last; statuses change in their owners) — managed by editorial
  discipline at integration time, not an automated sync (OQ-C57-2). Enabling/closing a residual (e.g. C44
  twins land → shrink the G31 caveat) is an explicit, auditable C57 edit.
- **License hygiene (its own cross-cut).** C57 owns the consolidated license view over C51's dispositions +
  the README census; a code-port from an unverified/restrictive exemplar is a flagged residual. This is the
  legal-hygiene ledger of the factory; the per-build gate is C51's.

## 8. Acceptance criteria & test strategy

C57 is an artifact, so its acceptance is **editorial-integrity checks** (reviewable by a person), not
runtime tests:

1. **Total coverage (G38)**: the coverage map contains **exactly 61 rows**, one per F-id F1–F61, **including
   F15**. No mode is missing; no mode is duplicated.
2. **Single status (G40)**: every mode carries **exactly one** status ∈ {addressed, partial, gap, caution},
   and **one owning component**. F32/F35/F47 each resolve to one status + one owner (Partial+Caution →
   `caution`, partial-mechanism noted in the residual).
3. **Counts reconcile (G39)**: the per-status counts **sum to 61**, the reconciliation arithmetic is
   **shown**, and the percentages are computed against 61. The summary is **derivable from the rows**.
4. **No bare "Addressed" (the honesty invariant)**: every "Addressed" resting on an unbuilt (twins/C44/C49)
   or detection-only (XC-8) mechanism **carries its caveat** in the `residual` column, linking to the
   residual register. F12/F44/F56 link to the G31 exposure-window entry.
5. **Gaps & cautions named (capstone honesty)**: every `gap` and every `caution` is present with its
   residual + owner; none silently dropped or upgraded. The 4 cautions (F52/F35/F25/F47) and the gap set are
   discoverable on the page.
6. **9 gaps registered, not resolved**: G31/G32/G33/G34/G35/G38/G39/G40/G44 each have a register entry with
   status + owner + residual **as the run left it**; C57 asserts **no** resolution it did not build (esp.
   G35/F54 audit = registered **unbuilt**, not claimed-built).
7. **License hygiene aggregated (C51)**: every factory-built component has a license disposition sourced from
   C51 (license fact + `verified?` + `transfusion_mode`); a code-port from an unverified/restrictive exemplar
   is flagged. No SBOM scanner; the view is the hand-maintained aggregate (C51:OQ-C51-4).
8. **Run-wide residuals carried**: XC-8/D-18 exposure window, prevent-vs-detect, F54/G35 objective-drift
   (unbuilt, homed at C57), D-1/FE-1 same-family-judge bias, C49/G19 unsolved replay, and FE-1..FE-5 are all
   in the residual register with owner + caveat.
9. **No over-build (bar)**: C57 contains **no CI gate, no coverage-enforcement engine, no automated
   license/SBOM scanner, no residual-risk service**. It is a hand-maintained Markdown artifact. (When in
   doubt, DROP.)
10. **Not the repo-level artifact**: C57 is the v4-internal register over F1–F61; it does **not** touch,
    mirror, or supersede `architectures/failure-modes.md` (the `0N-*` repo-level catalog).

(The concrete per-mode resolved-status table over all 61 modes, the license-hygiene aggregation field
mapping from C51, the residual-id scheme, and the column encodings are **sweep-2** deliverables — sweep-1
fixes the **register structure + the honesty invariants + the gap-registration policy**, at architecture
altitude.)

## 9. Open questions

- **OQ-C57-1** (→ review-log): **What is F15, and what is its status?** F15 is absent from the v4
  F-MODE-COVERAGE entirely (G38); recovering its definition requires the v3 source catalog
  (`architectures/v3/failure-modes-v3.md`, cited as F-MODE-COVERAGE's source). C57 *adds the row* (fixing the
  structural drop) but cannot set F15's status (addressed/partial/gap) until its definition is recovered.
  Until then F15's status is honestly TBD. Sweep-2 / requires the v3 catalog.
- **OQ-C57-2** (→ review-log): **Is C57 a point-in-time snapshot (re-authored at each integration) or a
  living doc with a propagation discipline from owning components?** Because C57 is finalized last and
  statuses change in their owners (e.g. C44 twins shrink the G31 caveat), the staleness risk is real. The
  faithful sweep-1 reading is a **hand-maintained snapshot updated at integration milestones** (no automated
  sync — that would be the dropped enforcement engine), but the cadence + who-owns-the-edit is open. Sweep-2.
- **OQ-C57-3** (→ review-log; **top open question**): **Does the F54 / objective-drift audit get a real
  owning mechanism, or does it stay an unbuilt residual homed at C57 indefinitely?** Per G35 (Reading A,
  §6) C57 *registers* the F54 residual as unbuilt + homed here (C52:OQ6/C56:OQ-3/C39:OQ3), but a
  self-modifying L5 factory with the **weakest** control on objective drift (the run's loudest unresolved
  security residual after G31) needs the audit-pack *built* by someone eventually. Confirm whether the
  orchestrator schedules a Batch-5 F54 audit component/pack (and who owns it), or accepts the residual as a
  permanent caveat on L5 autonomy. This is the residual most likely to be wrongly read as "covered."
- **OQ-C57-4** (→ review-log): **Does the G39 re-tally (Reading A, §4.3) belong at sweep-2 as a pure
  editorial pass, or does it need each owning component to re-confirm its mode's status first?** The faithful
  reading is that C57 re-tallies from the components' current spec §6 statuses (the owners are authoritative);
  but several statuses are themselves contested (the prevent-vs-detect residual means F12/F28's "Addressed"
  is contingent). Confirm whether the re-tally is C57-editorial or requires a per-owner status freeze.
  Sweep-2.
- **OQ-C57-5** (→ review-log): **Where do the architecture-wide editorial residuals routed to "integrator/C57"
  actually land — in C57's register, or in a separate integrator pass?** G01 (the two "layer" vocabularies,
  C54:OQ-1), G44 (the El Kaim principle-count bookkeeping), and the namespace-sprawl rulings (XC-4/XC-4b) are
  routed to "integrator/C57". Confirm which are C57 *register entries* (honest notes on a corpus defect) vs
  which need an *integrator edit pass* across the corpus (a rename C57 cannot perform as a register). C57's
  faithful scope is to *record* them as residuals; performing a corpus-wide rename is an integrator action,
  not a register's. Sweep-2 / integrator.
