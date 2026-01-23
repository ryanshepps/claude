# Enterprise Tone Guide

How to write like Google, Anthropic, Stripe, and other top tech companies. Their documentation is direct, precise, and respects the reader's time.

## Table of Contents

- [Core Principles](#core-principles)
- [Words and Phrases to Avoid](#words-and-phrases-to-avoid)
- [Voice and Mood](#voice-and-mood)
- [Precision Over Hedging](#precision-over-hedging)
- [What Enterprise Docs Never Do](#what-enterprise-docs-never-do)
- [Examples from Top Companies](#examples-from-top-companies)

---

## Core Principles

### 1. Direct Statement of Facts

State what something does. Not what it "can" do, "might" do, or "helps" do.

```
Bad:  The API can return user data.
Good: The API returns user data.

Bad:  This feature helps improve performance.
Good: This feature reduces latency by 40%.

Bad:  You might want to consider using caching.
Good: Use caching for repeated queries.
```

### 2. Imperative Mood for Instructions

Tell the reader what to do. Don't suggest, recommend, or advise.

```
Bad:  You should run the migration script.
Good: Run the migration script.

Bad:  It's recommended to backup your data first.
Good: Back up your data first.

Bad:  You might want to check the logs.
Good: Check the logs.
```

### 3. Precision Over Vagueness

Use specific numbers, names, and details. Avoid "some", "various", "many", "significant".

```
Bad:  Performance improved significantly.
Good: Response time decreased from 200ms to 45ms.

Bad:  The function accepts various parameters.
Good: The function accepts three parameters: userId, options, and callback.

Bad:  This may cause some issues.
Good: This causes a memory leak when processing files larger than 2GB.
```

### 4. Confidence Without Arrogance

State facts directly. Let readers draw conclusions about difficulty or importance.

```
Bad:  This is an extremely powerful feature that you'll love.
Good: This feature enables batch processing of up to 10,000 records.

Bad:  The elegant solution we've developed...
Good: The solution uses a hash map for O(1) lookups.
```

---

## Words and Phrases to Avoid

### Condescending Language

| Avoid | Why | Alternative |
|-------|-----|-------------|
| Simply | Implies it's easy; frustrates readers who struggle | (delete) |
| Just | Dismissive of complexity | (delete) |
| Obviously | Condescending; if obvious, don't state it | (delete) |
| Of course | Same as above | (delete) |
| Clearly | Implies reader should already know | (delete) |
| As you know | Assumes knowledge reader may not have | (delete or explain) |
| Easy / Simple | Subjective; often wrong | (delete or be specific) |
| Quick | Subjective; time varies by reader | (delete or give actual time) |

### Filler and Hedging

| Avoid | Why | Alternative |
|-------|-----|-------------|
| Please note that | Filler; just state it | (delete) |
| It's important to note | Same as above | (delete) |
| As you can see | Reader can see | (delete) |
| It goes without saying | Then don't say it | (delete) |
| Basically | Filler | (delete) |
| Actually | Filler | (delete) |
| Really | Filler | (delete) |
| Very | Weak intensifier | (delete or use stronger word) |
| Quite | Filler | (delete) |
| Somewhat | Vague | (be specific) |

### Marketing Speak and Hype

| Avoid | Why | Alternative |
|-------|-----|-------------|
| Awesome | Hype; unprofessional | (delete) |
| Amazing | Same | (delete) |
| Incredible | Same | (delete) |
| Revolutionary | Same | (delete) |
| Cutting-edge | Same | (delete or be specific) |
| Best-in-class | Same | (cite benchmarks) |
| Powerful | Vague hype | (describe capability) |
| Robust | Often meaningless | (describe what makes it reliable) |
| Seamless | Marketing term | (describe the integration) |
| Leverage | Corporate jargon | use |

### Weak Constructions

| Avoid | Why | Alternative |
|-------|-----|-------------|
| We believe | Unnecessary hedging | (state directly) |
| We think | Same | (state directly) |
| In my opinion | Opinions are clear from context | (state directly) |
| Helps to | Weak | (state what it does) |
| Try to | Weak | (state the action) |
| Allows you to | Wordy | (state capability directly) |
| Enables you to | Same | (state capability directly) |
| Is able to | Same | can |
| In order to | Wordy | to |

---

## Voice and Mood

### Use Active Voice

The subject performs the action. Passive voice obscures who does what.

```
Passive: The file is read by the parser.
Active:  The parser reads the file.

Passive: Errors are logged to the console.
Active:  The system logs errors to the console.

Passive: The request should be sent to the server.
Active:  Send the request to the server.
```

### Use Present Tense

Describe what the software does, not what it will do.

```
Future: The function will return a promise.
Present: The function returns a promise.

Future: The server will respond with JSON.
Present: The server responds with JSON.
```

### Use Second Person for Instructions

Address the reader directly.

```
Third person: The user should configure the settings.
Second person: Configure the settings.

Third person: Developers can extend the base class.
Second person: Extend the base class to add functionality.
```

---

## Precision Over Hedging

### When Hedging is Appropriate

Hedge only when:
- Behavior genuinely varies (OS differences, configuration-dependent)
- You're documenting edge cases
- Making predictions about external systems

```
Appropriate: Response time varies based on network conditions.
Appropriate: On Windows, the path separator is backslash.
```

### When to Remove Hedging

Remove hedging when describing deterministic behavior:

```
Hedged:   The function can throw an error if the input is null.
Direct:   The function throws an error if the input is null.

Hedged:   This may cause a memory leak.
Direct:   This causes a memory leak.

Hedged:   You might see improved performance.
Direct:   Performance improves by 30%.
```

---

## What Enterprise Docs Never Do

### No Rhetorical Questions

State the answer directly.

```
Bad:  Want to improve your API's performance? Try caching!
Good: Caching improves API performance.

Bad:  What if you need to process multiple files?
Good: To process multiple files, use batch mode.
```

### No Exclamation Points

They undermine authority and read as marketing.

```
Bad:  This feature is now available!
Good: This feature is now available.

Bad:  You've successfully configured the server!
Good: The server is configured.
```

### No Emoji

Unless documenting emoji functionality or explicitly matching brand voice.

```
Bad:  Great job! You've completed setup! 🎉
Good: Setup is complete.
```

### No First-Person Plural ("We")

Avoid "we" when it's unclear who "we" refers to.

```
Bad:  We recommend using version 2.0.
Good: Use version 2.0.

Bad:  We've improved the API.
Good: The API now supports batch requests.
```

Exception: "We" is acceptable in blog posts or release notes where the company is clearly speaking.

---

## Examples from Top Companies

### Google Style

From the Google Cloud documentation:

> "Cloud Storage stores objects in buckets. Objects are immutable. To modify an object, you must replace it with a new version."

**Why it works:**
- Active voice
- Present tense
- No hedging
- Direct statements

### Stripe Style

From Stripe API docs:

> "Create a PaymentIntent to start a payment. The PaymentIntent tracks the customer's payment lifecycle."

**Why it works:**
- Imperative mood for instructions
- Present tense for descriptions
- No filler words
- Clear cause-and-effect

### Anthropic Style

From Claude documentation:

> "Claude processes your prompt and generates a response. The response includes the generated text and usage metadata."

**Why it works:**
- Subject-verb-object structure
- Specific about what's returned
- No marketing language
- Factual tone

---

## Quick Checklist

Before publishing, verify:

- [ ] No condescending words (simply, just, obviously, easy)
- [ ] No filler phrases (please note, it's important to, as you can see)
- [ ] No marketing speak (amazing, powerful, seamless)
- [ ] Active voice throughout
- [ ] Present tense for descriptions
- [ ] Imperative mood for instructions
- [ ] Specific numbers instead of "various" or "significant"
- [ ] No exclamation points
- [ ] No rhetorical questions
- [ ] No unnecessary "we" statements

---

## Sources

- [Google Developer Documentation Style Guide - Voice and Tone](https://developers.google.com/style/tone)
- [Stripe Documentation](https://stripe.com/docs)
- [Apple Human Interface Guidelines - Writing](https://developer.apple.com/design/human-interface-guidelines/writing)
- [Microsoft Writing Style Guide](https://docs.microsoft.com/en-us/style-guide/)
