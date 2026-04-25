---
description: Synthesize a new entry for the knowledge base, write it to knowledge/, and regenerate MOCs.
argument-hint: "[instruction — e.g. 'add rubber duck debugging as a guide' or 'add Postel's Law']"
---

# /add-knowledge $ARGUMENTS

You are adding a new entry to the flat knowledge base at `~/.claude/knowledge/`. Follow the schema exactly — every leaf must fit the agent's retrieval flow.

## Existing Schema (required)

```yaml
---
slug: <kebab-case-slug>              # must match filename stem
categories: [<cat1>, <cat2>]         # 1-3 from: architecture, design, teams, planning, quality, scale, decisions, python, rust, java, elixir, frontend, testing, prs, style, communication
priority: 1                          # 1=foundational, 5=niche
description: <one sentence>          # lead with heuristic, not history
applies_when:
  - <2-4 task-context phrases>
related: [<other-slugs>]             # optional; use `[]` if none
source: <url>                        # optional; include if external
---

# <Human-readable Title>

> <one-line restatement of description>

## Key Takeaways (or equivalent body)

- <bullet 1>
- <bullet 2>
- <bullet 3>

## Source

<attribution if external, else omit>
```

## Flow

1. **Read `~/.claude/knowledge/index.md`** to see existing categories and pattern.
2. **Inspect 2-3 adjacent existing leaves** in the likely category to match voice/density. Announce each Read: `Reading <file> — to match style of similar entries`.
3. **Synthesize the entry** from the instruction ($ARGUMENTS):
   - Choose `slug` (kebab-case). Confirm no collision: `ls ~/.claude/knowledge/<slug>.md` must fail.
   - Choose `categories` — 1-3 matching the actual use-case, not just topical similarity.
   - Assign `priority` — be honest. Default to 3 if unsure. Priority 1 = cited in most coding contexts.
   - Write `description` — one sentence, applicability-forward.
   - Write `applies_when` — 2-4 short phrases the agent can match against task descriptions.
   - Populate `related` — existing slugs that pair with this entry. Use `[]` if truly isolated.
4. **Show the draft** to the user before writing. Single message, code-fenced frontmatter + body preview.
5. **On approval, write** to `~/.claude/knowledge/<slug>.md`.
6. **Regenerate MOCs**: run `python3 ~/.claude/scripts/gen_mocs.py`. Report the output.
7. **Validate**: run `python3 ~/.claude/scripts/validate_kb.py`. If it reports errors, fix the new file and revalidate.
8. **Report** the final file path, which MOCs now include it, and any warnings.

## Rules

- Never overwrite an existing file silently. If `<slug>.md` exists, stop and ask the user whether to update, rename, or abort.
- Never skip validation. The regen + validate pair is what keeps the corpus coherent.
- Never invent categories. The 16 existing categories are the only valid values. If the instruction genuinely doesn't fit any, stop and ask the user whether to add a new category (which requires updating `CATEGORY_META` in `~/.claude/scripts/gen_mocs.py` and validator).
- Match existing density. Leaves are typically 150-300 words with a short body (Key Takeaways bullets, sub-sections, or a procedure — whatever fits the content).

## MOC Best Practices

Categories are MOCs (Maps of Content). When adding a leaf, also consider MOC health:

- **5-entry minimum.** Do NOT propose a new category MOC unless 5+ related leaves exist or are imminent. Premature MOCs add maintenance burden without navigation value. If a leaf would land in an undersized category, prefer placing it in an adjacent existing MOC and noting the gap.
- **Brief orientation per MOC.** Each category MOC opens with 2-3 sentences explaining what the topic covers and how to use the map (not a bare entries list). Orientation lives in `CATEGORY_META[cat].orientation` in `gen_mocs.py` so regeneration preserves it.
- **Brief orientation per index group.** Each section in `index.md` (Task territories, Languages, Cross-cutting, etc.) opens with one sentence framing the group before the bullet list. Orientation lives in `GROUP_ORDER` entries in `gen_mocs.py`.
- **Healthy MOC size: 10-40 entries.** Above 50, consider splitting. Below 5, consider merging or absorbing into an adjacent MOC.
- **Context phrases on every link.** Bare `- [[slug]]` is an address book. Always include the description so readers can scan without opening each file (regen handles this automatically).

## Task

$ARGUMENTS
