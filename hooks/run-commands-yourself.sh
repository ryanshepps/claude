#!/bin/bash
# UserPromptSubmit hook: reminds Claude to execute commands itself
# rather than suggesting the user run them.

cat <<'EOF'
{
  "systemMessage": "IMPORTANT: Never tell the user to run commands themselves. Always execute commands directly using the Bash tool or other available tools. If you need information that only the user can provide (credentials, preferences, clarifications), ask for that specific information — do not ask them to run a command and paste the output. Keep working autonomously until you are truly blocked on user input."
}
EOF
