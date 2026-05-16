# Spec: `check-skills-before-adding-conventions`

## Intent

Before writing a new top-level convention file (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.) or adding a new repo-wide rule, grep `.claude/skills/` for the rule's keywords. If an existing skill already encodes the rule, prefer strengthening that skill's frontmatter description (so it actually triggers) over duplicating the rule in a parallel location. This earns its place because in this session I wrote a fresh `AGENTS.md` with two rules — "PRs default to ready-for-review" and "always subscribe to PR events" — only for the user to point out: "Maybe it is already in one of the skill files, and it isn't getting triggered?" A grep showed the subscribe rule had been sitting in `.claude/skills/always-commit-skill-to-repo/SKILL.md` for the entire conversation. The right move was to strengthen the skill (broader trigger description + add the missing draft-default rule to its body) and delete the redundant `AGENTS.md`.

## Trigger

Activate when about to:

- Write or modify any of: `AGENTS.md`, `CLAUDE.md`, `AGENT.md`, `.cursorrules`, `.windsurfrules`, top-level `README.md` "for agents" section, or a similar convention file at the repo root.
- Add a "rule" or "convention" anywhere outside `.claude/skills/` — e.g., adding a new instruction to a plan document about "always do X when Y."
- Respond to user requests phrased as: "make sure you always X", "from now on do Y", "I want you to always Z".

Direct user phrases that should trigger:
- "Make sure you always..."
- "From now on, when X..."
- "Add a rule that..."
- "Set up a convention that..."

Negative trigger (skip):
- The rule is genuinely transient ("just for this PR, do X") — does not need a long-lived home.
- The user has explicitly named the file the rule should live in (e.g. "add this to `docs/coding-style.md`") — defer to user.

## Inputs

- The rule the user (or you) want to encode.
- The current contents of `.claude/skills/`.
- The current contents of any existing top-level convention files (`AGENTS.md`, etc.).

## Outputs

- A decision: which file owns this rule.
- Either an edit to an existing skill (preferred) or a justified new file.
- If a duplicate would have been created, no duplicate.

## Workflow

1. **Extract the rule's keywords.** From the user's framing or your own draft, list 2–5 keywords that would appear in any existing implementation of the rule. Example: for "PRs default to ready-for-review, always subscribe", keywords are `draft`, `subscribe`, `pull request`, `pr_activity`, `create_pull_request`.

2. **Grep the skills directory:**

   ```bash
   grep -rli "<keyword1>\|<keyword2>\|<keyword3>" .claude/skills/ 2>/dev/null
   ```

   Run on the full keyword list; capture every hit.

3. **For each hit, read the matching skill's frontmatter description AND the line of the match.** Decide one of:

   - **(a) Rule is already encoded.** The skill says exactly what the new rule would say. → Do NOT add a new file. If the skill's trigger description is too narrow (so it's not actually firing), strengthen the trigger description. If the rule has drifted from current practice, update the skill body. Done.
   - **(b) Rule is partially encoded.** The skill covers some aspect but misses the rule's specific point. → Add the missing piece to the same skill's body. Strengthen the trigger description if needed. Done.
   - **(c) Rule belongs to a different scope than any existing skill.** Genuinely new territory. → Then *and only then*, write the new top-level convention file or create a new skill.

4. **If a top-level convention file already exists** (e.g. `AGENTS.md`), and a skill would also encode the rule, prefer the skill. Top-level files are best reserved for short pointers ("see `.claude/skills/X` for git/PR discipline") rather than detailed rules.

5. **Check the trigger.** A skill that holds a rule but doesn't fire is worse than no skill at all — the rule looks encoded but isn't reaching you. After editing, re-read the frontmatter `description:` field and confirm: do its named triggers actually match the situations where this rule must fire? In this session, the subscribe rule was in `always-commit-skill-to-repo` but its description said "Triggers broadly on file operations" — not "before any `git` operation or GitHub MCP PR call." Strengthening the trigger language was the highest-leverage fix.

## Concrete examples

### Example 1 — subscribe rule already in a skill (this session)

User: "Can you also, please please please do something so that when you create a PR that you are finished with, you create a full one, NOT a draft one? And that you ALWAYS subscribe to PR events whenever you submit one?"

Initial wrong move: wrote `/AGENTS.md` with both rules.

Correction: user prompted "Maybe it is already in one of the skill files, and it isn't getting triggered?"

```bash
grep -rli "draft\|subscribe_pr_activity\|create.*pull.*request" .claude/skills/
```

Showed `.claude/skills/always-commit-skill-to-repo/SKILL.md` had the subscribe rule already on line 61. The draft-default rule was NOT in the skill — it was in the system prompt only.

Right outcome: strengthen `always-commit-skill-to-repo` frontmatter to name every git command + PR-MCP-tool as a mandatory trigger; add the non-draft-by-default rule to its body; delete `AGENTS.md`.

### Example 2 — genuinely new rule

Hypothetical: user says "from now on, every commit message in this repo must include a Jira ticket reference like `[FACT-123]`."

Grep `.claude/skills/`: no skill encodes this.

Skill `always-commit-skill-to-repo` is about persistence + PR mechanics, not commit-message format — different scope.

→ This is genuinely new. Options: create `.claude/skills/jira-commit-format/SKILL.md`, or add a small section to a project-specific style file. Skill probably wins because the rule is enforcement-style.

## Anti-patterns

- **Writing `AGENTS.md` reflexively when the user says "make sure you always X".** Reflex is wrong; grep first.
- **Strengthening a skill but not strengthening its trigger description.** If the rule is in the body but the frontmatter doesn't promise to trigger on the relevant situation, the rule will continue to not fire. Both need to be updated together.
- **Maintaining duplicate copies of the same rule.** If `AGENTS.md` says "subscribe to PRs" and `always-commit-skill-to-repo/SKILL.md` says "subscribe to PRs", one will drift. Pick one home; the other carries at most a pointer.
- **Letting "rule visible in chat" substitute for "rule encoded durably."** A rule mentioned by the user but not added to a skill or convention file does not survive the session.

## Acceptance criteria

1. Before any new convention file is created, `.claude/skills/` has been grepped for the rule's keywords.
2. If a relevant skill exists, the edit lands in that skill (body + frontmatter trigger) rather than a parallel file.
3. After editing, the skill's frontmatter description names the trigger conditions explicitly enough that the executing agent would invoke the skill at the right moments.
4. No duplicate rules across `.claude/skills/` and top-level convention files.

## Files this skill creates / modifies

- `.claude/skills/<existing-skill>/SKILL.md` — preferred outcome: edit, not create.
- `AGENTS.md` / `CLAUDE.md` — created only if no existing skill is in scope. Reserve for short pointers to skills rather than detailed rules.
