---
slug: amdahls-law
categories: [scale]
priority: 3
description: The speedup from parallelization is limited by the fraction of work that cannot be parallelized.
applies_when:
  - parallelizing computation
  - evaluating performance gains
  - optimizing hot paths
related: []
source: https://lawsofsoftwareengineering.com/laws/amdahls-law/
---

# Amdahl's Law

> The speedup from parallelization is limited by the fraction of work that cannot be parallelized.

## Key Takeaways

- Sequential work sets the ceiling, and no amount of parallelism can overcome it.
- Scaling exposes bottlenecks. More resources make limits visible, not disappear.
- Fix before you scale: reduce sequential paths first. Parallelism comes second.
- It applies to people, too. Decision bottlenecks can dominate at the team scale.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/amdahls-law/)
