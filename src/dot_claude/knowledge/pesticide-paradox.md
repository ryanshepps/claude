---
slug: pesticide-paradox
categories: [quality]
priority: 3
description: Repeatedly running the same tests becomes less effective over time.
applies_when:
  - maintaining a test suite
  - keeping tests effective over time
  - preventing test rot
related: []
source: https://lawsofsoftwareengineering.com/laws/pesticide-paradox/
---

# Pesticide Paradox

> Repeatedly running the same tests becomes less effective over time.

## Key Takeaways

- Over time, an outdated test suite will identify fewer bugs. The tests are still helpful, but no longer effective at detecting new defects.
- This paradox illustrates the need to infuse new test data continuously. It is essential for testers not to become complacent with their test scripts, thinking that these alone will be sufficient in the future.
- By periodically creating new tests (by altering existing ones), you effectively “refresh the pesticide,” thereby providing an opportunity to catch new bugs. This involves extending tests for new functionality, trying new input combinations, or perhaps just investigating new boundary cases.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/pesticide-paradox/)
