# Agentic Software Factory / “Dark Factory” — One-Shot Specs & Research

*Compiled May 2026. All links verified against the named repositories at time of writing. Practitioner repos move fast; paths may shift.*

This report has two parts:

1. **Part 1 — Example one-shot specs**: actual spec files (each describing a target system to be built) that an agent can be pointed at to produce a working result. Generic harness/workflow/skill files are excluded unless a target-system spec is embedded in them.
1. **Part 2 — Research papers** on how specification attributes (completeness, ambiguity, specificity, requirement classes) affect how far an AI can get.

-----

## Part 1 — Example One-Shot Specs

### StrongDM Attractor — the original three specs

The core repo “contains no code at all — just three markdown files describing the spec in meticulous detail” (per Simon Willison’s Oct 2025 visit).

|Spec                                                                                                  |Description                                                                              |
|------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
|[attractor-spec.md](https://github.com/strongdm/attractor/blob/main/attractor-spec.md)                |The DOT-digraph workflow-engine spec that defines the whole dark-factory execution model.|
|[coding-agent-loop-spec.md](https://github.com/strongdm/attractor/blob/main/coding-agent-loop-spec.md)|Spec for the agent loop that generates, tests, and repairs code.                         |
|[unified-llm-spec.md](https://github.com/strongdm/attractor/blob/main/unified-llm-spec.md)            |Spec for the multi-provider LLM abstraction layer beneath the agent.                     |

### Kilroy — demo specs (Dan Shapiro’s Attractor implementation)

|Spec                                                                                                                       |Description                                                                 |
|---------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
|[demo/rogue/spec.md](https://github.com/danshapiro/kilroy/blob/main/demo/rogue/spec.md)                                    |Spec for a browser-playable port of the 1980 Rogue roguelike.               |
|[demo/rogue/DoD.md](https://github.com/danshapiro/kilroy/blob/main/demo/rogue/DoD.md)                                      |Definition-of-Done acceptance criteria for the Rogue port.                  |
|[demo/rogue/rogue-fast.dot](https://github.com/danshapiro/kilroy/blob/main/demo/rogue/rogue-fast.dot)                      |Workflow graph driving the Rogue build pipeline.                            |
|[demo/solitaire/solitaire-fast.dot](https://github.com/danshapiro/kilroy/blob/main/demo/solitaire/solitaire-fast.dot)      |Workflow graph for building a playable browser Solitaire game.              |
|[demo/substack-spec-v01.md](https://github.com/danshapiro/kilroy/blob/main/demo/substack-spec-v01.md)                      |Spec for a Substack-clone web app.                                          |
|[demo/substack-spec-v01.dot](https://github.com/danshapiro/kilroy/blob/main/demo/substack-spec-v01.dot)                    |Workflow graph paired with the Substack-clone spec.                         |
|[demo/substack-dod-v01.md](https://github.com/danshapiro/kilroy/blob/main/demo/substack-dod-v01.md)                        |Definition-of-Done criteria for the Substack clone.                         |
|[demo/dttf/dttf-v1.md](https://github.com/danshapiro/kilroy/blob/main/demo/dttf/dttf-v1.md)                                |Spec for a deterministic test-then-fix loop building a custom font renderer.|
|[demo/browser-smoke/browser-smoke.dot](https://github.com/danshapiro/kilroy/blob/main/demo/browser-smoke/browser-smoke.dot)|Workflow graph for a browser smoke-test runner.                             |

### Kilroy — `research/` folder (graded-detail experiment specs)

The same target re-specified at escalating detail levels — a practitioner version of “how far does an AI get as spec attributes change.”

|Spec                                                                                                                     |Description                                                                                      |
|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
|[research/green-test-vague.dot](https://github.com/danshapiro/kilroy/blob/main/research/green-test-vague.dot)            |“Build a terminal Klondike Solitaire in Go with TUI” stated vaguely — low-detail end.            |
|[research/green-test-moderate.dot](https://github.com/danshapiro/kilroy/blob/main/research/green-test-moderate.dot)      |Same Solitaire target at moderate spec detail.                                                   |
|[research/green-test-complex.dot](https://github.com/danshapiro/kilroy/blob/main/research/green-test-complex.dot)        |“Build DTTF: a bitmap-to-TrueType converter with custom Bézier tracer” — high-detail/complex end.|
|[research/refactor-test-vague.dot](https://github.com/danshapiro/kilroy/blob/main/research/refactor-test-vague.dot)      |A refactoring task specified vaguely.                                                            |
|[research/refactor-test-moderate.dot](https://github.com/danshapiro/kilroy/blob/main/research/refactor-test-moderate.dot)|Same refactoring task at moderate detail.                                                        |
|[research/refactor-test-complex.dot](https://github.com/danshapiro/kilroy/blob/main/research/refactor-test-complex.dot)  |Same refactoring task at high detail.                                                            |

### attractor-c (Justin McCarthy) — pure C11 reimplementation, one-shot-built from the specs

|Spec                                                                                                 |Description                                                                                                                           |
|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
|[spec-dod.dot](https://github.com/jmccarthy/attractor-c/blob/main/spec-dod.dot)                      |Pipeline whose embedded goal is to build the entire C11 Attractor engine by satisfying every DoD checkbox in the three upstream specs.|
|[spec-dod-multimodel.dot](https://github.com/jmccarthy/attractor-c/blob/main/spec-dod-multimodel.dot)|Same whole-codebase build spec, routing audit/fix stages to different models.                                                         |

### attractor-pi-dev (James Hugman) — TypeScript / pi.dev reimplementation

|Spec                                                                                                                            |Description                                                                               |
|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
|[examples/ralph-wiggum/pipeline.dot](https://github.com/jhugman/attractor-pi-dev/blob/main/examples/ralph-wiggum/pipeline.dot)  |“Implement epic $epic_id, one issue at a time” — a Ralph-loop build spec.                 |
|[examples/spec-to-beads/pipeline.dot](https://github.com/jhugman/attractor-pi-dev/blob/main/examples/spec-to-beads/pipeline.dot)|“Break $rfc_path into an implementation epic” — turns an RFC into a buildable issue graph.|
|[docs/specs/examples/branching.dot](https://github.com/jhugman/attractor-pi-dev/blob/main/docs/specs/examples/branching.dot)    |Minimal “implement and validate a feature” pipeline (teaching example).                   |
|[docs/specs/examples/human-gate.dot](https://github.com/jhugman/attractor-pi-dev/blob/main/docs/specs/examples/human-gate.dot)  |Minimal human-approval-gate pipeline (teaching example).                                  |
|[docs/specs/examples/simple.dot](https://github.com/jhugman/attractor-pi-dev/blob/main/docs/specs/examples/simple.dot)          |Minimal “run tests and report” pipeline (teaching example).                               |

### Fabro — documented example specs (each embeds a target-system goal)

|Spec                                                                                                                                      |Description                                                                      |
|------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
|[clone-substack.fabro](https://github.com/fabro-sh/fabro/blob/main/test/docs/examples/clone-substack/clone-substack.fabro)                |Builds a Substack-style React newsletter engine from a natural-language spec.    |
|[semantic-port.fabro](https://github.com/fabro-sh/fabro/blob/main/test/docs/examples/semantic-port/semantic-port.fabro)                   |Ports semantic changes from an upstream Python repo into a Go implementation.    |
|[spec-dod.fabro](https://github.com/fabro-sh/fabro/blob/main/test/docs/examples/definition-of-done/spec-dod.fabro)                        |Implements against a definition-of-done and loops until every criterion passes.  |
|[spec-dod-multimodel.fabro](https://github.com/fabro-sh/fabro/blob/main/test/docs/examples/definition-of-done/spec-dod-multimodel.fabro)  |Same DoD build, routing planning to a cheap model and coding to a frontier model.|
|[n-l-spec-conformance.fabro](https://github.com/fabro-sh/fabro/blob/main/test/docs/examples/nlspec-conformance/n-l-spec-conformance.fabro)|Implements from a natural-language spec then validates conformance to it.        |

### Notes on what was excluded

- **OpenHands** has no demo/app specs — only operational `SKILL.md` files (agent instructions), which don’t match the criterion.
- **Gas Town / Gas City / Wasteland** publish no one-shot application specs. Their work primitives are *formulas* and *protomolecules/molecules* — reusable workflow templates (design → plan → implement → review → test chains), not standalone target-system specs.
- Fabro’s generic bundled workflows (`implement-issue`, `goal`, `implement-plan`) and its `docs/internal/demo/01–14` teaching series are harness/workflow configs, not app specs, so they’re omitted here.

-----

## Part 2 — Research on Spec Attributes vs. Code-Generation Success

### Directly varies spec attributes and measures success

|Paper                                                                                                                           |Focus                                                                                                                                                                                             |
|--------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|[HumanEvalComm (arXiv:2406.00215)](https://arxiv.org/abs/2406.00215)                                                            |Injects ambiguity, inconsistency, and incompleteness into problem descriptions; measures whether models clarify vs. silently guess. Closest published analog to the Kilroy vague→complex gradient.|
|[Testing LLMs on Code Generation with Varying Levels of Prompt Specificity (arXiv:2311.07599)](https://arxiv.org/abs/2311.07599)|Runs the same problems at high vs. low specificity (with/without embedded tests) across models; reports pass-rate deltas. The “dial the detail knob” experiment.                                  |
|[Beyond Synthetic Benchmarks: Real-World Class-Level Code Generation (arXiv:2510.26130)](https://arxiv.org/abs/2510.26130)      |Examines how specification completeness affects class-level correctness; finds a “sweet spot” with partial docstrings (complete docs redundant, absent docs unanchored).                          |
|[Ambig-SWE / interactive agents for underspecification (arXiv:2502.13069, ICLR 2026)](https://arxiv.org/abs/2502.13069)         |Builds paired fully-specified vs. underspecified SWE-bench issues for causal measurement; interactivity boosts performance on underspecified inputs by up to 74%.                                 |

### Builds the spec/requirements into the pipeline and measures the lift

|Paper                                                                                                                          |Focus                                                                                                                                                               |
|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|[ArchCode (arXiv:2408.00994)](https://arxiv.org/abs/2408.00994)                                                                |Makes functional and non-functional requirements explicit; introduces HumanEval-NFR, the first benchmark to evaluate NFRs alongside FRs.                            |
|[PRDBench (arXiv:2510.24358)](https://arxiv.org/abs/2510.24358)                                                                |Generates structured PRDs (Requirement Overview, Functional Requirements, Data Requirements) and grades implementations against them using Arrange-Act-Assert tests.|
|[Understanding Specification-Driven Code Generation with LLMs (arXiv:2601.03878, SANER 2026)](https://arxiv.org/abs/2601.03878)|Registered-report empirical study on how human refinement of specification and tests changes pass rate, time-to-pass, and iteration behavior.                       |

### Long-horizon / degradation and ceiling

|Paper                                                                                                                  |Focus                                                                                                                                                 |
|-----------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
|[SlopCodeBench (arXiv:2603.24755)](https://arxiv.org/abs/2603.24755)                                                   |Argues benchmarks evaluate once against complete specs; feeds updated specs at checkpoints and watches code quality degrade (“structural attractors”).|
|[The Specification as Quality Gate (arXiv:2603.25773)](https://arxiv.org/abs/2603.25773)                               |Argues executable specs convert open-ended problems into bounded ones; defines the residual defect classes specs can’t catch (the ceiling).           |
|[Holistic Evaluation of State-of-the-Art LLMs for Code Generation (arXiv:2512.18131)](https://arxiv.org/abs/2512.18131)|Case studies of failure modes (syntax errors, logical flaws, suboptimal algorithms) and the role of prompt engineering / human oversight.             |

### Adjacent / supporting

|Paper                                                                                                                                       |Focus                                                                                                |
|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
|[Enhancing LLM-based Specification Generation via Program Slicing and Logical Deletion (arXiv:2509.09917)](https://arxiv.org/abs/2509.09917)|Program slicing improves spec relevance/completeness; logical deletion improves verification success.|
|[Do Prompt Patterns Affect Code Quality? (arXiv:2504.13656, EASE 2025)](https://arxiv.org/abs/2504.13656)                                   |Empirical assessment of how prompt patterns affect generated-code quality.                           |

### Research gap

No published study uses the exact Kilroy design — one fixed target app, re-specified at graded detail levels, run one-shot through an agentic harness to see how far it gets. Academic work is mostly function-/class-level (HumanEval/SWE-bench derivatives), not whole-app one-shot builds. HumanEvalComm and the prompt-specificity paper are nearest in spirit; Ambig-SWE is the most rigorous on causal “missing attribute” measurement. Kilroy’s `research/` folder may be closer to the whole-app version of this experiment than anything formally published.
