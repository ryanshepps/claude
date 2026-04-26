#!/bin/bash

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

case "$file_path" in
  "$HOME/.claude/knowledge/"*.md) ;;
  *) exit 0 ;;
esac

stats_dir="$HOME/.claude/knowledge/.stats"
mkdir -p "$stats_dir"

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
jq -nc --arg ts "$ts" --arg path "$file_path" '{ts: $ts, path: $path}' >> "$stats_dir/fetches.jsonl"

exit 0
