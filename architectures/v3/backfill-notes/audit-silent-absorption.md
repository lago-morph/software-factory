---
audit-kind: silent-absorption
bias-guard-role: silent-absorption-auditor (Wave 7.2)
based-on-specs-commit: c54daf1 (9 specs) + aa9d372 (u-c)
based-on-date: 2026-05-27
auditor-mandate: |
  Per auto-007 §Decision (Round 2) — base mandate + Reviewer 2 A3
  (Phase-6-followup #1 ADR-0036 framing audit) + Reviewer 6 D-H4
  (Phase-6-followup #2 cross-spec characterization of all 4 framework ADRs).
specs-audited:
  - architectures/v3/specs/gf-s.md
  - architectures/v3/specs/gf-m.md
  - architectures/v3/specs/gf-c.md
  - architectures/v3/specs/bf-s.md
  - architectures/v3/specs/bf-m.md
  - architectures/v3/specs/bf-l.md
  - architectures/v3/specs/u-a.md
  - architectures/v3/specs/u-b.md
  - architectures/v3/specs/u-c.md
  - architectures/v3/specs/d7-u-1.md
archive-files-audited:
  - archive/research-plan.md
  - archive/synthesis-v1-v2/00-synthesis.md
  - archive/synthesis-v1-v2/13-round-2-synthesis.md
  - archive/architectures-v2/00-comparison.md
  - archive/architectures-v2/01-specification-refinery.md
  - archive/architectures-v2/02-compound-atelier.md
  - archive/architectures-v2/03-phase-gated-foundry.md
  - archive/architectures-v2/04-evolutionary-tournament.md
  - archive/architectures-v2/failure-modes.md
finding-counts:
  high: 3
  medium: 7
  low: 5
  total: 15
self-check-results:
  ls-cited-files: PASS (all 19 cited files verified existing)
  section-headers: PASS (§A scope / §B findings / §B.1-§B.3 / §C recommendations)
  output-format-precedent: phase-6-verification-findings.md §A/§B/§C mirrored
---

# Silent-absorption audit — Phase 7 bias-guard

Independent re-audit of the 10 Phase-6 specs against the 9 archive files for **silent absorption** — spec content that looks like archive material WITHOUT an explicit citation to the archive. The per-candidate fanout (Wave 7.1) asks the inverse question ("what's in the archive that the candidate carries"); this audit asks "what's in the candidate that came from the archive without saying so?"

The audit is structured per the [`phase-6-verification-findings.md`](../phase-6-verification-findings.md) output precedent (Reviewer 6 D-H7). All §B findings carry the **confidence label** (`high` / `medium` / `low`) per [auto-007 § Round-2 reconciliation precedence rule](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) (Reviewer 5 Defect 3 amendment). Only `high`-confidence findings override per-candidate `rejected` verdicts at lead-agent aggregation; `medium` triggers `tbd` reconciliation; `low` is informational.

## §A Scope

**In scope.** (i) Cross-spec scan for archive material appearing in v3 specs without an archive-citation; (ii) Phase-6-followup #1 — BF-L vs U-A vs D7-U-1 ADR-0036 framing audit (Reviewer 2 A3); (iii) Phase-6-followup #2 — cross-spec characterization audit of all four framework ADRs (0028 P-19, 0029 P-28, 0030 P-29, 0036 P-30) across the candidates that claim each (Reviewer 6 D-H4).

**Out of scope.** Per-candidate verdicts (Wave 7.1 fanout owns these); per-candidate `not-applicable-to-candidate-mandate` cells (never overridden per the auto-007 precedence rule); D-1..D-7 default verification (per-candidate §1.5 owns this). Known-rejected items (OpenHands+Overstory substrate stack; Compound Atelier as baseline) are NOT silent-absorption candidates because v3 archives them as explicitly-excluded; per-candidate §N.2 carries the `rejected (explicitly-excluded)` verbatim verdict.

**Per-candidate §N.3 ADR-0036 framing characterizations** (required of BF-L / U-A / D7-U-1 per Reviewer 5 Defect 2) are authoritative for each spec; this audit's §B.2 is the cross-spec reconciliation surface, not a re-litigation.

## §B Findings

### §B.1 Silent-absorption findings (per-spec × per-archive-item)

| # | Spec | Spec section | Archive source | Finding | Confidence | Recommended action |
|---|---|---|---|---|---|---|
| 1 | U-A | §4 Knowledge promotion (line 133) | `02-compound-atelier.md` §3.2 (Knowledge document shape) | Near-verbatim lift: U-A names "Compound-Knowledge insight / playbook / correction / pattern envelopes" — the four-token category set is the Atelier `02-compound-atelier.md` §3.2 `type: solution | insight | playbook | correction | pattern` YAML enum. U-A cites no archive source. | **high** | **Override:** U-A × `02-compound-atelier.md` §3.2 → `absorbed (silently, high-confidence — flagged for Phase-8 cite)`. Spec-patch optional. |
| 2 | GF-M / U-A / U-B / U-C / D7-U-1 / BF-S / BF-M (7 specs) | §3 Methodology / §4 Three-loop bindings | `02-compound-atelier.md` §1 + v0.2 note ("FOUR-STEP Plan → Work → Review → Compound"); `00-synthesis.md` §0 mirror | The phrase "Compound-Engineering plan → work → review → compound" appears verbatim across 7 specs. Only GF-M cites `research/03-every-compound-engineering.md`; **none** cite the archive `02-compound-atelier.md` or `00-synthesis.md` where the four-step phrasing is canonicalized. | **high** | **Override** per-candidate `rejected` cells on Atelier core thesis. Cells for {U-A, U-B, U-C, D7-U-1, GF-M, BF-S, BF-M} × `02-compound-atelier.md` §1 → `absorbed (silently, high-confidence)`. BF-S exemplar §7.1.1 already `absorbed`; propagate to the other 6. Spec-patch optional (see §C #5). |
| 3 | BF-S / BF-L / BF-M / D7-U-1 / U-A | §3 work-unit-definition | `00-comparison.md` §1 (four-architecture taxonomy); `02-compound-atelier.md` §5 (issue-shape) | "Atelier-style / Refinery-style / Attractor-DOT pipelines" used as work-unit-shape taxonomy across 5 specs. The four-architecture taxonomy IS `00-comparison.md` §1; specs cite registry / tracks but never archive. | **high** | **Override** per-candidate `rejected` on `00-comparison.md` §1. All 5 cells → `absorbed (silently, high-confidence)`. BF-S exemplar §5.1.1 already `absorbed`; recommend extending cite to archive. |
| 4 | U-A / U-B / U-C / D7-U-1 | §2 typed-envelope schemas | `02-compound-atelier.md` §3 (artifact stack with YAML frontmatter / stable IDs) | Typed-envelope axis with `kind`, content-hash `id`, frontmatter-discipline fields is structurally the Atelier §3.2 YAML-frontmatter knowledge-doc shape lifted to substrate. Specs cite ADR 0029 P-28; ADR 0029's lineage to Atelier §3 is not surfaced. | medium | **`tbd` row** for {U-A, U-B, U-C, D7-U-1} × `02-compound-atelier.md` §3. Lead-agent adjudicates Atelier-derived vs sufficiently-transformed. |
| 5 | U-B | §1 Axis; §3 Layer structure | `02-compound-atelier.md` §3 artifact stack + §7.5 three memory tiers | U-B's 5-pace-layer stack (L0 Standards / L1 Architecture / L2 Spec / L3 Plan / L4 Code) cites "Brier convention" but mirrors the Atelier §3 artifact-tiering. U-B disclaims Brier metaphor-swap; does not disclaim Atelier-tier-shape lineage. | medium | **`tbd` row** for U-B × `02-compound-atelier.md` §3 + §7.5. |
| 6 | BF-M | §3 stage 6 Cross-model review | `02-compound-atelier.md` §4.3 (Reviewer panel) | BF-M stage 6 "Specialized critics for code-quality, security, conformance to existing-codebase conventions" is structurally the Atelier §4.3 reviewer panel. Cites CJ Hess `kevin/carl` + "Anthropic Auto-Review pattern" — no archive cite. | medium | **`tbd` row** for BF-M × `02-compound-atelier.md` §4.3. |
| 7 | GF-M | §3 Regime-B cycle shape | `02-compound-atelier.md` §1; `00-comparison.md` §1 | GF-M Regime-B "inherits the Compound-Engineering loop" cites `research/03-` but not the archive. Primary-source cite may sufficiently substitute. | medium | **`tbd` row** for GF-M × `02-compound-atelier.md` §1. |
| 8 | BF-S | §2 Brier absorption; §4 knowledge promotion | `02-compound-atelier.md` §2 + §7 | BF-S "Compound-Knowledge-style" + "Brier pace-layer absorption" cites `research/followup/11-`; primary-source cite doesn't fully substitute for archive Atelier §2+§7. | medium | **`tbd` row** for BF-S × `02-compound-atelier.md` §2 + §7. |
| 9 | BF-S | §3 step 5 cross-model judge | `04-evolutionary-tournament.md` §3.4; `failure-modes.md` F1 row | Substrate-enforcement of cross-family judge as F1/F46 mitigation closest to Tournament §3.4 "Diversity policy (structural)" — Architecture-4's distinctive contribution per failure-modes.md. | medium | **`tbd` row** for BF-S × `04-evolutionary-tournament.md` §3.4. |
| 10 | GF-S | §3 step 5; §4 bias-guard | `04-evolutionary-tournament.md` §3.4 | GF-S "3-of-N family-diverse ensemble" — same Tournament-derived structural-diversity pattern; cited to overlap.md + ADR rather than archive. | medium | **`tbd` row** for GF-S × `04-evolutionary-tournament.md` §3.4. |
| 11 | BF-M | §3 stage 4 "Klaassen four-clause plan-prompt" | `02-compound-atelier.md` §0.0 + §6 (Klaassen examples); `00-synthesis.md` §0 (Klaassen references) | "Klaassen four-clause plan-prompt" naming has no archive cite in BF-M; lineage to Klaassen articles is in archive synthesis but not invoked. | low | **Informational only.** |
| 12 | BF-L / U-B | BF-L §3.3 maintenance loop; U-B §3 layer structure | `03-phase-gated-foundry.md` §3 + §3.1 (CM + Defect-of-origin); §4 (RUP discipline × phase matrix) | BF-L's "three loops over a single durable artifact" mirrors Foundry's phase-bound + per-phase responsibility shape. U-B's L0-L4 parallels Foundry SRS/SAD/DD/RTM. Neither cites archive Foundry. Suggestive but shapes differ substantively. | low | **Informational only.** |
| 13 | All 10 specs | §3 framing "thin-methodology" / "substrate-heavy" | `00-comparison.md` §4.1 ("the architecture is the methodology; the infrastructure is shared") | The substrate/methodology split organizing v3 §2-§3 mirrors v2 comparison §4 framing. DEC-1/DEC-2 + registry cited; no archive cite. Framing-level lineage, not primitive-level. | low | **Informational only.** DEC-1/DEC-2/Phase-3 reframing arguably re-derived it. |
| 14 | GF-C | §1.2 "Council" + §3 cross-model judge | `02-compound-atelier.md` §4.3; `04-evolutionary-tournament.md` §3 | GF-C "Council" naming has no archive cite; closest precedents are Atelier §4.3 + Tournament §3.4. Track-internal lineage. | low | **Informational only.** |
| 15 | D7-U-1 | §1 "Popperian conjecture-and-refutation loop" | None in archive | **NEGATIVE finding.** Popperian framing is NOT in archive; D7-U-1-distinctive per blind-axis-test origin. Listed so reader sees auditor checked. | low | **Informational only.** No action; confirms D7-U-1's Popperian axis is candidate-original. |

**§B.1 cell-count tally.** 15 findings total: 3 `high` / 7 `medium` / 5 `low`. Findings #1, #2, #3 are load-bearing (override per-candidate `rejected` verdicts if any exist); findings #4-#10 trigger `tbd` reconciliation rows; findings #11-#15 are informational only per the [auto-007 confidence-threshold rule](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2).

### §B.2 ADR-0036 framing audit (Phase-6-followup #1)

Per [Phase-6 verification-findings §B.1 Finding-2](../phase-6-verification-findings.md#b1-interpretation-drift-on-shared-framework-adrs) the three claiming candidates' ADR-0036 framings:

- **U-A §0 row 0036:** *"P-30 Event registrar substrate | common-substrate"* (paired with 0053). U-A §2 (line 86 narrative): *"Temporal signal+timer+query triad + append-only event-log envelope shared with D7-U-1, with namespace-separation discipline"*. **U-A's registrar is event-driven** — state transitions on external triggers; timer half is incidental (deadline tracking only).
- **D7-U-1 §0 row 0036:** *"P-30 Event registrar substrate | common-substrate"* (paired with 0064). D7-U-1 §2 (line 80 narrative): *"shared Temporal substrate (signal+timer+query triad + append-only event-log + namespace separation)"*. **D7-U-1's registrar is timer-driven** — load-bearing transition is `survival-window-open → window-expired`, with cascade wake-up of dependent-FC graphs.
- **BF-L §0 row 0036:** *"P-30 Event registrar substrate | common-substrate"* (no Variant-of). BF-L §0 annotation (line 47): *"0036 IS consumed (without per-variant binding) by P-13 maintenance-loop dispatch ([ADR 0048])… so 0036 appears in §0 as a **commodity dispatch surface**, not as a framework requiring BF-L per-variant authorship."* BF-L §2.2 §3.3 (maintenance loop): the inspector emits typed `maintenance-trigger` events to P-30 substrate.

**Verdict — drift.** The U-A and D7-U-1 framings agree that 0036 is a *registrar framework* (per the Phase-4.2 overlap.md DISTINCT-primitives-despite-shared-substrate verdict — they share Temporal infra but the load-bearing semantics diverge: event-driven vs timer-driven). The BF-L framing as "commodity dispatch surface" is **materially different** — BF-L treats 0036 as a fire-and-forget event-emission API, not as a registrar holding state-machine semantics. This is **internally consistent** with BF-L's usage (BF-L does NOT instantiate a registrar workflow; it just publishes events that some downstream maintenance handler consumes), and BF-L's §0 annotation honestly names the asymmetry.

**Reconciliation recommendation.** The Phase-6-verification-findings §C non-blocking Recommendation #1 (glossary clarification — when does the framework + per-variant pair obligation fire?) remains the right resolution. Specifically: AGENTS-MD-a9fb7b42f8 should distinguish *consumption-only* framework references (BF-L's case for 0036 — no per-variant needed) from *substrate-primitive-claim* framework references (U-A/D7-U-1's case — per-variant required). The drift is **non-blocking** for Phase-6 closure and the per-candidate fanout has already produced or will produce the per-candidate §N.3 ADR-0036 framing characterizations per Reviewer 5 Defect 2.

### §B.3 Cross-framework-ADR characterization audit (Phase-6-followup #2)

For each of the four framework ADRs, enumeration of claiming candidates' framings + drift flags:

**0028 P-19 (Eligibility / regime classifier framework).** Claimed by GF-S, BF-L, U-A, U-C. Per-variant ADRs: 0039 (GF-S work-unit-class), 0049 (BF-L per-region), 0050 (U-A interval-kind), 0058 (U-C distance-tuple).

- GF-S §2 (line 81): *"shared decision-table engine (Drools / OPA Rego) + LLM-judge fallback via P-14 + OPA hard-floor post-check"* — verbatim from overlap.md.
- BF-L §2.3 (line 105): cites the verbatim overlap.md verdict + cites overlap.md BF-L row verbatim.
- U-A §2 (line 75): cites the verbatim overlap.md verdict.
- U-C §2 (line 67): cites the verbatim overlap.md verdict. U-C names this primitive a "*dispatcher* rather than *classifier*" (line 77) because P-32 has already done the feature engineering.

**Drift verdict — ALIGNED.** All four candidates carry the verbatim overlap.md verdict; their per-variant ADRs differ at *feature source* and *output enum* per the overlap.md "DISTINCT feature sources + distinct output regime sets" verdict. U-C's "dispatcher-not-classifier" relabeling is per-variant role-shift, not framework drift. **No silent absorption to flag at the framework-ADR layer.**

**0029 P-28 (Typed-object store framework).** Claimed by U-A, U-B, U-C, D7-U-1. Per-variant ADRs: 0051 (U-A interval envelope), 0055 (U-B layer-typed envelope), 0059 (U-C anchor envelope), 0062 (D7-U-1 FC envelope).

All four specs cite the verbatim overlap.md P-28 verdict; the envelope schemas are non-overlapping by overlap.md design ("DISTINCT envelopes" — interval-indexed / layer-indexed / immutability-metadata-indexed / commitment-indexed). **Drift verdict — ALIGNED at framework layer.** See §B.1 finding #4 (medium-confidence) for the orthogonal Atelier-knowledge-doc-shape lineage at the envelope-shape level.

**0030 P-29 (Policy mediator framework).** Claimed by U-A, U-B, D7-U-1. Per-variant ADRs: 0052 (U-A interval-policy DSL), 0056 (U-B per-layer-boundary), 0063 (D7-U-1 FC-survival).

All three specs cite the verbatim overlap.md P-29 verdict; the DSLs differ at *predicate vocabulary* per overlap.md ("DISTINCT policy DSLs"). **Drift verdict — ALIGNED at framework layer.** No silent absorption findings on P-29.

**0036 P-30 (Event registrar substrate).** Claimed (per-variant) by U-A and D7-U-1; **consumed-only** by BF-L. Per-variant ADRs: 0053 (U-A re-entry state machine), 0064 (D7-U-1 survival-window state machine).

**Drift verdict — see §B.2 above.** U-A vs D7-U-1 framings are DISTINCT-primitives-despite-shared-substrate per overlap.md verdict (event-driven vs timer-driven). BF-L's commodity-dispatch consumption-only framing introduces a *third* characterization that is internally consistent but not isomorphic to the registrar framings. Glossary clarification on consumption-only vs substrate-primitive-claim references is the right resolution; **non-blocking for Phase-6 closure** and **non-overriding** of per-candidate verdicts at any confidence level.

## §C Recommendations

Per the [auto-007 reconciliation precedence rule](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) (Reviewer 1 A3 + Reviewer 5 Defect 3 confidence-threshold amendment):

1. **Aggregation-time overrides (high-confidence; mechanical).** Lead agent at `backfill-notes.md` aggregation MUST downgrade the 3 `high`-confidence cells to `absorbed (silently, high-confidence — flagged for Phase-8 cite)` regardless of any per-candidate `rejected` verdicts on the same cells. Affected cells: (i) U-A × `02-compound-atelier.md` §3.2 (knowledge-doc category set); (ii) {U-A, U-B, U-C, D7-U-1, GF-M, BF-S, BF-M} × `02-compound-atelier.md` §1 / §5 (Compound-Engineering four-step loop); (iii) {BF-S, BF-L, BF-M, D7-U-1, U-A} × `00-comparison.md` §1 (four-architecture taxonomy as front-end work-unit-shape).

2. **`tbd` reconciliation rows (medium-confidence).** Lead agent MUST add `tbd` reconciliation rows in the aggregation matrix for findings #4-#10 (7 cells). These trigger lead-agent adjudication at aggregation time; outcome is per-cell judgment whether the cite-obligation fires or whether the primary-source/registry citation sufficiently substitutes.

3. **Informational-only (low-confidence).** Findings #11-#15 are recorded for completeness but do NOT trigger overrides or `tbd` rows. Recommend they surface in the Phase-7-close handoff under "carries to Phase-8 lean-eval calibration" rather than driving any in-run spec patches.

4. **NEVER overridden (auditor cannot re-litigate).** Per-candidate `not-applicable-to-candidate-mandate` verdicts. The audit's findings #4-#10 explicitly avoid touching N/A cells; the override surface is only `rejected` verdicts.

5. **Phase-7-followup spec-patch candidates (3-`high`-finding-derived; ≤3 candidates threshold check).** The three `high`-confidence findings touch ≥4 candidates total ({U-A} for #1; {U-A, U-B, U-C, D7-U-1, GF-M, BF-S, BF-M} for #2; {BF-S, BF-L, BF-M, D7-U-1, U-A} for #3). If the lead agent decides to spec-patch every silently-absorbed cell with an inline archive cite, this exceeds the ≤3-candidates in-run patch threshold and triggers Phase-7-followup deferral per auto-007. **Recommendation:** lead-agent at aggregation time decide whether (a) spec-patches are required (full inline archive cites — triggers deferral) or (b) the aggregation matrix's flagged-for-Phase-8-cite annotation is sufficient (no spec patches in this run; Phase-8 lean-eval briefs carry the cite obligation forward).

6. **ADR-0036 framing drift (Phase-6-followup #1).** Per §B.2, the BF-L "commodity dispatch surface" vs U-A/D7-U-1 "registrar-framework" framing is non-blocking and consistent with Phase-6-verification §C Recommendation #1. The right resolution is glossary clarification of AGENTS-MD-a9fb7b42f8 to distinguish consumption-only references from substrate-primitive claims. Carry to Phase-7-close handoff.

7. **Cross-framework-ADR drift (Phase-6-followup #2).** Per §B.3, the four framework ADRs (0028 / 0029 / 0030 / 0036) are aligned at framework layer; per-variant differences are by overlap.md design ("DISTINCT envelopes" / "DISTINCT feature sources" / "DISTINCT policy DSLs" / "DISTINCT primitives despite shared substrate"). No framework-layer drift across claiming candidates. The 0036 case is the only one that surfaces drift (between consumer-only BF-L and per-variant U-A/D7-U-1); that drift is §B.2's subject and is non-blocking.

8. **Audit-trail discipline.** This audit's findings should be folded into the `backfill-notes.md` aggregation file's reconciliation column. The per-candidate fanout's notes files remain authoritative for each spec's own cells; this audit's role is the cross-spec read that surfaces what individual per-candidate views cannot see.
