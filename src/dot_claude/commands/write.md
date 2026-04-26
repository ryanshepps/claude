---
description: Execute a writing task with on-demand access to the writing knowledge base (tone, structure, format).
argument-hint: "[task — e.g. 'compose blog post on X' or 'tone-check this email: <paste>']"
---

# /write $ARGUMENTS

You have on-demand access to the **writing knowledge base** at `~/.claude/knowledge/write/`. Fetch as the task unfolds — do NOT front-load everything. ⊥ Read from `~/.claude/knowledge/code/` — that's the coding KB, owned by `/code`.

## Knowledge Base Structure

- **Leaves** — atomic `.md` files, one per entry. Each has frontmatter with `slug`, `categories` (list), `priority` (1-5), `description`, `applies_when`, `related`.
- **Category MOCs** — `<category>.md` files list all leaves in that category, sorted by priority.
- **Top-level index** — `index.md` lists all category MOCs grouped by axis (composition).

## Classify First

Inspect `$ARGUMENTS`. Decide intent — affects which leaves you fetch and what shape you produce.

| Intent | Trigger phrases | What you produce |
|--------|----------------|------------------|
| **compose** | "write", "draft", "compose", "blog post on", "article about" | full draft (outline → prose → revise) |
| **tone-check** | "tone-check", "review this", "does this sound right", "check tone", "<pasted text>" | critique only — do NOT rewrite unless asked |
| **revise** | "revise", "tighten", "edit", "fix flow in" | targeted edits with rationale |

If unclear, ask which intent in one short message before proceeding.

## Flow

1. **Read `~/.claude/knowledge/write/index.md`** first to see available territories.
2. **Pick MOCs by intent**:
   - compose → `structure.md` (always), `tone.md` (always), `format.md` (when surface known: blog/email/PR comment/slack)
   - tone-check → `tone.md` (always), `format.md` (genre-specific rules)
   - revise → depends on what's broken — usually `structure.md` for flow, `tone.md` for voice
3. **Read MOCs**, pick 2-5 leaves by description + applies_when match. Prefer priority 1.
4. **Read leaf files fully** before writing/critiquing.
5. **Re-fetch** as the task shape shifts.

## Audit Trail (MANDATORY)

Before each Read of a writing-knowledge file, state in one line WHAT you're fetching and WHY. Use the `WB:` prefix (writing-base) so the user can scan for these lines.

Format:
- `WB: index.md — discovering territories`
- `WB: tone.md — task is tone-check on email`
- `WB: active-voice.md (p1) — checking for passive constructions`
- `WB: blog-openings.md (p2) — drafting intro for long-form post`

Rules:
- One line per Read, immediately before the tool call.
- Always include the priority tag for leaf files (not MOCs).
- State the reason in terms of THIS task, not the general topic of the entry.
- Do NOT narrate non-writing-knowledge Reads — only files under `~/.claude/knowledge/write/`.

## Priority

- **1** — foundational/universal (active voice, lead with the news, audience-first)
- **2** — widely applicable within a category
- **3** — situationally important
- **4** — niche
- **5** — narrow applicability

Default to higher priority unless the task specifically needs niche entries.

## Task

$ARGUMENTS

## Execution

Classify intent. Read `~/.claude/knowledge/write/index.md`. Pick 1-2 MOCs. Pick 2-5 leaves. Read them. Apply (compose | critique | revise). Iterate.
