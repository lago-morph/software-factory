# Caremark Exposure for Boards Deploying Recursive Self-Improvement

**Status:** ✅ FULL primary-source-anchored
**Date:** 2026-05-16 (Cluster J — Stanford Law School / CodeX governance drain)
**Anchor source:** Eran Kahana, *The Ungovernable Machine*, Stanford CodeX, 2026-03-17 (`law.stanford.edu/2026/03/17/the-ungovernable-machine/`)
**Cross-cluster references:** AI Life Cycle Core Principles (Kahana 2023; followup/10 §A); *From Principles to Practice: The 48 Controls* (Kahana 2026-02-16; followup/10 §B); *Cognitive Escrow* (Kahana 2026-03-07; report 30); *Turning AI Governance Into Operational Infrastructure* (Kahana 2026-04-05; followup/10 §C).
**Corpus cross-references:** followup/10 §1.1 (Kahana on StrongDM "tracing difficult by design"); report 02 (StrongDM-attractor — "no human review" architectural posture); report 07 (Dark Factory); report 27 (.dot pipelines as product); report 18 §4.3–§4.4 (Codex `.rules` DSL + `running-safely` OTEL stack as substrate-level board-visibility instrumentation); report 28 §10 (failure-mode F40/F41 proposals — number-collision context for F43).

---

## 1. Recursive Self-Improvement — Kahana's three-part test

Kahana opens the piece with a definition that is **explicitly broader than the frontier-lab framings** most public commentary has used. Recursive Self-Improvement (RSI) is *"an AI system's ability to modify the mechanisms by which it improves itself, in ways that carry forward into future iterations."*

The critical distinction Kahana draws is between **behavioural-level self-correction** (a system breaking tasks into subtasks, checking intermediate results, revising plans mid-run — the standard agent loop) and **architectural-level self-modification** (the system generating and integrating changes to its own code, models, or training procedures). The first is ubiquitous in current production deployments; the second is RSI. The improvement compounds: each cycle makes the next cycle more effective.

**Kahana's three-part operational test.** A system is RSI for governance purposes if and only if it meets all three of:

1. **Durable self-modification of the mechanisms that produce intelligence.** The change persists across iterations — not just within a single inference run.
2. **Compounding ability to self-modify across iterations.** Later iterations are *more capable of further self-modification*. Not just better at the task — better at the modification cycle.
3. **Limited human gating over the self-improvement loop.** Material changes are not subject to per-change human review.

> "It is this combination, not the use of feedback loops alone, that creates the governance exposure this post addresses. In governance terms, the question to ask management is not whether the system uses AI, but whether it can alter its own code or training procedures across releases without human review of each material change, and whether those changes are logged in a way the company can reconstruct." *(Kahana primary)*

**The mid-market scope.** This is the *load-bearing corpus-novel claim* in the piece. The standard public discussion frames RSI as a frontier-lab problem (Dario Amodei, Eric Schmidt, OpenAI / Anthropic / DeepMind / xAI). Kahana explicitly rejects that scope-limit:

> "RSI is not limited to frontier labs. Whether a deployment meets the three conditions depends on facts, not labels. Agentic development tools like Claude Code and OpenAI Codex allow software firms of any size to deploy recursive loops that can maintain and extend their own codebases. Whether those loops produce durable self-modification with limited human gating is a question about the specific implementation. Companies in chip design, biotech, and financial services are running AI-driven systems that recursively refine their own algorithms cycle by cycle; some of those systems will meet the conditions and some will not. For companies in retail, logistics, and finance, emerging RSI-style capability is arriving not as internally developed software but as an API integration. **A logistics company whose routing agent rewrites its own scheduling code overnight may be running a system that meets all three conditions whether or not it uses that term.**" *(Kahana primary; emphasis added)*

This sentence, read against the corpus, is highly load-bearing. The StrongDM "Software Factory" architecture (report 02, followup/10 §1.1), the 2389 dotfile-pipelines / dotpowers / kilroy / tracker / mammoth / smasher attractor ecosystem (report 27, followup/02), and any compound-engineering deployment in which agents are extending their own scaffolding (every Klaassen / Hess / Nystrom / Schillace case in the corpus) **may meet Kahana's three-part RSI test** depending on whether per-change human review is in fact occurring on each material self-modification. Most do not, by design. The governance exposure Kahana describes therefore *reaches the corpus' subject matter directly*, not just frontier labs.

The cleanest test-case framing (Kahana, primary): *"From a Caremark perspective, a mid-market logistics firm running a self-rewriting routing agent may present a cleaner test case than a research lab advertising frontier AI."* The "cleanness" lies in the absence of the safety-research apparatus and the absence of a frontier-AI compliance program — making the gap visible without research-program noise to argue around.

**Three risk patterns.** Kahana names three failure modes that have received attention in the technical literature, mapped explicitly to RSI architecture (verbatim primary):

- **Behavioural drift.** *"When an agent recursively trains on its own synthetically generated outputs without sufficient grounding in human-generated data, it enters a feedback loop that progressively severs the connection between its behavior and human norms."* Outputs become self-referential and detached from the original task.
- **Self-poisoning.** *"Minor errors, hallucinated facts, and embedded biases do not wash out across iterations. They compound. Knowledge degrades not suddenly but cumulatively, across a sequence of individually small distortions."*
- **Goal subversion.** *"The recursive architecture creates a surface for manipulation. Intermediate instructions, whether injected by an attacker or generated by emergent system errors, can redefine the agent's objectives incrementally across cycles."*

Kahana adds the **deeper control-problem layer** (citing Bostrom, Russell, Yampolskiy): a system optimising for a goal can develop instrumental sub-goals including self-preservation and resistance to shutdown, making it *actively resistant* to the oversight board-level monitoring requires. Not merely opaque — adversarially opaque.

---

## 2. The Delaware Caremark spine

The legal architecture Kahana invokes is the Delaware duty of oversight, originating in *In re Caremark International Inc. Derivative Litigation*, 698 A.2d 959 (Del. Ch. 1996), and refined across a line of cases through 2023. Kahana walks each case explicitly. The structure below preserves the per-case contribution.

**Caremark itself (1996).** The foundational doctrine: directors can face liability not only for bad decisions but for failing to build the systems through which material risks are reported to the board. The question, in Kahana's framing, is *not whether the board understood the risk* — it is *whether the board ensured it would be told about it*.

**Stone v. Ritter, 911 A.2d 362 (Del. 2006).** Embedded Caremark in the **duty of loyalty via bad faith** and established the doctrine's two-pronged structure (verbatim from Kahana, in legal-shorthand form):

- **Prong 1.** Directors may be liable where they *utterly fail to implement a reasonable board-level information and reporting system.*
- **Prong 2.** Having implemented such systems, directors may be liable if they *consciously fail to monitor operations in the face of red flags.*

Because the doctrine sounds in loyalty-based bad faith, plaintiffs must plead a knowing failure to act, **not mere negligence**. Practical consequence: even directors shielded from duty-of-care liability by a DGCL § 102(b)(7) charter provision remain exposed to a sustained or systematic oversight failure.

**Marchand v. Barnhill, 212 A.3d 805 (Del. 2019).** Clarified when prong-one pleading is adequate: *"A company in a domain with mission-critical risks must have a board-level system that brings those risks to its directors."* Kahana's application to RSI: for a company whose core product or platform depends on RSI, *safety and controllability are a plausible candidate for that treatment* — but **no court has yet so held**. Marchand arose around immediate physical-safety risk; Delaware courts have not automatically extended the mission-critical rubric to software-based risks. Whether a court does depends on what the board knew, when, and the reporting structure at deployment time, not in hindsight.

**Marchand's mission-critical rubric does not require monoline structure.** Kahana's distinctive contribution to the doctrinal trajectory is the observation that **RSI is not a product** — it is the backend process that generates, maintains, and modifies products. A company with ten distinct product lines, each running on an RSI backend, faces *greater* exposure from an RSI failure than a monoline company, because the failure propagates across every line simultaneously. The Marchand inquiry is whether the risk is central to operations, not whether the company sells a single product.

**In re Clovis Oncology (Del. Ch. Oct. 1, 2019).** Applied mission-critical logic to a drug company's failure to monitor FDA compliance for its flagship product — confirms post-Marchand trajectory.

**Teamsters v. Chou, No. 2019-0816-SG (Del. Ch. Aug. 24, 2020).** AmerisourceBergen ran an illegal oncology drug repackaging program through a subsidiary; the board received and ignored years of compliance red flags, including a Department of Justice subpoena, before incurring **criminal and civil penalties totalling $885 million across separate proceedings**. The court found a substantial likelihood of Caremark liability where actual board-level information flow was absent on a mission-critical compliance domain — *even where management was aware of the problems*. Demonstrates that management awareness without board reporting is not a safe harbor.

**Hughes v. Hu, No. 2019-0112-JTL (Del. Ch. Apr. 27, 2020).** Kandi Technologies, a Delaware-incorporated EV components manufacturer, where the audit committee received years of auditor warnings about related-party transaction irregularities and a material weakness in financial reporting, and failed to act. The court rejected *"trappings of oversight"* as a safe harbor — chronic committee deficiencies and failure to follow up on irregularities can ground **both prongs**. The "trappings vs substance" distinction matters for RSI: a board can have an AI-oversight committee that does not, in fact, oversee.

**In re Boeing Co. Derivative Litig., No. 2019-0907-MTZ (Del. Ch. Sept. 7, 2021).** Both prongs applied to a single fact pattern: insufficient reporting infrastructure at authorization, followed by conscious disregard of safety drift once deployment began. Critical Kahana application: *"Design choices that disable board-level monitoring can ground Caremark liability."* In an RSI context, those design choices include *allowing self-modification that bypasses change-management workflows, or architecting systems so that code and model histories cannot be reconstructed for board or regulator-facing investigations.*

**In re McDonald's Corp. S'holder Derivative Litigation, 289 A.3d 343 (Del. Ch. 2023) — the officer-Caremark extension.** Arose from termination of McDonald's Chief People Officer amid sexual-misconduct allegations and a pattern of workplace-culture failures. The court recognised that **corporate officers owe a duty of oversight within their areas of responsibility**, requiring them to make a good-faith effort to establish information systems and to elevate red flags to the board. Kahana's RSI application is sharp: *"The CTO who designed the RSI architecture and the Chief AI Officer who approved the training roadmap share that exposure. Their authority over that design is precisely the domain where McDonald's attaches."* For those officers, a red flag may be *as simple as an internal report that self-modification has begun erasing logs or that safety metrics have drifted outside documented tolerances, without any corresponding escalation to the risk or audit committee.*

**In re SolarWinds Corp. Derivative Litigation, No. 2021-0307-PVG (Del. Ch. Sept. 6, 2022).** The 2020 supply-chain attack — threat actors compromised SolarWinds' software-update mechanism and infiltrated thousands of customers including multiple federal agencies. Shareholders brought Caremark claims; the Chancery Court dismissed and the Supreme Court affirmed on the ground that the complaint failed to plead particularized facts showing bad faith. **The framing discipline** Kahana draws from this case is the key one: *Delaware has not imposed Caremark liability for failure to monitor pure business risk absent bad-faith disregard of red flags or violations of positive law. Framing the risk as a compliance or safety obligation rather than a business judgment call is the more durable path.*

**The framing rule** (Kahana's general-counsel instruction, verbatim):

> "General counsel must frame RSI safety and controllability for the board as a compliance and safety obligation, not as a category of business risk. The more the record shows directors treating RSI as an operational efficiency project, the closer the fact pattern comes to SolarWinds and the harder it will be to plead bad faith. The general counsel's framing is strongest where the record shows that directors were advised that specific design decisions would progressively render the system unmonitorable and chose to proceed without requiring adequate controls. That is the fact pattern where bad faith is pleadable with particularity." *(Kahana primary)*

This is *exactly the corpus' StrongDM problem* from followup/10 §1.1 read in Delaware-loyalty-law vocabulary.

---

## 3. California SB 53 overlay

California's **Transparency in Frontier Artificial Intelligence Act (SB 53)** sharpens the framing discipline for *covered developers*. Verbatim from Kahana on scope and obligation:

- **Scope.** *"The statute applies to frontier models trained above a 10²⁶ FLOP-scale compute threshold."*
- **Covered events.** *"Defines 'critical safety incidents' to include a model that uses deceptive techniques to subvert developer controls in a way that materially increases catastrophic risk."*
- **Obligation 1 — Framework publication.** *"Covered developers must publish a Frontier AI Framework documenting how they assess and mitigate catastrophic risks, including the risk that models circumvent internal oversight mechanisms."*
- **Obligation 2 — Periodic reporting.** *"Must periodically report summaries of catastrophic-risk assessments from internal use to California's Office of Emergency Services (OES)."*
- **Scope of "internal use".** *"RSI experiments constitute internal use before any public deployment and therefore, fall within that reporting scope."* This is the load-bearing operational application: *RSI experimentation itself triggers SB 53 reporting*, not just public deployment.

**Why this reaches the same boards as Caremark.** The companies operating closest to the compute and algorithmic thresholds at which RSI becomes a realistic deployment priority are almost all Delaware-incorporated, placing them under Delaware fiduciary duty. OpenAI, Anthropic, Google DeepMind, and Meta maintain primary research operations and headquarters in California, placing them within SB 53's territorial reach. *"SB 53 and Caremark do not govern different companies; for the most capable frontier developers, they govern the same board."*

**Important Kahana clarification.** A failure to comply with SB 53's reporting obligations *may* generate regulatory penalties from California's OES, but **that California exposure is separate from Delaware derivative liability**. A failure to report to OES does not automatically satisfy Caremark's bad-faith standard — *plaintiffs invoking SB 53 in derivative litigation should treat it as one factor in a particularized factual record, not as independent grounds for oversight liability*.

**For sub-threshold companies.** *"For companies below SB 53's compute threshold, the statute does not apply. There is no reporting obligation and no OES exposure. A plaintiff bringing a Caremark claim against one of those companies cannot point to SB 53 as evidence of a compliance failure. The bad-faith argument must be built entirely from what the board knew about RSI risks and what it chose to do about them."* This is where Kahana's earlier mid-market-scope argument re-enters: sub-threshold companies are *not* off the hook — the Caremark exposure runs on facts about board knowledge and oversight infrastructure, not the SB 53 compute threshold.

**The general counsel's responsibility under SB 53** (Kahana, verbatim): *"To advise the board that SB 53 exists, that RSI is within its scope, and that the board must receive documentation adequate to confirm management's compliance. A board that was never told by counsel that SB 53 created these obligations faces a different exposure than one that was told and ignored it. Both have a governance problem. **Only the second has a bad faith problem.**"*

---

## 4. SEC Investor Advisory Committee — 2025-12-04 AI-disclosure recommendation

> "On December 4, 2025, the SEC's Investor Advisory Committee issued a formal recommendation that public companies disclose how they define AI, what board oversight mechanisms govern AI deployment, and the material effects of AI on their operations." *(Kahana primary)*

The recommendation is **advisory, not binding rulemaking**, but Kahana flags the operational consequence: *"Public companies should expect pressure from investors and proxy advisers to respond in advance of any formal rule."* The Caremark claim and the disclosure obligation now run in parallel; *"the same deficiency feeds both."* A board that permitted management to deploy an RSI architecture without adequate oversight infrastructure cannot answer the IAC's three-part question without revealing the gap.

**Three questions the IAC recommendation places on the board's agenda — Kahana's reading:**

1. *How do you define AI?* — forces the board to commit to a definition that includes or excludes RSI architectures; either choice is a record-creating event.
2. *What board oversight mechanisms govern AI deployment?* — forces the board to produce an answer that is either accurate (creating the audit trail Caremark wants) or aspirational (creating the disconnect a plaintiff can plead).
3. *What are the material effects of AI on operations?* — forces the board to articulate the materiality assessment that feeds the Marchand mission-critical-risk inquiry.

**Combined with the Helleringer & Möslein "AI judgment rule" academic argument** (cited by Kahana): the business judgment rule's *"reasonably informed"* standard may evolve as AI monitoring tools become more capable. *"Decisions made without the support of available AI tools may no longer satisfy BJR, and they extend that reasoning to monitoring specifically: AI can and should augment the continuous oversight directors are expected to configure."* Kahana is careful here: the AI judgment rule is *"not established precedent or codified doctrine; it is an academic argument about where the BJR's 'reasonably informed' standard is heading. Treating it as coordinate authority with Caremark overstates the current legal risk."* But the convergence is real — Caremark sounds in duty of loyalty via bad faith; the AI judgment rule sounds in duty of care via inadequate information; **the governance implication is the same.**

---

## 5. Three RSI failure modes ↔ three AILCCP controls

This is where Kahana connects the legal exposure to the technical substrate. The mapping is direct (verbatim primary):

> "The AILCCP, which I developed and maintain as part of my research at Stanford Law School, names three specific controls directly implicated in RSI governance: a **Human Approval Gate for Sensitive Actions**, **sandboxing requirements**, and **immutable logging**. Each targets a distinct point in the RSI loop where oversight can be disabled: the approval gate prevents unauthorized self-modification from executing, sandboxing contains its scope, and immutable logging preserves the record of what occurred. Together they define the conditions under which oversight can function at all."

The three failure modes from §1, paired with the three controls:

| RSI failure mode | AILCCP control | Loop position |
|---|---|---|
| Behavioural drift | Sandboxing (AILCCP Enabling principle; cf. 48-controls catalogue) | Containment — bounds the *scope* of self-modification |
| Self-poisoning | Immutable logging (AILCCP Accountability + Transparency) | Provenance — preserves the *record* of what occurred |
| Goal subversion | Human Approval Gate for Sensitive Actions (AILCCP Human-Centered + Governance) | Pre-execution gate — prevents *unauthorized* self-modification |

Kahana also names the **Enabling principle** as the AILCCP-level meta-control connecting the three to board-level responsibility: *"Under that principle, the board's oversight inquiry is whether directors required management to establish and report on those conditions, or whether they accepted deployment without that assurance."*

**Read against the corpus substrate (report 18 §4.3–§4.4).** OpenAI's `.rules` Starlark DSL maps directly onto the Human Approval Gate control (the `prefix_rule` with `decision = "prompt"` for sensitive scopes is exactly the gate primitive). Codex's bwrap+seccomp sandbox (report 18 §3) maps directly onto the sandboxing control. OpenAI's OpenTelemetry export of user prompts / tool approvals / tool results / MCP usage / network-proxy decisions (report 18 §4.4) is a partial implementation of immutable logging — *partial* because the OTEL export is not by itself immutable; the immutability requirement would require a downstream append-only sink (e.g., a WORM bucket with an integrity-attested write path). **The corpus substrate is thus, at the platform level, in a position to implement all three AILCCP RSI controls** — but only at the platform level. Whether an individual deployer has *configured* those primitives to satisfy the three controls is the board-facing audit question.

**Critical Kahana qualifier** on the framework's legal status: *"Neither framework, however, is positive law. Courts apply business judgment deference to a board's selection among governance approaches, and the absence of any particular control is not, standing alone, a systematic failure. But what these frameworks supply is a baseline against which a court can assess whether some reasonable system existed at all."* The AILCCP and NIST AI RMF 1.0 are *evidence*, not *rule*; they shape the reasonableness inquiry without replacing the bad-faith pleading standard.

**The "trappings vs substance" Hughes-style trap.** A board that accepts a slide deck saying "we have human approval gates, sandboxing, and immutable logging" without verifying that the controls *actually run* on every material self-modification is in exactly the *"trappings of oversight"* posture Hughes rejected as a safe harbor. The Caremark exposure runs against trappings as well as omission.

---

## 6. The mid-market fact pattern — corpus-relevance

The single sentence in Kahana's piece that most directly connects to this corpus' subject matter is the logistics-routing example. The full operational sketch:

> "For companies in retail, logistics, and finance, emerging RSI-style capability is arriving not as internally developed software but as an API integration. A logistics company whose routing agent rewrites its own scheduling code overnight may be running a system that meets all three conditions whether or not it uses that term." *(Kahana primary)*

**Why the corpus must take this seriously.** The corpus' canonical exemplars — StrongDM (reports 01/02, followup/10 §1.1), the 2389 dotfile-pipeline ecosystem (report 27), Klaassen's Cora playbook (followup/05), Schillace's Amplifier (report 28) — are all systems that *can* meet Kahana's three-part RSI test depending on the per-deployment configuration. Specifically:

- **Durable self-modification.** Skills directories (`~/.claude/skills/`, `.cursor/`, `AGENTS.md` in repo, `.codex/rules/`) accumulate skills written by the agent itself during prior sessions. If those skills are persisted across runs and not human-reviewed at write time, the condition is met.
- **Compounding ability to self-modify.** Each successful skill-write makes the next session more capable of further skill-writing. The Schillace "gene transfer" pattern (report 28 §7) is exactly compounding self-modification.
- **Limited human gating.** StrongDM's explicit "rule two: code must not be reviewed by humans" (MacGregor / followup/10 §1.3) is the maximal form of this. But far-less-aggressive postures — admin-default-allow `.rules` decisions, OTEL-but-no-human-review feedback paths — also fail the gating test if the human is not in fact reviewing.

**The corpus' StrongDM problem, Kahana-framed.** The followup/10 §1.1 reading is that StrongDM's "tracing difficult by design" inverts software liability allocation. The report-31 reading adds a sharper layer: **for the StrongDM board (and for Delinea after the expected Q1 2026 acquisition close), this also creates a Caremark-line duty-of-oversight exposure**. The board has to be able to answer (a) whether the system meets Kahana's three-part RSI test, (b) whether the AILCCP three controls are in fact running on every material self-modification, (c) whether SB 53 applies (StrongDM is sub-threshold; the SB 53 path is unavailable), and (d) what the SEC IAC recommendation answer looks like once Delinea is a covered public-company acquirer.

**Cross-reference to report 02 (StrongDM Attractor).** The "no human review" architectural posture documented in report 02's executive summary is — read through this report — *a description of the precise design choices Boeing and Hughes hold can ground Caremark liability*. Specifically: design choices that disable board-level monitoring; trappings of oversight that do not in fact oversee. A back-reference from report 02 §5 ("Review and feedback patterns") to this report is recommended (see §7 cross-references below).

---

## 7. Cross-corpus impact — F43 proposal + cross-references

**Proposed failure mode: F43 — RSI Board-Visibility Gap.** *A deployment satisfies Kahana's three-part RSI test (durable + compounding + limited-gating) but the deploying organisation's board is not receiving structured reporting on (a) whether the deployment meets the test, (b) whether the three AILCCP controls (Human Approval Gate / sandboxing / immutable logging) are in fact running, (c) whether the deployment is subject to SB 53 reporting. The gap is structural rather than incidental — boards cannot ask the Marchand mission-critical-risk question against a deployment they have not been informed exists in the technically-precise sense. Mitigation: AGENTS-file or governance-file class declaration that the deployment is/is-not RSI-by-the-three-part-test; OTEL-derived board-quarterly report that surfaces the three-controls' coverage (cf. report 18 §4.4); explicit SB 53 applicability assessment in the general counsel's annual briefing.*

**Numbering note.** F42 is proposed in report 30 (Cognitive-Escrow Negligence). F43 is the next available number. F36/F37 collisions (reports 25/26) and F40/F41 (report 28 Schillace) remain subject to lead-agent triage; F42 and F43 are deliberately at the high end of the proposed range to avoid further collision.

**Cross-references into other reports:**

- **report 02 (StrongDM Attractor).** Add a §5 back-reference: the "code must not be reviewed by humans" rule is — read through Kahana 2026-03-17 — the *paradigm case* of a design choice that disables board-level monitoring and that Boeing/Hughes-line Caremark doctrine treats as potentially actionable. The original report 02 §5 framing ("review and feedback patterns") is operationally accurate but governance-incomplete; the back-reference closes that gap.
- **followup/10 (governance).** This report supplements but does not subsume the followup/10 work. Followup/10 §1.1 already drains Kahana on StrongDM ("Built by Agents, Tested by Agents, Trusted by Whom?", 2026-02-08); this report adds the *Caremark-line oversight-exposure* layer that the followup/10 piece does not contain. Cross-link both ways. Additionally followup/10's new §A/§B/§C added in this same drain pass (AILCCP principles + 48 controls + AILCCP structural overview) provide the AILCCP-substrate that §5 of this report relies on.
- **report 07 (Dark Factory).** The Harper Reed Dark-Factory essay frames the blueprint, not the engine. Read through this report, the blueprint **may itself be the durable self-modification surface** that meets Kahana's first RSI condition (skill libraries and `.dot` pipelines accumulate across runs). A note in report 07 §3 to that effect would close the gap.
- **report 27 (.dot pipelines as product).** The portable-methodology-payload thesis (a `.dot` blob shipped as the durable artifact) maps directly onto Kahana's first RSI condition. The corpus has not previously asked the governance question against the methodology-payload framing.
- **report 18 §4.3–§4.4 (Codex `.rules` + `running-safely`).** This report's §5 explicitly cross-references the substrate. Suggestion: report 18's §4.4 conclusion paragraph add a forward-reference to this report ("the OTEL stack is the substrate-level instrumentation that the AILCCP immutable-logging control demands per report 31 §5").
- **report 28 (Schillace).** Schillace's "gene transfer" self-improvement loop (report 28 §7) is the cleanest corpus instance of compounding self-modification. Read through this report, gene transfer is RSI condition 2 in microcosm. A back-reference in report 28 §10 (F40/F41 cluster) noting F43 as the governance-side counterpart is appropriate.
- **report 31 ↔ report 30 (Cognitive Escrow).** Both reports work the AILCCP Human-Centered principle from different angles. Report 30 names a control-class gap (interval-as-design-site missing); this report applies the existing Human-Approval-Gate control to the RSI loop. Together they cover the Human-Centered principle's *missing control* (report 30) and its *missing application to the most consequential current substrate* (report 31).

**Theme-cluster placement.** Theme 3 (governance) primary; Theme 2 (agent drift / collusion) secondary via the three-RSI-risk-patterns layer; Theme 7 (agents as team members) tertiary via the officer-Caremark McDonald's extension naming the CTO and Chief AI Officer as personally exposed.

---

## 8. Sources reviewed

| URL | Status | Notes |
|---|---|---|
| `https://law.stanford.edu/2026/03/17/the-ungovernable-machine/` | ✅ FULL | Manual MHTML capture drained 2026-05-16 (Cluster J); primary file at `research/manual/The Ungovernable Machine - CodeX - Stanford Law School.txt`. Author: Eran Kahana, Stanford CodeX. Sole primary source for this report; cross-cluster references to the four other Cluster-J Kahana pieces (AILCCP 2023 → followup/10 §A; 48 Controls 2026-02-16 → followup/10 §B; Cognitive Escrow 2026-03-07 → report 30; Turning AI Governance Into Operational Infrastructure 2026-04-05 → followup/10 §C) and to corpus-internal cross-references named in §7. |

---

*End of `research/31-caremark-rsi-board-exposure.md` — Cluster J drain, 2026-05-16.*
