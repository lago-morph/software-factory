---
guard: newcomer
target: draft-unified-synthesis
phase: 3.2
based-on-commit: 200ad3e
based-on-date: 2026-05-25
---

# Phase-3.2 naive newcomer critique — unified draft

## §1 Persona stance

I am a naive newcomer dropped into this draft with no prior context beyond the brief's §0 glossary. After one cold read: this is the document where the methodology is most ambitious — it claims one architecture covers both greenfield and brownfield — and yet is the hardest to read independently. Almost every load-bearing claim is expressed as an alphanumeric ID (ROBUST-U1, DPU-8, F-ANCHOR-3, CTR-C10, D7-U-1, X_UNM_G) without being restated in plain prose. I can follow the surface argument — "the mandate is a parameter on a typed object, not a top-level branch" — but I cannot evaluate it, because the three competing typed-object framings are introduced as fait accompli with no worked example.

## §2 Top 5-8 confusing passages

1. **The 95% / 55% convergence claim.** *"Effective overlap on substrate primitive content: ~55%. Effective overlap on the unified claim ('mandate is a parameter'): ~95%."* I cannot compute these numbers, do not know what "effective overlap" means (Jaccard? token overlap? rubric-scored?), and cannot tell whether "95% on a claim" means "all three tracks made it" (then why not say "3 of 3"?) or something subtler.

2. **The convergence-vs-anchor paradox at the top.** One sentence calls the convergence *"the most significant convergence in Phase-2 outputs"*; the very next paragraph says it *"is either strong corpus signal … or brief-derived"*. So is this the headline finding or a contamination warning? The draft never tells me which to believe.

3. **ROBUST-U1 itself.** *"Mandate is a parameter, not a top-level architecture distinction."* Intuitive only if I already know (a) UC4 (the user's stated hypothesis), (b) the brief's §3 framing, and (c) what "parameter" means in this context.

4. **DPU-1's three typed-object framings.** Three candidates — `EscrowInterval` (process-state node, many per cycle), `layer` (artifact-stack position, 5 per cycle), `Anchor` ("one or a few per architecture"). These differ in *granularity by ~3 orders of magnitude*. I have no way to judge "which is right" because the draft never shows what an actual cycle *looks like* under each framing. The "user question" is asked of someone given no observational basis for choosing.

5. **DPU-8 as a "pre-decision question."** I read the heading "DECISIONS-PENDING (tracks diverge; user input required)" then arrive at DPU-8 which says *"No user input required at Phase-3.4 for this"*. So is it a decision or not? It belongs in §4 (dispatch notes), not §2 (decisions pending).

6. **The cross-mandate dispatch in §4.** The four-subagent attack-and-defend grid (`X_UNM_G`, `X_UNM_B`, `X_GFB_A`, `X_GFB_X`) is dense with references to drafts I have not read.

7. **The defaults table.** D-1 through D-7 are not restated. The table assumes I remember the seven defaults verbatim.

8. **F-ANCHOR-2 / F-ANCHOR-3 / F-ANCHOR-4 sprinkled inline.** Each appears with a severity tag (HIGH / MEDIUM / MEDIUM-HIGH) and a parenthetical justification, but with no definition.

## §3 Hidden anchors and smuggled context

- **UC4 / UC1** appear several times without restatement. UC4 is the *foundation* of why this draft exists.
- **Brief §3** is the hidden frame for ROBUST-U1.
- **Splitter Cluster-N / Lumper Cluster-N references** referenced as if I have the bias-guard outputs in front of me.
- **CTR-B5 / CTR-C2 / CTR-C4 / CTR-C10 / CTR-G3** — contradictions referenced by ID with no inline gloss.
- **F-mode references** — twelve F-modes name-dropped without inline definition.
- **D-N references** not restated.
- **D7 / D6 / D4** as bias-guard test names (different from D-N as defaults) overload the "D" namespace.
- **AILCCP**, **STIR cascade**, **Kahana three-part test**, **El Kaim 9-field intent block**, **Jaymin thresholds**, **Brier layers**, **Caremark prong-1**, **SB 53 / SEC IAC** — author / framework names cited without restatement.

## §4 What the draft does well

The structural skeleton is admirable. The §1 ROBUST / §2 DECISIONS-PENDING / §3 per-track open questions / §4 adversarial dispatch four-part scaffold is exactly the right shape. The decision to flag F-ANCHOR-2 / F-ANCHOR-3 *inline* with the claims they touch is honest. The mandatory D7-U-1 blind-axis test is a strong intellectual move — the draft is willing to schedule its own falsification. And the DPU-1 framing ("three candidate instantiations of one family") is genuinely a useful synthesis stance.

## §5 Concrete recommendations for Phase-3.4

1. **Add a §0 reader's preamble** (≤500 words) restating UC4 verbatim, restating brief §3, defining "mandate is a parameter" in plain prose with one worked example.

2. **Replace the "95% / 55%" numbers with discrete claims**: "3 of 3 tracks make the mandate-as-parameter claim; 3 of 3 use a typed-object substrate; the typed-object content varies."

3. **Reconcile the convergence headline and the F-ANCHOR-3 caveat** into one paragraph with an explicit reader instruction: "Treat the unification claim as *provisional pending D7-U-1*. The rest of this draft is written under the *assumption* that the convergence is genuine; if D7-U-1 falsifies it, §1 ROBUST claims downgrade to ROBUST-IF-CONFIRMED."

4. **Work one cycle three ways**: pick a single representative work unit and walk through it under U-A (EscrowInterval graph), U-B (layer traversal), U-C (anchor-distance). One page, three columns. This is the *only* way DPU-1 becomes evaluable.

5. **Move DPU-8 out of the DECISIONS-PENDING section** — it is a meta-question about the document's fate, not a user decision.

6. **Inline-gloss the IDs the first time each is mentioned**: F-mode IDs, CTR IDs, Splitter/Lumper Cluster IDs, F-ANCHOR IDs. Or add a §0.5 reference card.

7. **Disambiguate the "D" namespace**: D-1..D-7 (brief defaults) versus D1..D7 (decisions-captured) versus D7-U-1 (blind-axis test) versus DPU-1..DPU-8 (decisions-pending-unified).

8. **Make the cross-mandate dispatch section self-contained or remove it**.

9. **Add a one-sentence verdict per ROBUST claim**: not just "all three tracks agree," but "all three tracks agree *because* …" — corpus citation, not just track concurrence.
