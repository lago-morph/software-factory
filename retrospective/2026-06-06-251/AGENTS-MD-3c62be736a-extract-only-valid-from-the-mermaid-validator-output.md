# agent instruction

**Extract only `.valid` from the mermaid validator output.** The `validate_and_render_mermaid_diagram` tool returns a payload with embedded SVG and PNG that can exceed the inline token limit; do not read its result inline. When it reports the output was saved to a file, run `jq '{valid, diagramType}'` on that file for the verdict instead.

*Grounded in: validating a single 6-node flowchart returned ~143k characters and overflowed the tool result.*

# justification

Validating one small (6-node) flowchart produced a ~143,000-character result because it embeds both a rendered SVG and a base64 PNG. Read inline, that blows the result budget and pollutes context for no benefit — all I needed was the boolean `valid`. The fix is a single `jq` call on the saved result file. One tool call versus a 143k-token dump: adopt the rule and never read a mermaid render inline.
