# agent instruction

**Validate Mermaid diagrams via MCP validator before shipping.** "Do not ship Mermaid diagrams in human-facing or AI-readable documents without validation via the Mermaid validator MCP tool. Validation catches syntax errors and ensures the diagram will render in the reader's environment. For large batches (≥10 diagrams), validate in parallel batches. When validator output overflows the context cap, use jq on the saved output file rather than retrying with smaller batches."

*Grounded in: v3 build-guide items 5-6 shipped 19 validated Mermaid diagrams (PRs #206, #207); v4 README ships 8 more validated diagrams. Zero rendering bugs in production.*

# justification

A broken Mermaid diagram in a published document is a silent failure — the reader sees a blank or error, not a useful diagram. Validation is cheap (one MCP call per diagram, parallelizable). The Mermaid validator output overflowing the context cap was the only friction; jq on saved files solved it (`jq -c '{title, valid}' <file>` extracts just the validity check). Zero rendering bugs across 30+ shipped diagrams in this session because validation was the default. Marginal cost of validation is seconds per diagram in parallel; cost of shipping a broken diagram is reader confusion plus a rework cycle.
