#!/bin/bash

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

domain=""
case "$file_path" in
  "$HOME/.claude/knowledge/code/"*.md) domain="code" ;;
  "$HOME/.claude/knowledge/write/"*.md) domain="write" ;;
  *) exit 0 ;;
esac

stats_dir="$HOME/.claude/knowledge/$domain/.stats"
mkdir -p "$stats_dir"

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
jq -nc --arg ts "$ts" --arg path "$file_path" --arg domain "$domain" '{ts: $ts, path: $path, domain: $domain}' >> "$stats_dir/fetches.jsonl"

exit 0
