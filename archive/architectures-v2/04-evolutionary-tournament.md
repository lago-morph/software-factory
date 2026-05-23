---
based-on-commit: c495dc9
based-on-date: 2026-05-10
---

# Architecture 4 — The Evolutionary Tournament
## A Software Factory Built on Population, Selection Pressure, and Lineage

**Version:** 0.2
**Status:** Draft architecture proposal
**Lineage:** Out-of-the-box. Borrows the "writing code is cheap" mindset (Willison), the parallel-coding-agent lifestyle (Willison/Cherny), satisfaction-as-judge (StrongDM), and explicit model-family diversity (Attractor's provider-aligned profiles, El Kaim's "different mind" principle), and reframes them as selection pressure on a population.
**Stance in one sentence:** *The factory does not specify the right answer; it sets up the conditions under which the right answer wins.*

---

## 0. Revision notes (v0.2)

Changes from v0.1 driven by the v2 research pass:

- **The "4-agent ceiling" reference was a v1 fabrication** and has been removed (the verbatim Lenny editorial says only "mentally exhausted by 11 a.m." — no specific count). §10 has been updated to refer to the *cognitive ceiling problem* in supervisor-mode architectures without citing a specific number.
- **Jay Taylor's DTU origin story** (HN 46931812) is new evidence for this architecture's bet that validation harnesses are the load-bearing engineering. StrongDM's DTU took roughly a year of dedicated effort (started August 2025; reimplementing in Rust by spring 2026; Slack was the hardest single SaaS to clone) — which is consistent with this architecture's stance that **scenario authorship + harness richness are the binding constraints, not population size.** If you cannot generate or maintain a strong scenario corpus, the tournament has nothing to select against.
- **DTU = Digital Twin Universe** (not "Users"). Architecture text uses generic "validation harness" / "twin" vocabulary; this terminological fix is captured for the comparison doc.
- **Attractor is "graph-structured" generically; DOT is community convention.** This architecture's tooling-profile reference to "codex-rs-aligned, claude-code-aligned, per Attractor's provider-aligned discipline" is unchanged (that discipline is in the published Attractor spec).
- **StrongDM scenarios are partially agent-generated** ("synthetic scenario curation and shaping interface") — this is *more* consistent with this architecture than v1 implied, since Predator-driven scenario generation is one of the named mechanisms.

No structural changes to the genome, generation cycle, or roles.

---

## 1. Core thesis

If writing code is genuinely cheap, the right unit of work is not "the implementation" — it is **a population of implementations**. Twenty candidate implementations of the same feature, produced from the same genome, judged against the same scenarios, by judges drawn from a different model family than the implementers, produce a *finalist gallery* the human picks from. The losers are not defects to fix; they are evolutionary dead ends to discard.

The architecture rejects two ideas that the other three architectures share:

1. **There is one right implementation.** This architecture says: there is a *distribution* of implementations that satisfy a spec, and the spec rarely uniquely determines a single implementation. Instead of pretending we can specify our way to one answer, we generate the population, score it, and let the winner emerge.

2. **Selection happens at the human review stage.** This architecture says: selection happens *throughout*. Every scenario evaluation, every adversarial probe, every diversity check is a selection event. The human's role is not to review code but to *tune the selection pressure* — to weight the fitness function, to add scenarios that are surfacing too few divergences, to inject diversity when the population is collapsing.

The slogan: **the spec is the seed; the scenarios are the climate; the judges are the predators; the population is what survives.**

This architecture is the most expensive per cycle in raw token spend, the most defensive against the Hallucination Loop, and the most natural fit for a "writing code is cheap" mindset. It is least useful in domains where the spec genuinely *does* uniquely determine the implementation (regulatory contracts, formal verification, well-understood domains) and most useful in domains where exploration matters (greenfield, uncertain requirements, contested design choices).

---

## 2. Vocabulary

The architecture uses biological language deliberately because the loop maps cleanly onto an evolutionary algorithm. Each term has a precise meaning.

- **Genome.** The seed package for a generation. Contains: a spec sketch (prose, deliberately under-specified), a scoring rubric (named fitness components and their weights), the scenario corpus reference (out-of-repo), and a diversity policy (which model families must be represented).
- **Individual / candidate.** One implementation produced from the genome by one Implementer Agent in one isolated worktree.
- **Population.** The full set of candidates in a generation. Default *N* = 8–32, depending on cost budget.
- **Generation.** One pass through commission → produce → score → select → mutate. Default duration: 2–4 hours.
- **Lineage.** The chain of generations from the original seed through the current population, with every parent recorded and every fitness score retained.
- **Fitness.** The judge's score on a candidate, decomposed into named components (correctness, robustness, simplicity, security, performance, etc.). Weighted sum is the headline number; component scores enable diagnosis.
- **Selection pressure.** The mechanism by which low-fitness candidates do not survive to the next generation. Tunable: tournament selection, top-K, fitness-proportional, etc.
- **Mutation.** A single candidate's genome is perturbed (different model, different prompt scaffold, different tooling) before next generation.
- **Crossover.** Two parent candidates' insights are blended into a new prompt for a child candidate.
- **Niche.** A cluster of candidates that solve the spec the same way. Niche collapse (one approach dominates) triggers diversity injection.
- **Predator.** An adversarial scenario or scenario class that is added specifically to penalize certain failure modes (reward hacking, brittle implementations, security vulnerabilities). Increases selection pressure on weak phenotypes.
- **Phenotype.** The observable behavior of a candidate. Same code can behave differently in different scenarios; the phenotype is what fitness measures.
- **Convergence.** The condition where the top-K candidates' fitness scores have stabilized across the last *m* generations. Tournament ends.
- **Gallery.** The final set of top-K candidates presented to the human for selection. Default K = 3.

---

## 3. Genome structure

Each genome contains five parts. The genome is version-controlled; every generation's genome is a separate artifact.

### 3.1 Spec sketch

**Deliberately under-specified prose.** Captures the problem, the externally-observable success, and the constraints — but does not prescribe an implementation. Roughly equivalent to a Layer-1 + Layer-2 spec from Architecture 1, written sparsely.

The under-specification is by design. A fully-specified spec collapses the population's diversity (every candidate ends up similar). The right level of specification is "enough that all candidates are *trying to solve the same problem* but room for them to make different choices."

### 3.2 Scoring rubric

A weighted vector of fitness components with explicit weights:

```yaml
fitness:
  scenario_pass_rate:        0.45  # primary correctness signal
  scenario_satisfaction:     0.20  # probabilistic LLM-judge score on near-pass scenarios
  code_simplicity:           0.10  # automated complexity metrics
  security_audit_score:      0.10  # adversarial security probes
  resource_cost_efficiency:  0.05  # compute/memory/token efficiency at runtime
  robustness_under_chaos:    0.05  # behavior when inputs are perturbed
  test_coverage:             0.05  # against held-out unit-level scenarios
```

Weights are mutable across generations — the human's primary tuning lever. If round 3 produces winners with great correctness but unmaintainable code, raise `code_simplicity`'s weight for round 4.

### 3.3 Scenario corpus reference

A *path* to the held-out scenario corpus (kept outside the construction tree). Implementers see only the scenario *interface* (input shape, expected externally-observable behavior types) — not the actual scenario instances. Judges see the full corpus. This preserves the holdout property.

### 3.4 Diversity policy

Explicit constraints on the population's composition:

- **Model families:** ≥3 distinct families per generation (e.g., Claude / GPT / Gemini / Llama / DeepSeek).
- **Prompt scaffolds:** ≥4 distinct top-level prompt templates (e.g., test-driven, design-first, refactor-from-skeleton, sketch-then-iterate).
- **Tooling profiles:** ≥2 distinct tool sets (e.g., codex-rs-aligned, claude-code-aligned, per Attractor's provider-aligned discipline).
- **Maximum lineage concentration:** no single ancestral lineage may produce >40% of a generation's candidates after generation 3.

The diversity policy is enforced at population assembly time. If the genome cannot satisfy it (e.g., the API for one model family is down), the generation is delayed or runs at reduced size with the policy violation logged.

### 3.5 Termination criteria

- **Maximum generations.** Default 8.
- **Convergence detection.** If the top-K fitness scores have not improved by ≥*ε* over the last *m* generations, terminate.
- **Budget exhaustion.** Hard token-spend ceiling.
- **Operator early termination.** The human can call the tournament at any point.

---

## 4. The generation cycle

Each generation runs five phases.

### Phase 1 — Population commission

The Conductor reads the genome, instantiates *N* Implementer Agents satisfying the diversity policy, allocates worktrees, and dispatches them in parallel.

For generations 2+, candidates are commissioned with one of three lineage strategies:

- **Mutation:** parent's worktree state is the starting point; the Implementer is given a different model + a hint about what the parent's weakest fitness component was.
- **Crossover:** two parents' worktrees are summarized and presented as inspiration; the Implementer must produce a new candidate that addresses both parents' weak components.
- **Fresh from genome:** start over with no parental context. Used for diversity injection when the population is concentrating.

### Phase 2 — Production

Each Implementer runs to completion in its worktree (sandboxed; capability-scoped per the genome). Production is bounded by per-candidate budgets (tokens, wall time). Failed candidates (ran out of budget, crashed, produced no output) are recorded with cause and excluded from selection.

### Phase 3 — Scoring

Each surviving candidate is scored by:

- **Primary judge** (LLM, different model family from the candidate's implementer) running scenarios from the held-out corpus.
- **Secondary judges** (specialized: security probe, simplicity analyzer, performance benchmark, etc.).
- **Adversarial judge (predator):** a separate agent whose explicit job is to find failure scenarios this candidate handles poorly. Generates new scenarios on the fly aimed at this candidate's apparent weakness.

The fitness vector is a weighted combination of all judge outputs. Each candidate's full vector is preserved (not just the headline number) so the human can see the *shape* of why a candidate scored.

### Phase 4 — Selection

Selection rule is part of the genome. Default: **tournament selection** — repeatedly pick *t* random candidates, keep the best of the *t*, until *K* survivors remain. Tournament size *t* tunes pressure (higher *t* = stronger pressure = faster convergence but lower diversity).

The architecture also records candidates that did not survive but had unusually high scores in *one* fitness component. These become **donors** — their genome is harvested for crossover use even though the whole candidate is discarded.

### Phase 5 — Generation close

The Conductor produces a generation summary:

- Population fitness distribution (mean, max, variance, top-K shape)
- Niche analysis (how many distinct approaches survived)
- Diversity health (model-family balance; lineage concentration)
- Convergence signal (is fitness still improving?)
- Cost telemetry (tokens, dollars, wall-time)
- Operator decisions required (any?)

The human reviews the summary. Default action: continue to next generation. Optional actions: tune scoring weights, inject scenarios (predators), terminate, hand-pick winners early.

---

## 5. The human's role

This architecture has the lightest line-by-line review of the four. The human does not read code candidates. The human does five things:

### 5.1 Author the genome

The seed of every tournament. The human writes the spec sketch (deliberately under-specified), the initial scoring rubric, the scenario corpus, and the diversity policy. This is the primary leverage point — a well-tuned genome produces a productive tournament; a badly-tuned one produces noise.

### 5.2 Tune scoring weights between generations

The most-tuned dial. If candidates are scoring high but the human knows the answers feel wrong, the scoring rubric is missing a component. Add it; reweight; run another generation. This is the architecture's analog of Channel-2 review.

### 5.3 Inject predators

When the population is converging on something the human knows is wrong (e.g., reward-hacking shortcut), the human writes a new adversarial scenario that penalizes that specific shortcut. The next generation's selection pressure includes the new predator. Old candidates that were winning suddenly lose; new winners must avoid the shortcut.

### 5.4 Pick from the gallery

At convergence, the top-K candidates are presented to the human. The human reads the **fitness vector shapes** (not the code) plus a *trajectory walkthrough* (Showboat-style markdown narrative of what each candidate did) and picks. The architecture supports picking 1, picking K (running them all in production with traffic shadowing), or picking 0 (rerunning with a tuned genome).

### 5.5 Cull the lineage retrospectively

Some lineages produce winners that, in hindsight, the human regrets. The human can mark a lineage as "do not breed from" and the genome forbids that ancestral line going forward. This is the meta-loop equivalent of refactoring decisions.

---

## 6. Roles

### 6.1 Agents

- **Genome Author Agent (optional):** assists the human in drafting the genome — proposes scenarios, suggests scoring components, recommends diversity-policy adjustments. *Never* runs unattended; always proposes for human approval. This is the only agent the human directly converses with at the genome level.
- **Conductor Agent:** schedules generations, allocates worktrees, enforces diversity policy, dispatches implementers, manages budgets, produces generation summaries.
- **Implementer Agent (one per candidate per generation):** produces a candidate from the genome (or from a parent's lineage). Sandboxed. Budget-capped. Submits to the worktree.
- **Primary Judge Agent (one per candidate):** runs the scenario corpus against the candidate; produces scenario_pass_rate and scenario_satisfaction components.
- **Secondary Judge Agents (named by fitness component):** simplicity-judge, security-judge, performance-judge, etc. Each produces one fitness component.
- **Predator Agent:** runs continuously across generations, generating new adversarial scenarios that target observed reward-hacking or brittleness in the population.
- **Lineage Tracker:** maintains the genealogical record. Records every parent-child relationship and every fitness score across generations.
- **Diversity Auditor:** monitors niche concentration; flags collapses; recommends diversity-injection actions.

### 6.2 Humans

- **Geneticist (the operator):** authors genomes, tunes scoring weights, injects predators, picks gallery winners. The role is more experimental scientist than software reviewer.
- **Strategist (optional, separate at scale):** decides which problems to run tournaments on; manages the meta-loop budget across many tournaments.

For solo operation, both are the same person. For team scale-up, multiple Geneticists run independent tournaments; the Strategist coordinates which problems to fund.

### 6.3 Independence policy

This architecture is the strictest on agent independence:

- **Implementer ≠ any Judge.** Different model family, by genome policy.
- **Primary Judge ≠ Secondary Judge.** Different model family.
- **Predator ≠ any other agent in this generation.** Different model family.
- **Genome Author Agent ≠ any Implementer.** (The Genome Author might know which scenarios are in the corpus; an Implementer that shared its model could be expected to game them.)

The diversity policy is the structural defense against the Hallucination Loop (F1).

---

## 7. Loops within loops

Three timescales operate concurrently.

### 7.1 The generation loop (hours)

One full pass through commission → produce → score → select. Budget-bounded. The unit of "the tournament makes progress."

### 7.2 The tournament loop (days)

A full sequence of generations from initial commission to gallery. Ends at convergence, max generations, or budget exhaustion. Produces one set of finalists. Equivalent to a "sprint" in Agile vocabulary, but with a clearly defined termination criterion.

### 7.3 The meta-loop (weeks-months)

Across many tournaments, patterns emerge. Some genomes reliably produce useful winners; some always converge on degenerate solutions. The human and the **Lineage Tracker** review aggregate data: which scoring rubric components correlate with downstream production success, which scenario classes catch the most reward hacking, which model-family pairings produce the most diverse populations. This loop tunes the *defaults* of new genomes.

The meta-loop is the architecture's compounding mechanism. Compound engineering's `docs/solutions/` becomes the **genome library** here: a stable of well-tuned genomes for problem classes the team has seen before, with annotations of what worked and what didn't. New tournaments reuse genome templates; the templates evolve.

---

## 8. Defenses against the 20 failure modes

| Failure | Defense in this architecture |
|---|---|
| F1 Hallucination Loop | Structurally defeated by the diversity policy: implementer model family ≠ judge model family ≠ predator model family. Fixed by genome, not optional |
| F2 Reward hacking | Predator agent generates adversarial scenarios specifically targeting observed shortcuts; held-out scenario corpus prevents memorization; fitness rewards diversity, penalizing collapsed approaches |
| F3 Spec-completeness | The architecture explicitly does *not* assume specs are complete; the population explores what the spec leaves underspecified |
| F4 Code-quality | Secondary judges include simplicity, maintainability, performance components; weighted in the rubric; predator probes brittleness |
| F5 Cognitive ceiling | The human reviews per-generation summaries (not per-candidate); gallery is K=3, not N=32; human-time scales sublinearly with population size |
| F6 Cognitive debt | Trajectory walkthroughs for gallery candidates; fitness vector explains *why* a candidate won |
| F7 Normalization of deviance | Predator agent continuously raises pressure on new failure classes; aggregate fitness trends track whether the population is learning around weaknesses or just gaming new metrics |
| F8 Stale-knowledge | Genome library curated in the meta-loop; old genomes pruned when their downstream production success rate decays |
| F9 Spec overfitting | Spec sketch is *deliberately* under-specified; fitness rewards diversity (niche maintenance); winners can be different shapes |
| F10 Findings disappear | Generation summary captures every Operator decision; lineage tracker preserves every score; genome history is durable |
| F11 Renumbering | Scenario IDs (S-N), generation IDs (G-N), candidate IDs (C-G-N), fitness component IDs are stable |
| F12 Lethal trifecta | Per-candidate sandboxes; capabilities scoped per genome; security-judge runs predators specifically |
| F13 Missing-config blindspot | Predator agent generates scenarios about environment/configuration; fitness includes "robustness under chaos" |
| F14 Attribution collapse | Every candidate is attributed to a model family + scaffold + lineage; the lineage tracker is the audit spine |
| F15 Single-prompt collapse | Population diversity policy prevents single-prompt convergence; minimum 4 prompt scaffolds per generation |
| F16 Resume-fidelity decay | Each candidate runs in isolation; failure of one does not corrupt others; resume = re-run that candidate |
| F17 Parallel agents on shared dirs | Strict worktree isolation per candidate; no shared state during production |
| F18 Prose-spec rigor | Replaced with **empirical rigor:** the held-out scenario corpus + scoring rubric is the contract; rigor is measured in scenario pass rate, not formal proof |
| F19 Model-floor dependency | Tournament structurally tests across model families; weakest-family candidates lose; the architecture *tracks* model-floor effects rather than depending on a single model |
| F20 Maintenance asymmetry | Maintenance cycles run new tournaments on bug-shaped genomes; production traffic feeds new scenarios into the predator's corpus |

This architecture's most distinctive coverage: F1 (Hallucination Loop), F19 (model-floor dependency), F15 (single-prompt collapse) are addressed *structurally*, not behaviorally. Diversity is a non-negotiable invariant of the genome.

---

## 9. Cost and economics

This is the **most expensive architecture per cycle in raw token spend.** A generation of *N* = 16 candidates costs ~16× the implementation cost of a single-implementation cycle. A tournament of 6 generations costs ~96× a single implementation.

What you get for the cost:

- **Empirical confidence in the implementation.** The winning candidate beat 95+ alternatives across multiple judges and predators.
- **Diverse implementation options.** The gallery shows you 3 distinct ways to solve the problem; you pick the one with the right tradeoffs for your context, not the one a single agent happened to write.
- **Aggregate signal about the spec.** If many candidates fail the same scenario, the spec or the scenario is wrong. The architecture surfaces this as a population fitness pattern.
- **Defense-in-depth against agent failures.** Reward hacking is hard when 30 candidates and 3 predators are watching. Hallucination-Loop is hard when implementations and judges live in different model families.

What you cannot get for the cost:

- **Predictable schedule.** A tournament that converges in generation 3 and one that runs to generation 8 take dramatically different amounts of time.
- **Audit trail in the regulatory sense.** Each candidate has a record, but the *decision* to ship a particular candidate from the gallery is the human's preference, not a structured V&V verdict.
- **Cheap iteration on small changes.** A 1-line bug fix should not run a tournament. The architecture knows this; small changes go through a single-implementation fast-path.

### 9.1 When this architecture is the right tool

- Greenfield work where the implementation shape is genuinely uncertain.
- Problems where multiple correct answers exist and tradeoffs need exploration.
- Adversarial domains (security, reliability) where predator-driven selection matters more than spec adherence.
- Long-running systems where the genome evolves; today's winning template seeds tomorrow's tournament.
- Organizations with budget and patience for the experimental temperament this architecture rewards.

### 9.2 When it is the wrong tool

- Regulated environments requiring structured V&V trails (use Architecture 3).
- Well-understood replication tasks where spec uniquely determines implementation.
- Time-critical bug fixes (run a single-implementation fast-path; don't run a tournament).
- Domains where scenario authorship is the bottleneck (the Geneticist's effort goes into scenarios; if scenarios are already exhausted, the tournament has nothing to select against).

---

## 10. Scaling

For solo operation, this architecture scales naturally. The Geneticist runs one tournament at a time; the population is the parallelism, not the human's calendar. The cognitive-ceiling problem that bites supervisor-style architectures (Simon Willison reports being "mentally exhausted by 11 a.m." running parallel agents in supervise-mode) doesn't apply here because the human isn't supervising candidates — the human is *tuning the conditions under which candidates compete*. The human reviews per-generation summaries and finalist galleries; the population's size is bounded by token budget, not by attention.

For team scale-up, multiple Geneticists run independent tournaments. The genome library is the shared asset; the Strategist coordinates which problems to fund. Cross-team coordination happens at genome-template-share-time, not at per-implementation-review-time.

The biggest scaling risk is **genome library bit rot.** Genomes stale; scenarios become outdated; predators become irrelevant. Without curation discipline (analogous to Architecture 2's `compound-refresh`), the genome library inverts from asset to liability. The architecture mandates a genome-curation cadence (default monthly).

---

## 11. Implementation roadmap

**Stage 1 — Single-generation tournament.** Run one generation of *N* = 4 candidates from one hand-written genome. No mutation, no crossover, no predator. Select top-1; ship. Goal: validate that diversity-of-implementation produces meaningful options.

**Stage 2 — Multi-generation, no mutation.** Run 4–6 generations with selection but no inter-generation context. Goal: validate that selection pressure converges; observe convergence rate.

**Stage 3 — Add mutation + lineage tracking.** Generations 2+ start from parents. Goal: verify mutation produces measurable improvement on weak fitness components.

**Stage 4 — Add crossover + diversity audit.** Lineage Tracker monitors niche concentration; Conductor injects fresh-from-genome candidates when concentration exceeds threshold. Goal: maintain diversity across generations.

**Stage 5 — Add predator agent.** Adversarial scenario generation begins. Goal: catch reward-hacking patterns before convergence.

**Stage 6 — Genome library + meta-loop.** Begin reusing genome templates across tournaments; monthly curation. Goal: tournament *n+1* on a similar problem is meaningfully cheaper than tournament *n*.

**Stage 7 — Multi-tournament parallel ops.** Run 2–4 tournaments simultaneously; budget allocation across them; Strategist coordination. Goal: scale without losing per-tournament quality.

Each stage runs ≥3 tournaments before advancing. The architecture rewards organizations willing to invest in scenario corpora and predator discipline; it punishes those that under-invest in the held-out scenario set.

---

## 12. What this architecture is not

- **Not a single-pass code generator.** Multi-generation tournaments are the unit of work.
- **Not free.** Token spend per shipped feature is high; the bet is that quality and confidence justify it.
- **Not deterministic.** The same genome run twice produces different finalist galleries. The architecture embraces this; reproducibility is at the *quality distribution* level, not the implementation level.
- **Not a replacement for spec authorship.** The genome's spec sketch is small but load-bearing. A bad sketch produces a bad tournament.
- **Not the right tool for everything.** Section 9.2 enumerates when not to use it.
- **Not a true genetic algorithm.** It is *inspired* by evolutionary computation but uses LLM agents as both reproductive units and judges. The biology metaphor is structural, not mechanical — there is no DNA-like representation, no actual mutation operators on a code-string level, no Schema theorem invocation.

---

## 13. Open questions

1. **Optimal population size.** *N* = 8? 16? 32? Depends on problem complexity, scenario corpus richness, and budget. The architecture surfaces this as a tunable; no clear default.
2. **Convergence detection sensitivity.** When is fitness "stable enough"? Too sensitive: terminate before exploring; too lax: burn budget on irrelevant generations. ε and *m* are heuristic.
3. **Cross-tournament knowledge.** Genome templates capture problem-class wisdom. Can fitness component definitions transfer? Can predators trained on one problem help on another? Open.
4. **Model-family diversity at small fleets.** With ≤3 model families available, the diversity policy is hard to satisfy at *N* = 16. Architecture currently requires 3 distinct families; empirically may need to relax for some setups.
5. **Predator overpressure.** A predator that gets too good at finding adversarial scenarios may produce an evolutionary plateau where no candidate can ever win enough. Tuning the predator's aggressiveness is open.
6. **Niche preservation.** Selecting purely on top-K fitness collapses niches. The architecture mentions niche analysis but doesn't formalize a niche-preserving selection rule (compare: NEAT's speciation in evolutionary algorithms). Worth incorporating.
7. **Gallery-to-deployment translation.** When the human picks a gallery winner, how is it integrated into the rest of the codebase? Each candidate is in its own worktree; merging the winner is a separate, currently unspecified, step.
8. **The genome itself as evolvable.** Should the meta-loop allow tournaments where the *genome*, not the implementation, is the evolved unit? (E.g., the rubric weights, scenario corpus, and diversity policy of a genome are themselves selected against downstream production success.) The architecture hints at this but does not commit to it.
9. **Disagreement among judges.** Two judges score the same candidate differently. Resolution: weighted average. Loss: signal that the spec is ambiguous in a way that even judges disagree on. The architecture currently averages; surfacing the disagreement would be valuable.
10. **Interaction with the other architectures.** Could a Foundry phase 4 run a small tournament rather than a single Implementer? Could a Compound Atelier persona panel review the gallery? Hybrid options are unexplored.

---

*End of architecture spec — Evolutionary Tournament v0.1*
