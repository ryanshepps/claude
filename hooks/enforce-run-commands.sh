#!/bin/bash
# Stop hook: forces Claude to actually run commands instead of suggesting them.
#
# Checks last_assistant_message for patterns that indicate Claude suggested
# a command rather than running it. If detected, blocks the stop and tells
# Claude to run the command.

INPUT=$(cat)

STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0
fi

MESSAGE=$(echo "$INPUT" | jq -r '.last_assistant_message // ""')

if [ -z "$MESSAGE" ]; then
  exit 0
fi

PATTERNS=(
  '[Yy]ou can run'
  '[Yy]ou could run'
  '[Yy]ou may want to run'
  '[Yy]ou might want to run'
  '[Ww]ould you like me to'
  '[Ss]hall I run'
  '[Ss]hould I run'
  '[Dd]o you want me to run'
  '[Dd]o you want me to execute'
  '[Ww]ant me to run'
  '[Ww]ant me to execute'
  '[Ll]et me know if you.* want me to'
  '[Tt]ry running'
  '[Rr]un the following'
  '[Rr]un this command'
  '[Ee]xecute the following'
  '[Ee]xecute this command'
)

COMBINED=$(IFS='|'; echo "${PATTERNS[*]}")

if echo "$MESSAGE" | grep -qE "$COMBINED"; then
  jq -n '{
    decision: "block",
    reason: "You suggested a command instead of running it. Run the command yourself using the Bash tool or other available tools. Never suggest commands for the user to run."
  }'
else
  exit 0
fi
