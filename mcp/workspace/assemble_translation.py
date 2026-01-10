"""Assemble translated chunks into the final output document."""

import json
import os
import re
from typing import Any, Dict


def extract_translated_text(translation_content: str) -> str:
    """Extract the translated text section from the translation markdown."""
    # Look for the "### Translated Text" section
    pattern = r'###\s*Translated Text\s*\n(.*?)(?=\n###|\Z)'
    match = re.search(pattern, translation_content, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    # Fallback: if no section header, try to find content between first header and next
    # This handles cases where the format might vary
    lines = translation_content.split('\n')
    in_translated_section = False
    translated_lines = []

    for line in lines:
        if re.match(r'^###\s*Translated Text', line, re.IGNORECASE):
            in_translated_section = True
            continue
        elif re.match(r'^###', line):
            if in_translated_section:
                break
        elif in_translated_section:
            translated_lines.append(line)

    if translated_lines:
        return '\n'.join(translated_lines).strip()

    # Last fallback: return the whole content
    return translation_content.strip()


def handle(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Assemble translated chunks into final output."""
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
    for chunk in chunks_sorted:
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
        "output_word_count": output_word_count
    }
