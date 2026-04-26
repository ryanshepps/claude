---
name: knowledge-stats
description: Report fetch frequency stats for the local knowledge base from the PostToolUse hook log at ~/.claude/knowledge/.stats/fetches.jsonl. Use when reviewing which leaves and MOCs are read most/least, to inform manual priority adjustments. Read-only.
---

# Knowledge Stats

## Purpose

Aggregates `~/.claude/knowledge/.stats/fetches.jsonl` (written by `log-knowledge-fetch.sh` PostToolUse hook on every Read of a `~/.claude/knowledge/*.md` file). Reports fetch counts split by leaf vs MOC. Cumulative, all-time. Read-only — never edits priorities.

## When to Use

- User asks for knowledge fetch stats / metrics / "what gets fetched most"
- Periodic review to inform manual priority bumps or demotions
- Identifying never-fetched entries (demote / delete candidates)

## Inputs

- Log: `~/.claude/knowledge/.stats/fetches.jsonl` (one JSON per line: `{ts, path}`)
- Knowledge dir: `~/.claude/knowledge/` — used to classify leaf vs MOC and surface never-fetched files

## Method

1. Read JSONL log. Count occurrences per `path`.
2. For each path, read frontmatter — `type: moc` → MOC, else leaf.
3. List all `*.md` files in `~/.claude/knowledge/` (excluding `.stats/`) — any not in the count map = 0 fetches.
4. Emit two tables sorted descending by count:
   - **Leaves** — `count | slug | priority`
   - **MOCs** — `count | name`
5. Append a **Never fetched** section listing leaves with count 0 (sorted by priority asc, so foundational-but-cold surfaces first).

## Output Shape

```
# Knowledge Fetch Stats

Source: ~/.claude/knowledge/.stats/fetches.jsonl
Range: <earliest ts> → <latest ts>
Total fetches: N

## Leaves (top 20)
| count | slug | priority |
|------:|------|---------:|
|   42  | conways-law | 1 |
...

## MOCs
| count | name |
|------:|------|
|  103  | index |
|   58  | architecture |
...

## Never fetched (N entries)
- foo (p1)
- bar (p3)
...
```

## Rules

- Do NOT recommend priority changes. The user reads the stats and decides.
- Do NOT edit any files. Report only.
- If log is missing or empty, say so plainly and exit.
- Truncate leaf table to top 20 by default; mention total leaf count.
