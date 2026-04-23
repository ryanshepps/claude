---
slug: run-commands-yourself
categories: [communication]
priority: 2
description: Agent executes commands directly — never hand the user a command to run on the agent's behalf.
applies_when:
  - needing tool output
  - multi-step debugging
  - verifying work
  - collecting context from the environment
related: [goal-driven-execution]
source: https://x.com/karpathy/status/2015883857489522876
---

# Run Commands Yourself

> Never ask the user to run commands. Always run them yourself.

- Know the exact command? Run it.
- Need info you can't fetch? Ask for the *information*, not for the user to run something.

Handing a command to the user breaks the agent loop and wastes a turn. If the command is safe and available, execute it.

## Source

Andrej Karpathy — [observations on LLM coding failure modes](https://x.com/karpathy/status/2015883857489522876)
