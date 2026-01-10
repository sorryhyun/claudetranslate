"""Read the translation manifest."""

import json
from typing import Any, Dict


def handle(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Read and return the manifest data."""
    manifest_path = arguments["manifest_path"]

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    return manifest
