---
name: code
description: Fetch domain knowledge from the code knowledge base (laws, language rules, workflow guides) before starting non-trivial coding work. Use when implementing a new file/function/feature, refactoring, making a design or architecture decision, choosing a language idiom, writing tests, or addressing PR review comments. Skip for one-line edits, typo fixes, comment tweaks, pure file reads, or trivial exploration without changes. Auto-triggers on substantive coding tasks; the user can also invoke explicitly by saying "fetch knowledge" or "consult the KB".
---

# Code Knowledge

You have on-demand access to the **code knowledge base** at `~/.claude/knowledge/code/`. Fetch as the task unfolds — do NOT front-load everything. ⊥ Read from `~/.claude/knowledge/write/` — that's the writing KB, owned by the `write` skill.

## Trigger Discipline

Before fetching, confirm the work is substantive enough to pay the KB-traversal tax:

| Substantive — fetch | Trivial — skip |
|---------------------|----------------|
| New module, file, or function | Renaming a single variable |
| Refactor touching 3+ files | Fixing a typo or comment |
| Architecture / design decision | Removing dead imports |
| Choosing language idiom or pattern | Reverting a one-line change |
| Writing or restructuring tests | Updating a string literal |
| Responding to PR review comments | Pure code reading / answering "what does this do?" |
| Resolving a non-obvious bug | Re-running a command |

If the task is trivial, skip the fetch entirely. Do not narrate. Do not explain.

## Knowledge Base Structure

- **Leaves** — atomic `.md` files, one per entry. Each has frontmatter with `slug`, `categories` (list), `priority` (1-5), `description`, `applies_when`, `related`.
- **Category MOCs** — `<category>.md` files list all leaves in that category, sorted by priority.
- **Top-level index** — `index.md` lists all category MOCs grouped by axis (task / language / cross-cutting).

## Flow

1. **Read `~/.claude/knowledge/code/index.md`** first to see available territories.
2. **Classify the task** against categories:
   - Task-axis: `architecture`, `design`, `teams`, `planning`, `quality`, `scale`, `decisions`
   - Language-axis: `python`, `rust`, `java`, `elixir`, `frontend`
   - Cross-cutting: `testing`, `prs`, `style`, `communication`
3. **Read relevant category MOC files** — each lists leaves with description and priority tag.
4. **Pick 3-7 leaves** by description + applies_when match. Prefer priority 1 unless task needs niche entries.
5. **Read leaf files fully** before decisions. Follow `related:` fields when adjacent entries would strengthen the reasoning.
6. **Re-fetch as task shape shifts** — different subtasks need different entries. Knowledge is cheap to re-read.

## Audit Trail (MANDATORY)

Before each Read of a knowledge file, state in one line WHAT you're fetching and WHY. Use the exact `KB:` prefix so the user can scan for these lines.

Format:
- `KB: index.md — discovering territories`
- `KB: architecture.md — task involves service boundaries`
- `KB: conways-law.md (p1) — applying to team-vs-module split`
- `KB: writing-python.md (p1) — Python codebase`

Rules:
- One line per Read, immediately before the tool call.
- Always include the priority tag for leaf files (not MOCs).
- State the reason in terms of THIS task, not the general topic of the entry.
- Do NOT narrate non-knowledge Reads (source code, configs, etc.) — only files under `~/.claude/knowledge/code/`.

This audit trail lets the user pause you if the wrong knowledge is entering context.

## Priority

- **1** — foundational/universal (Conway, DRY, KISS, coding-style, chatting-with-user-about-code)
- **2** — widely applicable within a category
- **3** — situationally important
- **4** — niche
- **5** — narrow applicability

Default to higher priority unless the task specifically needs niche entries.

## Execution

Read `~/.claude/knowledge/code/index.md` first. Classify. Read 1-2 category MOCs. Pick 3-7 leaves. Read them. Apply. Iterate.
