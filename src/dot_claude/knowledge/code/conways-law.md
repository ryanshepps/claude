---
slug: conways-law
categories: [teams, architecture]
priority: 1
description: Organizations design systems that mirror their own communication structure. Team topology predicts system topology.
applies_when:
  - designing service boundaries
  - splitting or merging teams
  - diagnosing cross-team integration friction
  - choosing between monolith and microservices
related: [brooks-law, dunbars-number, bus-factor]
source: https://lawsofsoftwareengineering.com/laws/conways-law/
---

# Conway's Law

> Organizations design systems that mirror their own communication structure.

## Key Takeaways

- The architecture of software systems often mirrors the organization's org chart or team structure.
- If your company is organized in silos, you might end up with siloed software modules that don't communicate well, reflecting those barriers.
- To achieve a desired software architecture (e.g., microservices), you might need to restructure teams accordingly, because teams build software aligned with their communication paths.
- When starting a project, realize that how you split teams or departments will likely lead to software boundaries at the same places.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/conways-law/)
