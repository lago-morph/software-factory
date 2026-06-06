# agent instruction

**Carry decision substance in chat, not only in AskUserQuestion.** When you put a decision to the operator via `AskUserQuestion`, also state the choices and their trade-offs in plain prose in the same chat turn — never rely on the question UI alone to carry the substance. If the operator declines the question, proceed with the recommended default and surface the open decision inside the deliverable rather than re-asking.

*Grounded in: the operator's AskUserQuestion popup did not render — "the UI didn't show your explanation; tell me in plain language what the choices are".*

# justification

The `AskUserQuestion` popup failed to render for the operator this session: they replied "The user interface didn't show your explanation. Tell me in plain language what the choices are." The two flagged decisions (real-driver strategy, portfolio scope) were entirely inside the unrendered widget, so the operator was momentarily blocked on a question they couldn't see. The cost of the rule is one extra paragraph of prose per question; the cost of omitting it is a stalled turn and an operator who can't act. The asymmetry is stark — always duplicate the choice substance in chat text.
