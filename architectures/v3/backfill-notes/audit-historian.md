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
  - archive/architectures-v2/01-specification-refinery.md (skimmed, no full re-extraction)
  - archive/architectures-v2/02-compound-atelier.md (skimmed)
  - archive/architectures-v2/03-phase-gated-foundry.md (skimmed)
  - archive/architectures-v2/04-evolutionary-tournament.md (skimmed)
  - architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5-close.md (per-candidate ADR table)
  - architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md (erratum reference)
  - architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md (dispatch brief)
  - architectures/v3/backfill-notes/bf-s.md (exemplar)
  - architectures/v3/phase-6-verification-findings.md (output-format precedent)
gap-finding-counts:
  load-bearing-gap: 5
  not-load-bearing-rejection: 6
  mandate-rejection: 4
  silent-omission: 3
handoff-erratum-rows-flagged: 2  # beyond the already-known BF-M / 0049 row
verdict: PASS WITH AMENDMENTS  # informational; lead agent reconciles at aggregation
---

# Historian audit — Phase 7 bias-guard

## §A Scope

**Mandate (base).** Per [auto-007 §Wave 7.2 historian description](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2): enumerate archive items appearing in **zero Phase-6 specs in any form** (no citation, no equivalent content, no rephrased presence). Independent gap detection — complement of the silent-absorption auditor (which finds material in specs without cites; the historian finds material that is in no spec at all).

**Mandate (expanded per Reviewer 6 D-H3).** Also perform a one-pass scan of the Phase-5-close handoff per-candidate ADR set table (`SESSION-HANDOFF-2026-05-25-phase-5-close.md` §"Candidate-set state at Phase 5 close") looking for documentation drift beyond the already-known BF-M / 0049 row (corrected in [Phase-6-close handoff erratum](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#adr-0049-documentation-erratum)).

**In scope.**

- All 10 Phase-6 specs at [`architectures/v3/specs/`](../specs/).
- All 9 archive files per [auto-007 §Common archive-file-to-path mapping](../decisions/auto-007-phase-7-dispatch-shape.md#common-archive-file-to-path-mapping).
- The Phase-5-close handoff per-candidate ADR set table.

**Not in scope.**

- Per-candidate verdicts on whether a gap is acceptable for that candidate (per-candidate fanout subagents own that read); the historian only flags absence in **all** specs.
- D-1 through D-7 default-verification (per-candidate §1.5 subagent responsibility).
- v3 non-spec files (`primitives/`, `failure-modes-v3.md`, `decisions-captured.md`, `candidate-registry.md`, `tracks/`, `contradictions.md`); the audit is against specs only because specs are the load-bearing Phase-6 output that Phase 8 lean-eval consumes. Where an item is absent from specs but present in a v3 non-spec file, the gap is flagged as `silent-omission` (load-bearing material lives outside specs and may not propagate to lean-eval).
- Bias-direction-protected known-rejected items per [auto-007 §Bias-direction discipline](../decisions/auto-007-phase-7-dispatch-shape.md#bias-direction-discipline) (OpenHands+Overstory substrate stack; Compound Atelier as baseline). These are *deliberately* absent from all specs and are NOT historian findings; they are noted once in §C for reconciliation completeness.

**Method.** (i) For each archive file, identify named items (claims, framings, primitives, recommendations, F-modes) at a paragraph-or-shorter granularity. (ii) Run `grep -lc <token-or-paraphrase>` across the 10 specs for each item. (iii) Item is a gap iff zero specs match AND no semantic equivalent appears (judgement call; rationale recorded per finding). (iv) Classify the gap per `recommended-action` categories defined below.

**Recommended-action taxonomy** (per auto-007 §B.1 rubric):

- `load-bearing-gap` — the item is methodologically important and the absence may materially affect Phase-8 lean-eval. Lead agent should consider whether at least one candidate should claim or address it.
- `not-load-bearing-rejection` — the item is a v3-rejected recommendation/framing/primitive; absence is correct. Includes the known-rejected substrate-stack items.
- `mandate-rejection` — the item is structurally inapplicable to all 10 candidate mandates (e.g., research-process discipline at the synthesis-pipeline layer rather than at the architectural layer).
- `silent-omission` — the item is absorbed into v3 non-spec material (`failure-modes-v3.md`, `decisions-captured.md`, etc.) but never propagates into any spec; lean-eval may miss it.

## §B Findings

### §B.1 Archive items appearing in zero specs (gap findings)

Each row: archive-source + item + grep witness + recommended-action + rationale.

| # | Archive source | Archive item | Spec presence | Recommended action | Rationale |
|---|---|---|---|---|---|
| H-1 | `00-synthesis.md` §5.5 + `02-compound-atelier.md` §6.1 | **Stable-identifier discipline (R/A/F/AE/U/S/K stable-ID lettering)** | 0 specs (`grep -c 'R/A/F/AE\|stable-ID\|stable identifier' specs/*.md` = 0). Only `contradictions.md` carries the lettering. | **load-bearing-gap** | Every v2 architecture treats stable IDs as load-bearing (F11 closure). Specs adopt P-22 symbol-range index + P-24 attribution envelope as the substrate substitution, but **no spec names the methodology-layer R/A/F/AE/U/S/K convention**. BF-S §3 mentions "per-symbol granularity via P-22" but doesn't tie back to the canonical stable-ID lettering scheme. Phase-8 lean-eval that needs to compare methodology-layer ID stability across candidates has no spec-level reference. Lead agent should consider a one-row open-carry in at least one candidate's §6 (GF-M, BF-S, or U-B are natural homes since they have the strongest knowledge-promotion / stable-ID workflows). |
| H-2 | `00-synthesis.md` §2.5 + Round-2 §1.2 §2.5 strengthening | **Self-improving prompts pattern** (Klaassen frustration-detector; Tedesco Montaigne; Klaassen named once in BF-L §6 only, not as the pattern) | 0 specs name "self-improving prompts" or the frustration-detector pattern. "Klaassen" hits once (BF-L §6) as a non-pattern citation. | **load-bearing-gap** | Round-1 + Round-2 syntheses both list self-improving prompts as a documented, reproducible pattern (Klaassen + Tedesco are concrete examples). The pattern is methodology-layer (prompt analysis + rewrite loop). v3 specs absorb knowledge-promotion via D-3 / ADR 0023 but no spec carries the prompt-self-improvement loop as a methodology obligation or primitive. Could be Phase-8 candidate methodology surface or an explicit §6 open carry. |
| H-3 | `00-synthesis.md` §5.1 | **Pulse report** (per-window outcome read; compound-engineering's downstream loop closer; named in §5.1 artifact stack) | 0 specs (`grep -c 'Pulse\|pulse report\|pulse_report'` = 0). Not in `failure-modes-v3.md` either. | **load-bearing-gap** | Listed as a canonical artifact-stack element in 00-synthesis §5.1. Closes the maintenance loop on production data → spec amendment (related to F20 maintenance asymmetry). BF-L's P-13 maintenance loop is the substrate-level analog, but BF-L spec doesn't name "pulse report" or address production observability. None of the brownfield specs (BF-S/BF-M/BF-L) carry production-trace-to-spec-amendment as an explicit primitive. Lead agent should consider whether BF-L or D7-U-1 specs should call this out in §6 open carries. |
| H-4 | `00-synthesis.md` §5.1 + `01-specification-refinery.md` §6.3 + `13-round-2-synthesis.md` Round-1-corpus row | **Showboat / trajectory-as-artifact** (per-cycle trajectory artifact for review; named in Round-1 + Refinery) | 0 specs (`grep -c 'Showboat\|showboat'` = 0). Trajectory CAPTURE is bound to P-05 (ADR 0012) in every spec, but the "trajectory-as-reviewable-artifact" framing is absent. | **silent-omission** | Trajectory capture as substrate primitive is universally absorbed (P-05 in all 10 specs). The Showboat-specific artifact-of-record framing is Refinery-flavored and arguably subsumed by the generic P-05 trajectory store. Bordering on `mandate-rejection` but the trajectory-as-artifact concept influences methodology design; flagging for lead-agent reconciliation. |
| H-5 | `13-round-2-synthesis.md` §1.1 C11 | **Scaffold vs harness layer split (C11)** | 0 specs use the canonical 2-layer "scaffold = pre-runtime / harness = runtime" vocabulary (`grep -l 'scaffold' = 4 specs` but in different contexts). "harness" appears in 2 specs only. | **load-bearing-gap** | C11 is a Round-2 promoted consensus item. The v3 substrate ADRs (0010-0017) effectively distinguish the layers (sandbox / cost-ceiling = harness; AGENTS.md = scaffold), but no spec uses the canonical Round-2 vocabulary. Operator coming from the Round-2 synthesis may be confused that v3 specs talk about "substrate" and "methodology" without explicitly mapping these to scaffold/harness. Lead agent should consider adding a glossary item to one or two specs OR to `decisions-captured.md`. |
| H-6 | `00-synthesis.md` §5.1 + Round-2 §C12 | **Specs-as-source-code doctrinal framing (Sean Grove citation)** | 0 specs name "Sean Grove" or use "specs-as-source-code" framing. v3 absorbs D-1 (specs durable) but not the source-code analogy. | **silent-omission** | D-1 default carries the same load-bearing claim. Sean Grove + BMAD Living Artifacts attribution lost. Not material to architectural design (lineage attribution is research-pipeline territory), but a Phase-8 reviewer asking "where does v3 say specs are source code?" finds no spec-level statement. |
| H-7 | `00-synthesis.md` §5.2 | **Diagnostician / Healer role + medical metaphor** (El Kaim attribution; production-trace-to-spec-amendment) | 0 specs (`grep -c 'Healer\|Diagnostician'` = 0). El Kaim cited in 4 specs but not for this role. | **mandate-rejection** | The Healer/Diagnostician role is production-observability-flavored and was named as an explicit gap in `00-comparison.md` §8 ("Production observability") with v3 inheriting the gap. None of the 10 v3 candidates claim production-observability as a load-bearing axis; the closest is BF-L's maintenance loop (P-13). Defensible as `mandate-rejection` for all 10. Lead agent confirms. |
| H-8 | `00-synthesis.md` §5.2 + `02-compound-atelier.md` §4.6 | **Prompt-self-improver role** (a special-case knowledge curator that rewrites instructions) | 0 specs name this role. Related to H-2 (self-improving prompts pattern). | **load-bearing-gap** | Distinct from H-2: H-2 is the pattern; H-8 is the **named methodology role**. Atelier §4.6 explicitly enumerates it as a role. No v3 spec carries a methodology-role enumeration that includes the prompt-self-improver. Lead agent should consider whether at least one candidate (GF-S, GF-M, or U-A as methodology-rich candidates) should claim or explicitly reject this role. |
| H-9 | `00-synthesis.md` §2.8 + `02-compound-atelier.md` §5.2 + Round-2 §1.2 §2.8 | **Tiered ceremony (Lightweight / Standard / Deep / Deep-product)** | 0 specs (`grep -c 'Lightweight\|Deep-product\|tiered ceremony'` = 0). "Standard" appears in 3 specs as commodity-baseline language. | **mandate-rejection** | Tiered-ceremony discipline is Atelier-methodology-flavored. v3's mandate-fit matrix per work-unit-class (DEC-2) provides the v3 substitution: instead of one method scaling across work-unit-classes via ceremony tiers, v3 distinguishes greenfield-mvp vs greenfield-post-mvp-evolution vs refactor vs change-request vs regression-fix and lets candidates have per-work-unit-class verdicts. Defensible as `mandate-rejection`: the v3 abstraction supersedes the Atelier abstraction. Lead agent confirms. |
| H-10 | `00-synthesis.md` §3.7 + `04-evolutionary-tournament.md` §3.4 | **Provider-aligned profiles (Attractor stance: do not unify provider tool interfaces)** | 0 specs. v3 specs are silent on whether tools are unified across providers or aligned per-family. | **load-bearing-gap** | Attractor's stance is a load-bearing minority position with practical consequences (a factory that unifies provider interfaces loses 10-30% capability per Round 1). v3 specs invoke P-14 judge router (LiteLLM-backed; cross-provider) without taking a stance on tool-interface unification. Phase-8 lean-eval choosing between candidates may care. |
| H-11 | `00-synthesis.md` §5.2 + `02-compound-atelier.md` §4.1-4.5 | **Workshop chain (specialized persona workshops + reviewer panel + synthesizer chain)** as a named cyclic primitive | 0 specs (`grep -c 'Workshop chain\|Workshop'` = 0). "Reviewer panel" 0 specs. "Synthesizer" 0 specs. | **not-load-bearing-rejection** | The workshop chain is Atelier-architecture-specific. v3's archive-and-rebuild discipline explicitly avoided architecture-specific primitives. v3 absorbs cross-model judging via P-14 (ADR 0016) + bias-guard discipline (ADR 0018) — which is the substrate-level abstraction the persona-panel pattern motivates. Defensible rejection. |
| H-12 | `00-synthesis.md` §5.4 | **Discoverability gate** (knowledge stores must be reachable from AGENTS.md or the gate fails) | 0 specs (`grep -c 'discoverability'` = 0). AGENTS.md mentioned in 9 specs as a project-conventions surface, not as a discoverability gate. | **silent-omission** | The discoverability discipline is enforced project-wide via AGENTS.md, but no spec carries it as a methodology-level closure gate. Compound-engineering Atelier §6 lists discoverability gate as a load-bearing primitive. Absorbed via v3's AGENTS.md infrastructure but not in any spec. Lead agent reconciles. |
| H-13 | `03-phase-gated-foundry.md` §2-§4 | **SRS / SAD / DD / TRS formal phase artifacts** | 0 specs (`grep -c 'SRS\|SAD\|DD \|TRS\|formal templates'` = 0). | **not-load-bearing-rejection** | Foundry-specific structured-document templates. v3's archive-and-rebuild discipline explicitly avoided Foundry-shaped methodology assumptions. Defensible rejection across all 10 candidates. |
| H-14 | `03-phase-gated-foundry.md` §6.1-6.2 + `00-comparison.md` §4.2 | **Cleanroom V&V independence + gate-board / gate-chair structure** | 0 specs (`grep -c 'Cleanroom\|gate chair\|gate board'` = 0). | **not-load-bearing-rejection** | Foundry-specific phase-gated process structure. The cross-model V&V independence concept IS absorbed via F46 + ADR 0018 (cross-model judging) in 9 specs; the Foundry-specific gate-chair role + V&V org structure is not. Defensible rejection. |
| H-15 | `04-evolutionary-tournament.md` §3 + §5.3 | **Genome library / Predator agent / tournament bracket / Geneticist role** | 0 specs (`grep -c 'genome library\|predator agent\|tournament bracket\|Geneticist'` = 0). "Tournament" only in BF-S §4 (methodology-layer plug-in framing). | **not-load-bearing-rejection** | Tournament-specific architectural primitives. Cross-model diversity discipline IS absorbed (F46 / ADR 0018 / P-14). Tournament-specific primitives are correctly rejected per v3's archive-and-rebuild discipline. Defensible. |
| H-16 | `04-evolutionary-tournament.md` §3.4 + `00-comparison.md` §2.1 | **Model-family diversity as structural (population-level genome diversity policy)** | Partial: 5 specs mention "model-family diversity" via P-14 / F46 / ADR 0018 cross-model judging. None invoke it as a **structural genome property**. | **silent-omission** | Cross-model judging absorbed at the judge-router substrate (P-14) and bias-guard discipline (ADR 0018); the population-level structural-diversity framing (genome-wide, not just judge-vs-builder) is absent. Bordering on `mandate-rejection`. Lead agent reconciles. |
| H-17 | `research-plan.md` §3-step | **"Run the §6 lean evaluation first" recommendation** (1-day manual run of the discipline before building any orchestration) | 0 specs. The Phase-8 lean-eval surface in the v1.2 plan IS the v3 fulfillment of this recommendation; it lives at the **plan** level, not in any spec. | **mandate-rejection** | Process-pipeline-level recommendation. Synthesis-pipeline discipline; not architectural. Defensible per scoping. The Phase-7 brief itself defers to Phase-8 lean-eval per candidate. No spec gap. |
| H-18 | `research-plan.md` paragraphs 1-3 | **Three-layer pipeline (reports → synthesis → architectures)** + folding policy | 0 specs. Already absorbed at the v3 synthesis-pipeline level via Phases 1-6. | **mandate-rejection** | Synthesis-pipeline framing, not architectural. Per BF-S exemplar §2 classification; defensible. |

### §B.2 Phase-5-close handoff erratum-sweep (Phase-6-followup #3)

**Method.** For each row in the Phase-5-close handoff's per-candidate ADR set table (rows GF-S through D7-U-1 inclusive), compare against the candidate's actual spec §0 ADR-citation index (extracted via grep). Flag rows that misassign ADRs in a way that would mislead a reader **beyond** the already-known BF-M / 0049 row.

**Reading convention.** The handoff uses the shorthand "Common substrate set" = Wave 5.1a (ADRs 0010-0017, 8 ADRs); discipline ADRs 0018-0027 explicitly listed; framework + 2-candidate-fold + designed-system ADRs (0028-0036 from Wave 5.1b) named individually only when the row's author chose to surface them; orphan / per-variant ADRs (0037-0064) named individually.

| Row | Handoff text | Actual spec §0 | Erratum-class | Recommended action |
|---|---|---|---|---|
| GF-S | "9 commodity-substrate ADRs (0010-0017 subset) + 0018-0027 discipline ADRs + 0037 P-10 orphan + 0038 P-15 orphan + 0039 P-19 variant" | Actual: 0010-0017 + 0018-0027 + 0028 (P-19 framework) + 0032 (P-12 designed-system) + 0037 + 0038 + 0039 (= 23 ADRs total) | **non-erratum** (handoff-shorthand) | Handoff omits **0028 framework** AND **0032 designed-system** but the framework-ADR is paired with the per-variant 0039 in the spec per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline). Spec is correct; handoff under-states. Not erratum per se but a reader using the handoff cannot reconstruct that GF-S carries framework 0028; if Phase-7-followup does a documentation-hygiene pass, surface this. |
| GF-M | "Common substrate set + discipline set + 0040 P-20 orphan + 0041 P-21 orphan" | Actual: 0010-0017 + 0018-0027 + 0040 + 0041 (= 20 ADRs). **Match** with handoff shorthand. | **match** | No action. |
| GF-C | "Common substrate set + discipline set + 0042 P-11 + 0043 P-17 + 0044 P-18 orphans" | Actual: 0010-0017 + 0018-0027 + **0032 (P-12 designed-system)** + 0042 + 0043 + 0044 (= 23 ADRs). | **minor under-statement** | Handoff omits 0032 (P-12 designed-system substrate). GF-C's spec annotation says "GF-C carries no framework-ADR + per-variant pairs" and lists 0032 in §0 as a designed-system primitive, not a commodity-common. If Phase-7-followup does a hygiene pass, surface. |
| BF-S | "Common substrate set + discipline set + 0033 P-25 (2-cand fold) + 0035 P-24 (2-cand fold)" | Actual: 0010-0017 + 0018-0027 + **0031 (P-23 designed-system)** + 0033 + 0035 (= 21 ADRs). | **minor under-statement** | Handoff omits 0031 (P-23 dependency-impact graph). BF-S's spec §0 lists 0031 explicitly. Hygiene-pass candidate. |
| BF-M | "Common substrate set + discipline set + 0033 + 0034 P-27 (2-cand fold) + 0045 P-03 + 0046 P-04 + **0049 P-19/BF-M variant**" | Actual: 0010-0017 + 0018-0027 + **0031** + **0032** + 0033 + 0034 + 0045 + 0046 (= 24 ADRs). **NO 0049.** | **KNOWN ERRATUM** (already corrected per [Phase-6-close handoff erratum](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#adr-0049-documentation-erratum)) | The 0049 error is already documented. **Additional non-erratum drift:** handoff omits **0031 + 0032 designed-system substrates**. Worth a one-line addition to the existing erratum note. |
| BF-L | "Common substrate set + discipline set + 0034 + 0035 (via P-26) + 0047 P-26 + 0048 P-13 + 0049 P-19/BF-L variant" | Actual: 0010-0017 + 0018-0027 + **0028 (P-19 framework as commodity dispatch)** + **0031 (P-23 designed-system)** + 0034 + 0035 + **0036 (P-30 commodity dispatch)** + 0047 + 0048 + 0049 (= 26 ADRs). | **material under-statement / candidate erratum** | Handoff omits **0028 (P-19 framework)**, **0036 (P-30 framework)**, and **0031 (P-23 designed-system)**. The 0028 + 0036 omissions are material because they are the framework ADRs paired with BF-L's per-variant 0049 (paired with 0028 in BF-L's §0) and consumed-only 0036 (the Phase-6 verifier Finding-2 carry-forward). The handoff reader does not learn that BF-L pairs 0028+0049 OR that BF-L consumes 0036 without per-variant pairing. **Flag for handoff-erratum extension.** |
| U-A | "Common substrate set + discipline set + 0050 P-19 variant + 0051 P-28 variant + 0052 P-29 variant + 0053 P-30 variant" | Actual: 0010-0017 + 0018-0027 + **0028 + 0029 + 0030 + 0036 (all four framework ADRs)** + 0050 + 0051 + 0052 + 0053 (= 26 ADRs). | **expected shorthand** (frameworks implied by per-variant pairings) | Handoff omits the 4 framework ADRs (0028 / 0029 / 0030 / 0036). For U-A this is a defensible shorthand because the per-variants name their framework via `Variant of`. But a stricter reading (per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline)) would surface the framework + per-variant pairing in the handoff row. Hygiene-pass candidate, not erratum. |
| U-B | "Common substrate set + discipline set + 0054 P-31 orphan + 0055 P-28 variant + 0056 P-29 variant" | Actual: 0010-0017 + 0018-0027 + **0029 + 0030 (framework ADRs)** + **0031 (P-23 designed-system)** + 0054 + 0055 + 0056 (= 24 ADRs). | **under-statement** | Handoff omits frameworks 0029 + 0030 (paired with per-variants 0055 + 0056 in spec) AND 0031. Same hygiene-pass pattern as U-A; not erratum. |
| U-C | "Common substrate set + discipline set + 0057 P-32 orphan + 0058 P-19 variant + 0059 P-28 variant" | Actual: 0010-0017 + 0018-0027 + **0028 + 0029 (frameworks)** + **0031 + 0032 (designed-system)** + 0057 + 0058 + 0059 (= 25 ADRs). | **under-statement** | Same pattern: handoff omits frameworks 0028 + 0029 and designed-system 0031 + 0032. Not erratum. |
| D7-U-1 | "Common substrate set + discipline set + 0060 P-33 orphan + 0061 P-34 orphan + 0062 P-28 variant + 0063 P-29 variant + 0064 P-30 variant" | Actual: 0010-0017 + 0018-0027 + **0029 + 0030 + 0036 (frameworks)** + 0060 + 0061 + 0062 + 0063 + 0064 (= 26 ADRs). | **under-statement** | Handoff omits frameworks 0029 + 0030 + 0036 (paired with per-variants 0062 + 0063 + 0064 in spec). Same pattern; not erratum. |

**Erratum-sweep summary.**

- **1 known erratum (already corrected):** BF-M / 0049 row attributes ADR 0049 to BF-M; specs correctly omit per the Phase-6-close handoff erratum note.
- **2 additional rows worth surfacing in a Phase-7-followup documentation-hygiene extension:**
  1. **BF-M row.** Add to the existing 0049 erratum a note that the handoff row also omits 0031 + 0032 (under-statement, not erratum).
  2. **BF-L row.** Handoff omits frameworks 0028 + 0036 paired/consumed in spec §0. Material because of the Phase-6-close handoff Finding-2 carry-forward (BF-L's 0036 framing). Flag as candidate erratum-extension.
- **6 rows show under-statement pattern** (omission of framework + designed-system ADRs): GF-S, GF-C, BF-S, U-A, U-B, U-C, D7-U-1. **Not erratum** because the per-variant pairings make the framework citations recoverable; but a documentation-hygiene extension could expand the handoff table to mirror the spec §0 row counts.
- **Zero NEW row-level misassignments** in the BF-M / 0049 erratum class. The known erratum is the only ADR misattribution; the rest is shorthand-under-statement.

## §C Recommendations

### §C.1 Per-finding lead-agent reconciliation (gap findings)

For lead-agent aggregation at fanout-close:

- **Treat H-1 (stable-ID lettering) as the highest-priority gap.** It is methodologically load-bearing, named in two archive files, and the v3 substrate substitution (P-22 + P-24) is only a partial absorption. Consider whether at least one candidate's spec needs a §6 open-carry naming the methodology-layer ID-stability convention.
- **Treat H-2 + H-8 (self-improving prompts pattern + prompt-self-improver role) as paired load-bearing gaps.** Both are documented and reproducible per Round 1 + Round 2 syntheses. Lead agent should consider whether GF-S / GF-M / U-A — the methodology-rich candidates — should claim or explicitly reject this pattern.
- **Treat H-3 (Pulse report) and H-12 (discoverability gate) as silent-omissions worth a one-line §6 open-carry.** BF-L (P-13 maintenance loop) is the natural home for pulse-report-style production-feedback; v3 AGENTS.md infrastructure is the natural home for discoverability gate.
- **Treat H-5 (scaffold vs harness vocabulary) as a glossary item.** Adding a one-line glossary mapping in `decisions-captured.md` (substrate ≈ harness; AGENTS.md ≈ scaffold) closes the C11 Round-2 consensus translation without a spec edit.
- **Confirm rejection of H-11 (workshop chain), H-13 (SRS/SAD/DD), H-14 (Cleanroom gate-board), H-15 (Genome/Predator) as `not-load-bearing-rejection`.** These are architecture-specific primitives the v3 archive-and-rebuild discipline correctly avoids. No reconciliation action.
- **Confirm rejection of H-7 (Healer), H-9 (tiered ceremony), H-17 (lean evaluation first), H-18 (three-layer pipeline) as `mandate-rejection`.** Defensible per scoping; no action.
- **H-4 (Showboat), H-6 (specs-as-source-code attribution), H-10 (provider-aligned profiles), H-16 (population-genome diversity)** are borderline `silent-omission` / `mandate-rejection`. Lead agent's call at aggregation time; lean toward `silent-omission` per the auto-007 §Bias-direction discipline ("be generous to archive items").

### §C.2 Phase-5-close handoff erratum extension

Lead agent should consider extending the Phase-6-close handoff's existing erratum section with two items:

1. **BF-M row supplement:** the existing 0049 erratum note should also acknowledge that the handoff row omits 0031 + 0032 designed-system ADRs (under-statement, not misattribution).
2. **BF-L row:** new erratum note. Handoff row omits framework 0028 (paired with per-variant 0049 in spec) and framework 0036 (consumed-only dispatch surface per Finding-2). Material because the Phase-6-close verifier Finding-2 carry-forward depends on the 0036 framing.

Optional: documentation-hygiene pass extending all 10 handoff rows to mirror spec §0 row counts. **Defer** — out of Phase-7 scope; carry-forward candidate for a future meta-governance PR if anyone complains the handoff under-states.

### §C.3 Bias-direction-protected items (informational; not gap findings)

For aggregation-completeness only, the following archive items are **known-rejected v3 items per [auto-007 §Bias-direction discipline](../decisions/auto-007-phase-7-dispatch-shape.md#bias-direction-discipline)** and are correctly absent from all 10 specs. The historian does NOT flag these as gaps:

- **OpenHands SDK + Overstory-design-in-Python as substrate stack** (Round-2 §6.2 / §8). Explicitly excluded per `constraints-extracted.md`. Per-candidate verdict: `rejected (explicitly-excluded-per-constraints-extracted)`.
- **Compound Atelier as baseline + selective borrows** (v2 `00-comparison.md` §7). Explicitly anchor-avoided per the archive-and-rebuild discipline. Per-candidate verdict: `rejected (explicitly-anchor-avoided)`.

These are bias-direction-protected; the per-candidate fanout subagents will independently flag them per the rubric; this historian audit acknowledges them once for cross-audit consistency.

### §C.4 Method limitations

- This audit operates at paragraph-or-shorter archive-item granularity. Some claims are sub-paragraph (e.g., specific factoids inside §2 of 00-synthesis.md) that the historian's enumeration did not break out individually. If lead agent or the silent-absorption auditor surface a sub-paragraph item absent from all specs, this audit will not have caught it.
- "Zero specs in any form" is a judgement call requiring keyword + paraphrase search; some absorptions may be at a higher abstraction level than this audit detected. The bias-direction in such close calls is toward `silent-omission` (false-positive gap) rather than missing a real gap (false-negative).
- The Phase-5-close handoff per-candidate ADR table erratum-sweep is bound to ADR-ID misattributions; broader handoff-quality issues (e.g., outdated phase status, broken links) are out of scope.

## §D References

**Phase-7 dispatch + rubric:**
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — dispatch brief; §Decision (Round 2) defines historian mandate.
- [`architectures/v3/backfill-notes/bf-s.md`](bf-s.md) — exemplar (context).
- [`architectures/v3/phase-6-verification-findings.md`](../phase-6-verification-findings.md) — output-format precedent.

**Phase-6 specs audited (all 10):**
- [`architectures/v3/specs/gf-s.md`](../specs/gf-s.md), [`gf-m.md`](../specs/gf-m.md), [`gf-c.md`](../specs/gf-c.md), [`bf-s.md`](../specs/bf-s.md), [`bf-m.md`](../specs/bf-m.md), [`bf-l.md`](../specs/bf-l.md), [`u-a.md`](../specs/u-a.md), [`u-b.md`](../specs/u-b.md), [`u-c.md`](../specs/u-c.md), [`d7-u-1.md`](../specs/d7-u-1.md).

**Archive (9 files):**
- [`archive/research-plan.md`](../../../archive/research-plan.md), [`archive/synthesis-v1-v2/00-synthesis.md`](../../../archive/synthesis-v1-v2/00-synthesis.md), [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md), [`archive/architectures-v2/00-comparison.md`](../../../archive/architectures-v2/00-comparison.md), [`archive/architectures-v2/01-specification-refinery.md`](../../../archive/architectures-v2/01-specification-refinery.md), [`archive/architectures-v2/02-compound-atelier.md`](../../../archive/architectures-v2/02-compound-atelier.md), [`archive/architectures-v2/03-phase-gated-foundry.md`](../../../archive/architectures-v2/03-phase-gated-foundry.md), [`archive/architectures-v2/04-evolutionary-tournament.md`](../../../archive/architectures-v2/04-evolutionary-tournament.md), [`archive/architectures-v2/failure-modes.md`](../../../archive/architectures-v2/failure-modes.md).

**Handoffs (erratum-sweep inputs):**
- [`architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5-close.md`](../SESSION-HANDOFF-2026-05-25-phase-5-close.md) — per-candidate ADR table audited.
- [`architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md`](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#adr-0049-documentation-erratum) — known-erratum reference.

**Constraints (bias-direction-protected items):**
- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — source for known-rejected substrate-stack flag.

**AGENTS.md rules referenced:**
- [`AGENTS.md` framework-ADR scope-boundary discipline](../../../AGENTS.md#framework-adr-scope-boundary-discipline) — basis for BF-L 0028 + 0036 framing finding in §B.2.
