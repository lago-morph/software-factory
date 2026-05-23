# Newcomer Critique of `00-brief-v3.md`

**Persona.** Experienced software engineer, first day on project. Read only `00-brief-v3.md` and `constraints-extracted.md`. Have not read any research reports, prior architectures, or syntheses.

**Method.** Each finding quotes the text, identifies what a newcomer cannot decode, names the synthesis risk, and proposes a fix.

---

## 1. "Lights-out" used as a term of art without definition

> **§1:** "an autonomous (lights-out) system that produces working software with minimal continuous human-in-the-loop intervention."
> **§2:** "The factory operates **lights-out** — autonomously over extended time horizons …"

**Unclear.** "Lights-out" is treated as a defined operating mode, but the brief gives only a parenthetical gloss ("autonomous"). The constraints file (C1) repeats the phrase but also does not define it. Is "lights-out" identical to "no human in inner loop" (§2), identical to "L5" (§2.1), or something distinct? §8 OQ-B3 then *asks whether* lights-out means "no human ever" vs. "no human in per-cycle inner loop" — i.e., the brief itself flags that the term is under-specified, yet uses it in §1, §2, and the title of §2.1 as if it were settled.

**Risk.** A subagent could synthesize an architecture optimized for "L5 dark factory" (no human ever) while the brief actually intends the looser per-cycle definition — or vice versa. The entire L5-vs-lights-out tension in §2.1 collapses if the two terms are conflated.

**Fix.** Define "lights-out" in §1 with a one-sentence operational definition, and disambiguate explicitly from L5 in §2.1.

---

## 2. The L0–L5 ladder is referenced but never enumerated

> **§2.1:** "**L5 ("dark factory") as an empirical anti-pattern**" … "positions himself at **L4 ("I'm here")**" … "names where the factory operates at L4 vs. L5".

**Unclear.** There is an implied 0–5 ladder ("Five Levels" is named in passing as a "canonical post"). The brief glosses L5 ("dark factory") and L4 ("I'm here") but never lists L0, L1, L2, L3, nor explains what the axis is (autonomy? oversight? capability?). The persona instructions to me even list "L5-vs-lights-out tension … does a newcomer know what L0/L1/L2/L3/L4/L5 mean?" — confirming this is a known gap.

**Risk.** Subagents will silently fill in the ladder from training-data priors (e.g., SAE driving levels). The "L4 vs. L5" classification scheme proposed as option (c) becomes uninterpretable, and architectures may be miscategorized.

**Fix.** Inline a 5-line enumeration of L0–L5 (Shapiro's), or a footnote with the canonical citation and a one-line summary of each level.

---

## 3. "Augmentation / Automation thresholds" cited as bars without listing the bars

> **§2.1:** "**Jaymin's Augmentation-vs-Automation threshold matrix** … Automation Mode requires ≥90% K=5 consistency, 5-of-5 prompt-paraphrase robustness, zero medium-or-high safety incidents."

**Unclear.** "K=5 consistency" is undefined (K of what? consistency of what — output? code? tests?). "Prompt-paraphrase robustness" is undefined as a metric. "Medium-or-high safety incidents" has no taxonomy attached. The reader is asked to treat these as empirical bars without being told how the bars are measured.

**Risk.** A synthesis subagent proposing how the lights-out mandate "clears Jaymin's empirical bars at a per-cycle level" (§2.1 option a) cannot do so concretely — they will invent measurement schemes that may not match Jaymin's.

**Fix.** One paragraph defining K=5, paraphrase-robustness, and safety-incident severity, or a direct quote from report 09 §5.5 with the definitions intact.

---

## 4. Numeric anchors quoted as authoritative with no methodology

> **§2.1:** "CodeRabbit (1.4× critical-issue rate vs. human-reviewed), Veracode (45% OWASP-vulnerable AI-generated code), METR (developers 19% slower than self-estimated when using agents unattended)."

**Unclear.** These are dropped as load-bearing numbers, but the brief does not say what populations, time windows, agent configurations, or task types produced them. Are they directly comparable to the factory's operating regime? A newcomer cannot tell whether they refute the lights-out mandate or are tangential.

**Risk.** Subagents will either over-weight these numbers (treating them as the empirical refutation of lights-out) or dismiss them (because they are unsourced at point of use). Both lead to bad synthesis.

**Fix.** A footnote per number with: study population, methodology, applicability caveat.

---

## 5. C-numbered tags in §4 are uninterpretable

> **§4:** "Agent = Model + Harness ([`13-round-2-synthesis`] §1.1 **C10**). Harness and scaffold are distinct layers (**C11**)." … "(**C13**)" … "(**C15**)" … "(**C14**)" … "(**C16**)".

**Unclear.** The C-prefix is never explained. Are these constraint numbers? Claim numbers? Conclusions of a prior synthesis round? They appear nowhere in `constraints-extracted.md` (which uses its own C1–C8 numbering — and the overlap of namespaces is itself a trap, see finding 6).

**Risk.** A reviewer trying to audit "what survived from Round 2" cannot locate C10/C11/C13/C14/C15/C16 without opening the Round-2 synthesis. A subagent may confuse them with the C1–C8 in `constraints-extracted.md` and apply the wrong provenance rules.

**Fix.** First mention of "Cnn" should say "(Round-2 claim Cnn in [link])"; or rename the constraints-file constraints to "UC1–UC8" (User Constraint) to remove the namespace collision.

---

## 6. Namespace collision between `Cn` (constraints file) and `Cn` (Round-2 synthesis)

> **`constraints-extracted.md`** uses C1, C2, …, C8 for user constraints.
> **§4 of the brief** uses C10, C11, C13, C14, C15, C16 — referring to a different thing in a different document.

**Unclear.** A newcomer reading the brief and the constraints file as a pair will assume the same numbering scheme. The gap (C9 missing) and the jump to C10+ may even read as "C9 was dropped" rather than "different document, different scheme."

**Risk.** Mis-citation: subagents may cite "C13" intending one document and have it parsed as the other. Auditors writing the back-fill audit (§6 item 9) will conflate provenance.

**Fix.** Adopt distinct prefixes (e.g., `UC1` for user constraints, `R2-C10` for Round-2 claims) and update both files.

---

## 7. F-numbered failure modes referenced before introduction

> **§6 item 1:** "A canonical, consolidated **failure-mode catalog** (F1–F49+ resolved including the **F36/F37 collision**; severity ranked separately for greenfield and brownfield)."

**Unclear.** F1–F49+ is treated as an existing artifact, and "F36/F37 collision" is mentioned as a specific known problem. A newcomer has no idea what these failure modes are, where they live, or what makes F36 and F37 collide.

**Risk.** A subagent assigned to produce the catalog cannot tell whether it is starting from scratch, deduplicating an existing list, or only resolving the named collision.

**Fix.** Link to the current pre-v3 failure-mode catalog (even if archived), and give a one-sentence summary of the F36/F37 collision.

---

## 8. "Substrate" used heavily but defined only by examples

> **§1:** "may also share a common **substrate** (sandbox, scenario storage, cost ceilings, watchdog, trajectory capture, etc.)."
> **§3:** "substrate-heavy + thin-methodology design"
> **§4:** "substrate-enforced, not methodology-optional"
> **§6 item 5:** "**shared-substrate document**"
> **§8 OQ-B2:** "boundary fall — at the methodology layer, the substrate layer, or both?"

**Unclear.** Substrate is given as an enumerated list once, then used as if it were a defined architectural layer with an opposing layer ("methodology"). The reader has to infer: substrate = shared platform primitives, methodology = the per-cycle process? But the brief never says so.

**Risk.** "Shared-substrate document" (§6 item 5) is one of the load-bearing artifacts — a synthesis subagent will produce a different document depending on whether they read "substrate" as runtime infra, as a software framework, or as the union of all non-methodology decisions.

**Fix.** A one-line definition in §1 ("By substrate we mean: …; by methodology we mean: …; the boundary between them is one of the v3 questions").

---

## 9. "Harness" and "scaffold" cited as distinct without naming the distinction

> **§4:** "**Agent = Model + Harness** (… C10). Harness and scaffold are distinct layers (C11)."

**Unclear.** The brief states the distinction exists but does not state *what* the distinction is. "Harness" is used in §4, §5, and the OQs without definition. Is the harness the runtime, the tool wrapper, the orchestration loop, the sandbox shell? Is the scaffold the project skeleton, the prompt template, the agent's working notes?

**Risk.** §5 says "the harness's `RouterLLM`-equivalent is the right level for [provider choice]" — that claim depends entirely on what "harness" means. A subagent proposing where model selection lives could place it in the wrong layer.

**Fix.** One-sentence definitions inline at first use; or a defined-terms section at the head of §4.

---

## 10. "Spec-malleable" vs. "code-archaeological + existing-architecture-as-given" — asymmetric precision

> **§3:** "Greenfield is **spec-malleable** (architecture changes during spec refinement). Brownfield is **code-archaeological + existing-architecture-as-given** (architecture is largely fixed by the existing codebase; the factory analyses what is there and grows it)."

**Unclear.** "Spec-malleable" gets one parenthetical. "Code-archaeological" gets none — the reader is left guessing whether it means literal source archaeology (git-log spelunking), structural archaeology (dependency graphing), or a documentation-recovery exercise. The two terms are introduced as a dichotomy but defined with very different levels of precision.

**Risk.** Brownfield architectures will be synthesized against a fuzzier target than greenfield ones — exactly the definitional asymmetry the persona brief warns about.

**Fix.** Match the level of definition: define "code-archaeological" with a parenthetical naming the activities it covers.

---

## 11. "Atelier-style" / "Refinery-style" name-drops in OQ-B4

> **§8 OQ-B4:** "is the unit of work an *issue* (**Atelier-style**), a *change request against a spec* (**Refinery-style**), or a *codebase-evolution proposal* (a shape not yet in the four-architecture set)?"

**Unclear.** Atelier and Refinery are two of the "four-architecture set" but the brief never names the set or characterizes any of them. The constraints file says the four architectures are *archived to prevent silent anchoring* (C6) — yet the brief then anchors OQ-B4 in two of their names. A newcomer cannot tell what an "Atelier-style issue" or a "Refinery-style change request" looks like.

**Risk.** The brownfield Phase-2 tracks will treat these as anchor templates because the names are concrete, while the third option ("not yet in the four-architecture set") is intentionally abstract — biasing the outcome toward the named two.

**Fix.** Either (a) one-sentence summaries of Atelier-style and Refinery-style at point of use, or (b) restate OQ-B4 without the proper nouns (e.g., "issue-driven, spec-delta-driven, or codebase-evolution-driven").

---

## 12. "Cold-start problem" enumerated by jargon, not characterized

> **§8 OQ-B5:** "how does the cold-start problem (no scenarios, no issue queue, no `docs/solutions/`, no prior runs) bootstrap?"

**Unclear.** `docs/solutions/` is referenced as if it were a known canonical directory. A newcomer has no idea what lives there, why its absence matters, or whether `docs/solutions/` is a convention from one of the four archived architectures (in which case it is anchoring — see C6).

**Risk.** A greenfield cold-start track may design around populating `docs/solutions/` specifically, baking in a convention from prior work that the v3 synthesis was meant to re-derive.

**Fix.** Replace `docs/solutions/` with a generic description ("no archived solution patterns"), or define what it is and why it is canonical.

---

## 13. "RouterLLM-equivalent" used as a level-of-abstraction marker

> **§5:** "the harness's `RouterLLM`-equivalent is the right level for that decision."

**Unclear.** `RouterLLM` is in code-font, suggesting it is a specific named component, but the brief does not say whose, from what report, or what it does. A reader who does not already know RouterLLM as a library/pattern cannot evaluate "the right level."

**Risk.** Out-of-scope boundary becomes fuzzy: subagents may either treat RouterLLM as a required substrate piece, or ignore the claim entirely.

**Fix.** "(a per-call model-routing layer — see [link])" inline.

---

## 14. "Tiered watchdog (Daemon / Triage / Patrol)" presented as fully-specified

> **§4:** "**Tiered watchdog (Daemon / Triage / Patrol) is a substrate primitive** (… C14)."

**Unclear.** Three role names — Daemon, Triage, Patrol — are presented as if their roles are obvious. They are not. A newcomer cannot tell which tier runs on what cadence, what each watches for, or whether the names map to known patterns (cron daemon? alert triage?).

**Risk.** Architectures must "respect" this invariant — but a subagent who guesses wrong about what each tier does may bake in incompatible assumptions.

**Fix.** One-line per tier, or a direct link with anchor to the C14 definition.

---

## 15. "OpenHands V1 sub-ms per-event persist, 7.4ms median crash recovery" — numbers without context

> **§4:** "(C16; OpenHands V1 sub-ms per-event persist, 7.4ms median crash recovery)."

**Unclear.** OpenHands V1 is named without expansion or link. The two numbers are dropped as if they support the invariant ("trajectory capture is cheap") but a newcomer cannot tell whether OpenHands is a system the factory uses, a reference implementation, or a competitor benchmark.

**Risk.** Subagents may treat OpenHands as a default substrate dependency (it appears in the constraints file's *NOT-a-constraint* list as "OpenHands SDK"), creating exactly the silent anchoring C6 was meant to prevent.

**Fix.** Footnote OpenHands V1 at first reference; clarify whether it is normative or merely the source of the cited numbers.

---

## 16. Report-by-number citations assume the reader can pick the right one

> **§2.1:** "report [`09`]" … "report [`32`], followup [`01`]"
> **§4:** "[`00-synthesis`] §2.1" … "[`13-round-2-synthesis`] §1.1"

**Unclear.** The brief uses pure numeric handles (09, 32, 01, 13) without enough at-the-citation context for a reader to know *why* they would open that file. A reader pointed to "followup [`01`]" has no idea what topic followup 01 covers — and there is presumably more than one followup 01 over the lifetime of the project.

**Risk.** When the synthesis is audited, claims will be checked against the wrong report, or a subagent reading the brief will silently ignore the references because opening 5+ reports to evaluate a single paragraph is impractical.

**Fix.** Each numeric citation gets a 3–8-word topic tag: "report 09 (Jaymin, *Agentic Engineering* harnesses & practices)".

---

## 17. §6 output list assumes the reader knows what each artifact is for

> **§6 items 1–10:** "failure-mode catalog", "contradictions register", "corpus inventory", "shared-substrate document and divergence document", "ADRs", "architecture specs", "comparison document with … mandate-fit matrix", "back-fill audit", "lean-evaluation briefs".

**Unclear.** Several of these are obvious to a v3-process insider but opaque to a newcomer:
- "**Contradictions register**" — register of what kind? Internal to corpus? Between architectures? Updated by whom?
- "**Corpus inventory** (per-report anchor + mandate-fit tag)" — what is a per-report anchor?
- "**Lean-evaluation briefs** (1-day manual run designs)" — manual run of what — the factory? a candidate architecture? a single agent?
- "**Back-fill audit**" — audit how? against what criteria?

**Risk.** A subagent assigned to produce any of these will guess at scope. The "1-day manual run designs" especially could mean five different things.

**Fix.** One-line gloss on each output describing scope, audience, and what "done" looks like.

---

## 18. "Mandate-fit YAML header" — convention not specified

> **§6 item 7:** "**Architecture specs** (count emergent, not predetermined), each carrying a `mandate-fit` YAML header."

**Unclear.** No schema is given. A newcomer cannot tell whether `mandate-fit: both` is valid, whether qualifiers are allowed (`mandate-fit: greenfield-strong, brownfield-weak`), or whether the values are exactly `greenfield | brownfield | both` (constraints file C3 implies the latter but the brief does not confirm).

**Risk.** Specs will be produced with inconsistent headers; the mandate-fit matrix (§6 item 8, "the single most user-facing artifact") will be hard to assemble.

**Fix.** Inline the allowed values, or cite the schema document.

---

## 19. "Back-fill" used as a defined process without definition

> **§7:** "**Archive-and-rebuild over edit-in-place** for the existing 4 architectures and 2 syntheses"
> **§6 item 9:** "A **back-fill audit** documenting what survived from archived v1/v2 material and why."
> **`constraints-extracted.md` C6:** "Back-fill happens later (Phase 7) as a controlled re-introduction."

**Unclear.** "Back-fill" is the name of a Phase-7 process but the brief gives no description of how the process works — what is considered? what is rejected? on what criteria?

**Risk.** The back-fill audit (§6 item 9) will be produced against undocumented criteria. The reader cannot evaluate whether items were fairly retained or fairly excluded.

**Fix.** A paragraph (or pointer to the plan) describing back-fill mechanics.

---

## 20. Reading-order trap: §2.1 depends on terms not introduced until §4 / not at all

> **§2.1** uses "lights-out", "L4", "L5", "Augmentation Mode", "Automation Mode", "K=5", "prompt-paraphrase robustness".

**Unclear.** §2.1 is the *first* section after the §1 framing, and is flagged "load-bearing, must be addressed." Yet it leans on terminology that is either never defined (the L-ladder, the threshold metrics) or defined only later (e.g., "harness" first appears in §4's invariant list). A reader hitting §2.1 fresh cannot evaluate the tension.

**Risk.** §2.1's "working stance: option (c) is the most likely shape" reads as obvious to insiders but unsupported to a newcomer — meaning a reviewer cannot challenge it on the merits, and a subagent will treat the working stance as a soft default.

**Fix.** Either move a "Defined terms" preface in front of §2.1, or push the L-ladder and threshold-metrics discussion into a §1.x glossary that §2.1 then references.

---

## 21. "Phase 0.4–0.6", "Phase 2", "Phase 3", "Phase 4", "Phase 6", "Phase 7" referenced without map

> Throughout: "Phase 0.4–0.6", "Phase-2 tracks", "Phase 3 by a dedicated cross-mandate adversarial pass", "Mandatory treatment in Phase 4", "Phase 6", "Phase 7".

**Unclear.** The phase numbering is treated as canonical but the brief does not enumerate the phases or link to the plan that does (only `ARCHITECTURE-V3-SYNTHESIS-PLAN.md` is mentioned once in §7, in passing). A newcomer cannot tell what each phase produces, who runs it, or in what order.

**Risk.** "Mandatory treatment in every Phase-2 track" is unenforceable if a subagent does not know what the Phase-2 tracks are.

**Fix.** A single-sentence phase map at the top of the brief, or a prominent "see plan" link in §1.

---

## 22. "Adversarial pass" / "persona-diverse review" treated as defined practices

> **§3:** "tested in Phase 3 by a dedicated cross-mandate **adversarial pass**."
> **§7:** "**Persona-diverse subagent review at every phase**, not just adversarial."

**Unclear.** Both phrases are used as if they name specific review protocols. The brief does not say who participates, what the deliverable of a "pass" or "review" is, or what distinguishes "persona-diverse" from "adversarial."

**Risk.** A subagent asked to run "the adversarial pass" produces a different artifact than one asked to run "persona-diverse review" — but the brief implies they are different things without saying how.

**Fix.** One-line definitions; or a single link to the bias-guards/process doc that defines them.

---

*End of newcomer-critique.md.*
