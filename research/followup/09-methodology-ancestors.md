# 09 — Methodology Ancestors

**Round 3, Thread 9** — per [`PLAN`](../PLAN.md) §11.9
**Date:** 2026-05-11
**One-line:** Three pre-LLM methodology ancestors that the four architectures structurally inherit from — and what the ancestors did that the descendants dropped.

## Provenance

WebFetch returned HTTP 403 on every primary URL attempted (sandbox-side, not source-side). Content below is reconstructed from WebSearch snippets that quote each source verbatim, plus widely-published summaries. Quotations are taken from snippets attributed to the author; paraphrases name the secondary. Blocked-URLs list at §5. Status: PARTIAL — structural shape firm; passage-level fidelity could be sharper with full-text access.

---

## 1. Cem Kaner — *An Introduction to Scenario Testing* (June 2003)

**Source identifier:** Kaner, Cem. *An Introduction to Scenario Testing*. Florida Tech / kaner.com, June 2003 (Ver. 4 PDF; Ver. 5 reissued on bbst.courses in 2023). Coined the phrase "scenario test" in the testing literature by October 2003.

### 1.1 The methodology in Kaner's own framing

A scenario test is "a hypothetical story, used to help a person think through a complex problem or system." It has **five characteristics**: it is a **story**; the story is **motivating** ("a stakeholder with influence would push to fix a program that failed this test"); **credible** ("stakeholders would believe that something like it probably will happen"); **complex** ("involves many features"); and **easy to evaluate** (easy to tell whether the program passed or failed). Kaner adds a sixth dimension — **power**: "one test is more powerful than another if it is more likely to expose a bug." Low-power tests, even ones satisfying the five characteristics, are candidates for revision.

Scenarios are **generated from stakeholders**: "Meet with users (and other stakeholders) individually and in groups. Ask them to describe the basic transactions … encourage them to tell you the system's funny stories, the crazy things people tried to do with the system." Use cases are a *weaker, simpler* form derived from product capabilities; scenarios come from "naturalistic observation." Kaner cites Hans Buwalda's **"soap opera testing"** — tests "exaggerated in activity and condensed in time" — as a parallel tradition.

### 1.2 What the descendants kept

- **Scenario as unit of acceptance**, distinct from unit/feature tests. All four architectures carry "held-out scenarios" or "acceptance scenarios" — Kaner's story-shaped test.
- **Story-shaped fitness, not assertion-shaped.** Arch 4's Predator generates adversarial *stories*; Kaner's soap-opera move with the agent as bug-hungry tester.
- **"Easy to evaluate."** Arch 4's primary judge requires per-scenario pass/fail clarity — Kaner's fifth characteristic in LLM-judge form.
- **Stakeholder-credible.** Atelier `STRATEGY.md` and Refinery spec practice both implicitly require credibility-to-stakeholders.

### 1.3 What the descendants dropped

- **Stakeholder-generated scenarios.** Kaner's recipe is to *interview users*. None of the four architectures formalize a stakeholder-interview phase. StrongDM's "synthetic scenario curation and shaping interface" replaces this with agent-generated scenarios shaped by a curator. Risk: synthetic scenarios reflect the system's existing model of itself, not the user's. Kaner's recipe was designed to break out of that loop.
- **The "power" dimension as a revisable property.** Kaner says a low-power test, even one that satisfies the five characteristics, should be revised. None of the architectures carry a **bug-discovery-rate-per-scenario** metric that re-ranks scenarios. Arch 4's Predator ranks candidates, not scenarios.
- **Explicit acknowledgement of scenario testing's limits.** Kaner says scenarios "miss testing the error handling … important hardware/software configurations, important timing issues" and should *complement* other test types. Arch 4 leans hardest on scenarios and most needs this guardrail; the Foundry's V&V phase comes closest.

### 1.4 Practical guidance not yet incorporated

- **Stakeholder-interview ritual** for new scenario corpora — even when LLMs do the eventual generation, the *seed* should be a verbatim human-told story.
- **Per-scenario power score** that retires low-power scenarios — the immune-system-editing analogue.
- **"Scenarios are not enough" reminder** in any architecture leaning hard on them: keep a non-scenario test layer (coverage, fault injection, configuration matrix) explicitly named.

---

## 2. Richard Rumelt — *Good Strategy / Bad Strategy* (2011)

**Source identifier:** Rumelt, Richard P. *Good Strategy / Bad Strategy: The Difference and Why It Matters*. Crown Business, 2011. The framework reappears in *The Crux* (2022), which sharpens the "leverage point" notion.

### 2.1 The methodology in Rumelt's own framing

Rumelt's core construct is **the kernel** of a good strategy, with three required elements:

- **Diagnosis** — "a great deal of strategy work is trying to figure out what is going on." It simplifies complexity by naming what is critical. "Without diagnosis there is no strategy — only wish lists, budgets, or hope."
- **Guiding policy** — "channels action without prescribing every step. Like the guardrails on a highway." It creates advantage by "concentrating effort on a pivotal or decisive aspect of the situation."
- **Coherent action** — "feasible coordinated policies, resource commitments, and actions designed to carry out the guiding policy."

Rumelt names four **hallmarks of bad strategy**: **fluff** (jargon masquerading as concepts), **failure to face the challenge** (no named central problem), **mistaking goals for strategy** ("being ambitious is not a strategy"), and **bad strategic objectives** (a long to-do list mislabeled).

Two further moves matter: **proximate objectives** — "a target that the organization can reasonably be expected to hit, even overwhelm," with strategy as "a series of proximate objectives rather than a long-term vision"; and **the crux / leverage point** — "the secret of strategic leverage is finding crucial pivot points and concentrating force on them."

### 2.2 What the descendants kept

The Compound Atelier (Arch 2) names the Rumelt kernel explicitly: the Strategist persona "owns `STRATEGY.md`. Rarely invoked. Rumelt-style: diagnosis / guiding policy / coherent action / explicit non-goals." Every.to's `ce-strategy` skill is the same move. Across architectures:

- **Diagnosis-before-action.** All four separate problem-framing from execution. The Refinery's "classify the failure" loop is diagnosis applied to errors.
- **Guiding-policy-as-guardrails.** The Atelier's decisions-not-pseudocode plans, the Foundry's SAD constraints on Phase 3, and the Tournament's fitness weights all constrain without choreographing.
- **Coherent action.** Stable IDs and traceability ensure moves cannot contradict the kernel.

### 2.3 What the descendants dropped

- **Explicit non-goals.** Only Arch 2 carries them. The Foundry's SRS has no "Non-Requirements"; the Refinery's spec has no "Deliberately Out of Scope" layer ("undiscovered preferences" is a different construct). Without non-goals, scope-creep is unbounded.
- **The crux / leverage point.** None of the four formalize "find the one decisive sub-problem; concentrate force there." Tournament concentrates *computational* force but does not require the Strategist to *name the crux* first.
- **Bad-strategy hallmarks as anti-patterns.** Fluff / unfaced-challenge / goals-as-strategy / to-do-list are checkable failure modes. No architecture reviews Strategist output against them.
- **Proximate objectives.** Cycle-sized goals exist everywhere, but Rumelt's discipline is *one the organization can overwhelm*. No architecture requires sizing-to-confidence.

### 2.4 Practical guidance not yet incorporated

- **STRATEGY.md reviewer persona** scoring against Rumelt's four bad-strategy hallmarks plus a positive "diagnosis + guiding policy + coherent action + non-goals" rubric. Sub-hour cycle.
- **Named "crux" field** in every strategy doc.
- **Explicit "Non-Goals" sections** in SRS (Foundry), spec layers (Refinery), genome seeds (Tournament).
- **Proximate-objective sizing check**: "will the team overwhelm this or merely hit it?" If the latter, the goal is too big.

---

## 3. W. Edwards Deming — PDCA / PDSA cycle (Shewhart 1939; Deming popularized; renamed PDSA later)

**Source identifier:** PDCA (Plan-Do-Check-Act) originates with Walter Shewhart (*Statistical Method from the Viewpoint of Quality Control*, 1939). Deming popularized it at Japanese industry in the 1950s. Deming renamed it **PDSA (Plan-Do-Study-Act)** in the late 1980s/early 1990s, with the change of "Check" to "Study" reflecting his theoretical commitments.

### 3.1 The methodology in Deming's own framing

The four phases as Deming taught them:

- **Plan** — develop a theory and a prediction. "Without theory, there is no learning. Theory leads to prediction. Without prediction, experience and examples teach nothing."
- **Do** — run the experiment on a small scale.
- **Study** — compare actual results to the prediction. "Management is prediction." Failed prediction means revising the theory.
- **Act** — adopt the change, abandon it, or run another cycle.

Deming **rejected** "Check" and substituted **"Study"** because (per the Deming Institute) study is closer to Shewhart's intent. Check focuses on plan success/failure; Study focuses on "predicting the results of an improvement effort, studying the actual results, and comparing them to possibly revise the theory." PDSA is **a learning cycle, not an audit cycle**: "spirals of increasing knowledge of the system that converge on the ultimate goal, each cycle closer than the previous."

### 3.2 What the descendants kept

The Compound Atelier's canonical loop is **Plan → Work → Review → Compound**. This is structurally identical to Plan → Do → Check → Act:

| Deming (PDCA) | Compound Engineering | Function |
|---|---|---|
| Plan | Plan | Theory + prediction of what will improve |
| Do | Work | Small-scale execution |
| Check | Review | Compare actual to expected |
| Act | Compound | Adopt, abandon, or feed forward |

The Foundry (Arch 3) is also PDCA-shaped — the gate-review-and-feedback structure is the same. The Refinery's revelation cycle is PDCA applied to a *spec* rather than a *change*. The Tournament's generation-fitness-feedback loop is PDCA at population scale.

### 3.3 What the descendants dropped

- **The PDSA "Study" upgrade.** Compound engineering's "Review" is closer to Shewhart's Check (audit) than to Deming's post-1990 Study (theory-test). Review-as-practiced asks "does the work meet the bar?"; Study asks "was the theory that motivated the Plan borne out?"
- **Prediction as a planning artifact.** None of the four architectures require the Planner to state a falsifiable prediction. They state intent and acceptance criteria. Without prediction, the cycle certifies the worker but cannot teach the planner.
- **Theory-laden iteration.** Arch 2's knowledge store accretes *findings*, not *theories revised by prediction failures*. There is no structured place where the Strategist records "I predicted X; after 20 cycles, X held / failed."
- **Small-batch experimentation.** Deming's "Do" is *small scale*. The Foundry runs full phases; the Atelier runs a full issue. The Refinery's probe-then-amend is the closest fit — essentially PDSA applied to spec evolution.

### 3.4 Practical guidance not yet incorporated

- **Predictions as required Plan fields**, checked explicitly at Review/Compound.
- **Adopt "Study," not "Review,"** or require Review to include "Did the prediction hold?"
- **Theory log** separate from the knowledge store: bets the team is on, with prediction and data accumulating for/against. Defunct theories retired explicitly.
- **Pilot discipline for methodology changes.** Before a new persona / skill / phase becomes standard, run one cycle with explicit prediction. Meta-PDSA: the methodology improves itself by Deming's own discipline.

---

## 4. Cross-ancestor synthesis

All three ancestors share a **prediction-versus-outcome** spine: Kaner predicts stakeholder-credible behavior, Rumelt predicts a diagnosis-fitting policy will overcome a challenge, Deming predicts a theory-driven change improves a system. The architectures keep the cycle shape but soften the predictive demand — they evaluate *artifacts*, not *predictions about artifacts*. Strongest single upgrade: every plan states a falsifiable prediction; every review tests it.

All three also share **naming what you will not do**: Kaner names what scenario testing misses; Rumelt names non-goals and bad-strategy hallmarks; Deming names Check-as-audit as the failure mode of his own original framing. Only Arch 2 inherits this explicitly. A uniform "what we are deliberately not doing this cycle" section in every plan is cheap and high-leverage.

The third shared move is **interview-driven seeding** — Kaner from stakeholders, Rumelt from the diagnosis-conversation with the situation, Deming from the gemba. None of our architectures formalize *seed-from-conversation-with-the-world*. The seed comes from the human Strategist's existing mental model. Deepest unincorporated discipline: scheduled, structured contact with the system-as-it-actually-is, before the cycle begins.

---

## 5. Sources and status

- **Kaner, *An Introduction to Scenario Testing* (June 2003)** — primary PDF blocked (403); content reconstructed from WebSearch snippets and Wikipedia *Scenario testing* (also blocked but widely quoted). High confidence in the five characteristics, soap-opera connection, and limits passage.
- **Rumelt, *Good Strategy / Bad Strategy* (Crown, 2011)** — book-only; primary site blocked. Kernel and bad-strategy hallmarks confirmed across multiple summaries with quoted passages; proximate-objective and crux quotes corroborated against multiple summaries.
- **Deming, PDCA → PDSA** — Deming Institute pages blocked (403); content reconstructed from WebSearch snippets quoting deming.org. "Check vs Study," "Management is prediction," and "Without theory there is no learning" appear verbatim in multiple secondary sources.

Blocked URLs: `kaner.com/pdfs/ScenarioIntroVer4.pdf`, `bbst.courses/.../Kaner_ScenarioIntroVer5.pdf`, `semanticscholar.org/.../Kaner`, `en.wikipedia.org/wiki/Scenario_testing`, `en.wikipedia.org/wiki/PDCA`, `deming.org/explore/pdsa/`, `lean.org/lexicon-terms/pdca/`, `goodstrategy.com`, `alexmurrell.co.uk/.../richard-rumelt-good-strategy-bad-strategy`, `desol-tech.com/buckets/An%20Introduction%20to%20Scenario%20Testing.pdf`.

Recommendation: file a `fetch-urls` issue for the Kaner Ver. 5 PDF, the Deming Institute PDSA page, and the Wikipedia PDCA article if passage-level fidelity is needed before architectural changes are made on this thread.
