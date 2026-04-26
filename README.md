# claude

Personal Claude Code configuration. Materialized into `~/.claude/` via [chezmoi](https://www.chezmoi.io/).

## Repo Layout

```
.chezmoiroot                          → points chezmoi at src/
CLAUDE.md                             → repo guide for Claude Code (not synced)
README.md                             → this file (not synced)
src/
  .chezmoi.toml.tmpl                  → init template; prompts for `work` bool
  dot_claude/                         → materializes to ~/.claude/
    knowledge/
      code/                           → code knowledge base (laws, style, workflow), consumed by /code
      write/                          → writing knowledge base (tone, structure, format), consumed by /write
    commands/                         → slash commands (*.md)
    skills/                           → skill directories (each has SKILL.md)
    agents/                           → agent definitions
    hooks/executable_*.sh             → shell hooks (executable_ preserves +x)
    scripts/                          → helper scripts (e.g., MOC regenerator)
    settings.json.tmpl                → Go-templated settings (work-gated)
```

## Knowledge Management System

The `knowledge/` folder holds two domain-scoped, agent-consumable corpora. Inspired by [arscontexta](https://github.com/agenticnotetaking/arscontexta).

- `knowledge/code/` — coding laws, style rules, language guides, workflow patterns. Consumed by `/code`.
- `knowledge/write/` — prose craft: tone, structure, format. Consumed by `/write`.

KBs are disjoint — no shared leaves, no parent index. Each domain is sovereign.

### Concepts

- **Leaf** — atomic `.md` file, one per entry (e.g., `conways-law.md`, `active-voice.md`). Each has YAML frontmatter: `slug`, `categories` (list), `priority` (1-5), `description`, `applies_when`, `related`, optional `source`.
- **Category MOC** (Map of Content) — `<category>.md` file listing all leaves in that category, sorted by priority.
  - `code/`: architecture, design, teams, planning, quality, scale, decisions, languages, ux, testing, prs, style, communication.
  - `write/`: tone, structure, format.
- **Top-level index** — `<domain>/index.md` lists that domain's category MOCs grouped by axis.

Leaves with multiple categories appear in multiple MOCs of their own domain. Filesystem stays flat within each domain; categorization lives in frontmatter.

### Retrieval Flow

The `/code <task>` and `/write <task>` slash commands direct the agent to:

1. Read `~/.claude/knowledge/<domain>/index.md` to see that domain's territories
2. Classify the task against categories
3. Read 1-2 relevant category MOCs
4. Pick 3-7 leaves by description + `applies_when` match
5. Read leaf files fully before decisions

`/code` reads only from `code/`; `/write` reads only from `write/`. The agent narrates each Read with a domain-scoped audit prefix:
- `KB:` — code knowledge fetch
- `WB:` — writing knowledge fetch

### Adding Knowledge

The `/add-knowledge <domain> <instruction>` slash command:

1. Parses the leading `<domain>` token (`code` or `write`)
2. Inspects existing leaves in that domain for voice matching
3. Synthesizes a new entry per the schema
4. Shows a draft for review
5. Writes the file on approval to `knowledge/<domain>/<slug>.md`
6. Regenerates MOCs via `scripts/gen_mocs.py --knowledge-dir <KB>`
7. Validates structural integrity via `scripts/validate_kb.py --knowledge-dir <KB>`

### Helper Scripts

- `scripts/gen_mocs.py` — regenerate category MOCs and `index.md` from leaf frontmatter. Domain auto-detected from `--knowledge-dir` basename (`code` or `write`). Per-domain `CATEGORY_META`, `GROUP_ORDER`, and `CATEGORY_TENSIONS`.
- `scripts/validate_kb.py` — static checks (slug matches filename, wiki-links resolve, priorities in range, no empty descriptions, etc.). Domain auto-detected from `--knowledge-dir` basename.

Both default to `knowledge/code/`. Always pass `--knowledge-dir <path>` for the write domain.

### Fetch-Frequency Logging

A `PostToolUse` hook (`hooks/log-knowledge-fetch.sh`) appends to `knowledge/<domain>/.stats/fetches.jsonl` on every Read of a `knowledge/<domain>/*.md` file. Domain is detected from the file path. Use the `knowledge-stats` skill to aggregate.
