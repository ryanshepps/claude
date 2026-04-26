# SPEC

## §G GOAL
split KB into domain subdirs (`code/`, `write/`), add `/write` skill mirror `/code`, parameterize tooling by domain.

## §C CONSTRAINTS
- chezmoi-managed repo. source = `src/dot_claude/` → `~/.claude/`. apply via `ccm apply`.
- caveman full intensity ∀ writes.
- existing 110 leaves preserve history (`git mv`, ⊥ delete+recreate).
- KBs disjoint. ⊥ shared leaves. ⊥ parent `knowledge/index.md`.
- `/write` = single command `/write <task>`. internal classify compose|tone-check.
- write-KB scope: tone + composition. MOC-ready. ~30-60 leaves target.
- audit prefix: `KB:` ∀ /code (status quo). `WB:` ∀ /write.

## §I INTERFACES
- cmd: `/code <task>` → reads `~/.claude/knowledge/code/index.md`. ⊥ touch write/.
- cmd: `/write <task>` → reads `~/.claude/knowledge/write/index.md`. ⊥ touch code/.
- skill: `add-knowledge <domain> <topic>` — domain ∈ {code, write}. routes write → `knowledge/<domain>/`.
- skill: `audit-knowledge [domain]` — no arg = audit both. arg = scope to one.
- skill: `knowledge-stats [domain]` — reads `knowledge/<domain>/.stats/fetches.jsonl`. no arg = both.
- hook: PostToolUse Read on `knowledge/<domain>/*.md` → append `knowledge/<domain>/.stats/fetches.jsonl`. domain detected from file path.
- file: `~/.claude/knowledge/code/index.md` — code-KB entry, lists code MOCs.
- file: `~/.claude/knowledge/write/index.md` — write-KB entry, lists write MOCs (tone, structure, format).
- file: `src/dot_claude/commands/write.md` — `/write` definition.

## §V INVARIANTS
V1: ∀ existing `src/dot_claude/knowledge/*.md` ! relocate to `code/` via `git mv`. history preserved.
V2: ∀ skill | hook ref `~/.claude/knowledge/` ! take `<domain>` arg | auto-detect from path. ⊥ hardcode bare `knowledge/`.
V3: ⊥ parent `knowledge/index.md`. domains sovereign.
V4: `/code` ! only Read `knowledge/code/**`. `/write` ! only Read `knowledge/write/**`. cross-domain Read ⊥.
V5: fetch-log hook ! detect domain from Read path → write `knowledge/<domain>/.stats/fetches.jsonl`. ⊥ shared log.
V6: post-migration `ccm apply` ! exit 0 & ⊥ broken symlinks. `/code` smoke-test ! pass before write-side starts.
V7: `/write` ! callable only after write-KB seeds ≥ 3 MOCs (tone, structure, format) + ≥ 1 leaf per MOC.
V8: ∀ leaf frontmatter shape ! match across domains: `slug`, `categories`, `priority`, `description`, `applies_when`, `related`. write-KB ? add fields but ! drop existing.

## §T TASKS
id|status|task|cites
T1|x|mkdir `src/dot_claude/knowledge/{code,write}/`|-
T2|x|`git mv` 110 leaves + `.stats/` → `code/`|V1
T3|x|grep hardcoded `~/.claude/knowledge/` refs across repo → enumerate edit targets|V2
T4|x|update `/code` skill: read path → `knowledge/code/index.md`|V2,V4,I.code
T5|x|update fetch-log hook: detect domain from path, write per-domain log|V2,V5
T6|x|parameterize `add-knowledge` skill: accept `<domain>` arg, route writes|V2,I.add-knowledge
T7|x|parameterize `audit-knowledge` skill: optional `[domain]` arg|V2,I.audit-knowledge
T8|x|parameterize `knowledge-stats` skill: optional `[domain]` arg|V2,I.knowledge-stats
T9|x|`ccm apply` + `/code` smoke-test (pick task, verify KB reads land in `code/`)|V6
T10|x|seed `knowledge/write/index.md` + 3 MOCs (`tone.md`, `structure.md`, `format.md`)|V7
T11|x|write `src/dot_claude/commands/write.md` mirroring `/code`. audit prefix `WB:`. internal classify compose\|tone-check|I.write
T12|x|seed write-KB w/ ≥ 1 leaf per MOC (min 3 leaves total)|V7
T13|x|smoke-test `/write` — one compose task + one tone-check task. verify only `knowledge/write/` Read|V4,V7

## §B BUGS
id|date|cause|fix
