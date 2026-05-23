---
based-on-commit: 6d45e31
based-on-date: 2026-05-23
---

# Miscategorization audit (1C bias guard)

**Method.** Pressure-tested mandate tags on all 50 entries in `/home/user/software-factory/architectures/v3/corpus-inventory.md`. Cross-referenced the brief's §0 definitions (greenfield = no pre-existing implementation; brownfield = pre-existing codebase + tests + telemetry as primary inputs), D1 (3 unified-mandate tracks need their own "load-bearing for unified case" reading list), the §5.1 cold-start required reading (25, 26, 30, 31, followup/10 — designated for greenfield + greenfield-addressing both-mandates tracks), and the inventory's own §D disputed list. Specifically hunted for: (a) `both-primary` that should be single-mandate (the generosity bias); (b) `both-secondary` / `tangential` that should be `both-primary` (the dismissal bias); (c) anchor/tag mismatches where the paragraph describes a clearly-skewed report but the tag is symmetric; (d) coverage of the 3 D1 unified-mandate tracks.

The headline finding is structural: **the inventory contains zero `greenfield-primary` and zero `brownfield-primary` tags, even though the brief explicitly designates 5 reports as greenfield cold-start required reading (an asymmetric load) and several methodology/substrate reports are anchored on brownfield-shaped artifacts (queues of issues, existing codebases, production telemetry).** The symmetric tagging is not in itself wrong on any single entry — most of the corpus is genuinely cross-applicable — but the absence of *any* asymmetry in 50 entries is itself a bias signal.

11 tag challenges below. Material but not catastrophic; the inventory is in mostly-good shape, but the asymmetry-blindness is worth surfacing.

---

## Section 1 — Tag challenges (entries where I disagree with the subagent)

### CHALLENGE-1 — Report 25 — requirements-engineering-foundations
- **Current tag:** `both-primary`
- **Anchor (subagent):** "Cold-start required reading per brief §5.1 (Historian M5). The RE/SE counterpart to report 14 (El Kaim) ... best read as a domain instantiation of GtWR."
- **Proposed tag:** `greenfield-primary` (with brownfield as secondary use)
- **Reasoning:** Brief §5.1 explicitly designates this report as required reading for **every greenfield cold-start track and every both-mandates track that addresses greenfield** — not for brownfield tracks. EARS / GtWR / Complexity Primer / AFIS strategy-3 are tools for **bootstrapping** a spec without a codebase to mine; brownfield's primary spec source is the existing codebase, tests, and telemetry (per the §0 brownfield definition). A brownfield track could read 25 for vocabulary, but it isn't load-bearing for brownfield in the way it is for greenfield.
- **Confidence:** high

### CHALLENGE-2 — Report 26 — prompt-underspecification-academic
- **Current tag:** `both-primary`
- **Anchor (subagent):** "Cold-start required reading per brief §5.1. The corpus' academic-empirical anchor for the 'spec → code gap' intuition."
- **Proposed tag:** `greenfield-primary` (with brownfield as secondary use)
- **Reasoning:** Same logic as CHALLENGE-1. The Yang et al. "Pass@1 98.7%→85.0% as specs scale" finding is a **specs-as-the-only-input** failure mode — the situation a greenfield cold-start track inherits by definition. A brownfield track has the codebase as a second input and can triangulate; the silent contradictory-prompt collapse (73.8%→6.7%) is greenfield-shaped because brownfield's existing-code anchor catches the contradiction at compile/test time.
- **Confidence:** high

### CHALLENGE-3 — Report 30 — cognitive-escrow
- **Current tag:** `both-primary`
- **Anchor (subagent):** "Cold-start required reading per brief §5.1 ... names the prompt→response interval as a harness-engineering design surface."
- **Proposed tag:** keep `both-primary` (challenge rejected after consideration)
- **Reasoning:** Although flagged as cold-start required, the **prompt→response interval** is genuinely substrate-layer and applies symmetrically across mandates. Attention Firewall, AILCCP missing-fourth-question, STIR — none of these are greenfield-specific. The §5.1 designation reflects user-priority for cold-start, not mandate skew. Keep as-is.
- **Confidence:** medium (close call; flagging so lead agent can confirm)

### CHALLENGE-4 — Report 31 — caremark-rsi-board-exposure
- **Current tag:** `both-primary`
- **Anchor (subagent):** "Cold-start required reading per brief §5.1 ... Delaware-law-grounded board exposure analysis for RSI deployments."
- **Proposed tag:** keep `both-primary` (challenge rejected)
- **Reasoning:** Caremark / RSI / SB 53 / SEC IAC apply to any factory deployment regardless of mandate. The cold-start tag in §5.1 is about "defensible from day 0" framing for greenfield, but the underlying liability surface is mandate-agnostic. Keep as-is.
- **Confidence:** medium

### CHALLENGE-5 — Followup 10 — governance
- **Current tag:** `both-primary`
- **Anchor:** "Cold-start required reading per brief §5.1. Deepest governance-literature anchor."
- **Proposed tag:** keep `both-primary` (challenge rejected)
- **Reasoning:** AILCCP / BCG Five Pillars / Replit DB wipe / Moltbook breach are mandate-agnostic; brownfield refactoring runs into governance just as hard as greenfield bootstrap (arguably harder — production blast radius is larger). Keep as-is.
- **Confidence:** high

### CHALLENGE-6 — Report 03 — every-compound-engineering
- **Current tag:** `both-primary`
- **Anchor (subagent):** "Source of the Compound Engineering methodology (plan → work → review → compound) ... the queue of issues + accumulating skills + agent panel review shape ... treats the unit of work as an issue against an evolving knowledge base."
- **Proposed tag:** `brownfield-primary` (with greenfield as secondary)
- **Reasoning:** **Tag/anchor mismatch.** The anchor itself names "queue of issues against an evolving knowledge base" — the defining shape of a brownfield work cycle (issues presuppose a pre-existing system that has issues). Cora is a Klaassen brownfield workflow. The methodology can be adapted to greenfield but its native habitat is brownfield. OQ-B4 explicitly tags Atelier-style "issue from a queue" as a brownfield work-unit option.
- **Confidence:** high

### CHALLENGE-7 — Followup 11 — compound-knowledge
- **Current tag:** `both-primary`
- **Anchor:** "Companion to report 03 (Compound Engineering). CK is the knowledge-work twin of CE — same loop, same Git-tracked Markdown substrate."
- **Proposed tag:** `brownfield-primary` (with greenfield as secondary)
- **Reasoning:** Inherits CHALLENGE-6's logic — accumulating typed learnings (insight/playbook/correction/pattern) presupposes a queue of prior cycles to compound from. A greenfield day-0 factory has nothing to compound yet (cold-start is precisely this problem). Brownfield-native.
- **Confidence:** high

### CHALLENGE-8 — Report 22 — academic-foundations
- **Current tag:** `both-primary`
- **Anchor (subagent):** "SWE-bench Verified's 93-developer / 1,699-sample / 4-level-severity ... the canonical 'nutshell-bench' diagram (Issue + Codebase → LM → PR → Tests)."
- **Proposed tag:** `brownfield-primary` (with greenfield as secondary, for V&V baseline only)
- **Reasoning:** **Tag/anchor mismatch.** SWE-bench Verified is structurally a brownfield benchmark — Issue + Codebase → PR is the prototypical brownfield work cycle. The benchmark methodology cannot be applied to greenfield day-0 (there is no codebase). Greenfield tracks can borrow the *V&V annotation discipline* (4-level severity, ensemble-3), but the load-bearing content is brownfield-shaped.
- **Confidence:** high

### CHALLENGE-9 — Report 12 — adjacent-ecosystem
- **Current tag:** `both-secondary`
- **Anchor (subagent):** "The §2.5 Kiro extension ... is the most actively-loaded section — Kiro's spec-driven development paradigm overlaps with brownfield refactoring concerns."
- **Proposed tag:** keep `both-secondary` but add a `brownfield-leaning` note
- **Reasoning:** The anchor explicitly says the load-bearing slice overlaps with brownfield refactoring. A brownfield track interested in spec-driven refactoring should treat Kiro as a primary touchpoint within this secondary report. Not a full re-tag because the rest of the report is breadth.
- **Confidence:** medium

### CHALLENGE-10 — Report 21 — tabnine-enterprise
- **Current tag:** `tangential` (subagent §D-2 flagged this as pressure-test candidate)
- **Anchor:** "Vendor audit; enterprise context isolation, on-prem deploy, model-routing posture."
- **Proposed tag:** `both-secondary` (promote one notch)
- **Reasoning:** On-prem deploy + context isolation are the substrate concerns of a brownfield factory operating on a regulated enterprise codebase (the situation OQ-B4 brownfield tracks must address). Tangential is too dismissive when the substrate posture has direct brownfield relevance. Not `both-primary` — narrow scope — but `both-secondary` with a `brownfield-context` note fits.
- **Confidence:** medium

### CHALLENGE-11 — Report 24 — el-kaim-book-product-line-variability
- **Current tag:** `both-secondary` (subagent §D-3 flagged)
- **Anchor:** "Family-of-products / variability framing as a meta-architectural concern ... tangential to single-codebase scope (per brief §7) but informs the v3 multi-architecture question of when one architecture is many."
- **Proposed tag:** keep `both-secondary` (challenge rejected after consideration)
- **Reasoning:** Brief §7 explicitly defers multi-codebase to future work. OQ-B7 leaves alternative axes open, but variability is genuinely orthogonal to the mandate axis. Secondary is right.
- **Confidence:** high

### CHALLENGE-12 — Followup 09 — methodology-ancestors
- **Current tag:** `both-secondary` (subagent §D-5 flagged)
- **Anchor:** "Kaner's five characteristics ... underlie the corpus' 'scenarios as holdout set' default (D-2). Rumelt's kernel ... underlies the spec-as-strategic-direction framings."
- **Proposed tag:** keep `both-secondary` (challenge rejected)
- **Reasoning:** Partial-source provenance (WebFetch 403s; reconstructed from snippets) caps confidence at secondary even though the structural framings underlie D-2. The anchor explicitly notes passage-level fidelity is soft. Secondary right.
- **Confidence:** high

### CHALLENGE-13 — Reports 04 / 17 / 23 scaffold-substrate triple (subagent §D-7)
- **Current tags:** 23 = `both-primary`; 04 = `both-primary`; 17 = `both-secondary`
- **Proposed tags:** keep 23 + 04 `both-primary`; keep 17 `both-secondary` (no change)
- **Reasoning:** No actual double-counting. Report 23 is the primary-doc anchor (concrete schema constraints: 64-char limit, ~100 token Level-1, zero network access). Report 04 is the convention/origin anchor. Report 17 is El Kaim's adjacent treatment. The substrate track needs 23 + 04 deep-read; 17 confirmable as secondary. Tags as-is correctly reflect this.
- **Confidence:** high

### CHALLENGE-14 — Followup 12 — brier-pace-layers (subagent §D-6)
- **Current tag:** `both-primary`
- **Anchor:** "The corpus' single explicit public counter-metaphor to the software-factory framing."
- **Proposed tag:** keep `both-primary` but with **special "counter-metaphor / every track must engage" status** (see §3 below)
- **Reasoning:** The subagent's reasoning (every track must engage because it's the only counter-voice) is correct. But that reason is **categorically different** from "load-bearing for both mandates' substantive content" — Brier is load-bearing as the **dialectical counterweight**, not as substantive design input. The current scheme can't express this distinction; §3 below proposes a `counter-metaphor` supporting tag to mark it.
- **Confidence:** high

### CHALLENGE-15 — Report 37 — academic-llm-agent-collusion (subagent §D-4)
- **Current tag:** `both-primary`
- **Anchor:** "First academic-empirical anchor for Theme-2 alignment-drift / collusion in a market setting at LLM scale."
- **Proposed tag:** demote to `both-secondary`
- **Reasoning:** The subagent kept it primary on three grounds: (a) extends language-as-harness to decision layer, (b) F48/F49 named, (c) first academic-empirical anchor for Theme-2 in market. All three are *novelty* arguments, not *load-bearing-for-architecture-design* arguments. The empirical setting is **market pricing of a duopoly**, not software production. A factory architecture does not need to clear Bertrand-Nash to be valid. Multi-agent tracks should read it; single-agent tracks safely skip. Secondary is honest.
- **Confidence:** medium

---

## Section 2 — Disputed-tag resolutions (subagent §D, items 1–7)

**§D-1 — Report 10 (overstory-substrate-audit) → `both-secondary`.** **Keep as-is.** The substrate-audit content is narrow scope; report 11 (OpenHands) is the deeper substrate anchor. Overstory is useful as a *non-OpenHands baseline* but no Phase-2 substrate question is load-bearingly dependent on it. Secondary is right.

**§D-2 — Report 21 (tabnine-enterprise) → `tangential`.** **Promote to `both-secondary`** per CHALLENGE-10. Enterprise context isolation + on-prem are brownfield-relevant.

**§D-3 — Report 24 (product-line-variability) → `both-secondary`.** **Keep as-is** per CHALLENGE-11. Multi-codebase is scope-deferred (brief §7); variability is orthogonal to mandate axis.

**§D-4 — Report 37 (academic-llm-agent-collusion) → `both-primary`.** **Demote to `both-secondary`** per CHALLENGE-15. Novelty is not load-bearingness.

**§D-5 — Followup 09 (methodology-ancestors) → `both-secondary`.** **Keep as-is** per CHALLENGE-12. Partial-source provenance + structural-only firmness caps at secondary.

**§D-6 — Followup 12 (brier-pace-layers) → `both-primary`.** **Keep at `both-primary` + add `counter-metaphor` distinguishing tag** per CHALLENGE-14. The subagent's reasoning is right but the category is special enough to deserve its own marker. The current scheme treats Brier and (say) report 28 Schillace as same-tag, but Brier is read for **positioning** while Schillace is read for **substantive input**.

**§D-7 — Reports 04 / 17 / 23 (scaffold-substrate triple).** **Keep as-is** per CHALLENGE-13. No double-counting in practice.

---

## Section 3 — Coverage for the 3 D1 unified-mandate tracks (per D1)

**The gap.** The 5-tag mandate-relevance scale (greenfield-primary / brownfield-primary / both-primary / both-secondary / tangential) does not expose a **unified-track must-read** category. D1 dispatches 3 no-axis-prescribed subagents tasked to find ONE architecture covering both mandates — these tracks need a different reading list than the 6 mandate-specific tracks. The current both-primary tag bundles two distinct uses (load-bearing for **single-mandate-but-applies-to-both** vs. load-bearing for **the-unified-case-itself-might-be-possible**).

**Proposed must-read list for unified-mandate tracks** (drawn from the 50 entries; these are the sources that suggest cross-mandate primitives or directly speak to the unified case):

1. **Followup 12 (brier-pace-layers)** — the counter-metaphor + pace-layers stack (Code / Plans / Specs / Architecture / Standards) is a candidate unified primitive: a layered substrate spanning both mandates with different lifecycle cadences.
2. **Report 27 (dotfile-pipelines-as-product)** — `.dot` file as the durable artifact + engines as commodity reframes methodology as data; the same `.dot` pipeline could serve greenfield bootstrap and brownfield refactor as different rigs.
3. **Report 38 (gas-systems-substrate)** — substrate-vs-application split (Gas City SDK vs Gastown pack) is the corpus' most explicit unified-substrate candidate; both deployment sketches (`darkfactory` pack + `compound` pack on Gas City) live on the same engine.
4. **Followup 13 (gas-city-deep-dive)** — engine-level depth source for #3.
5. **Report 28 (schillace-sunday-letters)** — agent-OS building-block list + Amplifier internals (Dev Foundry / session analyst / Crusty Old Engineer) suggest a unified substrate stack independent of mandate.
6. **Report 14 (el-kaim-spec-and-intent)** — typed spec objects + intent-block discipline operate identically on greenfield (spec creates the system) and brownfield (spec constrains refactor); the 1:1 GtWR mapping makes it a unified substrate candidate for the spec layer.
7. **Report 18 (openai-codex-substrate)** — `.rules` DSL + OTEL five-event export are mandate-agnostic substrate primitives — strongest commercial substrate exemplar for the unified case.
8. **Report 11 (openhands-substrate-audit)** — trajectory capture + RouterLLM as mandate-agnostic measurement substrate.
9. **Followup 07 (evals-deepdive)** — orchestrator-worker + filesystem-as-shared-artifact + binary-judge findings are V&V primitives that apply to either mandate without modification.
10. **Followup 08 (security-primitives)** — CaMeL + sandboxing are substrate-layer security; mandate-agnostic.
11. **Report 30 (cognitive-escrow)** — interval-as-design-surface is mandate-agnostic (humans wait for AI in both greenfield and brownfield cycles).
12. **Report 09 (jaymin-harnesses)** — regime / threshold-bars apply to both mandates; load-bearing for OQ-B6 in both cases.

**Coverage observation:** the unified-track must-read list skews toward **substrate** reports (11, 14, 18, 28, 30, 38, F07, F08, F13) rather than methodology reports. This is consistent with the lead-agent working stance that "substrate-heavy + thin-methodology" may be how a unified architecture emerges. The 3 unified tracks should be warned that the corpus' methodology reports tend to be **single-mandate-shaped** (Compound = brownfield; cold-start = greenfield) and unified architectures will have to invent or borrow methodology cross-cuts.

**Recommendation.** Add a §C-bis section to corpus-inventory.md listing these 12 entries as "Unified-mandate track must-read," parallel to the existing §C (Cold-start required reading).

---

## Section 4 — Tag-distribution observations

**The numbers.** 30/50 = 60% `both-primary`; 14/50 = 28% `both-secondary`; 1/50 = 2% `tangential`; 0 `greenfield-primary`; 0 `brownfield-primary`.

**View.** **60% `both-primary` is too high** — but more importantly, **0% single-mandate is structurally wrong.** The brief explicitly treats greenfield and brownfield as potentially-distinct mandates with a falsifiable hypothesis (UC4/D1) that no single architecture works for both. If the corpus inventory tags 0 of 50 entries as primarily serving one mandate, the inventory is implicitly asserting the unified-hypothesis is already proved — pre-empting Phase 2's D1 falsification work.

The cold-start required-reading set (reports 25, 26 in particular) is genuinely greenfield-skewed by the brief's own §5.1 designation. The compound-engineering family (03, F11) and the SWE-bench-anchored report 22 are brownfield-skewed by their structural shape (queue of issues; Issue + Codebase → PR).

Applying my 11 challenges + the §D resolutions yields a revised distribution of approximately:
- `greenfield-primary`: 2 (reports 25, 26)
- `brownfield-primary`: 3 (reports 03, 22, F11)
- `both-primary`: ~26 (down from 30, after demoting 37)
- `both-secondary`: ~17 (up by promoting 21, +F09/F13/F14 unchanged)
- `tangential`: 0–1 (after promoting 21)

This puts both-primary at ~52% — still the plurality, which is corpus-accurate (most reports do speak to both) — but with the asymmetry signal restored. **The asymmetry restoration is the load-bearing fix; the absolute distribution is downstream.**

**Brier note (subagent flagged "every track must engage with counter-metaphor voice").** Brier deserves a **special category**, not the standard both-primary. The "every track must engage" reason is *dialectical* (read to position against), not *substantive* (read for design input). The current scheme conflates these. My recommendation in CHALLENGE-14 / §D-6: add a `counter-metaphor` supporting tag (Brier is currently the sole holder; reports 12 Schillace soft-team-shape framing and 07 Dark Factory are partial contestants but already substrate-laden). This tag would warn subagents: "Brier is mandatory reading for positioning, but don't try to absorb his framework — it actively rejects yours."

---

## Section 5 — Coverage notes (areas I couldn't fully verify)

- **Did not deep-read all 50 reports.** Sampled the disputed-tag and challenge-candidate entries via the inventory anchor + INDEX.md per-report subject line; relied on the subagent's anchor paragraphs for entries not flagged for challenge. A deeper pass on (say) followups 5–8 might surface additional skew I missed.
- **The "unified-track must-read" list in §3 is my judgment call** based on which entries name mandate-agnostic substrate primitives. Other readers may include/exclude differently — e.g., I included followup/07 (evals) and excluded report 29 (prompt taxonomy); a track focused on judge design might invert that.
- **Reports 19 (github-copilot-cloud-agent) and 20 (replit-agent)** I left at `both-secondary` because they are vendor-substrate breadth, but Copilot Spaces ≈ AGENTS.md analog at team scope is arguably brownfield-relevant (teams operate on existing codebases). Did not raise a challenge because the both-secondary tag is defensibly broad.
- **The F36/F37 collision is real and orthogonal** — the inventory correctly defers it to lead-agent triage per brief §0 glossary. Out of scope for this audit.
- **Did not audit the §C cold-start subset list itself** — the 5 reports listed match brief §5.1 verbatim; no work to do.

*End of miscategorization-audit.md.*
