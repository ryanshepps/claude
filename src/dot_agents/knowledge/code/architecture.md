---
description: Laws governing system structure, coupling, service boundaries.
type: moc
---

# Architecture

How components couple, where boundaries fall, and why organizational shape leaks into design. Reach for these when scoping services, drawing boundaries, or diagnosing coupling.

## Entries (by priority)

- [[architect-before-agent]] (p1) — Design module boundaries, data ownership, and concurrency invariants before writing code — implementation cannot invent coherent architecture.
- [[conways-law]] (p1) — Organizations design systems that mirror their own communication structure. Team topology predicts system topology.
- [[galls-law]] (p1) — A complex system that works is invariably found to have evolved from a simple system that worked.
- [[hyrums-law]] (p1) — With a sufficient number of API users, all observable behaviors of your system will be depended on by somebody.
- [[solid-principles]] (p1) — Five main guidelines that enhance software design, making code more maintainable and scalable.
- [[designing-testable-cpp-robotics]] (p2) — Design C++ and ROS 2 components with explicit seams, deterministic lifetimes, and pure decision logic so correctness can be verified without hardware.
- [[fallacies-of-distributed-computing]] (p2) — A set of eight false assumptions that new distributed system designers often make.
- [[hexagonal-architecture]] (p2) — Isolate domain logic from I/O by defining ports (interfaces the core needs) and adapters (implementations for DB, HTTP, queues).
- [[keep-test-paths-out-of-production-runtime]] (p2) — Keep test and local-only execution paths out of production runtime code; mock external systems at process or protocol boundaries instead.
- [[law-of-demeter]] (p2) — An object should only interact with its immediate friends, not strangers.
- [[law-of-leaky-abstractions]] (p2) — All non-trivial abstractions, to some degree, are leaky.
- [[resilience-patterns]] (p2) — Defensive patterns — circuit breaker, bulkhead, timeout, retry with backoff — that contain failures in distributed systems.
- [[sans-io]] (p2) — Separate pure logic from I/O — push computation into pure functions, let a thin shell own filesystem, network, time, and randomness.
- [[second-system-effect]] (p2) — Small, successful systems tend to be followed by overengineered, bloated replacements.
- [[teslers-law]] (p2) — Every application has an inherent amount of irreducible complexity that can only be shifted, not eliminated.
- [[c4-model]] (p3) — Four-level diagram hierarchy — Context, Container, Component, Code — for communicating software architecture at varying zoom levels.
- [[cap-theorem]] (p3) — A distributed system can guarantee only two of: consistency, availability, and partition tolerance.
- [[cqrs-event-sourcing]] (p3) — CQRS splits read and write models; event sourcing stores state as an append-only log of events. Powerful, expensive — use only when justified.
- [[law-of-unintended-consequences]] (p3) — Whenever you change a complex system, expect surprise.
- [[zawinskis-law]] (p3) — Every program attempts to expand until it can read mail.
