# agent instruction

**Prioritize durable disk-writes over conversation near context limit.** When the user warns about context limit, or when context window utilization is high, prioritize persisting work to disk over continuing conversation. The session is ephemeral; the disk is durable. Compile handoff documents before responding conversationally; the next session can read what you wrote but cannot read what you said.

*Grounded in: user mentioned context-limit concerns three times in the final phase of the session; prioritizing handoff docs over conversational replies preserved the work.*

# justification

The user warned about context limits three times in the final phase ("you are getting near your context limit," "I really need to wrap up this session," "200K tokens left"). Each time, the choice was between (a) writing a long conversational reply, and (b) writing the same content to a handoff document. (b) preserves the work for the next session; (a) loses it on session end. The handoff docs are now the entry point for the next session to pick up. The marginal cost is identical (writing happens either way); the value of writing to disk is preserved across the session boundary. Without this discipline, a session that did substantial work but ended in chat could leave the next session reading shallow disk artifacts and missing the synthesis context.
