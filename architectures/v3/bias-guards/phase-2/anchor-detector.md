---
based-on-commit: 5c4deeb
based-on-date: 2026-05-24
---

# Phase-2 anchor-detector audit

**Method.** Cross-track diff across the 9 Phase-2 outputs, classifying each
convergence as `honest corpus signal` (multiple tracks cite the same corpus
material with independent reasoning chains; verdict survives variation in
framing) vs `bias-guard contamination` (tracks lean on the bias-guard finding
language rather than independent corpus reading; verdict would not survive
removing the bias-guard finding from the input set) vs `brief-implicit
anchoring` (the brief's framing makes the convergence near-inevitable; not
contamination but reduces the value of the convergence as evidence). Auditor
read all nine tracks plus the brief, decisions-captured, and the three Phase-1
bias-guard reports; classifications below cite verbatim phrasing where
relevant.

---

## Section 1 — Major convergence findings

### CONVERGENCE-1: Invariant/body split for MISSED-3 reconciliation

- **Tracks:** 1 (greenfield-substrate §2.2 + §1.1 S3), 2 (greenfield-methodology
  §0.3 critique C + §1.4 primitive 1), 3 (greenfield-cold-start §5.5 — labelled
  "two-velocity model"), 7 (unified-A §2 — labelled "tier-graded invariant
  ratchet"), 8 (unified-B §3.3 — done via pace-layer placement), 9 (unified-C
  §3.1 + §7.2). Lead-agent count of 6 verified. **Track 5
  (brownfield-methodology)** uses the El Kaim intent block at Stage 1 but does
  *not* explicitly split body-vs-invariants — it just adopts the whole block as
  upstream prerequisite. **Tracks 4 and 6 (brownfield substrate / ingestion)**
  do not engage MISSED-3 at this level; they elide it (T4) or sidestep with
  EAI-store-as-replacement (T4 §4 D-1 challenge).
- **Convergent claim:** the El Kaim non-negotiable `invariants` field is
  substrate-stable and authoritative; the rest of the spec body is malleable
  and methodology-layer. UC4 is preserved *below* the invariants; El Kaim is
  preserved *at* the invariants.
- **Independent reasoning chains?** Partially. Track 8 derives the split from
  Brier pace-layers (invariants at Standards, malleability at Specs);
  track 7 derives it from risk-tier (invariants ratchet with tier); track 3
  derives it from cold-start spec velocity (slow-velocity vs fast-velocity
  fields, *naming which El Kaim fields fall in which set*); track 1 derives
  it from substrate-stability arguments; track 2 derives it from "RE/SE
  discipline applies to the intent layer." Track 9 derives it from the
  Discovery overlay's per-tier shape. The reasoning paths are genuinely
  different and three of them (3, 7, 8) attach the split to a *different*
  structural feature (cold-start velocity / tier / pace-layer), not just to
  "MISSED-3 says do it."
- **Corpus citation diversity?** All six cite El Kaim Ch 3 §4.1 verbatim
  (`"non-negotiable conditions that any valid realization of the intent must
  preserve"`). Track 3 alone enumerates *which* El Kaim fields fall on which
  side (slow: identity/invariants/non-goals/policy/guardrails; fast:
  statement/business-outcomes/capability-scope/decision-seeds/feedback) —
  that's independent corpus engagement, not bias-guard repetition.
- **Verdict:** **mixed (largely corpus-signal, but with bias-guard amplifier).**
  The bias-guard MISSED-3 finding plainly accelerated convergence — every
  track that engages this names MISSED-3 by ID, often verbatim ("the
  contradiction is real and load-bearing"). However, the *resolution shape*
  (invariant/body split) is genuinely the corpus-obvious resolution that
  multiple independent reasoning chains land on. Without the MISSED-3
  finding, fewer tracks would have engaged the contradiction *at all*; but
  those that did would likely have reached the same resolution because
  El Kaim's `invariants` field literally names the split.
- **Recommendation for Phase 3:** Treat the invariant/body split as ROBUST
  for greenfield (tracks 1, 2, 3 converge with diverse mechanisms) but
  flag the bias-guard amplification when surfacing the convergence to the
  user. The shape is corpus-real; the speed of convergence is bias-guard-
  driven. Tracks 4, 5, 6 (brownfield) did not converge — their absence is
  itself informative (see Section 3).

### CONVERGENCE-2: D-2 challenged (scenarios outside the codebase)

- **Tracks challenging:** 3 (with "bootstrap-borrowed-priors" replacement),
  4 (with CDS — codebase-derived scenarios), 5, 6 (most aggressive — D-2
  oversimplifies its own primary source per WEAK-3), 7 (tier-indexed
  location), 8, 9 (overlay-dependent). **Tracks accepting:** 1 and 2 (both
  greenfield, where D-2 is uncontroversial because there is no codebase to
  inherit from). That's 7 of 9; matches the lead-agent count.
- **Convergent claim:** holdout *discipline* (D-4) is the load-bearing
  primitive; holdout *location* is mandate- or tier-conditional. Most
  tracks specifically reformulate as "scenarios live where they can be
  held out from the builder."
- **Independent reasoning chains?** Strong. Track 6 reasons from
  ingestion-as-substrate ("existing tests are scenarios"); track 4 from
  five-item brownfield-load-bearing list (ESS B-3); track 7 from risk-tier
  ("T0 inline, T1 in-codebase, T2+ out-of-tree"); track 9 from
  overlay-selection; track 8 from artifact-pace-layer placement. The
  reasoning chains diverge.
- **Corpus citation diversity?** Three tracks (4, 5, 6) cite WEAK-3's
  sharpening of StrongDM's own pages verbatim (`"incident replays,
  agentic simulation"`). Tracks 7, 8, 9 cite CTR-B5 directly.
  Tracks 4 and 6 independently rediscover the StrongDM-internal evidence
  rather than just leaning on WEAK-3.
- **Verdict:** **honest corpus-signal.** The brief itself flags D-2 as
  fragile for brownfield in §4.1 (`"flagged fragile for brownfield"`), so
  challenge by brownfield tracks is brief-anchored, not contamination.
  Greenfield tracks 1 and 2 accept D-2 with justification — exactly what
  honest reasoning predicts. The convergence is the brief operating as
  designed.
- **Recommendation for Phase 3:** ROBUST. D-2 should be reformulated
  per Track 6's framing (`"holdout discipline enforced at substrate's
  scenario-selection layer, not at scenario-storage location"`) and
  promoted out of DECISIONS-PENDING. The challenge is corpus-anchored,
  multi-track, with independent reasoning chains.

### CONVERGENCE-3: Tier-based unified axis (2 of 3 unified tracks)

- **Tracks:** 7 (unified-A: risk-tier T0–T4) and 9 (unified-C: stakes-tier
  T0–T3). Track 8 (unified-B) picks Brier pace-layers instead.
- **Convergent claim:** the right organizing axis for a unified architecture
  is the per-work-unit blast-radius/reversibility/regulatory tier; mandate
  is a *derived statistical distribution* over tiers, not a peer axis.
- **Convergent specifics that are suspiciously identical:**
  - Both define tier by **same three orthogonal properties** —
    reversibility × scope/blast-radius × regulatory/RSI-exposure. T7 uses
    "blast radius × reversibility × Kahana-RSI exposure"; T9 uses
    "reversibility × scope of impact × regulatory exposure."
  - Both make the **classifier deterministic, not LLM-judged**, with
    identical F51-Ashby reasoning. T7 §3-2: classifier sample-audited;
    T9 §0.3 point 4: `"the router itself must not be a probabilistic
    guard."`
  - Both have **tier-indexed cost ceilings, judge-counts, watchdog
    cadence, escrow shape**.
  - Both make **mandate the input adapter** (T7 "mandate-feed adapters";
    T9 "discovery overlay vs excavation overlay") and **tier the
    selector**.
  - Both **pin cold-start to T2** (T7 §5.1 explicitly; T9 §5.4
    "Augmentation-mode by substrate default; T0-only work").
  - Both **dissolve CTR-A4 via per-tier regime declaration** with nearly
    identical mappings (T7 §1.3: T0–T2 = lights-out, T3 = L4, T4 =
    forbidden L5; T9 §7.1: T0–T1 = L5-equivalent post-bar, T2 = L4,
    T3 = AILCCP gate).
  - Both **resolve MISSED-3 by tier-graded invariant** ratchet (T7 §2;
    T9 §3.1).
- **Independent reasoning chains?** Weaker than they should be. The
  identical 3-property tier definition with identical F51-derived
  determinism argument is striking. Both tracks independently invoke
  the same five-named corpus anchors (Kahana RSI, Shapiro R3, Replit
  DB wipe, CodeRabbit/Veracode/METR, F44) in support — that *is* the
  corpus shape, so this part is not anchoring.
- **Corpus citation diversity?** Both cite essentially the same set:
  report 31 (Kahana), report 32 §8.2 (Shapiro R3), followup 10 (Replit
  G14), F44/F56/F43, report 09 §7 Jaymin. No track-unique citations
  on the tier-axis side.
- **Verdict:** **mixed — corpus-signal with brief-implicit anchoring.**
  The brief's D2 decision (mandate-fit is per-(architecture ×
  work-unit-class), per Skeptic #7) and OQ-B7 (`"organizing axes beyond
  mandate"`) explicitly seed regime / stakes / synchronicity as
  candidate axes. Both unified-A and unified-C are operating in
  brief-blessed territory. The convergence on *risk-tier specifically*
  (rather than e.g. regime, synchronicity, work-unit-class) is the
  corpus' empirical anchors aligning — F12/F30/F33/F44/F56 all
  escalate at the production boundary, and the corpus has no
  equivalent volume of evidence for synchronicity or audience-tier.
  However, the *specific 3-property classifier shape* (reversibility ×
  scope × regulatory) is too identical to be independent — likely
  cross-pollination via the corpus' shared F-mode severity-driver
  language.
- **Recommendation for Phase 3:** Treat the tier axis as a **strong
  candidate**, not as ROBUST. The fact that two of three unified
  tracks land here while the third (Brier pace-layers) does not is
  load-bearing evidence the axis is *one of two* defensible unified
  framings — not the only one. The Phase-3 unified synthesis should
  produce a tier-shaped draft AND a pace-layer-shaped draft, and
  treat the cut between them as a user-decision, not a merge.

---

## Section 2 — Other suspicious agreements

### CONVERGENCE-4: "lights-out = L4-with-re-entry, NOT L5"

- **Tracks:** All 9. T1 §1.3, T2 §1.5, T3 §2, T4 §6, T5 §4.4, T6 §6.1,
  T7 §1.3, T8 §3.2, T9 §7.1.
- **Convergent claim:** UC1 "lights-out" maps to L4 (Shapiro "I'm here")
  with substrate-triggered re-entry, not to L5 (Jaymin's dark factory).
- **Verdict:** **brief-implicit anchoring.** Brief §2.1 explicitly lists
  option (c) "regime classification scheme" as the lead-agent working
  stance (`"the lead agent's working stance: option (c) plus (b) is the
  most likely shape"`). All nine tracks land on (c)+(b); they were told
  this was the working stance. This is not convergence as evidence; it
  is compliance with the brief's stated direction. Treat as
  brief-given, not as corpus-confirmed.
- **Recommendation:** Do NOT surface as a robust independent finding;
  treat as a brief constraint that all tracks honored.

### CONVERGENCE-5: Cognitive escrow as substrate primitive (F42/F53 fix)

- **Tracks:** T1 (S8), T2 (primitive throughout §1.4), T3 (P5), T5
  (Stage-2 escrow harness §5.3), T7 (primitive 10), T8 (per-layer
  re-entry trigger sets), T9 (S3). Seven of nine.
- **Convergent claim:** the prompt→response interval (report 30) is a
  substrate-designed surface, and substrate-triggered (not
  operator-voluntary) re-engagement prompts are the structural fix for
  F53 voluntary-discipline-fragility.
- **Verdict:** **bias-guard contamination — moderate.** F53 was
  promoted from `missing-failure-modes-audit.md` CANDIDATE-2 (Kahana
  fragile-dependency class). The bias-guard's framing — that *every*
  voluntary-discipline pattern in the corpus is structurally fragile,
  and the *meta-failure* is the assumption that operator-voluntary
  discipline is reliable — is recited by tracks 1, 2, 3, 7, 9
  near-verbatim. Cognitive-escrow-as-substrate-primitive is the
  bias-guard's stated fix.
- **Test of contamination:** would tracks have proposed substrate-
  triggered escrow without the F53 finding? Probably some would (the
  report 30 / Kahana material is in the cold-start required-reading
  set), but not seven of nine.
- **Recommendation:** Treat as DECISIONS-PENDING, not ROBUST. The
  primitive is well-grounded but its prominence across tracks is
  bias-guard-amplified. Phase 3 should specifically ask: does the
  evidence in report 30 + Kahana alone justify substrate-primitive
  status, independent of the bias-guard's editorial framing?

### CONVERGENCE-6: WEAK-5's "third F1-mitigation position" (Anthropic same-model-different-role)

- **Tracks:** T1 (S5 — explicitly cites WEAK-5), T2 (primitive 10 —
  "uses both"), T5 (Stage 6 — Anthropic Auto-Review explicit),
  T7 (primitive 8 — tier-conditional), T9 (S7 + §3.3 — tier-conditional).
- **Convergent claim:** F1 mitigation is *three* positions, not two;
  the third is Anthropic's same-model-different-role specialist
  critics (CTR-D7 + report 23 §3.5 Auto-Review).
- **Verdict:** **bias-guard contamination — high.** WEAK-5 was the
  Phase-1 bias-guard finding that explicitly named the three-position
  split. Three tracks (T1, T2, T9) cite WEAK-5 by name. The corpus
  evidence (Anthropic's five specialist critics; OpenAI's Auto-Review
  subagent) was in the corpus pre-WEAK-5, but the *framing as a third
  position* is bias-guard-originated. Without WEAK-5, tracks would
  likely have framed this as one of two positions plus an Anthropic
  outlier.
- **Recommendation:** Surface in Phase 3 with the explicit caveat that
  the third-position framing originated in the bias-guard, not in the
  corpus directly. The substantive claim (Anthropic ships same-model
  specialist critics as substrate) is corpus-true; the framing as a
  peer to RouterLLM and `kevin/carl` is editorial.

### CONVERGENCE-7: "Agent = Model + Harness + Natural-Language-Register" (CTR-C10 / MISSED-8)

- **Tracks:** T1 §4 D-3 caveat, T2 §4 D-3 caveat, T4 §4 D-3 caveat,
  T5 §4 D-3 challenged, T6 §4 D-3 caveat, T8 §4 D-3 challenged
  (vocabulary update), T9 §4 D-3 extension. Seven of nine.
- **Convergent claim:** D-3 (Agent = Model + Harness) is incomplete;
  report 37's Portuguese-vs-English finding shows natural-language
  register as a behavior-shifting harness parameter the formula does
  not model.
- **Verdict:** **bias-guard contamination — moderate-to-high.** MISSED-8
  is the Phase-1 finding that elevated report 37 (cited once in the
  corpus, for CTR-D5) to the D-3-fragility-extension argument. The
  empirical finding is real, but the framing as a D-3 vocabulary
  incompleteness is exactly the bias-guard's framing, reproduced
  near-verbatim across seven tracks. Most tracks flag it but do not
  redesign around it — which is itself diagnostic of bias-guard
  compliance rather than load-bearing engagement.
- **Recommendation:** Note in Phase 3 but do NOT treat as a robust
  convergence requiring action. Surface as an OQ that emerged in
  Phase 1, was acknowledged in Phase 2, and awaits substantive
  treatment.

### CONVERGENCE-8: F52 (Tempting-Wrong-Hybrid) as self-applied warning

- **Tracks:** T1 §7 OQ-T6, T2 §0.3 critique A, T3 §3.1 + §3.3, T5
  §2.6, T9 §7.7. Five of nine.
- **Convergent claim:** the track's own substrate-layer-accretion
  invites Schillace's F52 critique; defense is "we wrap typed
  artifacts, not the model itself."
- **Verdict:** **bias-guard contamination — moderate.** F52 is
  CANDIDATE-1 from `missing-failure-modes-audit.md`. The framing
  "wrap typed outputs, not the model" appears in multiple tracks
  with similar phrasing. The corpus material (Schillace Letter 11)
  is genuine, but the "self-applied warning" reflex is bias-guard-
  triggered. Track 5's §2.6 treatment is genuinely the most
  rigorous; others recite.
- **Recommendation:** Robust in T5's articulation; treat others as
  derivative. Phase 3 should adopt T5's framing as the canonical
  F52-defense formulation.

### CONVERGENCE-9: Brier pace-layers as universal background reference

- **Tracks:** All 9 reference Brier; T8 makes it primary; T5 §1.1
  drift detector; T6 §2.2 property 7; T1 §1.1 (S3 invariants); T7
  §0.2 (rejected as primary axis with reason); T9 §0.2 (rejected
  as primary axis); T2 §1.4 primitive 12.
- **Convergent claim:** Brier's pace-layer stack
  (Code/Plans/Specs/Architecture/Standards) is at minimum a
  reference framework and at most an organizing principle.
- **Verdict:** **brief-implicit anchoring + miscategorization-audit
  amplification.** Miscategorization-audit CHALLENGE-14 explicitly
  tagged Brier as `counter-metaphor` "every track must engage." All
  tracks engaged. This is compliance with bias-guard direction, not
  convergence. The engagements vary substantially in depth (T8
  builds on it; T7/T9 reject it as primary axis with reason; others
  cite once).
- **Recommendation:** Do NOT treat as convergence. The bias-guard's
  mandate was followed; that's the finding. Phase 3 should observe
  that pace-layers became a *coordinate system* across tracks even
  where rejected as the axis — that's the durable signal.

### CONVERGENCE-10: Beads `discovered-from` edge (report 38) for knowledge graph

- **Tracks:** T4 §2.6 (PR-archaeology cache), T5 §3 (Compound
  Knowledge typing), T6 §3.4 (sharpens F35), T7 §3 primitive 11,
  T9 S6. Five of nine.
- **Convergent claim:** typed knowledge accumulation requires a
  `discovered-from` edge primitive; Beads (report 38) is the
  corpus' strongest engine candidate.
- **Verdict:** **honest corpus-signal.** Report 38's Beads is
  named in the corpus inventory as the unified-track must-read
  list (item 3 in miscategorization-audit §3). Multiple tracks
  independently identify it as the typed-edge primitive without
  bias-guard prompting on this specific point. The corpus
  genuinely has one strong candidate for this primitive role.
- **Recommendation:** ROBUST. Surface in Phase 4 substrate
  extraction.

### CONVERGENCE-11: Cold-start protection via three layered defenses

- **Tracks:** T1 §5.4 (three substrate-side answers), T3 §5.3
  (three layered defenses), T9 §5.3 (four mitigations).
- **Convergent claim:** day-0 silent failure protection requires
  layered defenses — deterministic substrate + cross-model judging
  + escrow-triggered re-engagement.
- **Verdict:** **brief-implicit anchoring.** Brief §5.2 lists
  exactly four questions cold-start must answer, one of which is
  silent-failure protection. Three greenfield tracks answer it
  similarly because the corpus material (report 26 Larbi/Yang,
  report 30 Kahana, F1/F27 cross-model lit) is the same and the
  brief's question is direct. No contamination; no robust
  inter-track signal beyond "the brief asked a question, three
  tracks gave overlapping answers."
- **Recommendation:** Note but do not over-weight.

---

## Section 3 — Tracks that did NOT converge where expected

The non-convergences carry signal too. Five worth flagging:

1. **Track 6 (brownfield-legacy-ingestion) does NOT do the invariant/body
   split.** Instead it treats the spec as separate from the ingestion
   artifact (§2.3 — `"not a spec"`). T6 is the only brownfield track that
   makes the codebase-derived ingestion artifact the substrate-durable
   peer of the spec — a *different* MISSED-3 resolution: spec stays
   malleable, but it sits *next to* (not above) a code-derived artifact
   that carries de facto invariants. Lead agent should treat T6's
   alternative reading as a *substantive* dissent from CONVERGENCE-1,
   not as a track that simply didn't engage MISSED-3.

2. **Track 4 (brownfield-substrate-first) challenges D-1 outright** — the
   only track that says specs are NOT the most durable artifact (the
   EAI store and archaeology cache are). Surfaces as DECISIONS-PENDING
   in T4 §4. This is a load-bearing dissent from D-1, the most-accepted
   default across other tracks.

3. **Track 8 (unified-B) rejects tier-as-primary** with reasoned argument
   that pace-layers is shape-giving while tier is just per-cycle gates.
   This is the strongest available counter to CONVERGENCE-3 and should
   weight against treating tier-axis as the consensus unified shape.

4. **Tracks 4 and 6 do not engage MISSED-3 directly.** Both brownfield
   substrate-leaning tracks elide the El Kaim vs UC4 tension. This
   asymmetry (greenfield + unified tracks engage; pure brownfield
   substrate/ingestion does not) is informative: MISSED-3 may be a
   greenfield-and-unified concern, not a brownfield-load-bearing one.

5. **No track adopts Tournament-style population architecture.** D-3's
   fragility flag for population architectures led every track to
   disclaim it. The bias-guard MISSED-8 didn't help here, but the
   absence is consistent across nine tracks — Tournament is effectively
   dead in v3 Phase 2, despite being one of four v2 architectures.
   This should be a Phase-7 back-fill audit item.

6. **No track engages MISSED-9 (CaMeL utility tax) as load-bearing
   against the substrate-is-cheap thesis.** Tracks 2, 4, 5, 7 mention
   it; only T4 §2.9 and T5 primitive 11 explicitly accept the cost.
   The unified tracks (T7, T9) acknowledge it in cost-ceiling
   discussion but do not let it constrain substrate choices. This is
   a silent skip relative to what the bias-guard surfaced as a
   load-bearing tension.

---

## Section 4 — Vocabulary contamination

Identical/near-identical phrasings appearing across tracks that did not
appear in the brief or inputs.

### VOCAB-1: "ESS wedge" / "ESS primitive"

- T4 invents "Existing-System Substrate (ESS) wedge" as track-local
  vocabulary. No other track uses it. **No contamination.**

### VOCAB-2: "Sentinel" (cross-layer drift judge)

- T8 only. **No contamination.**

### VOCAB-3: "Tier-classifier" / "tier-overlay matrix" / "stakes router"

- T7 uses "Tier-classifier" + "tier-overlay matrix" + "mandate-feed
  adapter." T9 uses "Stakes Router" + "overlays" + "tier-lock."
  The vocabulary differs but the *structural taxonomy* is identical
  (deterministic classifier emits tier → matrix/overlay selects
  configuration → mandate-specific feed adapters at input). Two
  tracks reached structurally-identical proposals with different
  names. **Concept convergence, not vocabulary contamination —
  diagnostic of corpus shape, not copying.**

### VOCAB-4: "Cognitive-escrow surface" / "escrow-interval harness"

- T1 calls it "cognitive-escrow primitive (S8)." T3 calls it
  "escrow-interval harness (P5)." T9 calls it "Cognitive Escrow
  (S3)." T7 calls it "cognitive-escrow primitive." Phrasing varies;
  concept is identical and traceable to report 30 directly. **No
  contamination.**

### VOCAB-5: "Bootstrap-borrowed prior" + "sunset edge"

- T3 invents both as track-local. No other track uses them. **No
  contamination.**

### VOCAB-6: "Two-velocity model" / "tier-graded invariant ratchet" /
"slow-velocity vs fast-velocity fields"

- T3 §5.5 uses "two-velocity model" and enumerates slow-velocity
  vs fast-velocity El Kaim fields by name. T7 §2 uses "tier-graded
  invariant ratchet." T8 §3.3 uses Brier pace-layer placement
  instead. T9 §3.1 uses "non-negotiable below invariant line." The
  underlying concept (invariant/body split) is shared but each
  track's vocabulary is its own. **Concept convergence with
  vocabulary divergence — this is the *healthy* shape of honest
  convergence.**

### VOCAB-7: "F-mode self-applied warning" patterning around F52

- T1, T3, T5, T9 all invoke F52 (Tempting-Wrong-Hybrid) as a
  self-critique with similar structure. T5 §2.6 phrasing is the
  most specific (`"gates wrap the model's typed outputs, not the
  model"`). Other tracks have similar but not identical phrasings.
  Mild contamination — the *practice* of self-applied F52
  warning is bias-guard-prompted; the *specific phrasings* vary
  enough to indicate independent attempts.

### VOCAB-8: Numbered primitive naming (S1–S8 in T1; P1–P7 in T3; S1–S7 in T9)

- Multiple tracks number their substrate primitives identically
  (S1, S2, ...). This is a generic-engineering tic, not
  vocabulary contamination. **No finding.**

### Summary of vocabulary check

**No strong vocabulary-copying contamination detected.** Identical
phrasings exist only for:
- Quoting El Kaim's `invariants` definition verbatim (corpus-required).
- Quoting brief §0 definitions of lights-out / L4 / L5
  (brief-required).
- Bias-guard finding IDs (MISSED-3, WEAK-5, F52, F53, F57) cited
  by ID across tracks — this is correct engagement discipline, not
  vocabulary copying.

The strongest contamination signal in vocabulary is the *practice*
of citing bias-guard finding IDs in track text (e.g., `"per WEAK-5"`,
`"per MISSED-3"`). This is good discipline — but it also means
tracks are visibly steering toward bias-guard-flagged territory
rather than independently rediscovering the same tensions. Tracks
that engage MISSED-3 without naming it (T8 does this best — frames
the resolution in Brier's terms) are giving stronger evidence of
honest convergence than tracks that engage MISSED-3 by citing the
bias-guard explicitly.

---

## Section 5 — Recommendations for Phase 3 merge

### Convergences to treat as ROBUST (enter Phase-3 synthesis without DECISIONS-PENDING)

1. **D-2 reformulation:** holdout *discipline* is substrate-enforced;
   holdout *location* is mandate/tier-conditional. Seven tracks; three
   independent reasoning chains; brief-flagged-fragile in advance.
   (CONVERGENCE-2)

2. **Beads `discovered-from` edge as typed-knowledge primitive.** Five
   tracks; corpus genuinely has one strong candidate.
   (CONVERGENCE-10)

3. **Cold-start day-0 = L3/L4-augmented, transitioning to lights-out
   per work-unit-class as evidence accumulates.** Tracks 1, 3, 7, 9
   converge with mechanistic detail. Brief §2.1 option (c)+(b)
   territory; corpus-grounded in Jaymin thresholds.

### Convergences to surface as DECISIONS-PENDING (corpus-real but bias-guard-amplified)

1. **Invariant/body split for MISSED-3.** Strong for greenfield;
   brownfield tracks disagree or elide. The split is corpus-grounded
   but the *six-track speed* is bias-guard-driven. (CONVERGENCE-1)

2. **Tier-axis as unified-architecture organizing principle.** Two of
   three unified tracks; the third (Brier pace-layers) is a coherent
   alternative. Phase 3 should produce *two* unified drafts (tier-shape
   and pace-layer-shape) and let the user / Phase 4 substrate
   extraction adjudicate. (CONVERGENCE-3)

3. **Cognitive escrow as substrate primitive.** Seven tracks; bias-guard
   F53 amplified prominence. Phase 3 should explicitly check whether
   report 30 + Kahana alone justify substrate-primitive status without
   the bias-guard editorial framing. (CONVERGENCE-5)

### Convergences to NOT weight as evidence

1. **Lights-out = L4-with-re-entry NOT L5.** Brief told all tracks to
   resolve via option (c)+(b). Compliance, not convergence.
   (CONVERGENCE-4)

2. **Brier pace-layers as universal reference.** Miscategorization-audit
   CHALLENGE-14 mandated all tracks engage. Compliance.
   (CONVERGENCE-9)

3. **WEAK-5 third position framing.** Bias-guard-originated framing
   reproduced verbatim. (CONVERGENCE-6)

4. **D-3 Natural-Language-Register extension.** Bias-guard-prompted
   acknowledgment; no track actually redesigns around it.
   (CONVERGENCE-7)

### Non-convergences to surface explicitly

1. T4's D-1 challenge (EAI store more durable than spec for brownfield)
   is a load-bearing dissent — surface as DECISIONS-PENDING.

2. T6's alternative MISSED-3 resolution (ingestion artifact alongside
   spec, not above) is a substantive minority position — preserve in
   Phase 3 brownfield draft, do not silently overwrite with the
   invariant/body split.

3. T8's pace-layer-axis as alternative unified shape is the strongest
   available counter to tier-axis convergence — Phase 3 must produce
   both drafts.

4. The collapse of Tournament-style population architecture across
   all nine tracks is a Phase-7 back-fill question, not a Phase-3
   merge question — surface for the back-fill audit, not for the
   synthesis draft.

5. MISSED-9 (CaMeL utility tax) is acknowledged but not acted on —
   surface to Phase-4 substrate-extraction as a specific
   `"is the substrate-is-cheap thesis safe against the CaMeL anchor?"`
   question.

### Overall recommendation

Phase 3 should produce **three drafts** as planned per D1
(greenfield-synthesis, brownfield-synthesis, unified-synthesis), but
the unified-synthesis should explicitly carry *two alternatives*
(tier-shape from T7+T9, pace-layer-shape from T8) rather than
collapsing them. The MISSED-3 invariant/body split should be
adopted for greenfield (corpus-strong, six-track convergence) but
flagged as DECISIONS-PENDING for brownfield (T4, T6 dissent
substantively).

The Phase-3 adversarial pass should specifically test:
- whether the invariant/body split survives without the MISSED-3
  citation prompt (CONVERGENCE-1 amplifier test);
- whether cognitive-escrow primitive status survives without the F53
  citation prompt (CONVERGENCE-5 amplifier test);
- whether the tier-axis classifier's deterministic-not-LLM
  commitment survives F51 scrutiny when the classifier itself is
  the substrate's hottest path (CONVERGENCE-3 robustness test).

*End.*
