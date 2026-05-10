# StrongDM Attractor — Research Report
**Sources covered:**
- https://github.com/strongdm/attractor (repo root listing)
- https://raw.githubusercontent.com/strongdm/attractor/main/README.md
- https://raw.githubusercontent.com/strongdm/attractor/main/attractor-spec.md
- https://raw.githubusercontent.com/strongdm/attractor/main/coding-agent-loop-spec.md
- https://raw.githubusercontent.com/strongdm/attractor/main/unified-llm-spec.md

**Date:** 2026-05-10

## Executive summary

Attractor is StrongDM's open, do-it-yourself recipe for a "software factory." The repo is intentionally minimal: a short README plus three "NLSpecs" (natural-language specifications "intended to be directly usable by coding agents to implement/validate behavior"). The README's "build" instruction is itself a single prompt: `codeagent> Implement Attractor as described by https://github.com/strongdm/attractor`. So Attractor is simultaneously (a) an artifact-level demonstration of spec-driven agentic dev — the spec *is* the product — and (b) a runtime/methodology for orchestrating multi-stage AI workflows.

The methodology layer comes in three vertically-stacked specs:

1. **attractor-spec.md** — a graph-based pipeline orchestrator. Workflows are written in **Graphviz DOT**: nodes are stages (LLM, human gate, tool, parallel, conditional, supervisor loop), edges are deterministic routes with conditions and weights. The "graph IS the workflow" — declarative, version-controlled, visually renderable. Stages exchange a shared key-value `Context`, write `status.json` audit files, and reach the exit only after `goal_gate` nodes are satisfied (with retry-target jumps if not).
2. **coding-agent-loop-spec.md** — a programmable, headless coding-agent loop (the "worker" inside a codergen node). Notable design choices: provider-aligned (one profile per provider that mirrors that provider's own reference CLI — codex-rs for OpenAI, Claude Code for Anthropic, gemini-cli for Gemini), event-stream-first, with explicit support for steering and follow-up message injection mid-loop.
3. **unified-llm-spec.md** — a thin SDK that abstracts OpenAI/Anthropic/Gemini behind common Request/Response/Message types while exposing each provider's *native* API to preserve cache, thinking, and reasoning features.

The methodology's strongest opinions: workflow logic belongs in a declarative graph, not in prompts or code; **human-in-the-loop is a first-class node type** (hexagons); **goal gates** plus retry-targets implement "definition of done" enforcement; **context fidelity** is a per-node/per-edge slider (`full`, `compact`, `summary:low|medium|high`, `truncate`) that explicitly manages context-window usage as a routing concern; and **supervisor loops** (`stack.manager_loop`) let one node observe-and-steer a child pipeline, giving a clean recursive "manager managing workers" pattern. These primitives are domain-agnostic and could underpin a factory in which a single human runs many agents because the human only interacts at hexagon nodes — everywhere else, the graph decides.

## Agents and roles

Attractor itself defines **node handlers**, not agent personas. A "role" is a node shape + handler combination, configurable via attributes. The set is small and orthogonal:

- **`start` (Mdiamond shape)** — pipeline entry; no-op handler; exactly one per graph.
- **`exit` (Msquare)** — terminal node; the engine (not the handler) checks goal gates here.
- **`codergen` (box, default)** — LLM stage. Expands `$goal` in the prompt, calls a pluggable `CodergenBackend`, writes `prompt.md` / `response.md` / `status.json` to the stage dir. This is where a coding agent (per the Coding Agent Loop spec) executes.
- **`wait.human` (hexagon)** — human-in-the-loop gate. Builds a multiple-choice question from the outgoing edges' labels and waits for an `Interviewer.ask()` answer.
- **`conditional` (diamond)** — pure routing point; handler is a no-op; the engine evaluates edge conditions.
- **`parallel` (component)** — fan-out to concurrent branches with a join policy (`wait_all` or `first_success`) and `max_parallel`.
- **`parallel.fan_in` (tripleoctagon)** — consolidates parallel results; can use either a heuristic ranker or an LLM-evaluator (if `prompt` is set).
- **`tool` (parallelogram)** — runs a shell command / API call.
- **`stack.manager_loop` (house)** — **supervisor loop**: orchestrates observe / steer / wait cycles over a child pipeline (child DOT file referenced via `stack.child_dotfile`). Observes child telemetry, scores progress, and can inject "steering" instructions into the child's active stage directory.
- **Custom handlers** — register any `type` string; node `type` attribute overrides shape resolution.

Inside a `codergen` node, the Coding Agent Loop spec layers in **provider profiles** as the agent's identity:
- **OpenAI profile** — codex-rs–aligned tools and system prompt (uses `apply_patch` for edits).
- **Anthropic profile** — Claude Code–aligned (uses `edit_file` exact-match search/replace; 120s default shell timeout).
- **Gemini profile** — gemini-cli–aligned (adds optional web search and web fetch).

These profiles are explicitly **not unified**: Attractor's authors argue each model is best left in the tool format it was trained on (see "Pitfalls / lessons").

## Workflows and cycles

The unit of work is a **pipeline run** of a DOT graph. The execution lifecycle is six phases: **PARSE → TRANSFORM → VALIDATE → INITIALIZE → EXECUTE → FINALIZE** (attractor-spec.md §3.1). The EXECUTE loop is:

1. Resolve start node (`shape=Mdiamond` or id `start`/`Start`).
2. For the current node:
   - Build a retry policy (node `max_retries` → graph `default_max_retries` → 0).
   - Execute the handler with retries and backoff (presets: `none`, `standard`, `aggressive`, `linear`, `patient`).
   - Record outcome (`SUCCESS`, `PARTIAL_SUCCESS`, `RETRY`, `FAIL`, `SKIPPED`); merge `context_updates` into context.
   - Save a checkpoint to `{logs_root}/checkpoint.json` (resume-capable).
3. **Edge selection** (deterministic 5-step priority): condition match → preferred label → suggested next IDs → highest `weight` → lexical tiebreak on target id.
4. If the next edge has `loop_restart=true`, terminate this run and re-launch with a fresh log dir.
5. On reaching a terminal node, **goal-gate enforcement** runs: every visited node with `goal_gate=true` must be SUCCESS or PARTIAL_SUCCESS; otherwise jump to that node's `retry_target` (or `fallback_retry_target`, or graph-level retry target). If no retry target, FAIL.
6. Failure routing order on FAIL: fail-edge (`condition="outcome=fail"`) → node `retry_target` → node `fallback_retry_target` → terminate.

Handoffs happen via three mechanisms: (a) **edges** (typed routing), (b) **the shared `Context`** (key-value, with reserved namespaces `context.*`, `graph.*`, `internal.*`, `parallel.*`, `stack.*`, `human.gate.*`, `work.*`), and (c) the **`status.json` contract** at each stage directory, which is a written, inspectable audit trail (Appendix C). External agents can write `status.json` to communicate outcomes back to the engine.

The **manager_loop** pattern provides the meta-cycle: a supervisor node loops every `manager.poll_interval` (default `45s`), executing `observe`, `steer`, and `wait` actions over a child run until a stop_condition fires or the child terminates. This is how Attractor scales from "one pipeline" to "one human running a fleet of pipelines" — humans interact with the manager; the manager interacts with the workers.

## Specification / brief methodology

Attractor reifies two distinct "specs":

1. **NLSpecs (the repo's own contribution).** Per the README, an NLSpec is "a human-readable spec intended to be directly usable by coding agents to implement/validate behavior." The three spec files are themselves the canonical example: hand-written markdown with section numbering, BNF grammars, pseudocode, attribute tables, a **"Definition of Done"** section with explicit checklists, and a **"Cross-Feature Parity Matrix"** (a test grid every implementation must pass). The Integration Smoke Test at §11.13 is a runnable acceptance scenario embedded in the spec.

2. **Pipeline briefs (the DOT file).** The graph attribute `goal` is the human-readable mission, exposed as `$goal` in every node's prompt template. Node `prompt` is the "task description," `label` is the display name, `class` selects model presets via the **model_stylesheet** (CSS-like cascade: `*` → shape → class → id, with explicit node attrs winning). The brief is **declarative, diffable, and renderable to SVG**.

Validation/linting is built in (§7): 12+ rules including `start_node`, `terminal_node`, `reachability`, `edge_target_exists`, `condition_syntax`, `stylesheet_syntax`, `goal_gate_has_retry`, `prompt_on_llm_nodes`. `validate_or_raise()` refuses to execute any pipeline with error-severity diagnostics. Custom lint rules can be registered.

## Review and feedback patterns

Reviews are not implicit — they are explicit `wait.human` (hexagon) nodes inserted into the graph wherever a human gate is needed. The mechanism (§4.6, §6):

- The node's outgoing edges' **labels become the answer options**. Labels like `"[A] Approve"`, `"A) Approve"`, `"A - Approve"`, or first-letter conventions all parse into keyboard accelerators.
- A `Question` (text, type, options, optional timeout, optional default) goes to the active `Interviewer`. Built-in implementations: `AutoApproveInterviewer` (CI/automation), `ConsoleInterviewer` (CLI prompt), `CallbackInterviewer` (Slack/web), `QueueInterviewer` (deterministic replay/testing), `RecordingInterviewer` (wraps another to record Q&A pairs for audit).
- The selected answer becomes a `preferred_label` and `suggested_next_ids` on the outcome, which the engine uses to route.
- Timeouts: if no `human.default_choice` on the node, the node returns `RETRY`.

Inside a codergen node, the agent loop adds **steering** (host-app injects user-role messages between turns) and **follow-up** (queue a message that triggers a new processing cycle after the current input completes). This lets a human or supervisor course-correct mid-task without restarting the session. The supervisor loop handler builds on the same mechanism: it writes "intervention instructions" into the child's active stage directory.

The event stream (§9.6) — `PipelineStarted`, `StageStarted/Completed/Failed/Retrying`, `ParallelBranchStarted/Completed`, `InterviewStarted/Completed/Timeout`, `CheckpointSaved` — is the primary review surface for both UIs and audit logs. The HTTP server mode (§9.5) exposes pipeline status, SSE event streams, pending questions, and answer endpoints over REST.

## Human leverage techniques

1. **Visible declarative pipelines.** A DOT file diffs cleanly in PRs and renders to SVG; humans review the *structure of the work*, not chase ad-hoc scripts.
2. **Human gates are explicit and ergonomic.** Hexagon nodes generate keyboard-shortcutted menus from edge labels — designed for fast triage.
3. **Goal gates + retry_target.** The human writes the definition of done once, declaratively, and the engine loops back automatically when gates are unsatisfied.
4. **Supervisor loops.** One human watches a manager that watches N workers. The supervisor's `observe / steer / wait` cycle is configurable, with cooldowns to avoid over-steering.
5. **Context fidelity as a knob.** Per-node `fidelity` (`full` / `compact` / `summary:low|medium|high` / `truncate`) lets the pipeline designer trade off context cost for continuity without code changes — and the edge can override the target node, so different *entry paths* into the same node can carry different histories.
6. **Pluggable Interviewer.** The same pipeline runs unattended (AutoApprove), via CLI, via Slack, or in replay mode — same graph, different human-presence regime.
7. **Checkpoint + resume.** Crashes don't lose progress; the human can intervene, edit the checkpoint or context, and resume.
8. **Status-file contract.** External processes (other agents, scripts) can hand off control to the engine just by writing `status.json` — a low-friction integration surface.

## Pitfalls, gotchas, and lessons learned

The repo is mostly normative spec, but several explicit "we did this because…" passages surface lessons:

- **Don't reuse the SDK's `generate()` tool loop inside an agent.** The Coding Agent Loop spec explicitly says: *"The agent loop does NOT use the Unified LLM SDK's `generate()` high-level function (which has its own tool loop). It uses the low-level `Client.complete()` and implements its own loop because it needs to interleave tool execution with output truncation, steering, events, and loop detection."* A single shared loop is the wrong abstraction; the agent owns its loop.
- **Character truncation must run before line truncation.** *"A file could have 2 lines that are each 10MB. Line-based truncation would see 'only 2 lines' and pass it through untouched, blowing up the context window."* (Coding Agent Loop, Design Decision Rationale)
- **Untruncated output goes to events; truncated output goes to the LLM.** Hosts always have the full data; the model sees only what fits.
- **Reject universal tool interfaces across providers.** *"Each model family works best with its native agent's tools and system prompts."* The Attractor team picks codex-rs / Claude Code / gemini-cli tool sets per provider rather than forcing convergence. (Coding Agent Loop §1.3)
- **Streaming and non-streaming must be separate methods.** *"A single method with a stream flag was rejected because the return types are fundamentally different."* (Unified LLM spec)
- **Prompt caching matters and is provider-asymmetric.** Anthropic requires explicit `cache_control` annotations; OpenAI is automatic; the SDK must inject cache markers automatically to capture up to ~90% cost reduction.
- **Model catalog is data, not code.** *"AI agents building on top of this SDK often hallucinate model identifiers from stale training data"* — so ship the catalog as updateable data so new models work without SDK updates.
- **Concurrency is single-threaded at the graph level.** Attractor explicitly chooses single-threaded traversal "to simplify reasoning about context state and avoid race conditions" (§3.8). Parallelism is opt-in inside `parallel` nodes only; parallel branch context changes are **not** merged back — only the handler's outcome+context_updates are.
- **Resume degrades fidelity for one hop.** *"If the previous node used `full` fidelity, degrade to `summary:high` for the first resumed node, because in-memory LLM sessions cannot be serialized."* (§5.3) A real consequence of statefulness vs. checkpointability.
- **Goal-gate without a retry_target is suspicious.** The linter warns (`goal_gate_has_retry`). Defining the gate without an escape route is a common authoring mistake.

## Skill / agent file taxonomy

Attractor does not ship a `.claude/` agents directory, AGENTS.md template, or skill files at top level. Its "agent definitions" are entirely captured by:

1. **Per-stage prompts** inside DOT nodes (`prompt` attribute, with `$goal` expansion).
2. **The `class` attribute** on each node + a graph-level `model_stylesheet` that maps classes/shapes/ids to `llm_model`, `llm_provider`, `reasoning_effort`. This is the closest thing to a "skill file taxonomy" — it's CSS-style cascading model selection.
3. **Subgraph-derived classes.** A subgraph labeled `"Loop A"` produces the class `loop-a` on all enclosed nodes, so groups of nodes can share defaults.
4. **Provider profiles** (Coding Agent Loop spec) — implicit "agent personas" defined by which reference CLI's tools and system prompt are loaded.
5. **Project-doc layering** in the coding-agent loop: system prompt is assembled from (a) provider base instructions, (b) environment context, (c) tool descriptions, (d) AGENTS.md / CLAUDE.md / GEMINI.md (up to 32KB), (e) user overrides — later layers win. This is the only place Attractor names project-level agent docs, and it explicitly defers to community filenames rather than inventing its own.

There is **no formal hierarchy of "Planner / Implementer / Reviewer" agent roles** as separate artifacts; instead, those roles emerge from how the user wires nodes in DOT.

## Notable quotes

- "The graph is the workflow: nodes are tasks, edges are transitions, and attributes configure behavior." — attractor-spec.md §1.1
- "The pipeline can pause at designated nodes, present choices to a human operator, and route based on the human's decision. This supports approval gates, code review, and manual override — critical for AI workflows where automated judgment may not be sufficient." — attractor-spec.md §1.3
- "Handlers SHOULD NOT embed provider-specific logic; LLM orchestration is delegated to the integrated SDK." — attractor-spec.md §4.12
- "The fidelity of control is the point. Every coding agent CLI is built on an agentic loop internally; this spec makes that loop a first-class, programmable interface." — coding-agent-loop-spec.md §1
- "The `TOOL_CALL_END` event carries the FULL untruncated tool output. The LLM receives the truncated version." — coding-agent-loop-spec.md, Design Decision Rationale
- "Each model family works best with its native agent's tools and system prompts." — coding-agent-loop-spec.md §1.3 (Provider-aligned principle)
- "NLSpec (Natural Language Spec): a human-readable spec intended to be directly usable by coding agents to implement/validate behavior." — README.md, Terminology
- "Application code should not contain provider-specific logic. The unified interface handles all translation. Provider-specific features are available through an explicit escape hatch, not through leaky abstractions." — unified-llm-spec.md §1 (Design Principles)

## Recommended additional sources

- https://graphviz.org/doc/info/lang.html — the DOT language reference. Attractor explicitly cites this; understanding the DOT subset is necessary to evaluate whether DOT is the right brief language for a factory.
- https://github.com/openai/codex — codex-rs, the OpenAI reference agent whose tools (`apply_patch`) and system prompt structure Attractor mirrors for the OpenAI profile.
- https://github.com/anthropics/claude-code — Claude Code, the Anthropic reference agent whose `edit_file` semantics and system prompt are mirrored.
- https://github.com/google-gemini/gemini-cli — gemini-cli, the Gemini reference agent (web search/fetch tools).
- StrongDM Factory blog/docs (parent project referenced in the README's framing "create your own software factory") — needed to reconcile Attractor's primitives with the parent Factory methodology being studied in research report #1.

## Open questions for synthesis

1. **DOT vs. layered-spec.** spec-driven-ai-dev.md positions the *specification* as the scarce artifact and uses layered prose. Attractor positions the *pipeline graph* as the canonical workflow definition and uses DOT. Can a factory have both — DOT for orchestration, layered prose for the spec the orchestration is working on? Where do they meet (probably: the `goal` attribute and per-stage `prompt`)?
2. **Failure-mode taxonomy.** spec-driven-ai-dev.md classifies failures as silence / ambiguity / incorrectness / inconsistency / undiscovered preference. Attractor classifies outcomes as success / partial / retry / fail / skipped and errors as retryable / terminal / pipeline. How do these map? Attractor's outcomes are operational; the baseline's failure modes are epistemic. Bridging them would require a diagnostic node that classifies a FAIL into one of the five spec-driven categories.
3. **Channel 1 vs Channel 2 in DOT.** spec-driven-ai-dev.md splits compliance failures (automated tests) from completeness failures (human-only). Attractor unifies these behind `wait.human` and `tool` nodes but doesn't enforce the channel distinction. Should a factory enforce that Channel 2 reviews happen at hexagon nodes only?
4. **Supervisor recursion depth.** `stack.manager_loop` supports one level of supervision. Real factories may need 2–3 levels (human → manager → squad → worker). Does Attractor's design generalize, or does it implicitly cap at one?
5. **Spec evolution.** Attractor's NLSpecs are static markdown. spec-driven-ai-dev.md treats the spec as a versioned, iteratively-refined document with a "pending observations buffer." Is there a place in Attractor for spec amendments to be written back as artifacts of a run? Likely a custom handler — but it isn't shown.
6. **Context fidelity vs. layered probing.** Attractor's fidelity modes manage *LLM context*; the baseline's layering principle manages *epistemic context* (which abstraction layer is being probed). Both are about scoping what's "in scope" at a given step — is there a unified model?
7. **Provider-aligned profiles vs. agent personas.** Attractor's provider profiles are model-identity layers, not role personas (Planner/Reviewer/etc.). A factory will likely need both: provider profile × role persona, composed. Attractor doesn't address composition.
8. **Single-threaded graph traversal.** Attractor's single-threaded execution simplifies state but may bottleneck a many-agent factory. The supervisor loop and `parallel` handler are the only fan-out points — is that enough leverage for "one human, many agents"?
