---
description: Turn knowledge-base fetch/gap telemetry into reviewed curation edits (new leaves, related-links, priority signals). Proposes; you approve every write.
argument-hint: "[domain] — code, write, or omit for both"
---

# /knowledge-reflect $ARGUMENTS

Close the knowledge-base loop: read usage telemetry, propose bounded curation
edits, apply only what the user approves. This is the **Reflector + Curator** for
the KB. The `code`/`write` skills produce the trajectories (fetches logged, misses
recorded as gaps); you turn them into edits.

Argument `$ARGUMENTS` is an optional domain: `code`, `write`, or omitted (reflect
both, one section each). Telemetry lives at `~/.agents/knowledge/<domain>/.stats/`
(`fetches.jsonl`, `gaps.jsonl`, `last_reviewed`). If a domain has none, say so and
skip it.

## Flow

1. **Mine.** For each domain:
   ```bash
   python3 ~/.agents/scripts/kb_reflect.py --knowledge-dir ~/.agents/knowledge/<domain>
   ```
   Present the report's five buckets. Edit nothing yet.

2. **Walk candidates with the user, one bucket at a time** — explicit decision before any file changes:
   - **New-leaf candidates (recorded gaps)** → hand approved ones to `/knowledge-add <domain> <gap>`, citing the gap note. Skip stale/already-covered gaps and say why.
   - **Missing `related:` links (co-fetched, not linked)** → for approved pairs, add each slug to the other leaf's `related:`. Cheapest, highest-signal edit.
   - **Priority signals (hot but low-priority)** → propose a bump; flag that fetch count is a weak proxy (Goodhart). User decides.
   - **Cold demote/delete (p3-5, never fetched)** → only when the log is substantial (script suppresses on thin logs). Per-leaf, never batched.
   - **Cold but foundational (p1-2, never fetched)** → informational only. Do NOT demote on fetch count.

3. **Apply approved edits**, then for any changed/deleted leaf regenerate + validate:
   ```bash
   python3 ~/.agents/scripts/gen_mocs.py    --knowledge-dir ~/.agents/knowledge/<domain>
   python3 ~/.agents/scripts/validate_kb.py --knowledge-dir ~/.agents/knowledge/<domain>
   ```
   Fix errors before continuing. (New leaves via `/knowledge-add` already ran this pair.)

4. **Advance the watermark** so the nudge resets — even if nothing was accepted:
   ```bash
   python3 ~/.agents/scripts/kb_reflect.py --knowledge-dir ~/.agents/knowledge/<domain> --mark-reviewed
   ```

5. **Contribution scope.** Edits landed only in `~/.agents/` on this machine. For
   universal edits, sync into the chezmoi source and push (same mechanism as
   `/knowledge-add`: `chezmoi $CFG add` new files, `re-add` regenerated MOCs and
   edited leaves, commit + push from the source repo). Leave machine-specific edits local.

6. **Report** proposals, applied edits, the new watermark, and the contribution scope.

## Guardrails

- **Approve every write.** This command proposes; the user disposes.
- **Fetch count is a weak proxy.** Never auto-adjust priority from counts.
- **Cold ≠ useless.** Never demote/delete a foundational (p1-2) leaf for being unfetched.
- **Bounded edits only.** One leaf, one field at a time. No sweeping rewrites or recategorization unless asked.
- **Never cross domains**, and never skip regen + validate after a change.

## Task

$ARGUMENTS
