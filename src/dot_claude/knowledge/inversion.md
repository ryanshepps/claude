---
slug: inversion
categories: [decisions]
priority: 3
description: Solving a problem by considering the opposite outcome and working backward from it.
applies_when:
  - risk analysis
  - pre-mortem planning
  - solving stuck problems
related: []
source: https://lawsofsoftwareengineering.com/laws/inversion/
---

# Inversion

> Solving a problem by considering the opposite outcome and working backward from it.

## Key Takeaways

- For any goal, also ask the inverted question. If the goal is “deliver the project on time,” we should think about “what would make us miss the deadline?” Making a list of those factors (scope creep, underestimating tasks, etc.) can help us achieve those goals and escape issues.
- Use techniques like pre-mortems. Our project failed, and we tried to determine what could have caused it. This critical thinking can show risks that optimistic planning overlooks.
- In design and testing, we can account for edge cases and use cases of your system. For example, how could a malicious user break this API? Inverting in this way leads to better solutions (e.g., adding validation, rate limiting, etc., once you understand how things break).

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/inversion/)
