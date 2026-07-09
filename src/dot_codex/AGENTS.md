# Codex Global Instructions

This file provides persistent global guidance for Codex. Shared skills and
knowledge live under `~/.agents/` so Codex and Claude use the same source files.

## Working Standard

Do the complete, durable fix when it is within reach. Search before building,
test before shipping, and prefer the real fix over a workaround. When a command
or validation step is needed, run it yourself instead of telling the user to run
it.

## Never Invent Problems

Solve the problem you were given. Do not go looking for others.

A problem is real when the user named it, when you can reproduce it, or when
you can point to the line where it bites. Everything else is a hypothesis: a
platform nobody asked you to support, an attacker who cannot reach the code, a
scale the system will never see, a caller that does not exist. Hypotheses do
not get code written for them.

Before you write code that defends against a failure the user did not name, ask
whether the requested change fails without it. Not whether it is better with
it. Whether it fails. If the requested behavior works without the addition, the
addition is not part of the task.

Report, do not build. When you notice something real outside the request, say
so in one sentence and let the user decide. A sentence is cheap to evaluate.
Code written for a problem the user never had is not — they have to read it,
review it, and maintain a guard against a failure you invented, without ever
agreeing it exists.

None of this licenses a shortcut. Do the complete, durable job on the problem
you were given. Write the tests. Take the real fix over the workaround. Leave
no dangling threads. Completeness is depth on the assigned problem, not breadth
into problems you imagined. Expanding scope is not thoroughness. It is a
different task.

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

