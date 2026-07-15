# AGENTS.md

This file provides guidance to Codex when working in this repository. Claude
reads the sibling `CLAUDE.md`; keep the dual-agent contract below aligned in
both files.

## Dual-Agent Contract

- This repository must work for both Claude and Codex.
- Shared agent assets live in `src/dot_agents/` and materialize to `~/.agents/`.
- Claude-specific adapters live in `src/dot_claude/` and materialize to `~/.claude/`.
- Codex-specific adapters live in `src/dot_codex/` and materialize to `~/.codex/`.
- Do not put shared skills, shared knowledge, or shared helper scripts directly under `src/dot_claude/` or `src/dot_codex/`.
- When adding a Claude slash command in `src/dot_claude/commands/<name>.md`, add a matching shared skill in `src/dot_agents/skills/<name>/SKILL.md` so Codex has the same workflow.
- When adding shared guidance to either root instruction file, update the sibling root instruction file.
- Keep the global instruction files `src/dot_claude/CLAUDE.md` and `src/dot_codex/AGENTS.md` byte-identical; edit both together.
- Validate compatibility with `python3 src/dot_agents/scripts/validate_dual_agent_repo.py`.

## Purpose

This is a chezmoi-managed personal agent configuration repo. It stores global
rules, shared skills, shared knowledge bases, hooks, and runtime-specific
settings for Claude and Codex. It is not an application project: there is no
build step and no dependency install.

## Key Commands

All chezmoi commands for this repo pass `--config=$HOME/.config/chezmoi/dotagents.toml`.
The existing shell alias is:

```bash
alias ccm='chezmoi --config=$HOME/.config/chezmoi/dotagents.toml'
```

Use:

- `ccm apply` to sync repo state into `~/.agents/`, `~/.claude/`, and `~/.codex/`.
- `ccm diff` to preview pending changes.
- `ccm status` to verify the managed files are in sync.
- `ccm re-add <path>` to pull ad-hoc runtime edits back into source.

## Architecture

```text
.chezmoiroot
src/
  dot_agents/
    skills/                 # Shared Claude/Codex skills
    knowledge/              # Shared code/write knowledge bases
    scripts/                # Shared KB and validation scripts
  dot_claude/
    commands/               # Claude slash commands
    hooks/                  # Claude-compatible hook scripts
    settings.json.tmpl      # Claude settings
    symlink_*               # Compatibility links to ~/.agents/*
  dot_codex/
    AGENTS.md               # Codex global instructions
    config.toml             # Codex global config
    hooks.json.tmpl         # Codex hook config
```

Claude sees shared assets through symlinks:

```text
~/.claude/skills    -> ~/.agents/skills
~/.claude/knowledge -> ~/.agents/knowledge
~/.claude/scripts   -> ~/.agents/scripts
```

Codex reads shared skills directly from `~/.agents/skills` and global guidance
from `~/.codex/AGENTS.md`.

## Conventions

- Shared skills are directories in `src/dot_agents/skills/<name>/` with a
  `SKILL.md` file containing `name` and `description` frontmatter.
- Shared knowledge entries are markdown files in
  `src/dot_agents/knowledge/<domain>/`, where domain is `code` or `write`.
- Claude commands are allowed, but every command must have a same-named shared
  skill for Codex parity.
- Runtime-specific config stays runtime-specific. Do not symlink Claude
  `settings.json` to Codex `config.toml`; share scripts and skills instead.
- Use `~/.agents/...` in shared skills and docs. `~/.claude/...` should appear
  only in Claude-specific adapter files or compatibility explanations.
- After changing settings or hooks, validate rendered JSON/TOML where possible.
