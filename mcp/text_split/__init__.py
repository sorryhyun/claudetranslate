"""Text splitting tools for MCP."""

from . import count_words, split_paragraphs, split_text

# Tool name -> module mapping
TOOLS = {
    "count_words": count_words,
    "split_paragraphs": split_paragraphs,
    "split_text": split_text,
}
