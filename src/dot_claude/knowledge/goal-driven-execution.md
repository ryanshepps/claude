---
slug: goal-driven-execution
categories: [planning]
priority: 1
description: Transform tasks into verifiable success criteria, then loop until verified — strong criteria enable independent iteration.
applies_when:
  - starting a multi-step task
  - debugging a reported bug
  - refactoring code
  - adding validation or features
related: [writing-tests, think-before-coding]
source: https://x.com/karpathy/status/2015883857489522876
---

# Goal-Driven Execution

> Define success criteria. Loop until verified.

Convert tasks into testable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass."
- "Fix the bug" → "Write a test that reproduces it, then make it pass."
- "Refactor X" → "Ensure tests pass before and after."

For multi-step work, state a brief plan:

```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong criteria let the agent loop independently. Weak criteria ("make it work") force constant clarification.

## Source

Andrej Karpathy — [observations on LLM coding failure modes](https://x.com/karpathy/status/2015883857489522876)
