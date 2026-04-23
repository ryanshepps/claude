---
slug: simplicity-first
categories: [design, quality]
priority: 1
description: Write the minimum code that solves the asked problem — no speculative features, abstractions, flexibility, or defensive handling.
applies_when:
  - writing new code
  - reviewing AI-generated output
  - resisting over-engineering
  - deciding between solutions
related: [kiss-principle, yagni, coding-style, surgical-changes]
source: https://x.com/karpathy/status/2015883857489522876
---

# Simplicity First

> Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you wrote 200 lines and it could be 50, rewrite it.

Test: "Would a senior engineer call this overcomplicated?" If yes, simplify.

Karpathy-flavored KISS/YAGNI, tuned for LLM failure modes that default to speculative generality.

## Source

Andrej Karpathy — [observations on LLM coding failure modes](https://x.com/karpathy/status/2015883857489522876)
