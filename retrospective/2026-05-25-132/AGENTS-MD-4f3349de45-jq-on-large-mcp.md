# agent instruction

**Use `jq` on the saved tool-result file when MCP output exceeds the tool result cap.** Some MCP tool results (e.g., mermaid validators returning rendered SVG) exceed the tool result token cap. When this happens, the harness saves the full output to `/tmp/.../tool-results/<id>.txt` and gives you the path; use `jq` on the file to extract specific fields rather than trying to Read the full result. Don't abandon validation because output is large.

*Grounded in: mermaid validator returned 94K characters; used `jq` on the saved file to extract `.valid`.*

# justification

The mermaid validator MCP tool returned a response that exceeded the tool result token cap. The harness saved the full output to `/tmp/.../tool-results/<id>.txt` and surfaced an error message with the path. The naive response would have been "validation tool is unusable, ship the diagrams unvalidated." The right response is `jq '.valid, .diagramType' /path/to/file` — two tokens of output, full validation confirmed. The pattern generalizes: any MCP tool whose output exceeds the cap can be queried via `jq` on the saved file. Cost of the workaround: one Bash call. Cost of skipping validation: shipping broken diagrams the user has to debug visually.
