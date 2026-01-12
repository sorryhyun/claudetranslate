"""Merge per-chunk glossaries into the main glossary.json."""

import json
import os
from typing import Any, Dict, List


def handle(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Merge all chunk glossaries into the main glossary.

    Reads glossary files from chunks/glossaries/, deduplicates terms
    (keeping first occurrence), and writes to the main glossary.json.
    """
    manifest_path = arguments["manifest_path"]

    # Validate manifest exists
    if not os.path.isfile(manifest_path):
        raise ValueError(f"Manifest not found: {manifest_path}")

    workspace_dir = os.path.dirname(manifest_path)
    glossaries_dir = os.path.join(workspace_dir, "chunks", "glossaries")
    main_glossary_path = os.path.join(workspace_dir, "glossary.json")

    # Read main glossary for metadata
    with open(main_glossary_path, "r", encoding="utf-8") as f:
        main_glossary = json.load(f)

    # Collect all chunk glossary files
    if not os.path.isdir(glossaries_dir):
        raise ValueError(f"Glossaries directory not found: {glossaries_dir}")

    glossary_files = sorted([
        f for f in os.listdir(glossaries_dir)
        if f.startswith("glossary_") and f.endswith(".json")
    ])

    if not glossary_files:
        return {
            "success": True,
            "terms_merged": 0,
            "duplicates_removed": 0,
            "chunk_glossaries_processed": 0,
            "glossary_path": main_glossary_path
        }

    # Merge terms from all chunk glossaries
    seen_sources: Dict[str, Dict[str, Any]] = {}  # source -> term object
    total_terms = 0
    duplicates = 0

    for glossary_file in glossary_files:
        glossary_path = os.path.join(glossaries_dir, glossary_file)

        try:
            with open(glossary_path, "r", encoding="utf-8") as f:
                chunk_glossary = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Skip invalid or missing files
            continue

        # Handle both array format and object-with-terms format
        terms = chunk_glossary if isinstance(chunk_glossary, list) else chunk_glossary.get("terms", [])

        for term in terms:
            if not isinstance(term, dict):
                continue

            source = term.get("source", "").strip()
            if not source:
                continue

            total_terms += 1

            # Normalize source for deduplication (case-insensitive)
            source_key = source.lower()

            if source_key in seen_sources:
                duplicates += 1
            else:
                seen_sources[source_key] = term

    # Build merged terms list
    merged_terms: List[Dict[str, Any]] = list(seen_sources.values())

    # Sort by source term for consistency
    merged_terms.sort(key=lambda t: t.get("source", "").lower())

    # Update main glossary
    main_glossary["terms"] = merged_terms

    with open(main_glossary_path, "w", encoding="utf-8") as f:
        json.dump(main_glossary, f, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "terms_merged": len(merged_terms),
        "duplicates_removed": duplicates,
        "total_terms_processed": total_terms,
        "chunk_glossaries_processed": len(glossary_files),
        "glossary_path": main_glossary_path
    }
