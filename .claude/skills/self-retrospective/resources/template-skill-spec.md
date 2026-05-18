<!--
TEMPLATE: per-skill spec (one per suggested skill)
Path target: retrospective/<UTC_DATE>-<PR>/SKILL-SPEC-<hash>-<skill-id>.md
Hash: first 10 hex of sha256("<TITLE>\n\n<INTENT_PARAGRAPH>\n"); frozen on first write.
Filename order: TYPE-<hash>-<name>.md (do NOT use the legacy <name>-TYPE-<hash> order).
Word count target: 400–1200 words.
Quality bar: a fresh-context agent with only this file as a brief should be able to build the skill.
Substitute every <ANGLE_BRACKETED_TOKEN> before writing.
-->

# Spec: `<skill-id>`

- **ID**: SKILL-SPEC-<hash>
- **Source retrospective**: ../<retro-basename>.md

## Intent

<One paragraph: what problem the skill solves and why it earns its
place in the skill library. Ground in a real session moment.>

## Trigger

<When should this skill activate? Direct user phrases + proactive
triggers + negative triggers. Be specific.>

## Inputs

<What the skill receives at invocation: arguments, current workspace
state, environment variables, recent context.>

## Outputs

<What the skill produces: files, commits, comments, side effects.>

## Workflow

<Numbered steps. Each step is concrete enough to execute. No "consider
doing X" — say "do X" or "if condition, do X; else do Y".>

1. <step>
2. <step>
3. <step>

## Concrete examples

<At least TWO worked examples, end-to-end. Show input, intermediate
state, output. Use the session's actual material where possible —
real file paths, real commit messages, real error text.>

### Example 1: <name>

<worked example>

### Example 2: <name>

<worked example>

## Anti-patterns

<Specific things NOT to do, each traceable to a session moment.>

- **<anti-pattern>**. <why it fails — cite the moment.>

## Acceptance criteria

<3–5 testable properties.>

- [ ] <property>
- [ ] <property>
- [ ] <property>

## Files this skill creates / modifies

<Paths the skill writes to, with one-line description of each.>

- `<path>` — <description>
