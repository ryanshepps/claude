---
name: knowledge-stats
description: Report fetch frequency stats for a domain-scoped knowledge base from the PostToolUse hook log at ~/.claude/knowledge/<domain>/.stats/fetches.jsonl. Use when reviewing which leaves and MOCs are read most/least, to inform manual priority adjustments. Read-only.
---

# Knowledge Stats

## Purpose

Aggregates per-domain `~/.claude/knowledge/<domain>/.stats/fetches.jsonl` (written by `log-knowledge-fetch.sh` PostToolUse hook on every Read of a `~/.claude/knowledge/<domain>/*.md` file). Reports fetch counts split by leaf vs MOC. Cumulative, all-time. Read-only — never edits priorities.

## When to Use

- User asks for knowledge fetch stats / metrics / "what gets fetched most" — ask which domain if unclear
- Periodic review to inform manual priority bumps or demotions
- Identifying never-fetched entries (demote / delete candidates)

## Inputs

Argument: `[domain]` — `code`, `write`, or omitted (report both, two sections).

Per-domain inputs:
- Log: `~/.claude/knowledge/<domain>/.stats/fetches.jsonl` (one JSON per line: `{ts, path, domain}`)
- Knowledge dir: `~/.claude/knowledge/<domain>/` — used to classify leaf vs MOC and surface never-fetched files

If no domain arg → emit both reports back-to-back, headed by domain.

## Method

For each domain:
1. Read JSONL log. Count occurrences per `path`.
2. For each path, read frontmatter — `type: moc` → MOC, else leaf.
3. List all `*.md` files in `~/.claude/knowledge/<domain>/` (excluding `.stats/`) — any not in the count map = 0 fetches.
4. Emit two tables sorted descending by count:
   - **Leaves** — `count | slug | priority`
   - **MOCs** — `count | name`
5. Append a **Never fetched** section listing leaves with count 0 (sorted by priority asc, so foundational-but-cold surfaces first).

## Output Shape

```
# Knowledge Fetch Stats — <domain>

Source: ~/.claude/knowledge/<domain>/.stats/fetches.jsonl
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
- If a domain's log is missing or empty, say so plainly for that domain and skip its tables.
- Truncate leaf table to top 20 by default; mention total leaf count.
