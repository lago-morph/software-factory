---
based-on-commit: 6d45e31
based-on-date: 2026-05-23
---

# Uncomfortable contradictions audit (1A bias guard)

**Method.** Re-read the contradictions register (`contradictions.md`, 38 registered + 4 soft candidates) against the post-Round-12 corpus, with explicit hunt for contradictions skipped because they would undermine corpus-popular positions (OpenHands+Overstory substrate stack, Compound Engineering as baseline, "Specs are the durable artifact" D-1, "Agent = Model + Harness" D-3, "Scenarios outside the codebase" D-2, Jaymin's L3-ceiling stance, the 4-architecture v2 set's framing). Sampled deeply from reports the register cites once or zero times (14, 23, 31, 33, 36, 37) plus reports the coverage-gaps section admitted skipping. Produced 11 MISSED findings, 5 WEAK findings, two confirmation-bias patterns, and two load-bearing coverage-gap escalations.

---

## Section 1 — Missed contradictions (new findings)

### MISSED-1 — Anthropic single-judge finding vs. CTR-D4 cross-model-critic framing

- **Claim 1 (Anthropic multi-agent research-system post, via followup [`07`](../../research/followup/07-evals-deepdive.md) §2.3 and §3.6 verbatim):** *"a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements"* — and explicitly: *"For LLM-as-Judge selection, using the same model is usually fine because the judge is doing a different task than your main LLM pipeline."*
- **Claim 2 (CJ Hess `kevin`/`carl`, report [`34`](../../research/34-lenny-howiai-personal-harnesses.md); F46 single-model-review-blindspot; OpenHands RouterLLM mitigation per report [`11`](../../research/11-openhands-substrate-audit.md)):** Same-model self-review is the failure pattern; cross-model critic (carl = Codex/GPT-5.2 reviewing Claude Code) catches what same-model review misses.
- **The contradiction:** Anthropic (the corpus' deepest evals primary) says **same-model judging is fine when the task is different**; CJ Hess/Round-2 say same-model judging is structurally blind. CTR-D4 only captures the substrate-vs-architecture cut of this; it does not register that the corpus is split on whether *judge-model-family independence is even a necessary condition* for the F1/F27 fix.
- **Why this was likely skipped:** Registering this directly undermines the corpus-popular RouterLLM-as-substrate-primitive position AND the corpus-popular "always use cross-model review" rule. Anthropic's claim is inconvenient for both.
- **Recommended CTR-section + impact rating:** Section D (or a new CTR-D7). **High** — directly contests whether judge-diversity is a substrate primitive (D-7-adjacent) or a methodology preference.

### MISSED-2 — Same-model judge legitimacy vs. F46 / Tournament model-family-diversity

- **Claim 1 (followup [`07`](../../research/followup/07-evals-deepdive.md) §3.6 quoting the Husain/Shankar FAQ verbatim):** *"using the same model is usually fine because the judge is doing a different task than your main LLM pipeline. While research has shown that models can exhibit bias when evaluating their own outputs, what ultimately matters is how well your judge aligns with human judgments."*
- **Claim 2 (Tournament spec via archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) Appendix; CTR-D3):** *"explicit model-family diversity to defeat the Hallucination Loop"* — model-family diversity is named as a *necessary* defense.
- **The contradiction:** Husain/Shankar empirically and operationally argue same-model judging is fine if alignment-with-human is measured; Tournament treats model-family diversity as load-bearing. The register flags Tournament-vs-Round-2 (CTR-D3) but not Tournament-vs-Husain/Shankar.
- **Why this was likely skipped:** followup/07 is cited once for OQ-B6 framing only; deep contradictions with the corpus-popular cross-model-review stance would dilute Round-2's RouterLLM endorsement.
- **Recommended CTR-section + impact rating:** Section D, sibling to CTR-D4. **High.**

### MISSED-3 — El Kaim 9-field intent block vs. UC4 spec-malleable hypothesis

- **Claim 1 (El Kaim Ch 3 §4.1, report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md)):** Intent block is a Kubernetes-shaped typed object with `invariants` defined as *"Non-negotiable conditions that any valid realization of the intent must preserve"* — explicitly designed as the **stable upstream** anchor that protects against confabulation when an LLM drafts a spec.
- **Claim 2 (UC4 / glossary §0 [`constraints-extracted`](../constraints-extracted.md)):** Greenfield is **spec-malleable** — *"the system's architecture is still moving during spec refinement; commitments are reversible."*
- **The contradiction:** El Kaim's intent → decision → spec → control → feedback chain *requires* non-negotiable invariants at the top; UC4's spec-malleable framing makes everything reversible. The register has CTR-B2 (greenfield-fluid vs. fixed-once-mature) but does **not** surface that El Kaim's deepest spec-authorship primary anchor structurally rejects the spec-malleable framing as an *upstream* practice.
- **Why this was likely skipped:** Reports 14–17 admitted as covered only at INDEX-anchor depth (per coverage notes); registering this undermines UC4's working hypothesis (D1 motivation) by showing the strongest spec-authorship primary anchor in the corpus prescribes upstream stability, not malleability.
- **Recommended CTR-section + impact rating:** Section B (sibling to CTR-B2). **High** — UC4 hypothesis falsifiability.

### MISSED-4 — Schillace's "code review as firing offense" vs. Anthropic Auto-Review subagent

- **Claim 1 (Schillace, report [`28`](../../research/28-schillace-sunday-letters.md) §"Surprises and contradictions"; restated as CTR-H7):** *"code review as firing offense"* — code review treated as anti-pattern at the team-shape layer.
- **Claim 2 (Anthropic S15 / report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5; Codex Auto-Review subagent, report [`18`](../../research/18-openai-codex-substrate.md)):** Both Anthropic and OpenAI ship **named substrate-level Auto-Review agents** — Anthropic's five specialized critics (duplicate-code coalescer / compiler-performance / efficiency / Rust code-quality critic / documentation), OpenAI's substrate-resident Auto-Review subagent.
- **The contradiction:** CTR-H7 registers Schillace vs. Willison/Compound/Refinery/Foundry but **omits the most-load-bearing counter-claim**: the two largest substrate vendors have made automated code-review-by-a-distinct-agent a *first-class substrate primitive*. Schillace's framing is not just at odds with practice — it is at odds with substrate.
- **Why this was likely skipped:** Anthropic engineering trilogy (report 23) is in the admitted coverage-gap list. Registering this would force the v3 set to choose between two corpus-popular positions (Schillace's team-shape doctrine vs. substrate-resident auto-review).
- **Recommended CTR-section + impact rating:** Sharpens CTR-H7 to high impact (currently medium). **High.**

### MISSED-5 — Anthropic Skills "no network access" vs. "dreaming" overnight research Claws

- **Claim 1 (report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5, anchored on platform.claude.com docs):** Anthropic API-surface Skills have **zero network access by runtime fiat** — *"No network access, No runtime package installation, Pre-configured dependencies only."* This is the substrate-level closure rule.
- **Claim 2 (Shapiro Claw post / report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md), Jesse Vincent's assistant exemplar):** Corpus-canonical "dreaming" primitive — *"every night research things that might help it do its job"* — explicitly requires network access (web search, external research) overnight.
- **The contradiction:** Anthropic's substrate closes the network at the Skill-layer for safety; Shapiro's Claw-as-substrate-template requires nighttime network research to deliver the *dreaming* primitive (Round-2 referenced as a Claw-class capability).
- **Why this was likely skipped:** Both Anthropic Skills (D-3-adjacent) and Shapiro Claw (UC1 lights-out exemplar) are corpus-popular. Naming the contradiction would force resolution of which closure rule wins for the substrate-primitive ADR.
- **Recommended CTR-section + impact rating:** New Section D entry or Section C (substrate). **Medium-high.**

### MISSED-6 — Brier "code is fashion / free to reproduce" vs. report 35 "spec git-history IS the changelog" (CTR-B2 sharpening)

- **Claim 1 (Brier, followup [`12`](../../research/followup/12-brier-pace-layers.md), pace-layer 1):** *"in a world of AI, code is free to produce and reproduce."*
- **Claim 2 (Nystrom / Notion, report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)):** **The spec git-history is the project changelog**; Markdown specs in `agent specs/` subfolder are the **AFIS strategy-3 industrial anchor** — load-bearing durable artifact.
- **The contradiction:** Brier puts specs in pace-layer 3 above code; Nystrom puts the **spec's version-control history** at the heart of the methodology. Both agree spec > code, but disagree on whether the spec itself moves slowly (Brier: stable mid-layer) or *needs an entire revision-tracked change discipline because it moves fast enough that the deltas are the project narrative* (Nystrom). The register has CTR-B3 (El Kaim spec-primary vs. Brier spec-third) but misses this sharper **spec-velocity** disagreement: Brier predicts spec stability; Nystrom predicts spec churn rich enough to function as changelog.
- **Why this was likely skipped:** Both Brier and Nystrom are corpus-popular ("the only voice publicly disagreeing with the factory metaphor" / "first industrial AFIS strategy-3 anchor"). Naming the contradiction is awkward for whichever side wins.
- **Recommended CTR-section + impact rating:** Section B (sharpening CTR-B2 / CTR-B3). **Medium-high.**

### MISSED-7 — Sendbird per-employee token-tier visibility vs. F47 Goodhart + Cherny per-engineer $100K

- **Claim 1 (report [`36`](../../research/36-sendbird-quests-token-tiers.md) §3 verbatim):** Six-tier daily-token leaderboard *"Beginner (<1M tokens/day) → AI God (>100M/day)"*; **goal is curve-smoothness (smooth = AI works 24/7)**; the *executives should be top token consumers*.
- **Claim 2 (CTR-E1 Cherny $100K+/month token spend; F5 cognitive ceiling — archived synthesis §4):** Cherny's industrial-grade token spend per engineer (~$100K+/month); Willison's exhaustion-by-11am cognitive ceiling at 4 agents.
- **The contradiction:** Sendbird operationalizes **token-spend-per-person as a positive-direction org metric** (smoother curve = better) while CTR-E1 frames Cherny's number as a cost ceiling and F5 frames per-human attention as a hard scarce resource. The contradictions register notes CTR-H4 ("Per-employee Claw fleets vs. cognitive-ceiling caps") but **fails to register that report 36 has already crossed the threshold from "fleet of N per human" to "human is graded on aggregate fleet output (tokens) with smoothness as the autonomy proxy."** This inverts F5's framing.
- **Why this was likely skipped:** Report 36 is cited only in the per-employee org-design context, not for the metric inversion. Registering this would surface that the corpus' Theme-5 measurement primitive (curve-smoothness) directly competes with F5 (cognitive ceiling) as the org-design first-principle.
- **Recommended CTR-section + impact rating:** Sharpens CTR-H4 and CTR-E1; possibly a new CTR-H entry. **Medium-high.**

### MISSED-8 — Report 37 Portuguese-vs-English language effect on policy vs. RouterLLM provider-agnosticism

- **Claim 1 (report [`37`](../../research/37-academic-llm-agent-collusion.md) §5 verbatim):** *"The Portuguese-prompted agents are uniformly more collusive and more stably so across both persona conditions"* — natural-language-of-prompt produces a measurable behavioural-drift signal at the **policy/decision layer**, not just the code-generation layer.
- **Claim 2 (OpenHands V1 RouterLLM, report [`11`](../../research/11-openhands-substrate-audit.md); D-3 / Round-2 C10 "Agent = Model + Harness"):** The substrate-level routing abstraction treats the model+harness as a swappable unit. The substrate has no first-class abstraction for "prompt natural language" as a behaviour-influencing harness parameter.
- **The contradiction:** Report 37 supplies the **first empirical anchor** that a *harness parameter the substrate doesn't model* (natural language of the prompt) materially shifts agent behaviour at the policy layer. If true, "Agent = Model + Harness" is incomplete: it's "Agent = Model + Harness + Natural-Language-Register." The register treats F48/F49 (CTR-D5) as multi-agent-CaMeL questions but skips the **substrate-vocabulary-incompleteness** angle.
- **Why this was likely skipped:** Report 37 is cited once (CTR-D5). Registering this would force a re-opening of D-3 (Agent = Model + Harness) on grounds the brief flags as already-fragile, but adds an unfamiliar axis to the fragility argument.
- **Recommended CTR-section + impact rating:** Section C (substrate vocabulary). **Medium-high.**

### MISSED-9 — CaMeL "~7-point utility tax" empirics vs. lights-out cost / output framing

- **Claim 1 (followup [`08`](../../research/followup/08-security-primitives.md) §3, paper-body anchored):** *"77% of tasks with provable security vs. 84% with an undefended system"* — CaMeL imposes a measurable utility tax for substrate-level Trifecta closure.
- **Claim 2 (UC1 lights-out factory + Round-2 §1.1 C13 holdout-discipline-as-substrate; throughput-multiplier framing in report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)):** The substrate-investment thesis is that primitive-level safety is **net-positive** (throughput multiplier). No corpus discussion of the empirical CaMeL utility tax against throughput targets.
- **The contradiction:** The corpus assumes substrate-safety primitives are free or near-free; CaMeL's primary numbers show a 7-point single-pass utility tax (with high per-suite variance per the v2 paper-body fetch). Round-2 elevates substrate-as-cheap; CaMeL is the one substrate-anchored measurement that says **safety has a measurable cost**.
- **Why this was likely skipped:** CTR-D5 covers the multi-agent-generalization question for CaMeL but skips the **cost-of-safety** measurement that contests Round-2's "substrate is cheap" thesis.
- **Recommended CTR-section + impact rating:** Section E (empirical numbers). **Medium.**

### MISSED-10 — Notion Boxy "software factory internally" vs. Brier "software company not factory"

- **Claim 1 (Nystrom transcript via report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md) §3):** Notion engineers call Boxy *"both software factory… but I like its internal project name is uh Boxy."* — the most-cited industrial AFIS strategy-3 deployment **adopts the "software factory" framing internally** even while Boxy is the day-to-day name.
- **Claim 2 (Brier, followup [`12`](../../research/followup/12-brier-pace-layers.md); CTR-F1):** *"It's a software company, not a software factory."* Brier names StrongDM, Shapiro, Factory.ai as targets.
- **The contradiction:** CTR-F1 registers Brier vs. StrongDM/Shapiro/El Kaim, but **omits that the corpus' single strongest industrial primary anchor (Notion/Nystrom) ratifies the factory framing in its own internal vocabulary**. This strengthens the factory side of CTR-F1 in a way the register elides.
- **Why this was likely skipped:** Notion is held up as the AFIS strategy-3 anchor (corpus-popular); inconveniently for Brier, it also confirms the factory frame. Registering this disturbs the Brier-as-decisive-counter-metaphor framing.
- **Recommended CTR-section + impact rating:** Sharpens CTR-F1. **Medium.**

### MISSED-11 — Anthropic Skills "open standard / agentskills.io" vs. Skills "do not sync across surfaces"

- **Claim 1 (report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5, Dec 18 2025 update):** *"We've published Agent Skills as an open standard for cross-platform portability"* at agentskills.io.
- **Claim 2 (report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5, REFUTED-line):** *"Custom Skills do not sync across surfaces"* — claude.ai / API / Claude Code each maintain separate Skill stores; explicit portability gap.
- **The contradiction:** Skills are simultaneously promoted as a portable open standard and shipped with a per-surface portability barrier. Affects the scaffold-as-substrate-primitive ADR (CTR-C6 scaffold-vs-anti-pattern adjacent) — corpus is endorsing a substrate primitive whose own primary docs flag is not actually portable today.
- **Why this was likely skipped:** Report 23 is in the admitted coverage-gap list. Registering this is awkward because Anthropic Skills is the closest the corpus has to a cross-vendor scaffold standard.
- **Recommended CTR-section + impact rating:** Section C (scaffold/substrate). **Medium.**

---

## Section 2 — Weakly-registered contradictions (need sharpening)

### WEAK-1 — CTR-A1 (L5-as-target vs. L5-as-anti-pattern) understates how Jaymin himself contradicts his own anti-pattern claim

- **As registered:** *"One source positions L5 as the aspirational terminus; the other names it as currently dangerous and counter-recommended."*
- **Sharper framing:** Jaymin's Ch 9 §7 is itself a **two-sided text** — it names L5 as anti-pattern *and* frames 2026 as *"the third historical attempt"* at the factory concept with *"LLMs dissolving the flexibility problem that killed both prior attempts"* (report 09 §7 paraphrase). Jaymin is simultaneously the source of the strongest anti-L5 claim *and* a source of the strongest "this time it works" framing. The contradiction is not merely between Shapiro-and-Jaymin; it is internal to Jaymin Ch 9 §7 and parallel to CTR-C6's Jaymin-vs-Jaymin scaffold contradiction.
- **Why the sharpening matters:** CTR-A1 is currently the headline lights-out contradiction. The register treats it as Shapiro-vs-Jaymin. The internal Jaymin-vs-Jaymin reading suggests Jaymin's threshold framework is itself unstable; OQ-B6 cannot just default to "Jaymin's bars" as one credible option without engaging this instability.

### WEAK-2 — CTR-C6 (scaffold-as-load-bearing vs. anti-pattern) is rated high but misses that the Manifesto Rule 2 explicitly invokes "the bitter lesson"

- **As registered:** *"the book treats scaffold quality as something the harness depends on; the manifesto treats it as anti-pattern."*
- **Sharper framing:** The manifesto frames documentation/scaffold as *"the bitter lesson in action"* — i.e., grounded in the same principle Gas City's "Bitter Lesson" design mantra (report [`38`](../../research/38-gas-systems-substrate.md) §3) anchors its substrate exclusion list on. This puts Jaymin's manifesto on the **same intellectual side as the Gas City substrate** and against the Anthropic Skills / SKILL.md convention, the AGENTS.md discoverability primitive (Round-2 substrate primitive #9), and the Compound Engineering knowledge-store. The contradiction is not isolated to Jaymin: it is a **bitter-lesson vs. scaffold-substrate** cross-corpus cleavage.
- **Why the sharpening matters:** Re-frames CTR-C6 as a corpus-wide split (bitter-lesson camp: Jaymin manifesto + Gas City; scaffold-substrate camp: Anthropic Skills + Every SKILL.md + El Kaim Codex + Round-2 C11). The Phase-5 ADR on scaffold cannot be drafted without naming the bitter-lesson side as a coherent corpus position rather than a single-author quirk.

### WEAK-3 — CTR-B5 / D-2 fragility is rated high but understates StrongDM-internal contradiction

- **As registered:** Round-1 promotes out-of-tree scenarios; brief flags as fragile for brownfield.
- **Sharper framing:** StrongDM's own primary pages contain both *"end-to-end 'user story', often stored outside the codebase"* (scenarios out-of-tree) AND *"Tokens are the fuel"* page enumerating *"traces, screen capture, transcripts, **incident replays**, adversarial use, **agentic simulation**"* (report [`01`](../../research/01-strongdm-factory.md) §1) — many of which are **necessarily inside or generated from the running codebase/runtime**. StrongDM's own discipline already permits scenario-equivalents to live inside the running system; the D-2 default ("outside the codebase") is a simplification of StrongDM's actual practice.
- **Why the sharpening matters:** The register's framing makes brownfield look like the awkward case requiring D-2 inversion. The sharper framing shows the **D-2 default itself oversimplifies its primary source**; brownfield is not inverting anything novel — it is closer to StrongDM's actual practice than D-2's stated default is.

### WEAK-4 — CTR-H10 (L3 Augmentation ceiling vs. lights-out mandate) registered correctly but misses that Round-2 §7.6 already classified 3-of-4 v2 architectures at L4

- **As registered:** Round-2 names *"L3 Augmentation as 2026 ceiling"* vs UC1 lights-out.
- **Sharper framing:** Round-2 §7.6 actually classifies architectures across L3 and L4 (not "all at L3"); the contradiction is more precisely *"nothing in 2026 evidence supports L5 anywhere except as a research aspiration"* — which means Round-2's ceiling claim is **L5-anti**, not **L3-only**. If UC1 lights-out maps to L4 (per glossary §0), the Round-2 ceiling is **compatible** with UC1 lights-out. CTR-H10 conflates "ceiling is L3" with "ceiling excludes L5," and these have different downstream implications.
- **Why the sharpening matters:** The contradiction may dissolve at the L4-vs-L5 mapping rather than at the L3-vs-L4 mapping. CTR-A4 (vocabulary mapping) is the actual decisive contradiction; CTR-H10 should be subordinate to CTR-A4, not parallel to it.

### WEAK-5 — CTR-D4 (F1 substrate-mitigable vs. architecture-mitigable) understates that the corpus has a *third* position

- **As registered:** RouterLLM (substrate-mitigation) vs. `kevin`/`carl` (architecture-mitigation).
- **Sharper framing:** Anthropic's Auto-Review subagent (report 23 §3.5, five named specialist critics) is a **third position**: F1 is mitigated by same-model-different-role specialization, neither substrate routing nor cross-model topology. This is the position the largest model vendor ships in its own published doctrine. The register treats F1 mitigation as a two-position split; it is a three-position split, and the third position is the one the corpus' deepest substrate-vendor (Anthropic) actually deploys.
- **Why the sharpening matters:** Phase-4 substrate-vs-methodology boundary cannot be drawn cleanly between just two F1-mitigation positions. The same-model-different-role position belongs in the register.

---

## Section 3 — Suspected confirmation-bias patterns

### Pattern 1 — Contradictions between corpus-popular positions and "newer" corpus material are systematically under-registered

The contradictions register skews toward old-vs-old contradictions (Round-1 vs. Round-2, Shapiro vs. Jaymin, Brier vs. StrongDM) and under-registers contradictions involving **post-Round-9 reports** (especially reports 23, 25/26, 31, 33, 36, 37 and followups 07, 08, 10). Specifically:

- **Followup 07 (evals deepdive)** is cited once for OQ-B6 framing. It contains a primary-source-anchored Anthropic claim (same-model-judging-is-fine) that contradicts the corpus-popular RouterLLM / cross-model-review / F46 cluster. **Not registered** (now MISSED-1, MISSED-2, WEAK-5).
- **Report 23 (Anthropic trilogy)** is in the coverage-gap list. It contains substrate-vs-substrate contradictions (Skills no-network vs. Claw dreaming; open-standard vs. no-cross-surface-sync) plus contradictions with corpus-popular review framings (Auto-Review subagent vs. Schillace's review-as-firing-offense). **Largely unregistered** (now MISSED-4, MISSED-5, MISSED-11).
- **Report 14 (El Kaim spec/intent)** is cited only via CTR-B3 indirectly. The 9-field typed-intent object directly contradicts UC4's spec-malleable framing. **Not registered** (now MISSED-3).
- **Report 36 (Sendbird)** is cited only in CTR-H4 implicitly. Its operational token-tier-as-positive-metric framing directly inverts F5 (cognitive ceiling) as an org-design first principle. **Not registered** (now MISSED-7).
- **Report 37 (collusion)** is cited only via CTR-D5 (CaMeL-multi-agent). Its empirical language-effect-on-policy finding contradicts the D-3 vocabulary directly. **Not registered** (now MISSED-8).

**Diagnostic.** The register's narrative is dominated by Round-1/Round-2 archived material plus Shapiro/Jaymin/Brier/Willison. The deeper post-Round-9 substrate-and-empirical material is under-mined. This is structurally what one would expect if the subagent prioritized "well-known" tensions over "new" ones.

### Pattern 2 — Contradictions that would weaken Round-2's substrate-stack recommendation are absent

Round-2's substrate recommendation (OpenHands V1 + Overstory + RouterLLM, with substrate-cheap framing) generates several contradictions the register *does* surface (CTR-C5 OpenHands vs. Gas City; CTR-C7 mail-bus vs. GitHub-issues; CTR-C4 RouterLLM vs. provider-aligned profiles; CTR-E4 OpenHands sub-ms persist). What is **missing** is contradictions to the *thesis* of Round-2's substrate stack:

- **Substrate-cheap thesis vs. CaMeL utility tax** (MISSED-9). The corpus has one empirical anchor on substrate-safety cost; it points the wrong way for "substrate is cheap" and is unregistered.
- **RouterLLM provider-agnosticism vs. Anthropic same-model-fine** (MISSED-1 / MISSED-2). The corpus' deepest evals primary undermines the *premise* of RouterLLM being load-bearing (Anthropic: judge-diversity is not necessary when alignment-to-human is measured).
- **Natural-language-as-substrate-axis** (MISSED-8). Report 37 supplies the first empirical signal that "model + harness" is incomplete vocabulary; Round-2 C10 doesn't accommodate this.

**Diagnostic.** The register surfaces "where does the substrate stack live (OpenHands vs Gas City)" and "which provider abstraction is right" but does not surface "*should there be a unified provider abstraction at all*" — the latter would directly undermine the Round-2 recommendation. The register's frame implicitly accepts Round-2's substrate-investment thesis as the baseline; contradictions that would weaken the thesis itself are absent.

---

## Section 4 — Coverage gaps that look load-bearing

Two coverage gaps from the register's own list are load-bearing enough to escalate rather than leave as gaps:

### Escalation 1 — El Kaim 14-17/24 are load-bearing for UC4, not just textual-fidelity

The register's coverage notes describe the El Kaim discrepancies as *"largely textual fidelity issues rather than architectural contradictions."* This understates the case. Report 14 (El Kaim Ch 8) introduces a **typed `ArchitectureSpecification` object** with `derivedFrom: DecisionRecord` and `evidenceSources` rules, which is the corpus' deepest spec-authorship discipline. Report 17 (Codex skill substrate) adds a structured knowledge-store primitive. Report 24 (variability / product lines) proposes F35 (Federation-as-Family Drift) — a multi-architecture-family failure mode that is directly load-bearing for OQ-B7 (organizing axes beyond mandate). None of these is "textual fidelity"; all three contest UC4 (MISSED-3), the scaffold-substrate ADR (WEAK-2), and the architecture-count outcome (OQ-B7 / D1). **Recommendation:** dispatch a focused 1A-supplemental deep-read of reports 14, 17, 24.

### Escalation 2 — followup 07 (evals deepdive) is the corpus' deepest evals-discipline anchor and is barely surfaced

The register cites followup 07 only via OQ-B6 framing. The followup contains primary-source-anchored claims (Anthropic single-judge finding; Husain/Shankar same-model-judging-is-fine; Hamel >90% expert agreement in three iterations) that directly contest the corpus-popular F1-mitigation framings (Tournament model-family diversity; F46 single-model-review-blindspot; CTR-D4 substrate-vs-architecture). The contradictions in MISSED-1, MISSED-2, WEAK-5 all live in followup 07's primary material. **Recommendation:** treat followup 07 as a Phase-1A required-read rather than an OQ-B6-only citation, and re-run the register against it.

---

## Summary

- **MISSED findings:** 11
- **WEAK findings:** 5
- **Confirmation-bias patterns surfaced:** 2 (post-Round-9 material systematically under-registered; Round-2 substrate-thesis contradictions absent)
- **Coverage-gap escalations:** 2 (El Kaim 14/17/24; followup 07)

**Most architecturally-significant new contradiction surfaced:** **MISSED-3** — El Kaim's 9-field typed intent block with non-negotiable invariants structurally contradicts UC4's spec-malleable framing. This is load-bearing because the strongest spec-authorship primary anchor in the corpus prescribes upstream stability as a *prerequisite* for AI-driven downstream work, while UC4 makes upstream reversibility the *defining* greenfield characteristic. If El Kaim is right, the 3 both-mandates tracks (D1) and the 3 greenfield tracks (D1) are searching for an architecture in a regime UC4's own framing rules out at the spec layer. This is at minimum on par with CTR-A4 (the lights-out / L5 vocabulary mapping) as a v3-foundational tension.

*End of uncomfortable-contradictions-audit.md.*
