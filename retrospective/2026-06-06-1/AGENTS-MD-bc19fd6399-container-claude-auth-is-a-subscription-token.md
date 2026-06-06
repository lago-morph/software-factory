# agent instruction

**Container Claude auth is a subscription token, not an API key.** When packaging Claude agents in a container for a subscription user, authenticate with a `claude setup-token` OAuth token (`CLAUDE_CODE_OAUTH_TOKEN`); do not assume or require `ANTHROPIC_API_KEY`.

*Grounded in: the user is on Claude Max with no API key.*

# justification

The user clarified mid-session that they run on a Claude Max subscription and have no API key at all. A container that assumes `ANTHROPIC_API_KEY` would be unusable for them out of the box — they would have nothing to put in the variable, and the natural-but-wrong fix (telling them to "get an API key") imposes a separate paid plan on someone who already pays for Max. The correct path is a subscription OAuth token produced by `claude setup-token`, supplied to the container as `CLAUDE_CODE_OAUTH_TOKEN`. Baking this assumption into the package design (env var name, docs, entrypoint) is free at authoring time; getting it wrong means the user cannot authenticate the agents in the deliverable they asked for, defeating the whole package. Because subscription-only users are the default audience for a "bring up with `docker compose up --build` and only a Claude subscription" deliverable, the API-key assumption should be treated as the exception that must be justified, not the default.
