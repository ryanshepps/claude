---
slug: postels-law
categories: [quality, design]
priority: 2
description: Be conservative in what you do, be liberal in what you accept from others.
applies_when:
  - designing APIs
  - handling user input
  - building interoperable systems
related: []
source: https://lawsofsoftwareengineering.com/laws/postels-law/
---

# Postel's Law

> Be conservative in what you do, be liberal in what you accept from others.

## Key Takeaways

- When your system emits data or interacts with the outside world, adhere closely to protocols and standards.
- When receiving data, handle variations, minor errors, or deviations where possible. Don't crash or reject communication over minor issues.
- In modern times, overly liberal acceptance can sometimes mask errors, so this law is occasionally tempered with security considerations.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/postels-law/)
