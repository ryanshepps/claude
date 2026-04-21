# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Personal Claude Code configuration repository. Stores global rules, skills, commands, hooks, and settings that are applied into `~/.claude/` via [chezmoi](https://www.chezmoi.io/). Not a software project — no build step, no tests, no dependencies.

This repo is a **second, Claude-specific chezmoi source**. A separate chezmoi source at `~/.local/share/chezmoi` (the `dotfiles` repo) manages general dotfiles (vim, bash, git). The two are kept apart via a dedicated `~/.config/chezmoi/claude.toml` config file so each source stays in its own GitHub repo with its own history.

## Key Commands

All chezmoi commands for this repo pass `--config=$HOME/.config/chezmoi/claude.toml`. Simplest UX: add a shell alias to `.zshrc`:

```bash
alias ccm='chezmoi --config=$HOME/.config/chezmoi/claude.toml'
```

Then:

- `ccm apply` — sync repo → `~/.claude/`.
- `ccm diff` — preview pending changes.
- `ccm edit --apply <path>` — edit source file, auto-apply on save.
- `ccm re-add ~/.claude/<file>` — pull an ad-hoc `~/.claude/` edit back into source.
- `ccm status` — list files with pending changes. Exit 0 + empty output = in sync.

### First-time setup on a new machine

```bash
git clone git@github.com:<user>/<this-repo>.git ~/Projects/claude
printf "true\n" | chezmoi init \
  --config=$HOME/.config/chezmoi/claude.toml \
  --source=$HOME/Projects/claude
chezmoi --config=$HOME/.config/chezmoi/claude.toml apply
```

- Replace `true` with `false` for a personal machine (affects whether work-specific settings render).
- The answer is stored in `~/.config/chezmoi/claude.toml` — machine-local, never committed.
- Remove existing symlinks in `~/.claude/` that point into this repo before the first apply (`chezmoi apply` refuses to overwrite dangling/symlinked targets).

## Architecture

```
.chezmoiroot                           → points chezmoi at `src/`
CLAUDE.md, README.md, plans/…          → repo metadata, outside chezmoi's view
src/
  .chezmoi.toml.tmpl                   → init template; prompts for `work` bool, emits sourceDir
  dot_claude/                          → materializes to ~/.claude/
    rules/                             → Global rules (*.md) loaded every conversation
    skills/                            → Skill directories, each with a SKILL.md
    commands/                          → Slash commands (*.md)
    hooks/executable_*.sh              → Shell scripts; `executable_` prefix preserves +x
    settings.json.tmpl                 → Go-templated config (work-specific sections gated by {{ if .work }})
    agents/                            → Agent definitions
```

Work-specific config (e.g. `arc@voltra` plugin, `voltra` marketplace path, `knowledge/` repo hooks) lives inside `{{ if .work }} … {{ end }}` blocks in `settings.json.tmpl`. Values never touch the repo — they render into `~/.claude/settings.json` only on machines where `work = true`.

## Conventions

- Rules are standalone markdown files in `src/dot_claude/rules/` — one file per topic.
- Skills are directories in `src/dot_claude/skills/<name>/` containing at minimum a `SKILL.md`. Large skills split content into multiple reference files.
- Commands are markdown files in `src/dot_claude/commands/` that define slash commands.
- Hooks are shell scripts in `src/dot_claude/hooks/` with the `executable_` prefix (chezmoi restores the +x bit on apply).
- When adding a new machine-divergent setting, wrap it in `{{ if .work }} … {{ end }}` inside `settings.json.tmpl` rather than leaving it as a plain value that would diff on `git status`.
- After editing `settings.json.tmpl`, validate with:
  ```bash
  printf '[data]\nwork = true\n' > /tmp/data.toml
  chezmoi execute-template --config /tmp/data.toml < src/dot_claude/settings.json.tmpl | jq .
  ```
  Repeat with `work = false` to verify the personal render.
