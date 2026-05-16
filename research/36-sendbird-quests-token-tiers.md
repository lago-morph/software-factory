# 36 — Sendbird: Quests, Token Tiers, and the AI-God Leaderboard

**Status:** ✅ FULL
**Date:** 2026-05-16 (Cluster N manual drain)
**Primary sources:**
- *Lenny's Newsletter / How I AI* podcast — Claire Vo × John Kim, *"Quests, token leaderboards, and a skills marketplace: The elite AI adoption playbook"* (drained as show-notes summary `research/manual/Quests token leaderboards and a s.txt`).
- Companion blog: `https://www.chatprd.ai/how-i-ai/john-kims-playbook-for-ai-transformation`.

**Subject.** John Kim — co-founder and CEO of Sendbird. Describes the org-wide AI-adoption playbook that Sendbird has rolled out under its internal AI-product brand (the captures occasionally name an internal product "Delight.ai" — see §5.2 below for the disambiguation). The playbook has four interlocking primitives: (1) the **Automators** marketplace where employees file *quests* (automation requests) tagged with risk / weeks-saved / beneficiary, claimed by engineers or AI agents, completers earn XP; (2) **per-person daily-token tiers** from Beginner (<1M tokens/day) to **AI God** (>100M/day) as a visible AI-fluency leaderboard; (3) InfoSec-vetted secure app templates that let non-engineers build to production; (4) a cross-functional weekly AI task force led by an "AI Engineer for Internal Operations" who reports directly to the CEO + chief of staff.

**Cross-refs:**
- `research/32-shapiro-completion-chat-agent-claw.md` §6 (claw-printer / one-Claw-per-employee — supply-side peer).
- `research/35-lenny-howiai-spec-driven-and-team-ops.md` (Boxy as per-engineer fleet — peer demand-side primitive).
- `research/28-schillace-sunday-letters.md` §6 (compounding teams: 12-person team / >500 projects — the corpus-canonical supply-side anchor).
- `research/27-dotfile-pipelines-as-product.md` (per-pipeline as primitive — peer at a different layer).
- `research/13-round-2-synthesis.md` §3 (failure-mode framework F21–F33 — F47 is the candidate added here).
- `research/followup/10-governance.md` (governance overlay — visible-metric drift, Goodhart's-Law-on-tokens risk).

---

## 1. The thesis — gamified internal AI marketplace + visible per-employee fluency tiers

Sendbird's AI-adoption program is the corpus' first primary-source description of a top-down enterprise AI-transformation initiative that uses **game-design primitives** (XP, quests, leaderboards, tiered classes) rather than mandates. The two innovations that are corpus-novel:

1. **Automators** — an internal marketplace where any employee can file a "quest" (an automation request); engineers *or AI agents* claim the quest; completers earn XP redeemable for gift cards, tea-with-executives, or a slot to present at Wednesday standups. Quests are tagged with **risk level**, **weeks-saved**, and **beneficiary** so the org can see the value distribution. *"Make AI adoption fun, measurable, and rewarding."*

2. **Per-person daily-token tiers** — every employee has a token-usage tier visible on an internal leaderboard. The ladder: **Beginner (<1M tokens/day) → Intermediate → Expert → Architect → Catalyst → AI God (>100M/day)** (six tiers; verbatim from chatprd companion). The tiers are explicitly *not* performance-review inputs — they are aspirational + diagnostic; the goal is to bring people along the journey, not to penalize.

The framing intuition: **AI fluency is illegible by default** (you can't tell from the outside whether someone is using AI well, badly, or not at all). The token-tier leaderboard makes it legible at the cheapest possible measurement layer (token count). The Automators marketplace makes contributions legible too (you can see what each person has shipped / claimed / completed).

Three deep cross-references that make this corpus-significant:

- **Theme 1 (attention as scarce resource)** — the token-tier ladder is the empirical-practitioner inversion: *tokens spent per person* is the legible proxy for *attention deployed onto AI*. Where Schillace's framing is "output per unit of human attention," Sendbird's is "tokens consumed per person per day." They are the supply and demand sides of the same measurement.
- **Theme 5 (probing measurement)** — visible-metric design is itself a corpus-load-bearing concern. F47 below names the risk this metric *cannot* see, while §3 below argues for why Sendbird ships it anyway.
- **Theme 7 (agents as team members)** — the org-design primitive is the **person**, not the team. Three independent sources within ~90 days are converging on this primitive (§5 below).

---

## 2. The Automators platform — quest marketplace

### 2.1 What a quest looks like

Per the source captures, a quest in Automators is a structured object with at least the following fields (chatprd summary):

- **Title / description** — what the automation should do.
- **Risk level** — the safety/auditability classification.
- **Weeks saved** — projected time savings if shipped (the unit is *weeks-of-human-time-recovered*).
- **Beneficiary** — who in the org gets the recovered time.
- **Status / claimer** — open / claimed / shipped, with whoever (or whichever agent) is on it.

Anyone in the org files quests. Anyone (or any AI agent) can claim. The chatprd summary surfaces three reward currencies:
- **XP** — accrued for completed quests.
- **Gift cards** — XP cash-out.
- **Exec time** — XP redeemed for one-on-one time with John or another executive.
- **Wednesday standup slot** — XP redeemed for presenting your shipped quest to the entire company.

### 2.2 The marketing-team swag-store anchor

The companion blog opens with a vivid anchor: the marketing team — *not engineers* — built a **fully functional e-commerce swag store** with Stripe integration, custom designs, and a Konami Code easter egg that unlocks secret conference details. In the pre-AI world this would have required "two sprints of engineering time and probably would have been deprioritized." With Automators + secure templates (§4), it shipped in days, generates actual revenue, and was authored by a non-engineering team.

The corpus reading: this is the **non-engineer-as-builder** primitive that report 12 (adjacent ecosystem) and report 20 (Replit Agent) have been triangulating. Sendbird shows it works *at the marketing-function scale inside an enterprise SaaS*, not just at the individual-builder scale.

### 2.3 The "internal tooling as product" framing

Kim's framing per the chatprd summary:

> *"The most successful AI transformations treat internal tooling as a product, not a program."*

The distinction matters. A *program* is a directive ("Adopt AI by Q3"); a *product* has users, a roadmap, a feedback loop, and competitors-for-attention. Automators is the latter — non-mandate, opt-in, designed for delight, with reward mechanics. Compare:

- Glowforge (report 32 §6): "print Claws by the dozen" — supply-side product framing.
- Notion (report 35 §3): Boxy as an internal product engineers use as a harness.
- Sendbird: Automators as the *marketplace* product that brokers supply (engineers / agents) and demand (quest filings) inside the org.

The org-internal **marketplace** as primitive is corpus-novel. The other two are fleet primitives (one agent per person). Sendbird is a *trading floor* primitive (quests as the unit of trade).

### 2.4 The reward mechanics

The corpus' Theme-7 thread has not had a clear answer to *how* you produce voluntary AI adoption inside a large org. The mandate ("Adopt AI by Q3") is the negative incentive; what is the positive? Sendbird's answer is **game-design reward mechanics**:

- **XP** as the universal currency abstracts over the value of any given quest.
- **Tea with executives** is intentionally non-monetary — a status reward and a learning opportunity.
- **Wednesday standup slot** turns the completed quest into a public learning artifact for the rest of the org — supply-side compounding (other people see the demo and file their own quests).

This is structurally identical to the open-source contribution culture (commit badges, contributor leaderboards) translated to an enterprise. The intuition transfer is intentional: open-source taught us how to produce voluntary contributions at scale; Sendbird is applying that lesson to AI adoption.

---

## 3. Per-person daily-token tiers

### 3.1 The ladder

The full ladder, verbatim from the chatprd companion:

| Tier | Daily token usage | Frame |
|---|---|---|
| **Beginner** | < 1M tokens/day | "Start of the journey" |
| **Intermediate** | (mid-range, not specified verbatim) | — |
| **Expert** | (mid-range, not specified verbatim) | — |
| **Architect** | (mid-range, not specified verbatim) | — |
| **Catalyst** | (mid-range, not specified verbatim) | — |
| **AI God** | > 100M tokens/day | Top of the leaderboard |

Six tiers. The two anchored endpoints are < 1M (Beginner) and > 100M (AI God) — a 100× span. The Intermediate / Expert / Architect / Catalyst boundary numbers are not in the captures and would require a separate primary fetch.

### 3.2 What the tiers are *for*

Kim frames the tiers explicitly:

> *"Measure token usage without shame, and create tiers that make it aspirational. … Every manager can see where their team members are and tailor enablement accordingly. This isn't about performance reviews; it's about bringing people along the journey and making AI fluency visible and celebrated."*

Three properties:
1. **Aspirational, not punitive.** AI God is a *celebrated* tier, not a quota. Beginner is not a failing grade.
2. **Managerial-diagnostic.** Managers see their reports' tiers and tailor enablement. Low-tier reports get one-on-one support, not blame.
3. **Visible.** The leaderboard is public inside the org.

### 3.3 The "smoothness" interpretation — 24/7 agent work

The corpus-significant detail (from chatprd summary):

> *"The goal isn't just to use AI during work hours but, rather, to smooth the curve so AI works around the clock. John monitors token usage over time and looks for smoothness in the curve. Dips mean people are on weekends or vacation and AI isn't working. When the curve smooths out, it means AI partners are working 24/7."*

The argument: the *shape* of the token-usage curve is itself a measurement, not just the magnitude. A curve that dips on weekends means the agents are still gated on humans. A smooth curve means the agents are running unattended (heartbeats / dreaming in Shapiro's terms; report 32 §4). The smoothness target is the *autonomy* dimension expressed as a measurable curve property.

This connects directly to:
- **Shapiro's Claw definition** (report 32 §2): "works without you" — the smooth curve is the empirical signature of agents that work without the human.
- **Cherny's "5 agents steady state"** (followup/03): the agent runs while Cherny sleeps.
- **Schillace's "compounding teams"** (report 28 §6): the team-shape claim that 3 feels like 30 because agents work continuously.

Sendbird operationalizes this as a *curve-flatness metric* on token usage. That is a corpus-novel measurement primitive worth elevating.

### 3.4 Exec-modeled top usage

A small but corpus-significant detail:

> *"The top token consumers at Delight.ai are the executives."*

Leadership-modeled top usage. This is the inversion of the standard "executives don't use the tools they buy for their org" failure mode. Kim explicitly frames it:

> *"Leadership has to model the behavior, not just mandate it. When leaders show up with new capabilities and ship things faster, it signals to the team that this is real and important."*

Cross-reference with Nystrom (report 35 §8) and Klaassen (followup/05) — both make the argument that engineering managers should write code. Sendbird extends that to the executive layer: *the executives should be top token consumers*. The exec-as-power-user signal is the leadership-layer instance of the manager-as-engineer reframe.

### 3.5 The one-on-one-with-zero-tokens move

Final detail of the playbook:

> *"John also does one-on-ones with people who aren't using tokens: 'We noticed you haven't been spending any tokens. Can we help you? What's stopping you?'"*

This is the **diagnostic** layer of the tier system. Zero-tier employees aren't punished; they're individually engaged to find out what's blocking them. This is also a Theme-5 (probing measurement) implementation: the metric is not just a leaderboard, it's a *trigger condition* for individual-level enablement.

The combined system — aspirational tiers + curve smoothness + exec-modelled + zero-token-one-on-ones — is operationally sophisticated. It's a small example of what a well-instrumented AI adoption program can look like. The corpus' Theme-5 thread has not had an industrial-grade implementation of this kind before now; Sendbird's is the first.

---

## 4. InfoSec-vetted secure templates for non-engineer builders

The fourth interlocking primitive: **secure, compliant templates that non-engineers can build on top of.**

From the chatprd companion:

> *"The biggest unlock for non-technical builders is creating secure, compliant templates they can build on top of. John's team created app templates where authentication, environment setup, databases, and security are pre-configured and vetted by InfoSec. Marketers, salespeople, and CSMs just extract the template and build their idea on top."*

This is the substrate piece that makes Automators work. Without InfoSec-vetted templates, non-engineer builders would either (a) be blocked from production by security review, or (b) ship insecure things. Templates resolve the blocker.

### 4.1 The substrate parallel

This is structurally identical to:
- **Codex `.rules` DSL** (report 18 §4.3) — pre-vetted rules that constrain the agent's action space.
- **OpenAI's managed network policy + OS keyring credentials** (report 18 §4.4) — substrate-level security defaults.
- **Anthropic's Claude Code sandbox** (report 23 §8) — pre-vetted sandboxing.

In all four cases the principle is **the substrate carries the security guarantee, not the operator.** Sendbird's innovation is making this principle accessible to *non-engineer operators*: a marketer can build a swag store because the template already has the security checked.

### 4.2 The governance posture

This is also the corpus' first primary-source description of a **non-engineer-shipping-to-production** governance regime. The Caremark / RSI literature (report 31) names board-level exposure from RSI-equipped systems. Sendbird's template regime is the operational counterpart: by pre-vetting the substrate, the governance burden moves from the operator (the marketer) to the substrate maintainer (InfoSec + the AI Engineer for Internal Operations).

The strongest reading: **non-engineer-as-builder is only governance-tractable when the substrate carries the security and audit guarantees.** Without vetted templates, the only safe state is "no non-engineers in production"; with them, the org can scale builders far beyond its engineering count.

---

## 5. Cross-functional AI task force + per-employee primitive

### 5.1 The org structure

From chatprd companion:

> *"Build a cross-functional AI task force that meets weekly to unblock challenges. John created a role called AI Engineer for Internal Operations that reports directly to him and the chief of staff. This person works cross-functionally with the CTO, engineering, and InfoSec to vet tools, set up compliant tech stacks, and remove barriers. They meet weekly as a task force to discuss what's blocking people and how to enable faster iteration."*

Five org details to mark:
1. **AI Engineer for Internal Operations** is a *role*, not a one-off project.
2. **Reports directly to CEO + chief of staff** — not buried in engineering.
3. Works **cross-functionally** with CTO, engineering, InfoSec.
4. **Weekly cadence** — fast iteration on blockers.
5. The role's primary deliverable is *unblocking* + tool/stack vetting + template maintenance.

This is the org-design counterpart to Sendbird's culture-design innovations. The role is what keeps Automators + tiers + templates running. The corpus has not previously had a primary anchor for this role / structure.

### 5.2 The Delight.ai naming question

The chatprd summary says *"top token consumers at Delight.ai are the executives."* Sendbird is the company; Delight.ai appears to be either (a) an internal product name, (b) a rebrand for the AI-product surface, or (c) a separate Kim company. The two captures do not disambiguate. **Pinning notation: treat "Delight.ai" as the internal AI-product surface inside Sendbird until further captures resolve.** This is consistent with Kim being CEO of Sendbird and Delight being his internal AI initiative; cross-link followup target for the resolution.

### 5.3 Three independent sources converging on per-employee

The corpus-significant aggregation. Three sources within roughly 90 days (Feb–May 2026) describe **per-employee as the org-design primitive**:

| Source | Date | Per-employee framing |
|---|---|---|
| **Glowforge / Shapiro** (report 32 §6) | May 13 2026 | "Print Claws by the dozen: one for every coworker, one for every department, one for every special project." |
| **Notion / Nystrom** (report 35 §3) | recent (Lenny + chatprd) | Every engineer @-mentions Codex from Notion tasks; every engineer has their own Boxy-fed PR fleet. |
| **Sendbird / Kim** (this report) | recent (Lenny + chatprd) | Per-employee tokens / quests / tiers — visible on a leaderboard. |

The three vendors describe **the same primitive from three angles**: the supply side (Glowforge — each person gets a Claw fleet), the demand side (Notion — each person dispatches to Codex from Notion tasks), and the measurement side (Sendbird — each person's usage is measured + ranked). They are aware-of-but-not-citing one another; the convergence is genuine.

The corpus' Theme-7 ("agents as team members") had implicitly assumed the unit of analysis was the *team*. These three sources flip the unit to the *person*. Sendbird makes it most explicit (token tiers are per-person and visible). The convergence is large enough to warrant a synthesis-layer note: **the per-employee unit is replacing the per-team unit as the relevant org-design primitive for AI deployment**.

The supply-side compounding-teams anchor in report 28 §6.2 (12-person team / >500 projects) is the *ratio*; this report (and reports 32 + 35) ground the *unit*. Combine: 12 people × per-person-as-primitive = an org structure where every person is a single-IC team with a fleet of agents, and the team boundary is the management layer of those fleets.

### 5.4 Schillace ratio + Shapiro fleet + Sendbird measurement = a complete org-design pattern

Stack the three:

```
                           org-design pattern
  ┌─────────────────────────────────────────────────────────────────┐
  │ unit              : the person + their agent fleet              │
  │ supply ratio      : Schillace's >500 projects / 12 people       │
  │ supply primitive  : Shapiro's claw-printer (Claws by the dozen) │
  │ demand surface    : Nystrom's Boxy (Notion task → PR)           │
  │ measurement       : Kim's token tiers + smoothness curve        │
  │ marketplace       : Kim's Automators (quests + XP)              │
  │ substrate         : Kim's InfoSec-vetted templates              │
  │ governance        : Kim's weekly AI task force                  │
  └─────────────────────────────────────────────────────────────────┘
```

This is the corpus-first articulation of an end-to-end *per-employee org-design pattern for the AI era*. Each cell is anchored to a primary source. This is the strongest synthesis-layer artifact to come out of Cluster N.

---

## 6. Hiring rewrite — curiosity, agency, energy > years of experience

The fourth axis of Kim's playbook is hiring.

From the chatprd companion:

> *"The most important hiring criteria for AI-first companies are curiosity, agency, and energy — not tenure or experience. John rewrote job descriptions to optimize for people who are curious, willing to go deep, and figure things out on their own. He lowered the bar on years of experience and raised the bar on learning ability. In a world where you can build a custom learning center for any topic in 20 minutes, the constraint isn't access to knowledge; it's the drive to learn."*

Three explicit moves:
1. **Lower the years-of-experience bar.** Senior years are no longer the dominant signal.
2. **Raise the learning-ability bar.** The bar tightens on the rate at which someone learns, not the depth of what they know already.
3. **Optimize for curiosity, agency, energy.** Three behavioural signals that travel together.

### 6.1 Theme-7 implication

This is corpus-significant for Theme-7. If the agents handle execution, the human's *operator-level* capabilities — direction, judgement, curiosity-driven exploration — are what dominates. Years-of-execution-experience is partial obsolescence; rate-of-curiosity-driven-learning is the leading signal.

Compare:
- **Nystrom** (report 35 §8): managers should write code; AI removed the meeting-prep tax.
- **Klaassen** (followup/05): stop thinking of yourself as a coder; start thinking of yourself as someone who directs agents.
- **Kim** (this report): hire for the curiosity + agency + energy to drive AI well, not for the years of pre-AI execution experience.

All three converge: **the post-AI engineering role is "operator who supervises agents"**, and the dominant hiring signal is the disposition required to operate well, not the years of pre-AI execution.

### 6.2 Start-with-champions tactical advice

Kim's start-with-champions framing (chatprd summary):

> *"John's advice to CEOs struggling with AI adoption: find the people in your organization who are already curious and have agency. Make them the champions. Give them the spotlight. … Innovation doesn't start from theoretical structures — it starts with people who have energy and a story to tell."*

This pairs with the Wednesday-standup-slot reward (§2.1) — the champions get to present their work, which both rewards them and seeds adoption through demo-driven imitation.

---

## 7. Cross-corpus implications

### 7.1 Proposed candidate failure mode

**F47 — Visible-Metric Drift (Goodhart-on-Tokens).** When per-employee token tiers are visible on an org-wide leaderboard, employees will optimize tokens. Tokens are *not* a quality proxy. Goodhart's Law: when a measure becomes a target, it ceases to be a good measure. The token-tier system creates the metric-target conflation that Goodhart predicts will collapse the metric's usefulness.

Concrete operational signatures of F47:
- Employees pad token usage with low-value queries to climb tiers.
- Employees route work *away* from cheaper / better-targeted models / non-AI approaches to inflate token count.
- "Token theatre" — work that looks high-token-volume but produces no shipped artifacts.
- AI God tier becomes a vanity badge decoupled from impact.

Mitigations:
- **Pair token tiers with Automators-quest-completion-count** as a co-metric. Sendbird does this implicitly. The corpus should pin it as an explicit recommendation: token-tiers without a shipped-output co-metric will Goodhart.
- **Audit AI-God-tier outputs.** Spot-check what high-tier users are actually producing.
- **Curve-smoothness as a quality proxy.** Kim's smoothness metric is partial protection — token-padding gives smooth curves, but only if it's continuous; spiky padding fails the smoothness check.
- **Quest XP must dominate tier-XP for promotions / rewards.** Token tier is diagnostic; XP from completed quests is the real impact measurement.

F47 number rationale: F44 (Production-Scissors, report 32), F45 (Language-as-Harness, report 33), F46 (Single-Model Review Blindspot, report 34), F47 (Goodhart-on-Tokens, this report). The unresolved F36/F37 collision flagged in INDEX.md §"Looking for a failure mode" remains pending lead-agent reconciliation; F44–F47 chosen at the high end of the range to avoid further collision.

### 7.2 Net adds / refines

| Existing report / framework | What this report adds / refines |
|---|---|
| **Theme 1** (attention as scarce resource) | Sendbird's token-tier ladder is the empirical-practitioner inversion: tokens-per-person as a legible proxy for attention-deployed-onto-AI. |
| **Theme 5** (probing measurement) | First corpus primary anchor for per-employee AI-fluency measurement at industrial scale. Six-tier ladder + curve-smoothness + zero-token diagnostic. |
| **Theme 7** (agents as team members) | Combined with reports 32 + 35, this report makes three independent corpus anchors for **per-employee as the unit of org design**. The convergence deserves synthesis-layer elevation. |
| **Report 28 §6.2** (Schillace 12-person / >500 projects ratio) | Sendbird is the demand-side / measurement-side counterpart. The 500/12 ratio is the supply-side outcome; the per-employee primitive is the underlying mechanism. |
| **Report 32 §6** (claw-printer / one-claw-per-employee) | Sendbird's Automators + tiers + quests are the *measurement & marketplace* counterpart to Shapiro's *fleet* primitive. The two are complementary, not redundant. |
| **Report 35 §3** (Boxy as per-employee dispatch surface) | Sendbird is the *measurement* on top of the Boxy-style fleet. Together: Notion provides each engineer a dispatch surface; Sendbird measures + rewards each employee for using one. |
| **Followup 10** (governance) | Adds F47 (Goodhart-on-Tokens) to the governance/measurement risk surface. |
| **Followup 06** (competitor landscape) | Sendbird as a *user* of AI tooling (not a competitor in the AI-coding-agent space) — but worth a one-line note as a methodology survey reference: their Automators + token-tier + InfoSec-template pattern is a methodology benchmark for other CEOs / CTOs / CPOs. |

### 7.3 Project-internal corollaries

For the project:
- Add **per-person measurement + leaderboard** as a Theme-5 design pattern in the methodology library.
- Add **Automators-style quest marketplace** as a Theme-7 org-design pattern. The unit of work is the quest with structured risk / time-saved / beneficiary fields.
- Add **InfoSec-vetted secure templates** as a Theme-4 substrate primitive — the substrate carries the security guarantee, freeing non-engineer builders.
- Document the **"one-on-one with zero-token employees"** as a soft-power adoption pattern.
- Flag **F47 (Visible-Metric Drift / Goodhart-on-Tokens)** in any measurement-design discussions.

### 7.4 What this report does *not* answer

- The Intermediate / Expert / Architect / Catalyst tier boundaries (only Beginner < 1M and AI God > 100M are anchored).
- The Automators technical substrate — is it a Notion-style marketplace, a custom internal tool, a Slack-app, a Linear-app?
- Whether quest XP redemption rates are tracked.
- The Delight.ai vs Sendbird naming relationship.
- Whether the InfoSec-vetted templates are open-source / shareable across companies.
- How "AI agents claim quests" works mechanically — what dispatch surface? How is an AI agent given an Automators identity?

These are followup candidates for a future drain or a direct fetch of the chatprd workflow-detail pages.

---

## 8. Sources reviewed

| Source | Status | Notes |
|---|---|---|
| `research/manual/Quests token leaderboards and a s.txt` (Lenny show-notes / chatprd summary) | ✅ FULL | Show-notes / blog summary of the *How I AI* episode. ~600 words; covers all four primitives. |
| `https://www.chatprd.ai/how-i-ai/john-kims-playbook-for-ai-transformation` (companion blog) | ✅ FULL (as summary; companion to the above) | Confirms the six-tier ladder, AI-God endpoint, smoothness metric, exec-modelling, zero-token-one-on-ones, hiring rewrite, start-with-champions. |
| Lenny's Newsletter URL (audio episode primary) | ❌ not drained | The audio transcript was not in the manual folder; would surface the missing tier boundaries and Automators mechanical details. **Followup candidate.** |
| chatprd workflow detail pages — how-to-create-an-internal-AI-marketplace-to-crowdsource-automations; how-to-build-a-personal-AI-generated-learning-center-on-any-topic; how-to-automate-personal-knowledge-management-with-an-AI-gardener | ❌ not drained | Linked from chatprd companion. **Followup candidate.** |
| John Kim on X / Sendbird engineering blog | ❌ not surfaced | Likely external references exist. |
