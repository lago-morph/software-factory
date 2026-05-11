# GitHub Copilot Cloud Agent — Substrate Audit

**Round 5, Cluster 13.1.2.** Source-harvest pass on the GitHub Copilot cloud agent (formerly "Copilot coding agent") as a commercial software-factory substrate. Cites the two `sources.md`-registered IDs (S3, S24) plus the narrower official GitHub pages that `sources.md` §"Weak or missing citations" flagged as required for the code-review / Autofix / CodeQL claims that the S3 overview page does not substantiate on its own.

All web claims here were verified on **2026-05-11 America/Chicago**. The `docs.github.com` and `github.blog` hosts returned HTTP 403 to direct WebFetch from this sandbox; content was instead extracted via WebSearch result snippets, which return the same authored text. URLs are cited so a reader on an unblocked host can audit verbatim. The `blocked-urls` issue path is **not** opened for these — they are a known sandbox class, not a per-URL outage, and the snippet content is sufficient for the brief.

---

## 1. Execution model: the ephemeral GitHub-Actions sandbox

The cloud agent runs inside a per-task ephemeral environment that is "powered by GitHub Actions," in which the agent "can explore your code, make changes, execute automated tests and linters and more" (S3, https://docs.github.com/copilot/concepts/agents/coding-agent/about-coding-agent).

What is **inside** the sandbox, by GitHub's framing:

- A repository checkout on a GitHub-Actions runner.
- A Bash tool — the only tool the firewall guards. Per the allowlist reference, "the agent firewall … only applies to processes started by the agent via its Bash tool" (https://docs.github.com/en/copilot/reference/copilot-allowlist-reference).
- Whatever language toolchain, test runner, and linter the project's Actions workflow (or a `copilot-setup-steps.yml` override) installs.
- Optional MCP servers configured by repo or org (S3 calls these "integrations"; see §3).
- A **default outbound allowlist** covering "common operating system package repositories (for example, Debian, Ubuntu, Red Hat), common container registries (for example, Docker Hub, Azure Container Registry, AWS Elastic Container Registry), and packages registries used by popular programming languages (C#, Dart, Go, Haskell, Java, JavaScript, Perl, PHP, Python, Ruby, Rust, Swift)" (allowlist reference).

What is **not** in the sandbox by default:

- **Unrestricted internet.** GitHub describes the environment as "sandboxed … with restricted internet access." Rationale: "Limiting internet access helps manage data exfiltration risks, as unexpected behavior from Copilot, or malicious instructions, could lead to code or other sensitive information being leaked to remote locations" (allowlist reference).
- **Write access to protected branches.** "The agent can only push to branches it creates (e.g., `copilot/*`), ensuring your main and team-managed branches remain untouched" (S3).
- **Approval to run CI.** "The agent's pull requests require human approval before any CI/CD workflows are run."
- **Self-merge or self-approval rights.** "The developer who asks the agent to open a pull request cannot be the one to approve it — so any 'required reviews' rule you have set up in your repository will be honored" (https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot).

**Self-hosted runner mode (preview, 2025-10-28).** GitHub announced that "Copilot coding agent can now run its development environment on your own infrastructure using self-hosted GitHub Actions runners managed by Actions Runner Controller (ARC)" (https://github.blog/changelog/2025-10-28-copilot-coding-agent-now-supports-self-hosted-runners/). The trade-off: "Agent tasks can reach internal packages, private build tooling, or on-prem services that aren't exposed to the public internet — while still remaining ephemeral, isolated, and automated." Config is done by setting `runs-on` in `copilot-setup-steps.yml` to an ARC scale-set name. A network-routing change effective 2026-02-27 (https://github.blog/changelog/2026-03-02-network-configuration-changes-for-copilot-coding-agent-now-in-effect/) subscription-routes traffic by Copilot plan tier — relevant for VPC-isolated deployments.

**Resource accounting.** "Copilot cloud agent uses GitHub Actions minutes and Copilot premium requests" (S3) — the cost surface is the union of two metered pools, not a separate agent SKU.

Structurally, this matches Architecture 1 (`architectures/01-specification-refinery.md`) and Architecture 3 (`architectures/03-phase-gated-foundry.md`): isolated environment, checkout, tool surface, CI hook, branch + PR as the only durable output. Copilot cloud agent is the **closest commercially-shipping instantiation** of that pattern.

---

## 2. Workflow shape: research → plan → code → self-review → PR

The April 2026 changelog "Research, plan, and code with Copilot cloud agent" is the canonical statement of the three-stage shape (S24, https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/). Three changes are announced verbatim:

1. **Branch work without a PR.** "Copilot can work on a branch without creating one, giving you more flexibility over how and when you move your work forward. If you want a pull request from the start, just say so in your prompt and Copilot will create one when the session completes" (S24).
2. **Plan-first mode.** "Copilot can produce an implementation plan and let you review the approach before writing any code. Ask for a plan in your prompt and Copilot will generate one before taking any action. Review Copilot's proposed approach and approve or provide feedback before any code is written" (S24).
3. **Research sessions.** "Kick off a research session to have Copilot answer questions requiring thorough investigation and comprehensive answers. Ask broad questions about your codebase and get answers grounded in your repository context" (S24).

S24 thereby promotes the agent from "open-a-PR-on-an-issue" to the four-stage loop the brief calls for:

- **Research.** Repository-grounded Q&A. Output: an investigation summary, no commits. This is the closest commercial analog to the "investigation phase" in `architectures/03-phase-gated-foundry.md` §gates.
- **Plan.** A separately-approvable implementation plan, surfaced before any code is written. Output: a plan document, no commits. Direct analog to the "spec ratification" gate in `architectures/01-specification-refinery.md`.
- **Code.** The agent commits to a `copilot/*` branch. "As the agent works, it pushes commits to a draft pull request, and you can track it every step of the way through the agent session logs" (https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot). The "draft PR" framing is important: the PR exists as a *live build log*, not as a finished proposal.
- **Self-review.** The agent's *own* review surface is the in-PR diff plus Copilot code review (see §4). The agent does not approve its own PR; "Copilot can't approve or merge its own work" (same page).
- **PR handoff.** "Copilot will work on the task and push changes to its pull request, then add you as a reviewer when it has finished, triggering a notification" (same page). Commits are co-authored: "All commits are co-authored for traceability."

A separate mobile changelog (https://github.blog/changelog/2026-04-08-github-mobile-research-and-code-with-copilot-cloud-agent-anywhere/) confirms that research and code sessions are now first-class on GitHub Mobile, which is consistent with the agent's loop being asynchronous-by-design.

---

## 3. Integrations, memory, hooks: how state survives runs

The cloud agent has no implicit persistent scratchpad inside the runner — the environment is "ephemeral." State survives across runs through four explicitly-documented channels:

1. **The repository itself.** Branches, PR comments, and merged commits are the durable output. The agent reads the repo at the start of each session.
2. **Custom instructions files.** S3 names "custom instructions" as a first-class customization — `.github/copilot-instructions.md` and per-path files, analogous to AGENTS.md (Codex) and CLAUDE.md (Claude Code).
3. **MCP servers.** S3: "Model Context Protocol (MCP) servers that allow you to give Copilot access to different data sources and tools." For the cloud agent these are wired in via repo/org config (https://docs.github.com/en/copilot/concepts/agents/coding-agent/mcp-and-coding-agent) and start fresh each session — *tool* persistence, not *state* persistence.
4. **Custom agents.** S3: "custom agents that allow you to create different specialized versions of Copilot for different tasks" — typed agent definitions stored in the repo, the closest analog to Claude Code or Codex subagents.

The **firewall is itself a hook**: "If Copilot tries to make a request which is blocked by the firewall, a warning is added to the pull request body or to a comment, showing the blocked address and the command that tried to make the request" (allowlist reference). The firewall is an artifact-emitting boundary, not just a network ACL — every blocked-egress event becomes a traceable PR-side breadcrumb. **Org-level firewall settings** (2026-04-03, https://github.blog/changelog/2026-04-03-organization-firewall-settings-for-copilot-cloud-agent/) let the allowlist be configured centrally; combined with self-hosted runners, this is the configuration surface a regulated-deployment scenario would actually use.

There is **no documented long-term memory store** equivalent to Anthropic Skills (S13) or Codex's subagent registry beyond what fits inside the repo. State that needs to outlive a session must be checked in.

---

## 4. Autofix + CodeQL as a review pipeline

S3 names "self-review" only obliquely; the substantive review pipeline is in two adjacent products that integrate with the cloud agent. The `sources.md` §"Weak or missing citations" guidance is to cite those directly.

**Copilot code review.** "About GitHub Copilot code review" (https://docs.github.com/en/copilot/concepts/agents/code-review) describes a reviewer-bot surface: "Copilot code review reviews code written in any language and provides feedback by reviewing your code from multiple angles to identify issues and suggest fixes. Copilot always leaves a 'Comment' review, not an 'Approve' review or a 'Request changes' review, which means that Copilot's reviews do not count toward required approvals." This is the surface that cleanly composes with the cloud agent: when the agent finishes a draft PR, Copilot code review (if enabled) leaves comments on the same PR. Critically: "You can invoke Copilot cloud agent to implement suggested changes if you enable tools in Copilot code review and Copilot cloud agent, click Implement suggestion on review comments, create a draft comment on the pull request where you can instruct Copilot to address specific feedback, and Copilot will create a new pull request against your branch with the suggestions applied" (Microsoft Learn paraphrase of the same docs). That is a complete review-and-iterate loop performed inside PR-comment threads.

**Copilot Autofix on CodeQL alerts** (GA 2024-08-14 per https://github.blog/changelog/2024-08-14-copilot-autofix-for-codeql-code-scanning-alerts-is-now-generally-available/). The official framing: "GitHub Copilot Autofix is an expansion of code scanning that provides users with targeted recommendations to help them fix code scanning alerts so they can avoid introducing new security vulnerabilities. The potential fixes are generated automatically by large language models (LLMs) using data from the codebase and from code scanning analysis. … No user interaction is needed beyond enabling code scanning on the codebase and creating a pull request" (https://docs.github.com/en/code-security/responsible-use/responsible-use-autofix-code-scanning).

Coverage and effectiveness as of the GA announcement (2024-08-14, time-stamped per §13.4): "Code scanning autofix covers more than 90% of alert types in JavaScript, Typescript, Java, and Python, and delivers code suggestions shown to remediate more than two-thirds of found vulnerabilities with little or no editing" (same source). Autofix is free on public repos as of 2024-09-18 (https://github.blog/changelog/2024-09-18-now-available-for-free-on-all-public-repositories-copilot-autofix-for-codeql-code-scanning-alerts/).

**How the two compose with the cloud agent.** The pipeline as the docs describe it is:

1. The cloud agent commits to its `copilot/*` branch and opens (or transitions out of) a draft PR.
2. CodeQL code scanning runs on the PR (this is "code scanning on push/PR," not cloud-agent-specific).
3. Copilot Autofix attaches suggested fixes to any CodeQL alerts as PR-side fix suggestions.
4. Copilot code review attaches general-quality feedback as PR-side comments.
5. The human reviewer (who cannot be the requester) decides whether the agent should iterate. They can click "Implement suggestion" to spawn another cloud-agent session against the same branch.

The cloud agent's *own* self-review is therefore thin — what GitHub markets as "self-review" is largely the composition with the surrounding review products, not an internal critic loop. That is meaningfully different from Codex (which has an internal review subagent pattern, per S11) and from Claude Code (where review can be a long-running subagent in the same harness). In architectural terms: Copilot cloud agent **externalizes the critic** to two adjacent PR-side products, while Codex and Claude Code **internalize the critic** as a subagent or planner step. This is consistent with GitHub's broader product shape — every interesting thing eventually becomes a PR-side artifact.

---

## 5. Human-in-the-loop touchpoints

Three explicit human gates, in addition to the implicit final-merge gate every repo already enforces:

1. **Plan approval (S24).** Before any code is written, "Review Copilot's proposed approach and approve or provide feedback." This is opt-in via prompt — `"plan first"` triggers it. It maps cleanly onto the spec-ratification gate in `architectures/01-specification-refinery.md` and onto a "plan-phase exit gate" in `architectures/03-phase-gated-foundry.md`.
2. **CI-run approval.** "The agent's pull requests require human approval before any CI/CD workflows are run." A reviewer must explicitly authorize the first workflow run on the agent's branch — a defense against agent-introduced workflows that would otherwise auto-run on PR open.
3. **PR review and approval.** "Copilot can't approve or merge its own work." "The developer who asks the agent to open a pull request cannot be the one to approve it — so any 'required reviews' rule you have set up in your repository will be honored" (https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot).

A fourth, softer gate is **iterate-by-comment**: "If anything needs to be changed, you can leave comments tagging `@copilot` on the draft pull request, and coding agent will use your feedback to iterate on its work" (same page). This is the same shape as the "leave a comment, agent picks it up" loop in Architecture 1's revelation cycle — the human steers without rewriting code.

A fifth, structural gate is the **firewall warning**: a blocked-egress attempt surfaces on the PR. This is a *log-style* human touchpoint — the reviewer doesn't have to act on it, but it is there to be acted on.

---

## 6. Where Copilot cloud agent fits on the competitor map

(Cross-reference target was `research/followup/06-competitor-landscape.md`, which has not reached this branch. The mapping below is framed against the substrate audits we have: `research/11-openhands-substrate-audit.md`, `research/18-openai-codex-substrate.md` (Round-5 sibling), and `architectures/00-comparison.md`. The competitor-landscape file, when merged, should subsume this section.)

Copilot cloud agent occupies a distinctive niche on four shape-dimensions:

- **Deployment surface.** **CI-shaped** — its only deployment target is "a PR on GitHub." Not an IDE agent (that's Copilot agent mode in VS Code), not an app generator (Replit Agent), not a CLI (Claude Code, Codex CLI). The *purest CI-shaped agent* among major commercial substrates.
- **Critic location.** Externalized to Copilot code review and Copilot Autofix, both PR-side. Codex and Claude Code internalize the critic as subagents. OpenHands (report 11) is closer to Copilot — its review loop is also PR-shaped — but Copilot's critic has CodeQL's deterministic signal underneath, which OpenHands does not.
- **State persistence.** Repository-only. No long-term skill registry, no cross-session memory beyond what is checked in. The *thinnest* state model among major substrates; the dimension on which Anthropic Skills (S13) and Codex subagents (S11) most clearly outrun Copilot.
- **Governance posture.** Strong, but inherited from GitHub's existing primitives — required reviews, branch protections, Actions approvals, code scanning, CodeQL — rather than designed in fresh. The *path-of-least-resistance* substrate for organizations already on GitHub Enterprise Cloud, and arguably the only commercial substrate where the governance story doesn't require new policy authoring.

In short: Copilot cloud agent is the **least-novel-and-most-shipped** substrate. Its workflow shape is the one Architectures 1 and 3 are converging on independently; its governance posture is the one `architectures/03-phase-gated-foundry.md` requires; its weaknesses (thin self-critic, no durable memory, no off-GitHub deployment) are exactly the dimensions a software-factory built around it would need to add. The commercially-shipping minimum-viable substrate is closer to what we have been designing than the alternative substrates, but it stops at the point where the harder design problems begin.

---

## Sources cited (with S-IDs)

- **S3** — GitHub. *About GitHub Copilot cloud agent.* https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/cloud-agent/about-cloud-agent. Verified 2026-05-11.
- **S24** — GitHub. *Research, plan, and code with Copilot cloud agent.* https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/. Verified 2026-05-11.
- *Allowlist / firewall reference* — https://docs.github.com/en/copilot/reference/copilot-allowlist-reference.
- *Self-hosted-runner support* (2025-10-28) — https://github.blog/changelog/2025-10-28-copilot-coding-agent-now-supports-self-hosted-runners/.
- *Network-routing change* (effective 2026-02-27) — https://github.blog/changelog/2026-03-02-network-configuration-changes-for-copilot-coding-agent-now-in-effect/.
- *Org-level firewall settings* (2026-04-03) — https://github.blog/changelog/2026-04-03-organization-firewall-settings-for-copilot-cloud-agent/.
- *Mobile companion* (2026-04-08) — https://github.blog/changelog/2026-04-08-github-mobile-research-and-code-with-copilot-cloud-agent-anywhere/.
- *Reviewing a Copilot PR* — https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot.
- *About Copilot code review* — https://docs.github.com/en/copilot/concepts/agents/code-review.
- *Responsible use of Copilot Autofix* — https://docs.github.com/en/code-security/responsible-use/responsible-use-autofix-code-scanning.
- *Copilot Autofix GA* (2024-08-14) — https://github.blog/changelog/2024-08-14-copilot-autofix-for-codeql-code-scanning-alerts-is-now-generally-available/.
- *MCP and Copilot cloud agent* — https://docs.github.com/en/copilot/concepts/agents/coding-agent/mcp-and-coding-agent.

**Sandbox-access note.** All `docs.github.com` and `github.blog` URLs above returned HTTP 403 to direct `WebFetch` from the sandbox. Content was extracted via `WebSearch`, which surfaces page text in result snippets; the resulting quoted phrasing is verbatim from those snippets. The blocked-URL pattern is the standard `docs.github.com` / `github.blog` Cloudflare class — known and tracked elsewhere in `research/blocked-urls*.md`. No new `fetch-blocked-urls` issue was filed.
