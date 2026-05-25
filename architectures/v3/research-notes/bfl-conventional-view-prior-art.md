# BF-L conventional-view prior-art research notes

**Charter.** Phase-4.4 research dispatch per [auto-003 option A](../decisions/auto-003-bfl-rg-view-choice.md). Catalogues prior art and active work on machine-extracted code convention catalogues, feeding (i) the BF-L conventional-view sub-track design, (ii) Phase-5 BF-L ADRs alternatives-considered, (iii) Phase-8 lean-eval pressure-test design. The target artifact in the [P-26 Codebase Model sketch](../primitives/P-26-codebase-model.md) is a Pydantic-typed `Convention { name, pattern, scope, evidence-symbols, confidence }` covering idiom register, naming conventions, layering rules, and test patterns, deduplicated and voted across a cross-family judge ensemble.

**Scope note.** This document covers the *conventional* view only. The *invariant* view's parallel research dispatch lives in `bfl-invariant-view-prior-art.md`. Citations are author + year + title with arXiv ID/DOI where confidently known. Where I'm not sure a tool/paper exists at the claimed granularity, I flag it inline rather than fabricate.

---

## §1 Industry tools

The industry surface is *broad on style* and *narrow on convention*. Tools concentrate on what is mechanically checkable; the long tail of "the kind of thing this codebase does" goes uncovered.

- **SonarQube / SonarLint.** Multi-language static-analysis platform. Covers ~30 languages, ships ~5000 rules across "code smells," "bugs," and "security hotspots." Rules are *authored by SonarSource*, not inferred from the codebase under test. Custom rule plugins exist but require Java + a SonarQube API. Coverage of P-26's surface: **layering rules** partial (the Sonar "architecture" rule pack is opt-in and dependency-graph based); **naming conventions** strong for the conventions Sonar pre-ships (snake_case, camelCase) but not for project-specific naming patterns; **test patterns** essentially none. What it does NOT cover: idiomatic patterns specific to a codebase (e.g., "we use `dataclasses` with `frozen=True` in `core/`"), project-local layering invariants that aren't expressible as Sonar's pre-baked architecture rules.

- **ESLint + custom-rule plugins.** JavaScript / TypeScript. ESLint's strength is AST-rule authoring: a project can ship its own rules in its own repo (`eslint-plugin-internal`). The ecosystem includes `eslint-plugin-import` (import ordering, boundary rules), `eslint-plugin-boundaries` (module-level layering), `eslint-plugin-functional` (immutability conventions), and dozens of style/idiom packs (Airbnb, Standard, XO). Coverage: **strong** on style and import-graph layering when projects author the rules; the project author still bears the cost of writing the rule. No inference — ESLint enforces what you tell it.

- **ArchUnit** (Java; ports: ArchUnitNET for .NET, PyArchUnit for Python, ts-arch for TypeScript). Tests authored as JUnit-style code that asserts dependency rules ("classes in `..domain..` may not depend on classes in `..ui..`"). Coverage of P-26's surface: **layering rules** strong, **naming conventions** partial (assertions on class-naming regex), **idiom register / test patterns** none. Same authoring-cost shape as ESLint — humans write the rules. Worth citing as the most mature "layering as code" prior art the convention extractor would compete with.

- **Spotless / Prettier / Black / gofmt / rustfmt.** Pure formatting. No convention inference; *imposes* convention. Useful as a calibration point: these are what "style as code" looks like when the community converges. They do not extract from a codebase.

- **Pyflakes / Ruff / Bandit / Pylint.** Python lint family. Ruff is the modern superset (replaces Pyflakes, flake8, isort, partial Pylint at 10-100× the speed; written in Rust by Charlie Marsh). Rules are pre-baked; project-specific conventions require either writing a plugin or extending via `# noqa`. **Bandit** specializes in security idioms. Coverage of P-26's surface: same shape as ESLint — author-supplied rules, no inference.

- **golangci-lint.** Meta-runner aggregating ~50 Go linters (govet, staticcheck, errcheck, revive, etc.). Strong coverage of *Go idioms* the community has crystallized, near-zero coverage of project-specific conventions.

- **dependency-cruiser / madge / NDepend / jdeps / pydeps.** Import-graph and dependency analysis. dependency-cruiser (JS/TS) and jQAssistant (JVM) are the most relevant — both allow expressing layering rules over a parsed dependency graph. See §5 below for the layering-specific treatment.

- **Semgrep / CodeQL.** Pattern-matching / query-over-AST tools. Semgrep (r2c, now Semgrep Inc.) lets users author patterns in a YAML-DSL that abstracts AST shape; CodeQL (GitHub) lets users query a typed code database. Both are *enforcement* tools that scale to codebase-specific patterns *if* a human writes the pattern. Semgrep ships pattern packs ("react-best-practices", "django-security"). Neither **infers** conventions from a corpus.

**What none of these cover that P-26 wants.** The convention surface P-26 describes is *inferential* — looking at the codebase and producing a typed list of "what this codebase does idiomatically." Every tool above is either pre-baked rules (Sonar, lint families) or human-authored rules per project (ESLint custom plugins, ArchUnit, Semgrep custom). None produces a `Convention { name, pattern, scope, evidence-symbols, confidence }` from inspecting a corpus. **This is the gap the BF-L sub-track is attempting to fill.**

## §2 Academic prototypes — convention inference

The academic literature is substantially more relevant than the industry tooling, but the published precision/recall numbers are on narrower sub-problems than the P-26 surface.

- **Hindle, Barr, Su, Gabel, Devanbu (2012). "On the Naturalness of Software." ICSE 2012.** The foundational paper. Argues that code corpora have low cross-entropy under n-gram language models — i.e., software is *repetitive* in ways natural language isn't, which means statistical methods that work on text work even better on code. Reported perplexity numbers on Java corpora (Eclipse, Lucene, etc.) below natural-language baselines by a substantial margin. Not directly a "convention extractor" but the empirical basis for everything downstream. DOI: 10.1109/ICSE.2012.6227135.

- **Allamanis, Sutton (2014). "Mining Idioms from Source Code." FSE 2014.** Treats idiom-mining as nonparametric Bayesian inference over tree fragments (the **HAGGIS** system). Extracts repeated tree-fragment patterns ("idioms") from Java/Python corpora. Reports qualitative idiom catalogs and a held-out cross-entropy reduction. The closest published prior art to P-26's idiom-register notion. arXiv:1404.0417. Notably: the system extracts patterns; it does not name them, classify them by scope, or rate their confidence in the way P-26 requires.

- **Allamanis, Barr, Bird, Sutton (2014). "Learning Natural Coding Conventions." FSE 2014.** The **NATURALIZE** system. Specifically targets *naming and formatting* conventions, using an n-gram model to score whether a candidate identifier/format is consistent with the rest of the codebase. Reported "convention violation" detection precision around 94% on top-1 suggestions (small held-out evaluation; Java corpora). DOI: 10.1145/2635868.2635883. *Highly relevant but narrow:* only naming + formatting, not layering or idiom register.

- **Allamanis, Barr, Devanbu, Sutton (2018). "A Survey of Machine Learning for Big Code and Naturalness." ACM Computing Surveys.** arXiv:1709.06182. The canonical survey covering naming, code completion, defect prediction, summarization, idiom mining, and convention inference through ~2017. Not a primary source but the best single map of the literature; BF-L's sub-track should anchor on this survey's taxonomy.

- **Allamanis, Sutton (2013). "Mining Source Code Repositories at Massive Scale Using Language Modeling." MSR 2013.** The Github Java Corpus paper. Establishes the methodology of mining n-gram statistics over a large corpus. Foundation for empirical-convention work.

- **Movshovitz-Attias, Cohen (2013). "Natural Language Models for Predicting Programming Comments." ACL 2013.** Adjacent: predicting comment text from code with LMs. Useful as an analogue for predicting *convention descriptions* from code, which is closer to P-26's structured-output target.

- **Fowkes, Sutton (2016). "Parameter-Free Probabilistic API Mining across GitHub." FSE 2016.** Extracts API-usage patterns from large corpora (**PAM** system). Reported precision around 75% on top-extracted patterns against expert-labeled ground truth (small sample, hundreds of patterns). DOI: 10.1145/2950290.2950319. Relevant as a *pattern-mining* precedent at corpus scale.

- **DeepMind / Microsoft Research code-LM body of work, 2018-2022.** Several papers on representation learning for code (code2vec, code2seq, GraphCodeBERT, CodeBERT). These produce embeddings useful for *clustering* identifiers and methods, which downstream tools have used for naming-convention inference. Most relevant: Alon, Brody, Levy, Yahav (2019), "code2seq: Generating Sequences from Structured Representations of Code," ICLR 2019, arXiv:1808.01400. Not direct convention extraction, but a building block.

**Honest precision/recall summary.** The published literature reports:
- Naming-convention violation detection: ~94% top-1 precision (NATURALIZE, 2014) on Java naming only.
- Idiom mining: qualitative-only or perplexity reduction; no precision/recall against a labeled corpus that I'm confident of.
- API-pattern mining: ~75% precision on top extracted patterns (PAM, 2016).

None of these are at the granularity of "structured `Convention` object with scope, evidence-symbols, confidence covering naming + layering + idiom + test patterns." The literature offers building blocks; **the P-26 surface is not directly evaluated in any published work I'm confident of through January 2026.**

## §3 LLM-with-structured-output applications

This is the most-relevant-to-P-26 and *most-uncertain* sub-literature.

- **General LLM-code-understanding wave, 2022-2025.** Codex (OpenAI 2021), AlphaCode (DeepMind 2022, Science paper), Code Llama (Meta 2023, arXiv:2308.12950), DeepSeek-Coder, StarCoder (BigCode, arXiv:2305.06161), StarCoder2 (arXiv:2402.19173). Establishes that frontier LLMs do reasonable code understanding; the question is whether the structured-output mode at convention granularity is reliable.

- **JSON-schema / structured-output mode.** OpenAI's structured outputs (2024) and Anthropic's tool-use with JSON schemas are mature features. The *engineering* of "ask the LLM for a list of Pydantic Convention objects" is solved. The *evaluation* — does the LLM produce true conventions or hallucinate plausible-sounding ones — is the open question.

- **Sourcegraph Cody / GitHub Copilot Workspace / Cursor / Continue.dev / Aider / Codeium.** Production tools that consume codebase context. None publishes a "convention catalogue" output mode that I'm confident of. Internally these tools likely have convention-related prompts (e.g., "match the style of the surrounding code"), but the structured-output catalogue is not a marketed feature.

- **Anthropic, OpenAI, Google DeepMind internal evaluations.** Likely have internal benchmarks on code understanding; not enough published at the convention-extraction granularity I'm confident citing.

- **Academic work on LLM structured-output reliability.** A growing 2023-2025 body, including: Liu et al. "Is Your Code Generated by ChatGPT Really Correct?" (NeurIPS 2023, EvalPlus benchmark); various papers on JSON-schema-conformance under structured outputs. None evaluate at the *convention-catalogue* granularity P-26 needs.

- **CodeXGLUE benchmark (Microsoft, 2021; arXiv:2102.04664).** A multi-task code benchmark covering code summarization, defect detection, code completion, etc. Does NOT include a "convention extraction" task. Worth noting as the most-canonical code-eval benchmark *because* of its conspicuous absence of this task.

**Honest gap.** *I am not confident any published work measures precision/recall of an LLM-with-structured-output convention catalogue at the P-26 granularity (named + scoped + evidence-symbol-anchored + confidence-rated).* The sub-literature is plentiful for adjacent tasks (code summarization, code search, code completion), and the engineering primitives are mature, but the specific evaluation BF-L's gate calls for (manual-spot-check precision ≥0.7 on extracted Pydantic Convention objects) is unwitnessed in the published literature I can confidently cite. **The BF-L sub-track is — at best — replicating an internal-but-unpublished result, and at worst conducting genuinely novel work.**

## §4 Semantic naming-convention extractors

Naming is the convention-surface with the most published prior art.

- **NATURALIZE (Allamanis et al. 2014, above).** N-gram-based; the canonical citation. Targets violations against the codebase's own convention rather than against a global standard. ~94% top-1 precision on Java naming.

- **Alon, Zilberstein, Levy, Yahav (2019). "code2vec: Learning Distributed Representations of Code." POPL 2019. arXiv:1803.09473.** Predicts method names from method bodies. Reported F1 around 60% on a Java method-naming benchmark. Demonstrates that method-name *convention* is learnable from corpus.

- **Pradel, Sen (2018). "DeepBugs: A Learning Approach to Name-based Bug Detection." OOPSLA 2018. DOI: 10.1145/3276517.** Detects bugs caused by *swapped or misnamed* identifiers. The shape of the problem — "is this name consistent with the codebase's convention" — is the inverse of "what is the codebase's naming convention." ~85-90% precision reported on synthetic-bug benchmarks.

- **JSNice / DeGuard (Raychev, Vechev et al., ETH Zürich, 2015-2017).** Statistical de-obfuscation of JavaScript / Android bytecode. Recovers names by learning conventions from a large corpus. JSNice was a live service. Precision: ~63% on minified-name recovery (their reported number). DOI: 10.1145/2676726.2677009 (JSNice, POPL 2015).

- **Embedding-clustering approaches.** word2vec-style embeddings applied to identifier vocabularies; less rigorously evaluated; production tools (Cody, Copilot) likely use this kind of approach internally.

- **Identifier-splitting / camelCase-tokenization tools.** Spiral (CASICS lab, 2018) is a published splitter. Useful as preprocessing for naming-convention work.

**Realistic claim for P-26.** Naming conventions are the *most-tractable subset* of the convention surface. The literature supports a ≥0.7 precision target on naming-convention extraction at corpus scale, citing NATURALIZE, code2vec, DeepBugs as triangulated evidence. The sub-track should start here and treat naming as its highest-confidence deliverable.

## §5 Layering / architecture-rule extractors

The layering surface is *enforced* well by industry tooling and *inferred* poorly by published work.

- **ArchUnit (Peter Gafert et al., 2017+).** JUnit-style architectural-rule assertions for Java. Ports: ArchUnitNET, ts-arch, PyArchUnit (the Python port; less mature than the Java original). Coverage: human-authored layering rules over a parsed dependency graph. **No inference.**

- **jQAssistant (Buschmann + collaborators, 2014+).** Scans JVM codebases into a Neo4j graph; Cypher queries express layering rules. **No inference; human-authored queries.**

- **jdeps / jdeprscan.** OpenJDK tooling for module-graph extraction. Outputs the graph; says nothing about violation rules.

- **dependency-cruiser (Sander Verweij, JS/TS).** Configurable rules over a parsed dependency graph. JSON-config layering rules. **No inference.**

- **pydeps + visual-layering tools (Python).** Outputs dependency graphs. Inference of layering *violations* requires additional tooling.

- **NDepend (commercial, .NET).** Code-quality + dependency-rule tool with CQLinq query language. **No inference; human-authored rules.**

- **Sourcegraph SCIP + zoekt.** Cross-language symbol index. Provides the *graph*; the layering inference is downstream.

- **Academic layering-inference work.** **Sangal, Jordan, Sinha, Jackson (2005), "Using Dependency Models to Manage Complex Software Architecture" (OOPSLA 2005)** introduced **Lattix LDM** / **DSM (design structure matrix)** — extracts an implicit layering from import graphs via matrix reordering. Coverage: structural-layering inference *exists* in the academic record but commercial use (Lattix) has been niche. DOI: 10.1145/1094811.1094819.

- **Sarkar et al. (2009), "API-Based and Information-Theoretic Metrics for Measuring the Quality of Software Modularization."** Measures modularization quality from dependency graphs.

**Realistic claim for P-26.** Layering rules are mechanically tractable. The sub-track can either (a) emit declarative layering rules in ArchUnit-compatible syntax via LLM-with-structured-output over the dependency graph; (b) use DSM-style matrix reordering to *suggest* layering, then have the LLM name and scope each suggested layer. Precision ≥0.7 is plausible *given* the underlying dependency graph is accurate (which is a structural-view problem, not a conventional-view problem).

## §6 Test-pattern extractors

Sparsest sub-literature.

- **Industry tooling:** No mature tool I'm aware of extracts test idioms (mock patterns, fixture patterns, assertion patterns) as a structured catalogue. Coverage tools (Coverage.py, JaCoCo, Istanbul) measure *what* is tested; mutation-testing tools (Stryker, PIT) measure *test quality*. Neither categorizes *idiom*.

- **Academic prior art:** **Daniel, Jagannath, Dig, Marinov (2009-2012)** on test-refactoring; **Zhang, Mesbah (2015), "Assertions Are Strongly Correlated with Test Suite Effectiveness," FSE 2015** examines assertion patterns. **Beller, Gousios, Panichella, Zaidman (2015-2017)** on test smells and patterns. None publishes a structured catalogue extractor at P-26 granularity that I'm confident of.

- **tsdetect / PyNose / RTj** (test-smell detectors). Coverage: pre-baked test-smell rules, not corpus-inferred test conventions.

- **LLM-based test-pattern extraction.** Conjecturally feasible but no published evaluation I'm confident of through January 2026. This is the convention sub-surface with the *largest* gap between the P-26 ambition and the literature.

**Realistic claim for P-26.** Test-pattern extraction is the **weakest-supported** sub-surface. The sub-track should mark this as the highest-risk sub-deliverable; honest scoping might explicitly drop it from the v1 gate.

## §7 Golden-corpus precedents

No published "golden corpus of human-labelled conventions" at P-26 granularity that I'm confident of.

Adjacent labelled corpora:
- **CodeXGLUE (Microsoft, 2021).** Code-LM benchmark suite. No convention-extraction task.
- **HumanEval (Chen et al. 2021, arXiv:2107.03374) / MBPP / APPS / SWE-bench (Jimenez et al. 2024, arXiv:2310.06770).** Functional-correctness benchmarks. Not convention.
- **NATURALIZE evaluation corpus (Allamanis 2014).** Java naming conventions; small (~100s of held-out names).
- **Github Java Corpus (Allamanis, Sutton 2013).** Unlabeled; useful as input, not as ground truth.
- **Linux-kernel CHECKPATCH conventions.** A community-maintained list of conventions, mechanically enforced. Not a "golden corpus" in the ML sense, but a real-world artifact close to what P-26 wants to produce.
- **Style guides as proxies.** Google Style Guides (C++, Python, Java, etc.), Airbnb JS, PEP-8, Black opinions. These are *prescriptive*, not *descriptive of one codebase*, but the union of style-guide content + per-project deviation tracking is the closest existing artifact.

**What would be needed to build one.** For BF-L sub-track use:
- **Size.** 50-100 labelled conventions per language for the top-3 languages (~150-300 total) is the rough scale published convention-mining papers operate at. Below that, statistical claims are noisy.
- **Labelling discipline.** Inter-annotator agreement protocol (Cohen's κ ≥ 0.6 is the published-paper threshold), 2-3 expert labellers, blind labelling phase + adjudication phase.
- **Language coverage.** Python + TypeScript + Java is the right starting trio (matches the auto-003 sub-track scope and the published-paper convention).
- **Authoring effort.** Probably 5-15 engineer-days per language for a v1 corpus, plus 2-5 days adjudication. Tractable inside Phase-4 if scoped.

**Honest note.** Building the golden corpus is *itself* a research deliverable. The sub-track should treat corpus authoring + extractor authoring as a coupled pair; the extractor cannot be evaluated without the corpus, and the corpus cannot be authored without scoping decisions the extractor design forces.

## §8 Honest assessment

**Realistic precision/recall ceiling for the P-26 Pydantic-typed Convention extractor.**

| Sub-surface | Realistic v1 precision | Realistic v1 recall | Confidence |
|---|---|---|---|
| Naming conventions | 0.85-0.95 | 0.60-0.80 | High (NATURALIZE, code2vec, DeepBugs) |
| Layering rules | 0.70-0.85 | 0.40-0.70 | Medium (ArchUnit-shape, DSM-shape) |
| Idiom register | 0.50-0.70 | 0.30-0.50 | Low (Allamanis idiom-mining is qualitative; LLM-structured-output unwitnessed at scale) |
| Test patterns | 0.40-0.65 | 0.20-0.40 | Very low (no direct prior art I'm confident of) |
| **Aggregate** | **0.60-0.80** | **0.35-0.60** | **Medium-low** |

The auto-003 sub-track's gate of "manual-spot-check precision ≥0.7 on extracted conventions" is **plausible only if scoped to naming + layering**. Including idiom register and test patterns in the gate likely fails the bar.

**Most-likely-tractable subset to target first.** Naming conventions, then layering rules. This is the order the literature supports and the order industry tooling (NATURALIZE for naming, ArchUnit for layering) validates as solvable. Idiom register and test patterns should be flagged "best-effort, low-confidence" in the v1 deliverable.

**Biggest open problem the literature has not solved.** **Structured-output convention extraction at the P-26 granularity with measured precision/recall against a labelled ground truth.** Every adjacent task is studied; the precise task is not. The BF-L sub-track will either (a) produce the first published evaluation in this regime — genuinely novel research — or (b) accept "best-effort, confidence-scored" outputs and live with the unmeasured-precision risk that follows.

**Secondary open problem.** Cross-language convention representation. The Pydantic `Convention` schema is language-agnostic in the P-26 sketch, but the literature is overwhelmingly Java + Python. TypeScript / JS conventions are less-studied; polyglot codebases (the realistic BF-L target) compound the gap.

**Tertiary open problem.** Convention *staleness*. A convention extracted from a 5-year-old codebase reflects what the team *did*, which may differ from what they *currently want*. The P-26 sketch's stratified-sample (recency × churn) addresses this; the literature does not.

## Specific recommendations for the BF-L sub-track design

1. **Scope v1 to naming + layering.** Drop idiom register and test patterns from the gate (carry them as research-deliverables, not gate-deliverables). This raises the probability of clearing the 0.7 precision gate from ~30% to ~70% on my back-of-envelope estimate.

2. **Author the golden corpus first; couple corpus authoring to extractor authoring.** ~150-300 human-labelled conventions across Python + TypeScript + Java with documented IAA. This is itself ~3-6 engineer-weeks. Without it, the gate is unmeasurable.

3. **Build a triangulation extractor, not a single-method one.** Combine (a) mechanical analyzers (Tree-sitter symbol-table regex for naming, dependency-graph + DSM for layering) as the **floor**; (b) LLM-with-structured-output as the **ceiling**; (c) NATURALIZE-style n-gram statistical signal as the **calibrator**. Report disagreement between (a)/(b)/(c) as the *confidence score* in the Pydantic Convention object. This is the lowest-risk path because each component has independent prior art.

4. **Cite the literature in the ADR alternatives-considered.** The Phase-5 ADR for the conventional view should explicitly cite Allamanis 2018 survey, NATURALIZE, ArchUnit, dependency-cruiser, SonarQube, and the honest gap on LLM-structured-output convention catalogues. This is the strongest defense against a Round-2 adversarial reviewer claiming the sub-track invented a wheel.

5. **Carry idiom register and test patterns as Phase-6 RG flags even if the v1 gate scopes them out.** The methodology-degradation pattern for BF-L should describe how regime classification operates when these sub-surfaces are best-effort / unmeasured. This honors the auto-003 (b)-fallback shape per-sub-surface, even when (a) is chosen overall.

6. **Watch for active work — the dispatch is a watching mechanism.** Specific feeds to monitor through Phase-4: the BigCode project (StarCoder series), Microsoft Research's code-LM line, Sourcegraph's Cody architecture posts, GitHub's Copilot Workspace product launches, and academic venues (ICSE / FSE / OOPSLA / POPL / NeurIPS Big-Code workshop). The user's "a solution sketch may become available very soon" prior is plausible — the *general* LLM-code wave is moving fast.

7. **Treat polyglot as a v2 problem.** Lock v1 to one language (Python is the highest-leverage choice given the ecosystem and the literature) and prove the precision/recall claim there before generalizing. The auto-003 scope ("top-3 languages") is achievable but riskier; if forced to cut, cut to Python only and carry TS / Java as v2.

8. **Make the extractor's failure modes auditable.** Every Pydantic `Convention` carries `evidence-symbols`; the gate evaluation should *require* spot-checkers to look at the evidence-symbols when judging precision. This makes the precision number a measurement of "the extractor cites real evidence" rather than "the convention is true in the abstract" — a stronger and more reproducible bar.

---

**File status.** Phase-4.4 research dispatch deliverable. Feeds the Phase-4 BF-L sub-track design, the Phase-5 conventional-view ADR alternatives-considered, and the Phase-8 lean-eval pressure-test design per [auto-003 §Downstream impact](../decisions/auto-003-bfl-rg-view-choice.md#downstream-impact).
