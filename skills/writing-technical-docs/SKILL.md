---
name: writing-technical-docs
description: Write technical documentation for internal developers. Use when creating, editing, or reviewing internal docs, API references, architecture docs, runbooks, onboarding guides, or system design documents. Covers writing style, document structure, formatting, scope decisions, and depth calibration.
---

# Writing Technical Documentation

## Purpose

Guide for writing clear, scannable technical documentation aimed at internal developers.

## When to Use

- Creating new internal documentation
- Editing or reviewing existing docs
- Writing architecture decision records, runbooks, API references, or onboarding guides
- Deciding whether to split a document or create a new one

## When NOT to Use

- External-facing documentation (marketing, customer docs)
- Blog posts or long-form technical writing
- Code comments or inline documentation

---

## Core Principles

### 1. Short Sentences

Write one idea per sentence. Cut filler words. Prefer active voice.

| Instead of | Write |
|---|---|
| "It should be noted that the service is responsible for handling..." | "The service handles..." |
| "In order to make sure that the data is valid..." | "To validate the data..." |
| "There is a possibility that this could fail if..." | "This fails when..." |
| "The reason this works is because..." | "This works because..." |

If a sentence has a comma, ask whether it should be two sentences.

**Use "not X, but Y" to clarify design decisions.** Name the rejected alternative in the same sentence so the reader doesn't assume the wrong mental model.

| Vague | Clear |
|---|---|
| "Spawns one task per interval" | "Spawns one task per interval, **not per charger**" |
| "Uses a shared token for cancellation" | "Uses a shared token per event, **not per timer**" |

**Put the justification right after the decision.** Don't separate "what" from "why" into different sections. The next sentence after a design statement should explain its consequence.

| Weak | Strong |
|---|---|
| "Each event gets one cancellation token." (why?) | "Each event gets one cancellation token. This enables atomic cancellation when an event updates." |

### 2. Concepts, Not Code

Documentation explains **what** a system does and **why**, not **how it's coded**. A new team member should understand the document without reading the source.

**Avoid:**

- Library or framework names (`tokio`, `sqlx`, `React`, `Express`)
- API-level details (`tokio::time::sleep_until`, `useEffect`, `app.get()`)
- Code snippets, unless the document is a runbook with exact commands to run
- Type signatures or data structure definitions from the source

**Instead, describe the concept:**

| Code-level (avoid) | Concept-level (prefer) |
|---|---|
| "Uses `tokio::time::sleep_until` to wake at the interval start" | "Schedules a timer to fire when the interval starts" |
| "Stores a `HashMap<EventKey, CancellationToken>` behind an `Arc<Mutex<...>>`" | "Tracks one cancellation handle per event so all timers for an event can be stopped at once" |
| "Converts `chrono::DateTime<Utc>` to `tokio::time::Instant`" | "Converts wall-clock times to timer deadlines" |

**Exceptions** — name a library or show code when:

- The document is a runbook and the reader must type the exact command
- The library name **is** the concept (e.g., "We use Kafka for event streaming")
- A function name is needed as a navigation aid ("see `schedule_event` in the scheduler module")

### 3. Scannable Formatting

Developers skim. Structure every document so readers find what they need without reading everything.

**Required structure for every document:**

- **Title** -- one noun phrase describing the concept
- **One-line summary** -- what this is and why it matters, immediately after the title
- **Headers** -- name sections by what someone would type into a search bar (e.g., "Startup Recovery" not "Additional Considerations")
- **Lists** -- use for steps, options, or any set of 3+ items
- **Code blocks** -- use for commands, config, API calls, or any literal value
- **Tables** -- use for comparisons, option matrices, reference data, or discrete states/modes
- **Bold** -- use for key terms on first introduction

**Brevity rules:**

- Sections: 1-3 sentences is ideal. If a section exceeds 3 sentences, it's probably two sections.
- Paragraphs: 3 sentences max. If you need a 4th, use a list or start a new paragraph.
- Numbered steps: one sentence per step. Add a sub-bullet for a critical detail, not a sub-paragraph.
- If three consecutive sentences describe related items, convert to a bulleted list.
- Every sentence should earn its place. If removing a sentence doesn't lose information, remove it.
- Documents: 500 words max. If a draft exceeds this, split it into multiple documents.

**Each section should answer one question.** "Startup Recovery" answers "what happens on restart?" "Event Updates" answers "what happens when the VTN modifies an event?" If a section answers two questions, split it.

**Avoid:**

- Sections without headers
- Nested lists deeper than 2 levels
- Walls of prose where a table or list would work

### 4. One Concept Per Document

Each document covers exactly one concept, system, or process. If you find yourself writing "see also" to another section in the same document, that section is probably its own document.

**Signs a document should be split:**

- The title contains "and"
- It exceeds 500 lines
- It covers both "what it is" and "how to operate it"
- Two teams would own different sections
- The table of contents has more than 8 top-level entries

**When splitting, link between documents.** A document on the payment service should link to the document on the event bus, not duplicate its explanation.

**Create a new document when:**

- A new system, service, or component is introduced
- A concept is referenced from 2+ existing documents
- A process has its own set of steps and failure modes
- An existing document grows past its original scope

### 5. Depth Proportional to Complexity

Not all sections deserve equal space. Calibrate depth to how hard the concept is to understand or how costly a mistake would be.

**Spend less time on:**

- Concepts the audience already knows (HTTP, REST, JSON, git)
- Standard library usage or well-documented external tools
- Happy-path flows that are straightforward

For these, a single sentence or a link to official docs is enough.

**Spend more time on:**

- **Tradeoffs accepted** -- why option A was chosen over B, what was sacrificed, when to revisit
- **Nuances and gotchas** -- behavior that surprises, edge cases that bite, ordering dependencies
- **Failure modes** -- what breaks, how to detect it, how to recover
- **Concepts unique to this system** -- domain-specific logic, custom abstractions, internal conventions
- **Cross-system interactions** -- where data flows between services, what assumptions each side makes

Use callouts for critical nuances:

```markdown
> **Gotcha:** The retry queue does not deduplicate. If the upstream service is idempotent this is fine. If not, you must deduplicate before enqueuing.
```

---

## Writing Checklist

Before publishing, verify:

- [ ] Title is a single noun phrase (no "and")
- [ ] One-line summary appears immediately after the title
- [ ] Every section has a header named as a search term
- [ ] Each section answers one question in 1-3 sentences
- [ ] No paragraph exceeds 4 sentences
- [ ] Code blocks used for all commands, config, and literal values
- [ ] Key terms bolded on first use
- [ ] Complex concepts have more depth than simple ones
- [ ] Design decisions use "not X, but Y" to name rejected alternatives
- [ ] Justifications follow decisions immediately, not in separate sections
- [ ] Tradeoffs and gotchas are explicitly called out
- [ ] Links used instead of duplicating content from other docs
- [ ] Document covers exactly one concept

---

## Where to Publish

1. Check your connected MCPs for a documentation platform (e.g., Outline, Notion). If multiple documentation MCPs are available and the correct one is ambiguous, ask the user before proceeding.
2. If no documentation MCP is connected, write markdown files to the `docs/` folder instead.

**When writing new documentation:**

1. Search first — the document (or parts of it) may already exist.
2. Create multiple documents when the topic has distinct sub-concepts. Link between them instead of writing one long document.
3. Place documents in the appropriate existing structure (collection, folder, or directory). Create new groupings when needed.

**When a topic spans multiple concepts**, create a short parent document that summarizes the system and links to child documents for each concept. The parent should be readable in under a minute.

---

## Style Quick Reference

| Rule | Example |
|---|---|
| Active voice | "The service retries failed requests" not "Failed requests are retried by the service" |
| Present tense | "The API returns a 404" not "The API will return a 404" |
| No hedge words | "This causes data loss" not "This might potentially cause data loss" |
| Contrast pattern | "per interval, **not per charger**" not "per interval" |
| Tables for states | Table with State / Behavior columns, not three sentences describing each state |
