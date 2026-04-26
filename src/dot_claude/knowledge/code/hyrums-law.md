---
slug: hyrums-law
categories: [architecture]
priority: 1
description: With a sufficient number of API users, all observable behaviors of your system will be depended on by somebody.
applies_when:
  - changing a public API
  - deprecating legacy behavior
  - designing stable interfaces
related: []
source: https://lawsofsoftwareengineering.com/laws/hyrums-law/
---

# Hyrum's Law

> With a sufficient number of API users, all observable behaviors of your system will be depended on by somebody.

## Key Takeaways

- As the user count grows, everything your system does becomes a dependency point. Even unintended side effects or bugs can become 'features' that someone's workflow depends on.
- Hyrum's Law warns maintainers that any change can break something for someone. Consumers may have integrated your API in ways you didn't expect, including relying on timing, error messages, formatting, etc.
- The actual contract of your software isn't just the official API/spec; it's the exact behavior as observed in the wild. The contract can even be something informal, such as the UI that your users are used to.

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/hyrums-law/)
