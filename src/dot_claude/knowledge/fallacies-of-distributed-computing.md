---
slug: fallacies-of-distributed-computing
categories: [architecture]
priority: 2
description: A set of eight false assumptions that new distributed system designers often make.
applies_when:
  - building networked services
  - designing for failure modes
  - evaluating distributed architectures
related: []
source: https://lawsofsoftwareengineering.com/laws/fallacies-of-distributed-computing/
---

# Fallacies of Distributed Computing

> A set of eight false assumptions that new distributed system designers often make.

## Key Takeaways

- Networks drop messages, introduce delays, have finite throughput, and can be insecure. Properly built distributed systems must account for these with retries, timeouts, security measures, and dynamic discovery.
- The fallacies often manifest in subtle bugs. Assuming latency is zero might lead to chatty remote calls that work fine locally but become painfully slow over a network.
- Taking these fallacies into account leads to defensive design: using caches (bandwidth/latency aren't perfect), building redundancy (networks aren't reliable), and handling dynamic membership (topology changes).

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/fallacies-of-distributed-computing/)
