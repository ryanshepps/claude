#!/bin/bash

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

ext="${file_path##*.}"
case "$ext" in
  rs) rule="writing-rust" ;;
  py) rule="writing-python" ;;
  java) rule="writing-java" ;;
  ex|exs) rule="writing-elixir" ;;
  *) exit 0 ;;
esac

jq -nc --arg msg "IMPORTANT: Review the code you just wrote against rules/${rule}.md. Fix any violations silently." '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $msg}}'
