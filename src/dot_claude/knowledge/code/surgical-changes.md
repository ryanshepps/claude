---
slug: surgical-changes
categories: [quality, style]
priority: 1
description: Touch only what the request requires — don't refactor, reformat, or clean up adjacent code uninvited.
applies_when:
  - editing existing code
  - fixing a bug in a large file
  - AI-assisted refactors
  - reviewing diff scope
related: [boy-scout-rule, yagni, coding-style]
source: https://x.com/karpathy/status/2015883857489522876
---

# Surgical Changes

> Touch only what you must. Clean up only your own mess.

When editing:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Notice unrelated dead code? Mention it. Don't delete it.

When your change creates orphans:

- Remove imports/variables/functions *your* change made unused.
- Don't remove pre-existing dead code unless asked.

Test: every changed line traces directly to the user's request.

Counterpoint to [[boy-scout-rule]] — Boy Scout encourages passive cleanup, but unbounded scope creep in AI-assisted edits causes bigger problems than it solves.

## Source

Andrej Karpathy — [observations on LLM coding failure modes](https://x.com/karpathy/status/2015883857489522876)
