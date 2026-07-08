#!/bin/bash

cat >/dev/null 2>&1

gap_threshold=3
stale_days=14

now_epoch=$(date +%s)
lines=""

for domain in code write; do
  stats_dir="$HOME/.agents/knowledge/$domain/.stats"
  gaps="$stats_dir/gaps.jsonl"
  watermark_file="$stats_dir/last_reviewed"
  [ -f "$gaps" ] || continue

  watermark=""
  [ -s "$watermark_file" ] && watermark=$(tr -d '[:space:]' < "$watermark_file")

  pending=$(jq -rR --arg w "$watermark" 'fromjson? | select(.ts > $w) | .ts' "$gaps" 2>/dev/null | grep -c .)
  [ "$pending" -gt 0 ] || continue

  if [ -n "$watermark" ]; then
    wm_epoch=$(date -d "$watermark" +%s 2>/dev/null || echo "$now_epoch")
    days_since=$(( (now_epoch - wm_epoch) / 86400 ))
    age="${days_since}d since last review"
  else
    days_since=99999
    age="never reviewed"
  fi

  if [ "$pending" -ge "$gap_threshold" ] || [ "$days_since" -ge "$stale_days" ]; then
    noun="gap notes"
    [ "$pending" -eq 1 ] && noun="gap note"
    lines="${lines}- ${domain}: ${pending} ${noun} pending (${age})"$'\n'
  fi
done

[ -n "$lines" ] || exit 0

printf '📚 Knowledge base — pending curation:\n%sRun /knowledge-reflect to review. Recorded misses become new-leaf candidates; nothing changes without your approval.\n' "$lines"
exit 0
