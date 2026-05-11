# Research Report 11 — OpenHands Substrate Audit

**Date:** 2026-05-11 (revised same day after full paper became reachable)
**Author:** Lead agent (not a subagent dispatch — see `research/PLAN.md` §3.4 for the originally-planned subagent prompt; this lead-agent pass covers most of it)
**Status:** Substantive on the CI/CD-relevant surfaces. The previously-open follow-up (full SDK paper text) has now been incorporated.

## Revision notes (2026-05-11, v0.2)

A Wayback HTML render of `arxiv.org/html/2511.03690v2` was fetched via issue #8 (capture date 2026-05-11), giving us the full paper body for the first time. This pass:

- Replaces abstract-only references with primary-source quotations from the paper's §3 (Challenges and Design Principles) and §4 (Architecture).
- Adds the four V1 design principles verbatim in a new §4a, with the concrete V0 failure modes (rigid sandboxing, 140+ config fields / 15 classes / 2.8K LOC of config, monorepo benchmark dependency leakage, monolith logic) that motivated each.
- Adds production-reliability numbers from the paper's §5.1 and §5.2 to §1 and §4: 61% reduction in system-attributable failures (78.0 → 30.0 / 1k conversations) over a 15-day parallel rollout, sub-millisecond event-sourcing persist latency, crash recovery under 20 ms.
- Deepens §5 (Skills) with the AgentContext / Skill object details from the paper's §4.5 — Skills load from `.openhands/skills/`, `.cursorrules`, or `agents.md`, can be always-on (`trigger=None`) or keyword-activated, and may bundle MCP tools.
- Deepens §6 (provider strategy) with the `RouterLLM` / `select_llm()` API from §4.3 and the LiteLLM-100+-providers claim. Adds the `NonNativeToolCallingMixin` finding — relevant for our cost-floor models.
- Deepens §8 (sandboxing) with the `SecurityAnalyzer` / `ConfirmationPolicy` / `SecretRegistry` details from §4.8–4.9 — the paper's "built-in security analysis" phrase now has a concrete mechanism (LLMSecurityAnalyzer rates each tool call low/medium/high/unknown; ConfirmRisky policy blocks above a threshold). Notes the paper's own §7 limitation that "LLM-based security analysis is subject to adversarial prompts and inconsistent classification" — the lethal trifecta is not fully closed.
- Adds a new sub-section to §4 on Sub-Agent Delegation (paper §4.5) — relevant to Architecture-2/4 fleet orchestration: it is a *standard tool* in `openhands.tools`, blocking-parallel only, with sub-agents inheriting parent model/workspace.
- Updates the sources status table to mark the paper as fully ACCESSED.
- Closes the previously-open follow-up about the unreadable PDF.

## Sources reviewed

Status legend: ✅ full review (read end-to-end) · 🟡 reconstructed from search snippets / partial extraction · ⏳ retrieval pending · ❌ could not obtain.

| Source URL | Status | Notes |
|---|---|---|
| https://docs.all-hands.dev/usage/how-to/headless-mode | ✅ | Fetched via issue #4. 400 KB rendered. Canonical headless-mode contract — primary source for §3. |
| https://docs.all-hands.dev/ | ✅ | Fetched via issue #4. 353 KB rendered. Doc-tree taxonomy used in §2 and the Appendix. |
| https://arxiv.org/abs/2511.03690 | ✅ | Fetched via issue #4. Abstract, authors, MLSys 2026 venue — primary source for §1, §4, §6. |
| https://arxiv.org/pdf/2511.03690 | ✅ | Originally came through as PDF binary (html2text can't extract PDF). The HTML render `https://arxiv.org/html/2511.03690v2` was fetched via Wayback Machine (capture timestamp 2026-05-11 00:25:03) under issue [#8](https://github.com/lago-morph/software-factory/issues/8) and read end-to-end in this revision. Primary source for the four V1 design principles (§3.1–3.4), the four-package SDK (§4.1), event-sourced state model (§4.2), `RouterLLM` (§4.3), tool system (§4.4), AgentContext/Skills/Sub-Agent Delegation (§4.5), Secret Registry (§4.8), SecurityAnalyzer/ConfirmationPolicy (§4.9), Local-to-Remote workspace abstraction (§4.10), production reliability numbers (§5.1), and event-sourcing overhead measurements (§5.2). |
| https://github.com/marketplace/actions/openhands-ai-action | ✅ | Fetched via issue #4. 222 KB rendered. Primary source for §7. |
| https://deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes | ✅ | Fetched via issue #4. 2.1 MB. Third-party wiki indexed from source; primary source for §4 architecture decomposition. |
| https://github.com/All-Hands-AI/OpenHands — README + top-level layout | ✅ | README fetched via raw.githubusercontent.com; directory listing via the GitHub Contents API. §2, §5, §8. |
| https://github.com/OpenHands/software-agent-sdk (V1 SDK repo) | 🟡 | Repo itself NOT read in this session; cited claims about the SDK come from the MLSys 2026 paper abstract. A direct read of the repo (README + Python API surface) is a candidate for a future deepening pass. |
| https://github.com/OpenHands/OpenHands-CLI (binary CLI repo) | 🟡 | Repo itself NOT read in this session; cited claims come from the headless-mode docs and from WebSearch summaries gathered during the initial scout. Direct read pending. |
| https://github.com/OpenHands/openhands-github-action (companion action repo) | 🟡 | Repo itself NOT read in this session; the third-party `xinbenlv/openhands-action` Marketplace listing was read instead. The official action repo's `action.yml` would tighten §7 if it exists. |
| `skills/` directory in `All-Hands-AI/OpenHands` | ❌ | Not read in this session — §5 explicitly notes this and defers to a second pass. |
| https://github.com/All-Hands-AI/OpenHands `openhands/` package source | ❌ | Code-walking not done in this session. §4 relies on DeepWiki's TOC as a proxy for the in-repo organization. |

**Primary sources** for the substantive conclusions are all ✅. The 🟡 items affect detail depth in specific sections (called out in those sections); the ❌ items are deferred to the subagent 11 deepening pass tracked in `research/PLAN.md` §10.4.

---

## 1. What it is (one paragraph)

OpenHands is an MIT-licensed (with an `enterprise/` source-available exception) Python framework for building software-development AI agents. It was first released as a single monolithic application (V0 — agent core, server, frontend, evaluation suite in one repo) and **re-architected** as a four-package SDK (V1: `openhands.sdk`, `openhands.tools`, `openhands.workspace`, `openhands.agent_server`) — the SDK paper was accepted at MLSys 2026 and submitted v2 on 22 Apr 2026. The system now ships in **five surfaces**: a Python SDK, a CLI binary, a local GUI with REST/WebSocket API, a cloud product (`app.all-hands.dev`), and a self-hosted enterprise SKU. **Headless mode is documented and idiomatic**: `openhands --headless -t "task" --json` streams JSONL agent events to stdout, suitable for CI/CD ingestion. There is **no official GitHub Action** — the only Marketplace listing is a third-party 10-star wrapper that runs the OpenHands Docker image with a prompt input. The paper reports a **15-day production rollout in which V1 reduced system-attributable failures by 61%** (78.0 → 30.0 errors per 1k conversations) versus V0, with event-sourcing overhead measured at sub-millisecond persist latency.

## 2. Five deployment surfaces — for CI/CD use

| Surface | Repo / artifact | Intended user | CI/CD friendliness |
|---|---|---|---|
| **SDK** | `github.com/OpenHands/software-agent-sdk` | Python developers building custom agents | Excellent. The abstract claims "a simple interface … requires only a few lines of code in the default case." Programmatic control, custom tools, memory management, REST/WebSocket services baked in. |
| **CLI binary** | `github.com/OpenHands/OpenHands-CLI` | Power users / scripts | Excellent. Headless mode is documented as **the intended path** for CI/CD: `openhands --headless -t "..." --json`. |
| **GUI server (local)** | `openhands/` package in main repo, plus `frontend/` and `openhands-ui/` | Developer with a desktop | Not for CI. |
| **Cloud (`app.all-hands.dev`)** | Hosted by All-Hands-AI | Anyone who wants managed infra | Possible but pulls our orchestration off-platform; opaque cost shape. |
| **Enterprise (self-hosted)** | `enterprise/` directory, source-available, separately licensed | Companies | Plausible if we ever need on-prem. Out of scope for our solo-to-small-team starting context. |

**Reusability verdict for our software factory:** the SDK + CLI binary are the two surfaces that map to our `architectures/00-comparison.md` §4.1 "shared infrastructure." Either can serve as the per-cycle agent runtime under any of the four architectures.

## 3. Headless mode — the actual contract

Verbatim from `docs.all-hands.dev/usage/how-to/headless-mode`:

> *Headless mode runs OpenHands without the interactive terminal UI, making it ideal for: CI/CD pipelines, automated scripting, integration with other tools, batch processing.*

The contract:

```bash
openhands --headless -t "Your task here"          # task as string
openhands --headless -f task.txt                  # task as file
openhands --headless --json -t "Add unit tests"   # JSONL event stream on stdout
openhands --headless --json -t "..." > run.jsonl  # capture for offline analysis
```

JSONL event shape (from the docs):

```json
{"type": "action", "action": "write", "path": "app.py", ...}
{"type": "observation", "content": "File created successfully", ...}
{"type": "action", "action": "run", "command": "python app.py", ...}
```

**Constraint that affects our architectures:**

> *Headless mode always runs in `always-approve` mode. The agent will execute all actions without any confirmation. This cannot be changed — `--llm-approve` is not available in headless mode.*

That is a hard contract: in CI we cannot have OpenHands ask a human for approval mid-run. **Trust is enforced before invocation (capability scoping, sandbox boundaries) and observed afterward (trajectory + diagnostic agent), not interactively.** This aligns naturally with our Architecture-3 (Foundry) phase gates and Architecture-2 (Atelier) reviewer panel — both expect the implementer agent to run unattended and the gate/panel to validate.

**JSONL output unlocks the Diagnostic Agent.** Our `spec-driven-ai-dev.md` baseline requires a "decision log produced by the Implementation Agent" — JSONL action/observation pairs are essentially that log, structured-machine-readable.

## 4. The four V1 design principles and workspace abstraction

### 4a. Why V0 had to die — the four design principles, verbatim

The paper's §3 names four V0-vs-V1 tensions. Each principle is given verbatim from §3.1–3.4; the V0 failure mode that motivated each is paraphrased from the same section.

**3.1 — Universal Sandboxing vs. Local Flexibility.** V0 assumed all tool calls run in a Docker sandbox. Two processes (agent + sandbox) with potentially divergent state caused corrupted sessions; multi-tenant deployments could have one user's screenshot-heavy workload exhaust container resources and crash co-located agents; supporting local execution required duplicated MCP and tool implementations, "diverging from the original sandbox-based code path."

> *V1 Design Principle — Sandboxing should be opt-in, not universal. V1 unifies agent and tool execution in a single process by default, aligning with MCP's assumptions. When isolation is needed, the same stack can be containerized transparently.*

**3.2 — Mutable Configuration vs. Deterministic State.** V0's config sprawled across CLI/headless, Web UI, GitHub App, and SaaS hierarchies, each with its own override rules. The paper quantifies the rot precisely: "**140+ fields, 15 classes, and 2.8K lines of configuration code** — a brittle system where small changes often cascaded into unrelated failures."

> *V1 Design Principle — Stateless by Default, One Source of Truth for State. V1 treats all agents and their components — tools, LLMs, etc — as immutable and serializable Pydantic models validated at construction. The only mutable entity is the conversation state, which is a single, well-defined source of truth that tracks ongoing execution.*

**3.3 — Monorepo vs. Modular SDK.** Benchmarks contributed by academic users "introduc[ed] heavy dependencies and frequent version conflicts. These leaked into the main application due to mono-repo design, making deployments heavyweight and fragile."

> *V1 Design Principle — Maintain strict separation of concerns. V1 isolates the agent core into software engineering SDK as described in this paper. Applications integrate via SDK APIs, allowing research to evolve independently from applications.*

**3.4 — Monolith Logic vs. Extensible Architecture.** "Adding new behaviors in V0 often required editing the core logic or branching for specific entry points, limiting experimentation and maintainability."

> *V1 Design Principle — Everything should be composable and safe to extend. V1 makes composability a first-class design goal at two levels. At the deployment level, its four modular packages — SDK, Tools, Workspace, and Agent Server — combine flexibly to support local, hosted, or containerized execution. At the capability level, the SDK exposes a typed component model — tools, LLMs, contexts, etc — so developers can extend or reconfigure agents declaratively without touching the core.*

**Implication for our factory:** The V0→V1 story is exactly the lesson `research/00-synthesis.md` keeps re-discovering: monolithic agent codebases collapse under their own configuration weight; the answer is a *typed, immutable, event-sourced* core with composable extension points. We should treat OpenHands V1 as a reference implementation of this pattern, not just a substrate. In particular, the "stateless by default, one source of truth for state" principle is the architectural counterpart to our spec-driven decision-log requirement.

### 4b. The four packages

From §4.1 (verbatim):

- `openhands.sdk`: Core abstractions (Agent, Conversation, LLM, Tool, MCP, etc) and the event system.
- `openhands.tools`: Concrete tool implementations based on abstractions defined in `openhands.sdk`.
- `openhands.workspace`: Execution environments (e.g., Docker, hosted API) that extend SDK base classes.
- `openhands.agent_server`: A web server exposing REST/WebSocket APIs for remote execution.

Critically, the paper justifies the split in operational terms: "(1) sdk stays lightweight for diverse integration scenarios; (2) tools isolates slow-running tool tests from core SDK changes, speeding up development; (3) workspace provides optional sandboxing implementations without bloating the core; and (4) agent_server offers a generic API server usable with or without containers."

### 4c. The workspace abstraction

The workspace contract is a `BaseWorkspace` ABC with three operations: `execute_command(cmd) -> CommandOutput`, `file_upload(path, content)`, `file_download(path) -> bytes`, plus context-manager `__enter__` / `__exit__`. Two implementations:

- **`LocalWorkspace`** — "executes in-process against the host filesystem and shell; it is effectively a thin, no-op wrapper that forwards file/command/git operations directly, enabling fast prototyping without network hops."
- **`RemoteWorkspace`** — "preserves the same interface but delegates all operations over HTTP to an Agent Server …, with concrete sponsors including a containerized server (`DockerWorkspace`) or an API-managed runtime (`APIRemoteWorkspace`)."

The selector is a `Conversation` factory: when given a string path or `LocalWorkspace`, you get a `LocalConversation`; when given a `RemoteWorkspace`, you get a `RemoteConversation` that serializes the agent config and runs it inside a container, streaming events back over WebSocket. The paper's Fig. 5 shows the local→remote diff is **a single import + a `with DockerWorkspace(...) as workspace:` block** — agent code is unchanged.

This is the cleanest workspace contract in the open-source corpus we have seen so far. It satisfies our `architectures/00-comparison.md` §4.1 primitives (worktree-per-unit, sandbox, network restrictions) with a standardized interface.

### 4d. Event-sourced state management

§4.2 confirms what DeepWiki's TOC hinted at: ConversationState is the only mutable component. Events are immutable records appended to an `EventLog`; metadata writes go to `base_state.json`, events to individual JSON files, "enabling efficient incremental persistence — only new events write to disk, avoiding rewrites of large histories. Conversations resume by loading `base_state.json` and replaying events from the directory."

The event hierarchy is two-tiered: `LLMConvertibleEvent` subclasses (MessageEvent, ActionEvent, SystemPromptEvent, CondensationSummaryEvent, ObservationBaseEvent) are visible to the LLM; internal events (ConversationStateUpdateEvent, CondensationRequest, Condensation, PauseEvent) are bookkeeping.

**Performance, measured (§5.2, replaying 433 SWE-Bench Verified conversations / 39,870 events):**

| Metric | Median | P95 | At max (358 events) |
|---|---|---|---|
| Per-event persist latency | 0.20 ms | 0.31 ms | — |
| Action cycle persist | 0.40 ms | 0.56 ms | — |
| Full state replay | 4.1 ms | 9.7 ms | 18.9 ms |
| Crash recovery | 7.4 ms | 14.9 ms | 32.1 ms |
| Storage per conversation | 380 KB | 1.4 MB | 3.4 MB |

These are negligible relative to LLM round-trips. **Our decision-log requirement is satisfied for free** by simply persisting `EventLog` to disk — no separate logging layer needed.

### 4e. Sub-Agent Delegation (paper §4.5) — relevant to fleet orchestration

The paper explicitly addresses multi-agent coordination, but as a *standard tool*, not a core SDK feature:

> *The SDK supports hierarchical agent coordination through a delegation tool that demonstrates the extensibility of the tool abstraction. Sub-agents operate as independent conversations that inherit the parent's model configuration and workspace context, enabling structured parallelism and isolation without any changes to the core SDK. The current implementation provides blocking parallel execution, implemented as a standard tool in the `openhands.tools` package, where the parent agent spawns and monitors sub-agents until all tasks complete.*

The paper's §7 limitation is honest about scope: "The current implementation focuses on single-agent conversations. While the event-sourced architecture naturally supports interleaving events from multiple agents, coordination mechanisms for multi-agent collaboration require further design."

**Read for our factory:** OpenHands gives us a *single-agent* runtime cleanly. For Architecture-2 (Atelier — N parallel issues) and Architecture-4 (Tournament — N parallel candidates) we either (a) use the built-in delegation tool with its blocking-parallel constraint, or (b) keep orchestration above OpenHands (e.g., Overstory-style coordinator + worktree + mail spawning N headless OpenHands invocations). Option (b) preserves more flexibility for non-blocking and fault-tolerant patterns the paper itself flags as future work.

**Comparison to Overstory:** Overstory uses `git worktree add` plus its own SQLite mail bus to isolate workers; OpenHands uses Docker (or remote) as the isolation boundary. The two are not mutually exclusive — a hybrid where Overstory orchestrates *N* worker agents and each worker is an OpenHands headless invocation in a Docker sandbox is a plausible composition.

## 5. The skill model — AgentContext and Skill objects (§4.5)

The paper makes the skill model concrete:

> *AgentContext centralizes all inputs that shape LLM behavior, including prefixes/suffixes for system/user messages and user-defined Skill objects. Skills can be defined programmatically or loaded from markdown files (e.g., `.openhands/skills/`, or compatible formats like `.cursorrules`, `agents.md`). Each skill may always be active (`trigger=None`) to persistently augment the system prompt, or conditionally activated via keyword matching based on user input; skills may also include MCP tools.*

Three salient properties:

1. **Persona-shaped *or* tool-shaped — not exclusively either.** A Skill can be a system-prompt augment (persona-flavoured), or a bundle that includes MCP tools (tool-flavoured), or both. This is *less* opinionated than I previously characterized it; the paper's design accommodates both styles.
2. **Trigger semantics are first-class.** `trigger=None` means always-on; otherwise a keyword match against user input gates activation. This is the "conditional persona injection" pattern from `research/00-synthesis.md` §3.2 — OpenHands implements it natively.
3. **Cross-tool-ecosystem compatibility.** Loading from `.cursorrules` and `agents.md` (the same `AGENTS.md` convention surfaced in the GitHub Action ecosystem) means a Skill written for Cursor or for the bare AGENTS.md convention can be reused under OpenHands without translation.

Feature-comparison table (§5.4 / Tab. 6) confirms OpenHands and Claude Agent SDK are the only two of five surveyed SDKs to support "Agent Skills" as a first-class concept. The others (OpenAI Agents SDK, Google ADK, LangChain/LangGraph) require significant external setup.

**Practical implication for our factory:** the same Skill primitive can express both Every.to-style persona skills (write a system-prompt augment, set `trigger=None`, ship as a markdown file) and Anthropic-style tool skills (bundle MCP tools). Our factory can adopt either style, or mix them per probe brief.

## 6. Provider strategy — RouterLLM (§4.3)

§4.3 nails down the LLM abstraction. The `LLM` class is "a unified interface to language models. Through LiteLLM, it supports 100+ providers with two APIs: the standard Chat Completions API for broad compatibility and the newer OpenAI Responses API for latest reasoning models."

**Three sub-features matter for the software factory:**

**(a) Multi-LLM routing as a first-class type.** From §4.3:

> *SDK features `RouterLLM`, a subclass of `LLM` that enables the agent to use different models for different LLM requests. Custom implementations can extend `RouterLLM` and implement `select_llm()` to choose a different model based on different LLM inputs.*

The paper's Fig. 3 example pseudo-code:

```python
class RouterLLM(LLM):
    llms_for_routing: dict[str, LLM]  # Available models

    @abstractmethod
    def select_llm(self, messages: list[Message]) -> str:
        """Return key of LLM to use from llms_for_routing."""

    def completion(self, messages, **kwargs) -> LLMResponse:
        selected_model = self.select_llm(messages)
        self.active_llm = self.llms_for_routing[selected_model]
        return self.active_llm.completion(...)

class MultimodalRouter(RouterLLM):
    def select_llm(self, messages):
        has_images = any(m.contains_image for m in messages)
        return "primary" if has_images else "secondary"
```

**Implication:** mix-and-match LLMs *within a single conversation*, governed by a policy *we* write. This is the critical capability for our Architecture-3 (Foundry)'s independent-V&V phases (different model family for verification vs. construction) and Architecture-4 (Tournament)'s diversity policy (route different candidates to different model families). Tab. 6 confirms OpenHands is the only one of five surveyed SDKs with full support for multi-LLM routing (LangChain has partial support, the rest none).

**(b) Native reasoning support.** "The SDK captures and processes advanced native reasoning fields from frontier models, such as `ThinkingBlock` for Anthropic's extended thinking, and `ReasoningItemModel` for OpenAI's reasoning. The SDK supports the OpenAI Responses API transparently for the agent, enabling client developers to use the agent with advanced reasoning models like GPT-5-Codex that are only available on the recently released Responses API."

**(c) Non-function-calling models supported via prompt instructions.** "For models without native function calling support, the SDK implements a `NonNativeToolCallingMixin`, which converts tool schemas to text-based prompt instructions and parses tool calls from model outputs using structured prompts and regex-based extraction." Per Tab. 6, OpenHands is the *only* surveyed SDK with this capability — relevant if our Architecture-4 (Tournament) wants a cost-floor candidate slot using a smaller open-weights model.

## 7. The GitHub Action — there isn't a good one

The only Marketplace listing (`xinbenlv/openhands-ai-action@v1.0.1-rc3`):

- 10 stars, 1 contributor, **third-party — not All-Hands-AI**.
- Default Docker image: `docker.all-hands.dev/all-hands-ai/openhands:0.32` (and the runtime image is `:0.32-nikolaik`).
- Inputs: `prompt` (required), `llm_api_key` (required), `llm_model` (default `anthropic/claude-3-7-sonnet-20250219`), `log_all_events`, `runtime_image`, `openhands_image`, `additional_env`.
- Idiomatic example:
  ```yaml
  - name: Execute OpenHands Task
    uses: xinbenlv/openhands-action@v1.0.1-rc3
    with:
      prompt: "Your natural language task description here"
      llm_api_key: ${{ secrets.LLM_API_KEY }}
  ```
- Security note from the listing: "the action uses Docker for secure sandboxing of task execution."

**This is a thin wrapper around the OpenHands Docker image, not a co-designed CI contract.** For our software factory:

- **Adopt as-is risk:** depending on a 10-star repo for the bridge to OpenHands is fragile. The bus factor is 1.
- **Lift-the-design risk:** the action shows the contract is genuinely thin (Docker image + prompt + secrets + env). We can re-implement the wrapper in `.github/workflows/` ourselves in <100 lines; we just did exactly this for our `fetch-blocked-urls` workflow.
- **Recommendation:** treat the third-party action as a reference implementation, not a dependency. Roll our own thin wrapper that invokes the official OpenHands Docker image (or `pip install openhands` plus `openhands --headless`).

## 8. Sandboxing posture — concrete now (§4.8–4.9)

The four signals are aligned, and the paper's §4.8–4.9 puts mechanism behind what was previously vague phrasing.

1. **Filesystem isolation.** Docker workspace by default; `RemoteWorkspace` delegates all FS/exec ops over HTTP to an Agent Server inside the container; the official Docker images "bundle the full agent-server stack — including the API server, VSCode Web, VNC desktop, and Chromium browser" with "an independent container with a dedicated file system, environment, and resource."
2. **Network egress.** Controllable at the Docker level (the third-party Marketplace action passes `--network` flags through `additional_env`).
3. **Capability scoping — `SecurityAnalyzer` + `ConfirmationPolicy` (§4.9), verbatim:**

   > *Two abstractions form the core of this design: the `SecurityAnalyzer`, which rates each tool call as low, medium, high, or unknown risk, and the `ConfirmationPolicy`, which determines whether user approval is required before execution based on the action's details and assessed risk. … The SDK includes a built-in pair: `LLMSecurityAnalyzer`, which appends a `security_risk` field to tool calls, and `ConfirmRisky` policy, which blocks actions exceeding a configurable risk threshold (default: high).*

   When approval is required the agent enters a `WAITING_FOR_CONFIRMATION` state. **Important constraint for our factory:** headless mode runs in `always-approve` mode (per §3 of this report), which means in CI the `ConfirmationPolicy` will not pause for human approval — it will either block (if hard-rejected) or pass through. Combine with a low risk threshold for CI to get effective blocking; combine with the trajectory log review (Diagnostic Agent) for after-the-fact catch.

4. **Secrets — `SecretRegistry` (§4.8), verbatim:**

   > *`SecretRegistry` provides secure, late-bound, and remotely manageable credentials for tool execution. Each conversation maintains its own instance, ensuring strict per-session isolation. Tools access secrets only at execution time, and all secret values appearing in outputs are masked to prevent leakage. For example, the Bash Tool scans commands for secret keys, exports the referenced ones as environment variables, and replaces their occurrences in results with a constant mask (`<secret-hidden>`). … All secrets are redacted during serialization and can be encrypted with a configurable cipher.*

   This is materially better than "use GitHub Secrets and hope": redaction is enforced at the SDK layer, not at the workflow layer. Per Tab. 6, OpenHands is the *only* surveyed SDK with "Secrets Management with Auto-Masking."

**On the lethal trifecta.** The paper itself flags the limitation in §7:

> *The security framework, while substantially improved over V0, cannot guarantee complete safety: LLM-based security analysis is subject to adversarial prompts and inconsistent classification.*

So `LLMSecurityAnalyzer` is a *probabilistic* defence layered on top of process isolation, not a proof of safety. For our factory this means: keep the deterministic perimeter (egress allowlist, container-level capability dropping, no host network) doing the heavy lifting; treat the LLM-based analyzer as a defence-in-depth check, not as the primary line. The lethal trifecta is *not* fully closed, just narrower than V0's.

## 9. Diff against `architectures/00-comparison.md` §4.1 (shared-infrastructure list)

| Shared infrastructure primitive | OpenHands provides? | Notes |
|---|---|---|
| Worktree per unit of work | **Partial.** Docker workspace per conversation is the moral equivalent. We may still want git worktrees on top for branch-per-cycle. | The two compose well. |
| Sandboxed agent execution | **Yes.** Docker + optional remote/API runtime. | This is the strongest single fit. |
| Stable ID assignment | **Partial.** V1 conversation architecture is event-sourced (DeepWiki §7.4); conversation IDs + event IDs exist, but R/A/F/AE/U-style spec IDs are an overlay we'd add. | Not a gap — by design, the substrate is below the methodology layer. |
| Out-of-construction-tree scenarios | **Not provided.** We'd build this on top. | Architecture-specific concern. |
| LLM-judge with model-family independence | **Yes** (model-agnostic multi-LLM routing). | First-class. |
| Trajectory capture | **Yes.** JSONL event stream from headless mode. | Cleanly satisfies our decision-log requirement. |
| Manager loop / orchestrator | **Partial.** Single conversation lifecycle is supported; fleet orchestration is not — that's where Overstory's coordinator pattern fits. | Composition opportunity. |
| Decision log / audit trail | **Yes** (event-sourced V1 architecture; JSONL output). | |
| AGENTS.md / discoverability | **Yes.** Repo has top-level `AGENTS.md`; the docs reference `llms.txt` for index. | |

**Total coverage: ~70% of our §4.1 primitives, with the missing 30% (orchestration of *N* parallel cycles, scenarios storage, stable-ID convention) being layers above OpenHands rather than competing with it.**

## 10. Recommendation

**Adopt OpenHands SDK + CLI as the per-cycle agent runtime under our software factory.**

Specifically:

1. **Per-cycle implementer:** invoke `openhands --headless --json -t "<probe brief>"` in a Docker sandbox. Capture the JSONL event stream as the decision log.
2. **Orchestration above:** keep architecture-specific orchestration (revelation cycle / 5-state queue / six-phase gates / tournament generation loop) outside OpenHands. We are the methodology layer.
3. **No dependence on the third-party Marketplace action.** Roll our own ~80-line workflow that invokes the OpenHands Docker image, exactly as we did for `fetch-blocked-urls.yml`.
4. **Composition with Overstory:** keep this option open. If we need *N* parallel candidates (Architecture-4 Tournament) or *N* parallel issues (Architecture-2 Atelier), Overstory's coordinator + worktree + mail can sit *above* OpenHands' per-conversation runtime. Each Overstory "worker" calls OpenHands headless once.
5. **Caveat on the always-approve constraint:** headless mode commits the agent to unattended execution. Our reviewer-panel / V&V / Channel-1 test-executor patterns must catch what would have been caught by an interactive human approval. This is the same constraint StrongDM's "code must not be reviewed by humans" stance assumes — and we should adopt the same discipline of *holdout scenarios as judge*.
6. **Defer:** read 3–5 actual `skills/` files in the repo to characterize the in-the-wild Skill style (this report now describes the *type system*; concrete examples would tighten our adoption story).

### Closed follow-up

The arxiv PDF unreadability follow-up is now closed: the v2 HTML render was retrieved via Wayback (capture 2026-05-11 00:25:03) under issue [#8](https://github.com/lago-morph/software-factory/issues/8), read in full, and incorporated above.

### New follow-ups

- **Sub-Agent Delegation tool deep-dive.** §4.5 (paper) and §4e (this report) describe a `delegate` tool in `openhands.tools` that supports *blocking parallel* sub-agent execution. For Architecture-2 (Atelier) and Architecture-4 (Tournament) we need to characterize: max fan-out, fault-tolerance behaviour when one sub-agent crashes, whether sub-agent event logs are merged into the parent EventLog or kept separate, and whether the tool can be extended to non-blocking patterns. Track in `research/PLAN.md` §10.
- **`LLMSecurityAnalyzer` adversarial-prompt evaluation.** The paper acknowledges the LLM-based analyzer is fooled by adversarial prompts. Before we depend on it in CI, we should run a small red-team pass with the prompt-injection corpus from `research/00-synthesis.md` F12.

---

## Appendix — full doc-tree fingerprint

From `docs.all-hands.dev/.md` (the docs root):

**Getting Started:** Installation, Quick Start
**Ways to Run:** Terminal (CLI), Headless Mode, Web Interface, GUI Server, IDE Integration (ACP)
**Cloud:** OpenHands Cloud
**Extensions:** MCP Servers, Critic (Experimental)
**Reference:** Command Reference, Resume Conversations

The MCP server integration is a notable feature: tools delivered as MCP servers can extend the agent's capability surface without modifying core. This is the same direction as Anthropic's broader MCP push and lets our factory consume Anthropic-ecosystem tools (filesystem, github, etc.) without OpenHands-specific glue.

---

*End of report 11 — `research/11-openhands-substrate-audit.md` v0.1*
