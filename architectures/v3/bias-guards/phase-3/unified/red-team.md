---
guard: red-team
target: draft-unified-synthesis
phase: 3.2
based-on-commit: 200ad3e
based-on-date: 2026-05-25
---

# Phase-3.2 red-team critique — unified draft

## §1 Persona stance

The unified draft is selling a falsified-UC4 story whose central claim — ROBUST-U1, "mandate is a parameter" — rests on convergence among three Phase-2 tracks that were all reading from the same brief-mandated cold-start reading list. The draft itself names the cause (anchor-detector F-ANCHOR-2 / F-ANCHOR-3) but stops short of the obvious conclusion: the 95% convergence is a downstream artifact of brief §5.1, which forced reports 25 / 26 / 30 / 31 / followup-10 onto every cold-start-touching track. Three subagents reading the same five required-reading papers and then "independently converging" on a (typed-object + policy + parameterised-mandate) shape is not a falsification of UC4 — it is a moderately well-mixed echo.

## §2 Top attack findings

### Attack 1 — ROBUST-U1 ("mandate as parameter") is a re-encoding of the convergence, not an independent finding. Severity: HIGH.

The 95% number measures *agreement among the three tracks* on the surface predicate "mandate-as-parameter," but the three tracks reach that predicate by structurally different routes: U-A makes mandate a `priors.in-tree` content difference; U-B makes it a *traversal-direction* difference over five Brier layers; U-C makes it an *anchor `kind`-content* difference. Agreement on "the difference is a parameter" is trivial once the brief invited unification (D1) — *any* substrate primitive admits a content-slot for "what's different per mandate."

**Corpus counter-example.** Report 01 (StrongDM "Tokens are the fuel") and report 35 (Nystrom/Notion specs-as-changelog) describe primitives that are not parameterisable across mandates. StrongDM's NLSpec scenario discipline assumes scenarios live out-of-tree; Nystrom's spec-git-history-as-changelog is a brownfield-impossible primitive (no checkable history at day 0). CTR-G4 is direct: StrongDM treats code as opaque ML weights, UC4 brownfield treats code as readable archaeology. These are *substrate-shape* differences. ROBUST-U1 only holds for the subset of primitives the three tracks happened to enumerate (gates, judges, logs, holdouts). The primitives where mandate matters most — codebase-model views (U-A treats `priors.in-tree: []` as vacuous greenfield slot; brownfield-legacy-ingestion-first builds six explicit views) — are exactly where "mandate as parameter" stops working.

**Phase-3.4 action.** Demote ROBUST-U1 to *robust within the substrate envelope the three tracks share, not robust across the substrate envelope mandate-difference actually occupies.*

### Attack 2 — ROBUST-U2 "typed-object substrate primitive" lumps three structurally different primitives. Severity: HIGH.

The three tracks' typed objects have *incompatible* topologies: U-A `EscrowInterval` is *many per cycle*; U-B Layer is *5 per architecture*; U-C Anchor is *one or a few per architecture lifetime*. Calling these "instantiations of one primitive" via splitter Cluster-3 collapses a 1000:1 cardinality difference into surface vocabulary.

**Corpus counter-example.** Report 30 §1 (Kahana) defines the escrow *interval* as a *phenomenological* unit. Followup 12 §4 (Brier) defines pace-layers as five *artifact* strata changing at five different time-scales. Report 14 §4.1 (El Kaim) defines intent-block invariants as project-lifetime stable upstreams. These three primitives serve incompatible jobs: escrow intervals govern *attention transfers*; pace-layers govern *artifact-change rates*; anchors govern *commitment-stability*. The corpus does not say they are the same primitive.

**Phase-3.4 action.** Split ROBUST-U2 into ROBUST-U2a "all three carry a *substrate-resident typed object*" (true and trivial) and DPU-1-PRIMARY "the typed object is incommensurate across tracks; the merged architecture cannot import all three under a single primitive name without losing what the original primitives were *for*."

### Attack 3 — ROBUST-U10 EscrowSurface is single-source promoted; corpus has phenomenology convergence but not substrate-primitive convergence. Severity: HIGH.

Report 30 §3-§4 is the *only* corpus source naming the interval as a designable substrate site. Schillace's Attention Firewall and Anthropic Auto-Review — which the draft cites as corroboration — are *attention-management* tools that fire post-response, not interval-design tools that fire *inside* the prompt-to-response gap. Kahana himself is explicit at report 30 §3: the corpus' adjacent disciplines all "bracket the interval rather than entering it." The phenomenon is multi-anchored — Willison, Cherny, Vaughan/Challenger, Veracode all describe it differently. The *substrate-primitive promotion* is single-source Kahana.

**Phase-3.4 action.** Demote ROBUST-U10 to ROBUST-U10' "the *phenomenon* of cognitive-escrow burden is corpus-multi-anchored; the substrate-primitive promotion is currently single-source Kahana and *contingent on* D7-U-1's outcome."

### Attack 4 — ROBUST-U12 / U13 / U14 bootstrap claims are greenfield-flavoured smuggled into the unified shape. Severity: MEDIUM-HIGH.

Every primitive ROBUST-U13 names is *greenfield-shaped*: the El Kaim 9-field intent block presumes there is no system yet; the `EvaluationSuite` with `protects: RULE-ID` linkage presumes scenarios are out-of-tree. CTR-G3 is the smoking gun: cold-start was promoted to mandatory in brief §5 per Historian M4; legacy-ingestion was left at OQ-B4 framing. ROBUST-U12 inherits this asymmetry — the unified-track bootstrap section is *the greenfield bootstrap with brownfield as an afterthought* (U-A §5.2: "brownfield bootstrap has tests + traces + codebase, greenfield does not. *Everything else is shared.*" — a single sentence).

**Phase-3.4 action.** Split ROBUST-U13 into U13-G (greenfield bootstrap output set — corpus-supported) and U13-B (brownfield ingestion-output set — currently *not enumerated in the unified draft*).

### Attack 5 — DPU-1 framing ("pick one typed object") concedes the falsification before it occurs. Severity: MEDIUM.

The three primitives are not competitors; they are *non-overlapping observations* about what substrate must mediate. Picking U-A's interval forecloses U-B's artifact-stack invariants and U-C's commitment-stability machinery; the draft does not say where those go.

**Phase-3.4 action.** Replace DPU-1's pick-one framing with a structural question: "is the substrate single-primitive (with interval / layer / anchor being views) or multi-primitive (with three coexisting primitives serving three jobs)?"

## §3 What survives the attack

The genuine convergences hold: cross-model judging at high-stakes (G-CONV-1); D-4 holdout discipline as substrate (G-CONV-2); D-2 challenged for brownfield (G-CONV-3); D-7 trajectory capture (G-CONV-4); F36/F37 Yang/Larbi underspecification (G-CONV-5). These are real and the draft is right to mark them robust.

The unified architecture also survives in a weaker form: there is *a* unified envelope (cross-model judging + holdout + trajectory + sandbox + cost ceilings + watchdog) inside which mandate is genuinely a parameter. ROBUST-U4 through ROBUST-U9 and ROBUST-U11 are mostly defensible at the primitive level. What does *not* survive is the headline claim that this envelope is the architecture rather than the substrate.

## §4 Recommended edits for Phase-3.4 integration

1. **Reframe ROBUST-U1.** Replace with: "Within the substrate envelope the three tracks share (judges, logs, sandboxes, holdouts, cost ceilings, watchdog tiers), mandate-difference reduces to policy-slot content. *Outside* that envelope — codebase models, intent invariants, in-tree-priors schemas — mandate-difference is primitive-shape difference, currently un-enumerated in the unified draft." Cite CTR-G1 / CTR-G3 / CTR-G4 explicitly.

2. **Demote ROBUST-U10 to "contingent on D7-U-1."** Add: "If D7-U-1 produces a defensible non-escrow unified axis, the substrate-primitive promotion is rescinded and EscrowSurface drops to methodology."

3. **Split ROBUST-U13 into U13-G and U13-B and admit U13-B is currently unwritten.** Before ROBUST-U13 can claim unified status, the brownfield legacy-ingestion primitive set must be added.

4. **Restate DPU-1 as a structural question.** "Is the substrate single-primitive with three views, or multi-primitive with three coexisting primitives?"

5. **Add a §1.6 explicit-asymmetry note.** Document that the unified draft's primitive enumeration is greenfield-asymmetric per F-ANCHOR-2.

6. **Tighten citation discipline on Kahana primitives.** Per F-ANCHOR-2 Phase-3 recommendation, require every Kahana-derived substrate-primitive claim to cite at least one non-Kahana primary corpus source for the *substrate-primitive promotion* specifically.
