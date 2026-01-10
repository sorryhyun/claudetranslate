"""Word counting utility."""


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def handle(arguments: dict) -> dict:
    """MCP tool handler."""
    text = arguments.get("text")
    file_path = arguments.get("file_path")

    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif text is None:
        text = ""

    return {"word_count": count_words(text)}
