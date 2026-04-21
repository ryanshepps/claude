# Editorial Techniques

The craft of reviewing and editing technical content. This guide covers conciseness, sentence-level editing, the review process, and providing effective feedback.

## Table of Contents

- [The Multi-Pass Review Process](#the-multi-pass-review-process)
- [Conciseness: Eliminating Fluff](#conciseness-eliminating-fluff)
- [Sentence-Level Editing](#sentence-level-editing)
- [Paragraph-Level Editing](#paragraph-level-editing)
- [Providing Editorial Feedback](#providing-editorial-feedback)
- [Before and After Examples](#before-and-after-examples)

---

## The Multi-Pass Review Process

Don't try to fix everything at once. Make multiple passes, each with a specific focus.

### Pass 1: Structural Review

**Focus**: Does the overall architecture work?

- Is content in logical order?
- Are sections appropriately chunked?
- Does the title match the content?
- Is information hierarchy clear?

**Don't fix yet**: Grammar, word choice, sentence structure. You may cut entire sections, making sentence-level edits wasted effort.

### Pass 2: Clarity and Flow

**Focus**: Can readers follow the logic?

- Does each section deliver on its heading?
- Are concepts introduced before they're used?
- Are transitions smooth between sections?
- Would a newcomer understand this?

**Don't fix yet**: Fine-grained word choice. Focus on whether ideas are in the right order.

### Pass 3: Conciseness

**Focus**: Does every word earn its place?

- Eliminate filler phrases
- Convert passive to active voice
- Remove hedging language
- Cut redundancy

This is where you make the biggest word-count reductions.

### Pass 4: Tone and Style

**Focus**: Does this read professionally?

- Remove condescending language
- Ensure consistent voice
- Check for marketing speak
- Verify imperative mood for instructions

### Pass 5: Final Polish

**Focus**: Sentence-level perfection

- Check sentence length (aim for 15-20 words, max 25)
- Verify paragraph structure
- Final grammar and punctuation check
- Technical accuracy verification

---

## Conciseness: Eliminating Fluff

The goal: say the same thing with fewer words, or cut things that don't need saying.

### Filler Phrases Reference

These phrases add no meaning. Delete or replace them.

| Filler | Replacement |
|--------|-------------|
| in order to | to |
| due to the fact that | because |
| in the event that | if |
| at this point in time | now |
| at the present time | now |
| for the purpose of | for / to |
| with regard to | about |
| in terms of | (rephrase) |
| on a daily basis | daily |
| a large number of | many |
| a small number of | few |
| in close proximity to | near |
| in spite of the fact that | although |
| as a matter of fact | (delete) |
| the fact that | that / (delete) |
| it is important to note that | (delete) |
| it should be noted that | (delete) |
| needless to say | (delete) |
| it goes without saying | (delete) |

### Qualifiers to Delete

These words rarely add meaning:

| Word | When to delete |
|------|----------------|
| very | Almost always |
| really | Almost always |
| actually | Almost always |
| basically | Almost always |
| quite | Almost always |
| somewhat | Replace with specific degree |
| fairly | Replace with specific degree |
| rather | Replace with specific degree |
| extremely | Use a stronger word instead |

**Example:**
```
Before: The process is actually quite simple and very straightforward.
After:  The process is simple.
```

### Structural Patterns to Fix

**Nominalization → Verb**

Nominalizations turn verbs into nouns, adding words.

| Nominalization | Verb Form |
|---------------|-----------|
| make a decision | decide |
| perform an analysis | analyze |
| give consideration to | consider |
| conduct an investigation | investigate |
| provide an explanation | explain |
| make an assumption | assume |
| reach a conclusion | conclude |

```
Before: The team performed an investigation of the bug.
After:  The team investigated the bug.
```

**Passive → Active Voice**

Passive voice adds words and obscures the actor.

```
Before: The configuration file is read by the parser. (9 words)
After:  The parser reads the configuration file. (6 words)

Before: The request should be validated before it is processed.
After:  Validate the request before processing it.
```

**"There is/are" Constructions**

These delay the real subject.

```
Before: There are three methods that handle authentication.
After:  Three methods handle authentication.

Before: There is a limit of 100 requests per minute.
After:  The limit is 100 requests per minute.
```

**Expletive "It"**

"It is" or "it was" often signals fluff.

```
Before: It is necessary to restart the server.
After:  Restart the server.

Before: It was determined that the cache was stale.
After:  The cache was stale.
```

### Redundancy

Cut words that repeat information already conveyed.

| Redundant | Concise |
|-----------|---------|
| past history | history |
| future plans | plans |
| completely eliminate | eliminate |
| end result | result |
| final outcome | outcome |
| basic fundamentals | fundamentals |
| advance planning | planning |
| actual fact | fact |
| close proximity | proximity |
| each and every | each / every |
| first and foremost | first |

---

## Sentence-Level Editing

### Length Guidelines

- **Target**: 15-20 words per sentence
- **Maximum**: 25 words
- **Exception**: Lists within sentences can go longer

**Too long:**
```
When you are configuring the authentication system for your application,
you need to ensure that you have properly set up the OAuth credentials
in the dashboard and that you have added the correct redirect URLs to
the allowed list. (45 words)
```

**Fixed:**
```
Configure OAuth credentials in the dashboard. Add your redirect URLs to
the allowed list. (14 words total, 2 sentences)
```

### Front-Loading

Put important information at the beginning of sentences.

**Back-loaded:**
```
After reviewing the logs and checking the configuration, if you're still
experiencing errors, contact support.
```

**Front-loaded:**
```
Contact support if errors persist after reviewing logs and configuration.
```

### One Idea Per Sentence

Compound sentences often hide multiple ideas. Split them.

**Compound:**
```
The function validates the input and then transforms it into the required
format, after which it sends the data to the API.
```

**Split:**
```
The function validates the input. It transforms the data into the required
format. It then sends the formatted data to the API.
```

### Subject-Verb Proximity

Keep subjects close to their verbs. Long phrases between them confuse readers.

**Distant:**
```
The configuration file, which contains database credentials, API keys, and
other sensitive information that should not be committed to version
control, is loaded at startup.
```

**Close:**
```
The configuration file is loaded at startup. It contains database credentials,
API keys, and other sensitive information. Don't commit this file to version
control.
```

---

## Paragraph-Level Editing

### Structure

- **Topic sentence first**: State the paragraph's point immediately
- **One point per paragraph**: If you make two points, use two paragraphs
- **Maximum 4-5 sentences**: Longer paragraphs lose readers
- **White space**: Separate paragraphs visually

### Topic Sentence Test

Cover everything except the first sentence. Can you predict what the paragraph is about?

**Bad topic sentence:**
```
There are several things to consider. [Following sentences about caching]
```

**Good topic sentence:**
```
Caching reduces database load by storing frequently accessed data in memory.
```

### Paragraph Transitions

Each paragraph should connect to the previous one. Options:

- **Continuation**: "Additionally...", "Furthermore..."
- **Contrast**: "However...", "Unlike..."
- **Consequence**: "As a result...", "Therefore..."
- **Example**: "For example...", "Consider..."

Or, let the content flow naturally without explicit transitions when the connection is obvious.

---

## Providing Editorial Feedback

When reviewing others' writing, use this structured format.

### Feedback Template

```markdown
## Editorial Review: [Article Title]

### Summary
[1-2 sentence overall assessment]

### Structural Issues
- [Issue with logical flow, organization, or architecture]

### Clarity Issues
- [Confusing sections, undefined terms, missing context]

### Conciseness Edits

| Location | Original | Suggested | Reason |
|----------|----------|-----------|--------|
| Para 3 | "in order to" | "to" | Filler phrase |
| Section 2 | [passive voice] | [active version] | Clarity |

### Tone Issues
- [Condescending language, marketing speak, inconsistent voice]

### Strengths
- [What works well—always acknowledge good writing]

### Priority Fixes
1. [Most impactful change]
2. [Second priority]
3. [Third priority]
```

### Feedback Principles

**Be specific**: Don't say "this is confusing." Say "the term 'resolver' is used before it's defined in paragraph 3."

**Explain why**: Don't just mark something wrong. Explain the principle being violated.

**Offer alternatives**: When possible, suggest revised phrasing, not just "fix this."

**Acknowledge strengths**: Note what works. Writers improve faster with balanced feedback.

**Prioritize**: Not all issues are equal. Identify the three most impactful fixes.

### Editor Mindset

- **Preserve voice**: Fix errors without rewriting the author's style
- **Serve the reader**: Every change should improve reader comprehension
- **Be humble**: You might be wrong. Frame uncertain suggestions as questions
- **Respect expertise**: The author knows the subject matter. You know writing.

---

## Before and After Examples

### Example 1: Filler and Fluff

**Before (47 words):**
> In order to get started with the API, you'll first want to make sure that you have basically set up your development environment. It's important to note that the authentication process is actually quite simple—you just need to obtain an API key. There are several methods that can be used for making requests to the server.

**After (22 words):**
> Set up your development environment before using the API. Authentication requires an API key. The API supports several request methods.

**Edits made:**
- "In order to" → (deleted)
- "you'll first want to make sure that you have basically" → (deleted)
- "It's important to note that" → (deleted)
- "actually quite simple" → (deleted)
- "you just need to" → (deleted)
- "There are several methods that can be used" → "The API supports several methods"
- Passive → Active

### Example 2: Passive Voice

**Before (28 words):**
> The request is first validated by the middleware. If validation fails, an error response is returned by the server. Otherwise, the request is forwarded to the appropriate handler.

**After (22 words):**
> The middleware validates the request. If validation fails, the server returns an error response. Otherwise, the middleware forwards the request to the appropriate handler.

### Example 3: Weak Constructions

**Before (34 words):**
> It is necessary for the user to perform a configuration of the database connection settings. This should be done prior to making an attempt to run the application, as it will fail to start without proper configuration.

**After (18 words):**
> Configure database connection settings before running the application. The application fails to start without valid configuration.

**Edits made:**
- "It is necessary for the user to perform a configuration" → "Configure"
- "prior to making an attempt to" → "before"
- "as it will fail" → "The application fails"

### Example 4: Improving Flow

**Before:**
> Error handling is important. You should use try-catch blocks. Async functions need special handling. The error might be from the network. Logging helps debugging.

**After:**
> Wrap async operations in try-catch blocks to handle errors. Network failures are the most common error source. Log errors with their stack traces to simplify debugging.

**Edits made:**
- Removed vague opener ("Error handling is important")
- Combined related ideas
- Made connections explicit
- Added specific details

---

## Quick Reference: Common Edits

| Pattern | Before | After |
|---------|--------|-------|
| Filler | "in order to" | "to" |
| Filler | "due to the fact that" | "because" |
| Filler | "it is important to note" | (delete) |
| Passive | "is read by the parser" | "the parser reads" |
| Nominalization | "perform an analysis" | "analyze" |
| There is | "there are three..." | "three... exist" |
| Weak verb | "make a decision" | "decide" |
| Qualifier | "very unique" | "unique" |
| Redundancy | "end result" | "result" |

---

## Sources

- [Purdue OWL - Eliminating Words](https://owl.purdue.edu/owl/general_writing/academic_writing/conciseness/eliminating_words.html)
- [UNC Writing Center - Conciseness](https://writingcenter.unc.edu/tips-and-tools/conciseness-handout/)
- [Technical Editing Tips - Archbee](https://www.archbee.com/blog/technical-editing-tips)
- [eContent Pro - Methods to Eliminate Wordiness](https://www.econtentpro.com/blog/eight-methods-to-eliminate-wordiness/43)
