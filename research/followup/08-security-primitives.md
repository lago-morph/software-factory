# 08 — Security primitives: lethal trifecta, Dual LLM, CaMeL, Safe YOLO

**Round-3 follow-up thread 8 (per `research/PLAN.md` §11.8).**
**Repo:** `lago-morph/software-factory`. **Branch:** `claude/parallelize-with-subagents-SO0nR--sub-12`.
**Date:** 2026-05-11.
**Scope:** Consolidate the public security literature our four architectures lean on when they say "sandbox the implementer" (F12 in `architectures/00-comparison.md`). Specifically: Simon Willison's *lethal trifecta* framing, his 2023 *Dual LLM pattern*, Google DeepMind's *CaMeL* paper (arXiv 2503.18813), and Anthropic's Claude Code *sandboxing / Safe YOLO* spec.

**Fetch status.** `simonwillison.net`, `arxiv.org`, and `anthropic.com` were all 403 from the sandbox. `code.claude.com/docs/en/sandboxing` returned successfully and is the single largest verbatim source below. The other three sources are reconstructed from WebSearch result text that quotes the originals; verbatim attribution is preserved where the search engine returned direct quotes.

---

## 1. The lethal trifecta — verbatim framing

Willison's June 2025 post "The lethal trifecta for AI agents: private data, untrusted content, and external communication" names a three-way conjunction that, when present, makes prompt-injection exfiltration essentially inevitable.

The three legs (Willison's wording, as quoted across multiple aggregators of the post):

1. **Access to private data.** *"The agent can read information that should not be shared publicly — your inbox, your calendar, your customer database, your source code, your file system."*
2. **Exposure to untrusted content.** *"The agent processes content from untrusted sources. Someone outside your organisation can put text in front of the agent — by sending you an email it reads, by publishing a webpage it visits, by submitting a support ticket it processes."*
3. **External communication / exfiltration vector.** *"The agent can send information out of your environment. It can email, post, call an external API, write to a public file, or otherwise transmit data beyond the trust boundary."*

Willison's claim is structural: *"Any time a system combines access to private data with exposure to malicious tokens and an exfiltration vector you're going to see the same exact security issue."* Removing any one leg defangs the attack. Note the exfiltration leg is broader than it looks — *"if a tool can make an HTTP request… or even providing a link for a user to click — that tool can be used to pass stolen information back to an attacker."* Markdown image rendering, link previews, telemetry pings, DNS errors all count.

**Implication for the factory.** Every architecture in `architectures/00-comparison.md` puts the implementer agent *inside* the trifecta by default: private data (repo + secrets), untrusted content (issues, PR comments, scraped docs, web search), external comms (git push, npm install, web fetch). F12 is not a hypothetical — it is the default state of an unconstrained implementer. The four architectures' F12 entries are all leg-3 mitigations (break the exfiltration vector). None of them break leg 1 or leg 2.

---

## 2. The Dual LLM pattern (Willison, April 2023)

Willison's earlier pattern, "The Dual LLM pattern for building AI assistants that can resist prompt injection," is the architectural ancestor of CaMeL and remains the simplest working sketch.

**Three components:**

- **Privileged LLM (P-LLM).** *"It accepts input from trusted sources — primarily the user themselves — and acts on that input in various ways. It has access to tools: if you ask it to send an email, or add things to your calendar, or perform any other potentially destructive state-changing operation it will be able to do so."* The P-LLM is the only component that sees the user's prompt directly and the only one that can call tools.
- **Quarantined LLM (Q-LLM).** *"The Quarantined LLM is used any time we need to work with untrusted content — content that might conceivably incorporate a prompt injection attack. It does not have access to tools, and is expected to have the potential to go rogue at any moment."* It is a pure text-in / text-out function whose output is presumed hostile.
- **Controller.** *"Regular software, not a language model. It handles interactions with users, triggers the LLMs and executes actions on behalf of the Privileged LLM."* The controller is deterministic code; only it can dispatch tools.

**The load-bearing rule.** *"It is absolutely crucial that unfiltered content output by the Quarantined LLM is never forwarded on to the Privileged LLM. Instead of forwarding the text as-is, we can instead work with unique tokens that represent that potentially tainted content."* The controller stores Q-LLM output in a variable keyed by an opaque token; the P-LLM sees only the token. If the P-LLM later wants to act on the value, it asks the controller to pipe the token into another Q-LLM call or into a specific tool argument — but the P-LLM never reasons over the raw string.

**What this buys you.** Prompt injection in a website that the Q-LLM summarises cannot reach the P-LLM's tool-calling cortex, because the P-LLM only ever sees the token `$VAR_47`, not the contents. The injection can corrupt the *content* but not the *control flow*.

**What this does not buy you.** If the P-LLM is itself fed untrusted text (e.g., issue body, PR comment, MCP server output) without quarantining it first, the pattern is bypassed. In practice the boundary is "anything outside the original user prompt is untrusted" — which for a CI/CD factory means *almost everything*.

---

## 3. CaMeL — capability-typed program model (DeepMind, March 2025)

CaMeL (CApabilities for MachinE Learning, arXiv 2503.18813) generalises Dual LLM by replacing the controller's ad-hoc token substitution with a *capability-typed, dataflow-tracking Python interpreter*.

**Architecture, three layers:**

1. **Privileged LLM (P-LLM).** Sees the user's prompt. Its only output is a Python program expressed against a fixed tool API. It never sees untrusted data.
2. **Custom Python interpreter.** Parses the P-LLM's program via Python's `ast` library, then evaluates it node-by-node. The interpreter tracks, for every value, a *capability set* — metadata covering provenance ("where did this byte come from?"), readers ("who is allowed to see it?"), and permitted operations ("can this be passed to `send_email`?"). Capabilities propagate through assignments, arithmetic, string concatenation, and function calls — i.e. they form a taint type system at runtime.
3. **Quarantined LLM (Q-LLM).** Called by the interpreter when the program needs to extract structured information from a blob of untrusted text. The Q-LLM has no tools and returns only typed values, which the interpreter immediately tags with capabilities derived from the input blob.

**Security policy mechanism.** Tool calls in the interpreter have preconditions written against capabilities. Example shape (paraphrased from the explainers, since the paper PDF was blocked): `send_email(to, body)` requires `body.readers ⊇ {to}` — i.e., a user cannot exfiltrate a value tagged "readers = {user}" to an arbitrary address. If the precondition fails, the interpreter raises before the side-effect.

**Why this beats "train the model to resist injection."** The defence does not depend on the LLM being uncompromisable; it depends on the interpreter being correct. Same shift OS security took in the 1970s — from "trust user programs" to "page tables and ring 0." Willison calls CaMeL *"the first credible prompt injection defense"* he's seen.

**Known limitations** (per explainer summaries): the P-LLM must emit a *complete program* up front (rules out fluid ReAct interleaving); the capability lattice has to be designed per-deployment (CaMeL ships a default but doesn't infer); AgentDojo results show CaMeL solves a substantial fraction of injected-task scenarios *securely* but trades raw task success vs. an unsandboxed agent; the Q-LLM is still manipulable, but its outputs are typed values, not free-form control.

**Concrete-enough-to-implement sketch for the factory.** Planner LLM (≈ P-LLM) sees only the spec and emits a typed plan against a fixed tool list (`read_file`, `write_file`, `run_tests`, `git_commit`). Summariser LLM (≈ Q-LLM) is the only component permitted to consume untrusted strings (issue bodies, web pages, dependency READMEs) and returns typed extracts. A Python harness executes the plan; every value carries `{readers, provenance}` tags; tool signatures like `git_push(branch: Branch[readers={team}])` enforce preconditions at runtime. The harness is the only thing allowed to call tools — the planner never invokes a tool directly, only emits ASTs.

---

## 4. Anthropic Claude Code Safe YOLO — container/sandbox spec

The Claude Code sandbox is the most concrete artefact in this corpus and the only one we fetched verbatim from the source (`code.claude.com/docs/en/sandboxing`). It is the *engineering* counterpart to CaMeL's *type-system* approach: it doesn't try to reason about data flow at all, it just imposes OS-level walls.

**Threat model addressed.** Direct quote from the docs:

> *"Even if an attacker successfully manipulates Claude Code's behavior through prompt injection, the sandbox ensures your system remains secure."*

Specifically: filesystem protection (cannot modify `~/.bashrc`, `/bin/`, cannot read denied paths), network protection (cannot exfiltrate data to attacker-controlled servers, cannot download malicious scripts, cannot make unexpected API calls, cannot contact any domains not explicitly allowed).

**Filesystem isolation.** Default writes: cwd and subdirs only. Default reads: entire computer minus deny paths. Enforced at OS level via Seatbelt on macOS and bubblewrap on Linux/WSL2 (WSL1 unsupported). Applies to *all subprocesses* — `kubectl`, `terraform`, `npm` — not just Claude's tool calls. `sandbox.filesystem.{allowWrite, denyWrite, allowRead, denyRead}` give per-path overrides; multi-scope settings are merged.

**Network isolation.** A proxy runs *outside* the sandbox; sandboxed processes only reach the network through it. The proxy enforces a hostname allowlist; new domains trigger user confirmation or are blocked if `allowManagedDomainsOnly` is set. **Critical limitation, quoted:** *"The built-in proxy enforces the allowlist based on the requested hostname and does not terminate or inspect TLS traffic."* Allowing broad domains like `github.com` opens domain-fronting / gist exfiltration. Custom TLS-terminating proxies plug in via `httpProxyPort`/`socksProxyPort`.

**Modes.** *Auto-allow* ("safe YOLO"): sandboxed bash runs without per-command approval; unsandboxable commands fall back to the permission flow; `rm`/`rmdir` against `/`, `$HOME`, or critical paths still prompts. *Regular permissions*: every bash command goes through the permission flow.

**Escape hatch.** A `dangerouslyDisableSandbox` parameter lets Claude retry a sandbox-blocked command *with explicit user permission*. Set `"allowUnsandboxedCommands": false` to make it a hard no.

**Documented weaknesses.** (1) TLS allowlist bypass via domain fronting; (2) privilege escalation via exposed Unix sockets (`/var/run/docker.sock` = host RCE); (3) filesystem escalation through writeable `$PATH` or `.bashrc`/`.zshrc`; (4) `enableWeakerNestedSandbox` for running inside Docker without privileged namespaces *"considerably weakens security."* The built-in `Read`/`Edit`/`Write` tools are *not* sandboxed (governed by permissions instead).

**Open source.** Published as `npx @anthropic-ai/sandbox-runtime <command>` — wrap arbitrary subprocesses (MCP servers, build tools) in the same primitives.

---

## 5. Threat model the factory must defend against — synthesis

Combining the four sources, here is the concrete threat surface for a CI/CD-shaped factory:

| # | Threat | Mitigation |
|---|---|---|
| T1 | Injected instruction in issue body / PR comment | Dual-LLM split: planner never sees untrusted strings |
| T2 | Injected instruction in scraped doc / web search | WebFetch allowlist + Q-LLM-only reads |
| T3 | Injected instruction in dependency README / npm package | Build in nested sandbox; allowlist registries |
| T4 | Secret exfiltration via `curl` to attacker domain | Sandbox network allowlist |
| T5 | Exfiltration via markdown image / link preview (`![](attacker/?key=...)`) | Strip rendered markdown; allowlist image hosts; remove secrets from agent env |
| T6 | Secret exfiltration via git push to attacker remote | Pin remote URL; gate push behind reviewer |
| T7 | Filesystem tampering — `.bashrc`, `$PATH`, `~/.ssh` | OS-level deny; no writeable `$PATH` |
| T8 | Privilege escalation via Docker socket | Never expose `/var/run/docker.sock` to the sandbox |
| T9 | Domain-fronting exfiltration via broad allowlist (`github.com`, gist) | TLS-terminating custom proxy |
| T10 | Injection persisting across worktrees / cycles | Per-cycle teardown; never share `$HOME`/caches |

The factory's F12 row in the comparison covers T4–T8 (sandboxing), partially T1–T3 (workpad / spec hygiene), and largely *misses* T5, T9, T10 today.

---

## 6. Security posture per architecture — adding nuance to F12

`architectures/00-comparison.md` §2.4 currently summarises F12 in a single cell per architecture. Here is what each architecture actually buys, in light of the primitives above.

### 6.1 StrongDM Factory (`architectures/01`) — F12: "Sandbox"
Relies on the Claude Code sandbox directly — Seatbelt/bubblewrap + proxy allowlist. Covers T4, T6, T7. **Gaps:** no Dual LLM split (injected issue content reaches the planner); secret/public separation is allowlist-only; domain-fronting (T9) and rendered-markdown exfiltration (T5) open. **Tighten:** disable `allowUnsandboxedCommands`; narrow `allowedDomains` to Git remote + registry; quarantine issue bodies through a Q-LLM before they reach the planner.

### 6.2 StrongDM Attractor / worktree-per-issue (`architectures/02`) — F12: "Worktree + sandbox"
Per-worktree isolation defeats T10 (state-leaking) by construction and strengthens T7. The worktree boundary is *not* a trust boundary against T1–T3 — the LLM still reasons over the same context. **Tighten:** make `$HOME` ephemeral per worktree; mount no shared credentials; treat the worktree as the secrets-in-env boundary.

### 6.3 Phased / Foundry (`architectures/03`) — F12: "Sandbox + Phase-2 security review"
Most layered of the four: sandbox at execution + a security-reviewer LLM in Phase 2 that audits diffs for trifecta-shaped patterns (new fetch domains, new ENV reads, new outbound calls). Closest to CaMeL-shape, but operates on *diffs* not *data capabilities*. **Gap:** review is post-hoc — if the implementer exfiltrated during the cycle, the reviewer sees the diff but not the traffic. **Tighten:** pair the reviewer with a TLS-terminating proxy and feed the request log into the review.

### 6.4 Candidate-fanout (`architectures/04`) — F12: "Per-candidate sandbox + security judge"
N-candidate fanout gives adversarial redundancy: a security-judge LLM can flag the odd-candidate-out. The only architecture with a built-in *diversity* defence (N-version programming for prompt injection). **Gap:** if the injection is in the shared issue body, all N candidates compromise identically and the judge cannot tell "all agree" from "all compromised the same way." **Tighten:** quarantine the shared input through a Q-LLM before fanout; vary the planner model across candidates.

### 6.5 Common recommendations
1. **Make the Dual LLM split explicit.** Planner sees only the spec; a summariser is the *only* component that reads issue bodies, PR comments, scraped docs, MCP outputs, tool stdout. One-shot architectural fix for T1–T3.
2. **Use `@anthropic-ai/sandbox-runtime` as the substrate.** Open source, OS-enforced, proxy-allowlist baked in. Wrap *every* subprocess agent in it (not just the Claude Code implementer) — MCP servers, dependency installers.
3. **Default `allowUnsandboxedCommands: false` and `allowManagedDomainsOnly: true`.** The escape hatch defeats the threat model for autonomous CI/CD.
4. **TLS-terminating proxy in production.** Hostname allowlist is fine for desktop, inadequate for a factory processing untrusted text 24/7. Squid / mitmproxy with a CA cert inside the sandbox; feed the request log to the security reviewer.
5. **Track capabilities informally.** Annotate every working-context value with `{provenance, readers}`. Even just displaying the tags in the agent's prompt nudges correct handling.
6. **Strip rendering surfaces.** Disable markdown image rendering on agent-emitted PR comments; sanitise links; no raw HTML to UIs that load arbitrary URLs.

---

## 7. Open follow-ups

- Read the CaMeL paper PDF for AgentDojo benchmark numbers and capability lattice details.
- Locate the `anthropics/claude-code` examples repo's sandbox presets; propose a `factory.json` baseline.
- Evaluate `@anthropic-ai/sandbox-runtime` for wrapping non-Claude-Code substrates (OpenHands, Overstory workers).
- Specify a minimal capability lattice for the factory's tool API (`{public, internal, secret, credential}`).

---

## Sources

- *The lethal trifecta for AI agents: private data, untrusted content, and external communication* — Simon Willison, 2025-06-16. (Direct fetch blocked; quotations reconstructed from WebSearch result snippets.)
- *The Dual LLM pattern for building AI assistants that can resist prompt injection* — Simon Willison, 2023-04-25. (Direct fetch blocked; quotations reconstructed from WebSearch result snippets.)
- *CaMeL offers a promising new direction for mitigating prompt injection attacks* — Simon Willison, 2025-04-11. (Direct fetch blocked; reconstructed from WebSearch.)
- *Defeating Prompt Injections by Design* (CaMeL) — arXiv 2503.18813, Debenedetti et al., DeepMind, 2025-03. (Direct fetch blocked; reconstructed from explainer summaries including InfoQ, MarkTechPost, ikangai, repo-explainer.)
- *Sandboxing* — Claude Code docs, `code.claude.com/docs/en/sandboxing`. Fetched verbatim 2026-05-11.
- *Making Claude Code more secure and autonomous* — Anthropic Engineering blog, `anthropic.com/engineering/claude-code-sandboxing`. (Direct fetch blocked; corroborated by search snippets.)

**Blocked URLs encountered:** `simonwillison.net/2025/Jun/16/the-lethal-trifecta/`, `simonwillison.net/2025/Apr/11/camel/`, `simonwillison.net/2023/Apr/25/dual-llm-pattern/`, `arxiv.org/abs/2503.18813`, `arxiv.org/html/2503.18813v2`, `anthropic.com/engineering/claude-code-sandboxing`. Verbatim quotations marked above were reconstructed from WebSearch result snippets that themselves quoted the originals; treat as second-hand and re-verify on next fetch pass.
