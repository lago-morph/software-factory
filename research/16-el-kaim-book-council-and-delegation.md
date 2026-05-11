# El Kaim — The EA Council and the L1–L4 Delegation Classification

**Source:** William El Kaim, *Continuous Enterprise Architecture* (Medium, 2026), Chapter 4 "Why AI and Automation Change the Stakes" (load-bearing); Chapter 6 "The Enterprise Architecture Codex" §§3.4 and 9 (Council-as-Codex-object).
**Round / cluster:** Round 4, Cluster C, per `research/PLAN.md` §12.3.
**Stance:** *Council governance becomes operable only when delegation is a typed, named, evidenced classification — not a cultural posture.*

This chapter substantially answers the Round-3 governance thread §11.10 in `research/PLAN.md`: where Round-3 left open "who is accountable when an agent approves," El Kaim names the principle ("an agent is not a legal actor") and gives an explicit failure-mode-by-level allocation. §5 records that answer; the rest is supporting structure. Pharma-specific examples (clinical operations, pharmacovigilance, GxP, PMDA) are renamed in this report to generic regulated-domain placeholders where the example matters; "EA Council" is preserved verbatim per brief.

---

## 1. The L1/L2/L3/L4 delegation classification (Chapter 4 §5.2)

El Kaim's central operating contract is a four-level classification. It is published as a typed Codex object (`kind: DesignAuthorityClassification`, id `DAC-001`, owner `chief-architect`). The matrix below is reproduced from §5.2 verbatim in its core fields.

| Level | Description | Agent role | Human role | Evidence required | Examples (generic) |
|---|---|---|---|---|---|
| **L1 automated** | Routine conformance checks; right answer is deterministic. No human review unless the check fails. | `execute-and-report` | `review-on-failure-only` | `audit-log-of-evaluation` | Schema/spec validation; OpenAPI lint; data-classification label consistency; retention-period compliance. |
| **L2 assisted** | Design assessments; agent produces a structured finding + recommendation; domain architect must approve. | `assess-and-recommend` | `domain-architect-approval` | `agent-finding + architect-sign-off` | API boundary changes; cross-domain integration; event-schema changes; landing-zone template deviations. |
| **L3 escalated** | Cross-domain, regulatory, or precedent-setting. Agent flags + briefs; design authority board resolves. | `flag-and-brief` | `design-authority-board-resolution` | `decision-record with rationale and dissent` | New capability boundaries; jurisdiction-scope changes; AI in regulated workflows; platform retirement. |
| **L4 reserved** | Reserved to named human authorities regardless of agent confidence. No delegation. | `none` | `named-authority-only` | `board-minutes with accountability record` | Enterprise-wide policy changes; intent approval / supersession; exception grants for regulatory invariants; cross-enterprise data-authority reassignment. |

Two properties matter. First, **the classification is itself a governed artifact** with owner, version, and approval state — not an informal convention. Second, **the auditable question becomes which decisions sit at which level**, not whether agents may be "trusted" — converting an abstract debate into a tractable design choice the board reviews on a cadence.

---

## 2. The Chief Architect orchestrator (Chapter 4 §5.3)

The Council is anchored by a single orchestrator agent (`kind: EACouncilOrchestrator`, id `ORCH-CA-001`, `role: chief-architect`, `authority: final-recommendation`). It performs **no domain analysis itself** — it convenes, coordinates, and synthesizes.

**Membership.** Three layers under the orchestrator:

- *Orchestrator layer:* the Chief Architect agent.
- *Domain layer (six capability-scoped agents):* Clinical Operations / Domain-A, Regulatory & Quality / Domain-B, Data & AI, Application, Integration, Platform. Each declares a `scope` list of capability IDs (`CAP-*`).
- *Cross-cutting layer (three special-authority agents):* Security (`veto`), Compliance (`escalation`), Red Team (`challenge-only`).

A **shared knowledge layer** sits beneath all agents. Every agent retrieves the Codex (capabilities, decisions, policies, specifications, intents) and EA-tool factsheets through MCP at evaluation time, **not from embedded prompt context**. Council behavior therefore updates the moment the Codex updates, without redeploying agents.

**Deliberation protocol (six phases):** (1) Triage — classify request, select agents; (2) Parallel assessment — each selected agent emits a structured finding; (3) Conflict detection — contradictions, overlaps, coverage gaps; (4) Synthesis — merge non-conflicting findings, flag conflicts; (5) Recommendation — single verdict (*approve* / *request changes* / *escalate*) with all findings attached as evidence; (6) Record — draft an ADR linked to the intent artifact, affected specifications, and agent findings.

**Routing rules.** Six declared triggers map request shapes to agent panels: `touches-regulated-capability` → domain-A + regulatory-quality + security + compliance; `modifies-api-contract` → integration + application + security; `introduces-ai-component` → data-AI + security + compliance + red-team; `catalog.new-service-registration` → application + platform + integration + security; `specification.change-proposal` → domain-by-capability-match + compliance; `exception.request` → all-domain-by-scope + security + compliance + red-team.

The output contract names the schema (`council-recommendation`) and required fields: `request_id`, `delegation_level`, `agents_consulted`, `findings_summary`, `conflicts_detected`, `recommendation`, `evidence_refs`, `adr_draft (if applicable)`.

---

## 3. The four agent shapes and their authorities (Chapter 4 §5.4)

El Kaim distinguishes four operationally distinct agent shapes by the authority they hold. The four authority types — **none / veto / escalation / challenge-only** — are the operational vocabulary El Kaim's model contributes, declared in the agent spec as a structural role, not as informal severity.

- **Domain agents (no special authority).** Operate at **L1 + L2**, capability-scoped. Tool boundaries are read-mostly: they may `write: pull-request.comment`, `write: pull-request.review`, `write: decision-record.draft`, but are **prohibited** from `decision-record.approve`, `policy.modify`, and `deployment.any`. They escalate on declared finding types (e.g., `data_classification_conflict`, `new_jurisdiction_introduced`). *Operationally:* author and recommend; cannot ship.

- **Security with `veto` (cross-cutting, blocking).** When it identifies an unmitigated critical vulnerability, its finding **blocks the change regardless of what other agents recommend**. Veto is asymmetric — it does not require board action to bind; the orchestrator's recommendation cannot synthesize past it. *Operationally:* a runtime guarantee that one class of harm cannot be silently merged. Cost: false-veto is more expensive than false-positive, so the Security Agent must be tightly specified.

- **GxP / Compliance with `escalation` (cross-cutting, board-routing).** Operates at **L2 + L3**. Always-escalate on declared finding types (validated-system status affected, revalidation required, regulatory notification required). The agent generates a structured briefing and routes to named human roles (head-of-quality, chief-architect, design authority board). *Operationally:* re-classifies the change as L3 mid-flight. Its authority is to **force a board review**, not to decide.

- **Red Team with `challenge-only` (cross-cutting, non-blocking).** Cannot approve or reject. Injects adversarial questions ("What if this API is called with a jurisdiction the system has never seen?") that are attached to the recommendation as challenges the approving authority **must address**. *Operationally:* raises the cost of approval (someone must write a response) without blocking; a structural devil's-advocate that human review boards aspire to but rarely sustain.

---

## 4. Worked example: a pull request triggers six agents in parallel (Chapter 4 §5.6)

A pull request extends an onboarding service to a new jurisdiction (Domain-J): new regulatory package, modified assembly logic, jurisdiction-specific retention period, new country-specific submission step.

- **Triage.** Orchestrator matches `pull-request.touches-regulated-capability` and `new jurisdiction introduced`. Six agents consulted in parallel.
- **Parallel assessment.** *Domain-A:* submission step implemented as code branch, not configuration — violates `DD-CT-009`; **L2**. *Data & AI:* retention period hard-coded instead of declared in `retentionPolicy`; **L1** + **L2** (new-jurisdiction data-residency assessment). *Compliance:* service is on the validated-systems register, jurisdiction change = validated-system change; **L3 — automatic escalation**. *Red Team:* challenges whether Domain-J document types fit the evidence schema or require a cross-jurisdiction schema extension. *Security:* no critical vulnerabilities; flags Domain-J consent mechanisms differ from baseline; **L2**.
- **Conflict detection.** Domain-A and Data-AI findings share a root cause (jurisdiction-specific behavior in code rather than configuration). No contradictions.
- **Recommendation.** "Request changes. Three L2 findings require domain-architect review. One L3 finding requires board escalation. One Red Team challenge requires response before approval."
- **Record.** ADR amendment drafted to `DD-CT-009`, linked to the intent artifact and the Red Team challenge.

**Total elapsed time:** minutes. The example demonstrates two structural moves at once: **parallel fanout across heterogeneous specialist agents** (echoing Atelier-style review panels) and **typed escalation that re-classifies the change mid-flight** (a move the Atelier does not currently make).

---

## 5. The accountability chain (Chapter 4 §5.7) — direct answer to §11.10

This section answers `research/PLAN.md` §11.10 directly. The principle in one sentence:

> "The answer cannot be 'the agent,' because an agent is not a legal or organizational actor. Accountability follows the delegation chain."

Failure-mode allocation **by delegation level**:

- **L1 failure** — a conformance check missed a violation. Accountable: the architect who defined the check and the platform team that deployed it.
- **L2 failure** — agent recommended approval, domain architect signed off. Accountable: the domain architect who approved the finding.
- **L3 failure** — a board decision informed by a briefing with errors. Accountable: the board; the briefing serves as evidence of what information was available.
- **L4 failure** — by construction, an L4 decision is the named human authority's; no agent role exists.

A second-order point: **defining the classification is itself an L3 decision.** Misclassifying (putting an L3 at L2, or an L2 at L1) propagates through every agent that inherits the classification; `DAC-001` is therefore one of the most consequential governed artifacts the enterprise maintains.

This is the cleanest published answer in our corpus to "what does it mean to hold an agent accountable?". The answer: **you don't — you hold the human at the appropriate delegation level accountable, and you make sure the level is correctly assigned.**

---

## 6. The four named risks (Chapter 4 §7) — operational vs aspirational mitigations

| Risk | Mechanism named | Operational? |
|---|---|---|
| **Hallucination / reasoning errors (§7.1)** | Output contracts require explicit references to existing Codex artifacts with validation that those artifacts exist; human review of L2/L3 findings. | **Operational** (validation runs against the Codex; L2/L3 gates declared). Residual: "augmentation, not replacement." |
| **Context decay / stale Codex (§7.2)** | Override rates, agent-vs-runtime comparison, periodic re-validation by owning teams. | **Partial.** Override tracking is implementable (Data-AI Agent already declares `override_rate`, `false_positive_rate`). Periodic re-validation is **aspirational** unless tooling forces it. |
| **Design-authority erosion (§7.3)** | "Categories of decisions that never descend below L3, regardless of agent confidence or board convenience." | **Aspirational** — policy commitment, no system check against reclassification drift. |
| **Cost / operational complexity (§7.4)** | Honest accounting of inference, retrieval, coordination, logging, review costs. | **Aspirational** — no cost-routing mechanism specified. (Contrast: Atelier `model-hierarchy`.) |
| **Toolchain lock-in (§7.5)** | Prefer open protocols (MCP); portable artifact formats. | **Operational** insofar as MCP is declared. |

Honest reading: hallucination and lock-in have operational defenses; design-authority erosion and cost discipline are governance commitments the architecture relies on the chief architect to defend. El Kaim names that structural weakness openly.

---

## 7. Side-by-side: El Kaim Council vs. compound-engineering review vs. our Atelier

| Dimension | El Kaim EA Council (Ch. 4) | Compound-engineering review (Every.to, `research/03`) | Compound Atelier v0.2 (`architectures/02`) |
|---|---|---|---|
| **Specialist agents** | 9 named (6 domain + 3 cross-cutting) + 1 orchestrator | 14 in the public count; 50+ in current plugin | ~15–20 code + 4 doc + 2 adversarial + curators |
| **Authority typology** | **None / Veto / Escalation / Challenge-only** — explicit | Implicit: all findings advisory, human disposes | Severity × autofix-class — orthogonal axes, no role-level gating |
| **Orchestrator** | Chief Architect (named, single, governed object) | `kw-compound` skill chain | Conductor (structurally separate from personas) |
| **Routing** | Six declared triggers → panel | Diff-aware persona selection | Diff-aware persona selection |
| **Mid-flight re-classification** | **Yes** — Compliance promotes to L3 | No (no levels) | No (severity, not level) |
| **Adversarial role** | Red Team, `challenge-only` | `adversarial-reviewer` as a synthesis voice | `adversarial-reviewer` + `adversarial-document-reviewer` |
| **Accountability framing** | **Failure allocated by delegation level** | "Trust the system; human reviews intent" | Operator at `Human Review`; residual-work gate |
| **Durable artifact** | Decision records, intents, specs in a Codex with stable IDs | Knowledge docs in `docs/solutions/` | STRATEGY → brainstorm → plan → workpad → knowledge doc |
| **Cost stance** | Risk named, no mechanism | Implicit | `model-hierarchy` skill (explicit routing) |
| **Volume frame** | 50 capabilities, 300 services, thousands of PRs/month | Single-person engineering teams, thousands of users | 4-concurrent default; small team |

The Atelier and the compound-engineering review army are the **same shape** (parallel persona panel + synthesizer), differing in role count and curation discipline. **The El Kaim Council differs structurally** in three places:

1. **Authority typology is part of the role.** Veto / escalation / challenge-only are declared in the agent spec; in Atelier these are emergent properties of severity+autofix-class.
2. **Decisions carry a delegation level**, not just a severity. A finding's level determines who must sign off.
3. **Escalation re-classifies the change in flight.** A change entering as L2 can exit as L3 because Compliance matched a declared finding type; the orchestrator routes the verdict automatically.

Atelier's severity (P0–P3) × autofix-class (`safe_auto` / `gated_auto` / `manual` / `advisory`) approximates the Council's authority typology at the **finding** layer; the Council operates one level up — classifying *the kind of decision* before it classifies findings.

---

## 8. Proposal: delegation-classification rows for `architectures/00-comparison.md`

Proposal only; no edit to `00-comparison.md`. The proposed rows would sit in §2.1 (Methodology dimensions) or as a new §2.5 "Delegation typology."

| Architecture | Decision-level classification | Authority types | Mid-flight re-classification | Failure attribution | Gap vs. El Kaim |
|---|---|---|---|---|---|
| **1. Refinery** | Implicit: revelation gates determine when a decision "binds"; no L1–L4 typology. | Specs / lenses, not authorities. | Yes (revelation can demote a binding spec). | Author of binding spec; humans gate revelations. | No veto / escalation / challenge roles; no failure-by-level. |
| **2. Atelier** | Severity (P0–P3) × autofix-class — finding granularity, not decision granularity. | All reviewers advisory; Synthesizer routes; Operator disposes residual. | No (severity ≠ level). | Operator at `Human Review`; durable-sink for residuals. | **No role-level authority typology;** no decision-classification artifact; accountability-by-level absent. |
| **3. Foundry** | Implicit: phase gates ≈ L2/L3 human approvals; pre-gate ≈ L1/L2. | Gate owners hold approval; sub-gate agents advisory. | Rare (re-running a phase is the heavy form). | Gate owner. | Gates approximate L3/L4 but **without typed `DAC-001`** and without L1↔L2 distinction. |
| **4. Tournament** | None — tournament ranks variants; "decision" = "which variant wins." | Tournament judges; no veto/escalation/challenge. | N/A. | Operator who selects the winner. | No delegation typology; needs Council overlay in regulated contexts. |

**Borrowing paths** if each architecture adopted the typology:

- *Refinery:* add `kind: DesignAuthorityClassification` as a Codex object; mark binding-spec revelations L3 by default; introduce `escalation` and `challenge-only` lens roles.
- *Atelier:* add a decision-level field to the finding schema; promote `security-sentinel` → `veto`, `adversarial-reviewer` → formal `challenge-only`; add a Compliance role with `escalation` for regulated repos.
- *Foundry:* map existing phase gates to L3/L4; introduce explicit L1/L2 sub-flows inside each phase; record gate-owner identity per ADR.
- *Tournament:* not applicable natively, but a Council overlay could classify *which kinds of decisions* a tournament may settle (e.g., an L4 invariant cannot be a tournament parameter).

---

## 9. Council-as-Codex-object (Chapter 6 §§3.4 and 9)

Chapter 6 confirms a structural detail: **the EA Council is itself a first-class Codex object**, not an external committee. Members, L1–L4 classifications, escalation paths, and approval thresholds are all typed entries. Consequences: (a) required reviewers on a merge request are resolved from the Council's organizational model rather than from a static CODEOWNERS file that ages out of sync; (b) compliance reports name the accountable owner from the capability's `owningCouncilMember` field; (c) the L1–L4 classification connects to runtime policy — §9.2 ties L1 (read-only retrieval) to "passes the Rego policy without further review," L3 (regional workflow write) to "passes only when on the allow list and the human review route is present," and L4 ("modification to a regulated case in the platform of record") to "blocked at the gateway."

The closing pattern: **the Council writes the classification; the Codex carries it; the gateway enforces it at runtime.** The board does not need to be in the loop for every action because its policy is materialized as enforced code.

---

## 10. What is load-bearing for our Atelier

Three borrows, in order of tractability:

1. **Authority typology on cross-cutting reviewers.** Promote `security-sentinel` → `veto`, `adversarial-reviewer` → `challenge-only`, and (for regulated repos) add a `compliance-reviewer` with `escalation`. Extend the synthesizer to honor authority before severity. Low cost, high signal.
2. **A `DAC-001`-equivalent artifact at the repo root.** Typed YAML declaring which kinds of decisions in this repo are L1 / L2 / L3 / L4 — auto-consulted by the planner and synthesizer at routing time. Resolves the open question "when is a finding board-level vs operator-level?" with a typed answer.
3. **Failure-by-level accountability in the residual-work gate.** Today the gate forces disposition but does not record *which delegation level was applied*. Adding the level to the durable-sink record makes post-incident attribution tractable per Ch. 4 §5.7.

Not yet borrowable: mid-flight re-classification (requires the routing layer to honor escalation findings that change a verdict's authority); a runtime gateway that enforces L4-prohibited actions (we have CI gates, not a runtime policy engine).

---

## 11. Open follow-ups

- Compliance escalation triggers are domain-specific; generalizing what *we* would treat as "always escalate" finding types is unresolved.
- Risk §7.3 (design-authority erosion) is named without mechanism; a periodic-audit-of-the-classification routine would be a Round-5 design topic.
- The "agent is not a legal actor" framing is sharper than anything currently in `architectures/00-comparison.md` §5.2; revising that subsection to incorporate failure-by-level would tighten the comparison.

---

*Sources: Chapter 4 §§1–8 (full); Chapter 6 §§3.4 and 9 (focused). Context: `architectures/02-compound-atelier.md`, `architectures/00-comparison.md`, `research/03-every-compound-engineering.md`.*
