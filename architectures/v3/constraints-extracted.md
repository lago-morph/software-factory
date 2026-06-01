# Extracted user-given constraints (Phase 0.1)

**Source-of-truth rule.** This document carries **only constraints the user has stated** — not recommendations the lead agent or prior synthesis rounds have generated. Recommendations are explicitly excluded so they cannot anchor the v3 synthesis from the brief.

**Provenance convention.** Every constraint cites where the user said it. If a constraint cannot be cited to user-authored text, it does not belong here.

**Naming convention.** User constraints are tagged `UC1` through `UC8` (UC = *User Constraint*). The `UC` prefix is deliberate — it disambiguates user constraints from the `C10–C16` Round-2 *consensus* tags that appear in [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §1.1 (which `UC9` would have collided with). Anywhere downstream synthesis cites a `C`-tag without the `UC` prefix, the reference is to the Round-2 consensus catalog, not this file.

---

## UC1 — The artifact being built

> *"a running lights-out software factory for greenfield applications."*

— [`research-plan.md`](../../archive/research-plan.md) opening sentence (user-authored).

**Extracted as constraint:**
- **The artifact is a software factory** (not a coding assistant, not a chatbot, not an IDE plugin).
- **The operating mode is lights-out** (no continuous human-in-the-loop).
- **The original mandate was greenfield.**

---

## UC2 — Brownfield added as a co-equal mandate

> *"I want to add one complication. I eventually want to have something that also works with existing systems. Greenfield and brownfield can be totally different solutions."*

— User message, current conversation.

**Extracted as constraint:**
- **Brownfield is a first-class mandate alongside greenfield.**
- **Greenfield and brownfield may produce different architectures** — they are not required to share a single architecture, but they are required to share substrate where it makes sense.

---

## UC3 — Mandate-fit must be explicit in the final recommendations

> *"when creating the final recommendations, it should explicitly say which solutions are strong for greenfield, brownfield, or both."*

— User message, current conversation.

**Extracted as constraint:**
- **Every architecture in the v3 set carries an explicit `mandate-fit` tag**: `greenfield`, `brownfield`, or `both`.
- **`both` is a stronger claim** and requires affirmative justification (not assumed).

---

## UC4 — User's working hypothesis (treated as falsifiable, not assumed)

> *"My suspicion is that we won't find one that works best with both, because a brownfield one will focus on analyzing what is there and growing it, whereas a greenfield approach is going to strongly depend on the spec, and will have a malleable architecture during refinement of the spec, whereas brownfield will not."*

— User message, current conversation.

**Extracted as constraint:**
- **The synthesis treats the "no single architecture works for both" claim as a hypothesis to test against the corpus**, not as an assumed truth. The plan must be able to *find* a both-mandates architecture if the corpus supports one (e.g., a substrate-heavy + thin-methodology design).
- The specific tensions the user names — **spec-malleability for greenfield** vs. **existing-architecture-as-given for brownfield** — are first-class concerns in the synthesis.

---

## UC5 — Accuracy ranks above speed and tokens

> *"accuracy >> speed >> tokens. I have more tokens than I know what to do with, and I can wait for the results. But it has to be right."*

— User message, current conversation.

> *"I'd rather get this right than get this fast or cheap."*

— User message, current conversation.

**Extracted as constraint:**
- **The synthesis budget is dominated by accuracy.** Token spend and wall-clock time are explicitly de-prioritized when they trade against correctness.
- **Default to more bias guards, not fewer.** Default to persona-diverse review. Default to archive-and-rebuild over edit-in-place when there's risk of silent anchoring.

---

## UC6 — The corpus is the post-Round-12 corpus

> *"I expect MAJOR changes to both the suggestions and the number and content of all the specific architecture recommendations."*

— User message, current conversation.

> *"we have that stuff in our git history, just get it out of the way so we don't confuse things."*

— User message, current conversation, on archiving the existing 4 architectures.

> *"We might also want to consider doing that with the existing syntheses. Get rid of them, and then after we are done, see if there are any things in there that can be added. But start fresh."*

— User message, current conversation, on archiving the existing syntheses.

**Extracted as constraint:**
- **The synthesis inputs are the post-Round-12 corpus** (reports 01–38 + followups 01–14 + supporting catalog material), not a subset.
- **The synthesis output is not constrained by the existing 4 architectures**: their count, their names, and their conclusions are explicitly *not* binding on v3.
- **Existing 4 architectures and existing 2 syntheses are archived** before v3 work begins, to prevent silent anchoring. Back-fill happens later (Phase 7) as a controlled re-introduction.

---

## UC7 — Seed source list (frozen, primary research input)

> The 17-URL list in [`initial-sources.md`](../../archive/PR-180-initial-sources.md) — user-authored, Round-1 seed.

**Extracted as constraint:**
- The original seed list is frozen and remains primary research input. Subsequent rounds extended it; the v3 synthesis works against the full extended corpus, not just the seed.

---

## UC8 — Process constraints from AGENTS.md (binding)

> [`AGENTS.md`](../../AGENTS.md) — user-authored project conventions.

**Extracted as constraint:**
- **PRs default to ready-for-review, not draft** ([`AGENTS.md`](../../AGENTS.md) "PRs" section).
- **Internal markdown references use descriptive relative links** ([`AGENTS.md`](../../AGENTS.md) "Internal document references" section). All v3 artifacts must comply.
- **External-source citations in `.md` files go through [`sources.json`](../../reference-only/sources.json)** ([`AGENTS.md`](../../AGENTS.md) rule 4).
- **Process skills are non-negotiable triggers** ([`AGENTS.md`](../../AGENTS.md) "Process skills" section). `issue-management`, `always-commit-skill-to-repo`, `in-flight-workflow-tracking` apply throughout.

---

## What is explicitly NOT a constraint

The following appear in prior documents but are **lead-agent or prior-synthesis recommendations**, not user constraints. They do *not* anchor v3:

- ❌ "Compound Atelier as baseline" ([[`00-comparison`](../../archive/architectures-v2/00-comparison.md)](../00-comparison.md) §7.1).
- ❌ "Atelier + Refinery's layered-spec discipline on top" ([`research-plan.md`](../../archive/research-plan.md) §"What 'enough research' should trigger" item 2).
- ❌ "OpenHands SDK + Overstory-design-in-Python as substrate stack" ([`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §6.2, §8).
- ❌ "Four architectures" as a count ([[`00-comparison`](../../archive/architectures-v2/00-comparison.md)](../00-comparison.md) §1).
- ❌ "L3 Augmentation as the empirical 2026 ceiling" ([`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §2.1) — this is a corpus claim worth testing against the lights-out mandate, not a user constraint.

These items live in the archive after Phase 0.4–0.6; they re-enter the v3 process as Phase-7 back-fill candidates, judged against the v3-from-scratch output.

---

*End of constraints-extracted.md.*
