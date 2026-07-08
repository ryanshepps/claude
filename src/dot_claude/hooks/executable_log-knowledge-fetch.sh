#!/bin/bash

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

domain=""
case "$file_path" in
  "$HOME/.agents/knowledge/code/"*.md) domain="code" ;;
  "$HOME/.agents/knowledge/write/"*.md) domain="write" ;;
  "$HOME/.claude/knowledge/code/"*.md) domain="code" ;;
  "$HOME/.claude/knowledge/write/"*.md) domain="write" ;;
  *) exit 0 ;;
esac

stats_dir="$HOME/.agents/knowledge/$domain/.stats"
mkdir -p "$stats_dir"

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
session_id=$(echo "$input" | jq -r '.session_id // empty')
cwd=$(echo "$input" | jq -r '.cwd // empty')
jq -nc \
  --arg ts "$ts" \
  --arg path "$file_path" \
  --arg domain "$domain" \
  --arg session_id "$session_id" \
  --arg cwd "$cwd" \
  '{ts: $ts, path: $path, domain: $domain, session_id: $session_id, cwd: $cwd}' \
  >> "$stats_dir/fetches.jsonl"

exit 0
