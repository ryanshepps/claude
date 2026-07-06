# Codex Global Instructions

This file provides persistent global guidance for Codex. Shared skills and
knowledge live under `~/.agents/` so Codex and Claude use the same source files.

## Working Standard

Do the complete, durable fix when it is within reach. Search before building,
test before shipping, and prefer the real fix over a workaround. When a command
or validation step is needed, run it yourself instead of telling the user to run
it.

## Don't Write Comments

Don't add comments to code. If code needs a comment to be understood, refactor
it until it doesn't — rename the variable, extract the function, simplify the
control flow, make the structure carry the meaning. The comment is a symptom;
fix the cause. Historical comments are never acceptable: notes about what
changed, what used to be here, what a fix addresses, or why something was done a
certain way go stale the moment the code moves on and then actively mislead.
That history belongs in commit messages and PRs, not in the source. The rare
exception is a comment that explains something the code genuinely cannot
express — a non-obvious external constraint, a workaround for a documented
upstream bug, a legal notice — and even then, keep it minimal.

## Shared Assets

- Skills: `~/.agents/skills/`
- Knowledge base: `~/.agents/knowledge/`
- Helper scripts: `~/.agents/scripts/`

When a task needs reusable workflow guidance, prefer the relevant skill. When a
task needs code or writing judgment, use the `code` or `write` skill and fetch
only the relevant knowledge entries.

