# Tabnine — Enterprise Governance Posture as a Product

**Source cluster:** S17 in `reference-only/chatgpt-deep-research-2026-05-11/sources.md`, expanded per the "Weak or missing citations" §: five non-umbrella subpages on deployment, privacy, context engine, agent guidelines, and provenance/attribution.
**Round / cluster:** Round 5, Cluster 13.1.4, per `research/PLAN.md` §13.1.4.
**Stance:** *Tabnine's enterprise positioning is the closest existing-product analog to the governance discipline that `research/followup/10-governance.md` (Round-3 §11.10) and `research/16-el-kaim-book-council-and-delegation.md` (Round-4 L1–L4) argue any regulator-defensible factory needs. Treated as a product specification rather than as marketing, it supplies four primitives — private deployment, governed context, typed instructions, and per-output provenance — that the four architectures of this corpus do not currently name as first-class.*

---

## Drain note (issue #27) — 2026-05-11

This report was upgraded from snippet-anchored to primary-source-anchored on 2026-05-11 by draining `research/fetched/issue-27/` (8 Tabnine doc subpages fetched via the GitHub Action workaround for Cloudflare-gated `docs.tabnine.com`). Concrete changes at the claim level:

- **§1 deployment shapes:** clarified that "SaaS / VPC / On-prem / Air-gapped" is **not four sibling SKUs** — air-gapped is a *property of* private installations, not a separate top-level shape. The primary source lists three shapes (SaaS, VPC, On-prem) with air-gapped as a deployable mode of the latter two.
- **§2 Context Engine:** replaced WebSearch claim that the engine "goes beyond traditional RAG / extracts entities, relationships, dependencies" — the primary subpage does **not** contain that language; it describes a procedural admin-setup workflow. The "beyond-RAG / structured organizational intelligence" framing comes from marketing copy, not from the docs subpage that was probed. Privacy doc *does* describe a "RAG index" with vector embeddings on the server GPU — Tabnine's Context Engine **is RAG plus a graph layer on remote repos**, not "beyond RAG."
- **§2 Context Engine governance:** added five operationally specific facts the snippet did not contain: (i) admin-set "Context Engine User" runs the engine and inherits that user's permissions and quota, (ii) admins choose the indexing model and schedule, (iii) the agent's `check_provenance` and Context Engine tools must be **explicitly enabled** per workspace, (iv) the agent prioritizes local workspace context by default — remote-graph reach requires explicit prompt phrasing ("in remote repositories"), (v) agentic context layers are **per-repository opt-in**, not automatic.
- **§3 Agent Guidelines:** primary source confirms four-kind typing (Custom System Prompts / Workflow Rules / Tool Instructions / Team Standards) and admin-precedence — Admin-UI guidelines "**take precedence over personal guidelines**" — but also reveals there is **"no _real_ structural requirement"** for guideline files. Tabnine itself describes them by analogy to `agents.md`. Sharpened the §3 "structurally sympathetic but incomplete" finding: primary source confirms the typing is *advisory naming convention*, not enforced schema.
- **§4 Provenance and Attribution:** replaced WebSearch-snippet quotes with verbatim primary source, and added six previously-unknown concrete mechanisms: (i) reference DB is Postgres updated quarterly, (ii) the privacy-preserving wire protocol — only signature hashes that pass a local bloom-filter check are sent to `attribution.tabnine.com`, **no plain text code is ever sent**, (iii) air-gapped installs may host the full attribution DB on-prem, (iv) match criterion is ≥150 characters and multiline, (v) the check is structurally non-overridable ("Custom behaviors and custom commands cannot be used to override the censorship check"), (vi) `check_provenance` is disabled by default and must be enabled per workspace.
- **§4 Attribution logs:** new — primary source enumerates a per-event audit-log schema (detectionId, userId, organizationId, teamId, source, model, isNonPermissive, snippet, codeAttribution, plus action counts) with default 14-day retention.
- **§5 Privacy:** primary source confirms "no-train-no-retain" applies "regardless which model is being used," ephemeral context window enumerated (chat history, lines of code, variables, type declarations, functions, objects, imports, related files, syntactic/semantic error reports), and the air-gapped operational-telemetry path goes to *customer-hosted* Prometheus and log aggregator rather than to Tabnine. This **fixes a snippet-era ambiguity** about whether air-gapped clusters still phone home.
- **§0 source-status:** flipped all eight previously-probed URLs from `WebSearch snippet` to `full subpage (primary)`. T7 (`air-gapped-deployment-guide`) is the one URL not in the cache — content for it is now covered by the deployment-options and privacy primary subpages, not a dedicated air-gapped guide.

**Refutations found:** the snippet-era "extracts entities, relationships, dependencies, and patterns / goes beyond RAG" framing for the Context Engine was **not corroborated** by the docs subpage; this was marketing-page language conflated with docs. Corrected in §2 below.

---

## 0. Source-status table

All URLs probed 2026-05-11 (America/Chicago) via WebFetch returned **HTTP 403** from the sandbox; the GitHub Action-side fetcher pulled them into `research/fetched/issue-27/` for the drain.

| # | Subpage | Source used |
|---|---|---|
| T1 | `docs.tabnine.com/main/welcome/readme/architecture/deployment-options` | ✅ full subpage (primary) |
| T2 | `docs.tabnine.com/main/welcome/readme/privacy` | ✅ full subpage (primary) |
| T3 | `docs.tabnine.com/main/getting-started/context-engine` | ✅ full subpage (primary) |
| T4 | `docs.tabnine.com/main/getting-started/tabnine-agent/guidelines` | ✅ full subpage (primary) |
| T5 | `docs.tabnine.com/main/welcome/readme/protection/provenance-and-attribution` | ✅ full subpage (primary) |
| T6 | `docs.tabnine.com/main/administering-tabnine/private-installation` | ✅ full subpage (primary) |
| T7 | `docs.tabnine.com/.../private-installation/server-setup` | ✅ full subpage (primary, HTML only) |
| T8 | `docs.tabnine.com/.../managing-your-team/settings/agent-guidelines` | ✅ full subpage (primary) |
| T9 | `docs.tabnine.com/main/welcome/readme/ai-models/tabnines-private-and-protect` | ✅ full subpage (primary, HTML only) |
| T10 | `docs.tabnine.com/.../context-engine/admin-console/coaching-guidelines` | ✅ full subpage (primary) |

Snapshot date for all numbers: 2026-05-11.

---

## 1. Private deployment / VPC / on-prem options and their constraints (T1, T6)

The primary subpage documents **three deployment shapes**, with air-gapped as a *mode* of private installations rather than a fourth shape (T1, verbatim):

> "**Private installation** (self-hosted deployments): Virtual private cloud (VPC) / On-premises. Private installations can be deployed in a completely air-gapped environment."

> "**Secure SaaS** — This type of deployment is available for Starter, Pro, and Enterprise customers. The solution is hosted, managed, and monitored by Tabnine, and is frequently updated."

> "**VPC** — This is an option for Tabnine Enterprise customers. In a VPC setup, the Tabnine cluster is a Kubernetes-hosted unit on your virtual private cloud (GCP, AWS, or Azure). Tabnine doesn't have access to the customer environment. Periodic software updates are done in a controlled way." (T1)

> "**On-premises** — In an on-premises private installation, the Tabnine cluster is a Kubernetes cluster hosted on the customer's servers on their private network. Tabnine doesn't have access to the customer environment. Periodic software updates are done in a controlled way." (T1)

> "**Fully air-gapped private installation** — This is an option for Tabnine Enterprise customers. The Tabnine solution can also be deployed in a completely air-gapped environment." (T1)

The substrate is **Kubernetes** for the three private modes; T6 confirms "In a private installation deployment, the Tabnine team has no access to your servers, but the Tabnine professional team works with your team to set up and frequently update your Tabnine installation." The customer holds the cluster identity, the secret store, the audit-log destinations, and the network policy — *Tabnine inherits whatever NHI discipline the customer's Kubernetes operator already enforces* rather than imposing a parallel one.

**Two constraints worth naming:** (1) air-gapped trades model freshness for runtime compliance — model and image updates flow only at the cadence the customer chooses to mirror, which is the property that makes air-gapped deployment compatible with EU AI Act high-risk conformity assessment (model versions can be pinned under a certificate and cannot update silently). (2) Tabnine professional services touch the install (T6 verbatim above), reintroducing the third-party-in-the-chain vector `research/followup/10-governance.md` §1.3 named via Pragmatic CTO.

---

## 2. The Context Engine — how context scoping is governed at the enterprise level (T3, T10)

The Context Engine's own docs page describes a **procedural admin-setup workflow** rather than the architectural prose the marketing site uses. From T3 verbatim:

> "The Tabnine Context Engine extends your agents' awareness beyond the local workspace by generating structured context from connected remote repositories."

> "Repositories are automatically indexed / The agent can search, navigate, and list the following: remote repositories, folders, files, and code elements / Basic context becomes available within a few hours."

The "structured context" referenced is two-layer: (i) an initial repo-level index made automatically on connect; (ii) per-repository, opt-in **"agentic pre-processing"** that produces "higher-level summaries, services, dependencies, and structured architectural insights" reviewable under Context Engine > Assets (T3). The privacy doc (T2) clarifies that the underlying mechanism is RAG: "Tabnine's personalization capabilities … require creating a RAG index of your code. The computation for vector embeddings for the chat RAG index … Tabnine performs this computation on the server GPU."

**Correction vs. snippet-era prose.** The earlier snippet-anchored draft claimed the Context Engine "goes beyond traditional Retrieval-Augmented Generation (RAG), building a structured model of the enterprise by extracting entities, relationships, dependencies, and patterns from both structured and unstructured sources." That phrasing is not on the docs subpage. The docs describe **RAG plus an agentic graph layer on remote repos plus reviewable asset artifacts**, not a categorical departure from RAG. Treat the marketing framing as aspirational; the primary mechanism is more conventional.

**Five governance-relevant properties** from T3 verbatim:

- **Admin-set Context Engine User runs the engine.** "Select the Context Engine User / Must be an admin / Must belong to a team with agents enabled / The Context Engine runs on behalf of this user (permissions and quota apply)" (T3). This is a load-bearing identity decision: the engine's reachable context is bounded by what *that user* can see, which is the runtime analog of El Kaim's per-domain-agent `scope` declarations (`research/16-…md` §2), expressed as a single human identity with delegated permissions rather than as capability IDs.
- **Per-repository, admin-opted-in advanced indexing.** "Advanced (agentic) context layers are not generated automatically for all repositories. For each repository: Go to the Personalization page / Locate the connected repository / Enable agentic context processing using the repository action icon" (T3). Opt-in is the default, which materially limits the leg-(1) surface of the lethal trifecta (§5 below).
- **Admin must enable Context Engine tools for end users.** "This step is mandatory. Without enabling tools, end users will not be able to access Context Engine capabilities in the IDE or CLI, even if repositories were processed successfully" (T3). Two-stage gating: indexing on, tools on.
- **Local-default reach.** "By default, the agent prioritizes local workspace context. If you want the agent to explicitly use remote repositories, specify it in your prompt" (T3). The remote graph is *recall-on-request*, not pulled by default.
- **Reviewable asset artifacts.** "From there, admins can: Filter assets by repository, team, or type / Open and inspect generated context layers" (T3). Generated context is *inspectable*, which is what makes it auditable for the EU-AI-Act / SR-11-7 documentation surface.

The **Coaching Guidelines** primary page (T10) confirms that team leads (as of 5.27.0) can author team-scoped coaching guidelines via CSV import or default templates: "Only the Language and Description fields are required. Other fields (e.g., tags, good/bad code examples) can be auto-generated by Tabnine."

**Not visible even in primary sources** and governance-material: retention policy for the structured-graph assets themselves, and whether the graph respects source-system row-level permissions at retrieval time (Tabnine documents that the Context Engine User's permissions apply, but does not specify per-retrieval ACL enforcement).

---

## 3. Agent Guidelines as a typed-instruction primitive (T4, T8)

Tabnine's "Agent Guidelines" are positioned as the place teams encode their conventions. The shape (T4 verbatim):

> "Guidelines are Markdown files stored in your project's `/.tabnine/guidelines/` directory that act as: **Custom System Prompts** — Define how the agent should behave. **Workflow Rules** — Specify procedures and processes to follow. **Tool Instructions** — Control how and when tools should be used. **Team Standards** — Encode your team's coding practices and conventions."

> "This directory will either reside either 1) in your home directory or 2) on a per-project basis within your project directory."

> "There is no *real* structural requirement, but it is still a best practice to list the various guidelines in a *hierarchical structure* for easy interpretation, both by Agents and other users."

> "Think of these in a similar fashion to the `agents.md` file that other agentic tools use."

> "It is recommended to keep your `guidelines.md` file to 500 lines or less."

Admin-tier governance (T4 + T8 verbatim):

> "In the Admin UI, navigate over to Agent Guidelines on the left-hand side of the page. Beneath the **General Guideline** title, you can add your natural language guideline description. They will also be applicable to all your organization's users and projects."

> "Guidelines that are input here will have the same effect as guidelines listed in your `guidelines.md` file, **but they will take precedence over personal guidelines** that exist in the `guidelines.md` file." (T4)

> "These changes will be applied in the IDE extension after 15 minutes, or upon restarting the IDE or the extension." (T8)

Three properties make this a *governance* primitive rather than prompt-templating convenience:

1. **Three-tier inheritance with admin precedence.** User-home (`~/.tabnine/guidelines/`), project (`<repo>/.tabnine/guidelines/`), and admin (Admin UI > Agent Guidelines), with explicit precedence: admin > personal. T10's Coaching Guidelines feature adds a team-scoped fourth tier with CSV-import as the authoring interface.
2. **Markdown surface, four named kinds.** Custom System Prompts, Workflow Rules, Tool Instructions, Team Standards (T4 verbatim above). The seed of the typed-instruction primitive `research/16-…md` §3 identifies as the EA Council's operational vocabulary (none / veto / escalation / challenge-only). Tabnine has not gone as far — guidelines remain advisory rather than authority-typed — but the *scoping* and *kind* dimensions are present.
3. **Soft authoring discipline rather than enforced schema.** Primary source explicitly says "There is no *real* structural requirement" and recommends a 500-line file ceiling. Tabnine's own analogy is to `agents.md` (T4 verbatim). The four-kind typing is *naming convention*, not enforced schema.

**Gap vs. El Kaim and Foundry — sharpened by primary source:** Tabnine guidelines are *prompts*, not *contracts*. No machine-checkable invariant, no decision-of-origin attribution, no failure-by-level allocation, no schema validation. A guideline can drift, get longer (up to and past the 500-line guideline), contradict an earlier guideline, and the system does not flag the contradiction — the **G7 intent drift** failure mode in `research/followup/10-governance.md` §3. The admin-UI precedence rule is structural (admin > personal), but no precedence ordering is documented *among* admin guidelines themselves. Tabnine has done the *plumbing* (multi-scope, named kinds, admin-administered, admin-precedence) without the *typing*: structurally sympathetic but incomplete for a regulator-defensible factory.

---

## 4. The Provenance / Attribution model and how it differs from SLSA's (T5)

Tabnine's Provenance and Attribution feature operates at the **per-snippet output** layer (T5 verbatim):

> "Tabnine checks the code generated within our AI chat against the publicly visible code on GitHub, flags any matches it finds, and references the source repository and its license type."

> "Attribution and Censorship is *always* checked as the last step of code generation. Custom behaviors and custom commands cannot be used to override the censorship check."

**Two levels of protection** (T5 verbatim):

> "**Training time protection**: We have trained the Tabnine Protected 2 model exclusively on code that does not have any restrictions on use. This ensures that when using this model, every recommendation from Tabnine can be accepted without the risk of IP infringement."

> "**Inference time protection**: Tabnine informs you if the output of the LLM matches any publicly visible code on GitHub and identifies the source repo and its license type. By adding guardrails around Tabnine's output, we minimize the risk of IP liability of third-party models."

**Privacy-preserving wire protocol** (T5 verbatim — this is new vs. snippets):

> "The code snippet is sent to the *recitation service*, which is then installed on premises. From there, we calculate the *signature hashes* in that snippet, then check a *bloom filter* to see if those signature hashes are in the *attribution database*. Only the signature hashes that are found in the bloom filter are sent to the attribution service in order to find the references. Note that no plain text code is *ever* sent to the attribution service, *only* the signature hashes."

The check is engineered so that the agent's own code never leaves the customer's perimeter for the attribution lookup — only locally-computed hashes that already passed a local bloom filter. Air-gapped customers can host the full attribution database on-prem (T5: "Some self-hosted users with air-gapped deployments may install the full attribution database on-prem").

**Operational specifics** (T5 verbatim):

> "The reference database is Postgres, containing signatures and their metadata. That metadata includes the license information, commit hash, repo, and number of starts among other things. It is updated about once every quarter."

> "**Censorship in Agent**: Censorship exists in Agent as a tool called `check_provenance`. The tool is disabled by default and must be activated in the Admin Console. … If the proposed code contains a match of more than 150 characters from non-permissive code, the Agent is instructed to rewrite only the offending portion while still addressing the original task."

> "**Code match criteria**: At least 150 characters, and multiline."

> "**System requirements**: Provenance and Attribution requires up to 10TB of free storage."

Available on every model Tabnine routes to — Anthropic, OpenAI, Cohere, Llama, Mistral, and Tabnine (T5). As of 2026-05-11, in private preview for Enterprise customers.

**Audit log schema** (new from primary, T5 verbatim):

> "The logs will have the following fields: `detectionId`, `timestamp`, `userId`, `organizationId`, `teamId`, `source` (Chat, Agent, or Test), `model`, `isNonPermissive` (TRUE/FALSE), `snippet` (License information plus the code snippet itself), `codeAttribution` (JSON data attributing the code to source), `newFile actions count`, `apply actions count`, `insert actions count`, `copy actions count`."

Default retention is 14 days, configurable via API. This is a per-event audit trail at exactly the granularity SR-11-7 wants for model-output governance.

**Differs from SLSA** (S25 in `sources.md`):

| Dimension | SLSA v1.2 (build provenance) | Tabnine P&A (generation provenance) |
|---|---|---|
| **Unit / where it fires** | Build artifact / build pipeline | Per-snippet model output / "last step of code generation" |
| **What is attested against what corpus** | Builder identity, materials, build steps / build-system trace | Source repo on GitHub that overlaps with the snippet; license type / Postgres-hosted signature DB updated quarterly |
| **Adversary modeled / failure addressed** | Tampered build, unverified materials / supply-chain risk | Inadvertent reproduction of copyleft code / IP-license risk |
| **Privacy of the check** | Build attestation is public/verifiable | Bloom-filtered local pre-check; only signature hashes leave the perimeter |
| **Override path** | Verifier policy choice | Structurally non-overridable: "Custom behaviors and custom commands cannot be used to override the censorship check" |

**Complementary, not overlapping.** SLSA covers the question `research/followup/10-governance.md` §2 lists as #4 (build provenance: model family / version / prompt / seed / tool calls). Tabnine P&A covers a question that section does *not* list but should: **derivation provenance — what existing source did this output structurally resemble**. A regulator-defensible factory needs both: SLSA-style attestation on the build, Tabnine-style on the generation. Architecture 3 (Foundry) implicitly assumes the former through V-Model traceability; none of the four architectures currently names the latter as a first-class artifact. The non-overridability property is what makes P&A *governance* rather than *advice*: it is wired into the codegen path the way a kernel-mode check is wired into a syscall.

---

## 5. Privacy posture and lethal-trifecta implications (T2)

Tabnine's documented privacy posture, verbatim from the primary subpage:

> "Tabnine has a *no-train-no-retain* policy. This is in place regardless which model is being used."

> "These requests include some code from the local project as context (the 'context window' as described below) to allow Tabnine to return the most relevant and accurate answers. This context window may include elements from your local environment, such as: Chat history (for chat) / Lines of code / Variables / Type declarations / Functions / Objects / Related imports from the current file / Related files / Syntactic and semantic error reports. This context is deleted **immediately** after the server returns the answer to the client."

> "Tabnine doesn't retain any user code beyond the immediate time frame required for inferencing the model. This is what we call ephemeral processing. … This is true even for Tabnine Enterprise's private deployment options (on-premises and VPC)."

> "Tabnine's code completion model and Tabnine Protected chat model are only trained on open source code with permissive licenses." (T2; license list referenced via the AI Models subpage, T9)

**Air-gapped data plane** (T2 verbatim — fixes a snippet-era ambiguity):

> "In an air-gapped deployment, metrics can be sent to a Prometheus server and logs can be sent to your log aggregator. In a self-hosted deployment, the Tabnine cluster sends operational metrics and logs to Tabnine's servers to allow improved support when required. **No code or PII data is ever sent to Tabnine's servers**."

> "The Tabnine cluster sends operational metrics and logs (every 1 second) to Tabnine's servers. Metrics and logs data are retained for a week. This includes: GPU and CPU utilization / GPU and CPU memory / Server throughput / Server latency."

The air-gapped mode routes operational telemetry to **customer-hosted** Prometheus and log aggregator endpoints — there is no outbound dependency on `*.tabnine.com` from an air-gapped cluster.

Certifications (referenced from T2 sidebar and Trust Center link): SOC 2, ISO 27001, GDPR alignment. TLS for transport.

**Lethal-trifecta lens** (Simon Willison's framing per `research/05-simon-willison.md`): exfiltration risk requires (1) access to private data, (2) exposure to untrusted content, (3) an outward path. Tabnine's posture attacks the trifecta unevenly:

- **Leg (3), outward path:** in air-gapped mode, *there is no outward path* from the inference cluster to Tabnine — confirmed by T2's "metrics can be sent to a Prometheus server and logs can be sent to your log aggregator" routing. Trifecta legs that depend on an outbound HTTP to a Tabnine endpoint are structurally absent. In on-premises mode without air-gap, only operational metrics (no code, no PII) flow out at 1 Hz, retained one week. In VPC mode, same. In SaaS mode, the inference itself round-trips to Tabnine, but the context window is "deleted immediately after the server returns the answer."
- **Leg (1), private data:** the Context Engine indexes whatever the admin connected, *and only repos with agentic pre-processing explicitly enabled get the deeper graph layer* (§2 above) — leg (1) is doubly configurable, and its boundary is the admin's per-repository decision plus the Context Engine User's permission scope. Materially better than "the agent reads the file system, period."
- **Leg (2), untrusted content:** *not* obviously addressed. A prompt-injected README, a poisoned dependency, a Jira ticket containing an instruction-override payload — all reachable through the Context Engine if the admin connected those sources and opted those repos into agentic pre-processing. Tabnine's documented controls do not include content-classification at the boundary. The non-overridable provenance check (§4) catches *generation-time* IP exfiltration but does not catch *input-time* instruction injection. The El Kaim Red Team agent (`research/16-…md` §3) is the only structural response to leg (2) named anywhere in the corpus — and it is `challenge-only`, not blocking. Leg (2) is the natural place for a Council/Red-Team-style overlay on top of Tabnine.

---

## 6. How Tabnine's governance posture composes with each of our four architectures

The four primitives — (a) private deployment, (b) governed Context Engine, (c) typed/scoped Guidelines, (d) non-overridable per-output provenance — compose unevenly across the four architectures. Snapshot 2026-05-11.

| Arch | Best-fit primitive | Friction | Net |
|---|---|---|---|
| **1 — Refinery** | Guidelines-as-typed-instructions. The layered-spec idiom maps to scoped Guidelines (admin → team-coaching → project → user) with binding spec at project scope and lens-specific rules at user scope. Provenance slots in cleanly as a per-revelation check, with the non-overridability property turning the check into an artifact gate rather than advice. | Context Engine's per-repo opt-in agentic indexing is over-eager relative to "the spec is the world"; needs a `only index artifacts the binding spec references` filter. Tabnine's "no structural requirement" on guidelines clashes with Refinery's preference for typed lenses. | Refinery + Guidelines + scoped Context Engine is a coherent compound; gains runtime governance without losing the spec-first stance. |
| **2 — Atelier** | Context Engine. The persona panel needs a *shared* governed context to keep personas from disagreeing about facts; the admin-set Context Engine User identity is what makes the "shared" claim auditable. | Guidelines-as-Custom-System-Prompts overlap awkwardly with persona prompts; either personas *are* guidelines or inheritance gets four-deep (admin / team / project / user) plus persona-deep. | Largest single accuracy/governance upgrade available to Atelier. Provenance slots in at the synthesizer with non-overridable gating. |
| **3 — Foundry** | Private deployment + Provenance. The Foundry already produces audit-trail-grade artifacts per phase; private deployment makes them physically containable; provenance gives V&V a license/IP check it currently lacks, with the audit-log schema (detectionId, organizationId, source, isNonPermissive, codeAttribution JSON) hitting SR-11-7 documentation requirements directly. | Guidelines and Context Engine are too lightweight for the Foundry's typed-artifact discipline — it needs typed Codex objects (per `research/16-…md` §1), not markdown rules with "no real structural requirement." | The architecture whose **deployment surface** Tabnine most improves; its content surface is already more disciplined than Tabnine's. Pair with El Kaim Codex objects for full coverage. |
| **4 — Tournament** | Provenance / Attribution. The candidate population is exactly where per-output provenance is essential — selection pressure does not screen for IP risk on its own. Non-overridability is critical here: a tournament strategy that "learned" to evade attribution would defeat governance. | Prompt-shaped Guidelines fit poorly with scenario-set-as-contract; Context Engine introduces **G8 scenario-corpus poisoning** if scenarios are reachable through the indexed graph. The Context Engine User identity is the wrong granularity for adversarial-population isolation. | Provenance is the most useful primitive; the other three need careful firewalling against adversarial-selection dynamics. |

**Cross-architecture observation.** Each architecture finds *one* primitive obviously load-bearing and the others more awkward, consistent with `research/00-synthesis.md`'s finding that the four architectures are differentiated by which governance dimension they make first-class. Tabnine is not a fifth architecture — it is a **menu of governance primitives** any of the four can adopt selectively, with the L1–L4 typology from `research/16-…md` §1 supplying the typing discipline Tabnine itself lacks. The single most transferable primitive across all four architectures is the **non-overridable provenance check** with its **plain-text-never-leaves-perimeter** wire protocol — every architecture in the corpus benefits from it, and none of the four currently names it.

---

## 7. Substrate posture per architecture

Preserved from the snippet-era version; primary sources sharpen but do not change the call:

- **Architecture 1 (Refinery):** Kubernetes-on-customer-iron substrate is over-engineered relative to Refinery's needs but adds little friction.
- **Architecture 2 (Atelier):** Context Engine substrate is the right shape; agentic pre-processing matches Atelier's curator role.
- **Architecture 3 (Foundry):** Private installation with air-gapped option matches the Foundry's physical-containment story most cleanly.
- **Architecture 4 (Tournament):** Air-gapped private installation with on-prem attribution DB is the only safe substrate for adversarial-population dynamics.

## 8. Governance posture

Preserved from the snippet-era version, with one sharpening: Tabnine's posture is **runtime-enforced where it can be (P&A non-overridability) and convention-enforced everywhere else (Guidelines)**. The pattern to import is the *non-overridability* — wire governance into the codegen path, not into a sidecar that the agent can ignore.

---

## 9. Open follow-ups

- **Trifecta leg (2)** — content-classification at the boundary of indexed sources — is the cleanest single gap revealed here. Candidate for a Round-6 follow-up thread.
- **Vendor numbers** in §2 (accuracy/token/time-to-resolution claims) are time-stamped and not independently audited; primary docs do not contain them (they live on the marketing site).
- Round-5 cluster 13.1.5 and §11.10 governance both touch provenance; cross-link the SLSA / Tabnine P&A distinction (§4) into both to tighten the corpus's governance vocabulary.
- Tabnine's Context Engine **per-retrieval ACL enforcement** is not documented; worth a direct vendor question if the corpus pursues a Tabnine-pattern recommendation.

---

*Sources: T1–T10 (see §0 source-status table for URLs and access status), all probed 2026-05-11 and drained from `research/fetched/issue-27/` on the same day. Context: `research/followup/10-governance.md`, `research/16-el-kaim-book-council-and-delegation.md`, `architectures/03-phase-gated-foundry.md`, `reference-only/chatgpt-deep-research-2026-05-11/sources.md`.*
