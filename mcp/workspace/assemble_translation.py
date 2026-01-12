"""Assemble translated chunks into the final output document."""

import json
import os
import re
from typing import Any, Dict, Optional


# Known non-translation sections to exclude (case-insensitive)
NON_TRANSLATION_SECTIONS = [
    'glossary additions',
    'glossary',
    'translation notes',
    'confidence level',
    'transition notes',
    'translation output',
    'revised translation',
    'revision notes',
]


def strip_non_translation_sections(content: str) -> str:
    """Remove known non-translation sections from content as fallback."""
    patterns = [
        r'#{1,6}\s*Glossary Additions?\s*\n.*?(?=\n#{1,6}|\Z)',
        r'#{1,6}\s*Translation Notes?\s*\n.*?(?=\n#{1,6}|\Z)',
        r'#{1,6}\s*Confidence Level\s*\n.*?(?=\n#{1,6}|\Z)',
        r'#{1,6}\s*Transition Notes?\s*\n.*?(?=\n#{1,6}|\Z)',
        r'#{1,6}\s*Translation Output\s*\n',
    ]

    result = content
    for pattern in patterns:
        result = re.sub(pattern, '', result, flags=re.DOTALL | re.IGNORECASE)

    return result.strip()


def extract_translated_text(translation_content: str, file_path: str = "") -> str:
    """Extract the translated text from translation file.

    For .txt files (pure translation): returns the content as-is.
    For .md files (legacy format): extracts the "Translated Text" section.
    """
    # Pure text files (.txt) contain only the translation - return as-is
    if file_path.endswith('.txt'):
        return translation_content.strip()

    # For markdown files, try to extract the "Translated Text" section
    lines = translation_content.split('\n')
    in_translated_section = False
    translated_lines = []
    header_level = None

    for line in lines:
        # Check if this line is a "Translated Text" header (2 or 3 hashes)
        header_match = re.match(r'^(#{2,3})\s*Translated Text\s*$', line, re.IGNORECASE)
        if header_match:
            in_translated_section = True
            header_level = len(header_match.group(1))
            continue

        # Check if we've hit another section header
        if in_translated_section and re.match(r'^#{1,6}\s+', line):
            # Check if it's a known non-translation section
            header_text = re.sub(r'^#{1,6}\s+', '', line).strip().lower()
            if any(section in header_text for section in NON_TRANSLATION_SECTIONS):
                break
            # Also break on any same-or-higher level header
            current_level_match = re.match(r'^(#{1,6})', line)
            if current_level_match:
                current_level = len(current_level_match.group(1))
                if header_level and current_level <= header_level:
                    break

        if in_translated_section:
            translated_lines.append(line)

    if translated_lines:
        return '\n'.join(translated_lines).strip()

    # Last fallback: strip known sections from whole content
    return strip_non_translation_sections(translation_content)


def extract_revised_translation(verification_content: str) -> Optional[str]:
    """Extract revised translation from verification report.

    Returns the revised translation text if present, or None if not available
    or marked as "No revision needed".
    """
    lines = verification_content.split('\n')
    in_revised_section = False
    revised_lines = []

    for line in lines:
        # Check for Revised Translation header (## or ###)
        if re.match(r'^#{2,3}\s*Revised Translation\s*$', line, re.IGNORECASE):
            in_revised_section = True
            continue

        if in_revised_section:
            # Stop at Revision Notes or any other major section
            if re.match(r'^#{1,6}\s+', line):
                header_text = re.sub(r'^#{1,6}\s+', '', line).strip().lower()
                # Stop at any known section header
                if any(section in header_text for section in [
                    'revision notes', 'verification report', 'quality score',
                    'critical issues', 'warnings', 'notes', 'terminology',
                    'tone assessment', 'summary', 'recommended actions'
                ]):
                    break
            revised_lines.append(line)

    result = '\n'.join(revised_lines).strip()

    # Check if it's a "no revision needed" response
    if not result or result.lower() in ['no revision needed', 'no revision needed.']:
        return None

    return result


def get_chunk_path(workspace_dir: str, chunk_type: str, index: int) -> str:
    """Get the path for a chunk file based on type and index.

    Args:
        workspace_dir: The workspace directory path
        chunk_type: One of 'source', 'translation', 'verification', 'summary', 'metadata'
        index: 1-based chunk index
    """
    ext = "txt" if chunk_type in ("source", "translation") else "md"
    if chunk_type == "glossary":
        ext = "json"

    prefix_map = {
        "source": "chunk",
        "translation": "translation",
        "verification": "verification",
        "summary": "summary",
        "metadata": "metadata",
        "glossary": "glossary"
    }
    prefix = prefix_map.get(chunk_type, chunk_type)
    filename = f"{prefix}_{index:03d}.{ext}"

    if chunk_type == "source":
        return os.path.join(workspace_dir, "chunks", "source", filename)
    elif chunk_type == "glossary":
        return os.path.join(workspace_dir, "chunks", "glossaries", filename)
    else:
        folder = f"{chunk_type}s" if not chunk_type.endswith("s") else chunk_type
        return os.path.join(workspace_dir, "chunks", folder, filename)


def handle(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Assemble translated chunks into final output.

    Prioritizes revised translations from verification files when available,
    falling back to original translations otherwise.
    """
    manifest_path = arguments["manifest_path"]
    output_path = arguments["output_path"]

    # Read manifest
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    workspace_dir = os.path.dirname(manifest_path)
    chunk_count = manifest.get("chunk_count", 0)

    if chunk_count == 0:
        raise ValueError("No chunks found in manifest")

    # Collect translated text from each chunk
    translated_parts = []
    revision_count = 0

    for i in range(1, chunk_count + 1):
        translated_text = None

        # First, check if revision exists in verification file
        verification_path = get_chunk_path(workspace_dir, "verification", i)
        if os.path.exists(verification_path):
            with open(verification_path, "r", encoding="utf-8") as f:
                verification_content = f.read()
            revised = extract_revised_translation(verification_content)
            if revised:
                translated_text = revised
                revision_count += 1

        # Fall back to original translation
        if not translated_text:
            translation_path = get_chunk_path(workspace_dir, "translation", i)
            if not os.path.exists(translation_path):
                raise ValueError(f"Translation file not found: {translation_path}")

            with open(translation_path, "r", encoding="utf-8") as f:
                translation_content = f.read()

            translated_text = extract_translated_text(translation_content, translation_path)

        translated_parts.append(translated_text)

    # Join with double newlines
    final_translation = "\n\n".join(translated_parts)

    # Write output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_translation)

    # Count words in output
    output_word_count = len(final_translation.split())

    return {
        "success": True,
        "output_path": output_path,
        "chunk_count": chunk_count,
        "output_word_count": output_word_count,
        "revisions_applied": revision_count
    }
