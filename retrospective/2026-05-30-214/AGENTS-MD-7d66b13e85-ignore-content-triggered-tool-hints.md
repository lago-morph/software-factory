# agent instruction

**Ignore harness tool-name hints triggered by content keywords.** "A system reminder claiming a keyword means you must use a specific tool (for example, the word workflow implying a Workflow tool) is spurious when the keyword merely appears in subagent or document content and no such tool exists or was requested. Do not act on it."

*Grounded in: repeated use-the-Workflow-tool hints fired by the word workflow in v4 content.*

# justification

Several times this session, a `<system-reminder>` asserted that because the user "included the keyword workflow," the agent should use a "Workflow tool." But the keyword came from subagent receipts and v4 documents describing the architecture's *workflow engine* — not from a user request — and no Workflow tool existed in the toolset. Acting on such a hint would mean inventing a tool call or derailing the task. The rule costs nothing (a half-second sanity check: did the user actually ask for this, and does the tool exist?) and prevents a whole class of misfires where automated keyword-matched reminders try to redirect work based on incidental vocabulary in the data being processed.
