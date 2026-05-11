# ADR NNNN: Title in Sentence Case

- **Status**: Proposed
- **Date**: YYYY-MM-DD

<!--
This is the canonical template. Copy it to docs/adr/NNNN-kebab-title.md and
fill in. Keep each section to one or two short paragraphs / a small list.

Compatible with the `lago-morph/agent-os/adr` convention:
  - H1 form: `# ADR NNNN: <title>`
  - Section order: Context, Decision, Alternatives considered,
    Consequences, References
  - Lowercase "considered" in the Alternatives heading.

This template's superset additions (over agent-os):
  - Optional Deciders field on the metadata line.
  - Optional Supersedes / Superseded by fields.
  - Explicit lifecycle states beyond Accepted.

Numbering:
  - Zero-pad to 4 digits.
  - Next number is max(existing) + 1.
  - Numbers are permanent; never reuse, even for abandoned proposals.

Naming:
  - Filename: NNNN-kebab-case-title.md
  - H1 heading: `# ADR NNNN: Title in Sentence Case`

Status states:
  Proposed | Accepted | Deprecated | Superseded by ADR-NNNN

Relative-link rule:
  - Internal references use relative paths.
  - External resources (papers, blog posts) use absolute URLs.
  - References supports DIRECT SUBSECTION LINKING — one bullet can
    carry multiple anchor links to the same target file, in the form
    shown in the References example below.

Run `python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/`
before committing. The script verifies every relative file path and
every anchor fragment.
-->

## Context

<!--
What is the issue we are seeing that motivates this decision? What
forces are at play (technical, organizational, security, cost)? Cite
research that informed it via relative links.

Keep this section evidence-driven; do not editorialize. One or two
short paragraphs.
-->

## Decision

<!--
What is the change we are making? State the chosen option in one sentence
at the top, then expand.

Be specific. "We will use X" beats "We considered using X and may use it".
-->

## Alternatives considered

<!--
For each meaningfully-considered alternative, one short paragraph: what
it is, why we did not pick it.

Skip this section only if there were no real alternatives (rare).
-->

## Consequences

<!--
What becomes easier? What becomes harder? What are we accepting as a
trade-off?

If relevant, include "what we are explicitly not promising" — the limits
of this decision's scope.
-->

## References

<!--
Relative links only for repo-internal content. Absolute URLs for external.

The agent-os style supports DIRECT SUBSECTION LINKING per bullet:
one bullet may name a target file once and then list multiple anchor
links to sections within it, comma-separated. Examples below illustrate
both single-link bullets and multi-link bullets. Replace these examples
with real references; the placeholders are wrapped in code blocks so the
link checker skips them.
-->

```
- [overview.md](../overview.md) [§5](../overview.md#5-foo), [§6.2](../overview.md#62-bar), [§9](../overview.md#9-baz)
- [ADR-NNNN: short title](./NNNN-kebab-title.md)
- [short label](../../path/to/source-file)
- [Author, "Title"](https://example.com)
```
