# agent instruction

**Don't drive to decisions when the user is thinking aloud.** "When the user asks clarifying questions during exploration ('what would we lose?', 'is this substantially different?', 'what's the trade-off?'), answer the question and stop. Don't append AskUserQuestion decision blocks. Wait for an explicit 'make a decision', 'what should we do?', or 'pick one' before driving to a choice. Distinguish exploration from commitment by the verb form of the user's message."

*Grounded in: PR #218, the operator said "Can you stop fucking giving me these decision block things? They take up more than half the space I have to read your output. JUST STOP AND WAIT."*

# justification

This session repeatedly hit the same trap: the user would ask a clarifying question about Track A vs Track B (e.g., "do we lose anything with optimized?"), I would answer the question — and then immediately tack on an `AskUserQuestion` block trying to drive to a direction ("Now, given the answers above, which direction should the plan target?"). After three rounds the operator wrote, verbatim: "Can you stop fucking giving me these decision block things? They take up more than half the space I have to read your output. JUST STOP AND WAIT."

The cost asymmetry is severe. The marginal cost of restraint is zero — the conversation flows naturally when the agent answers and stops. The marginal cost of the decision-block-after-every-answer pattern is real: (a) the decision block consumes 30–80 lines of the operator's reading budget, (b) it forces the operator to either engage with a premature decision or explicitly defer, both of which interrupt their thinking, (c) repeated occurrences erode trust that the agent can read the conversation register.

The fix is a register-detection heuristic on the operator's message verb forms. Questions asking what we'd lose, how things compare, how something works, why we chose X — these are exploration. Questions asking what we should do, which option to pick, whether to proceed, when to start — these are commitment. The `AskUserQuestion` tool is for commitment conversations. In exploration mode, answer and wait.

The rule is robust against the obvious counter-case ("but sometimes the operator does want to be driven to a decision"). If they do, they'll say so, and the next message's verb form will tell you. Default to the cheaper failure mode (under-driving when over-driving was wanted) over the more expensive one (over-driving when exploration was wanted).
