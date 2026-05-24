---
guard: anchor-detector
phase: 2
based-on-commit: a0d4b67716d5158f7fa559344aa00463b4f5fece
based-on-date: 2026-05-24
---

# Phase-2 anchor-detector audit (cleaned-source re-run)

## §1 Method

Cross-read all 9 Phase-2 track outputs against the four candidate anchor
sources:

- `architectures/v3/00-brief-v3.md` (glossary, §2.1 option menu, §3 UC4
  framing, §4.1 defaults, §5 cold-start mandatory section).
- `architectures/v3/constraints-extracted.md` (UC1–UC8 prose).
- `architectures/v3/decisions-captured.md` (D1 unified-track instruction,
  D2 mandate-fit matrix, D5/D7 bias-guard disciplines).
- `architectures/v3/contradictions.md` + `failure-modes-v3.md` (the
  Phase-1 outputs that Phase-2 read as corpus-proxies).

Phase-1 bias-guard reports (`uncomfortable-contradictions-audit.md`,
`missing-failure-modes-audit.md`, `miscategorization-audit.md`) consulted
for methodological framing only — they are explicitly NOT cited as
corpus authority below; their findings appear here only as the lens for
"did Phase-2 inherit Phase-1's voice in a way that bypasses the underlying
corpus material?"

Did NOT read anything under `architectures/v3/history/`.

For each candidate anchor I checked four things:

1. Vocabulary echo across tracks vs. corpus-grounding of the term.
2. Architectural-move echo (same structural pattern across many tracks).
3. Citation-laundering (CTR-N / F-N IDs used as authority for a claim
   stronger than the cited material).
4. Convergence asymmetry (multiple tracks landing on "the same answer"
   in a way that traces to brief framing rather than to independent
   corpus drilling).

Quantitative pass: keyword-frequency sweep across the 9 tracks for
several anchor-suspect terms (per-track counts in §2).

---

## §2 Suspected anchoring findings

### F-ANCHOR-1 (HIGH, load-bearing) — Brief §2.1's "option (c)+(b)" working stance has become a 9-of-9 unanimous convergence

**Pattern.** Brief §2.1 enumerates 5 candidate resolutions to the
lights-out / L5 / regime tension (options a–e). At the end the brief
writes:

> *"The lead agent's working stance: option (c) plus (b) is the most
> likely shape, but the choice is open and load-bearing."*

Every track that I read addressed this concern by adopting exactly
option (c) + (b) — regime-classification + lights-out-over-a-defined-
surface. The unified-tracks defended it explicitly (`unified-A` §2,
`unified-B` §2.1, `unified-C` §2 lights-out section). The 6 mandate-
specific tracks each adopted it, several with the verbatim string
"option (c)+(b)" or "option (c) + (b)" (greenfield-cold-start-first §1.3
and §2; greenfield-methodology-first §2.1; greenfield-substrate-first
§2.A; brownfield-legacy-ingestion-first §2.1; brownfield-substrate-first
§2 (paraphrased); brownfield-methodology-first §2.1 (per-stage
restatement of the same shape)). No track adopted (a), (d), or (e); no
track meaningfully argued for a different framing.

**Tracks exhibiting:** all 9.

**Anchor source.** `00-brief-v3.md` §2.1 final paragraph
("*the most likely shape*"). The brief invited subagents to *test* the
mapping (CTR-A4) and *choose* among five options. They tested the
mapping (good) and then unanimously picked the option the brief
pre-recommended.

**Severity: HIGH, load-bearing.** This is the single highest-stakes
substantive convergence in the Phase-2 outputs, and it inherits its
shape almost entirely from one sentence in the brief. The underlying
corpus split (Shapiro L4 / Jaymin L5-anti / StrongDM
no-review-by-principle / Round-2 L3-ceiling) genuinely *might* be
resolved by (c)+(b), but the unanimity is suspicious because options
(a), (d), and (e) are not absurd — (e) in particular (corpus
counter-evidence to Jaymin's anti-pattern claim) is defensible from the
CTR-A1 internal-Jaymin tension that the bias-guard sharpening surfaced.

**Recommended Phase-3 action:** *challenge.* Dispatch a D7-style
blind-axis subagent with the instruction *"address brief §2.1 OQ-B1
without using option (c) or option (b). Defend an (a), (d), or (e)
resolution from the corpus."* If the subagent finds a defensible
alternative, the (c)+(b) convergence is partially brief-anchored. If
the subagent concedes (c)+(b) is best, the convergence is genuine. Cost:
one subagent; value: definitive separation of corpus signal from prompt
framing for the load-bearing OQ-B1.

---

### F-ANCHOR-2 (HIGH, load-bearing) — "Cognitive escrow" + Kahana primitives are now substrate-default across all unified tracks despite originating in a single late-corpus report

**Pattern.** All three unified tracks promote Kahana's "cognitive escrow
interval" (report 30) and the AILCCP three-controls (report 31 +
followup 10) to first-class *substrate primitives* — unified-A makes
the escrow interval the architecture's name and load-bearing object;
unified-B's axis is literally "pace-layer × cognitive-escrow"; unified-C
uses Kahana's framing as the structural-vs-voluntary discipline
warrant. The same Kahana-substrate framing then propagates downward into
4 of the 6 mandate-specific tracks (greenfield-cold-start-first's
"Cognitive-Escrow-Aware Operator Surface" primitive; greenfield-methodology-
first's STIR mandate; greenfield-substrate-first's Patrol scope;
brownfield-substrate-first's voluntary-discipline argument).

Keyword counts (escrow/EscrowInterval/interval-as-substrate):
unified-A 23, unified-B 37, unified-C 5, plus 4–7 in three of the
greenfield tracks.

**Tracks exhibiting:** unified-A, unified-B, unified-C, greenfield-cold-
start-first, greenfield-methodology-first, greenfield-substrate-first,
brownfield-substrate-first. (7 of 9.)

**Anchor source.** Two layers:
- Brief §5.1 names reports 25, 26, 30, 31, followup 10 as *required
  reading* for cold-start. Report 30 (Kahana cognitive escrow) is one
  of five.
- `contradictions.md` introduced F53 ("voluntary-discipline fragility")
  as a class with high architectural leverage — and the F53 class is
  Kahana-shaped. Tracks read F53 (and the bias-guard sharpening text
  that surrounds it) and inherited the Kahana framing as if it were
  multi-source corpus convergence.

**Why this is anchoring, not convergence.** Kahana is *one* author
(Stanford CodeX, 2026-03 papers). The corpus has at least four
independent voluntary-discipline-fragility surrogates (Willison "drift
under load," Vaughan/Challenger "normalization of deviance," Schillace's
own Attention Firewall, Anthropic Auto-Review). The tracks consistently
foreground Kahana as the *substrate-primitive-warrant* rather than as
*one of several converging voices*. That shape is what the brief's
required-reading list selected for. The corpus does support escrow-as-
phenomenon at multiple sources; it does NOT independently support
escrow-as-substrate-primitive at multiple sources.

**Severity: HIGH, load-bearing.** This is anchored because the cold-
start required-reading list told subagents which 5 reports to weight
heavily, and one of the 5 (Kahana) carried a substrate-shaped framing
(escrow interval as designable object). The Phase-2 outputs then made
the interval load-bearing in their substrate primitives — turning a
*phenomenology* into an *architecture*. Brief §5.1 caused this; brief
§5.1 is in turn user-mandated (Historian M5).

**Recommended Phase-3 action:** *re-cite + challenge.* For every track
that uses Kahana / escrow-interval / STIR as substrate-primitive
warrant, Phase-3 should: (a) require the citation to name the
*independent* corpus voices that support the *substrate-primitive* claim
(not the phenomenology claim), and (b) dispatch a blind-axis subagent
that addresses OQ-B2 (substrate-vs-methodology boundary) with cognitive-
escrow / interval-as-primitive *prohibited as a substrate primitive*.
The phenomenon stays; the substrate-promotion is what needs to clear an
anti-anchor bar.

---

### F-ANCHOR-3 (MEDIUM-HIGH, load-bearing for unified tracks specifically) — "Interval / escrow" is a likely D7 blind-axis-test trigger across unified-A, unified-B, and unified-C

**Pattern.** The three unified tracks were explicitly briefed (D1) to
*pick their own axis* and the brief expected divergence. Per D7 the
lead agent must dispatch a supplementary "axis-prohibited" subagent
whenever two or more unified tracks converge.

- **unified-A:** axis = "escrow-interval-as-substrate."
- **unified-B:** axis = "pace-layer × cognitive-escrow (interval-as-design-site)."
- **unified-C:** axis = "distance-from-frozen-anchor." Different axis,
  but unified-C still bases its threshold layer on Kahana / cognitive-
  escrow (§2 "Lights-out / L5 tension"; §5.3 silent-failure protection).

Two of three unified tracks have *interval* in their axis name; the
third leans on the same Kahana primitive for its discipline argument.
This trips D7's threshold ("two or more parallel subagents converge on
the same axis / framing / pattern-name").

**Tracks exhibiting:** unified-A, unified-B (axis-name level);
unified-C (framing-level).

**Anchor source.** The brief did not name "interval" or "escrow" as an
axis candidate — but `contradictions.md` heavily features Kahana's
escrow interval (CTR cluster on F42/F53; the bias-guard sharpening
quotes Kahana's "fragile dependency" phrasing repeatedly), and the
cold-start required-reading list put Kahana into every greenfield-
touching track. The unified tracks (all three address greenfield)
inherited the Kahana framing through this channel.

**Severity: MEDIUM-HIGH, load-bearing for the unified search
specifically.** Per D1, the divergence between the three unified tracks
*is the signal*. If two of three converge on interval-as-primitive
because the brief-required reading list put Kahana in front of all of
them, the D1 falsifiability test for UC4 is weakened — Phase-3's
"unified-mandate-attacker" pass operates on three drafts that are less
independent than they look.

**Recommended Phase-3 action:** *D7 blind-axis test, mandatory.*
Dispatch one supplementary unified-mandate subagent with the brief
*"pick an organizing axis for a unified greenfield + brownfield
architecture, but axes mentioning 'interval', 'escrow', or 'cognitive
escrow' are prohibited; substrate-primitives derived from Kahana
report-30/report-31 are also prohibited."* If the subagent finds a
defensible alternative axis, the interval/escrow convergence was at
least partially anchored on the cold-start required-reading list. If
the subagent concedes the interval framing is the corpus's strongest
answer, the convergence is genuine corpus signal that survived
cleaning.

---

### F-ANCHOR-4 (MEDIUM) — "Per-work-unit-class classifier" as a substrate primitive: D2's matrix has been promoted from documentation to architectural mechanism

**Pattern.** D2 defines a `mandate-fit` matrix (rows = architectures;
columns = work-unit-classes; cells = fit values). This is documentation
discipline — how the comparison artifact should be shaped. Most Phase-2
tracks have promoted it into a *runtime substrate mechanism* — a
"classifier" or "eligibility classifier" that decides per-work-unit-
class regime at cycle-open time.

- greenfield-substrate-first §1.S9: "Eligibility classifier (regime-
  naming substrate primitive)."
- unified-A §1: "Classifier" is one of the 5 substrate primitives;
  decides automation-eligibility and work-unit-class per interval.
- brownfield-legacy-ingestion-first §1: "model-driven classifier is the
  substrate primitive that resolves the §2.1 lights-out / L5 / regime
  tension."
- brownfield-methodology-first §1 stage-1: classifier-shaped trigger
  intake.
- unified-C §1 primitive 3: "Distance-gated dispatcher" plays the
  same role.
- greenfield-cold-start-first §1.3 graduation protocol: graduation
  protocol is a temporal classifier.
- unified-B §1: regime is per-layer, which is a classifier on a
  different axis but the same shape.

Per-track classifier/work-unit-class mention counts: greenfield-substrate-
first 21; brownfield-methodology-first 14; unified-A 12; greenfield-cold-
start-first 12; brownfield-legacy-ingestion-first 10.

**Tracks exhibiting:** 7 of 9 in load-bearing fashion (all except
greenfield-methodology-first, which uses Regime A/B instead of a per-
unit classifier, and unified-B, which uses per-layer rather than per-
unit).

**Anchor source.** D2 (decisions-captured.md): the matrix-by-work-unit-
class schema. The brief §0 enumerates the 5 work-unit-classes
(`initial-spec / refactor / mvp / post-mvp-evolution / regression-fix`)
and warns they are *illustrative*. Subagents read this as a typology
rather than as a documentation schema, and built classifiers around it.

**Why this is anchoring (and partially genuine).** The corpus does
support *some* per-work-unit regime declaration (Jaymin's per-task
thresholds, Anthropic's per-task auto-review, Klaassen's per-cycle
dispatch). But the precise shape *"a substrate-resident classifier
that names regime and automation-eligibility per work-unit-class at
cycle-open time"* is much more specific than the corpus warrant
supports. D2's documentation-matrix was the seed.

**Severity: MEDIUM.** Load-bearing for the Phase-5 substrate-primitive
ADR set (which now inherits a "classifier" primitive across 7 tracks).
Not load-bearing for the UC4 hypothesis test.

**Recommended Phase-3 action:** *re-cite.* Phase-3 should require any
track using a substrate-resident classifier as a primitive to cite a
corpus warrant for *the substrate-resident classifier itself*, not for
"per-work-unit regime classification in general." If no such warrant
exists, the classifier is a brief-derived primitive that should be
demoted to a *methodology* primitive in Phase-4's substrate/methodology
extraction — or surfaced as a DECISIONS-PENDING item.

---

### F-ANCHOR-5 (MEDIUM) — "Two-regime split" (cold-start vs steady-state) is brief-suggested phrasing now baked into greenfield architectures

**Pattern.** Brief §5 mandates a cold-start section. The brief itself
does not say "treat cold-start and steady-state as two regimes," but
the cold-start required-reading list + the §5.2 questions ("What is the
trajectory from day 0 → day N?") strongly imply a regime-split.

- greenfield-cold-start-first §1: explicit "Cold-Start Regime" and
  "Steady-State Regime" with a "graduation protocol" between them.
- greenfield-methodology-first §1.1 / §1.2: explicit "Regime A —
  Spec-discovery" / "Regime B — Spec-anchored execution."
- greenfield-substrate-first §5.3: implicit day-0 → day-N trajectory
  with similar shape.
- unified-A §5.4: graduation conditions (3 numbered).
- unified-B §5.6: explicit day-0–7 / day-7–30 / day-30+.
- unified-C §5: "distance-distribution shift" as the steady-state
  transition.

**Tracks exhibiting:** 5 of 9 (3 greenfield, 2 unified) name an
explicit two-regime or graduation structure.

**Anchor source.** Brief §5.2 four questions; cold-start required-
reading list which weights graduation/maturity framings (Kahana's
"factory-without-track-record"; Caremark/RSI's "compounding ability").

**Severity: MEDIUM.** Largely *defensible* — cold-start vs steady-state
is a real distinction. But the *substrate-level mechanism* (graduation
protocol; bench saturation; K=5 ≥90% bar) repeats almost verbatim
across the cold-start track, the unified tracks, and the methodology-
first track. The specific *mechanism* is more anchored than the
*distinction.*

**Recommended Phase-3 action:** *challenge mildly.* Phase-3 should
test whether the graduation protocol could plausibly be replaced by a
continuous-regime model (no discrete transition; the substrate just
re-measures bars per cycle). If the continuous model is defensible,
the discrete-regime convergence is brief-anchored.

---

### F-ANCHOR-6 (LOW-MEDIUM) — "Spec-malleable" and "code-archaeological" labels appear as architectural premises despite the brief's contamination footnote warning

**Pattern.** The brief's §3 footnote explicitly flags these as "lead-
agent shorthand for UC4's longer prose" and instructs adversarial
subagents to *challenge the underlying claim, not the labels*. Several
tracks treat the labels as the claim:

- greenfield-cold-start-first §0 / §2: cites "spec-malleable" then
  challenges it by *appealing to El Kaim invariants* (good — challenges
  the claim).
- unified-C §0: "spec-malleable" is operationalised as
  "near-anchor-on-greenfield" — a re-encoding of the label rather than
  a challenge to the underlying UC4 claim.
- brownfield tracks generally use the label faithfully (claim is
  brownfield-true even by the contamination footnote's logic).
- unified-A §2: treats spec-malleability and code-archaeological as
  per-interval-policy expressions.

**Tracks exhibiting:** 9 of 9 use the labels; 2 (greenfield-cold-start-
first, unified-A) interrogate the underlying claim non-trivially; the
other 7 essentially accept the label.

**Anchor source.** Brief §3 + glossary. Despite the contamination
footnote, the labels are *frequent* in the brief and decisions documents,
which gives them anchor-weight regardless of the footnote disclaimer.

**Severity: LOW-MEDIUM.** The brief acknowledged this risk and adopted
the footnote as the agreed mitigation. The footnote partially worked
(2 of 9 tracks substantively interrogate); largely did not (7 of 9
treat label as fact).

**Recommended Phase-3 action:** *ignore in Phase 3, surface for Phase
7.* The footnote mitigation is structurally what the brief intended;
expecting more would require re-writing UC4 itself, which is a user
constraint. Phase-7 back-fill should be alert to this when re-examining
v1/v2 material that used different language.

---

### F-ANCHOR-7 (LOW) — Citation laundering check (mostly clean)

**Pattern checked.** Across the 9 tracks, I checked for cases where
CTR-N or F-N IDs are cited as authority for a stronger claim than the
underlying corpus item supports.

**Findings.** Citation discipline in the Phase-2 tracks is largely
clean. Most tracks cite the underlying report (e.g., "report 30 §3"
rather than "F53") and where they cite CTR-IDs they usually do so as
shorthand for the underlying split. Exceptions are minor:

- unified-B §2.5 cites "F46 mitigation" as if F46 named a specific
  mechanism (cross-model review); in `failure-modes-v3.md` F46 is the
  failure mode, not the mitigation — the mechanism is corpus-anchored
  elsewhere (CJ Hess kevin/carl, report 34). The track does cite
  report 34 separately, so this is shorthand-laundering at worst.
- Several tracks cite "CTR-C2" as authority for "substrate-heavy is
  contested" — accurate.
- The bias-guard sharpening citation discipline (cite the underlying
  corpus, not the WEAK-N / MISSED-N ID) is honored in the tracks I
  checked; no track cites a WEAK-N ID as authority.

**Severity: LOW.** Discipline is being followed.

**Recommended Phase-3 action:** *no action; standing discipline
maintained.*

---

## §3 Genuine convergences (corpus signal that survived cleaning)

The following are convergences I assess as *not* primarily brief- or
decisions-anchored — they look like the cleaned corpus pushing the
same answer:

**G-CONV-1 — Cross-model judging at high-stakes work units.** 9 of 9
tracks adopt some form of cross-model / different-family judge for
high-stakes or far-anchor cycles, citing the CJ Hess kevin/carl
exemplar (report 34) and the F46 failure-mode anchor independently of
the brief. The corpus pressure on this is genuine: Anthropic auto-
review (report 23 §3.5), kevin/carl (report 34), Husain/Shankar
(followup 07) all push at this. The tracks correctly diverge on
*how much* cross-model is required (Anthropic same-model-different-role
vs. CJ Hess cross-model vs. mixed); this divergence is the signal of
real corpus engagement. Phase-3 should treat this as keep-load-bearing.

**G-CONV-2 — Holdout-discipline-as-substrate (D-4).** 9 of 9 tracks
accept D-4 with justification. This is corpus-grounded (Round-2 C13,
StrongDM, El Kaim EvaluationSuite, OpenHands SecurityAnalyzer) and the
tracks' justifications cite the underlying material. Genuine.

**G-CONV-3 — D-2 challenged for brownfield, accepted for greenfield.**
The three brownfield tracks all challenge D-2 ("scenarios outside
codebase as holdout"); the three greenfield tracks accept it. The
unified tracks split it per-mandate (greenfield branch accepts;
brownfield branch challenges). This is the exact shape the brief
itself flagged as "fragile for brownfield" — but the tracks' arguments
cite primary sources (CTR-B5 WEAK-3 sharpening of StrongDM's own
practice; production traces; existing tests) rather than the brief's
flag. Convergence is corpus-supported.

**G-CONV-4 — Trajectory capture (D-7) accepted across the board.**
Anchored on OpenHands V1 sub-ms persist; corroborated by
multiple tracks citing the same measurement context. Genuine; the
caveats about generalization beyond OpenHands' benchmark are also
inherited correctly.

**G-CONV-5 — F36/F37 (Yang/Larbi underspecification) as a cold-start /
spec-author bottleneck.** All cold-start and greenfield-touching tracks
cite Yang's 98.7%→85.0% ceiling and Larbi's 73.8%→6.7% contradictory-
prompt collapse independently, propose chunking and contradiction-
detection as mitigations independently. Corpus signal is real.

**G-CONV-6 — Sandbox / production-scissors-off as substrate default.**
F44 (Shapiro R1–R5) cited independently across mandate-touching
tracks. Genuine.

**G-CONV-7 — D-3 (Agent = Model + Harness) challenged by multiple
tracks.** unified-A, unified-B, unified-C, plus several mandate-
specific tracks all challenge D-3 from different angles (graph-node /
population shapes; CTR-C10 natural-language-register; anchor-context).
The brief flagged D-3 as fragile, but the tracks bring *additional*
corpus material (CTR-C10 report 37) beyond what the brief warned of.
Convergence is partially-anchored-but-extended-with-real-evidence.

---

## §4 Recommendations to Phase 3

1. **Mandatory D7 blind-axis test on the lights-out / L5 (c)+(b)
   convergence (F-ANCHOR-1).** Dispatch one supplementary subagent with
   the brief *"address OQ-B1 without using option (c) or (b) from brief
   §2.1; defend an (a), (d), or (e) resolution."* The unanimity is the
   single highest-stakes brief-anchored convergence in the Phase-2
   outputs and clearing this through the D7 mechanism is the cheapest
   way to separate signal from anchoring.

2. **Mandatory D7 blind-axis test on the interval / escrow unified-
   track convergence (F-ANCHOR-3).** Dispatch one supplementary
   unified-mandate subagent with cognitive-escrow / interval-as-
   substrate-primitive *prohibited*. If a defensible alternative
   emerges, the D1 falsifiability test for UC4 is partially
   anchor-driven and needs adjustment.

3. **Citation-tightening pass on substrate-primitive claims derived
   from Kahana (F-ANCHOR-2).** Phase-3 merge should require any
   substrate-primitive claim (interval, escrow, classifier, STIR,
   graduation protocol) to cite *multiple independent corpus voices*
   for the substrate-primitive promotion specifically — not just
   independent voices for the underlying phenomenon. Single-source
   substrate primitives should be demoted to methodology primitives or
   surfaced as DECISIONS-PENDING.

4. **Re-examination of "per-work-unit-class classifier" as substrate
   primitive (F-ANCHOR-4).** Phase-4's substrate/methodology extraction
   should treat the classifier as a primitive-candidate that has to
   *earn* substrate status, not as inherited from D2's documentation
   schema. The corpus warrant for a runtime classifier (vs. a
   documentation matrix) needs to be cited explicitly.

5. **Continuous-regime alternative test for the graduation protocol
   (F-ANCHOR-5).** When merging the greenfield syntheses, surface
   "continuous regime measurement per cycle" as an alternative to the
   discrete cold-start → steady-state transition and let Phase-3 weigh.

6. **No action needed on labels (F-ANCHOR-6) and citation discipline
   (F-ANCHOR-7).** The mitigation footnote is the agreed mechanism;
   citation laundering is minor and within accepted shorthand.

---

## §5 Limits of this audit

- **The audit cannot reach the contaminated prior run** (history/
  forbidden). If the prior contamination produced a specific anchor
  shape that the cleaned re-dispatch *appears* to have escaped, I
  cannot verify that the new convergences are not the same convergences
  reached by a slightly different route. The D7 blind-axis tests in
  §4 are the only definitive separation.
- **Reading depth.** I read all 9 tracks in full but the corpus
  material itself only at the level of the framing documents
  (`contradictions.md`, `failure-modes-v3.md`, `00-brief-v3.md`,
  `constraints-extracted.md`, `decisions-captured.md`). For
  citation-laundering checks (§2 F-ANCHOR-7) I relied on the tracks'
  citations + the framing documents' own cited material; I did NOT
  re-read the underlying research reports. A track citing report 30
  for something report 30 doesn't actually say would slip past this
  audit.
- **Concurrent bias-guard dispatch.** The splitter, lumper, and
  axis-divergence-auditor are running concurrently and independently. I
  cannot triangulate findings against theirs. Specifically, the
  axis-divergence auditor is likely to surface F-ANCHOR-1 and
  F-ANCHOR-3 from a different angle; the splitter/lumper may surface
  the classifier primitive (F-ANCHOR-4) as a granularity issue. Any
  agreement across all four guards is itself signal.
- **Brief / constraints / decisions / contradictions are themselves
  anchored.** The brief explicitly inherits Round-2 framing; the
  contradictions register includes bias-guard sharpening text that
  reads at near-corpus authority weight to subagents. I cannot
  cleanly distinguish "brief anchored Phase-2" from "Phase-1 anchored
  Phase-2 via the contradictions register Phase-2 read." Several of
  the findings above (especially F-ANCHOR-2 and F-ANCHOR-4) carry
  some of both.
- **No quantitative anchor-detection model.** Keyword counts in §2 are
  illustrative, not measurement; the severity assignments are my
  judgment, not derived from a model.
- **9 of 9 unanimity is suspicious by construction; I may be over-
  weighting unanimity.** Some convergences (G-CONV-1, G-CONV-2,
  G-CONV-4) are unanimous and look genuine. Unanimity is necessary
  but not sufficient evidence of anchoring; the §4 D7 tests are the
  way to resolve which is which.

---

*End of anchor-detector.md.*
