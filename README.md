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
    knowledge/                        → flat knowledge base, fetched on demand
    commands/                         → slash commands (*.md)
    skills/                           → skill directories (each has SKILL.md)
    agents/                           → agent definitions
    hooks/executable_*.sh             → shell hooks (executable_ preserves +x)
    scripts/                          → helper scripts (e.g., MOC regenerator)
    settings.json.tmpl                → Go-templated settings (work-gated)
```

## Knowledge Management System

The `knowledge/` folder is an agent-consumable corpus of coding laws, style rules, and workflow guides. Inspired by [arscontexta](https://github.com/agenticnotetaking/arscontexta).

### Concepts

- **Leaf** — atomic `.md` file, one per entry (e.g., `conways-law.md`, `writing-python.md`). Each has YAML frontmatter: `slug`, `categories` (list), `priority` (1-5), `description`, `applies_when`, `related`, optional `source`.
- **Category MOC** (Map of Content) — `<category>.md` file listing all leaves in that category, sorted by priority. 16 total: 7 task-based (architecture, design, teams, planning, quality, scale, decisions), 5 language-based (python, rust, java, elixir, frontend), 4 cross-cutting (testing, prs, style, communication).
- **Top-level index** — `index.md` lists all 16 category MOCs grouped by axis.

Leaves with multiple categories appear in multiple MOCs. Filesystem stays flat; categorization lives in frontmatter.

### Retrieval Flow

The `/code <task>` slash command directs the agent to:

1. Read `~/.claude/knowledge/index.md` to see territories
2. Classify the task against categories
3. Read 1-2 relevant category MOCs
4. Pick 3-7 leaves by description + `applies_when` match
5. Read leaf files fully before decisions

The agent narrates each Read with a `KB:` prefix so you can audit which knowledge is entering context.

### Adding Knowledge

The `/add-knowledge <instruction>` slash command:

1. Inspects existing leaves for voice matching
2. Synthesizes a new entry per the schema
3. Shows a draft for review
4. Writes the file on approval
5. Regenerates all MOCs via `scripts/gen_mocs.py`
6. Validates structural integrity via `scripts/validate_kb.py`

### Helper Scripts

- `scripts/gen_mocs.py` — regenerate category MOCs and `index.md` from leaf frontmatter. Run after manual leaf edits.
- `scripts/validate_kb.py` — static checks (slug matches filename, wiki-links resolve, priorities in range, no empty descriptions, etc.). Run before `ccm apply`.

Both default to the sibling `knowledge/` directory. Override with `--knowledge-dir <path>`.
