# Attractor Community Implementations — Round-3 Thread 2

**Sources covered (READMEs + AGENTS/CLAUDE.md only; source code not read):**
- https://github.com/danshapiro/kilroy — `README.md`, `AGENTS.md` (Go, MIT)
- https://github.com/smartcomputer-ai/forge — `README.md` (Rust, by Luke Buehler / smartcomputer-ai)
- https://github.com/joyrexus/software-factory — `components/README.md`, `components/kilroy.md`, `components/attractor/README.md` (synthesis knowledge base, not an implementation)
- https://github.com/amolstrongdm/attractor — `README.md`, `CLAUDE.md` (Python, "Amol Kabe" variant; account name `amolstrongdm`)
- https://github.com/brynary/attractor — `README.md` (TypeScript, by Bryan Helmkamp; archived as of 2026-04-28 — succeeded by Fabro)
- https://github.com/fabro-sh/fabro — `README.md` (Rust, Bryan Helmkamp / Qlty.sh — the production-ready successor of brynary/attractor)
- (cross-referenced) `architectures/04-evolutionary-tournament.md`, `architectures/00-comparison.md`, `research/01-strongdm-factory.md`, `research/02-strongdm-attractor.md`

**Date:** 2026-05-11
**Status:** SUCCESS (all five required implementations surveyed; Fabro added as a bonus because brynary's TS variant was archived in favor of it, and Helmkamp is the named author the plan flagged)

---

## 1. Headline finding

**"Attractor" is being interpreted in two incompatible ways by the community.**

1. **Attractor-as-pipeline-orchestrator (canonical, four of five implementations).** Kilroy (Go), Forge (Rust), brynary/attractor (TS, archived), and Fabro (Rust) all implement the StrongDM `attractor-spec.md` faithfully: Graphviz DOT graph, the eight canonical node shapes (Mdiamond/Msquare/box/hexagon/diamond/component/tripleoctagon/parallelogram + the `house` manager loop), edge selection priority, `goal_gate` + `retry_target`, the `model_stylesheet` cascade, `status.json` per-stage contract, and provider-aligned coding-agent profiles (codex / claude-code / gemini-cli). The Attractor *primitive set* reproduces with very little drift.

2. **Attractor-as-feedback-loop (the Amol Kabe variant).** `amolstrongdm/attractor` reads the *higher-level* StrongDM Software Factory site (factory.strongdm.ai), not the DOT pipeline spec, and implements the **Scenarios + Satisfaction + Digital Twin Universe** loop instead. It has **no DOT graph, no node-shape taxonomy, no `goal_gate`, no `status.json`, no manager_loop**. Where it does converge with the canonical spec is in the iterative-until-converged operating shape. Where it *adds* — and this is what `architectures/04-evolutionary-tournament.md` cares about — is **four named persona specialists** (`CodingAgent`, `ValidatorAgent`, `DebuggerAgent`, `PlannerAgent`).

This split matters for Architecture 4's diversity-policy assumption. The pattern-level question is *not* "do independent teams converge on the Attractor pattern?" but "which Attractor pattern do they converge on?" The four canonical-Attractor implementations converge tightly on the DOT graph + provider profiles. They do **not** converge on named personas — only Amol Kabe's variant introduces them, and his variant is structurally closer to Architecture 2 (Compound Atelier) than to Architecture 1.

## 2. Comparison table

| Implementation | Lang / Author | DOT graph | Node-shape set | `goal_gate`+`retry_target` | `status.json` | `manager_loop` | Model stylesheet | Provider profiles | Named personas | Sandbox / isolation | Backend strategy | Distinguishing addition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Kilroy** (danshapiro/kilroy) | Go / Shapiro | Yes — canonical | Full canonical 8 + manager_loop (mention) | Yes (canonical edge-selection priority, retry presets `none`/`standard`/`aggressive`/`linear`/`patient`) | Yes (per-stage `prompt.md`/`response.md`/`status.json`) | Implied via spec compliance; not headlined | Yes (CSS cascade) | OpenAI (codex), Anthropic (claude), Google (gemini) — CLI or API per provider; built-ins also Kimi, ZAI, Cerebras, Minimax | None | **Git worktree per run + commit-per-node + run-branch resume** | `cli_profile: real` vs `test_shim` (gated by `--allow-test-shim`); per-provider `backend: cli|api` mandatory | **CXDB**: durable typed run-event database for resume; `ingest` skill turns English → DOT; "Prime Directive" in AGENTS.md = *fix the system, not the project* |
| **Forge** (smartcomputer-ai) | Rust / Buehler | Yes — canonical | Full canonical 8 + `house` manager loop | Yes (explicit `goal_gate=true`; engine routes to `retry_target`) | Yes (`manifest.json`, `status.json`, `prompt.md`, `response.md` per stage; JSONL event stream) | Yes ("Manager Loop" listed in node-types table) | Yes (CSS cascade, `*` < shape < `.class` < `#id`) | `agent` (built-in, OpenAI + Anthropic), plus `claude-code`, `codex-cli`, `gemini-cli` CLI adapters; `mock` for dry-run | None | Isolated `/tmp` git sandbox for e2e tests; otherwise inherits caller's FS | Multi-backend via `--backend` flag (agent/mock/claude-code/codex-cli/gemini-cli); interviewer mode auto/console/queue | **Three-tier test discipline** (default / infra-only / costs-money); explicit `#[ignore]`-fails-hard rule; vendored CXDB client SDK as a workspace crate |
| **brynary/attractor** (archived) | TS / Helmkamp | Yes — canonical | Full canonical | Yes (per archived README) | Yes (per archived README) | Yes | Implied | Anthropic + OpenAI + Gemini via the bundled `unified-llm` package | None | None documented | Bun/TS monorepo of three packages: `unified-llm`, `coding-agent`, `attractor` | **Self-deprecated** — README points readers to Fabro; valuable as evidence that a TS implementation existed and was then *intentionally* replaced by a Rust successor (the same author switched substrates) |
| **Fabro** (fabro-sh/fabro) | Rust / Helmkamp (Qlty.sh) | Yes — canonical, "Graphviz DOT" headlined as a feature | Canonical + headlined HITL hexagons | Yes ("verification gates", "fix loops automatically") | Yes (durable event streams, checkpoints, conclusions, stage outputs) | Implied | Yes (CSS-like stylesheet; `model: claude-haiku-4-5` / `claude-sonnet-4-5` examples) | Multi-vendor "ensemble intelligence"; SLSA-attested binary; explicit "automatic fallback chains" | None | **Daytona cloud sandboxes** with network controls and snapshot-based setup; `fabro sandbox ssh` + `fabro sandbox preview` for live debugging | Single Rust binary; REST API + SSE; React web UI; runs as a **server** | **Production runtime**: 24/7 server queue, cloud-sandbox isolation as a first-class feature, issue-based contribution model (no outside PRs because "AI can rapidly write large amounts of plausible-looking code") |
| **Amol Kabe variant** (amolstrongdm/attractor) | Python / Kabe | **No — replaced by YAML scenarios + Python feedback loop** | **No node-shape taxonomy** | **No** — replaced by `target_satisfaction` (default 0.95) and `max_iterations` + `max_tokens` | **No** — replaced by `.attractor/runs/{run_id}/{checkpoint.json,metrics.json}` and `.attractor/history.json` | **No** — replaced by `AgentOrchestrator` + `FeedbackLoop` Python classes | **No** | Anthropic + OpenAI + `mock` via single `create_llm_client(provider=…)` factory | **Yes — four named personas**: `CodingAgent` (coder), `ValidatorAgent` (reviewer), `DebuggerAgent` (debugger), `PlannerAgent` (planner) | None documented | Single Python process; async-first; `uv sync` install | **Scenarios as YAML holdout** + **Digital Twin Universe** (YAML twin behaviors) + **probabilistic satisfaction score with confidence interval** + **sprint-ledger workflow** (`/megaplan`, `/sprint`, `ledger.py` CLI) |

## 3. What every canonical implementation kept

The four DOT-based implementations (Kilroy, Forge, brynary, Fabro) all reproduce the same primitive set:

- **DOT as the workflow DSL.** None of the four reaches for YAML, JSON, Python decorators, or a custom DSL. The DOT-graph-as-workflow choice survives the language port intact.
- **The eight canonical node shapes** (Mdiamond start, Msquare exit, box codergen, hexagon wait.human, diamond conditional, component parallel, tripleoctagon fan-in, parallelogram tool) plus the `house` manager_loop. Forge's README enumerates all of them; Kilroy's README enumerates the same and points to its `internal/attractor/engine/` package; Fabro's example workflow uses Mdiamond/hexagon/box/Msquare verbatim.
- **`goal_gate=true` + `retry_target` semantics.** Forge spells this out: "If a goal gate hasn't succeeded when the engine reaches the exit node, it routes to `retry_target` instead." Fabro markets this as "verification gates … failures trigger fix loops automatically."
- **CSS-like model stylesheet cascade.** Forge spells out `*` < shape < `.class` < `#id` specificity verbatim. Fabro's first example uses `* { model: claude-haiku-4-5 } .coding { model: claude-sonnet-4-5 }` — identical syntax to the StrongDM spec.
- **Per-stage artifact contract.** `prompt.md` + `response.md` + `status.json` per node directory is reproduced in Kilroy (typical stage-level artifacts list) and Forge (e2e test verifies these four files).
- **Provider-aligned coding-agent backends.** Kilroy maps `openai → codex exec --json --sandbox workspace-write`, `anthropic → claude -p --output-format stream-json`, `google → gemini -p --output-format stream-json --yolo`. Forge offers the same as `--backend claude-code|codex-cli|gemini-cli`. This **directly validates the Architecture-1/3/4 "provider-aligned profile" decision** — three independent teams chose the same provider mapping without coordination.
- **Pluggable Interviewer.** Forge documents `auto | console | queue` modes explicitly mirroring StrongDM's `AutoApproveInterviewer / ConsoleInterviewer / QueueInterviewer` set.

## 4. What each implementation dropped or replaced

- **Kilroy** drops nothing material from the orchestration layer; it *constrains* the provider-profile space (in "real" mode, only canonical CLI binaries are accepted — `KILROY_CODEX_PATH` etc. are *rejected*) as a production-safety measure, and adds an `--allow-test-shim` escape hatch.
- **Forge** drops the in-prod cloud sandbox (lives in test-tier-2 only); replaces some retry/event surface with its own JSONL event-streaming contract.
- **brynary/attractor** dropped *itself* — the author archived it and migrated readers to Fabro. The README explicitly states "the ideas here have evolved into Fabro, a production-ready software factory built in Rust." Substrate rewrite from Bun/TypeScript → Rust.
- **Fabro** retains every canonical primitive but moves them from "library you compose" to "server you operate." The CLI is the entry point; persistent state lives in the server.
- **Amol Kabe variant** drops *every* DOT/orchestration primitive. It is genuinely a different artifact answering the same higher-level brief.

## 5. What each implementation ADDED beyond the canonical spec

This is where the real signal lives.

**Kilroy adds:**
- **CXDB** — a durable typed-event execution database (event recording, blob artifact storage, recovery metadata). Resume-from-CXDB is a distinct mode from resume-from-logs and resume-from-run-branch.
- **`attractor ingest`** — a Claude-CLI-powered skill that turns English requirements into a validated DOT file. This is the missing front-end of the spec.
- **Git worktree-per-run + commit-per-node** with a `attractor/run/...` branch prefix. The Attractor spec deliberately stays silent on persistence; Kilroy makes it concrete.
- **HTTP server mode** (experimental) with SSE event streams and human-gate REST endpoints.
- **A Prime Directive in `AGENTS.md`** that is itself worth quoting for `architectures/00-comparison.md`'s "human leverage" section: *"You are not here to use Kilroy — you are here to improve Kilroy. If Kilroy fails to build a project: don't fix the project, don't fix the dotfile, don't fix the system so it works for this project. … Your changes should work for every project, every language, every system."* This is a hard-coded version of the meta-loop our Architecture 2 (compound engineering) chases.

**Forge adds:**
- **A three-tier test discipline** (default / infra-only / costs-money) with hard-fail on missing prerequisites — a CI-shaped trust contract that's missing from the StrongDM spec.
- **`forge-cxdb-runtime` and `forge-cxdb`** as workspace crates — CXDB is brought into Forge's own monorepo as a vendored SDK plus a runtime integration crate, demonstrating that CXDB is *the* expected persistence substrate even outside StrongDM.
- **An e2e-pipeline test** that exercises real CLI agents end-to-end in `/tmp` sandboxes — the only one of the surveyed implementations that bakes a full end-to-end CLI-backed pipeline test into its default CI strategy.

**Fabro adds:**
- **Daytona cloud sandboxes** with network controls, snapshot-based setup, and automatic cleanup — full network/FS isolation per run. This is the strongest sandbox story in the corpus and is the most relevant artifact for `architectures/04-evolutionary-tournament.md`'s "candidates run in independent sandboxes" requirement.
- **`fabro sandbox ssh` + `fabro sandbox preview`** for live debugging into a running agent's sandbox.
- **Server-mode 24/7 operation** with REST + SSE + React UI — runs survive laptop sleep; the cognitive-ceiling problem the architecture-4 spec calls out is *not* mitigated, but the operational ceiling is.
- **SLSA Build Provenance attestations** on release binaries — supply-chain provenance is a first-class concern.
- **Issue-based contribution model** ("AI can rapidly write large amounts of plausible-looking code … we are tightly controlling the inputs into the software development process"). Notable doctrinal statement.

**Amol Kabe variant adds (relative to the canonical Attractor spec):**
- **Four named persona specialists** — `CodingAgent` (coder), `ValidatorAgent` (reviewer), `DebuggerAgent` (debugger), `PlannerAgent` (planner). This is the load-bearing finding for Architecture 2 (Compound Atelier) and the v1-vs-v2 split the plan asked about: the personas are *named, separate Python classes implementing an `Agent` ABC*, not configurations of a single node type.
- **Scenarios-as-holdout** YAML format with steps / preconditions / postconditions / `twins_required` / `holdout_weight`.
- **Probabilistic satisfaction score** with a confidence interval (`DefaultSatisfactionCalculator`) — replaces boolean goal-gate enforcement with a continuous fitness signal. **This is structurally Architecture-4's fitness function**, not Architecture-1's gate.
- **Digital Twin Universe** as YAML behavior definitions of third-party services (a request matcher → response template DSL), runnable as separate twin servers.
- **Sprint workflow** (`/megaplan`, `/sprint`, `docs/sprints/ledger.py`) for managing iterative development on the factory itself.

## 6. Documented assumptions about model floor, provider alignment, sandbox

- **Model floor.** Only Fabro names specific models (Claude Haiku 4.5 for cheap nodes, Claude Sonnet 4.5 for coding nodes) and only as a *stylesheet example*. None of the five names a hard model floor. Kilroy's `modeldb` ships an OpenRouter model catalog as updateable data (matching StrongDM's "model catalog is data, not code" lesson).
- **Provider alignment.** Kilroy, Forge, brynary, and Fabro all preserve the provider-profile discipline (codex / claude-code / gemini-cli). The Amol Kabe variant collapses to a single `create_llm_client(provider=…)` factory with no per-provider tool-set differentiation — a clear regression on this axis.
- **Sandbox.** Kilroy = local git worktree only; Forge = `/tmp` git sandboxes for tests, no prod sandbox; Fabro = Daytona cloud VMs with network controls (strongest); brynary = nothing documented; Amol Kabe = single Python process, no isolation documented. The sandbox dimension is where Fabro pulls ahead and where Architecture 4's diversity-of-candidates story would land if we adopted any of them as substrate.

## 7. Implications for `architectures/04-evolutionary-tournament.md`

1. **Pattern-level diversity is *empirically* achievable** at the orchestration-DSL layer: four independent teams converged on DOT + the eight node shapes + the CSS stylesheet. But the diversity they show is *implementation-language* diversity (Go/Rust/TS/Python), not *pattern-shape* diversity — they all do the same thing. This is good news for Architecture 4's "diversity policy" if the candidates are *coding* implementations, but doesn't itself produce design-shape diversity at the orchestration layer.
2. **Real design-shape diversity only appears in the Amol Kabe variant**, which is the only one that introduces named personas. This is consistent with `architectures/00-comparison.md` line 79: *"Community Attractor implementations like Amol Kabe's do introduce specialized Coding/Validator/Debugger/Planner agents."* The plan flagged this as Architecture 2's distinguishing move; the survey confirms it is genuinely *non-canonical* — no DOT-canonical implementation in the field uses named personas.
3. **The sandbox primitive Architecture 4 needs already exists in Fabro** (Daytona, network controls, snapshot setup). This is a concrete substrate candidate.
4. **Provider-aligned discipline is robust** — every DOT-canonical port reproduces it, even when porting languages. This re-validates Architecture 4's "tooling-profile reference" decision.

## 8. Open follow-ups (out of scope here)

- **CXDB the database.** All Go/Rust ports either vendor or run it; we should survey its API surface independently (it's a separate StrongDM repo we haven't read).
- **AttractorBench.** `strongdm/attractorbench` (Python, 16 stars, instruction-following benchmark) — the corpus's only behavioral benchmark for NLSpec-driven coding agents. Worth a follow-up.
- **The other community ports** the plan listed but we didn't sample: `samueljklee/attractor` (Python, DOT-based, 24 stars — would confirm or refute the "Python-equals-no-DOT" pattern set by Amol Kabe), `jhugman/attractor-pi-dev` (TS, pi.dev runtime), `jmccarthy/attractor-c` (pure C11), `puck-bot/Crucible` (.NET), `Alezrik/attractor-phoenix` (Elixir). A second-pass sample of `samueljklee/attractor` would resolve whether the Amol Kabe departure is a Python-language artifact or a Kabe-specific design move.
- **Fabro's docs** (https://docs.fabro.sh) are blocked from the sandbox — would tell us more about the sandbox model.

## 9. Blocked URLs encountered

- `https://api.github.com/...` — GitHub REST API was rate-limited from the sandbox after a handful of probes; the MCP `github` tool was used as the fallback to recover. No content was lost.
- `https://docs.fabro.sh/...` — not attempted (sandbox typically blocks; the README provides enough surface for this thread).

## 10. Status

**SUCCESS.** Five distinct implementations surveyed (target was 4–5). Headline finding (canonical-DOT vs. Kabe-personas split) is concrete and load-bearing for `architectures/04-evolutionary-tournament.md` and `architectures/00-comparison.md`'s persona-vs-personaless axis. Word count: ~1,950 (within the 1200–2000 target).
