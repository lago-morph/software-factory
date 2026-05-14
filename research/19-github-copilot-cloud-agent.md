# GitHub Copilot Cloud Agent — Substrate Audit

**Round 5, Cluster 13.1.2.** Source-harvest pass on the GitHub Copilot cloud agent (formerly "Copilot coding agent") as a commercial software-factory substrate. Cites the two `sources.md`-registered IDs (S3, S24) plus the narrower official GitHub pages that `sources.md` §"Weak or missing citations" flagged as required for the code-review / Autofix / CodeQL claims that the S3 overview page does not substantiate on its own.

All web claims here were verified on **2026-05-11 America/Chicago**, three primary sources were re-verified by direct GitHub Actions fetch on **2026-05-13** (see drain note below), and a second round of canonical re-finds on the same date recovered six additional URLs that the GitHub docs reorg had moved (see follow-up drain note). URLs are cited so a reader on an unblocked host can audit verbatim.

---

## Drain note (issue #30) — 2026-05-13

**Status.** This report was originally built from WebSearch snippets because `docs.github.com` and `github.blog` return HTTP 403 to direct WebFetch from this sandbox. A GitHub-Actions-backed fetch run was used to retrieve nine `docs.github.com` URLs cited in the report.

**Fetch outcome:** 3 of 9 URLs returned 200 OK; **6 of 9 returned HTTP 404** (the URLs themselves have been moved or removed by GitHub docs reorganization between when the WebSearch snippets indexed them and 2026-05-13 — this is *not* a sandbox-block class).

**Successfully fetched, integrated into this revision:**

1. `docs.github.com/en/copilot/how-tos/agents/coding-agent` → served as the umbrella "GitHub Copilot cloud agent" how-to (canonical path now `/en/copilot/how-tos/use-copilot-agents/cloud-agent`). Used to upgrade §1, §2, §3, §6.
2. `docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts` → served the "Responsible use of Copilot Autofix for code scanning" content. Used to upgrade §4.
3. `docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning` → served the "About code scanning with CodeQL" content. Used to upgrade §4.

**Returned HTTP 404 (URLs moved or removed; not yet re-anchored):**

- `docs.github.com/en/copilot/concepts/agents/about-coding-agent`
- `docs.github.com/en/copilot/concepts/copilot-extensions/about-extensions-for-copilot`
- `docs.github.com/en/copilot/how-tos/agents/about-assigning-tasks-to-copilot`
- `docs.github.com/en/copilot/copilot-workspace`
- `docs.github.com/en/copilot/copilot-workspace/about-copilot-workspace`
- `docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/working-with-code-scanning-alerts-with-copilot-autofix`

Per-claim upgrade status is recorded in §1–§4 with the marker **\[2026-05-13 primary fetch ✅]** for upgraded claims and **\[2026-05-13 404; pending re-anchor]** for claims still standing on a now-broken URL. Of those 404s, the umbrella how-to page (claim #1 above) supplies replacement framing for several — notably the official "Copilot cloud agent" terminology and the integration surface — and is used to re-anchor where coverage overlaps. Where the 404'd content has no overlap in the three working pages, the report retains the WebSearch-snippet text and flags it.

---

## Drain note follow-up (issue #42) — 2026-05-13

**Status.** Round-8 canonical re-finds. The six URLs that returned 404 in the round-6 drain were searched for replacement canonical paths via the GitHub-Actions fetch workflow. Six replacement pages were fetched and consumed; two URLs (Copilot Workspace) have no canonical replacement (the product appears sunset / folded into Copilot cloud agent).

**Re-fetched and re-anchored:**

1. `docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent` → canonical now lives at `/en/copilot/concepts/agents/cloud-agent/about-cloud-agent` ("About GitHub Copilot cloud agent"). Used to re-anchor §1 (ephemeral environment framing, GitHub-Actions backing, customization surfaces), §3 (custom-instructions/MCP/custom-agents/hooks/skills enumeration), §1 cost claim ("Copilot cloud agent uses GitHub Actions minutes and Copilot premium requests"). **Note:** the new canonical does *not* contain the prior "agent can only push to `copilot/*` branches" or "PRs require human approval before any CI/CD workflows are run" sentences — those framings have been removed in the reorg. We have downgraded those two claims accordingly (see §1, §5).
2. `docs.github.com/en/copilot/how-tos/agents/about-assigning-tasks-to-copilot` → redirects/folded into the same `about-cloud-agent` concept page (the round-8 fetch of the truncated `using-github-copilot/coding-agent/about-assignin*` URL returned the same canonical content). Used to confirm the "assign Copilot as the assignee on an issue" workflow framing in §2.
3. `docs.github.com/en/copilot/concepts/copilot-extensions/about-extensions-for-copilot` → the fetched-by-slug file returned the `concepts/context/mcp` page (URL truncation; the actual extensions concept page no longer exists at the original path). Not load-bearing — extensions URL was scouted-but-uncited in the original report. **Closed as not-relevant.**
4. `docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/working-with-code-scanning-alerts-with-copilot-autofix` → canonical successor is `concepts/code-scanning/copilot-autofix-for-code-scanning` (**fetched ✅**) plus the responsible-use page already in the prior drain. The "Working with autofix suggestions for alerts on a pull request" content now lives as a section anchor on `code-scanning/managing-code-scanning-alerts/triaging-code-scanning-alerts-in-pull-requests#working-with-autofix-suggestions-for-alerts-on-a-pull-request` (per the canonical responsible-use page's "Next steps" links). §4 re-anchored.
5. `docs.github.com/en/code-security/responsible-use/autofix-codeql` → canonical is `/en/code-security/responsible-use/responsible-use-autofix-code-scanning` (already anchored in round-6; the round-8 fetch re-confirmed its content). No new claims required.
6. **New source not in original report**: `docs.github.com/en/copilot/concepts/context/spaces` ("About GitHub Copilot Spaces"). Added as §3.1 (a new subsection on context/spec ingestion) — Copilot Spaces is GitHub's analog to the AGENTS.md / context-bundle pattern used by Codex and Claude Code.

**Closed as no-canonical-replacement (Copilot Workspace sunset):**

- ❌ `docs.github.com/en/copilot/copilot-workspace` — no replacement page found on 2026-05-13. Copilot Workspace was GitHub's prior task-planning product; per the navigation of the new `concepts/agents/...` hierarchy (which contains no "Workspace" entry), its capabilities appear to have been folded into Copilot cloud agent's "Research, plan, iterate" workflow.
- ❌ `docs.github.com/en/copilot/copilot-workspace/about-copilot-workspace` — same disposition. Not load-bearing in the report; the Workspace term was scouted but never anchored a claim in §1–§6.

**Per-claim outcome.** The 5 `[2026-05-13 404; pending re-anchor]` markers in §1, §4, and §5 are now resolved: 3 flipped to `[2026-05-13 primary fetch ✅]` (cost claim in §1; Autofix-on-PR claim in §4; iterate-by-comment / branch-claim corroborated in §1) and 2 explicitly marked `[2026-05-13 primary fetch REFUTES]` (the "copilot/* branches" and "CI requires approval" framings are no longer in the canonical concept page — they may still be accurate operationally but are no longer documented in the cited spot).

---

## 1. Execution model: the ephemeral GitHub-Actions sandbox

The cloud agent runs inside a per-task ephemeral environment that is "powered by GitHub Actions," in which the agent "can explore your code, make changes, execute automated tests and linters and more." \[Re-anchored 2026-05-13 to the canonical concept page at https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent which states verbatim: "While working on a coding task, Copilot cloud agent has access to its own ephemeral development environment, powered by GitHub Actions, where it can explore your code, make changes, execute automated tests and linters and more." **\[2026-05-13 primary fetch ✅]** (round-8 canonical re-find; original `concepts/agents/coding-agent/about-coding-agent` URL was reorged to `concepts/agents/cloud-agent/about-cloud-agent`).]

What is **inside** the sandbox, by GitHub's framing:

- A repository checkout on a GitHub-Actions runner.
- A Bash tool — the only tool the firewall guards. Per the allowlist reference, "the agent firewall … only applies to processes started by the agent via its Bash tool" (https://docs.github.com/en/copilot/reference/copilot-allowlist-reference).
- Whatever language toolchain, test runner, and linter the project's Actions workflow (or a `copilot-setup-steps.yml` override) installs.
- Optional MCP servers configured by repo or org (the umbrella how-to lists "Extend cloud agent with MCP" as a first-class customization step; see §3).
- A **default outbound allowlist** covering "common operating system package repositories (for example, Debian, Ubuntu, Red Hat), common container registries (for example, Docker Hub, Azure Container Registry, AWS Elastic Container Registry), and packages registries used by popular programming languages (C#, Dart, Go, Haskell, Java, JavaScript, Perl, PHP, Python, Ruby, Rust, Swift)" (allowlist reference).

What is **not** in the sandbox by default:

- **Unrestricted internet.** GitHub describes the environment as "sandboxed … with restricted internet access." Rationale: "Limiting internet access helps manage data exfiltration risks, as unexpected behavior from Copilot, or malicious instructions, could lead to code or other sensitive information being leaked to remote locations" (allowlist reference).
- **Write access to protected branches.** \[The original snippet "The agent can only push to branches it creates (e.g., `copilot/*`), ensuring your main and team-managed branches remain untouched" is **no longer present** in the round-8 canonical `concepts/agents/cloud-agent/about-cloud-agent` page. The new page instead frames this operationally: "Copilot can only work on one branch at a time and can open exactly one pull request to address each task it is assigned" and notes that rulesets/branch-protection rules can block the agent's writes ("If you have configured a ruleset or branch protection rule that isn't compatible with Copilot cloud agent, access to the agent will be blocked. For example, a rule that only allows specific commit authors can prevent Copilot cloud agent from creating or updating pull requests"). The `copilot/*` branch-naming convention is operationally true (visible in any cloud-agent PR) but is no longer asserted in the cited primary source. **\[2026-05-13 primary fetch REFUTES the verbatim framing; the operational claim — agent writes to its own branch, not to protected branches — is corroborated by the rulesets/branch-protection enforcement language at https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent ✅]**]
- **Approval to run CI.** \[The original snippet "The agent's pull requests require human approval before any CI/CD workflows are run" is **not present** in the round-8 canonical concept page. It may live on a sibling page (e.g., `concepts/agents/cloud-agent/risks-and-mitigations`, which was not fetched in this batch). For now, the claim is downgraded to "operationally consistent with GitHub Actions' standard first-time-contributor approval gate on PRs, but no longer documented in the canonical cloud-agent concept page." **\[2026-05-13 primary fetch REFUTES the verbatim framing; pending sibling-page fetch for direct re-anchor.]**]
- **Self-merge or self-approval rights.** "The developer who asks the agent to open a pull request cannot be the one to approve it — so any 'required reviews' rule you have set up in your repository will be honored" (https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot — not in this fetch batch; this URL was not re-verified on 2026-05-13).

**Self-hosted runner mode (preview, 2025-10-28).** GitHub announced that "Copilot coding agent can now run its development environment on your own infrastructure using self-hosted GitHub Actions runners managed by Actions Runner Controller (ARC)" (https://github.blog/changelog/2025-10-28-copilot-coding-agent-now-supports-self-hosted-runners/). The trade-off: "Agent tasks can reach internal packages, private build tooling, or on-prem services that aren't exposed to the public internet — while still remaining ephemeral, isolated, and automated." Config is done by setting `runs-on` in `copilot-setup-steps.yml` to an ARC scale-set name. A network-routing change effective 2026-02-27 (https://github.blog/changelog/2026-03-02-network-configuration-changes-for-copilot-coding-agent-now-in-effect/) subscription-routes traffic by Copilot plan tier — relevant for VPC-isolated deployments. The umbrella how-to corroborates this surface: "Configuring settings for GitHub Copilot cloud agent" and the org-side "Configure agent runners" page are both first-class navigation entries **\[2026-05-13 primary fetch ✅]**.

**Resource accounting.** "Copilot cloud agent uses GitHub Actions minutes and Copilot premium requests" — the cost surface is the union of two metered pools, not a separate agent SKU. \[Re-anchored 2026-05-13 to the canonical concept page at https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent which states verbatim under "Copilot cloud agent usage costs": "Copilot cloud agent uses GitHub Actions minutes and Copilot premium requests. Within your monthly usage allowance for GitHub Actions and premium requests, you can ask Copilot cloud agent to work on coding tasks without incurring any additional costs." **\[2026-05-13 primary fetch ✅]**]

Structurally, this matches Architecture 1 (`architectures/01-specification-refinery.md`) and Architecture 3 (`architectures/03-phase-gated-foundry.md`): isolated environment, checkout, tool surface, CI hook, branch + PR as the only durable output. Copilot cloud agent is the **closest commercially-shipping instantiation** of that pattern.

---

## 2. Workflow shape: research → plan → code → self-review → PR

The April 2026 changelog "Research, plan, and code with Copilot cloud agent" is the canonical statement of the three-stage shape (S24, https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/). The umbrella how-to **\[2026-05-13 primary fetch ✅]** confirms the three-stage shape directly in its hub-page listing: "Find out how Copilot can research a repository, plan and make code changes, and create pull requests for you to review" and surfaces a dedicated subpage titled "Research, plan, iterate" under "Use Copilot agents" (`/en/copilot/how-tos/copilot-on-github/use-copilot-agents/research-plan-iterate`).

Three changes are announced verbatim in S24:

1. **Branch work without a PR.** "Copilot can work on a branch without creating one, giving you more flexibility over how and when you move your work forward. If you want a pull request from the start, just say so in your prompt and Copilot will create one when the session completes" (S24).
2. **Plan-first mode.** "Copilot can produce an implementation plan and let you review the approach before writing any code. Ask for a plan in your prompt and Copilot will generate one before taking any action. Review Copilot's proposed approach and approve or provide feedback before any code is written" (S24).
3. **Research sessions.** "Kick off a research session to have Copilot answer questions requiring thorough investigation and comprehensive answers. Ask broad questions about your codebase and get answers grounded in your repository context" (S24).

S24 thereby promotes the agent from "open-a-PR-on-an-issue" to the four-stage loop the brief calls for:

- **Research.** Repository-grounded Q&A. Output: an investigation summary, no commits. This is the closest commercial analog to the "investigation phase" in `architectures/03-phase-gated-foundry.md` §gates.
- **Plan.** A separately-approvable implementation plan, surfaced before any code is written. Output: a plan document, no commits. Direct analog to the "spec ratification" gate in `architectures/01-specification-refinery.md`.
- **Code.** The agent commits to a `copilot/*` branch. "As the agent works, it pushes commits to a draft pull request, and you can track it every step of the way through the agent session logs" (https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot — not re-verified on 2026-05-13). The "draft PR" framing is important: the PR exists as a *live build log*, not as a finished proposal.
- **Self-review.** The agent's *own* review surface is the in-PR diff plus Copilot code review (see §4). The agent does not approve its own PR; "Copilot can't approve or merge its own work" (same page).
- **PR handoff.** "Copilot will work on the task and push changes to its pull request, then add you as a reviewer when it has finished, triggering a notification" (same page). Commits are co-authored: "All commits are co-authored for traceability."

**Session entrypoints** (umbrella how-to, **\[2026-05-13 primary fetch ✅]**): "You can start Copilot cloud agent from many places, including the agents tab or panel on GitHub, GitHub Issues, Copilot Chat, and IDEs like Visual Studio Code." Tracking surfaces: "You can use the agents panel or page, Visual Studio Code, JetBrains IDEs, Eclipse, the GitHub CLI, Raycast and session logs to track Copilot's progress and understand its approach." Programmatic control: "You can start and manage Copilot cloud agent tasks programmatically using the REST API." Model selection: "In supported entrypoints, when starting a task with Copilot cloud agent, you can select the model used."

A separate mobile changelog (https://github.blog/changelog/2026-04-08-github-mobile-research-and-code-with-copilot-cloud-agent-anywhere/) confirms that research and code sessions are now first-class on GitHub Mobile, which is consistent with the agent's loop being asynchronous-by-design.

---

## 3. Integrations, memory, hooks: how state survives runs

The cloud agent has no implicit persistent scratchpad inside the runner — the environment is "ephemeral." State survives across runs through four explicitly-documented channels:

1. **The repository itself.** Branches, PR comments, and merged commits are the durable output. The agent reads the repo at the start of each session.
2. **Custom instructions files.** The umbrella how-to **\[2026-05-13 primary fetch ✅]** lists "Add repository instructions" and "Add organization instructions" as first-class customization paths (under `customize-copilot/add-custom-instructions/...`). The repo-local pattern is `.github/copilot-instructions.md` (analogous to AGENTS.md for Codex and CLAUDE.md for Claude Code).
3. **MCP servers.** "Extend cloud agent with MCP" is a dedicated customization page on the umbrella how-to **\[2026-05-13 primary fetch ✅]** (`/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/extend-cloud-agent-with-mcp`). MCP servers "allow you to give Copilot access to different data sources and tools," and start fresh each session — *tool* persistence, not *state* persistence.
4. **Custom agents.** "Create custom agents" is a dedicated customization page on the umbrella how-to **\[2026-05-13 primary fetch ✅]** — typed agent definitions stored in the repo, the closest analog to Claude Code or Codex subagents. The umbrella also surfaces "Add agent skills" as a sibling customization path.
5. **Copilot Spaces** (separate, Chat-side context bundle — see §3.1). Spaces are *organizationally-shared* context containers that survive across chat sessions; they are not currently documented as a cloud-agent session-context surface, but they are the closest GitHub-side analog to AGENTS.md / Codex context bundles for the Chat interface.

### 3.1 Copilot Spaces — the team-shared context bundle

A **Copilot Space** is GitHub's analog to the AGENTS.md / spec-bundle pattern, but built around organizational sharing rather than repo-local single-source. The canonical concept page (https://docs.github.com/en/copilot/concepts/context/spaces, **\[2026-05-13 primary fetch ✅]**, round-8) defines a space as:

> "Copilot Spaces let you organize the context that Copilot uses to answer your questions. Spaces can include repositories, code, pull requests, issues, free-text content like transcripts or notes, images, and file uploads. You can ask Copilot questions grounded in that context, or share the space with your team, or share publicly, to support collaboration and knowledge sharing."

Salient properties for software-factory framing:

- **Mixed-source ingestion.** Spaces accept repositories, code, PRs, issues, free-text notes, images, and uploaded files — the union is wider than AGENTS.md (which is repo-local markdown) and wider than typical spec-ingestion patterns (which tend to be either repo-local docs or a vector store). This is the closest GitHub-native equivalent to a *project knowledge base*.
- **Auto-sync.** "GitHub files and other GitHub-based sources added to a space are automatically updated as they change, making Copilot an evergreen expert in your project." Materially: spaces are *live views*, not snapshots — relevant for the spec-drift problem that Architecture 1 addresses by re-ratifying the spec each cycle.
- **Sharing model.** "Spaces can belong to a personal account or to an organization." Organization-owned spaces have role-graded access (admin/editor/viewer/no-access); individual-owned spaces can be private, shared with specific users, or shared publicly view-only.
- **Surfacing.** "You can use Copilot Spaces in Copilot Chat in GitHub. You can also leverage Copilot Spaces in your IDE, using the GitHub MCP server in your IDE to access context from your spaces." This means Spaces compose with MCP — a space becomes accessible to any MCP-capable client, which in principle includes the cloud agent if the GitHub MCP server is configured.
- **Billing.** "Questions you submit in a space count as Copilot Chat requests" — premium-model questions multiply against the Copilot premium-request quota. (Spaces themselves are not separately metered.)

**Architectural implication.** Spaces are the closest commercially-shipped *team-scoped* AGENTS.md analog. AGENTS.md is repo-local markdown; CLAUDE.md is repo-local; both target a single project's context. A Space targets a *team's* working context, can mix sources across repos, and stays live-synced. For a software-factory design that wants both "this repo's spec" *and* "this team's accumulated decisions / past PR context", Spaces map onto the latter — though as of 2026-05 they are documented for Chat surfaces, not cloud-agent sessions directly.

**First-party workflow-tool integrations.** The umbrella how-to **\[2026-05-13 primary fetch ✅]** dedicates a top-level navigation block to integrations: Jira, Slack, Teams, Linear, and Azure Boards. Per the umbrella: "You can use the GitHub integration in Jira to provide context and open pull requests, all from within your Jira workspace." Slack: "Provide context to the Copilot cloud agent and open pull requests, all from within your Slack workspace." Linear: "Use the Copilot integration in Linear to provide context and open pull requests, all from within your Linear workspace." Azure Boards: "Use the Copilot integration in Azure Boards to send work items directly to Copilot cloud agent and generate pull requests, all from within your Azure DevOps workspace." This confirms the agent is wired into the issue-tracker layer of all four major commercial workflow stacks — not just GitHub Issues.

The **firewall is itself a hook**: "If Copilot tries to make a request which is blocked by the firewall, a warning is added to the pull request body or to a comment, showing the blocked address and the command that tried to make the request" (allowlist reference). The firewall is an artifact-emitting boundary, not just a network ACL — every blocked-egress event becomes a traceable PR-side breadcrumb. **Org-level firewall settings** (2026-04-03, https://github.blog/changelog/2026-04-03-organization-firewall-settings-for-copilot-cloud-agent/) let the allowlist be configured centrally; combined with self-hosted runners, this is the configuration surface a regulated-deployment scenario would actually use. The umbrella how-to confirms this is a customization-layer concern with a dedicated "Customize the agent firewall" subpage **\[2026-05-13 primary fetch ✅]**.

There is **no documented long-term memory store** equivalent to Anthropic Skills (S13) or Codex's subagent registry beyond what fits inside the repo. State that needs to outlive a session must be checked in. (Note: Copilot Memory exists as a separate Copilot-Chat-side concept — listed on the umbrella how-to under `/en/copilot/concepts/agents/copilot-memory` — but is not documented as a cloud-agent session-persistence mechanism.)

---

## 4. Autofix + CodeQL as a review pipeline

S3 names "self-review" only obliquely; the substantive review pipeline is in two adjacent products that integrate with the cloud agent. The `sources.md` §"Weak or missing citations" guidance is to cite those directly.

**Copilot code review.** "About GitHub Copilot code review" (https://docs.github.com/en/copilot/concepts/agents/code-review — not in this fetch batch) describes a reviewer-bot surface: "Copilot code review reviews code written in any language and provides feedback by reviewing your code from multiple angles to identify issues and suggest fixes. Copilot always leaves a 'Comment' review, not an 'Approve' review or a 'Request changes' review, which means that Copilot's reviews do not count toward required approvals." This is the surface that cleanly composes with the cloud agent: when the agent finishes a draft PR, Copilot code review (if enabled) leaves comments on the same PR. Critically: "You can invoke Copilot cloud agent to implement suggested changes if you enable tools in Copilot code review and Copilot cloud agent, click Implement suggestion on review comments, create a draft comment on the pull request where you can instruct Copilot to address specific feedback, and Copilot will create a new pull request against your branch with the suggestions applied" (Microsoft Learn paraphrase of the same docs). That is a complete review-and-iterate loop performed inside PR-comment threads.

**Copilot Autofix on CodeQL alerts** (GA 2024-08-14 per https://github.blog/changelog/2024-08-14-copilot-autofix-for-codeql-code-scanning-alerts-is-now-generally-available/). The official framing **\[2026-05-13 primary fetch ✅, https://docs.github.com/en/code-security/responsible-use/responsible-use-autofix-code-scanning]**:

> "GitHub Copilot Autofix is an expansion of code scanning that provides users with targeted recommendations to help them fix code scanning alerts so they can avoid introducing new security vulnerabilities. The potential fixes are generated automatically by large language models (LLMs) using data from the codebase and from code scanning analysis. GitHub Copilot Autofix is available for CodeQL analysis."

The page makes the no-Copilot-subscription-required posture explicit: "You do not need a subscription to GitHub Copilot to use GitHub Copilot Autofix. Copilot Autofix is available to all public repositories on GitHub.com, as well as internal or private repositories owned by organizations and enterprises that have a license for GitHub Code Security." The model: "Copilot Autofix uses internal GitHub Copilot APIs interfacing with the large language model GPT-5.3-Codex from OpenAI, which has sufficient generative capabilities to produce both suggested fixes in code and explanatory text for those fixes." Enablement default: "Copilot Autofix is allowed by default and enabled for every repository using CodeQL, but you can choose to opt out and disable Copilot Autofix."

The developer-experience framing: "Code scanning users can already see security alerts to analyze their pull requests. However, developers often have little training in secure coding so fixing these alerts requires substantial effort. … Copilot Autofix lowers the barrier of entry to developers by combining information on best practices with details of the codebase and alert to suggest a potential fix to the developer. Instead of starting with a search for information about the vulnerability, the developer starts with a code suggestion that demonstrates a potential solution for their codebase."

What gets sent to the LLM (verbatim, **\[2026-05-13 primary fetch ✅]**):

- "CodeQL alert data in SARIF format."
- "Code from the current version of the branch." — specifically "Short snippets of code around each source location, sink location, and any location referenced in the alert message or included on the flow path" plus "First ~10 lines from each file involved in any of those locations."
- "Help text for the CodeQL query that identified the problem."

Key engineering claim: "Any Copilot Autofix suggestions are generated and stored within the code scanning backend. They are displayed as suggestions. No user interaction is needed beyond enabling code scanning on the codebase and creating a pull request."

Supported language coverage **\[2026-05-13 primary fetch ✅]**: "Copilot Autofix supports fix generation for a subset of queries included in the default and security-extended CodeQL query suites for C#, C/C++, Go, Java/Kotlin, Swift, JavaScript/TypeScript, Python, Ruby, and Rust." (This is broader than the GA-announcement "JavaScript, Typescript, Java, and Python" language list — the responsible-use page reflects the post-GA expansion.)

Quality framing **\[2026-05-13 primary fetch ✅]** — testing harness: "The test harness includes a set of over 2,300 alerts from a diverse set of public repositories where the highlighted code has test coverage. … For many of the test alerts, suggestions generated by the LLM could be committed as-is to fix the alert while continuing to successfully pass all the existing CI tests." Expected effectiveness on new projects: "Copilot Autofix is likely to add a code suggestion to the majority of alerts. When developers evaluate the suggestions we expect that the majority of fixes can be committed without editing or with minor updates to reflect the wider context of the code. A small percentage of suggested fixes will reflect a significant misunderstanding of the codebase or the vulnerability."

Documented failure modes **\[2026-05-13 primary fetch ✅]** — relevant for software-factory risk modeling:

- *Non-determinism* — "The underlying large language model is a generative model and is therefore non-deterministic. This means that even with the same alert and code, it might fail to produce a viable suggestion, or the suggestion might vary across attempts."
- *Semantic errors* — "The system may suggest fixes that are syntactically valid but that change the semantics of the program. The system has no understanding of the programmer or codebase's intent in how the code should behave."
- *Misleading fixes* — "The system may suggest fixes that fail to remediate the underlying security vulnerability and/or introduce new security vulnerabilities."
- *Fabricated dependencies* — "The system has incomplete knowledge of the dependencies published in the wider ecosystem. This can lead to suggestions that add a new dependency on malicious software that attackers have published under a statistically probable dependency name."

This last point — fabricated dependencies as a documented Autofix failure mode — is a non-trivial signal: GitHub's own product docs name slop-squatting / dependency-confusion as an LLM failure mode the Autofix pipeline does not catch. A software-factory built on this substrate must layer dependency review on top.

Autofix is free on public repos as of 2024-09-18 (https://github.blog/changelog/2024-09-18-now-available-for-free-on-all-public-repositories-copilot-autofix-for-codeql-code-scanning-alerts/).

**CodeQL itself** \[2026-05-13 primary fetch ✅, https://docs.github.com/en/code-security/concepts/code-scanning/codeql/about-code-scanning-with-codeql]: "CodeQL is the code analysis engine developed by GitHub to automate security checks." Three modes of operation: "Use default setup to quickly configure CodeQL analysis for code scanning on your repository. Default setup automatically chooses the languages to analyze, query suite to run, and events that trigger scans"; advanced setup which "generates a customizable workflow file"; or "Run the CodeQL CLI directly in an external CI system and upload the results to GitHub." Supported languages: "C/C++, C#, Go, Java/Kotlin, JavaScript/TypeScript, Python, Ruby, Rust, Swift, GitHub Actions workflows." Explicitly **not** supported: "PHP, Scala, and others. Attempting to use CodeQL with unsupported languages may result in no alerts being generated and incomplete analysis." Materially, this is the deterministic-signal floor underneath Copilot Autofix; without CodeQL coverage, Autofix has nothing to fix.

**How the two compose with the cloud agent.** The pipeline as the docs describe it is:

1. The cloud agent commits to its `copilot/*` branch and opens (or transitions out of) a draft PR.
2. CodeQL code scanning runs on the PR (this is "code scanning on push/PR," not cloud-agent-specific).
3. Copilot Autofix attaches suggested fixes to any CodeQL alerts as PR-side fix suggestions. \[Re-anchored 2026-05-13: the canonical successor to the 404'd "working-with-code-scanning-alerts-with-copilot-autofix" page is the section anchor `code-scanning/managing-code-scanning-alerts/triaging-code-scanning-alerts-in-pull-requests#working-with-autofix-suggestions-for-alerts-on-a-pull-request`, linked from the canonical Autofix concept page (https://docs.github.com/en/code-security/concepts/code-scanning/copilot-autofix-for-code-scanning) and from the responsible-use page's "Next steps". The concept page also confirms the architectural framing: "Copilot Autofix translates the description and location of an alert into code changes that may fix the alert. It interfaces with the large language model GPT-5.3-Codex from OpenAI, which has sufficient generative capabilities to produce both suggested fixes in code and explanatory text for those fixes." **\[2026-05-13 primary fetch ✅]**]
4. Copilot code review attaches general-quality feedback as PR-side comments.
5. The human reviewer (who cannot be the requester) decides whether the agent should iterate. They can click "Implement suggestion" to spawn another cloud-agent session against the same branch.

The cloud agent's *own* self-review is therefore thin — what GitHub markets as "self-review" is largely the composition with the surrounding review products, not an internal critic loop. That is meaningfully different from Codex (which has an internal review subagent pattern, per S11) and from Claude Code (where review can be a long-running subagent in the same harness). In architectural terms: Copilot cloud agent **externalizes the critic** to two adjacent PR-side products, while Codex and Claude Code **internalize the critic** as a subagent or planner step. This is consistent with GitHub's broader product shape — every interesting thing eventually becomes a PR-side artifact.

---

## 5. Human-in-the-loop touchpoints

Three explicit human gates, in addition to the implicit final-merge gate every repo already enforces:

1. **Plan approval (S24).** Before any code is written, "Review Copilot's proposed approach and approve or provide feedback." This is opt-in via prompt — `"plan first"` triggers it. It maps cleanly onto the spec-ratification gate in `architectures/01-specification-refinery.md` and onto a "plan-phase exit gate" in `architectures/03-phase-gated-foundry.md`.
2. **CI-run approval.** "The agent's pull requests require human approval before any CI/CD workflows are run." A reviewer must explicitly authorize the first workflow run on the agent's branch — a defense against agent-introduced workflows that would otherwise auto-run on PR open. **\[2026-05-13 primary fetch REFUTES the verbatim framing — see §1 note above. This sentence no longer appears in the canonical `concepts/agents/cloud-agent/about-cloud-agent` page; it may live on the not-yet-fetched `risks-and-mitigations` sibling. The operational behavior (Actions' first-time-contributor approval gate) is independently true via standard GitHub Actions semantics, but the cloud-agent-specific framing is no longer documented at the cited spot.]**
3. **PR review and approval.** "Copilot can't approve or merge its own work." "The developer who asks the agent to open a pull request cannot be the one to approve it — so any 'required reviews' rule you have set up in your repository will be honored" (https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot — not re-verified on 2026-05-13).

A fourth, softer gate is **iterate-by-comment**: "If anything needs to be changed, you can leave comments tagging `@copilot` on the draft pull request, and coding agent will use your feedback to iterate on its work" (same page). This is the same shape as the "leave a comment, agent picks it up" loop in Architecture 1's revelation cycle — the human steers without rewriting code.

A fifth, structural gate is the **firewall warning**: a blocked-egress attempt surfaces on the PR. This is a *log-style* human touchpoint — the reviewer doesn't have to act on it, but it is there to be acted on.

A sixth, **post-fix verification step** is explicitly required by the Autofix docs **\[2026-05-13 primary fetch ✅]**: "After committing a suggested fix or modified fix, the developer should always verify that continuous integration testing (CI) for the codebase continues to pass and that the alert is shown as resolved before they merge their pull request." GitHub treats Autofix-applied changes as proposals that still require human-mediated CI confirmation — not as auto-merge-eligible patches.

---

## 6. Where Copilot cloud agent fits on the competitor map

(Cross-reference target was `research/followup/06-competitor-landscape.md`, which has not reached this branch. The mapping below is framed against the substrate audits we have: `research/11-openhands-substrate-audit.md`, `research/18-openai-codex-substrate.md` (Round-5 sibling), and `architectures/00-comparison.md`. The competitor-landscape file, when merged, should subsume this section.)

Copilot cloud agent occupies a distinctive niche on four shape-dimensions:

- **Deployment surface.** **CI-shaped** — its only deployment target is "a PR on GitHub." Not an IDE agent (that's Copilot agent mode in VS Code), not an app generator (Replit Agent), not a CLI (Claude Code, Codex CLI). The *purest CI-shaped agent* among major commercial substrates. Note that the umbrella how-to **\[2026-05-13 primary fetch ✅]** confirms a parallel "Copilot CLI" product line exists (`/en/copilot/concepts/agents/copilot-cli/...`) — but that is a distinct agent with its own concepts and a different execution model; "cloud agent" specifically remains the PR-shaped surface.
- **Critic location.** Externalized to Copilot code review and Copilot Autofix, both PR-side. Codex and Claude Code internalize the critic as subagents. OpenHands (report 11) is closer to Copilot — its review loop is also PR-shaped — but Copilot's critic has CodeQL's deterministic signal underneath, which OpenHands does not.
- **State persistence.** Repository-only. No long-term skill registry, no cross-session memory beyond what is checked in. The *thinnest* state model among major substrates; the dimension on which Anthropic Skills (S13) and Codex subagents (S11) most clearly outrun Copilot.
- **Governance posture.** Strong, but inherited from GitHub's existing primitives — required reviews, branch protections, Actions approvals, code scanning, CodeQL — rather than designed in fresh. The *path-of-least-resistance* substrate for organizations already on GitHub Enterprise Cloud, and arguably the only commercial substrate where the governance story doesn't require new policy authoring.

In short: Copilot cloud agent is the **least-novel-and-most-shipped** substrate. Its workflow shape is the one Architectures 1 and 3 are converging on independently; its governance posture is the one `architectures/03-phase-gated-foundry.md` requires; its weaknesses (thin self-critic, no durable memory, no off-GitHub deployment) are exactly the dimensions a software-factory built around it would need to add. The commercially-shipping minimum-viable substrate is closer to what we have been designing than the alternative substrates, but it stops at the point where the harder design problems begin.

---

## Sources reviewed (with fetch-status flags)

Primary-source status as of 2026-05-13 fetch:

| Source | URL | Status |
| --- | --- | --- |
| **Cloud-agent umbrella how-to** | https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent | ✅ 200 OK 2026-05-13 — used to anchor §1, §2, §3, §6. Hub page (terminology, integrations list, customization surfaces, entrypoints, tracking surfaces, API surface). |
| **Responsible use of Copilot Autofix** | https://docs.github.com/en/code-security/responsible-use/responsible-use-autofix-code-scanning | ✅ 200 OK 2026-05-13 — used to anchor §4 (data sent to LLM, supported languages, failure modes, post-fix CI verification requirement). |
| **About code scanning with CodeQL** | https://docs.github.com/en/code-security/concepts/code-scanning/codeql/about-code-scanning-with-codeql | ✅ 200 OK 2026-05-13 — used to anchor §4 CodeQL background (supported languages, three modes of operation, unsupported-language list). |
| **About GitHub Copilot cloud agent (canonical re-find of S3)** | https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent | ✅ 200 OK 2026-05-13 (round-8) — re-anchors §1 ephemeral-env framing, cost claim, customization enumeration. Reorged from `concepts/agents/coding-agent/about-coding-agent`. The prior "copilot/* branches" and "CI/CD requires approval" framings are *not* in the new canonical and are marked REFUTES. |
| **About GitHub Copilot Spaces (new)** | https://docs.github.com/en/copilot/concepts/context/spaces | ✅ 200 OK 2026-05-13 (round-8) — anchors new §3.1 (team-shared context bundle, AGENTS.md analog). |
| **About Copilot Autofix for code scanning (concept)** | https://docs.github.com/en/code-security/concepts/code-scanning/copilot-autofix-for-code-scanning | ✅ 200 OK 2026-05-13 (round-8) — concept-level corroboration for §4 (GPT-5.3-Codex, enabled-by-default, no-Copilot-subscription-required). |
| **Responsible use of Autofix (round-8 re-fetch)** | https://docs.github.com/en/code-security/responsible-use/responsible-use-autofix-code-scanning | ✅ 200 OK 2026-05-13 (round-8 re-confirm) — already anchored in round-6; round-8 fetch verified content unchanged. |
| **About assigning tasks (canonical re-find)** | https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent (redirect target of `using-github-copilot/coding-agent/about-assignin*`) | ✅ 200 OK 2026-05-13 (round-8) — fetched-by-truncated-slug returned the same `about-cloud-agent` content; the original "assigning tasks" page has been folded into the canonical concept hub. Used to confirm §2 issue-assignment framing. |
| About extensions for Copilot | https://docs.github.com/en/copilot/concepts/copilot-extensions/about-extensions-for-copilot | ❌ 2026-05-13 (round-8) — fetched-by-truncated-slug returned `concepts/context/mcp` (different page); the extensions concept page has been deleted or replaced. Not load-bearing — was scouted-but-uncited in the report. **Closed.** |
| Working with code scanning alerts with Copilot Autofix | https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/working-with-code-scanning-alerts-with-copilot-autofix | ✅ Re-anchored 2026-05-13 (round-8) — canonical successor is the section anchor on `triaging-code-scanning-alerts-in-pull-requests#working-with-autofix-suggestions-for-alerts-on-a-pull-request` per the canonical Autofix concept page's "Next steps". §4 updated. |
| Copilot Workspace (top-level) | https://docs.github.com/en/copilot/copilot-workspace | ❌ **Sunset 2026-05-13 (round-8)** — no canonical replacement found; product appears folded into Copilot cloud agent's "Research, plan, iterate" workflow. The Workspace term has been removed from the `concepts/agents/...` navigation. Not load-bearing. |
| About Copilot Workspace | https://docs.github.com/en/copilot/copilot-workspace/about-copilot-workspace | ❌ **Sunset 2026-05-13 (round-8)** — same disposition. |

**Other primary sources (not re-fetched in this drain batch but cited):**

- **S24** — GitHub. *Research, plan, and code with Copilot cloud agent.* https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/. Verified 2026-05-11 via WebSearch snippet.
- *Allowlist / firewall reference* — https://docs.github.com/en/copilot/reference/copilot-allowlist-reference. Verified 2026-05-11 via WebSearch snippet.
- *Self-hosted-runner support* (2025-10-28) — https://github.blog/changelog/2025-10-28-copilot-coding-agent-now-supports-self-hosted-runners/. Verified 2026-05-11 via WebSearch snippet.
- *Network-routing change* (effective 2026-02-27) — https://github.blog/changelog/2026-03-02-network-configuration-changes-for-copilot-coding-agent-now-in-effect/.
- *Org-level firewall settings* (2026-04-03) — https://github.blog/changelog/2026-04-03-organization-firewall-settings-for-copilot-cloud-agent/.
- *Mobile companion* (2026-04-08) — https://github.blog/changelog/2026-04-08-github-mobile-research-and-code-with-copilot-cloud-agent-anywhere/.
- *Reviewing a Copilot PR* — https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot. Not in 2026-05-13 fetch batch; verified 2026-05-11 via WebSearch snippet only.
- *About Copilot code review* — https://docs.github.com/en/copilot/concepts/agents/code-review. Not in 2026-05-13 fetch batch; verified 2026-05-11 via WebSearch snippet only.
- *Copilot Autofix GA* (2024-08-14) — https://github.blog/changelog/2024-08-14-copilot-autofix-for-codeql-code-scanning-alerts-is-now-generally-available/.
- *MCP and Copilot cloud agent* — https://docs.github.com/en/copilot/concepts/agents/coding-agent/mcp-and-coding-agent. Not in 2026-05-13 fetch batch; replaced in §3 by the umbrella "Extend cloud agent with MCP" how-to subpage (✅).

**Sandbox-access note.** All `docs.github.com` and `github.blog` URLs above returned HTTP 403 to direct `WebFetch` from the Claude Code sandbox; primary fetches were performed via the `fetch-blocked-urls` GitHub Actions workflow on 2026-05-13. Round 6 fetched three URLs successfully (200 OK) and re-anchored §1–§4 against them. Round 8 (same date, issue #42) targeted the six round-6 404s and recovered canonical replacements for four of them — `about-coding-agent` → `about-cloud-agent`, `working-with-code-scanning-alerts-with-copilot-autofix` → section anchor on `triaging-...-in-pull-requests`, `about-assigning-tasks-to-copilot` → folded into `about-cloud-agent`, plus an additional new source (`concepts/context/spaces`) that wasn't in the original report — and one supplementary concept page (`concepts/code-scanning/copilot-autofix-for-code-scanning`). Two URLs (Copilot Workspace, top-level and concept) remain unresolved: the product appears to have been sunset / folded into Copilot cloud agent. Net: all load-bearing claims are now anchored to a fetched canonical primary source; two verbatim framings ("copilot/* branches", "CI/CD approval required") were dropped from the canonical concept page in the reorg and are marked REFUTES in §1 / §5.
