---
slug: gustafsons-law
categories: [scale]
priority: 3
description: It is possible to achieve significant speedup in parallel processing by increasing the problem size.
applies_when:
  - scaling workloads with compute
  - designing parallel algorithms
  - sizing problems for clusters
related: []
source: https://lawsofsoftwareengineering.com/laws/gustafsons-law/
---

# Gustafson's Law

> It is possible to achieve significant speedup in parallel processing by increasing the problem size.

## Key Takeaways

- As computing resources grow, you can compute more problems in a given time, rather than solving the same issues faster.
- It opposes the pessimism of Amdahl's Law by assuming the size of the problem to be solved will increase proportionally with computing power, so that parallel processors remain busy.
- Practically, Gustafson’s Law promotes the use of more resources in computation to achieve more in terms of the scope of tasks, rather than obtaining diminishing returns.
- “The law,” it says, “teaches that software and algorithms should be designed to ‘scale out.’ That means that as available processor cores or machines increase, the amount of work that can be done can be scaled up accordingly.”

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/gustafsons-law/)
