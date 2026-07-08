---
name: knowledge-reflect
description: Turn knowledge-base fetch/gap telemetry into reviewed curation edits — new-leaf candidates from recorded gaps, missing `related:` links from co-fetches, and priority/cold signals. Use when the SessionStart nudge flags pending curation, or when the user asks to reflect on / curate / prune the knowledge base from usage data. Proposes; the user approves every write.
---

# Knowledge Reflect

## Purpose

Closes the knowledge-base loop. The `code`/`write` skills generate trajectories
(fetches are logged; misses are recorded as gaps); this skill is the **Reflector +
Curator**: it reads that telemetry, proposes bounded curation edits, and — only
on your approval — applies them. It never rewrites the corpus on its own.

Complements the family:
- `knowledge-stats` — raw fetch counts, read-only. [[knowledge-stats]]
- `knowledge-audit` — static structural health, read-only. [[knowledge-audit]]
- `knowledge-add` — writes a single new leaf. [[knowledge-add]]
- **`knowledge-reflect`** — usage-driven curation across the corpus, gated on approval.

## When to Use

- The SessionStart nudge printed "📚 Knowledge base — pending curation".
- User asks to "reflect on / curate / prune / review usage of" a KB.
- Periodically, to convert accumulated gaps and co-fetch patterns into edits.

## Inputs

Argument: `[domain]` — `code`, `write`, or omitted (reflect both, one section each).

Telemetry lives at runtime under `~/.agents/knowledge/<domain>/.stats/`:
`fetches.jsonl`, `gaps.jsonl`, `last_reviewed`. If a domain has no telemetry,
say so and skip it.

## Flow

1. **Mine.** For each domain, run:
   ```bash
   python3 ~/.agents/scripts/kb_reflect.py --knowledge-dir ~/.agents/knowledge/<domain>
   ```
   It reports five candidate buckets since the last-reviewed watermark. Present
   the report; do not edit anything yet.

2. **Walk candidates with the user, one bucket at a time.** For each, get an
   explicit decision before touching a file:

   - **New-leaf candidates (recorded gaps)** → for each gap the user wants to
     fill, hand off to `knowledge-add` (`/knowledge-add <domain> <the gap>`),
     citing the gap note as the source need. Skip gaps that are stale or already
     covered — say why.
   - **Missing `related:` links (co-fetched, not linked)** → for approved pairs,
     add each slug to the other leaf's `related:` list. These are the cheapest,
     highest-signal edits — two leaves repeatedly read together should point at
     each other.
   - **Priority signals (hot but low-priority)** → propose a bump, but flag
     explicitly that fetch count is a weak proxy (Goodhart). The user decides.
   - **Cold demote/delete (p3-5, never fetched)** → only actionable once the log
     is substantial (the script suppresses this bucket on a thin log). Discuss
     demotion or deletion per leaf; never batch.
   - **Cold but foundational (p1-2, never fetched)** → informational only. Do
     **not** demote on fetch count — foundational entries are often cold because
     they are internalized, not useless.

3. **Apply approved edits.** For any leaf whose `related:` or `priority`
   frontmatter changed, or any leaf deleted, regenerate and validate:
   ```bash
   python3 ~/.agents/scripts/gen_mocs.py    --knowledge-dir ~/.agents/knowledge/<domain>
   python3 ~/.agents/scripts/validate_kb.py --knowledge-dir ~/.agents/knowledge/<domain>
   ```
   Fix any validation errors before proceeding. (New leaves added via
   `knowledge-add` already run this pair.)

4. **Advance the watermark** so the nudge resets — even if you accepted nothing,
   the review still happened:
   ```bash
   python3 ~/.agents/scripts/kb_reflect.py --knowledge-dir ~/.agents/knowledge/<domain> --mark-reviewed
   ```

5. **Contribution scope.** Steps 2-3 only touched `~/.agents/` on this machine.
   For universal edits, sync into the chezmoi source and push (same mechanism as
   `knowledge-add` step 8: `chezmoi $CFG add` new files, `re-add` regenerated
   MOCs and edited leaves, then commit + push from the source repo). Leave
   machine-specific edits local.

6. **Report** what was proposed, what you applied, the new watermark, and the
   contribution scope chosen.

## Guardrails

Self-improving loops optimize whatever signal they are given, so this one keeps a
human in the decision seat:

- **Approve every write.** This skill proposes; the user disposes. No unattended
  curation.
- **Fetch count is a weak proxy.** Never auto-adjust priority from counts. See
  [[goodharts-law]] — the moment a metric becomes a target it stops measuring
  what you cared about.
- **Cold ≠ useless.** Never demote or delete a foundational (p1-2) leaf because
  it is unfetched. Protect corpus diversity.
- **Bounded edits only.** One leaf, one field at a time. No sweeping rewrites,
  no recategorization without the user asking.
- **Read-mostly.** Mining and reporting are safe to run anytime; only steps 2-3
  mutate, and only with approval.

## Rules

- Always pass `--knowledge-dir ~/.agents/knowledge/<domain>` to every script.
- Never cross domains: a `code` reflection never touches `write` leaves.
- Never skip the regen + validate pair after a frontmatter or file change.
- Always advance the watermark at the end of a review, or the nudge will keep
  firing on already-reviewed telemetry.
