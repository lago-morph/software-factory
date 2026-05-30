# v4 architecture — ambiguities and gaps (adversarial review)

Adversarial review of the four v4 docs: `README.md`, `AI-CONTEXT.md`, `F-MODE-COVERAGE.md`, `one-shot-specs-and-research.md`. Each finding has a stable ID, a one-line statement, location, and severity (blocker | major | minor).

Severity key: **blocker** = will produce a wrong or unbuildable artifact if specced as-is; **major** = real gap a spec author must resolve before building; **minor** = polish / clarity / hygiene.

---

## Contradictions

- **G01** — *(major)* "Three-layer architecture" vs Layer 0-6 numbering: P2 names exactly **three layers + persistence** (README Part 3; AI-CONTEXT §2), but the same docs everywhere use a **Layer 0 through Layer 6** scheme (AI-CONTEXT §6 "Layer 2-6 coverage", README Part 6 "Layer 2", "Layer 5", "Layer 6"). The two "layer" vocabularies are never reconciled, so "Layer 2" is ambiguous (the agent-loop tier? the scenarios/judge tier?). Two different meanings of the word "layer" run through the whole corpus.

- **G02** — *(major)* Phase count vs phase references: README Part 6 says "**Four-phase plan**" and the diagram shows P0→P1→P2→P3+. But the same line says "you don't wait for **Phase 6** to get value" (README:342), and Part 6 header / Part 1 bullet describe phases as P0, P1, P2, P3+. There is no Phase 4/5/6. "Phase" and "Layer" are conflated; a reader cannot tell whether "Phase 6" is a typo for "Layer 6" or a missing phase.

- **G03** — *(major)* Principle count "6 of 12 native" is internally unsupported. AI-CONTEXT §11.1 states "Smallest viable install handles **6 of 12** principles natively"; AI-CONTEXT §3.6 lists "P1, P2, P3, P4, P9, P10 native" = 6. But the §3.1 coverage map rates P3 as "**Strong when `[formulas]` enabled**" and Phase 0 explicitly turns `[formulas]` **off** (§3.4, README Phase 0). So at the *smallest* install P3 is **not** delivered (README Phase 0 itself says "full when formulas turn on in Phase 1"). The native count at Phase 0 is 5, not 6 — the headline claim double-counts P3.

- **G04** — *(minor)* CXDB vs OTel framing tension. AI-CONTEXT §5.2 stresses CXDB has "**no native OTLP receiver**" and is positioned *against* OTel, yet Phase 1 (README:386-389) routes Claude Code OTLP → OTel Collector → LangFuse **and** raw-bodies → CXDB in parallel. This is consistent but never stated as "two separate sinks"; a naive reader may try to wire OTel→CXDB, the explicitly-rejected path (AI-CONTEXT §11.3).

- **G05** — *(minor)* "10 candidate methodologies" (README Part 1) vs "v3's **ten** candidates" vs "GF-M (the cheapest candidate)" — README:512 calls GF-M "the cheapest", §553 calls it "smallest custom-pack scope", AI-CONTEXT §11.2 says "likely GF-M". Cheapest, smallest-scope, and "likely" are three different commitments to the same choice; the actual selection criterion is never pinned.

## Undefined terms

- **G06** — *(major)* "**Gas City placement**", "**pack**", "**formula**", "**bead**", "**rig**", "**molecule**", "**sling**", "**convoy**", "**wisp**", "**Order**", "**Health Patrol**", "**convergence gate**", "**model stylesheet**" are used as load-bearing throughout README Part 4 before AI-CONTEXT §3.2/§3.3 defines a subset. README is the human-facing doc and uses ~10 Gas City terms with no inline glossary; the vocabulary table lives only in the companion. A spec author reading README alone cannot resolve them.

- **G07** — *(major)* "**Gene transfusion**" is the core Phase 3+ mechanic but is defined only by analogy (AI-CONTEXT §9: "pointing the agent at a concrete exemplar and asking it to reproduce the behavior"). There is no acceptance criterion for *when a transfusion is correct/complete*, no contract for what "behaves like the exemplar" means operationally, and no handling for exemplars under incompatible licenses. The whole factory-builds-factory plan rests on an undefined success predicate.

- **G08** — *(major)* "**Cross-family enforcement**" / "judge must be a different model family than coder" (P6; F1/F27/F46/F48). "Model family" is never defined. Are two Anthropic models different families? Is Claude-judge vs Claude-coder allowed? Since the only sanctioned coder is Claude Code under Max (P2, F31), an independent-*family* judge implies a **second provider/API key** that AI-CONTEXT §4.1 says Max does not issue. The enforcement rule and the single-adapter floor are in direct tension (see G20).

- **G09** — *(minor)* "**Satisfaction**" vs "satisfaction threshold" vs "time-to-threshold" (P6, P12 meta-metrics) — the satisfaction *metric* is described as "a distribution over trajectory population" but no threshold semantics, no pass/fail cutline, and no definition of "satisfied" is given. F40/F47 reference thresholds that are never defined.

- **G10** — *(minor)* "**Held-out**" / "read-isolation" — P5 says the agent "cannot see" scenarios, but the enforcement is "file permissions + agent-prompt **discipline** + audit logging" (README:177). "Discipline" is not enforcement; the term "held-out" implies a guarantee the mechanism doesn't provide (see G21).

## Unstated assumptions

- **G11** — *(blocker)* The entire plan assumes **Gas City exists, is obtainable, and works as described**. README §552 admits "Gas City is the load-bearing third-party dependency. If Gas City fails, the whole plan reorganizes." Yet there is no evidence any author has run `gc`, no version pin, and the repo URL (`github.com/gastownhall/gascity`, AI-CONTEXT §15.1) is asserted, not verified. Every "Native" cell in README Part 4 is an unverified assumption about a third-party tool's behavior.

- **G12** — *(major)* Assumes **Claude Code subprocess automation under Max is and stays permitted** for unattended L4/L5 operation. AI-CONTEXT §4.1 asserts "officially supported" but the cited basis is a support-article URL; §14 risk register rates "Claude Code Max policy changes" as Low/High with mitigation "have API-key fallback ready" — but the API-key fallback contradicts §4.1 ("No separate API key issued" under Max). The fallback path is named but not designed.

- **G13** — *(major)* Assumes the factory can run **thousands of scenarios/hour** (P7 rationale) under a **$200/month Max subscription** (AI-CONTEXT §4.1). Max has rate limits and usage caps; running held-out scenario suites + multi-judge ensembles + A/B variant replays at L5 volume against a single Max seat is a cost/throughput assumption that is never reconciled with the subscription model. No token-budget math anywhere.

- **G14** — *(major)* Assumes **gene transfusion is reliable for bounded components** (explicitly a "bet", README:511) — yet Phases 3b/3c/3d (the Healer, twins, self-optimizer) are *all* gated on this bet, and they are the highest-value, highest-risk components. If the bet is wrong, ~half the principles (P7, P8, P11, P12) have no delivery path. The plan has no fallback for "factory cannot reliably transfuse."

- **G15** — *(minor)* Assumes **one operator can author specs fast enough** to feed an L4/L5 factory. F-MODE-COVERAGE F25 (design starvation) flags this as "by construction" and the guard is "honest staffing / document it" — i.e., the docs concede the bottleneck but offer no design response.

- **G16** — *(minor)* Assumes **the 12 principles are the right set** (README:508, the first "bet"). Substituting self-optimization (P12) for El Kaim's "pipeline files worth sharing" is asserted as "natural extension" with no argument for why community-sharing can be dropped from a *factory* definition.

## Missing / underspecified pieces

- **G17** — *(blocker)* **No schema for any of the core stores.** Beads are referenced with types (`override`, `fix_task`, `factory_build_in_progress`, `factory_build`) across README and AI-CONTEXT §16, but no bead schema is given. CXDB's "turn" model is described (AI-CONTEXT §5.3) but the v4-specific type bundle (`{bundle_id, type, version}`) that v4 must register is never specified. AI-CONTEXT §16 tells a cold agent to run `gc bd find --type factory_build_in_progress` — a type the schema docs never define.

- **G18** — *(blocker)* **Self-healing loop has no termination / no loop-closure contract.** P11 lists "Loop closure tracking — did the fix actually fix it? (custom, small)" but there is no spec for: how many fix attempts before escalation, what happens when the Healer's fix *creates* a new anomaly (oscillation), or who authorizes a Healer-generated fix to ship at L5. "Observability → anomaly → diagnosis → fix → ship, without human intervention" (README:246) is a loop with no stated bound — the exact F52 "more controller patches" trap the docs warn about (F-MODE-COVERAGE §8).

- **G19** — *(major)* **The counterfactual-replay driver (P12) is admitted unsolved.** AI-CONTEXT §12: "no good exemplar; design problem largely unsolved"; README:470 calls it "your most significant invention." This is named as the single hardest invention and has zero interface, zero contract, zero acceptance scenario — yet P12 is counted in the "12 principles delivered" framing.

- **G20** — *(major)* **The judge model is unsourced.** Cross-family judging (G08) requires a non-Claude model, but every model-provider decision in the docs is "Claude Code under Max" with "no API key." There is no named judge provider, no judge budget, no judge auth path. P6 cannot be built as specified without resolving where the second model family comes from.

- **G21** — *(major)* **Holdout-integrity enforcement has no real mechanism.** P5's "read-isolation" is filesystem permissions + rig `read_partition` config (AI-CONTEXT §13.3) + "agent-prompt discipline." But the implementer agent runs as a Claude Code subprocess with broad tool access (Bash, Read); nothing in the docs prevents it from reading outside its declared partition. The "Holdout integrity audit" is *detection after the fact*, not prevention. F28 ("Holdout leakage") is marked **Addressed** on the strength of a mechanism that is detect-only.

- **G22** — *(major)* **Digital-twin fidelity has no acceptance contract.** P7 / Layer 5 is "the most labor-intensive principle," "no turnkey OSS," "build per-dependency." "Behavioral fidelity testing: None turnkey / DIY / Manual diff tooling" (AI-CONTEXT §7 Layer 5). There is no definition of *how close is close enough* for a twin, yet F12/F33/F44/F56 are all marked **Addressed** on the basis of twins that don't yet exist and have no fidelity bar.

- **G23** — *(major)* **Bootstrap-validation success criteria are subjective.** Phase 2's pivotal milestone is "Human review the output / Deploy if it works" (README:434). "If it works" is the make-or-break gate for the entire factory-builds-factory thesis and it has no rubric, no scenario set for the bootstrap component itself, no pass bar. The most consequential checkpoint in the plan is "looks good to a human."

- **G24** — *(minor)* **Formula↔DOT bidirectional translator** is described as "few hundred lines" but TOML formulas and DOT graphs have different expressive power (TOML sections-as-flags, AI-CONTEXT §3.2 concept 4, vs DOT's arbitrary edge attributes). Lossless bidirectionality across two unequal formats is asserted, not shown; round-trip fidelity is unaddressed.

- **G25** — *(minor)* **Inspect AI session-id vs Gas City session-id adapter** is listed as an open question (AI-CONTEXT §12, §13 implies it) — "likely needs adapter layer; impedance unknown" — but Phase 2 depends on it and no adapter is scoped.

## Boundary ambiguities

- **G26** — *(major)* **Raw-bodies → CXDB bridge seam.** The bridge "watches the `OTEL_LOG_RAW_API_BODIES` directory and posts to CXDB HTTP API" (README:389). Undefined at the seam: ordering/at-least-once vs exactly-once delivery, what happens to partially-written body files, back-pressure when CXDB is down, and how `session.id` maps to CXDB's parent-turn pointer (AI-CONTEXT §5.4 says "parent-chain via session.id" but the mapping rule is not given). This is "the first non-trivial integration; budget a week" (README:541) with the hard parts unspecified.

- **G27** — *(major)* **Gas City event bus ↔ CXDB.** AI-CONTEXT §5.4 ranks "Gas City event bus JSONL → CXDB" as **lowest impedance / best**, but §11.1 and README both then choose the **raw-API-bodies** path (ranked #2). The decision table recommends one path and the build chooses another with no stated reason for overriding the ranking.

- **G28** — *(major)* **Scenario storage seam: "separate git repo" + "rig partition" + "OPA later".** Three mechanisms (git repo separation, filesystem permissions, Gas City rig `read_partition`, plus OPA "for finer control later") are named for one boundary with no statement of which is authoritative or how they compose. README:171 and AI-CONTEXT §13.3 give partially different mechanism lists for the same isolation requirement.

- **G29** — *(minor)* **Pack ↔ Go-library boundary.** The docs repeatedly insist v4 needs no Go imports because "packs cover all extension needs" (README:334, §509, §518; AI-CONTEXT §3.5, §10.1, §11.1, §11.3, §14). But "tool node binaries" in packs are themselves Go programs that must speak Gas City's tool-node protocol — that protocol/ABI is never specified. The pack/runtime contract (how a subprocess tool node receives inputs and returns outputs) is the actual seam and is undocumented.

- **G30** — *(minor)* **Diagnosis agent ↔ Tracker transfusion seam.** P11's diagnosis agent transfuses from "Tracker's `Diagnose`/`Audit`/`Doctor` programmatic APIs," but Tracker is wrapped by Mammoth and its license is **unverified** (README:292, AI-CONTEXT §12). If Tracker is non-permissive, the strongest Layer-4 exemplar is unusable for code transfusion (only pattern transfusion) — the boundary between "transfuse the code" and "reimplement the pattern" is left to chance.

## Cross-cutting risks (scale / failure / security / cost)

- **G31** — *(blocker)* **Security: lethal trifecta is marked "Addressed" but the addressing mechanism (twins) is unbuilt and last.** F12/F44/F56 depend on twins (Phase 3c) and deterministic boundary typing (P4), yet from Phase 0 through Phase 3b the factory runs Claude Code with Bash/network/filesystem access and **no twin isolation**. The most dangerous security failure class is "Addressed" on paper for the entire period it is actually exposed.

- **G32** — *(major)* **Cost is essentially unmodeled.** The only cost figure in the corpus is "$200/month Max" (AI-CONTEXT §4.1). P12's headline meta-metric is "cost-per-satisfaction" (README:269) yet there is no cost model for: scenario-suite runs, multi-judge ensembles, A/B variant replays, embedding all trajectories (sentence-transformers), or the second-family judge tokens. "Cost amortizes across methodologies" (README:512) is asserted without a single number.

- **G33** — *(major)* **Failure: no story for partial/cascading failure of the OSS stack.** Phase 1+ adds OTel Collector, LangFuse, CXDB, Inspect AI, Temporal, plus Python tool nodes (PyOD, sentence-transformers, HDBSCAN, DSPy, Optuna, scipy). What happens when CXDB is down mid-run? When LangFuse loses traces? When a Python tool node OOMs? No degradation/retry/circuit-breaker design exists; "Gas City Orders survive crashes" is claimed for Gas City only.

- **G34** — *(major)* **Scale: the single-Max-seat throughput ceiling.** P7's entire justification is "scenarios run thousands per hour without rate limits" — but the *coder/judge* still hit Max rate limits even when the twinned *dependency* doesn't. The rate-limit relief is on the wrong side of the boundary; the agent-side throughput ceiling under one Max subscription is never addressed.

- **G35** — *(major)* **Security: RSI / goal-subversion is the weakest acknowledged mechanism, on a self-modifying factory.** F-MODE-COVERAGE §11 lists F54 (goal subversion over cycles) among "weakest matches," guard = "audit pack" (a Phase 3+ recommendation, not built). A factory that builds and deploys its own components (P11 fix-tasks auto-ship at L5) with the *weakest* control on objective drift is a structural risk the docs note but do not resolve.

- **G36** — *(minor)* **Attribution integrity is optional/deferred.** P9 ("strongest match") relies on `created_by` flowing through beads — but "Identity verification — verify claimed actor matches actual" is "optional, deferred" (README:229). Without signed provenance, attribution is *self-asserted*; F32 (mail-injection) is marked **Addressed** via "**optional** HMAC signing." An optional guard does not address a security failure.

- **G37** — *(minor)* **Secret/credential handling is absent.** OAuth tokens (Max), CXDB endpoints, LangFuse, OTel mTLS certs, and the (required-but-undefined) judge provider credentials all appear in `city.toml`/env (AI-CONTEXT §13.2) with no secrets-management story. `env = { ... }` in TOML implies plaintext secrets in version-controlled config.

## Cross-reference / count inconsistencies

- **G38** — *(major)* **F15 is missing entirely from the 61-mode coverage.** F-MODE-COVERAGE claims to map "each of the 61 catalogued failure modes (F1-F61)" but only **60 distinct F-numbers** appear in any table row; **F15 is absent** (no row in any of §1-§9). A doc whose stated purpose is exhaustive coverage silently drops one mode.

- **G39** — *(major)* **Summary status counts don't reconcile with the table rows.** §10 summary: Addressed 24, Partial 20, Gap 11, Caution 4 (= 59, not 61; +10 "overlap" Phase-3 row). But the actual rows contain **30 cells reading "Addressed"** and **18 reading "Partial"** before dedup. The discrepancy is partly explained by F32/F35/F47 each appearing **twice** (see G40) and §7 being flagged "overlap," but the arithmetic is never shown and 24+20+11+4 = 59 ≠ 61. The headline "39% / 33% / 18% / 7%" percentages are computed against an unreconciled base.

- **G40** — *(major)* **F32, F35, F47 are each double-counted across sections** with conflicting status. F32: §2 "Addressed" and §7 "Addressed" (two different mechanisms). F35: §6/§7 row "Partial" **and** §8 Caution. F47: §5 "Partial" **and** §8 Caution. A mode listed as both "Partial/Addressed" and "Caution" has no single status — the summary table cannot be derived deterministically from the rows.

- **G41** — *(minor)* **F32 listed under two different layer owners.** §2 (Layer 3, P8/observability) and §7 (Phase 3+ gene-transfusion). Same failure mode, two homes, two mechanisms (P9 attribution + "optional HMAC" vs "HMAC signing on mail bus") — the canonical owner is ambiguous.

- **G42** — *(minor)* **"~72% have some mechanism" vs the component counts.** §10 net claim "~72% addressed or partial" = (24+20)/61 = 72%. But if Gap=11 and the three double-counted modes resolve to a single status each, the denominator/numerator shift. The summary percentage is presented as precise ("~72%", "39%") atop counts that don't sum to 61.

- **G43** — *(minor)* **Principle-coverage table (AI-CONTEXT §3.1) vs delivered-in-Phase-0 list (README) disagree on P3 and P8.** §3.1 rates P8 "Weak (convergence gates partially impose)"; README Phase 0 "What's delivered" omits P8 entirely; F-MODE-COVERAGE leans on P8 for F10. The P8 maturity claim varies by document.

- **G44** — *(minor)* **El Kaim "10 of 11" arithmetic.** AI-CONTEXT §1: "10 of 11 originally from El Kaim"; original P12 ("pipeline files worth sharing") deferred; self-optimization added as 12th. So the working set is 11 original-minus-1 (=10) + 1 new = 11, not 12 — unless one El Kaim principle was split. The "12 working principles" count is asserted but the +1/-1 bookkeeping yields 11 unless something is uncounted. (Header says "10 of 11"; table lists 12 rows; the missing reconciliation is the El Kaim P11↔P12 boundary.)

- **G45** — *(minor)* **`one-shot-specs-and-research.md` is orphaned.** It is one of the four v4 docs but is never referenced by README, AI-CONTEXT, or F-MODE-COVERAGE, and AI-CONTEXT §0 says "Primary outputs: this file + README.md" (excluding it). Its relationship to the architecture (input research? appendix? the basis for Phase 2 spec authoring?) is undeclared — a doc in the architecture set with no stated role.

---

*Review date: 2026-05-30. 45 findings: 5 blocker, 22 major, 18 minor.*
