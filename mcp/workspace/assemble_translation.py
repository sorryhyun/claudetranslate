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


def extract_translated_text(translation_content: str) -> str:
    """Extract the translated text section from the translation markdown.

    Handles both ## and ### header levels, and stops at known non-translation
    sections like Glossary, Notes, Confidence, etc.
    """
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
    chunks = manifest["chunks"]

    if not chunks:
        raise ValueError("No chunks found in manifest")

    # Sort chunks by index
    chunks_sorted = sorted(chunks, key=lambda c: c["index"])

    # Collect translated text from each chunk
    translated_parts = []
    revision_count = 0

    for chunk in chunks_sorted:
        translated_text = None

        # First, check if revision exists in verification file
        if chunk.get("revision_applied", False):
            verification_file = chunk.get("verification_file")
            if verification_file:
                verification_path = os.path.join(workspace_dir, verification_file)
                if os.path.exists(verification_path):
                    with open(verification_path, "r", encoding="utf-8") as f:
                        verification_content = f.read()
                    translated_text = extract_revised_translation(verification_content)
                    if translated_text:
                        revision_count += 1

        # Fall back to original translation
        if not translated_text:
            translation_file = chunk.get("translation_file")
            if not translation_file:
                raise ValueError(f"No translation file for chunk {chunk['index']}")

            translation_path = os.path.join(workspace_dir, translation_file)
            if not os.path.exists(translation_path):
                raise ValueError(f"Translation file not found: {translation_path}")

            with open(translation_path, "r", encoding="utf-8") as f:
                translation_content = f.read()

            translated_text = extract_translated_text(translation_content)

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
        "chunk_count": len(chunks_sorted),
        "output_word_count": output_word_count,
        "revisions_applied": revision_count
    }
