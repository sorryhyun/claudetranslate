"""Initialize translation workspace directory structure."""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict


def handle(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Create workspace directory and initial manifest."""
    source_file_path = arguments["source_file_path"]
    target_language = arguments["target_language"]
    target_language_code = arguments["target_language_code"]
    output_path = arguments.get("output_path")
    skip_verify = arguments.get("skip_verify", False)

    # Validate source file exists
    if not os.path.isfile(source_file_path):
        raise ValueError(f"Source file not found: {source_file_path}")

    # Create workspace directory next to source file
    source_dir = os.path.dirname(os.path.abspath(source_file_path))
    source_basename = os.path.splitext(os.path.basename(source_file_path))[0]
    source_ext = os.path.splitext(source_file_path)[1]

    workspace_dir = os.path.join(source_dir, f"{source_basename}_translate_temp")

    # Create directory structure
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs(os.path.join(workspace_dir, "context"), exist_ok=True)
    os.makedirs(os.path.join(workspace_dir, "chunks", "source"), exist_ok=True)
    os.makedirs(os.path.join(workspace_dir, "chunks", "summaries"), exist_ok=True)
    os.makedirs(os.path.join(workspace_dir, "chunks", "glossaries"), exist_ok=True)
    os.makedirs(os.path.join(workspace_dir, "chunks", "translations"), exist_ok=True)
    os.makedirs(os.path.join(workspace_dir, "chunks", "metadata"), exist_ok=True)
    os.makedirs(os.path.join(workspace_dir, "chunks", "verifications"), exist_ok=True)

    # Determine output path
    if not output_path:
        output_path = os.path.join(
            source_dir,
            f"{source_basename}_{target_language_code}{source_ext}"
        )

    # Count words in source file
    with open(source_file_path, "r", encoding="utf-8") as f:
        source_content = f.read()
    word_count = len(source_content.split())

    # Create initial manifest
    now = datetime.now(timezone.utc).isoformat()
    manifest = {
        "version": "2.0",
        "created_at": now,
        "updated_at": now,
        "source": {
            "file_path": os.path.abspath(source_file_path),
            "word_count": word_count
        },
        "target": {
            "language": target_language,
            "code": target_language_code,
            "output_path": os.path.abspath(output_path)
        },
        "options": {
            "skip_verify": skip_verify
        },
        "phases": {
            "input_validation": {"status": "completed", "completed_at": now},
            "context_analysis": {"status": "pending"},
            "text_splitting": {"status": "pending"},
            "summarization": {"status": "pending"},
            "glossary_translation": {"status": "pending"},
            "translation": {"status": "pending"},
            "verification": {"status": "pending" if not skip_verify else "skipped"},
            "assembly": {"status": "pending"}
        },
        "chunk_count": 0
    }

    manifest_path = os.path.join(workspace_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Create empty glossary
    glossary = {
        "version": "1.0",
        "target_language": target_language,
        "target_language_code": target_language_code,
        "terms": []
    }
    glossary_path = os.path.join(workspace_dir, "glossary.json")
    with open(glossary_path, "w", encoding="utf-8") as f:
        json.dump(glossary, f, indent=2, ensure_ascii=False)

    return {
        "workspace_dir": workspace_dir,
        "manifest_path": manifest_path,
        "glossary_path": glossary_path,
        "output_path": output_path,
        "source_word_count": word_count
    }
