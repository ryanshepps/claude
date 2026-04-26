---
slug: premature-optimization
categories: [planning]
priority: 1
description: Premature optimization is the root of all evil.
applies_when:
  - deciding whether to optimize
  - profiling before refactoring
  - balancing performance against readability
related: []
source: https://lawsofsoftwareengineering.com/laws/premature-optimization/
---

# Premature Optimization (Knuth's Optimization Principle)

> Premature optimization is the root of all evil.

## Key Takeaways

- Most code doesn't run in performance-critical hotspots, so obsessing over micro-optimizations everywhere wastes time and makes code harder to read and maintain.
- According to Knuth, we should forget about small efficiencies about 97% of the time, and focus on clean design and correct functionality.
- Optimized code is often more complex or less readable. If done prematurely, you incur this cost even when it's unnecessary.
- Get it working correctly first, then make it fast, then make it pretty.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/premature-optimization/)
