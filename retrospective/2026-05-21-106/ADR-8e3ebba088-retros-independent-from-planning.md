# ADR: Retrospective process is independent from research planning

- **ID**: ADR-8e3ebba088
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-106.md
- **PRs covered**: #106

## Context

`research/PLAN.md` had explicit retrospective entanglement across five sections: §1 status line referenced "the cumulative retrospective backlog has grown well past v0.13's five-retrospective snapshot (17+ new retrospectives have landed since 2026-05-16; §3.4 has not been recounted)"; §3.4 ("Pending retrospective decisions") tabulated unbuilt skill specs and proposed ADRs from a five-retrospective snapshot; §5.0 item 7 made "the cumulative five-retrospective decision backlog (§3.4) resolved one way or the other" part of the definition-of-done; §5 list item 5 was "Retrospective decisions — pick scope across the cumulative backlog"; §6.2 in-flight tracking table had a "Retrospective backlog" row.

The user's instruction during cleanup-plan v1 review: "I also want to completely excise any reference to following up on retrospectives. That is an independent process that must not be in any plan documents."

The conceptual reasoning surfaces in why this entanglement was wrong: retrospectives capture lessons from completed work; plans capture intended future work. When lessons-as-tasks live in the plan, ownership becomes ambiguous — does the retrospective "own" the unbuilt skill spec, or does the plan? In practice both, which means neither. The "stale snapshot" pathology in §3.4 (17 newer retros not counted) is the inevitable symptom.

## Decision

Retrospective management is an independent process; plan documents (`research/PLAN.md`, `research-plan.md`, equivalents) do not reference retrospective backlogs, follow-ups, or pending retrospective decisions.

The self-retrospective skill produces its own artefacts (per-skill specs, per-rule agents files, ADR drafts) in `retrospective/<date>-<pr>/`. The user reviews them on their own cadence. Adoption of any individual artefact (instantiating a proposed skill, accepting a proposed ADR, adding a proposed AGENTS rule) is an independent action with its own track — not mediated through a plan-doc table.

## Alternatives considered

- **Track retrospective backlog in a separate plan doc (e.g., `retrospective/BACKLOG.md`).** Rejected: produces the same ambiguity at a different file path. The clean separation is "retrospectives produce artifacts; user decides what to adopt; no centralised backlog."
- **Keep a retrospective summary in PLAN.md but auto-regenerate it.** Rejected: any auto-regenerated content is a coupling between systems. The user's "must not be in any plan documents" was unambiguous.
- **Keep the legacy §3.4 entanglement but mark it "advisory only."** Rejected: doesn't solve the drift problem (which was already evident — the 5-retro snapshot was stale by 17 retros at session start).

## Consequences

**Easier:**
- PLAN.md becomes purely about research work — no cross-system entanglement.
- Retrospective artifacts have a single home (`retrospective/<date>-<pr>/` directories) and a single workflow (self-retrospective skill produces; user adopts ad-hoc).
- §3 / §5 / §6 of PLAN.md become shorter and more focused.

**Harder:**
- There is no single "what retrospective work is outstanding?" register. A user who wants to systematically work through retro artifacts has to ls `retrospective/` and inspect each. For now this is acceptable; if the volume grows, a separate retrospective-tracking tool is the right answer, not putting it back in PLAN.md.

**Trade-off accepted:** loss of centralised retrospective-backlog tracking in PLAN.md, in exchange for ending the cross-system drift pathology.

## References

- [`../2026-05-21-106.md`](../2026-05-21-106.md) — the source retrospective.
- [`./AGENTS-MD-d2e1803350-no-retro-refs-in-plan-docs.md`](./AGENTS-MD-d2e1803350-no-retro-refs-in-plan-docs.md) — the corresponding AGENTS.md rule.
- Pre-existing skill: `.claude/skills/self-retrospective/SKILL.md` (produces retro artifacts independently of any plan).
- PR the decision was made in: #106.
