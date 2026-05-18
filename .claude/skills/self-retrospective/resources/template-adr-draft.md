<!--
TEMPLATE: ADR draft (full content)
Path target: retrospective/<UTC_DATE>-<PR>/ADR-<hash>-<kebab-title>.md
Hash: first 10 hex of sha256("<TITLE>\n\n<ONE_SENTENCE_DECISION>\n"); frozen on first write.
Filename order: TYPE-<hash>-<name>.md (do NOT use the legacy <name>-TYPE-<hash> order).
Word count target: 400–1000 words.
Quality bar: a fresh-context agent reading only this draft should be able to either adopt it
            into docs/adr/ via the `adr` skill, OR challenge / supersede it.
Substitute every <ANGLE_BRACKETED_TOKEN> before writing.
-->

# ADR: <Title in Sentence Case>

- **ID**: ADR-<hash>
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: <UTC_DATE>
- **Source retrospective**: ../<retro-basename>.md
- **PRs covered**: #<N>, #<M>

## Context

<What is the issue that motivated this decision? Be evidence-driven.
Cite the session moment, the bug, the workaround, the spec
contradiction — whatever made this a binding architectural call rather
than a tactical implementation choice. One or two short paragraphs.>

## Decision

<The chosen option in one sentence at the top. Expand below if needed.>

## Alternatives considered

<For each meaningfully-considered alternative: what it is, why it was
rejected. At least one alternative — if none, justify briefly.>

- **<alternative>** — <why rejected>.
- **<alternative>** — <why rejected>.

## Consequences

<What becomes easier, what becomes harder, what trade-off we accept.>

## References

<Relative links to the source retrospective and the relevant skill specs
in the sibling directory. Absolute URLs only for external sources.>

- [`../<retro-basename>.md`](../<retro-basename>.md) — the source retrospective.
- [`./SKILL-SPEC-<hash>-<skill-id>.md`](./SKILL-SPEC-<hash>-<skill-id>.md) — related skill spec(s).
- PRs the decision was made in: #<N>, #<M>.

<!--
PROMOTION NOTE:
When this draft is adopted into docs/adr/ via the `adr` skill, preserve
the `**ID**: ADR-<hash>` line verbatim. The NNNN number in the
docs/adr/ filename is a separate human-friendly sequence; the hash is
the durable identifier and must not drift.
-->
