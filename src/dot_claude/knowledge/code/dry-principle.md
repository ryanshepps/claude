---
slug: dry-principle
categories: [design]
priority: 1
description: Every piece of knowledge must have a single, unambiguous, authoritative representation.
applies_when:
  - duplicated code spotted
  - refactoring similar logic
  - extracting shared abstractions
related: []
source: https://lawsofsoftwareengineering.com/laws/dry-principle/
---

# DRY (Don't Repeat Yourself)

> Every piece of knowledge must have a single, unambiguous, authoritative representation.

## Key Takeaways

- The DRY principle is about avoiding duplication of knowledge in code. If the same idea or logic is in multiple places, it's a signal to refactor.
- When requirements change, you should update logic in only one place. Repeated code increases the risk of inconsistencies and bugs (you might fix a bug in one copy and forget about the others).
- Be careful to apply DRY wisely. It’s about knowledge repetition, not just duplication. Sometimes two pieces of code look alike but do different jobs; merging them could over-complicate things.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/dry-principle/)
