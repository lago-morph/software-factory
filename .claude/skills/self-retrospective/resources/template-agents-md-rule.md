<!--
TEMPLATE: per-rule agents-file addition (one per proposed AGENTS.md rule)
Path target: retrospective/<UTC_DATE>-<PR>/AGENTS-MD-<hash>-<kebab-rule-name>.md
Hash: first 10 hex of sha256("<RULE_NAME>\n\n<AGENT_INSTRUCTION_BODY>\n"); frozen on first write.
       <RULE_NAME> is the human-readable rule name in sentence case (the kebab form goes in the filename).
       <AGENT_INSTRUCTION_BODY> is the verbatim text under the `# agent instruction` heading,
       trimmed of surrounding whitespace.
Filename order: TYPE-<hash>-<name>.md (uniform with SKILL-SPEC- and ADR-).

STRICT FORMAT — the body of this file is EXACTLY two H1 sections, in this order, nothing else:

    # agent instruction
    <verbatim rule text — what the CI/CD assembler will concatenate into AGENTS.md>

    # justification
    <persuasion text — why this rule earns its place; STRIPPED by the assembler>

DO NOT add metadata bullets (`**ID**`, `**Source retrospective**`) at the top of this file.
The ID is encoded in the filename. The strict two-section structure is what lets the
CI/CD assembler extract `# agent instruction` cleanly and discard everything under
`# justification`.

DO NOT add any other H1 headings (extra `# Section` blocks would confuse the assembler).
DO NOT add `##` sub-headings inside either section — keep each section as flowing
markdown body content (paragraphs, bullets, blockquotes are fine; `##` headers are not).
-->

# agent instruction

**<Rule name>.** <The rule, phrased as a do/don't statement, ready to
paste verbatim into AGENTS.md.>

*Grounded in: <one-phrase session-event reference>.*

# justification

<A persuasive paragraph or two. Name the specific session event.
Quantify the cost of not having the rule — "took 20 minutes to undo",
"produced two parallel mechanisms", "five fabrications propagated for
two passes before catching". State the marginal cost of adopting the
rule — "one extra grep at session start", "two tool calls". Make the
asymmetry vivid.>
