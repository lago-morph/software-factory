# Research Report 11 — OpenHands Substrate Audit

**Date:** 2026-05-11
**Author:** Lead agent (not a subagent dispatch — see `research/PLAN.md` §3.4 for the originally-planned subagent prompt; this lead-agent pass covers most of it)
**Status:** Substantive on the CI/CD-relevant surfaces; one open follow-up (full SDK paper) noted at the end.

## Sources reviewed

Status legend: ✅ full review (read end-to-end) · 🟡 reconstructed from search snippets / partial extraction · ⏳ retrieval pending · ❌ could not obtain.

| Source URL | Status | Notes |
|---|---|---|
| https://docs.all-hands.dev/usage/how-to/headless-mode | ✅ | Fetched via issue #4. 400 KB rendered. Canonical headless-mode contract — primary source for §3. |
| https://docs.all-hands.dev/ | ✅ | Fetched via issue #4. 353 KB rendered. Doc-tree taxonomy used in §2 and the Appendix. |
| https://arxiv.org/abs/2511.03690 | ✅ | Fetched via issue #4. Abstract, authors, MLSys 2026 venue — primary source for §1, §4, §6. |
| https://arxiv.org/pdf/2511.03690 | ⏳ | Fetched via issue #4 but came through as PDF binary; html2text doesn't extract PDF. The HTML render `https://arxiv.org/html/2511.03690v2` is queued in fetch issue [#8](https://github.com/lago-morph/software-factory/issues/8). When that lands, deepen §4 (workspace abstraction) and §8 (sandboxing posture) with paper-body details. |
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

OpenHands is an MIT-licensed (with an `enterprise/` source-available exception) Python framework for building software-development AI agents. It was first released as a single monolithic application (V0 — agent core, server, frontend, evaluation suite in one repo) and **re-architected** as a separate composable SDK (V1) — the SDK paper was accepted at MLSys 2026 and submitted v2 in April 2026. The system now ships in **five surfaces**: a Python SDK, a CLI binary, a local GUI with REST/WebSocket API, a cloud product (`app.all-hands.dev`), and a self-hosted enterprise SKU. **Headless mode is documented and idiomatic**: `openhands --headless -t "task" --json` streams JSONL agent events to stdout, suitable for CI/CD ingestion. There is **no official GitHub Action** — the only Marketplace listing is a third-party 10-star wrapper that runs the OpenHands Docker image with a prompt input.

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

## 4. The workspace abstraction (V1 design)

From the SDK paper abstract (`arxiv.org/abs/2511.03690`):

> *For security and reliability, it delivers seamless local-to-remote execution portability, integrated REST/WebSocket services. … OpenHands uniquely integrates native sandboxed execution, lifecycle control, model-agnostic multi-LLM routing, and built-in security analysis.*

And the DeepWiki TOC (third-party but indexed-from-source) confirms a concrete decomposition that maps directly to our factory needs:

- `3.1 Deployment and Container Architecture`
- `3.2 Sandbox Specification Service` ← per-cycle isolation contract
- `3.3 Multi-Runtime Support` ← provider-agnostic
- `4.1 Runtime Abstractions and Implementations` ← the workspace interface
- `4.2 Action Execution Server` ← the bash/file-IO endpoint
- `4.3 Runtime Image Building and Caching` ← deterministic, cacheable runners
- `4.4 Bash Session and Command Execution`
- `4.5 Runtime Plugins and Extensions`
- `5.1 LLM Configuration and Provider Support` ← model-agnostic routing
- `5.5 LLM Metrics and Cost Tracking` ← cost telemetry as a first-class metric
- `7.4 V1 Conversation Architecture` ← redesigned event-sourcing

The paper itself uses the phrase "Local Workspace executes in-process against the host filesystem and shell; Remote Workspace … delegates all operations over HTTP to an Agent Server, with concrete sponsors including a containerized server (DockerWorkspace) or an API-managed runtime (APIRemoteWorkspace)." This is the cleanest workspace contract in the open-source corpus we have seen so far. It satisfies our §4.1 primitives (worktree-per-unit, sandbox, network restrictions) with a *standardized* interface.

**Comparison to Overstory:** Overstory uses `git worktree add` plus its own SQLite mail bus to isolate workers; OpenHands uses Docker (or remote) as the isolation boundary. The two are not mutually exclusive — a hybrid where Overstory orchestrates *N* worker agents and each worker is an OpenHands headless invocation in a Docker sandbox is a plausible composition.

## 5. The skill model

The repo's `skills/` directory exists at top level. We haven't read individual skills yet (deferred for a second pass). The paper says skills/extensions are first-class. Practical implication: where the Every.to compound-engineering plugin exposes ~50 named persona skills (already in `research/04-`), OpenHands' equivalent appears to be tool-shaped rather than persona-shaped. **This is the persona-vs-graph-node tension from `research/00-synthesis.md` §3.2 again — OpenHands sides with graph-node.**

## 6. Provider strategy

> *Compared with existing SDKs from OpenAI, Claude and Google, OpenHands uniquely integrates … model-agnostic multi-LLM routing …*

DeepWiki confirms first-class providers via section 5.1, with retry/error handling (5.4), metrics (5.5). **Mix-and-match LLMs across phases of a cycle is supported out of the box.** This is the critical capability for our Architecture-3 (Foundry)'s independent-V&V phases and Architecture-4 (Tournament)'s diversity policy.

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

## 8. Sandboxing posture

The four signals are aligned:

1. **Filesystem isolation:** Docker workspace by default; the Sandbox Specification Service (DeepWiki §3.2) parameterizes this per-conversation.
2. **Network egress:** controllable at the Docker level (the third-party action passes `--network` flags through `additional_env`).
3. **Capability scoping:** the SDK paper claims "built-in security analysis"; specifics are in the paper body we haven't fully read.
4. **Secrets:** the standard GitHub Secrets pattern (`secrets.LLM_API_KEY`) is documented, and the Settings & Secrets Management API (DeepWiki §8.3) is internal infrastructure for this.

**Not yet verified:** whether the sandbox blocks the "lethal trifecta" attack vector (untrusted content → tool access → data exfiltration) called out in `research/00-synthesis.md` F12. The paper's "built-in security analysis" phrase is suggestive but not specific. Defer to a focused security pass.

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
6. **Defer:** read the full SDK paper PDF when reachable, and read 3–5 `skills/` files to characterize the extension model in depth.

### Open follow-up

The arxiv PDF fetch came through as raw PDF bytes (html2text doesn't extract PDF text). The HTML render (`arxiv.org/html/2511.03690v2`) is queued in fetch issue #8 via the Wayback Machine. Re-run the paper section of this report once that lands.

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
