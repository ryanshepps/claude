---
slug: cap-theorem
categories: [architecture]
priority: 3
description: A distributed system can guarantee only two of: consistency, availability, and partition tolerance.
applies_when:
  - designing distributed systems
  - choosing database consistency model
  - evaluating partition tolerance
related: []
source: https://lawsofsoftwareengineering.com/laws/cap-theorem/
---

# CAP Theorem

> A distributed system can guarantee only two of: consistency, availability, and partition tolerance.

## Key Takeaways

- A distributed system can only guarantee two out of three things at once: Consistency, Availability, and Partition Tolerance. When the network is healthy you can have all three, but the moment a partition happens, you have to give one up.
- When a network split occurs, you face a choice: stay consistent (every node agrees, but some requests may fail) or stay available (every request gets an answer, but the data might be slightly out of date). You can't fully have both.
- Real databases pick a side. MongoDB leans toward consistency, blocking writes during a partition so all replicas stay in sync. Cassandra leans toward availability, keeping the lights on and serving queries even if replicas briefly disagree.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/cap-theorem/)
