# agent instruction

**Store invocation prompts and commands durably in the repo.** When a prompt, command, or input drives real work (a `gc bd create` task body, a subagent brief, a generation prompt), commit it to the repo as the durable source of truth — do not leave it only in chat, a subagent brief, or an ephemeral / un-synced store (e.g. a local bead store). If it was worth running, it is worth re-running and reviewing.

*Grounded in: the chunk-1 `gc bd create` prompt existing only in the ephemeral bead and the subagent brief until the operator asked where it was stored.*

# justification

The chunk-1 build prompt was the load-bearing input that made the prototype build its own TUI — and for most of the session it existed only in three non-durable places: the chat transcript, the subagent brief, and the bead itself (which lives in the prototype's local Dolt store that is explicitly never synced). When the operator asked "what was the gc bd create command used? where is it stored?" the honest answer was "nowhere durable." That is a silent data-loss risk: the artifact that defines how the next rung is built would vanish with the sandbox. The fix cost one small committed file (`tui/prompts/chunk-1-beads-browser.md`) and a link from the README. The asymmetry — a few lines committed versus losing the exact, re-runnable recipe for the factory's own work — is stark, and the rule scales to every future rung and every subagent-driven generation.
