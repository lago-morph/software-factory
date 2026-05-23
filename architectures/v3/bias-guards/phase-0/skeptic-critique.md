# Skeptic / Contrarian Methodologist — Critique of v3 Brief

**Target:** [`00-brief-v3.md`](../../00-brief-v3.md)
**Persona:** Skeptic / Contrarian Methodologist
**Central question:** *"What assumptions is this brief making that it doesn't acknowledge?"*

The brief is coherent. That is the first thing to be suspicious about. A brief built from twelve rounds of research and two prior syntheses, then "rebuilt from scratch," is almost guaranteed to inherit the framings that made the prior work *feel* like it converged. The findings below are ordered most-severe-first. Severity ≈ how much downstream synthesis would be misled if the assumption is wrong.

---

## 1. "Two mandates" is itself the smuggled assumption

**Quote (§1):** *"Two mandates, treated as potentially distinct solutions: Greenfield mandate. … Brownfield mandate. …"*

**Buried assumption.** That **greenfield vs. brownfield is the primary axis** along which factory architectures vary. The constraint document only says the user wants both to be addressed and that they "may produce different architectures." That is not the same as electing greenfield/brownfield as the *organizing decomposition* of the whole synthesis.

**Why it matters.** A factory designed for *low-stakes throwaway tooling* vs. *regulated production code* may differ more than greenfield vs. brownfield. Same for *synchronous* (operator-driven) vs. *asynchronous* (queue-driven) factories, or *one-shot delivery* vs. *continuous evolution*. By making mandate the top-level axis, six Phase-2 tracks, twelve adversarial passes, and the final mandate-fit matrix all get organized around an axis that may not be the load-bearing one. The corpus's regime-classification material (Jaymin L0–L5, Augmentation vs. Automation thresholds) suggests *regime* is at least as foundational an axis as *mandate*.

**Remediation.** Add an explicit §1.x "Why mandate, not some other axis?" — list the candidate axes (mandate, regime, stakes, synchronicity, codebase-lifecycle stage), state the lead-agent reason for choosing mandate as primary, and add an open question (OQ-B7) authorizing Phase-2 tracks to surface a better axis if the corpus supports one. At minimum, instruct one of the six Phase-2 tracks to *not* organize itself by mandate, as a control.

---

## 2. "Lights-out" is treated as binary when the brief's own evidence says it is a spectrum

**Quote (§2):** *"The factory operates **lights-out** — autonomously over extended time horizons, with the human's role moved upstream … and downstream …, but **not in the per-cycle inner loop**."*

**Buried assumption.** That "lights-out" names a single, coherent operating mode. §2.1 then introduces Jaymin's L0–L5 ladder and Augmentation/Automation thresholds as *modifiers* of lights-out, but the brief still talks about *the* lights-out mandate (singular). OQ-B3 acknowledges the binary may be wrong but doesn't change the framing.

**Why it matters.** If lights-out is actually a spectrum (per-task autonomy level, per-decision autonomy level, time-budget autonomy, blast-radius autonomy), then "the factory operates lights-out" is a category error — different work units inside one factory will run at different autonomy levels. Architectures designed *to be lights-out* will systematically over-automate easy decisions and under-automate hard ones. The §2.1 (c) option ("regime-classification scheme") is essentially a tacit admission of this — but it is offered as a *resolution shape* rather than as a critique of the framing itself.

**Remediation.** Rewrite §2 to define lights-out as *"no human in the per-cycle inner loop for work units the factory has classified as automation-eligible"* and make work-unit classification a first-class architectural concern, not a footnote. Or, alternatively, demote "lights-out" from a mandate to a *target regime* and require each architecture to declare which work-unit classes it operates lights-out on.

---

## 3. The substrate-vs-methodology distinction is inherited from Round 2 without re-litigation

**Quote (§1):** *"They may also share a common **substrate** (sandbox, scenario storage, cost ceilings, watchdog, trajectory capture, etc.)."*
**Quote (§4):** lists items as either substrate primitives or methodology choices.
**Quote (§3):** *"A substrate-heavy + thin-methodology design could plausibly work for both with different overlays (Round-2's 'substrate is shared; methodology differs' framing leaves room for this)."*

**Buried assumption.** That **"substrate" and "methodology" are real, distinguishable layers** with a defensible boundary between them. This distinction comes directly from Round 2's §3.2 reframing ("substrate supports both; the methodology chooses"). The brief explicitly cites Round 2 as the source of the framing — but it inherits it as an organizing principle, not as a claim to be tested.

**Why it matters.** Phase 4 ("shared-substrate extraction") *presumes* the substrate/methodology axis is the right boundary. If the actual divergence between greenfield and brownfield runs *through* what Round 2 called substrate (e.g., scenario storage works fundamentally differently when scenarios come from production traces vs. cold-start), then Phase 4's output will be a category-confused diff. Worse, the falsifiability of §3's hypothesis depends on this distinction: "substrate-heavy + thin-methodology design works for both" is unfalsifiable if the substrate/methodology line itself is movable.

**Remediation.** Add an explicit §4.x: "The substrate/methodology distinction is itself a hypothesis. Phase 4 must first justify the boundary before reporting what falls on each side." Make 'boundary stability' a checkpoint criterion. Alternatively, allow Phase 2 tracks to organize around primitives that ignore the distinction.

---

## 4. §4 "What's invariant" is a list of un-tested defaults, not invariants

**Quote (§4):** seven bulleted items (specs durable, scenarios outside codebase, Agent = Model + Harness, holdout discipline, cost ceilings, tiered watchdog, trajectory capture) — each cited to a prior synthesis.

**Buried assumption.** That **"well-supported across the corpus"** = **invariant for v3**. The lead-agent note at the bottom waves at this ("free to challenge") but the practical effect is that these seven items are *removed from Phase-2 deliberation*. Six tracks will all assume these items.

**Why it matters.** Two of these items are particularly fragile:
- *"Scenarios live outside the codebase as a holdout set."* For brownfield, the corpus suggests scenarios may be inseparable from the codebase (production traces, existing test suites, runtime telemetry). Treating this as invariant *biases the brownfield synthesis toward greenfield-shaped assumptions*.
- *"Agent = Model + Harness."* This is a 2026-vintage vocabulary convention, not a structural truth. Architectures that treat agents as graph nodes, populations, or processes do not decompose cleanly into "model + harness."
- *"Trajectory capture is cheap and production-tested."* The OpenHands data is one substrate's measurement on one benchmark. Generalizing it as "cheap" across all architectures is an empirical claim, not an invariant.

**Remediation.** Rename §4 from "What's invariant" to "Round-1/Round-2 defaults carried forward" and require every Phase-2 track to mark at least one of these as "challenged" or "accepted with justification." The current framing makes challenge socially costly.

---

## 5. The falsifiability test for §3's hypothesis is structurally incapable of falsifying it

**Quote (§3):** *"The v3 synthesis treats this as a **falsifiable hypothesis**. … The plan must be able to *find* a both-mandates architecture if it exists, not rule it out structurally. The hypothesis is tested in Phase 3 by a dedicated cross-mandate adversarial pass."*

**Buried assumption.** That a Phase-3 "cross-mandate adversarial pass" (4 subagents per the plan: G→B advocate/attacker, B→G advocate/attacker) constitutes a falsification test. It does not. By Phase 3, the inputs are *two mandate-specific syntheses* already drafted independently in Phase 2. Asking "could G work for B too?" *after* G has been authored to be G-shaped will systematically under-find both-mandates architectures.

**Why it matters.** A genuine falsification test would require a Phase-2 track explicitly tasked with producing a **both-mandates architecture from scratch**, parallel to the mandate-specific tracks, scored on the same axes. The current 6-track design (3 greenfield framings + 3 brownfield framings) *structurally cannot produce* a both-mandates output, because no track is allowed to ignore the mandate split. The adversarial pass then operates on outputs that were not built to be cross-mandate, and finds — predictably — that they aren't.

**Remediation.** Either (a) add a 7th Phase-2 track: "no mandate split; produce one architecture that addresses both," scored against the others, or (b) restate §3 honestly: "the hypothesis is *not* being treated as falsifiable; the synthesis will produce mandate-specific architectures and *consider* whether any of them generalize."

---

## 6. The brief inherits the "no pre-existing codebase / scenarios / issue queue" framing from research-plan.md without examining it

**Quote (§1):** *"Greenfield mandate. The factory produces a new software system from a problem statement / spec, with no pre-existing codebase, no pre-existing scenarios, no pre-existing issue queue."*

**Buried assumption.** That **"greenfield = absence of priors"** is the right definition. The phrasing is verbatim-similar to [`research-plan.md`](../../../research-plan.md) §"One specific risk for the greenfield mandate." But real greenfield factories operate against: a problem-domain corpus, the user's prior projects, exemplar codebases, library ecosystems, frameworks, and the operator's accumulated `docs/solutions/` from *other* factory runs. "No priors" is an extreme on a spectrum, not a definition.

**Why it matters.** Defining greenfield as zero-priors makes the cold-start problem look harder than it is and biases the synthesis toward bootstrapping-heavy architectures (à la Foundry's phase scaffolding) over priors-leveraging architectures (à la Atelier with cross-project `docs/solutions/`). It also makes the greenfield/brownfield boundary look sharper than it is — most real greenfield work has *some* priors, most real brownfield work has *some* greenfield-shaped components.

**Remediation.** Re-define greenfield as *"the target system has no pre-existing implementation; priors from adjacent domains, exemplar projects, and operator-curated knowledge are permitted and expected."* Then explicitly raise the spectrum question (is the boundary mandate-by-codebase or work-unit-by-work-unit?) as an open question.

---

## 7. "Mandate-fit" as a tag presupposes mandate-fit is a property of architectures, not of work units

**Quote (§6, item 7):** *"Architecture specs (count emergent, not predetermined), each carrying a `mandate-fit` YAML header."*
**Quote (§6, item 8):** *"a comparison document with a first-class **mandate-fit matrix**…"*

**Buried assumption.** That an architecture has a single mandate-fit value. Real factories execute many work units; some units inside a "greenfield" project are greenfield-shaped (initial spec authoring), others are brownfield-shaped (refactoring once the codebase exists, adding features after MVP). A unitary `mandate-fit: greenfield` tag conflates these.

**Why it matters.** The mandate-fit matrix becomes the "single most user-facing artifact" (§6). If its unit of analysis is wrong, the artifact misleads. An architecture that runs at L4 lights-out for brownfield-shaped work and at L3 augmented for greenfield-shaped work would have to choose a tag, and would lose its actual character in the choice.

**Remediation.** Make `mandate-fit` per-work-unit-class rather than per-architecture, or at minimum allow tags like `greenfield-bootstrap + brownfield-evolution` and require the matrix to be cell-level over (architecture × work-unit-class) rather than (architecture × mandate).

---

## 8. The OQ-B3 framing is "no human ever vs. no human in inner loop" — but those are not the two options

**Quote (§8, OQ-B3):** *"Does 'lights-out' mean *no human ever*, or *no human in the per-cycle inner loop*? The brief currently uses the latter framing (§2)."*

**Buried assumption.** That the dichotomy is "no human ever" vs. "no human in inner loop." Real options include: *no human in inner loop for routine units, human-in-loop for exceptional units*; *no human in inner loop but humans set policy that the loop self-applies*; *humans sample-audit a fraction of inner loops post-hoc*; *humans intervene only on watchdog escalation*. By framing OQ-B3 as a binary, the brief preempts the more interesting answers.

**Why it matters.** The interesting architectural lever is *what triggers human re-entry*. The current OQ-B3 framing prevents the answer "lights-out with conditional re-entry triggers" from being a first-class option.

**Remediation.** Re-state OQ-B3 as: "What is the *re-entry mechanism* — what conditions cause a human to enter the inner loop, who decides, and what is the substrate-level protocol for handing back?"

---

## 9. "Working hypothesis to test" is rhetorically falsifiable but operationally pre-committed

**Quote (§3):** the user's hypothesis is reproduced verbatim, framed as falsifiable. **Quote (§7, item 1):** *"Accuracy ≫ speed ≫ tokens … Default to more bias guards, more personas, more checkpoints."*

**Buried assumption.** That the synthesis is genuinely neutral on the hypothesis. But the *entire phase plan* (6 tracks split 3-3 by mandate, mandate-fit matrix as headline output, mandate-specific syntheses, mandate-specific ADRs) operationalizes the hypothesis. The synthesis cannot conclude "actually, there is one architecture that works for both" without invalidating the structure that produced it.

**Why it matters.** If the corpus would support a unified architecture, the plan is structured to discover mandate-specific architectures anyway. The "falsifiability" is rhetorical: at the level of artifacts produced, the answer is already shaped.

**Remediation.** Either reduce the structural commitment to the mandate split (collapse to fewer mandate-specific phases, run a unified track in parallel) or drop the "falsifiable hypothesis" framing and admit the synthesis is built on the hypothesis as a working premise.

---

## 10. Citation completeness: the lights-out *empirical bars* claim is load-bearing but the citation chain is one-deep

**Quote (§2.1):** *"Jaymin's Augmentation-vs-Automation threshold matrix … ≥90% K=5 consistency, 5-of-5 prompt-paraphrase robustness, zero medium-or-high safety incidents. These are empirical bars the lights-out mandate must clear, not aspirations."*

**Buried assumption.** That Jaymin's threshold matrix is a *standard* the v3 architectures must meet. Jaymin is one author. The thresholds (90%, 5-of-5, zero medium-or-high) are not user-authored constraints — they are imported from a single source and elevated to gating criteria. The user's actual constraint (C1) says only "lights-out." Nothing in `constraints-extracted.md` mandates Jaymin's thresholds.

**Why it matters.** The brief uses these thresholds as a forcing function on the synthesis ("must either clear the bars, redefine the mode, or regime-classify"). If the thresholds are not user-authored constraints, the forcing function is lead-agent-imposed and should be flagged as such. Other authors in the corpus may have different (looser, stricter, differently shaped) thresholds.

**Remediation.** Flag the Jaymin thresholds as a *corpus-derived recommendation, not a user constraint*. Add an open question: "Which empirical bars should the lights-out architectures be required to clear, and from which source(s)?"

---

## 11. Out-of-scope item: "Choosing a specific LLM provider" hides a load-bearing decision

**Quote (§5):** *"Choosing a specific LLM provider or model. The architectures must work across providers; the harness's `RouterLLM`-equivalent is the right level for that decision."*

**Buried assumption.** That provider-independence is achievable and that `RouterLLM`-equivalent is the right abstraction. Both are *architectural decisions* dressed as scope exclusions. Real architectures couple meaningfully to model behavior (Foundry's V&V-independence assumes provider diversity is available and meaningful; Tournament's diversity policy *requires* multi-provider; Atelier's persona-aligned providers presume different providers behave differently).

**Why it matters.** By declaring provider-choice out of scope, the brief preempts architectures that are explicitly provider-coupled. It also assumes the `RouterLLM` abstraction works — which is a hypothesis, not a fact (does it work for vision-required tasks? for long-context? for tool-calling-heavy work?).

**Remediation.** Restate the exclusion as: "Specific provider selection is deferred to operator time, but architectures may declare provider-property requirements (diversity, long-context, vision, tool-calling latency). The `RouterLLM`-equivalent abstraction is itself open for challenge."

---

## 12. Out-of-scope item: "Methodology evolution as a separate sub-architecture" smuggles an ADR

**Quote (§5):** *"Methodology evolution as a separate sub-architecture. Each v3 architecture must include its own methodology-evolution mechanism, but a meta-architecture for evolving the architecture itself is out of scope."*

**Buried assumption.** That methodology-evolution is *internal* to each architecture rather than a shared substrate primitive. This is a real ADR (it determines whether prompts-as-code, regime tuning, scenario curation, and PRESERVE/APPEND/DATE/REMOVE protocols are per-architecture or shared infrastructure). Tucking it into §5 as scope-exclusion prevents it from getting ADR treatment.

**Why it matters.** If methodology evolution turns out to be substrate-shaped (e.g., a shared knowledge-curation primitive that all architectures consume), the brief has already excluded the right answer.

**Remediation.** Move this out of §5 and into the synthesis as an explicit open question: "Is methodology evolution a per-architecture concern or a shared-substrate primitive?"

---

## 13. The brief silently inherits Round-2's "L3 ceiling" without owning it

**Quote (§2.1):** cites Jaymin's L5 anti-pattern + Shapiro's L4 stance + Jaymin's thresholds. **Quote (§4 ¶note):** ["These items are derived from Round-1 and Round-2 syntheses … free to challenge."]

**Buried assumption.** That the L5-vs-lights-out *tension* is a tension at all. The user's constraint (C1) says "lights-out." Round 2 says "L5 is empirically bad in 2026." The brief frames these as in tension. But the user did not say "L5" — the user said "lights-out," which the brief itself (§2) defines as *L4-or-better-with-conditions*. The "tension" may be a strawman manufactured by mapping the user's word "lights-out" onto Jaymin's "L5" without justification.

**Why it matters.** Treating this as a load-bearing tension consumes Phase-2 attention ("Mandatory treatment in every Phase-2 track") on a problem that may be a vocabulary mismatch. The constraints-extracted doc itself notes "L3 Augmentation as the empirical 2026 ceiling … this is a corpus claim worth testing against the lights-out mandate, not a user constraint."

**Remediation.** Reword §2.1 to acknowledge: "lights-out (as the user used the term) is not necessarily L5 (as Jaymin used the term). The tension is real only if these vocabularies map onto each other; the first task is to test the mapping."

---

## 14. The "common substrate" enumeration is a smuggled ADR list

**Quote (§1):** *"They may also share a common **substrate** (sandbox, scenario storage, cost ceilings, watchdog, trajectory capture, etc.)."*

**Buried assumption.** That this *specific list* of substrate primitives is the right list. Each item is a Round-2 carryover. The "etc." closes the door rhetorically. But other primitives — *coordination medium*, *judge/model-family diversity*, *guard mediator*, *spec storage*, *credential store* — appear in the Phase-5 ADR list (§5.x of the plan) without appearing in this enumeration.

**Why it matters.** The brief's enumeration becomes the de facto substrate definition, anchoring Phase-2 tracks. Items left out get less attention; items included get assumed. The substrate boundary is therefore set by §1's parenthetical, not by Phase 4 deliberation.

**Remediation.** Remove the enumeration from §1 entirely (it pre-decides Phase 4). Replace with: "They may share substrate; *which* primitives are shared is determined in Phase 4, not pre-listed here."

---

## 15. "Archive-and-rebuild over edit-in-place" assumes anchoring risk dominates regression risk

**Quote (§7):** *"Archive-and-rebuild over edit-in-place for the existing 4 architectures and 2 syntheses."*

**Buried assumption.** That the cost of silent anchoring on prior work exceeds the cost of losing hard-won insights when rebuilding from scratch. The user's instruction does support archive-and-rebuild (C6), but Phase 7's back-fill audit is the explicit mitigation — and back-fill audits are notoriously prone to *recency bias*: the v3 output, freshly authored, will feel more compelling than the archived material, and rejection-with-reason will be the path of least resistance.

**Why it matters.** If anchoring risk was actually low (e.g., because the prior work is itself well-grounded), rebuild-from-scratch destroys real signal that back-fill cannot reliably recover. The brief does not estimate the relative magnitudes.

**Remediation.** Add a §7.x explicit acknowledgment: "Archive-and-rebuild prioritizes anchor-avoidance over insight-preservation. The back-fill audit (Phase 7) is the asymmetric mitigation, and is itself subject to recency bias. Lead agent should be especially generous toward archive items in Phase 7."

---

## Summary of severity ranking

1. Mandate as primary axis (smuggled organizing assumption)
2. Lights-out as binary (defining away the architecturally interesting question)
3. Substrate/methodology distinction inherited un-examined
4. §4 "invariants" treated as non-deliberable
5. Falsifiability test cannot falsify
6. Greenfield = "no priors" is an extreme, not a definition
7. Mandate-fit as architecture-level (not work-unit-level) tag
8. OQ-B3 binary preempts the interesting answers
9. Hypothesis is operationally pre-committed despite rhetorical neutrality
10. Jaymin thresholds elevated to gating criteria without user mandate
11. Provider-choice exclusion hides architectural commitment
12. Methodology-evolution exclusion hides an ADR
13. L5-vs-lights-out tension may be vocabulary mismatch
14. Substrate enumeration in §1 is a smuggled ADR list
15. Archive-and-rebuild trade-off un-estimated

*End of critique.*
