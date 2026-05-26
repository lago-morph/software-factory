# Phase-6 verification findings

**Author.** Phase-6 verification subagent (combined Verifier-1 structural + Verifier-2 semantic-consistency scope per [auto-006 Round 2 Amendment 2](decisions/auto-006-phase-6-dispatch-shape.md#decision-round-2)).
**Inputs read.** All 10 specs (`architectures/v3/specs/{gf-s,gf-m,gf-c,bf-s,bf-m,bf-l,u-a,u-b,u-c,d7-u-1}.md`); all 55 ADR files at `docs/adr/0010-0064`; [Phase-4.2 overlap.md](primitives/overlap.md); [Phase-5-close handoff](SESSION-HANDOFF-2026-05-25-phase-5-close.md); [auto-006 brief](decisions/auto-006-phase-6-dispatch-shape.md); [AGENTS.md](../../AGENTS.md).

## Section 1: Verdict

**PASS WITH AMENDMENTS** — no structural-citation finding requires re-author of any spec; all framework-ADR + per-variant pairings are correctly co-located; the four-variant ADR set matches overlap.md verdicts; ADR 0049 anomaly is resolved by BF-M omission + BF-L pairing as authored. Two non-blocking findings (one paraphrase-drift on framework ADR 0036 framing in BF-L; one cosmetic note on D7-U-1 ADR-row ordering against the §0 rubric's pair-co-location best-practice) are folded into Recommendations below; neither blocks Phase 6 closure.

## Section 2: Findings per check

### A.1 Every cited ADR file exists

**PASS.** Every ADR ID referenced across §0 indexes and §7 references in all 10 specs resolves to an existing file at `docs/adr/00NN-*.md`. The full set of ADRs used: 0010-0036 (common-substrate + framework + discipline), 0037-0039 (GF-S orphans + per-variant), 0040-0041 (GF-M orphans), 0042-0044 (GF-C orphans), 0045-0046 (BF-M orphans), 0047-0049 (BF-L orphans + per-variant), 0050-0053 (U-A per-variants), 0054-0056 (U-B orphan + per-variants), 0057-0059 (U-C orphan + per-variants), 0060-0064 (D7-U-1 orphans + per-variants). No false reference.

### A.2 Framework + per-variant ADR pairing in §0

**PASS with one note.** Every spec claiming a framework ADR co-locates the per-variant pair with `Variant of` filled: GF-S 0028↔0039; BF-L 0028↔0049; U-A 0028↔0050 / 0029↔0051 / 0030↔0052 / 0036↔0053; U-B 0029↔0055 / 0030↔0056; U-C 0028↔0058 / 0029↔0059; D7-U-1 0029↔0062 / 0030↔0063 / 0036↔0064. GF-M, GF-C, BF-S, BF-M claim no framework ADR and explicitly annotate this in §0.

**Finding-1 (non-blocking):** BF-L §0 lists 0036 (P-30 framework) as `common-substrate` with no Variant-of entry. BF-L's annotation explains this as consumption-only ("0036 IS consumed without per-variant binding by P-13 maintenance-loop dispatch"). Overlap.md confirms P-30 has only 2 per-variants (U-A, D7-U-1); no BF-L per-variant exists. The pairing rule's intent is satisfied (BF-L does not claim a P-30 substrate primitive of its own). **Phase-6-followup glossary clarification recommended:** does consumption-only consumption fire the pairing obligation?

### A.3 mandate-fit YAML frontmatter schema

**PASS.** Every spec uses the canonical 5-key schema with all values ∈ {greenfield, brownfield, both, n/a, silent}. No `-fit` suffix variants. No off-schema tokens. Distribution: GF-S 5×greenfield; GF-M 4×greenfield+1×silent; GF-C 2×greenfield+3×silent; BF-S 4×brownfield+1×n/a; BF-M 3×brownfield+2×n/a; BF-L 4×brownfield+1×n/a; U-A 4×both+1×greenfield; U-B 4×both+1×greenfield; U-C 1×brownfield+1×greenfield+3×both; D7-U-1 5×both.

### A.4 §0-§7 header presence

**PASS.** Every spec has `## §0 ADR-citation index`, `## §1 Overview`, `## §2 Substrate composition`, `## §3 Methodology shape`, `## §4 Discipline binding`, `## §5 Mandate fit`, `## §6 Open carries`, `## §7 References`. No missing header in any spec.

### A.5 `n/a` cells accompanied by one-line rationale

**PASS.** All four `n/a` cells (BF-S mvp; BF-M initial-spec + mvp; BF-L mvp) carry inline rationale in §5 ("MVP/initial-spec presupposes greenfield... `n/a` not `silent` — explicit out-of-scope" with track-section back-references). No `n/a` cell lacks justification.

### B.1 Interpretation drift on shared framework ADRs

**PASS WITH ONE PARAPHRASE NOTE.**

- **0028 (P-19)**: GF-S, BF-L, U-A, U-C all characterise the engine identically (Drools/OPA Rego decision-tables + LLM-judge fallback via P-14 + OPA hard-floor post-check), verbatim from overlap.md. U-C's "dispatcher rather than classifier" framing applies to U-C's variant role, not the framework. Non-material.
- **0029 (P-28)** and **0030 (P-29)**: U-A/U-B/U-C/D7-U-1 cite identical construction recipes; differences confined to per-variant envelope-schema / policy-DSL layers per overlap.md verdicts. Consistent.
- **0036 (P-30) — Finding-2 (non-blocking):** U-A (ADR 0053) and D7-U-1 (ADR 0064) characterise 0036 as the Temporal signal+timer+query triad with namespace-separation discipline. BF-L characterises 0036 as "commodity dispatch surface" consumed by P-13. The characterisation elides the registrar's state-machine semantics but is internally consistent with BF-L's dispatch-only usage. Phase-6-followup glossary clarification recommended.

### B.2 2-candidate-fold ADR consistency

**PASS.** ADR 0033 (P-25 CaMeL) — BF-S+BF-M agree on `CaMeL.execute()` contract, NORMAL/STRICT per-work-unit-class config, production-scissors-default-off, CTR-E6 utility-tax. ADR 0034 (P-27 archaeological-brief) — BF-M (per-cycle brief at stage 2+7) vs BF-L (ingestion-time over regions) differ in deployment timing but agree on the tool-using LLM-judge synthesis loop. ADR 0035 (P-24 attribution) — BF-S owns S-4; BF-L composes as historical view of P-26; both agree on immutable signed log + three signer classes.

### B.3 Four-variant ADR sets match overlap.md verdicts

**PASS.** P-19 has 4 variants (0039 GF-S / 0049 BF-L / 0050 U-A / 0058 U-C); P-28 has 4 (0051 U-A / 0055 U-B / 0059 U-C / 0062 D7-U-1); P-29 has 3 (0052 U-A / 0056 U-B / 0063 D7-U-1); P-30 has 2 (0053 U-A / 0064 D7-U-1). Every variant ADR is claimed by the correct candidate spec; every overlap.md-named variant exists as an ADR file.

### B.4 ADR 0049 anomaly resolution

**PASS — resolution confirmed.** The Phase-5-close handoff's per-candidate ADR set table contains an authoring error: it lists "0049 P-19/BF-M variant" against BF-M and "0049 P-19/BF-L variant" against BF-L. The actual ADR file name is `0049-p-19-variant-bf-l-per-region.md` — BF-L's per-region variant only.

- **BF-M spec**: correctly OMITS 0028 (P-19 framework) and 0049 from §0. BF-M's §0 annotation explicitly states "BF-M does not name any of P-28, P-29, P-30, or P-19" and the [AGENTS-MD-a9fb7b42f8 framework-scope discipline](../../AGENTS.md#framework-adr-scope-boundary-discipline) does not bind. **Resolution: ✓ CORRECT.**
- **BF-L spec**: correctly PAIRS 0028 + 0049 in §0 with `Variant of` = 0028. The framework + per-variant pairing check annotation explicitly confirms the pairing. **Resolution: ✓ CORRECT.**

The handoff-prose error is a documentation defect in the Phase-5-close handoff itself; the specs ignored it and authored correctly. **No spec-authoring action required.** Recommendation: surface the handoff defect to a Phase-6-close handoff-erratum note (one-line correction in the next handoff).

### C Mandate-fit YAML / §5 prose consistency

**PASS.** All 50 YAML cells (10 specs × 5 work-unit-classes) match §5 prose. Specs that distinguish `silent` from `n/a` (GF-M refactor; GF-C 3× silent; U-A/U-B mvp where prose explicitly names "greenfield, not silent") carry the explicit distinction in §5 prose. No YAML cell contradicted by §5 prose; no §5 prose contradicts its YAML cell.

## Section 3: Cross-spec semantic-consistency findings

The only material flag is the **Finding-2 paraphrase note on ADR 0036**:

- **U-A §2** characterises 0036 as "the Temporal signal+timer+query triad + append-only event-log envelope shared with D7-U-1, with namespace-separation discipline (`state-machine-class` field)" — event-driven semantics.
- **D7-U-1 §2** characterises 0036 as "the shared Temporal substrate (signal+timer+query triad + append-only event-log + namespace separation)" — timer-driven semantics.
- **BF-L §0** characterises 0036 as "commodity dispatch surface" consumed by P-13 maintenance-loop.

The difference between U-A and D7-U-1 is canonical (overlap.md verdict: DISTINCT primitives despite shared substrate; one event-driven, one timer-driven). The BF-L characterisation is materially different — treating 0036 as commodity dispatch surface rather than registrar framework — but is **defensible** because BF-L's usage is dispatch-only (emit `maintenance-trigger` events), not registrar-state-machine instantiation. **The difference is not material to Phase 6 closure** because each spec's usage is internally consistent with the ADR's contract and no spec contradicts another spec's load-bearing claim on 0036. Phase-6-followup glossary clarification recommended.

All other shared framework ADR references (0028 / 0029 / 0030) are consistently characterised across claiming specs — the *engine* layer is verbatim from overlap.md across all spec citations, with variations confined to per-variant feature-source / envelope-schema / policy-DSL layers per overlap.md's explicit verdict.

## Section 4: ADR 0049 anomaly resolution

**CONFIRMED.** Per detailed check in §B.4 above:

- **BF-L spec correctly pairs 0028 + 0049** in its §0 ADR-citation index with `Variant of` = 0028. The framework + per-variant pairing check annotation in BF-L's §0 explicitly confirms the pairing.
- **BF-M spec correctly OMITS 0028 and 0049** from its §0 ADR-citation index. BF-M's §0 annotation explicitly states "BF-M does not name any of P-28, P-29, P-30, or P-19" and confirms no framework + per-variant pair appears.

The Phase-5-close handoff's per-candidate ADR table line for BF-M ("...0049 P-19/BF-M variant") is the documentation error; the actual ADR file is BF-L's per-region variant. Specs authored correctly despite the handoff defect.

**Recommendation:** add a one-line erratum note in the Phase-6-close handoff documenting the Phase-5-close handoff table defect (BF-M does not own ADR 0049; ADR 0049 is BF-L's per-region variant only).

## Section 5: Per-spec one-line summary

- **gf-s**: PASS | 0 blocking findings; mandate-fit YAML 5× greenfield consistent with §5 prose; P-19 framework correctly paired with 0039.
- **gf-m**: PASS | 0 blocking findings; no framework ADR claimed; mandate-fit YAML 4× greenfield + silent on refactor correctly distinguished from n/a.
- **gf-c**: PASS | 0 blocking findings; no framework ADR claimed; three orphan ADRs (0042/0043/0044) carry distinctive substance; 3× silent cells all have rationale.
- **bf-s**: PASS | 0 blocking findings; no framework ADR claimed; 2-candidate-fold ADRs (0033/0035) consistent with BF-M/BF-L respectively; mvp `n/a` has rationale.
- **bf-m**: PASS | 0 blocking findings; correctly OMITS 0028 + 0049 (per the ADR 0049 anomaly resolution); 2-candidate-fold ADRs (0033/0034) consistent.
- **bf-l**: PASS | 1 non-blocking paraphrase note (0036 as commodity dispatch surface vs U-A/D7-U-1 registrar framing) per Finding-1 + Finding-2 above; otherwise fully consistent.
- **u-a**: PASS | 0 blocking findings; four framework + per-variant pairs all correctly co-located (the most variant pairings of any v3 candidate); §0 ADR row count = 28.
- **u-b**: PASS | 0 blocking findings; two framework + per-variant pairs (0029↔0055, 0030↔0056) plus orphan 0054; honest X_UNM_B completeness gap declaration.
- **u-c**: PASS | 0 blocking findings; **exemplar spec** demonstrates correct framework + per-variant pairing pattern that 7-of-9 downstream specs inherit; structurally clean.
- **d7-u-1**: PASS | 0 blocking findings; heaviest spec (28 §0 rows); three framework + per-variant pairs all co-located; mandate-fit 5× both per spec's load-bearing unified-attempt claim.

## Section 6: Recommendations

**Verdict: PASS WITH AMENDMENTS — Phase 6 may close.** Phase-6 closure proceeds; the matrix-subagent output goes into the handoff.

### Non-blocking amendments — carry to Phase-6-followup

1. **Finding-1 (BF-L treatment of 0036 in §0):** glossary clarification — when does the framework + per-variant pair obligation fire? On any §0 citation, or only when the spec claims the framework primitive as its own substrate? Recommendation: AGENTS-MD-a9fb7b42f8 should be tightened to disambiguate consumption-only references from substrate-primitive claims. **Owner: lead agent at Phase-6-followup.**

2. **Finding-2 (paraphrase drift on 0036 between U-A / D7-U-1 / BF-L):** add a glossary item noting that BF-L's "commodity dispatch surface" framing of 0036 is *consumption-only* and does not contradict overlap.md's DISTINCT verdict between U-A's event-driven and D7-U-1's timer-driven registrar semantics. **Owner: lead agent at Phase-6-followup glossary task.**

3. **Phase-5-close handoff erratum (ADR 0049 anomaly):** the Phase-5-close handoff's per-candidate ADR table line for BF-M incorrectly attributes ADR 0049 to BF-M. Specs authored correctly. **Recommendation:** one-line erratum note in the Phase-6-close handoff. **Owner: lead agent at Phase-6-close handoff authoring.**

### Items for the lead agent to fold inline now

None — all findings are non-blocking; no spec re-author needed; PR-cap budget for re-dispatch (≤1 PR per [auto-006 R2 verifier triage](decisions/auto-006-phase-6-dispatch-shape.md#decision-round-2)) is unused.

### Phase-6-followup deferral

Per [AGENTS-MD-cb08b5a7f3](../../AGENTS.md#self-imposed-deferrals-re-validate-before-honoring) + [AGENTS-MD-2adf78e54a](../../AGENTS.md#deferred-work-binding-artifact-triple): the three amendments above are non-load-bearing glossary / erratum items that should be carried via the binding-artifact-triple mechanism (Phase-6-close session handoff section + morning-summary line + next-run dispatch prompt slot). No mid-session deferral fires; the items are routine follow-ups, not blocking gates.
