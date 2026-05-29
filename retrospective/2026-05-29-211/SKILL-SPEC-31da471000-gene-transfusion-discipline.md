# Spec: `gene-transfusion-discipline`

- **ID**: SKILL-SPEC-31da471000
- **Source retrospective**: ../2026-05-29-211.md

## Intent

When a factory (or any AI agent) is asked to build a component the agent has not seen before, always identify the strongest available exemplar from public OSS or established research and brief the agent to transfuse from that exemplar rather than invent from scratch. Current-generation models port and adapt reliably; they invent unreliably. Reduces engineering risk on factory-built components by an order of magnitude. The exemplar's URL becomes the component's transfused_from attribution.

## Trigger

**Direct triggers**:
- User asks to build a new component / library / tool / pack.
- User asks "how would we build X?" where X is a known category.
- A planning conversation reaches "OK now we need to write the diagnosis agent / twin / judge harness / Healer".
- Slash-command style: `/transfuse <component-name>`.

**Proactive triggers**:
- An architecture proposal lists components that don't yet exist.
- A multi-component plan is about to be handed off to a factory or junior engineer.
- An "invent from scratch" prompt is being drafted for a subagent or downstream session.

**Negative triggers** (do NOT apply transfusion):
- The component is genuinely novel research (no exemplar exists in public domain).
- The component is small enough that transfusion overhead exceeds the build cost (<50 LOC).
- Licensing constraints prevent reading the exemplar.

## Inputs

- The name/category of the component to build (e.g., "Layer 4 diagnosis agent", "Anthropic API twin", "Bertrand-equilibrium A/B harness").
- The context the component will operate in (target language, integration substrate, downstream consumers).
- Optional: known constraints (license posture, deployment shape, performance contract).

## Outputs

- A short transfusion brief naming 1-3 candidate exemplars, ranked by fit.
- The exemplar's URL + repo locator.
- A one-paragraph description of what specifically to transfuse (the pattern, the interface, the algorithm).
- A note on license compatibility between exemplar and target use.
- A draft prompt fragment ready to drop into a build brief: "Reference X's implementation at <URL>; produce the equivalent for our context with adjustments Y, Z."

## Workflow

1. **Categorize the component.** Match the request to a recognized OSS category (event store, judge harness, twin, diagnosis agent, etc.).
2. **Identify candidate exemplars.** Use the v4 transfusion-source map (`architectures/v4/AI-CONTEXT.md` §9.1) for known categories. For unknown categories, search OSS via `mcp__github__search_repositories` or web search for the canonical implementation.
3. **Rank by fit.** Top exemplar should match: (a) the architectural shape, (b) the language/platform if relevant, (c) the maturity bar, (d) the license posture.
4. **Verify license compatibility.** Permissive (MIT, Apache 2.0, BSD) for OSS release; restrictive (Elastic, source-available) only for internal use.
5. **Identify what to transfuse.** Be specific: "the FSM lifecycle" vs "the file format" vs "the algorithm". One sentence.
6. **Write the brief.** Format: "Reference <name> at <URL>. Specifically transfuse <what>. Adapt for <our context> by <how>. License: <permissive/restrictive note>."
7. **Record attribution.** In the resulting component's metadata, add `transfused_from: <URL>`. Make this a checked field at code review time.

## Concrete examples

### Example 1: Layer 5 twin for Anthropic API

**Input**: "Build a digital twin of the Anthropic API for v4's Layer 5."

**Output**:
> Reference LocalStack's AWS twin pattern (`github.com/localstack/localstack`, Apache 2.0). Specifically transfuse: the SDK-fidelity testing approach — twins match what the public SDK can call, not internal service contracts. For Anthropic API, the SDK is `anthropic-python` and `anthropic-typescript`; the twin should accept the same shapes those clients emit and return matching response shapes. Adapt for our context by limiting initial coverage to messages.create + tool_use endpoints (the v4 critical path). License: clean (Apache 2.0 for transfusion, MIT for our work). transfused_from: github.com/localstack/localstack

### Example 2: Layer 4 diagnosis agent

**Input**: "Build the v4 Healer agent that reads CXDB trajectories, clusters failures, produces root-cause hypotheses, and writes fix-task beads."

**Output**:
> Reference two exemplars (this is a composite transfusion):
> 1. Tracker's `Diagnose`/`Audit`/`Doctor` programmatic APIs (`github.com/2389-research/tracker`, MIT). Transfuse: the JSON-serializable failure-report shape (structured payload, queryable, not unstructured logs).
> 2. Anthropic's Claude Code investigation patterns (observe in active sessions). Transfuse: the question-decomposition style — agent asks "what changed?", "what's similar?", "what's the smallest reproducer?" rather than monolithic root-cause prompts.
> Adapt for our context: outputs go to Gas City beads as type `fix_task`; queries go through CXDB HTTP API. License: clean (both MIT). transfused_from: github.com/2389-research/tracker + claude-code-investigation-pattern (Anthropic public)

## Anti-patterns

- **"Build a Healer agent."** (No exemplar named. Factory will invent unreliably.) → Always transfuse.
- **Transfusing whole code verbatim without adapting.** Transfusion = adapt the pattern, not paste the implementation. Adapter is part of the prompt.
- **Picking the most popular exemplar without checking fit.** Popularity ≠ fit. WireMock is popular for HTTP mocking but LocalStack is the better fit for behavioral service twins.
- **Skipping license verification.** If the exemplar is GPL or restrictive, transfusion could create downstream licensing issues. Always check.
- **Omitting `transfused_from` attribution.** Lose the trail and you lose accountability. This is principle 9 applied to factory-built components.

## Acceptance criteria

1. Every factory-built component the skill informs has a `transfused_from` field naming at least one URL.
2. The exemplar's license is recorded and verified compatible with the target use.
3. The brief specifies *what to transfuse* (the pattern, interface, algorithm), not just "look at X."
4. When the user reviews the resulting component, they can verify it matches the exemplar's shape (not just claims to).
5. When no exemplar exists, the skill says so explicitly and recommends the user revisit whether the component should be built at all vs. deferred.

## Files this skill creates / modifies

- `architectures/v4/AI-CONTEXT.md` §9.1 (transfusion source map) — periodically updated as new categories are encountered.
- Per-component build briefs — each component's spec gets a transfusion-source citation.
- Per-component metadata — each component's bead carries `transfused_from`.
