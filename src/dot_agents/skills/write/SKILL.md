---
name: write
description: Execute a writing task with on-demand access to the writing knowledge base. Use for drafting, revising, tone-checking, tightening, or critiquing prose, emails, posts, docs, and messages.
---

# Write

You have on-demand access to the writing knowledge base at `~/.agents/knowledge/write/`.
Fetch as the task unfolds. Do not front-load the whole corpus. Do not read from
`~/.agents/knowledge/code/`; that is the coding KB, owned by the `code` skill.

## Classify First

Inspect the request and choose one intent:

| Intent | Trigger phrases | What you produce |
|--------|----------------|------------------|
| compose | "write", "draft", "compose", "blog post on", "article about" | Full draft: outline, prose, revision |
| tone-check | "tone-check", "review this", "does this sound right", "check tone", pasted text | Critique only unless rewrite is requested |
| revise | "revise", "tighten", "edit", "fix flow in" | Targeted edits with rationale |

If unclear, ask which intent in one short message before proceeding.

## Flow

1. Read `~/.agents/knowledge/write/index.md` first to see available territories.
2. Pick MOCs by intent:
   - compose: `structure.md` and `tone.md`; add `format.md` when the surface is known.
   - tone-check: `tone.md`; add `format.md` for genre-specific rules.
   - revise: usually `structure.md` for flow and `tone.md` for voice.
3. Read 1-2 relevant MOCs and pick 2-5 leaves by description and `applies_when`.
4. Read leaf files fully before drafting, critiquing, or revising.
5. Re-fetch as the task shape shifts.

## Knowledge Gaps (record misses)

If you traverse the KB for a substantive writing task and no leaf adequately covers it, record the gap so `knowledge-reflect` can later turn it into a new-leaf candidate:

```bash
python3 ~/.agents/scripts/kb_gap.py --domain write --note "<what was missing, one line>" --task "<short task context>"
```

Record a gap only for a genuine miss on substantive work — not when an adequate leaf exists, and not for trivial tasks. One line per distinct gap.

## Audit Trail

Before each read of a writing-knowledge file, state one line with the `WB:`
prefix explaining what you are fetching and why.

Examples:

- `WB: index.md - discovering writing territories`
- `WB: tone.md - task is tone-check on an email`
- `WB: active-voice.md (p1) - checking for passive constructions`

Only narrate reads under `~/.agents/knowledge/write/`.

