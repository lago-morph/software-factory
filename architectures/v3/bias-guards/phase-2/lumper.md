---
guard: lumper
phase: 2
based-on-commit: a0d4b67716d5158f7fa559344aa00463b4f5fece
based-on-date: 2026-05-24
---

# Phase-2 lumper — false-convergence audit

## §1 Method

I read all 9 Phase-2 tracks plus the v3 framing artifacts ([brief](../../00-brief-v3.md), [corpus inventory](../../corpus-inventory.md), [contradictions](../../contradictions.md), [failure modes](../../failure-modes-v3.md), [decisions](../../decisions-captured.md)) and Phase-1 bias-guard outputs. For each candidate unified label I asked: *does the corpus draw a distinction the tracks are folding together?* For each candidate I checked at least one corpus citation that already preserves the split (CTR-ID, F-ID, or report anchor) and counted how many of the 9 tracks exhibit the collapse. I scored "load-bearingness" as: *would Phase-3 ADRs come out differently if the split were preserved?* I did not enumerate every shared phrase — only convergences large enough that the merger would harden into a Phase-3 default. False-divergence is out of scope (splitter's brief).

A note on the dominant pattern: most false convergences across the 9 tracks land at **substrate-mediation-of-discipline** vocabulary — "the substrate enforces X" gets reused across distinct enforcement mechanisms that have different cost, different failure modes, and different Phase-4 placement consequences. The single biggest such cluster is the **judge** lump (cluster 1). The lights-out / cold-start / scenarios clusters are also load-bearing but the corpus itself has done more disambiguation work there, so the tracks' collapses are visible against a clear corpus baseline.

## §2 False-convergence clusters

Numbered in rough order of architectural load-bearingness; split/keep-merged recommendation at each.

### Cluster 1. "Cross-model judge" / "cross-family judge" / "judge diversity" — single label, three corpus phenomena

**Surface concept.** All 9 tracks invoke some version of "cross-model judge" or "judge-diversity" (most often as the F46 / F1 / F27 mitigation), and treat it as one architectural commitment.

**Corpus distinctions being collapsed.** The corpus draws at least four distinct judge-shape positions, registered as separate contradictions:

- **CTR-D4** (F1 substrate-mitigable vs. architecture-mitigable) — *where* the diversity lives, not just *that* it lives.
- **CTR-D7** (Anthropic *same-model judging is fine when the judging task differs from the work task*, followup/07 §3.6) — Anthropic's primary-anchored finding that same-model-different-role suffices.
- **CTR-D8** (Tournament's *model-family diversity as necessary defense*) — diversity is necessary, not contingent.
- The **Anthropic "five-critic Auto-Review"** pattern (report 23 §3.5) is **same-model-different-role**; CJ Hess `kevin/carl` (report 34 §6.2) is **different-model-different-task**; OpenAI Codex Auto-Review (report 18) is **same-model-different-prompt**. These three are not interchangeable.

**Tracks exhibiting the collapse.**
- [`greenfield-substrate-first` §1.S6](../../tracks/greenfield-substrate-first.md) at least types the choice (`same-model-different-task` vs. `cross-model-different-task` vs. `same-model-different-role`) — closest to corpus-faithful but still flattens the four CTR positions into a single typed parameter.
- [`greenfield-methodology-first` §1.2](../../tracks/greenfield-methodology-first.md) declares cross-model review as the Regime-B default citing only F46 / `kevin/carl`, against CTR-D7.
- [`greenfield-cold-start-first` §1.2](../../tracks/greenfield-cold-start-first.md) runs *both* same-model and cross-model judges and escalates on disagreement — treats them as substitutable producers of "the judge signal," not as distinct mechanisms.
- [`brownfield-substrate-first` §1.1 S-5](../../tracks/brownfield-substrate-first.md) and [`brownfield-methodology-first` §1.1 stage 6](../../tracks/brownfield-methodology-first.md) both reduce to "cross-family routing" — same-model-different-role drops out.
- [`brownfield-legacy-ingestion-first` §3](../../tracks/brownfield-legacy-ingestion-first.md) cites CTR-D4 + CTR-D7 sharpening but then collapses to "cross-model independent signal."
- [`unified-A` §1](../../tracks/unified-A.md) types `judge-diversity: same-model | different-role | different-family` — most explicit retention, but the `different-role` slot is then never operationalized.
- [`unified-B` §2.4](../../tracks/unified-B.md), [`unified-C` §1](../../tracks/unified-C.md) merge again to "cross-model judge at mid/high distance."

**Consequence if preserved.** Phase-5 judge ADRs differ in cost (cross-family is ~2× per-cycle inference; same-model-different-role is ~1.1×), in failure mode (cross-family avoids F46; same-model-different-role does not), and in *whether the Anthropic primary-anchored finding has been engaged at all*. A merged "cross-model judge" default smuggles the Tournament side of CTR-D8 in as architecture; explicitly preserving the three judge-shapes forces a per-(work-unit-class × stakes) selection.

**Recommendation: SPLIT.** Phase-3 should retain at minimum the three-way distinction (cross-family / same-model-different-role / same-model-different-prompt) as separate substrate parameters, *not* a single `cross-model` flag. The Anthropic same-model-different-role position is corpus-load-bearing and currently being silently overridden by the F46 side of the cluster.

### Cluster 2. "The substrate enforces holdout" — D-4 collapsed across radically different enforcement loci

**Surface concept.** Every track marks D-4 as `accepted with justification` and asserts "substrate-enforced holdout." The phrase reads as one architectural commitment.

**Corpus distinctions being collapsed.** D-4 names *a discipline* (acceptance criteria withheld from builder agents); what the corpus actually requires varies sharply with where the scenarios live:

- **Out-of-tree directory holdout** (the original D-2 framing): substrate enforces by filesystem partition / read-mask. Cheap, deterministic.
- **In-tree-but-partitioned holdout** (CTR-B5 / CTR-G2 inversion): substrate must partition *reads of the live codebase* by agent role. This is structurally a different primitive: it requires per-role view filters on the codebase index itself, not directory-level isolation.
- **Telemetry-as-scenario holdout** (S-3 in `brownfield-substrate-first`): substrate must partition *runtime telemetry streams* by role at ingest time. Different mechanism again.
- **Builder-doesn't-share-context-with-bench-author** (cold-start track's day-0 D-4): substrate enforces *temporal/sessional* partition between two agent roles working on the same artifact set. None of the above primitives covers this case.

**Tracks exhibiting the collapse.** All 9 mark D-4 `accepted with justification`. [`brownfield-substrate-first` §1.1 S-3](../../tracks/brownfield-substrate-first.md), [`brownfield-methodology-first` stage 7](../../tracks/brownfield-methodology-first.md), and [`brownfield-legacy-ingestion-first` §1](../../tracks/brownfield-legacy-ingestion-first.md) all assert "in-model partition" without distinguishing the three brownfield enforcement loci (codebase view / test set / telemetry). [`greenfield-cold-start-first` §1.2 sub-phase B](../../tracks/greenfield-cold-start-first.md) collapses the bench-author/builder context-share case into "D-4 substrate-enforced." [`unified-A` §4 D-4](../../tracks/unified-A.md) is the most explicit lumper: a single policy-mediator interlock claims to cover all of these.

**Consequence if preserved.** Each enforcement locus is a distinct Phase-5 ADR with distinct cost and distinct attack surface. F28 (holdout leakage) does not have one mitigation; it has at least four. The merged framing lets a "substrate-enforced" assertion paper over the case the architecture has not actually built a primitive for.

**Recommendation: SPLIT.** Phase-3 should make D-4 a *family* of disciplines parameterized by scenario-locus (out-of-tree / in-tree-partitioned / telemetry / co-authored-bench). Phase-4 substrate/methodology extraction must then assign each to a primitive separately.

### Cluster 3. "Lights-out = brief §2.1 option (c)+(b)" — same answer, different operationalisations

**Surface concept.** All 9 tracks adopt brief §2.1 option (c)+(b) — regime classification + lights-out over a defined surface. The convergence reads as a coordinated resolution of OQ-B1.

**Corpus distinctions being collapsed.** What "the surface" actually is differs across tracks; the corpus separates several candidate surfaces and the collapse hides the choice:

- *Work-unit-class surface* (D2 mandate-fit matrix; the brief's nominal granularity).
- *Per-stage surface* (`brownfield-methodology-first` §2.1: stages 1–7 lights-out, stage 8 escalates).
- *Per-interval surface* (`unified-A`: every `EscrowInterval` carries its own automation-eligibility).
- *Per-distance surface* (`unified-C`: regime is a function of anchor-distance, not class).
- *Per-cold-start-phase surface* (`greenfield-cold-start-first`: uniform L3 in cold-start, classified in steady-state).
- *Per-layer surface* (`unified-B`: lights-out at L4 only; L0–L3 transitions are L3-Aug).

These are not the same answer. CTR-A4 (vocabulary mapping) is "decisive" only against a *specific* surface choice; the corpus' L5-anti-pattern claim (CTR-A1) bites differently against each.

**Tracks exhibiting the collapse.** All 9 use the (c)+(b) framing; only `unified-A`, `unified-B`, `unified-C`, and `greenfield-cold-start-first` actually pick a distinct surface. The other five tracks invoke (c)+(b) without specifying what the regime-classification axis is, which lets the surface default silently to D2's work-unit-class taxonomy.

**Consequence if preserved.** OQ-B6 (which empirical bars) is a *function* of which surface is chosen — Jaymin's K=5 is measured against work units, not intervals, not layers, not distances. A merged (c)+(b) framing makes the bar look settled when in fact each surface choice picks a different bar.

**Recommendation: SPLIT.** Phase-3 should treat "option (c)+(b)" as a *schema* with five surface-choice variants and force each track's lights-out treatment to declare its surface explicitly. The convergence on (c)+(b) is real but it is convergence on a *family* of answers, not one answer.

### Cluster 4. "Cold-start" / "legacy-ingestion" / "bootstrap interval" / "ingestion phase" — distinct phenomena merged under day-0 framing

**Surface concept.** Tracks freely interchange "cold-start," "bootstrap," "legacy-ingestion," "ingestion phase," and "day 0" — and treat them as a single phenomenon admitting one structural answer.

**Corpus distinctions being collapsed.** CTR-G3 is *the contradiction explicitly registered against this conflation*: "cold-start (greenfield) vs. legacy-ingestion (brownfield) — symmetric or asymmetric?" The corpus does not resolve symmetry; the brief §5 designation is greenfield-only. Two further distinctions:

- *Operator-intent-bootstrap* (greenfield day-0: no codebase, operator must author intent) — Historian M4/M5 designates as load-bearing risk.
- *Codebase-archaeology bootstrap* (brownfield day-0: codebase exists, must be ingested into a queryable model) — different inputs, different priors, different failure modes (F25 design-starvation vs. F21 context-exhaustion).
- *Micro-cold-start per new work-unit-class* (`greenfield-cold-start-first` §5: cold-start primitives reactivate for each new class). This is a third phenomenon — recurring intra-factory regime change, not a one-shot bootstrap.

**Tracks exhibiting the collapse.** [`brownfield-substrate-first` §5](../../tracks/brownfield-substrate-first.md) and [`brownfield-legacy-ingestion-first` §5](../../tracks/brownfield-legacy-ingestion-first.md) both treat their "legacy-ingestion" sections as the brownfield analog of greenfield cold-start while *also* invoking the cold-start required-reading subset (reports 25/26/30/31/followup-10) — the analog claim is asserted, but the required reading is the *greenfield* set, which Phase-1 bias-guard re-tagged greenfield-primary for reasons (CHALLENGE-1 / CHALLENGE-2). [`unified-A §5`](../../tracks/unified-A.md), [`unified-B §5`](../../tracks/unified-B.md), [`unified-C §5`](../../tracks/unified-C.md) all carry a single "bootstrap" treatment that elides whether they are answering the greenfield bootstrap, the brownfield ingestion, or both. `unified-A` is most explicit ("the bootstrap interval is the architecture's day-0 shape") and most lumping — greenfield and brownfield bootstrap are claimed to fall out of the same `EscrowInterval{kind: bootstrap}` with different `priors.in-tree`, which is precisely the symmetry CTR-G3 does not establish.

**Consequence if preserved.** Brief §5's required-reading discipline (Historian M5) is *greenfield-targeted*; brownfield analogs invoking it borrow corpus weight they have not earned. The micro-cold-start phenomenon, currently surfaced only in one track, has different substrate consequences (re-entry protocol, not bootstrap protocol).

**Recommendation: SPLIT.** Phase-3 should keep three distinct day-0/recurring-day-0 phenomena: greenfield intent-bootstrap, brownfield code-archaeology, and intra-factory regime-change (micro-cold-start). The brief §5 mandatory-section rule applies to greenfield intent-bootstrap only; brownfield code-archaeology needs its own discipline if it is to claim equivalent weight (CTR-G3 must be answered, not assumed).

### Cluster 5. "Scenarios" — Kaner / EARS-criteria / production-traces / holdout-set / acceptance / bench

**Surface concept.** "Scenario" is used uniformly across tracks. The example from the dispatcher brief.

**Corpus distinctions being collapsed.** Followup/09 (Kaner) gives scenarios five+sixth defining characteristics (story / motivating / credible / complex / easy-to-evaluate / power). Report 25 (EARS) gives acceptance criteria a five-pattern grammar. SWE-bench Verified gives held-out test cases. Report 1 ("Tokens are the fuel") gives production traces / incident replays / agentic simulation. These are *different artifact shapes* with different authoring discipline, different judges, different cost. The corpus distinguishes them; CTR-B5 / D-2's "fragile" flag is precisely the point at which the conflation bites.

**Tracks exhibiting the collapse.** [`greenfield-cold-start-first`](../../tracks/greenfield-cold-start-first.md) uses "bench" for a Kaner-style scenario set but "acceptance criterion" interchangeably in its EARS-mandated section; the two are conflated as "scenario+criterion" pairs. [`unified-A` §1](../../tracks/unified-A.md) lists `[scenarios, exemplars, adjacent-domains, operator-knowledge]` and `[codebase, tests, runtime-telemetry, prior-cycle-artifacts]` as `priors` slots — scenarios and tests are *distinct shapes*; the lump erases the distinction. [`brownfield-substrate-first` S-3](../../tracks/brownfield-substrate-first.md) calls telemetry "scenario" without preserving the Kaner-vs-trace distinction. [`brownfield-methodology-first` stage 7](../../tracks/brownfield-methodology-first.md) explicitly merges: "scenarios MAY be drawn *from the codebase* — production traces, existing integration tests, telemetry-derived assertions" — three corpus-distinct shapes under one label.

**Consequence if preserved.** Holdout discipline (cluster 2) cannot even be specified without knowing which shape is being held out. A Kaner scenario has a `power` field; an EARS criterion has a pattern type; a production trace has a sampling-policy; a regression test has expected output. Mitigation primitives differ per shape.

**Recommendation: SPLIT.** Phase-3 should keep at minimum a four-way taxonomy: (i) Kaner-scenarios (operator-authored ground-truth stories); (ii) EARS acceptance criteria (per-spec verifiability constraint); (iii) regression / holdout test cases (executable, pass/fail); (iv) production traces / telemetry (sampled runtime evidence). Tracks may then declare which they hold out, which they author, which they inherit. The merged "scenarios" label is currently doing all four jobs.

### Cluster 6. "The codebase" — monolithic substrate input

**Surface concept.** Brownfield tracks treat "the codebase" as the single substrate input the factory reads.

**Corpus distinctions being collapsed.** Brief §0 (Brownfield mandate definition) explicitly enumerates: *"The codebase, its tests, dependencies, runtime telemetry, and accumulated history"* — five distinct input categories. F20 (maintenance asymmetry, brownfield-critical), F21 (context exhaustion), F34 (cross-layer drift) attach to *different* categories. CTR-G4 (code-as-opaque vs. code-as-archaeological) is one slice; the test suite, the dependency graph, the runtime telemetry, and the issue/PR history each have their own corpus citations and their own mitigations.

**Tracks exhibiting the collapse.** [`brownfield-substrate-first`](../../tracks/brownfield-substrate-first.md) is actually the *least* lumper here — it splits into S-1 (index), S-2 (dependency graph), S-3 (telemetry), S-4 (change history). [`brownfield-methodology-first` stage 2](../../tracks/brownfield-methodology-first.md) merges all into "archaeological brief." [`brownfield-legacy-ingestion-first`](../../tracks/brownfield-legacy-ingestion-first.md) splits the model into six views but treats them as derivable from a single ingestion pass over "the codebase." The unified tracks (`unified-A` §1 `priors.in-tree`, `unified-C` §1) lump the five inputs into a flat list.

**Consequence if preserved.** The five inputs require different substrate primitives with different cost and different maintenance cadence (S-1's incremental index updates per commit vs. S-3's telemetry ingest pipeline vs. S-4's git-history scan). Treating the codebase as monolithic substrate is what F21 (context exhaustion) names as the load-bearing failure.

**Recommendation: SPLIT (partial).** The five-way input split is already corpus-canonical (brief §0); Phase-3 should require any track invoking "the codebase" or `priors.in-tree` to enumerate which of code / tests / deps / telemetry / history it actually consumes. Phase-4 substrate extraction is where this bites hardest — a single "codebase reader" primitive will not work.

### Cluster 7. "Re-entry" — a single OQ-B3 answer hiding distinct human-loop topologies

**Surface concept.** OQ-B3 (human re-entry) is treated as one mechanism across tracks: watchdog-escalation triggers re-entry, substrate hands a packet to the operator, operator decides.

**Corpus distinctions being collapsed.** Re-entry has at least three distinct corpus-grounded varieties:

- *Watchdog-triggered escalation* (Patrol-tier per C14): substrate-initiated, operator-receives-packet.
- *Operator-pulled inspection* (Jaymin Augmentation Mode, report 09 §5.5): operator-initiated sample audit.
- *Anchor-edit / regime-change re-entry* (`unified-C` §1: `anchor-edit` is always L4; `greenfield-cold-start-first` graduation): structural re-entry at typed events that are *not* failures.

Plus the **degradation re-entry** (`greenfield-cold-start-first` §2.4: de-graduation back to Augmentation when bars fall) — which is a fourth, different from escalation.

**Tracks exhibiting the collapse.** Most tracks invoke "re-entry per OQ-B3" without distinguishing which variety they mean. [`unified-A` §1](../../tracks/unified-A.md) does best by typing `kind: re-entry` as a node class, but then its policies do not distinguish escalation-re-entry from regime-change-re-entry.

**Consequence if preserved.** The handback protocol shape (what artifacts the operator receives, what state the substrate freezes, what authority the operator has on return) differs by re-entry kind. A merged OQ-B3 answer leaves the protocol underspecified.

**Recommendation: SPLIT.** Phase-3 should require any re-entry treatment to declare which variety (escalation / sample-pull / structural / degradation). The brief's reframe of OQ-B3 already names this is plural ("what conditions cause a human to enter the inner loop, who decides"); the tracks have flattened it back to singular.

### Cluster 8. "Spec" — five corpus shapes under one label

**Surface concept.** All tracks talk about "the spec." Some qualify (change-intent block, intent block, EARS criteria, delta-spec, layer-2-spec) but the qualifications drift across tracks.

**Corpus distinctions being collapsed.** D-1 names "the spec." The corpus actually has at least:

- El Kaim's 9-field **intent block** (report 14) — typed object.
- EARS **acceptance criteria** (report 25) — five-pattern grammar.
- Nystrom's **Markdown-spec-in-repo** (report 35) — AFIS strategy-3.
- Brier's **pace-layer-3 spec** (followup 12) — slow mid-layer.
- The **delta-spec** (brownfield change-intent per `brownfield-methodology-first` §1.1 stage 3).
- The El Kaim `ArchitectureSpecification` typed object (report 14) — distinct from the intent block.

CTR-B3, CTR-B6, CTR-B7 collectively establish that these are not the same artifact (spec velocity, spec primacy, intent vs. spec).

**Tracks exhibiting the collapse.** [`unified-B` §1](../../tracks/unified-B.md) flattens to "L2 Spec" with El Kaim shape one direction and delta-spec the other. Greenfield tracks generally hold the intent-block-vs-spec distinction (CTR-B6); brownfield tracks collapse it back. Most D-1 acceptance markings are uniform across artifact-shapes the corpus distinguishes.

**Consequence if preserved.** D-1 is currently being accepted in a form that hides which spec shape the architecture is committing to. Phase-5 ADRs need to pick.

**Recommendation: SPLIT.** Phase-3 should treat D-1 not as one default but as a *per-spec-shape* commitment, mapped to a corpus shape. Lower-priority than clusters 1–5 because the corpus has already done much of this work (CTR-B3/B6/B7); the tracks just need to honor it.

### Cluster 9. "Cross-layer drift" / "behavioural drift" / "design-authority erosion" / "goal subversion" — four F-modes lumped as "drift"

**Surface concept.** Tracks invoke "Patrol watches for drift" without distinguishing which drift.

**Corpus distinctions being collapsed.** Failure-modes-v3 explicitly catalogs four distinct mechanisms with separate F-numbers:

- **F34** cross-layer drift (Brier pace-layer mechanism).
- **F54** goal subversion (RSI prompt-injection across cycles).
- **F55** behavioural drift / self-reference loop (self-referential without external anchor).
- **F57** design-authority erosion (convenience reclassifies stakes).

The catalog (F55 entry) is explicit that F55 is "*distinct from F8* … *distinct from F27*"; the corpus has done the splitting work.

**Tracks exhibiting the collapse.** Multiple tracks lump these into "Patrol detects drift" without specifying which drift-detector each F-mode requires. [`greenfield-substrate-first` §1.S5](../../tracks/greenfield-substrate-first.md) is the most lumping (Patrol catches F55, F57, F8 in one sentence). [`brownfield-methodology-first` §2.5](../../tracks/brownfield-methodology-first.md) and [`unified-B` §2.5](../../tracks/unified-B.md) merge.

**Consequence if preserved.** Each F-mode requires a different detector: F34 needs pace-layer invariant comparison; F54 needs cross-cycle goal-frame comparison; F55 needs self-reference / external-anchor distance; F57 needs classifier-output distribution monitoring. Lumping into "Patrol" leaves the detector unspecified.

**Recommendation: SPLIT.** Lower priority. Phase-3 should require Patrol-mitigation claims to name which F-mode and which detector; the corpus already supplies the split, the tracks just need to use it.

### Cluster 10. "Substrate-default-off" / "production-scissors-off" / "lethal-trifecta closure" / "CaMeL boundary" — distinct mitigations conflated

**Surface concept.** Tracks refer to "substrate-default-off" or "production-scissors-off" as one mitigation covering the F12/F33/F44 cascade.

**Corpus distinctions being collapsed.** Failure-modes-v3 explicitly cascades F12 → F33 → F44 as *three distinct layers* of mitigation:
- F12 mitigation = perimeter typing (CaMeL-class typed-interpreter boundary).
- F33 mitigation = judge architecture (cross-model / deterministic perimeter).
- F44 mitigation = substrate default-off.
- F56 (Replit-class) adds *stress-bypass* as a fourth mechanism not covered by the F12/F33/F44 cascade.

The cascade comment is explicit: "mitigations stack; perimeter typing → judge architecture → substrate default-off."

**Tracks exhibiting the collapse.** Most tracks invoke F12/F33/F44 together citing "substrate-default-off" or "trifecta closure" as if one mitigation. [`brownfield-substrate-first` §1.1 S-5](../../tracks/brownfield-substrate-first.md) is best (it names CaMeL boundary + production-scissors-off + cross-model judge as distinct primitives). [`unified-A` §1](../../tracks/unified-A.md) lumps to "sandbox and approval-gate policies." `unified-C` §2.8 lumps to "anchor's `mutation-protocol` field forces production-scissors prohibition."

**Consequence if preserved.** The four mitigations have different costs (CaMeL ~7-point utility tax per CTR-E6; cross-model ~2× inference; substrate-default ~zero; stress-bypass detection requires watchdog Triage tier). They cannot be traded off without being distinguished.

**Recommendation: SPLIT.** Phase-3 should keep the F12/F33/F44/F56 four-layer cascade explicit in any trifecta treatment. Medium-priority — the corpus already split this work and the failure-modes catalog is unambiguous.

## §3 Convergences that are genuinely sound

A few cases where multiple tracks converge and the corpus *does* support treating the merged concept as one thing:

1. **Trajectory capture (D-7) as a single substrate primitive.** All 9 tracks accept D-7 with similar framing (sub-ms persist, content-addressed events, OpenHands measurement context cited as evidence-not-dependency). The corpus does not distinguish "trajectory" varieties; report 11 §6 supports treating it as one primitive. Keep merged.

2. **Tiered watchdog (D-6) Daemon / Triage / Patrol as a three-tier abstraction.** The corpus (Round-2 C14, brief glossary §0) explicitly defines the three tiers; the convergence on the three-tier abstraction reproduces a corpus-sanctioned distinction at the right granularity. The lump within Patrol (cluster 9 above) is a separate issue.

3. **"Lights-out ≠ L5" vocabulary resolution (CTR-A4).** All 9 tracks reach the same answer (lights-out is not identical to L5, mapping via glossary §0). This is corpus-faithful: CTR-A4 names the test, the brief's glossary supplies the mapping, and tracks correctly invoke the WEAK-4 sharpening (Round-2 ceiling is L5-anti, not L3-only). The convergence is decisive and load-bearing — preserving the merger is correct. **This is the single most important convergence that should stand.**

4. **Hard cost ceilings as non-optional (D-5).** The 10× variance in CTR-E1 is uniformly treated as configuration of a single primitive, not a substrate-level disagreement. Corpus-faithful.

5. **The brief's option (c)+(b) as a regime *family*.** The framing itself is a corpus-sanctioned superset; tracks correctly identify it as the right shape. (Cluster 3 above flagged the surface-choice collapse *within* (c)+(b), not the family-level convergence itself.)

6. **Compound Engineering / Compound Knowledge as one methodology family.** Tracks that invoke Compound treat its loop and knowledge-store discipline as a coherent shape; followup/11 and report 03 do support this. Phase-1 bias-guard CHALLENGE-6 / CHALLENGE-7 retagged both as brownfield-primary; the merger is corpus-grounded.

## §4 Recommendations to Phase 3

In priority order:

1. **Split the judge-shape lump (cluster 1).** Phase-3 must not let "cross-model judge" continue as a single architectural commitment. The CTR-D4 / D7 / D8 three-way contradiction is currently being silently resolved on the F46 side. Most load-bearing split.

2. **Split the holdout-enforcement lump (cluster 2).** D-4 is being marked accepted in four different operational forms; Phase-5 ADRs depend on which form. Second most load-bearing split.

3. **Split the lights-out-surface lump (cluster 3).** The convergence on option (c)+(b) is sound; the convergence on *which surface* is illusory. Force surface-declaration.

4. **Split the day-0 lump (cluster 4).** CTR-G3 is the corpus' explicit warning against treating cold-start and legacy-ingestion as symmetric; the brief §5 mandate is greenfield-only. Brownfield tracks claiming "the analog" must defend the symmetry or scope their claim narrower.

5. **Split the "scenarios" label (cluster 5).** The four-way taxonomy (Kaner / EARS / regression / telemetry) is corpus-canonical; the lump in tracks is corpus-distorting.

6. **Split "the codebase" into the five-way input enumeration (cluster 6).** Brief §0 already gives the split; require tracks to honor it.

7. **Split re-entry varieties (cluster 7), spec shapes (cluster 8), drift types (cluster 9), and trifecta-cascade layers (cluster 10).** Medium priority; corpus has already done much of the work.

8. **Keep merged:** trajectory capture (D-7); watchdog tier abstraction (D-6); lights-out ≠ L5 vocabulary; cost ceilings as non-optional (D-5); the (c)+(b) family; the Compound Engineering / Knowledge family. These are corpus-faithful lumps; resist a splitter overshoot.

A meta-recommendation: the dominant cluster type (1, 2, 5, 6, 8, 10) is "substrate-enforced X" where X is a discipline with multiple operational forms. Phase-4 substrate/methodology extraction should treat every "substrate enforces Y" claim as a *family* of primitives parameterized by Y-shape, not a single primitive. The lumper bias in this Phase-2 set is mostly a substrate-layer optimism.

## §5 Limits

- I did not deep-read corpus reports beyond what the tracks cite; corpus distinctions present in reports but not surfaced in any track's citations may exist and are not in my catalog.
- I did not pressure-test against the other Phase-2 bias-guards' outputs (anchor-detector, splitter, axis-divergence-auditor) — they may surface complementary or contradicting findings.
- The "load-bearingness" ranking is judgment; Phase-3 may weight differently. Clusters 9 and 10 in particular are arguably more load-bearing than I have rated them.
- I did not audit the F-mode tables in §2.5/§2.9 of every track for cluster-9-style drift-lumping at scale; the cited examples are illustrative, not exhaustive.
- Cluster 4 (day-0 phenomena) overlaps with my own Phase-1 bias-guard intuition that CTR-G3 is under-resourced in the corpus; if CTR-G3 is itself wrong, the split here loses force.
- I have not assessed whether *all* tracks would suffer if the splits were forced; in particular `unified-A`'s `EscrowInterval` schema is partly designed to absorb cluster-1 and cluster-7 splits inside one substrate primitive. Phase-3 must judge whether absorption-into-typed-parameter counts as "preserving the distinction" or as a sophisticated form of lumping.

*End of lumper.md.*
