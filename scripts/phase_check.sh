#!/bin/bash
# Stop hook: Check if translation phases are ongoing
# Reads manifest.json via symlink to check phase status
#
# This hook is triggered when Claude stops during a /translate command.
# It checks if more translation phases remain and blocks stopping if so,
# instructing Claude to compact and continue.

MANIFEST_LINK="/tmp/claude_translate_manifest.json"
INPUT=$(cat)

# Check stop_hook_active to prevent infinite loops
STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
if [ "$STOP_ACTIVE" = "true" ]; then
    exit 0
fi

# Check if manifest symlink exists
if [ ! -L "$MANIFEST_LINK" ] && [ ! -f "$MANIFEST_LINK" ]; then
    exit 0
fi

# Read manifest
MANIFEST=$(cat "$MANIFEST_LINK" 2>/dev/null)
if [ -z "$MANIFEST" ]; then
    exit 0
fi

# Define phase order
PHASES=("input_validation" "context_analysis" "text_splitting" "summarization" "translation" "verification" "assembly")

# Check if skip_verify is set
SKIP_VERIFY=$(echo "$MANIFEST" | jq -r '.skip_verify // false')

# Find the last completed phase and determine next phase
LAST_COMPLETED=""
NEXT_PHASE=""

for i in "${!PHASES[@]}"; do
    phase="${PHASES[$i]}"

    # Skip verification phase if skip_verify is true
    if [ "$phase" = "verification" ] && [ "$SKIP_VERIFY" = "true" ]; then
        continue
    fi

    status=$(echo "$MANIFEST" | jq -r ".phases.${phase}.status // \"pending\"")

    if [ "$status" = "completed" ]; then
        LAST_COMPLETED="$phase"
    elif [ "$status" = "pending" ] && [ -n "$LAST_COMPLETED" ]; then
        # Found first pending phase after a completed one
        NEXT_PHASE="$phase"
        break
    elif [ "$status" = "in_progress" ]; then
        # Phase is in progress, allow stopping (Claude will continue naturally)
        exit 0
    fi
done

# If we found a next phase to do, block stopping
if [ -n "$NEXT_PHASE" ]; then
    echo "{\"decision\": \"block\", \"reason\": \"Phase '$LAST_COMPLETED' completed. Run /compact to clear context and continue with phase: $NEXT_PHASE\"}"
    exit 0
fi

# All phases done or no active translation - allow stop and clean up
rm -f "$MANIFEST_LINK"
exit 0
