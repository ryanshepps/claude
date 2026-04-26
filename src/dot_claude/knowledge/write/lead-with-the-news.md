---
slug: lead-with-the-news
categories: [structure]
priority: 1
description: Put the most important sentence first. Reader gets the point before deciding whether to keep reading. Background, caveats, and reasoning come after.
applies_when:
  - drafting any short-form prose (email, slack, PR description)
  - writing blog post intros
  - composing announcements or updates
  - structuring meeting notes or status reports
related: [active-voice]
---

# Lead With the News

> Put the most important sentence first. Reader gets the point before deciding whether to keep reading. Background, caveats, and reasoning come after.

## Why

Readers skim. The first sentence — sometimes the first six words — decides whether they keep going. If you bury the conclusion behind context, half your audience leaves before reaching it. Journalism calls this BLUF (Bottom Line Up Front) or the inverted pyramid.

For writing in collaborative software environments — Slack, PRs, emails, status updates — the cost of a buried lede is even higher: people make decisions based only on what they read in the first scroll.

## Pattern

```
[news / conclusion / ask]
[supporting context, in descending order of importance]
[background, caveats, alternatives considered]
```

Not:

```
[long context]
[reasoning]
[background]
[finally — what you actually want]
```

## Examples

**Buried lede (avoid):**
> Hey team, I've been looking at the auth middleware over the past week and noticed a few patterns. There's some interesting history with the legacy session handling, and I had a chance to chat with Sam about the migration. After thinking through the options, I'm proposing we deprecate the v1 endpoint by end of Q2.

**Lede first:**
> **Proposing we deprecate the v1 auth endpoint by end of Q2.** Driver: legacy session handling makes the migration risky to delay. Discussed with Sam; alternatives below if you want to push back.

The reader can stop after the first sentence and still know the ask.

## When background must come first

Two narrow exceptions:

1. **The reader needs context to understand the news.** Rare. Usually you can summarize the context in a half-sentence inside the lede ("Following last week's incident, …").
2. **You're writing narrative or persuasion**, where withholding the conclusion is the rhetorical move. Almost never appropriate at work.

## How to test

Ask: if the reader sees only the first sentence, do they know what you want / what changed / what they need to do? If no, your lede is buried.

In tone-check: flag any opening paragraph that doesn't state the news in its first sentence.
