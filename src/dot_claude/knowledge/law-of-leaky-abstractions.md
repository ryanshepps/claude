---
slug: law-of-leaky-abstractions
categories: [architecture, design]
priority: 2
description: All non-trivial abstractions, to some degree, are leaky.
applies_when:
  - choosing an abstraction layer
  - debugging across library boundaries
  - evaluating framework tradeoffs
related: []
source: https://lawsofsoftwareengineering.com/laws/law-of-leaky-abstractions/
---

# The Law of Leaky Abstractions

> All non-trivial abstractions, to some degree, are leaky.

## Key Takeaways

- No matter how well-designed, abstractions (libraries, frameworks, etc.) have edge cases that depend on internal details.
- Developers should understand that using a high-level tool doesn't absolve them from knowing what's happening underneath, at least at a basic level.
- "Leaky" means you might encounter performance issues, bugs, or behavior that force you to consider the underlying system (e.g., networking, OS) on which the abstraction sits.
- When creating abstractions, strive to minimize leakage and document the cases in which it might break.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/law-of-leaky-abstractions/)
