#!/bin/bash
# PostToolUse hook for init_workspace - applies target language output style

# Read JSON input
INPUT=$(cat)

# Extract target_language from tool_input using grep/sed (no jq dependency)
TARGET_LANG=$(echo "$INPUT" | grep -o '"target_language"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"target_language"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

if [ -z "$TARGET_LANG" ]; then
    exit 0
fi

# Get plugin root (parent of scripts dir)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"

# Read style file
STYLE_FILE="$PLUGIN_ROOT/styles/${TARGET_LANG}.md"

if [ ! -f "$STYLE_FILE" ]; then
    exit 0
fi

STYLE_CONTENT=$(cat "$STYLE_FILE")

# Output JSON with additionalContext (escape for JSON)
ESCAPED_CONTENT=$(echo "$STYLE_CONTENT" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": $ESCAPED_CONTENT
  }
}
EOF
