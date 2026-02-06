#!/bin/bash
# Syncs rules and skills from this repo into ~/.claude/ as symlinks.
# Run after adding or removing files.

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

sync_rules() {
  local src="$REPO_DIR/rules"
  local dest="$HOME/.claude/rules"

  mkdir -p "$dest"

  # Remove stale symlinks pointing into this repo
  for link in "$dest"/*.md; do
    [ -L "$link" ] && [[ "$(readlink "$link")" == "$src/"* ]] && rm "$link"
  done

  # Create symlinks for current rule files
  for file in "$src"/*.md; do
    [ -f "$file" ] && ln -s "$file" "$dest/$(basename "$file")"
  done

  echo "Rules: $src -> $dest"
  ls -1 "$dest"
}

sync_skills() {
  local src="$REPO_DIR/skills"
  local dest="$HOME/.claude/skills"

  mkdir -p "$dest"

  # Remove stale symlinks pointing into this repo
  for link in "$dest"/*/; do
    link="${link%/}"
    [ -L "$link" ] && [[ "$(readlink "$link")" == "$src/"* ]] && rm "$link"
  done

  # Create symlinks for current skill directories
  for dir in "$src"/*/; do
    dir="${dir%/}"
    [ -d "$dir" ] && ln -s "$dir" "$dest/$(basename "$dir")"
  done

  # Symlink .gitignore if present
  [ -f "$src/.gitignore" ] && ln -sf "$src/.gitignore" "$dest/.gitignore"

  echo "Skills: $src -> $dest"
  ls -1 "$dest"
}

sync_rules
echo ""
sync_skills
