---
name: audit-knowledge
description: Audit the local knowledge base for MOC health, structural drift, and best-practice violations that scripts cannot catch. Use when reviewing `~/.claude/knowledge/` for issues like premature MOCs, missing orientations, stale index counts, miscategorized leaves, or semantic drift from add-knowledge rules. Read-only — surfaces a punch list, never edits.
---

# Audit Knowledge

## Purpose

Reviews the knowledge base at `~/.claude/knowledge/` (or `<repo>/src/dot_claude/knowledge/` when run from the chezmoi source) and reports a health punch list. Complements `validate_kb.py` — that script catches mechanical errors (missing fields, broken refs); this skill catches **judgment calls** that require reading content.

This skill is read-only. It produces a report. The user decides what to fix.

## When to Use

- User asks to "audit / review / check the knowledge base"
- After bulk additions, before pruning, or when the corpus feels off
- Periodic spring-cleaning of MOCs and index

## Inputs

Default knowledge dir resolution order:
1. If invoked inside the chezmoi source repo (file `src/dot_claude/knowledge/index.md` exists), use that.
2. Else `~/.claude/knowledge/`.

## What to Check

Group findings under these headings. Skip a heading if no findings.

### 1. Premature MOCs (`<5 entries`)

Best practice (per `commands/add-knowledge.md` and ars contexta): do NOT keep a category MOC with fewer than 5 entries. List every category MOC with `<5` leaves. For each, suggest a merge target or an absorbing MOC.

How to count: parse leaf frontmatter `categories:` lists; count leaves per category.

### 2. Oversized MOCs (`>50 entries`)

Healthy range 10-40, warning >50. Suggest split axes (sub-community, update frequency, distinct sub-topic).

### 3. Missing or thin orientations

Each category MOC must open with 2-3 sentence orientation. Each `index.md` group section must open with one sentence framing. Flag MOCs that jump straight to "## Entries" with no preamble. Flag groups in `index.md` rendered as title + bullets only.

Source of truth lives in `gen_mocs.py` (`CATEGORY_META` orientation field, `GROUP_ORDER` group orientation). If gen_mocs.py lacks orientation fields, that itself is a finding.

### 4. Index drift

- Total entry count in `index.md` vs actual `*.md` leaves (excluding MOC files).
- Per-category count claims in `index.md` vs actual.
- Categories present in leaves but not in `GROUP_ORDER`, or vice versa.

### 5. Semantic miscategorization

Sample 5-10 leaves at random plus any leaf whose `categories` list seems suspect. For each, ask: does the category actually fit the content? Flag mismatches with a short justification. Do NOT rewrite — just report.

### 6. Anti-patterns

- **Bare-link MOCs** — entries without context phrases (rare since regen prevents it, but possible if MOCs were hand-edited).
- **MOC-as-content** — synthesis prose inside an MOC that should be a leaf instead.
- **Orphan leaves** — leaf with `categories: []` or pointing to nonexistent category.
- **Stale `related:` lists** — `related` slugs that no longer exist.
- **Duplicate leaves** — slugs covering near-identical concepts.

### 7. Cross-cutting tensions

If two MOCs cover the same conceptual ground, note it (candidate for merge or for a Tensions section in the parent MOC).

## Output Format

Return one report. No edits.

```
# Knowledge Base Audit — <YYYY-MM-DD>

Knowledge dir: <resolved path>
Leaves: <count>  ·  Categories: <count>

## Premature MOCs
- `python` (1 entry) → fold into new `languages` MOC
- ...

## Oversized MOCs
- (none)

## Missing Orientations
- `architecture.md` — no preamble; jumps to "## Entries"
- `index.md` group "Languages" — no orientation sentence

## Index Drift
- index.md claims 94 entries; actual: 96

## Semantic Miscategorization
- `goodharts-law` listed under `quality` — fits `decisions` better. Reasoning: ...

## Anti-Patterns
- (none)

## Cross-cutting Tensions
- `design.md` and `quality.md` both cover testing pyramid — consider single home.

## Recommended Order of Operations
1. Fix orientations (cheap, no schema change)
2. Merge premature language MOCs (touches gen_mocs.py)
3. Update index counts (auto via regen)
4. Re-evaluate miscategorized leaves with user
```

## Rules

- Read-only. Never edit files. Never run gen_mocs.py or validate_kb.py with `--write`.
- Cite specific files and counts. No vague claims.
- If a finding is judgment-dependent, say so and give reasoning so the user can overrule.
- Defer to `validate_kb.py` for mechanical checks — don't duplicate its work; just note "run validator" if structural integrity is suspect.
- After reporting, ask the user which findings to act on. Do NOT begin fixes unprompted.
