# Spec: `dual-artifact-docs`

- **ID**: SKILL-SPEC-2a120d3e3d
- **Source retrospective**: ../2026-05-29-211.md

## Intent

For any architectural proposal substantial enough to be load-bearing for multiple downstream sessions, produce two paired documents: a human-facing approach document (narrative, diagrams, conversational tone, conventions from human-scoped-deliverables) AND a dense AI-readable context document (structured sections, navigable, decision history, all alternatives considered, all license caveats, all specific config skeletons). The human doc gets read; the AI doc gets pickup by future agents. Single-artifact docs serve neither audience well.

## Trigger

**Direct triggers**:
- "Write up the v4 architecture / the new auth design / the platform proposal."
- "Document this decision."
- User asks for a "complete writeup" or "definitive document" of an architectural choice.
- Slash-command: `/dual-docs <topic>`.

**Proactive triggers**:
- A proposal is being drafted that will be load-bearing for multiple PRs or sessions.
- A decision is being captured that involves multiple alternatives + license considerations + specific config.
- The output is going to be read by both a human reader and downstream AI agents.

**Negative triggers**:
- The proposal is tactical (single component, single session).
- The intended audience is only humans (e.g., a blog post).
- The intended audience is only AI (e.g., a runtime context file with no human reader).

## Inputs

- The topic / scope of the architectural proposal.
- The target directory (e.g., `architectures/v4/`).
- Optional: existing notes, prior conversations, related artifacts to incorporate.

## Outputs

Two paired documents in the same directory:

1. **`README.md`** (human-facing):
   - Top orientation block (~50 words, per human-scoped-deliverables convention).
   - Narrative structure (Part 1, Part 2, ...).
   - Mermaid diagrams (≤7 elements per diagram).
   - Conversational tone, "we propose to..." rather than "the proposal is...".
   - Honest acknowledgements section.
   - "How to start tomorrow" or similar actionable closing.

2. **`AI-CONTEXT.md`** (AI-readable):
   - Numbered hierarchical sections (1, 2, 3, ..., 1.1, 1.2, ...).
   - All decisions made + deferred + rejected, each with rationale.
   - License caveats per OSS component.
   - Specific config skeletons (pack.toml, env vars, etc.).
   - Risk register with likelihood/impact/mitigation.
   - URLs and references section.
   - Pickup instructions for the next agent ("If you're working on X, read sections Y and Z").

## Workflow

1. **Identify the topic and scope.** Confirm the proposal is load-bearing enough to warrant dual artifacts.
2. **Draft the README first.** This is the human-facing narrative. Use diagrams sparingly (≤7 elements each, multiple small > one large).
3. **Use the human-scoped-deliverables skill conventions.** Plain language, corpus vocabulary, descriptive effort scoping (no engineer-weeks), honest disclosure, lead with the idea.
4. **Write the AI-CONTEXT in parallel or after.** Extract every decision, every alternative considered, every license caveat, every specific config detail. Structure as numbered sections.
5. **Cross-reference between the two.** README points at AI-CONTEXT for detail; AI-CONTEXT points at README for narrative.
6. **Sync findings between them.** A new finding (e.g., from a research subagent) gets added to both, in appropriate form.
7. **Place both in the same directory.** Reader discovers them together.
8. **Commit + PR.** The PR description should mention both artifacts.

## Concrete examples

### Example 1: v4 architecture proposal (the canonical case)

**Input**: Topic = "v4 architecture: principles before methodology", target dir = `architectures/v4/`

**Output**:

- **`architectures/v4/README.md`** (~5600 words, 8 Mermaid diagrams):
  - Part 1: hypothesis and why it changes everything
  - Part 2: how v4 differs from v3
  - Part 3: convergent shape recap
  - Part 4: the 12 principles, decomposed (with tables: components × what each does × OSS source × license × Gas City placement)
  - Part 5: license hygiene table
  - Part 6: 4-phase implementation plan
  - Part 7: self-bootstrap mechanic
  - Part 8: risks
  - Part 9: how to start tomorrow

- **`architectures/v4/AI-CONTEXT.md`** (~5100 words, 16 sections):
  - §0: pivot summary
  - §1: 12 working principles
  - §2: convergent shape
  - §3: Gas City load-bearing (subsections 3.1-3.6)
  - §4: Claude Code under Max (4.1-4.4)
  - §5: CXDB (5.1-5.5)
  - §6: integrated runner survey (6.1-6.5)
  - §7: per-capability OSS landscape
  - §8: multi-capability projects
  - §9: gene transfusion technique
  - §10: license caveats
  - §11: decision history (11.1-11.3: made, deferred, rejected)
  - §12: open technical questions
  - §13: specific config skeletons (13.1-13.3)
  - §14: risk register
  - §15: URLs and references (15.1-15.3)
  - §16: for the agent picking up v4 cold

### Example 2: a smaller architecture decision

**Input**: Topic = "Choose Postgres vs SQLite for the dev environment", target dir = `docs/decisions/dev-env/`

**Output**:
- `README.md`: ~500 words. The decision, the rationale, what changes for developers, how to migrate. One small diagram of the dev stack.
- `AI-CONTEXT.md`: ~800 words. Both options' pros/cons table, performance benchmarks consulted, license clean, migration script reference, what happens if we reverse the decision.

For small decisions like this, the AI-CONTEXT can be lighter — but it should still exist if the decision is binding.

## Anti-patterns

- **One giant document trying to serve both audiences.** The human doc gets too dense; the AI doc gets too narrative. Neither gets read well.
- **AI-CONTEXT as a verbatim copy of the human doc.** Defeats the purpose. The AI-CONTEXT should be structurally different — more navigable, more dense, no narrative.
- **Human doc with full license tables and config skeletons.** That detail belongs in AI-CONTEXT. Human doc cites it.
- **Drift between the two over time.** When updating one, update the other. Either both or neither.
- **Skipping AI-CONTEXT because "the README is enough".** When a future AI agent picks up cold, the AI-CONTEXT is what saves them. README narrative is hard to navigate from a cold start.
- **Burying the decision history in commit messages.** Decision history belongs in AI-CONTEXT §11, not in `git log`.

## Acceptance criteria

1. README is readable by a human in one sitting; AI-CONTEXT is navigable for a cold pickup.
2. Every decision in AI-CONTEXT §11 has a rationale.
3. Every OSS component referenced has a license note.
4. README has at least one Mermaid diagram per major section; diagrams are ≤7 elements each.
5. The two documents are cross-referenced at appropriate points.
6. Both ship in the same directory in the same commit.

## Files this skill creates / modifies

- `<target-dir>/README.md` — human-facing approach document.
- `<target-dir>/AI-CONTEXT.md` — dense AI-readable context document.
