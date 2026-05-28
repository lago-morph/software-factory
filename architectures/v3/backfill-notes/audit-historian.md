---
audit-role: historian (Phase-7 bias-guard subagent)
based-on-specs-commit: c54daf1
based-on-date: 2026-05-27
inputs-read:
  - architectures/v3/specs/{gf-s,gf-m,gf-c,bf-s,bf-m,bf-l,u-a,u-b,u-c,d7-u-1}.md
  - archive/research-plan.md
  - archive/synthesis-v1-v2/00-synthesis.md
  - archive/synthesis-v1-v2/13-round-2-synthesis.md
  - archive/architectures-v2/00-comparison.md
  - archive/architectures-v2/failure-modes.md
  - archive/architectures-v2/{01-specification-refinery,02-compound-atelier,03-phase-gated-foundry,04-evolutionary-tournament}.md
  - architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5-close.md (per-candidate ADR table)
  - architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md (erratum reference)
  - architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md (dispatch brief)
  - architectures/v3/backfill-notes/bf-s.md (exemplar)
  - architectures/v3/phase-6-verification-findings.md (output-format precedent)
gap-finding-counts:
  load-bearing-gap: 5
  not-load-bearing-rejection: 4
  mandate-rejection: 4
  silent-omission: 5
handoff-erratum-rows-flagged: 2  # beyond the already-known BF-M / 0049 row
verdict: PASS WITH AMENDMENTS  # informational; lead agent reconciles at aggregation
---

# Historian audit — Phase 7 bias-guard

## §A Scope

**Mandate (base)** per [auto-007 §Wave 7.2](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2): enumerate archive items appearing in **zero Phase-6 specs in any form**. Complement of the silent-absorption auditor (which finds material in specs without cites; the historian finds material absent from all specs).

**Mandate (expanded per Reviewer 6 D-H3)**: one-pass scan of the Phase-5-close handoff per-candidate ADR set table for documentation drift beyond the already-known BF-M / 0049 row (corrected in [Phase-6-close handoff erratum](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#adr-0049-documentation-erratum)).

**In scope.** 10 Phase-6 specs; 9 archive files; Phase-5-close handoff per-candidate ADR table.

**Not in scope.** Per-candidate verdicts (per-candidate fanout owns those); D-1..D-7 verification (per-candidate §1.5); v3 non-spec files (`primitives/`, `failure-modes-v3.md`, `decisions-captured.md`, `candidate-registry.md`, `tracks/`, `contradictions.md`) — where an item is absent from specs but present in a v3 non-spec file, the gap is flagged as `silent-omission`. Bias-direction-protected known-rejected items (OpenHands+Overstory; Compound Atelier baseline) are NOT flagged; noted once in §C.3 for completeness.

**Method.** Per archive file, identify named items at paragraph-or-shorter granularity; `grep -lc` across the 10 specs; item is a gap iff zero matches AND no semantic equivalent found (judgement). Classify per `load-bearing-gap` / `not-load-bearing-rejection` / `mandate-rejection` / `silent-omission`.

## §B Findings

### §B.1 Archive items appearing in zero specs (gap findings)

| # | Source | Item | Spec presence | Action | Rationale (≤30 words) |
|---|---|---|---|---|---|
| H-1 | `00-synthesis.md` §5.5 + `02-compound-atelier.md` §6.1 | **Stable-identifier discipline (R/A/F/AE/U/S/K lettering)** | 0 specs (`grep 'R/A/F/AE\|stable-ID\|stable identifier'` = 0). Only `contradictions.md`. | **load-bearing-gap** | F11 closure depends on stable IDs. v3 substitutes P-22 symbol-range + P-24 attribution but no spec names the methodology-layer ID convention. Lean-eval cross-candidate ID-stability comparison has no spec anchor. |
| H-2 | `00-synthesis.md` §2.5 + Round-2 §1.2 strengthening | **Self-improving prompts pattern** (Klaassen frustration-detector; Tedesco Montaigne) | 0 specs name pattern. "Klaassen" appears once (BF-L §6, non-pattern citation). | **load-bearing-gap** | Documented, reproducible methodology pattern (prompt analysis + rewrite loop). v3 absorbs knowledge-promotion via D-3 / ADR 0023 but no spec carries prompt-self-improvement as methodology obligation. |
| H-3 | `00-synthesis.md` §5.1 | **Pulse report** (per-window production-outcome read; compound-engineering's downstream loop closer) | 0 specs (`grep 'Pulse\|pulse report'` = 0); also absent from `failure-modes-v3.md`. | **load-bearing-gap** | Closes maintenance loop on production data → spec amendment (related to F20). BF-L P-13 maintenance loop is closest substrate analog but BF-L spec doesn't name pulse-report or production observability. |
| H-5 | `13-round-2-synthesis.md` §1.1 C11 | **Scaffold vs harness layer split (C11)** | 0 specs use canonical Round-2 vocabulary. "harness" in 2 specs, "scaffold" in 4 (different contexts). | **load-bearing-gap** | Round-2 promoted consensus item. v3 substrate ADRs effectively distinguish layers but no spec uses canonical Round-2 mapping. Operator coming from Round-2 synthesis may be confused. |
| H-8 | `00-synthesis.md` §5.2 + `02-compound-atelier.md` §4.6 | **Prompt-self-improver named methodology role** (distinct from H-2 pattern: the role, not the pattern) | 0 specs name role. | **load-bearing-gap** | Atelier §4.6 explicitly enumerates as a role. No v3 spec carries methodology-role enumeration that includes prompt-self-improver. Paired with H-2. |
| H-4 | `00-synthesis.md` §5.1 + `01-specification-refinery.md` §6.3 | **Showboat / trajectory-as-reviewable-artifact framing** | Trajectory CAPTURE absorbed (P-05 in all 10 specs); Showboat-specific artifact-of-record framing absent. | **silent-omission** | Capture-as-substrate universally absorbed; Refinery-flavored artifact-of-record framing subsumed by generic P-05. Borderline `mandate-rejection`. |
| H-6 | `00-synthesis.md` + Round-2 §C12 | **Specs-as-source-code doctrinal framing (Sean Grove)** | 0 specs name Sean Grove or use source-code analogy. D-1 carries the claim. | **silent-omission** | D-1 default carries the load-bearing claim; lineage attribution lost. Not material to design; Phase-8 reviewer asking "where does v3 say specs are source code?" finds no spec-level statement. |
| H-10 | `00-synthesis.md` §3.7 + `04-evolutionary-tournament.md` §3.4 | **Provider-aligned profiles (Attractor stance: do NOT unify provider tool interfaces)** | 0 specs. v3 invokes P-14 (LiteLLM-backed; cross-provider) without taking stance. | **silent-omission** | Minority but load-bearing position with practical consequences. Phase-8 lean-eval choosing between candidates may care. |
| H-12 | `00-synthesis.md` §5.4 | **Discoverability gate** (knowledge stores reachable from AGENTS.md or gate fails) | 0 specs (`grep 'discoverability'` = 0). AGENTS.md in 9 specs as project-conventions, not gate. | **silent-omission** | Enforced project-wide via AGENTS.md but no spec carries as methodology-level closure gate. Atelier §6 lists as load-bearing. |
| H-16 | `04-evolutionary-tournament.md` §3.4 + Round 1 §C10 | **Model-family diversity as structural population-level genome property** (not just judge-vs-builder) | 5 specs invoke cross-model judging via P-14/F46/ADR 0018; none invoke population-level structural-diversity. | **silent-omission** | Cross-model judging absorbed at judge-router substrate; population-level structural-diversity framing absent. Borderline `mandate-rejection`. |
| H-7 | `00-synthesis.md` §5.2 | **Diagnostician / Healer role + medical metaphor** (El Kaim; production-trace-to-spec-amendment) | 0 specs (El Kaim cited 4 specs but not this role). | **mandate-rejection** | `00-comparison.md` §8 explicitly names production-observability as v3-inherited gap. No v3 candidate claims production-observability axis. |
| H-9 | `00-synthesis.md` §2.8 + `02-compound-atelier.md` §5.2 + Round-2 strengthening | **Tiered ceremony (Lightweight / Standard / Deep / Deep-product)** | 0 specs. | **mandate-rejection** | v3's mandate-fit matrix per work-unit-class (DEC-2) supersedes Atelier ceremony tiers. Defensible rejection. |
| H-17 | `research-plan.md` §3-step | **"Run the §6 lean evaluation first" recommendation** | 0 specs; Phase-8 lean-eval surface in v1.2 plan IS the v3 fulfillment (plan-level, not spec-level). | **mandate-rejection** | Process-pipeline-level recommendation; not architectural. Per BF-S exemplar §2. |
| H-18 | `research-plan.md` ¶1-3 | **Three-layer pipeline (reports → synthesis → architectures) + folding policy** | 0 specs; absorbed at v3 synthesis-pipeline level via Phases 1-6. | **mandate-rejection** | Synthesis-pipeline framing, not architectural. Per BF-S exemplar §2. |
| H-11 | `02-compound-atelier.md` §4.1-4.5 | **Workshop chain (specialized persona workshops + reviewer panel + synthesizer chain)** | 0 specs. v3 absorbs cross-model judging via P-14 / ADR 0018. | **not-load-bearing-rejection** | Atelier-architecture-specific. v3's archive-and-rebuild discipline explicitly avoided. |
| H-13 | `03-phase-gated-foundry.md` §2-§4 | **SRS / SAD / DD / TRS formal phase artifacts** | 0 specs. | **not-load-bearing-rejection** | Foundry-specific structured-document templates. Defensible rejection across all 10. |
| H-14 | `03-phase-gated-foundry.md` §6.1-6.2 + `00-comparison.md` §4.2 | **Cleanroom V&V independence + gate-board / gate-chair structure** | 0 specs. Cross-model V&V IS absorbed via F46 + ADR 0018; gate-chair role + V&V org structure not. | **not-load-bearing-rejection** | Foundry-specific phase-gated process structure. |
| H-15 | `04-evolutionary-tournament.md` §3 + §5.3 | **Genome library / Predator agent / tournament bracket / Geneticist role** | 0 specs (Tournament only in BF-S §4 as methodology-layer plug-in framing). Cross-model diversity IS absorbed (F46 / ADR 0018 / P-14). | **not-load-bearing-rejection** | Tournament-specific primitives correctly rejected per archive-and-rebuild discipline. |

**Tally:** 5 load-bearing-gaps (H-1, H-2, H-3, H-5, H-8); 5 silent-omissions (H-4, H-6, H-10, H-12, H-16); 4 mandate-rejections (H-7, H-9, H-17, H-18); 4 not-load-bearing-rejections (H-11, H-13, H-14, H-15). 18 findings total.

### §B.2 Phase-5-close handoff erratum-sweep (Phase-6-followup #3)

**Method.** For each row in the [Phase-5-close handoff per-candidate ADR set table](../SESSION-HANDOFF-2026-05-25-phase-5-close.md#candidate-set-state-at-phase-5-close), compare against spec §0 ADR-citation index. Flag rows misassigning ADRs **beyond** the known BF-M / 0049 erratum.

**Reading convention.** Handoff shorthand: "Common substrate set" = Wave 5.1a (0010-0017, 8 ADRs); discipline (0018-0027) listed explicitly; framework / 2-cand-fold / designed-system ADRs (0028-0036 from Wave 5.1b) named individually only when surfaced; orphan / per-variant (0037-0064) named individually.

| Row | Handoff lists (variant/orphan/fold portion) | Spec §0 actual (variant/orphan/fold portion) | Erratum-class |
|---|---|---|---|
| GF-S | 0037 + 0038 + 0039 | **0028** (framework, paired) + **0032** (designed-system) + 0037 + 0038 + 0039 | under-statement (framework + designed-system omitted; per-variant pairing-recoverable) |
| GF-M | 0040 + 0041 | 0040 + 0041 | **match** |
| GF-C | 0042 + 0043 + 0044 | **0032** + 0042 + 0043 + 0044 | minor under-statement |
| BF-S | 0033 + 0035 | **0031** + 0033 + 0035 | minor under-statement |
| BF-M | 0033 + 0034 + 0045 + 0046 + **0049** | **0031** + **0032** + 0033 + 0034 + 0045 + 0046 (**NO 0049**) | **KNOWN ERRATUM** (already corrected) + handoff omits 0031+0032 (under-statement) |
| BF-L | 0034 + 0035 + 0047 + 0048 + 0049 | **0028** + **0031** + 0034 + 0035 + **0036** + 0047 + 0048 + 0049 | **material under-statement** — 0028 + 0036 omitted; 0028 is framework paired with per-variant 0049; 0036 is the Phase-6 Finding-2 consumed-only commodity dispatch |
| U-A | 0050 + 0051 + 0052 + 0053 | **0028 + 0029 + 0030 + 0036** + 0050 + 0051 + 0052 + 0053 | under-statement (frameworks paired-recoverable from per-variants) |
| U-B | 0054 + 0055 + 0056 | **0029 + 0030** + **0031** + 0054 + 0055 + 0056 | under-statement |
| U-C | 0057 + 0058 + 0059 | **0028 + 0029** + **0031 + 0032** + 0057 + 0058 + 0059 | under-statement |
| D7-U-1 | 0060 + 0061 + 0062 + 0063 + 0064 | **0029 + 0030 + 0036** + 0060 + 0061 + 0062 + 0063 + 0064 | under-statement |

**Erratum-sweep summary.**

- **1 known erratum (already corrected):** BF-M / 0049 row.
- **2 rows worth surfacing as erratum-extensions** (beyond the known erratum):
  1. **BF-M row supplement:** the existing 0049 erratum should also note the handoff omits 0031 + 0032 (under-statement, not misattribution).
  2. **BF-L row:** material under-statement. Handoff omits framework 0028 (paired with per-variant 0049 in spec) and framework 0036 (consumed-only commodity dispatch — the Phase-6-close verifier Finding-2 carry-forward). Worth a new erratum line.
- **7 rows show under-statement pattern** (framework + designed-system ADRs omitted): GF-S, GF-C, BF-S, U-A, U-B, U-C, D7-U-1. **Not erratum** because per-variant pairings make framework citations recoverable; but a documentation-hygiene pass could expand the handoff table.
- **Zero NEW row-level misattributions** in the BF-M / 0049 erratum class. The known erratum is the only ADR misattribution; the rest is shorthand-under-statement.

## §C Recommendations

### §C.1 Per-finding lead-agent reconciliation

- **Highest-priority gap: H-1 (stable-ID lettering R/A/F/AE/U/S/K).** Methodologically load-bearing, named in two archive files, only partially absorbed by P-22 + P-24 substrate substitution. Consider §6 open-carry in at least one candidate naming the methodology-layer ID convention.
- **H-2 + H-8 paired (self-improving prompts pattern + prompt-self-improver role).** Methodology-rich candidates (GF-S / GF-M / U-A) should claim or explicitly reject.
- **H-3 (Pulse report) and H-12 (discoverability gate)** as silent-omissions worth one-line §6 open-carries. BF-L (P-13 maintenance loop) is natural home for pulse-report-style production-feedback.
- **H-5 (scaffold vs harness vocabulary)** as glossary item in `decisions-captured.md` (substrate ≈ harness; AGENTS.md ≈ scaffold).
- **Confirm rejection of H-11 / H-13 / H-14 / H-15** as `not-load-bearing-rejection`. Architecture-specific primitives v3 archive-and-rebuild discipline correctly avoids.
- **Confirm rejection of H-7 / H-9 / H-17 / H-18** as `mandate-rejection`. Defensible per scoping.
- **H-4 / H-6 / H-10 / H-16** are borderline silent-omission / mandate-rejection. Per [auto-007 §Bias-direction discipline](../decisions/auto-007-phase-7-dispatch-shape.md#bias-direction-discipline) "be generous to archive items", lean toward `silent-omission` at aggregation.

### §C.2 Phase-5-close handoff erratum extension

Lead agent should consider extending the [Phase-6-close handoff's existing erratum section](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#adr-0049-documentation-erratum) with two items:

1. **BF-M row supplement:** existing 0049 erratum should also acknowledge the handoff row omits 0031 + 0032 designed-system ADRs (under-statement).
2. **BF-L row:** new erratum line. Handoff omits framework 0028 (paired with per-variant 0049 in spec) and framework 0036 (consumed-only dispatch — Finding-2 carry-forward). Material because the Phase-6-close verifier Finding-2 carry-forward depends on the 0036 framing.

Optional: documentation-hygiene pass extending all 10 handoff rows to mirror spec §0 row counts. **Defer** — out of Phase-7 scope; future meta-governance carry-forward.

### §C.3 Bias-direction-protected items (informational; not gap findings)

For aggregation completeness, the following archive items are **known-rejected v3 items** per [auto-007 §Bias-direction discipline](../decisions/auto-007-phase-7-dispatch-shape.md#bias-direction-discipline) and are correctly absent from all 10 specs; the historian does NOT flag them as gaps:

- **OpenHands SDK + Overstory-design-in-Python as substrate stack** (Round-2 §6.2 / §8). Explicitly excluded per `constraints-extracted.md`. Per-candidate verdict: `rejected (explicitly-excluded-per-constraints-extracted)`.
- **Compound Atelier as baseline + selective borrows** (`00-comparison.md` §7). Explicitly anchor-avoided per archive-and-rebuild discipline. Per-candidate verdict: `rejected (explicitly-anchor-avoided)`.

### §C.4 Method limitations

- Paragraph-or-shorter granularity may miss sub-paragraph items.
- "Zero specs in any form" is judgement; bias-direction in close calls is toward `silent-omission` (false-positive gap) rather than missing real gaps.
- Erratum-sweep is bound to ADR-ID misattributions; broader handoff-quality issues out of scope.

## §D References

**Phase-7 dispatch + precedent:**
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md), [`architectures/v3/backfill-notes/bf-s.md`](bf-s.md), [`architectures/v3/phase-6-verification-findings.md`](../phase-6-verification-findings.md).

**Phase-6 specs (all 10):** [`gf-s.md`](../specs/gf-s.md), [`gf-m.md`](../specs/gf-m.md), [`gf-c.md`](../specs/gf-c.md), [`bf-s.md`](../specs/bf-s.md), [`bf-m.md`](../specs/bf-m.md), [`bf-l.md`](../specs/bf-l.md), [`u-a.md`](../specs/u-a.md), [`u-b.md`](../specs/u-b.md), [`u-c.md`](../specs/u-c.md), [`d7-u-1.md`](../specs/d7-u-1.md).

**Archive (9 files):** [`research-plan.md`](../../../archive/research-plan.md), [`synthesis-v1-v2/00-synthesis.md`](../../../archive/synthesis-v1-v2/00-synthesis.md), [`synthesis-v1-v2/13-round-2-synthesis.md`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md), [`architectures-v2/00-comparison.md`](../../../archive/architectures-v2/00-comparison.md), [`architectures-v2/01-specification-refinery.md`](../../../archive/architectures-v2/01-specification-refinery.md), [`architectures-v2/02-compound-atelier.md`](../../../archive/architectures-v2/02-compound-atelier.md), [`architectures-v2/03-phase-gated-foundry.md`](../../../archive/architectures-v2/03-phase-gated-foundry.md), [`architectures-v2/04-evolutionary-tournament.md`](../../../archive/architectures-v2/04-evolutionary-tournament.md), [`architectures-v2/failure-modes.md`](../../../archive/architectures-v2/failure-modes.md).

**Handoffs (erratum-sweep inputs):**
- [`SESSION-HANDOFF-2026-05-25-phase-5-close.md`](../SESSION-HANDOFF-2026-05-25-phase-5-close.md#candidate-set-state-at-phase-5-close) — per-candidate ADR table audited.
- [`SESSION-HANDOFF-2026-05-26-phase-6-close.md`](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#adr-0049-documentation-erratum) — known-erratum reference.

**Constraints (bias-direction-protected items):** [`constraints-extracted.md`](../constraints-extracted.md).

**AGENTS.md rule referenced:** [framework-ADR scope-boundary discipline](../../../AGENTS.md#framework-adr-scope-boundary-discipline) (basis for BF-L 0028 + 0036 framing finding in §B.2).
