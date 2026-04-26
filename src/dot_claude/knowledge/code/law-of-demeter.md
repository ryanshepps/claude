---
slug: law-of-demeter
categories: [design, architecture]
priority: 2
description: An object should only interact with its immediate friends, not strangers.
applies_when:
  - reducing object coupling
  - evaluating method call chains
  - refactoring fragile code
related: []
source: https://lawsofsoftwareengineering.com/laws/law-of-demeter/
---

# Law of Demeter

> An object should only interact with its immediate friends, not strangers.

## Key Takeaways

- An object should only call methods of: itself, its direct components, its function parameters, or objects it creates. It should not navigate through one object to reach another (“don’t talk to strangers”).
- If object A only calls B (its immediate friend) and doesn’t reach into B’s internals (like C), then changes to C or removal of C don’t affect A. Each class knows as little as possible about others, reducing the impact of changes
- It often leads to adding wrapper methods or delegations. While that might increase the number of methods, it results in cleaner interactions.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/law-of-demeter/)
