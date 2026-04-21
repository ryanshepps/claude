---
name: technical-editor
description: Review and edit technical articles for clarity, conciseness, and professional tone. Removes fluff, improves logical flow, validates mental models, ensures direct enterprise-quality writing like Google, Anthropic, or Stripe documentation.
---

# Technical Editor

## Overview

Review technical articles with the rigor of a senior editor at a major tech company. Focus on three pillars:

1. **Conciseness** — Eliminate fluff; every word earns its place
2. **Clarity** — Validate mental models and logical flow from reader's perspective
3. **Tone** — Direct, literal, professional; no marketing speak

The goal: documentation that reads like it came from Google, Anthropic, or Stripe.

---

## Quick Start: The 5-Pass Review

1. **Structural Review** — Does the architecture work? (order, chunking, title-content match)
2. **Clarity Pass** — Can readers follow the logic? (mental models, transitions)
3. **Conciseness Pass** — Does every word earn its place? (filler, passive voice)
4. **Tone Pass** — Does this read professionally? (condescension, hedging, hype)
5. **Final Polish** — Sentence-level perfection (length, grammar, accuracy)

---

## Reference Files

For detailed guidance on specific areas:

### [ENTERPRISE_TONE.md](ENTERPRISE_TONE.md)
How large tech companies write documentation:
- Core principles (direct statements, imperative mood, precision)
- Words and phrases to avoid (condescending, filler, marketing)
- Voice and mood guidelines
- Examples from Google, Stripe, Anthropic

### [READER_CLARITY.md](READER_CLARITY.md)
Ensuring readers can follow your logic:
- Understanding mental models and cognitive load
- The outsider test (reading as a newcomer)
- Title-content alignment
- Logical flow patterns
- Information architecture
- Concept introduction (concrete before abstract)

### [EDITORIAL_TECHNIQUES.md](EDITORIAL_TECHNIQUES.md)
The craft of editing and providing feedback:
- Multi-pass review process (detailed)
- Conciseness techniques (filler phrases, nominalizations, passive voice)
- Sentence and paragraph-level editing
- Providing structured editorial feedback
- Before/after examples

---

## Quick Reference: Common Edits

| Pattern | Before | After |
|---------|--------|-------|
| Filler | "in order to" | "to" |
| Filler | "due to the fact that" | "because" |
| Filler | "it is important to note" | (delete) |
| Passive | "is read by the parser" | "the parser reads" |
| Nominalization | "perform an analysis" | "analyze" |
| Condescension | "simply", "just", "obviously" | (delete) |
| Hedging | "can potentially cause" | "causes" |
| Hype | "amazing", "powerful" | (delete or be specific) |

---

## Quick Reference: Checklist

**Structure**
- [ ] Title accurately reflects content
- [ ] Logical section order
- [ ] Clear hierarchy (scannable)

**Clarity**
- [ ] Prerequisites stated
- [ ] Concepts build progressively
- [ ] No undefined terms before definition

**Conciseness**
- [ ] No filler phrases
- [ ] Active voice dominant
- [ ] Every word earns its place

**Tone**
- [ ] Direct and literal
- [ ] No condescension
- [ ] No marketing speak

**Polish**
- [ ] Sentences under 25 words
- [ ] Paragraphs under 5 sentences
- [ ] Technical accuracy verified

---

## Editorial Feedback Format

When reviewing, use this structure:

```markdown
## Editorial Review: [Article Title]

### Summary
[1-2 sentence assessment]

### Priority Fixes
1. [Most impactful change]
2. [Second priority]
3. [Third priority]

### Detailed Edits
| Location | Original | Suggested | Reason |
|----------|----------|-----------|--------|
| ... | ... | ... | ... |

### Strengths
- [What works well]
```

See [EDITORIAL_TECHNIQUES.md](EDITORIAL_TECHNIQUES.md) for the complete feedback template.

---

## Example: Before and After

**Before (47 words):**
> In order to get started with the API, you'll first want to make sure that you have basically set up your development environment. It's important to note that the authentication process is actually quite simple—you just need to obtain an API key.

**After (17 words):**
> Set up your development environment before using the API. Authentication requires an API key.

**Reduction:** 64% fewer words. Same information.

---

## When to Use This Skill

Invoke `/technical-editor` when:
- Reviewing a draft technical article
- Editing documentation before publishing
- Providing feedback on technical writing
- Polishing blog posts, tutorials, or guides

---

## Related Files

- [ENTERPRISE_TONE.md](ENTERPRISE_TONE.md) — Tech company writing standards
- [READER_CLARITY.md](READER_CLARITY.md) — Mental models and logical flow
- [EDITORIAL_TECHNIQUES.md](EDITORIAL_TECHNIQUES.md) — Editing craft and feedback
