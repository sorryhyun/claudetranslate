"""Paragraph splitting with metadata."""

import re
from typing import Any, Dict, List

from .count_words import count_words


def split_into_paragraphs(text: str) -> List[Dict[str, Any]]:
    """Split text into paragraphs with metadata."""
    paragraphs = []
    current_pos = 0

    para_pattern = re.compile(r'\n\s*\n')
    parts = para_pattern.split(text)

    for i, part in enumerate(parts):
        part = part.strip()
        if part:
            start_pos = text.find(part, current_pos)
            paragraphs.append({
                'index': i,
                'text': part,
                'word_count': count_words(part),
                'start_pos': start_pos
            })
            current_pos = start_pos + len(part)

    return paragraphs


def handle(arguments: dict) -> list:
    """MCP tool handler."""
    text = arguments.get("text")
    file_path = arguments.get("file_path")

    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif text is None:
        text = ""

    return split_into_paragraphs(text)
