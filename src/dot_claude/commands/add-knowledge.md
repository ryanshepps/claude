---
description: Synthesize a new entry for a knowledge base (code or write), write it, and regenerate MOCs.
argument-hint: "<domain> <instruction>  — domain ∈ {code, write}; e.g. 'code add rubber duck debugging' or 'write add active voice rule'"
---

# /add-knowledge $ARGUMENTS

You are adding a new entry to a domain-scoped knowledge base under `~/.claude/knowledge/<domain>/`. Two domains exist:

- `code` — software-engineering laws, language rules, workflow guides. Consumed by `/code`.
- `write` — prose craft, tone, voice, composition, format rules. Consumed by `/write`.

**First token of `$ARGUMENTS` MUST be the domain.** Parse it. If missing or invalid (`code|write`), stop and ask the user which KB this entry belongs to.

Let `<DOMAIN>` = parsed domain. Let `<KB>` = `~/.claude/knowledge/<DOMAIN>`.

## Existing Schema (required)

```yaml
---
slug: <kebab-case-slug>              # must match filename stem
categories: [<cat1>, <cat2>]         # 1-3 from the domain's category set (read <KB>/index.md to see)
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

1. **Read `<KB>/index.md`** to see existing categories + pattern for that domain.
2. **Inspect 2-3 adjacent existing leaves** in the likely category to match voice/density. Announce each Read: `Reading <file> — to match style of similar entries`.
3. **Synthesize the entry** from the instruction (the rest of `$ARGUMENTS` after the domain token):
   - Choose `slug` (kebab-case). Confirm no collision: `ls <KB>/<slug>.md` must fail.
   - Choose `categories` — 1-3 matching the actual use-case, not just topical similarity. Must be drawn from THIS domain's category set.
   - Assign `priority` — be honest. Default to 3 if unsure. Priority 1 = cited in most tasks for this domain.
   - Write `description` — one sentence, applicability-forward.
   - Write `applies_when` — 2-4 short phrases the agent can match against task descriptions.
   - Populate `related` — existing slugs in the same domain that pair with this entry. Use `[]` if truly isolated. ⊥ cross-domain related links.
4. **Show the draft** to the user before writing. Single message, code-fenced frontmatter + body preview.
5. **On approval, write** to `<KB>/<slug>.md`.
6. **Regenerate MOCs**: run `python3 ~/.claude/scripts/gen_mocs.py --knowledge-dir <KB>`. Report the output.
7. **Validate**: run `python3 ~/.claude/scripts/validate_kb.py --knowledge-dir <KB>`. If errors, fix the new file and revalidate.
8. **Report** the final file path, which MOCs now include it, and any warnings.

## Rules

- Never overwrite an existing file silently. If `<slug>.md` exists in `<KB>`, stop and ask whether to update, rename, or abort.
- Never skip validation. The regen + validate pair keeps the corpus coherent.
- Never invent categories. Each domain has a fixed category set defined in the script's META. If the instruction doesn't fit, stop and ask whether to add a new category (which requires updating per-domain META in `~/.claude/scripts/gen_mocs.py` and validator).
- Never cross domains. A `code` entry ! land in `<KB>/code/`; a `write` entry ! land in `<KB>/write/`. ⊥ shared leaves.
- Match existing density. Leaves are typically 150-300 words with a short body (Key Takeaways bullets, sub-sections, or a procedure — whatever fits).

## MOC Best Practices

Categories are MOCs (Maps of Content). When adding a leaf, also consider MOC health:

- **5-entry minimum.** Do NOT propose a new category MOC unless 5+ related leaves exist or are imminent. Premature MOCs add maintenance burden without navigation value. If a leaf would land in an undersized category, prefer placing it in an adjacent existing MOC and noting the gap.
- **Brief orientation per MOC.** Each category MOC opens with 2-3 sentences explaining what the topic covers and how to use the map (not a bare entries list). Orientation lives in the per-domain `CATEGORY_META[cat].orientation` in `gen_mocs.py` so regeneration preserves it.
- **Brief orientation per index group.** Each section in `index.md` opens with one sentence framing the group before the bullet list. Orientation lives in per-domain `GROUP_ORDER` entries in `gen_mocs.py`.
- **Healthy MOC size: 10-40 entries.** Above 50, consider splitting. Below 5, consider merging or absorbing into an adjacent MOC.
- **Context phrases on every link.** Bare `- [[slug]]` is an address book. Always include the description so readers can scan without opening each file (regen handles this automatically).

## Task

$ARGUMENTS
