---
guard: newcomer
target: draft-greenfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 naive newcomer critique — greenfield draft

## §1 Persona stance

I walked into this repo today. My first-pass experience was this: roughly the first half of §1 reads like a checklist written by people who can finish each other's sentences, and the second half (DECISIONS-PENDING) is where I finally start to understand what's being argued about — because divergence forces the authors to *name* the alternatives. By the time I reached §2, I had a working model of what the document is doing, but I had to read past at least eight terms whose meaning I could only guess from context. The §0 brief glossary recovers most of them, but the draft never tells me to go read it.

## §2 Top confusing / jargon-heavy passages

**(1) ROBUST-G1.** *"All three tracks adopt some variant of brief §2.1 option (c)+(b)."* I do not know what option (a), (b), (c), (d), or (e) is until I open the brief §2.1. **Help:** inline footnote enumerating the five options.

**(2) "Splitter Cluster-N" / "Lumper Cluster-N" used as load-bearing references.** I do not know what "Splitter Cluster-3" *is*. Is it a group of findings? A taxonomy entry? A specific bias-guard subagent's output? **Help:** preamble at top of §1: "Splitter / Lumper Cluster-N references point to the corresponding entry in `bias-guards/phase-2/{splitter,lumper}.md`."

**(3) ROBUST-G6.** *"Deterministic GtWR/EARS lint... Not LLM-judge — explicit refusal of F51 (Ashby-deficient probabilistic guard)."* GtWR (Guide to Writing Requirements?). EARS (Easy Approach to Requirements Syntax?). "Substrate-typed." "Ashby-deficient" — Ross Ashby's law of requisite variety, I assume. **Help:** spell out acronyms; gloss Ashby in one clause.

**(4) `EscrowSurface`, "STIR cascade," "delegation-level."** I have no idea what a "STIR cascade" is. "Cognitive escrow" is mentioned but the draft never tells me *what cognitive escrow is*. This is the exact spot the dispatcher flagged. **Help:** 2-3 sentence inline gloss of cognitive escrow as a phenomenon.

**(5) "F-mode" citations as substance-replacements.** *"F22 (zombie agents) / F23 (stalled-vs-thinking) at Daemon+Triage tiers; F8/F34/F55/F57 at Patrol tier."* F22 gets a 2-word gloss; F8/F34/F55/F57 get nothing. **Help:** when an F-mode determines what a primitive must do, give it the 4–6 word phenomenon gloss.

**(6) ROBUST-G9.** "Production-scissors," "CaMeL-class," "~7-point utility tax," "four-layer cascade." None expanded. **Help:** expand CaMeL at first use; state the utility-tax units; list the four cascade layers.

**(7) ROBUST-G7.** *"Yang et al. 10–20 simultaneous-requirement ceiling, gpt-4o 98.7% → 85.0%."* 98.7% → 85.0% of *what*? **Help:** "instruction-following accuracy on multi-requirement prompts."

**(8) DPG-7 itself.** I cannot evaluate (a) vs. (b) because I do not know (i) what cognitive escrow is, (ii) what a "substrate-typed primitive" buys over a "methodology convention," (iii) what makes Kahana's interval load-bearing. **Help:** 3-sentence preamble to DPG-7 stating phenomenon, multi-anchor corpus, and architectural commitment.

## §3 Hidden anchors and smuggled context

**(a) ROBUST-G1 smuggles "L3-Augmentation = day-0" as if it were a definition.** L3 is Shapiro's level; Augmentation Mode is Jaymin's mode. Are they synonymous? Neither says so. **Re-phrase:** *"Greenfield's day-0 regime is L3 (Shapiro's level) operating in Augmentation Mode (Jaymin's mode); the two vocabularies happen to align at day 0."*

**(b) ROBUST-G3 invokes "lights-out ≠ L5" as a precondition without explaining why it matters.** **Re-phrase:** name the consequence — *"If lights-out and L5 were identical, the L5-as-anti-pattern claim would refute the whole UC1 mandate. The mapping refusal is what makes the mandate coherent."*

**(c) ROBUST-G14 promotes Kahana to substrate primitive while flagging it as a problem — D5 violation.** The phrasing *"Substrate-triggered cognitive-escrow surface ... `EscrowSurface`, Splitter Cluster-7 ... substrate-fired"* commits the architecture to a substrate-primitive shape before DPG-7 has been adjudicated. **Re-phrase:** move the entire `EscrowSurface` framing into DPG-7. State the *phenomenon* without naming the primitive.

**(d) ROBUST-G19 smuggles RSI-declaration as if every greenfield factory will meet Kahana's three-part test.** **Re-phrase:** spell out the three-part test in one sentence; state the lead-agent assessment of whether *this* factory meets it.

**(e) ROBUST-G12 quietly leans on OpenHands as feasibility evidence.** **Re-phrase:** one phrase noting the generalization caveat.

**(f) "Co-extensive with AILCCP immutable logging" — AILCCP appears unexplained.** Expand at first use.

## §4 What the draft does well

The DECISIONS-PENDING section is the strongest part of the document. Each DPG entry names the divergence with concrete track positions, asks a *clean* user question, and supplies a concrete-next-action per ADR-0005. A newcomer can read DPG-2 and *fully understand the choice* without leaving the document — because the divergence forces the authors to spell out the alternatives in English. The contrast between §1 (terse, anchor-dense) and §2 (legible, alternative-aware, self-contained) is large enough that a Phase-3.4 reader might genuinely understand the open questions while remaining confused about the supposedly-settled claims. The §1.5 defaults-marking table is exemplary: it states the stance, the justification, and the surrounding context in one row.

## §5 Concrete recommendations for Phase-3.4

**Rephrase in place:**
- ROBUST-G1: inline one-sentence enumeration of brief §2.1's options (a)–(e).
- ROBUST-G3: name the consequence of the mapping refusal.
- ROBUST-G6: expand GtWR, EARS, "Ashby-deficient" at first use.
- ROBUST-G9: expand CaMeL; state utility-tax units; name the four cascade layers.
- ROBUST-G14: re-state phenomenon without `EscrowSurface` framing; move primitive-naming to DPG-7.
- ROBUST-G19: spell out Kahana's three-part RSI test; spell out AILCCP.
- For every F-mode named in a load-bearing position, supply a 4–6 word phenomenon gloss inline.

**Add a "see X" pointer header at the top of §1:**
*"This draft presumes the brief §0 glossary. Splitter / Lumper Cluster-N references point to `bias-guards/phase-2/{splitter,lumper}.md`. CTR-N references point to `contradictions.md`. F-N references point to `failure-modes-v3.md`."*

**Inline gloss for terms that are load-bearing in §1:** "cognitive escrow," "STIR cascade," "production-scissors."

**Restructure DPG-7 specifically:** rebuild in three steps: (1) state the phenomenon in plain English; (2) state what the corpus multi-anchors (Schillace / Anthropic / Notion variants); (3) state what substrate-primitive-promotion commits to. Then (a)/(b) becomes evaluable.

**Apply D5 self-check to ROBUST-G14, ROBUST-G9, ROBUST-G11.** Each names a primitive and integrates a splitter/lumper finding *in a way that commits to the primitive's architectural shape*. D5's neutralization self-check applies.

The single biggest gain is the §1 pointer header. The next biggest is the cognitive-escrow gloss at DPG-7.
