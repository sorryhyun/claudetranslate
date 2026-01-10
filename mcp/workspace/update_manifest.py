"""Update the translation manifest."""

import json
from datetime import datetime, timezone
from typing import Any, Dict


def handle(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Update manifest with phase progress or chunk status."""
    manifest_path = arguments["manifest_path"]
    phase = arguments.get("phase")
    phase_status = arguments.get("phase_status")
    phase_progress = arguments.get("phase_progress")
    chunk_index = arguments.get("chunk_index")
    chunk_updates = arguments.get("chunk_updates")

    # Read current manifest
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    now = datetime.now(timezone.utc).isoformat()
    manifest["updated_at"] = now

    # Update phase status
    if phase and phase_status:
        if phase in manifest["phases"]:
            manifest["phases"][phase]["status"] = phase_status
            if phase_status == "completed":
                manifest["phases"][phase]["completed_at"] = now
            if phase_progress:
                manifest["phases"][phase]["progress"] = phase_progress

    # Update chunk
    if chunk_index is not None and chunk_updates:
        # Find chunk by index (1-based)
        for chunk in manifest["chunks"]:
            if chunk["index"] == chunk_index:
                chunk.update(chunk_updates)
                break

    # Write updated manifest
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "manifest_path": manifest_path,
        "updated_at": now
    }
