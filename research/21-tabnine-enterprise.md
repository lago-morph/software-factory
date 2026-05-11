# Tabnine — Enterprise Governance Posture as a Product

**Source cluster:** S17 in `research/external-syntheses/chatgpt-deep-research-2026-05-11/sources.md`, expanded per the "Weak or missing citations" §: five non-umbrella subpages on deployment, privacy, context engine, agent guidelines, and provenance/attribution.
**Round / cluster:** Round 5, Cluster 13.1.4, per `research/PLAN.md` §13.1.4.
**Stance:** *Tabnine's enterprise positioning is the closest existing-product analog to the governance discipline that `research/followup/10-governance.md` (Round-3 §11.10) and `research/16-el-kaim-book-council-and-delegation.md` (Round-4 L1–L4) argue any regulator-defensible factory needs. Treated as a product specification rather than as marketing, it supplies four primitives — private deployment, governed context, typed instructions, and per-output provenance — that the four architectures of this corpus do not currently name as first-class.*

---

## 0. Source-status table

All URLs probed 2026-05-11 (America/Chicago); all returned **HTTP 403** to direct WebFetch from the sandbox.

| # | Subpage | Substitute used |
|---|---|---|
| T1 | `docs.tabnine.com/main/welcome/readme/architecture/deployment-options` | WebSearch snippet (Google-indexed page) |
| T2 | `docs.tabnine.com/main/welcome/readme/privacy` | WebSearch snippet |
| T3 | `docs.tabnine.com/main/getting-started/context-engine` | WebSearch snippet + `context.tabnine.com` |
| T4 | `docs.tabnine.com/main/getting-started/tabnine-agent/guidelines` | WebSearch snippet |
| T5 | `docs.tabnine.com/main/welcome/readme/protection/provenance-and-attribution` | WebSearch snippet + Tabnine blog launch post |
| T6 | `docs.tabnine.com/main/administering-tabnine/private-installation` (supp.) | WebSearch snippet |
| T7 | `docs.tabnine.com/.../air-gapped-deployment-guide` (supp.) | WebSearch snippet |
| T8 | `docs.tabnine.com/.../managing-your-team/settings/agent-guidelines` (supp.) | WebSearch snippet |

`[fetch-urls]` issue **#27** filed requesting GitHub-Actions-side fetches of all five primary subpages plus three supplementaries. Snippet content is **provisional**; quotes are preserved verbatim for re-verification once #27 lands. Snapshot date for all numbers: 2026-05-11.

---

## 1. Private deployment / VPC / on-prem options and their constraints (T1, T6, T7)

Tabnine documents **four deployment shapes** (T1-snip): **SaaS** (Tabnine-managed cloud, default for Pro & Enterprise); **private cloud / VPC** (Tabnine cluster inside customer AWS/GCP/Azure tenant); **on-premises** (Kubernetes cluster on customer iron — "Tabnine doesn't have access to the customer environment"); and **air-gapped** (no network egress to Tabnine; "you will need to manually provision the docker images into the Kubernetes cluster… using organization internal docker registry or, for single-node environments, by side-loading the images," T7-snip).

The substrate is **Kubernetes + Helm charts** for the three private shapes. The customer holds the cluster identity, the secret store, the audit-log destinations, and the network policy — *Tabnine inherits whatever NHI discipline the customer's Kubernetes operator already enforces* rather than imposing a parallel one.

**Two constraints worth naming:** (1) air-gapped trades model freshness for runtime compliance — models update only at the cadence the customer chooses to mirror images, which is the property that makes air-gapped deployment compatible with EU AI Act high-risk conformity assessment (model versions can be pinned under a certificate and cannot update silently). (2) Tabnine professional services touch the install ("the Tabnine professional team works with your team to set up and frequently update your Tabnine installation," T6-snip), reintroducing the third-party-in-the-chain vector `research/followup/10-governance.md` §1.3 named via Pragmatic CTO.

---

## 2. The Context Engine — how context scoping is governed at the enterprise level (T3)

Tabnine's Context Engine is the substrate the agentic platform reasons over. Two characterizations matter (T3-snip):

> "The Tabnine Context Engine extends your agents' awareness beyond the local workspace by generating structured context from connected remote repositories."

> "The Enterprise Context Engine is a continuously evolving organizational intelligence layer that goes beyond traditional Retrieval-Augmented Generation (RAG), building a structured model of the enterprise by extracting entities, relationships, dependencies, and patterns from both structured and unstructured sources."

Positioned **explicitly against vanilla RAG**: not a vector store over chunks but a structured graph of entities and relationships. Vendor-attested numbers (T3-snip, 2026-05-11 snapshot, *not independently audited*): "up to 2× improvement in accuracy, up to 80% reduction in token consumption… up to 50% faster time to resolution."

**Three governance-relevant properties** distilled from T3-snip and adjacent connector docs:

- **Connector inventory is admin-administered.** Connections to Bitbucket, GitHub, GitLab, Perforce, Jira, and Confluence are configured at the enterprise level; the agent's reachable context is bounded by what the admin connected. This is the runtime analog of El Kaim's per-domain-agent `scope` declarations (`research/16-…md` §2), expressed as integration credentials rather than capability IDs.
- **Indexing is continuous.** "Continuously indexes your repositories using real-time semantic and graph-based techniques and maps relationships between services, functions, and files." This addresses El Kaim's "context decay / stale Codex" failure mode (`research/16-…md` §6) operationally, not aspirationally.
- **Cross-tool reach.** "Works alongside tools like Cursor, GitHub Copilot, Claude Code, and Tabnine" — the Context Engine is a *separable substrate*, an existence proof that the governed context layer can be productized independently of the coding agent.

**Not visible in snippets** and governance-material (issue #27 should resolve): per-user / per-team access controls inside the engine, retention policy for the structured graph itself, and whether the graph respects source-system permissions at retrieval time.

---

## 3. Agent Guidelines as a typed-instruction primitive (T4, T8)

Tabnine's "Agent Guidelines" are positioned as the place teams encode their conventions. The shape (T4-snip):

> "Guidelines are Markdown files stored in your project's `/.tabnine/guidelines/` directory that act as Custom System Prompts, Workflow Rules, Tool Instructions, and Team Standards to encode your team's coding practices and conventions."

Three properties make this a *governance* primitive rather than prompt-templating convenience:

1. **Four-tier inheritance.** User-home (`~/.tabnine/guidelines/`), project (`<repo>/.tabnine/guidelines/`), enterprise (Admin UI), and team-scoped (the Coaching Guidelines feature: "a new Team designation for Coaching Guidelines allows you to define each guideline for all teams or for specific (single to multiple) teams," T8-snip).
2. **Markdown surface, typed role.** Four named kinds — Custom System Prompts, Workflow Rules, Tool Instructions, Team Standards (T4-snip). The seed of the typed-instruction primitive `research/16-…md` §3 identifies as the EA Council's operational vocabulary (none / veto / escalation / challenge-only). Tabnine has not gone as far — guidelines remain advisory rather than authority-typed — but the *scoping* and *kind* dimensions are present.
3. **One-rule-one-pattern authoring discipline.** "A rule should be descriptive, clear, and concise, and should focus on a single pattern of code that should be followed or avoided" (T4-snip).

**Gap vs. El Kaim and Foundry:** Tabnine guidelines are *prompts*, not *contracts*. No machine-checkable invariant, no decision-of-origin attribution, no failure-by-level allocation. A guideline can drift, get longer, contradict an earlier guideline, and the system does not flag the contradiction — the **G7 intent drift** failure mode in `research/followup/10-governance.md` §3. Tabnine has done the *plumbing* (multi-scope, named kinds, admin-administered) without the *typing*: structurally sympathetic but incomplete for a regulator-defensible factory.

---

## 4. The Provenance / Attribution model and how it differs from SLSA's (T5)

Tabnine's Provenance and Attribution feature operates at the **per-snippet output** layer:

> "Tabnine checks the code generated within their AI chat against the publicly visible code on GitHub, flags any matches it finds, and references the source repository and its license type." (T5-snip)

> "Tabnine reads code like a human; it not only flags the output that exactly matches the open source code, but also flags output if there are functional or implementation matches, like cases where the overall function is the same, but the variable names are changed." (T5-snip)

A toggled "Censor code" mode prevents emission of snippets that match non-permissively-licensed sources (T5-snip). Available on every model Tabnine routes to — Anthropic, OpenAI, Cohere, Llama, Mistral, and Tabnine. As of 2026-05-11, in private preview for Enterprise customers (vendor description, time-stamped).

**Differs from SLSA** (S25 in `sources.md`):

| Dimension | SLSA v1.2 (build provenance) | Tabnine P&A (generation provenance) |
|---|---|---|
| **Unit / where it fires** | Build artifact / build pipeline | Per-snippet model output / generation time (and CI per Tabnine's blog) |
| **What is attested against what corpus** | Builder identity, materials, build steps / build-system trace | Source repo on GitHub that overlaps with the snippet; license type / public GitHub codebase |
| **Adversary modeled / failure addressed** | Tampered build, unverified materials / supply-chain risk | Inadvertent reproduction of copyleft code / IP-license risk |

**Complementary, not overlapping.** SLSA covers the question `research/followup/10-governance.md` §2 lists as #4 (build provenance: model family / version / prompt / seed / tool calls). Tabnine P&A covers a question that section does *not* list but should: **derivation provenance — what existing source did this output structurally resemble**. A regulator-defensible factory needs both: SLSA-style attestation on the build, Tabnine-style on the generation. Architecture 3 (Foundry) implicitly assumes the former through V-Model traceability; none of the four architectures currently names the latter as a first-class artifact.

---

## 5. Privacy posture and lethal-trifecta implications (T2)

Tabnine's documented privacy posture is unusually direct:

> "Tabnine does not train on your code. Tabnine has a no-train-no-retain policy, which is in place regardless which model is being used." (T2-snip)

> "Code snippets sent for completion are processed in memory and discarded immediately… Tabnine doesn't retain any user code beyond the immediate time frame required for inferencing the model." (T2-snip)

> "The Tabnine cluster sends operational metrics and logs (every 1 second) to Tabnine's servers, with metrics and logs data being retained for a week. However, no code or PII data is ever sent to Tabnine's servers." (T2-snip)

> "Tabnine's code completion model and Tabnine Protected chat model are only trained on open source code with permissive licenses." (T2-snip; license list: MIT, MIT-0, Apache-2.0, BSD-2-Clause, BSD-3-Clause, Unlicense, CC0-1.0, CC-BY-3.0, CC-BY-4.0, RSA-MD, 0BSD, WTFPL, ISC.)

Certifications (T2-snip and adjacent marketing): SOC 2, ISO 27001, GDPR alignment. TLS for transport.

**Lethal-trifecta lens** (Simon Willison's framing per `research/05-simon-willison.md`): exfiltration risk requires (1) access to private data, (2) exposure to untrusted content, (3) an outward path. Tabnine's posture attacks the trifecta unevenly:

- **Leg (3), outward path:** in air-gapped and on-premises modes, *there is no outward path* from the inference cluster to Tabnine. Trifecta legs that depend on an outbound HTTP to a Tabnine endpoint are structurally absent.
- **Leg (1), private data:** the Context Engine indexes whatever the admin connected — leg (1) is configurable, and its boundary is the connector-admin's decision. Materially better than "the agent reads the file system, period."
- **Leg (2), untrusted content:** *not* obviously addressed. A prompt-injected README, a poisoned dependency, a Jira ticket containing an instruction-override payload — all reachable through the Context Engine if the admin connected those sources, and Tabnine's documented controls do not include content-classification at the boundary. The El Kaim Red Team agent (`research/16-…md` §3) is the only structural response to leg (2) named anywhere in the corpus — and it is `challenge-only`, not blocking. Leg (2) is the natural place for a Council/Red-Team-style overlay on top of Tabnine.

---

## 6. How Tabnine's governance posture composes with each of our four architectures

The four primitives — (a) private deployment, (b) governed Context Engine, (c) typed/scoped Guidelines, (d) per-output provenance — compose unevenly across the four architectures. Snapshot 2026-05-11.

| Arch | Best-fit primitive | Friction | Net |
|---|---|---|---|
| **1 — Refinery** | Guidelines-as-typed-instructions. The layered-spec idiom maps to scoped Guidelines (enterprise → team → project → user) with binding spec at project scope and lens-specific rules at user scope. Provenance slots in cleanly as a per-revelation check. | Context Engine's continuous indexing is over-eager relative to "the spec is the world"; needs a `only index artifacts the binding spec references` filter. | Refinery + Guidelines + scoped Context Engine is a coherent compound; gains runtime governance without losing the spec-first stance. |
| **2 — Atelier** | Context Engine. The persona panel needs a *shared* governed context to keep personas from disagreeing about facts; the structured-graph engine is what the workpad and curators currently approximate. | Guidelines-as-Custom-System-Prompts overlap awkwardly with persona prompts; either personas *are* guidelines or inheritance gets four-deep. | Largest single accuracy/governance upgrade available to Atelier. Provenance slots in at the synthesizer. |
| **3 — Foundry** | Private deployment + Provenance. The Foundry already produces audit-trail-grade artifacts per phase; private deployment makes them physically containable; provenance gives V&V a license/IP check it currently lacks. | Guidelines and Context Engine are too lightweight for the Foundry's typed-artifact discipline — it needs typed Codex objects (per `research/16-…md` §1), not markdown rules. | The architecture whose **deployment surface** Tabnine most improves; its content surface is already more disciplined than Tabnine's. Pair with El Kaim Codex objects for full coverage. |
| **4 — Tournament** | Provenance / Attribution. The candidate population is exactly where per-output provenance is essential — selection pressure does not screen for IP risk on its own. | Prompt-shaped Guidelines fit poorly with scenario-set-as-contract; Context Engine introduces **G8 scenario-corpus poisoning** if scenarios are reachable through the indexed graph. | Provenance is the most useful primitive; the other three need careful firewalling against adversarial-selection dynamics. |

**Cross-architecture observation.** Each architecture finds *one* primitive obviously load-bearing and the others more awkward, consistent with `research/00-synthesis.md`'s finding that the four architectures are differentiated by which governance dimension they make first-class. Tabnine is not a fifth architecture — it is a **menu of governance primitives** any of the four can adopt selectively, with the L1–L4 typology from `research/16-…md` §1 supplying the typing discipline Tabnine itself lacks.

---

## 7. Open follow-ups

- **Issue #27** (filed 2026-05-11) should land direct subpage content; on merge, flip the §0 source-status table from `WebSearch snippet` to `full subpage` and re-verify inline citations.
- **Trifecta leg (2)** — content-classification at the boundary of indexed sources — is the cleanest single gap revealed here. Candidate for a Round-6 follow-up thread.
- **Vendor numbers** in §2 are time-stamped and not independently audited.
- Round-5 cluster 13.1.5 and §11.10 governance both touch provenance; cross-link the SLSA / Tabnine P&A distinction (§4) into both to tighten the corpus's governance vocabulary.

---

*Sources: T1–T8 (see §0 source-status table for URLs and access status), all probed 2026-05-11. Context: `research/followup/10-governance.md`, `research/16-el-kaim-book-council-and-delegation.md`, `architectures/03-phase-gated-foundry.md`, `research/external-syntheses/chatgpt-deep-research-2026-05-11/sources.md`.*
