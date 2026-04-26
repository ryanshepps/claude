---
slug: lehmans-laws
categories: [quality, design]
priority: 3
description: Software that reflects the real world must evolve, and that evolution has predictable limits.
applies_when:
  - maintaining long-lived software
  - planning for system evolution
  - managing aging systems
related: []
source: https://lawsofsoftwareengineering.com/laws/lehmans-laws/
---

# Lehman's Laws of Software Evolution

> Software that reflects the real world must evolve, and that evolution has predictable limits.

## Key Takeaways

- The first law, Continuing Change, states that if a system isn't continuously updated to meet new needs, it becomes less satisfactory to use. In practice, this means that successful software is never truly “finished”; to remain useful, it undergoes ongoing enhancements (or else users abandon it for something that keeps up).
- Over time, changes accumulate, making the system more complex (Law 2). Unless developers invest in refactoring or restructuring (i.e., paying down technical debt), the system's internal complexity will increase, slowing further development.
- Even if users demand more, a development organization can only do so much in a given time. They can't exponentially accelerate delivery forever. Factors such as team knowledge (familiarity) and process overhead limit it.
- The perceived quality of the system will decline (perhaps due to rising user expectations, environmental changes, or the accumulation of minor issues).

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/lehmans-laws/)
