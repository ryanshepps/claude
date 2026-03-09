# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo is a personal Claude Code configuration repository. It stores global rules, skills, commands, hooks, and settings that get symlinked into `~/.claude/` via `sync.sh`. It is not a software project — there is no build step, no tests, and no dependencies.

## Key Commands

- **Sync all config to `~/.claude/`:** `./sync.sh` — run after adding, removing, or renaming any files. It creates symlinks for rules, skills, commands, hooks, and settings.

## Architecture

```
rules/        → ~/.claude/rules/       Global rules (*.md) loaded into every conversation
skills/       → ~/.claude/skills/      Skill directories, each with a SKILL.md
commands/     → ~/.claude/commands/    Slash commands (*.md)
hooks/        → ~/.claude/hooks/       Shell scripts triggered by Claude Code events
settings.json → ~/.claude/settings.json  Global settings (hooks config, plugins, permissions)
.claude/settings.local.json             Per-repo permissions (not synced)
```

`sync.sh` removes stale symlinks pointing into this repo before creating new ones, so deleted files are cleaned up automatically.

## Conventions

- Rules are standalone markdown files in `rules/` — one file per topic.
- Skills are directories in `skills/<name>/` containing at minimum a `SKILL.md`. Large skills split content into multiple reference files.
- Commands are markdown files in `commands/` that define slash commands.
- Hooks are executable shell scripts in `hooks/`.
