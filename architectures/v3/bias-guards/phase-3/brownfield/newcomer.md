---
guard: newcomer
target: draft-brownfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 naive newcomer critique — brownfield draft

## §1 Persona stance

I am reading this draft as a competent engineer who has never seen the v3 research corpus, never opened any of the bias-guard reports, and has only the brief's glossary as a reference. I am sympathetic to the project and want to understand it. My test: at every paragraph, can I picture what is being claimed concretely enough to disagree with it? When the answer is "no — I would have to first go read three other documents," that is jargon weight I'm logging. I am not attacking the underlying ideas; I am attacking the surface that a Phase-6 architecture spec reader will hit. The draft frequently loses me — not because the ideas are obscure, but because almost every load-bearing claim is *named* (CTR-G3, F44, splitter Cluster-11, Lumper Cluster-6) rather than *stated*. The result reads like meeting minutes whose participants share a private dictionary.

## §2 Top confusing or jargon-heavy passages

**(1) ROBUST-B1's opening clause.** *"CTR-G1 (corpus admits brownfield asymmetry but designs as if it doesn't) is honored, not retrofitted."* I had to stop. "CTR-G1" is not in the brief glossary. From context I infer it is a contradiction-register entry, but the draft never says so. **What would help.** Inline gloss on first use: "CTR-G1 — a registered corpus contradiction that says the literature acknowledges brownfield is different but still designs greenfield-only architectures." Same for *every* CTR-* token on its first appearance.

**(2) ROBUST-B2's punchline.** *"Greenfield's cold-start (brief §5) is methodology-creation from priors; brownfield's legacy-ingestion is methodology-application against an existing artifact."* This is the most important conceptual claim in the entire section and it is buried in a one-clause aside. **What would help.** Two sentences with a concrete contrast: "In greenfield day 0 the factory has no codebase, so it must *invent* the methodology that produces the first commit. In brownfield day 0 the factory has a codebase, so it must *apply* its methodology to read what exists. These are not mirror images: ingestion is a one-time-and-incremental setup operation; cold-start is a never-repeated bootstrap."

**(3) ROBUST-B3 / B4 — the codebase model itself.** The list of five sub-stores is *named well* (codebase index, dependency-and-impact graph, runtime/telemetry view, change-history/attribution view, invariant/debt view). But the framing leans on two undefined anchors at once:
   - *"incrementally maintained"* — never defined. Maintained how? Polled? Hooked? On every commit? The phrase is repeated in B13 and DPB-4 without ever being unpacked.
   - *"splitter Cluster-11"* — opaque without the bias-guard report.

**What would help.** Add a footnote on first use: "Splitter Cluster-11 = the bias-guard's pass that re-grouped the corpus's treatments of 'the codebase' into a single named substrate primitive." And define incremental maintenance with a one-liner.

**(4) ROBUST-B6 / ROBUST-B7 — the holdout claim.** *"Holdout is unseen subset, not out-of-tree subset"* is repeated as a slogan three times. I never *understand* it the first time. **What would help.** A worked example: "Traditional D-2 says: hold a directory `/scenarios/` outside the codebase that the builder agent cannot read. Brownfield inverts this: the *source* of scenarios is production traces and existing tests that *live inside the codebase tree*. The discipline is preserved by withholding *which subset* of those scenarios is the acceptance set, not by withholding their *location*."

**(5) ROBUST-B8 — judge sub-shapes.** *"The three judge sub-shapes (same-model-different-role / different-family-on-builder / different-family-on-spec) remain distinct per lumper Cluster-1; brownfield primarily uses sub-shape (b)."* The three sub-shapes are not defined. **What would help.** A three-row definition table on first use.

**(6) DPB-5 / DPB-6 — the D2 invocation.** The draft conflates "the 5-class taxonomy that appears in D2's worked example" with "D2 itself." A newcomer wondering "what is D2?" will go to decisions-captured.md and find a decision about *matrix shape*, not a list. **What would help.** Say "the D2-illustrative 5-class taxonomy" or just "the 5-class taxonomy from the brief §0."

**(7) ROBUST-B12, cycle steps.** The 8 steps are *mostly* comprehensible. But step 3 cites *"BF-M's § 1.1 stage-3 — a contraction of El Kaim's 9-field intent block fit to a per-PR change"* and step 4 cites *"Klaassen four-clause plan-prompt."* Both names are dropped without context. **What would help.** Either footnote-cite once or drop the proper noun and describe the artifact.

**(8) ROBUST-B9 / Patrol.** *"Lumper Cluster-9 split still applies: the F34 / F54 / F55 / F57 lump must be split per-F-mode with named detectors."* This sentence has four undefined F-codes and one undefined cluster reference, and the only verb is "applies." **What would help.** Translate the meta-instruction into prose: "Patrol must distinguish between four different failure modes it might detect — cross-layer drift (F34), goal subversion (F54), behavioral drift (F55), design-authority erosion (F57) — and run a named detector per mode rather than a single generic 'drift' check."

## §3 Hidden anchors and smuggled context

| Target claim | Hidden anchor | Recommended re-phrase |
|---|---|---|
| "CTR-G1 / CTR-G3 / CTR-G4 are honored" (B1, B2) | Reader must know the contradiction register | Inline one-sentence gloss on first occurrence |
| "Splitter Cluster-N unifies as X" (B3, B4, B6, B7, B8, B9, DPB-4, DPB-10) | Reader must know bias-guard output | Replace with the *substance* of the finding |
| "F44 brownfield-critical" (B5) and the 20+ F-code mentions in §1.6 | Reader must have failure-modes-v3.md open | Inline F-codes should each carry a 3-word gloss on first appearance |
| "Anthropic Auto-Review pattern (report 23 §3.5); Codex Auto-Review (report 18)" | Reader must have read both reports | One-sentence gloss |
| "kevin/carl" (B8 prose) | Reader must know CJ Hess / report 34 | Drop the names or define: "the kevin/carl pattern — pair the builder model with a reviewer model from a different family" |
| "Caremark prong-1" (B10, DPB-6) | Reader must know SEC/SOC governance vocabulary | Gloss: "the duty to maintain an information-and-reporting system the board can rely on" |
| "Brier pace-layer-1 / pace-layer-3" (DPB-1) | Reader must have read followup 12 | Gloss in one line or drop |
| "Ashby-aware deterministic perimeter check" | Reader must know Ashby's law | Gloss: "the deterministic checker must have at least as many degrees of distinction as the failure modes it claims to catch" |

## §4 What the draft does well

The macro-structure is excellent. ROBUST-vs-DECISIONS-PENDING is a strong frame: a newcomer can read §1 as "what the three tracks agree on" and §2 as "what the user has to decide," and that scaffolding survives the jargon. The 8-step cycle in B12, taken on its own *names*, is comprehensible. The failure-mode table in §1.6 is the most accessible part of the draft — each row is short, the mitigation locus is concrete, and the F-codes are at least anchored to one-line descriptions. The decision-pending blocks (DPB-1 through DPB-10) consistently end with a "User question" and "Concrete next action" — that pattern is doing real work and should propagate to the rest of the document.

## §5 Concrete recommendations for Phase-3.4

1. **Add a §0 glossary local to the draft.** ~20 lines defining: CTR-* code → contradiction register; splitter Cluster-N / lumper Cluster-N → bias-guard outputs; CodebaseModel, PerimeterClosure, TypedJudgeCall, AttributedEventLog; incremental maintenance; role-partitioned reads; legacy-ingestion vs. cold-start; the three judge sub-shapes.
2. **Worked example for ROBUST-B7.** A paragraph showing a concrete scenario flowing from a production trace, into the codebase model's runtime view, through role-partitioned access by the V&V agent, and finally being declared "unseen" by virtue of being held back from the builder context.
3. **Unpack "incremental maintenance" once, in B3.** One sentence describing the maintenance contract (bulk on day 0; per-commit thereafter; refresh cadence per view). Then DPB-4's three options become legible.
4. **Translate meta-instructions to prose.** Any sentence of the form "Lumper Cluster-N split applies" should be rewritten as direct guidance: "Phase-4 must split X into A and B because…".
5. **Drop or gloss proper nouns on first use** (El Kaim, Klaassen, Brier, Husain/Shankar, kevin/carl, Cherny, Kahana, Ashby, Caremark).
6. **Distinguish "D2 the decision" from "the 5-class taxonomy in D2's example."**
7. **Make the §1.6 table the model for §1.1-§1.5.** That table works because each row pairs a named hazard with a concrete locus. The narrative sections could borrow the same shape.

The draft contains a coherent and defensible architecture. The newcomer barrier is overwhelmingly *terminological*, not *conceptual* — which means Phase-3.4 can fix most of it with a glossary, a few worked examples, and a search-and-replace pass on the bias-guard meta-vocabulary.
