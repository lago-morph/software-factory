# agent instruction

**Validate Mermaid diagrams with a validator, not a grep for the diagram type.** "When a deliverable requires valid diagrams, verify each one renders by running it through a Mermaid validator — do not accept a grep that merely confirms the diagram-type keyword (`stateDiagram-v2`/`sequenceDiagram`) is present. A `;` inside a `stateDiagram-v2` transition label (and `/`, `--`, `:` in labels) silently breaks the parse while the type keyword still greps clean. If a validator tool is available, self-validate every diagram before returning."

*Grounded in: four Gas City diagrams were invalid despite passing the builders' type-presence self-check; only the validator caught them.*

# justification

The depth bar required valid Mermaid; builders self-attested by grepping for the diagram-type keyword, which passed while four diagrams were actually unparseable — semicolons in transition labels act as statement terminators, so the parser fails on the next token while the `stateDiagram-v2` line still matches the grep. A broken diagram renders as an error block in the deliverable a human then has to debug. One validator call per diagram (or a single fix-pass subagent) is cheap; a corpus of broken diagrams that "passed self-check" is a silent quality failure that propagates until someone opens the rendered view.
