"""PDF to text extraction tool."""

import os
import re
from typing import Optional


def _is_structural_line(line: str) -> bool:
    """Check if line is a structural element (header, list, table, etc.)."""
    if not line.strip():
        return True
    return bool(
        re.match(r'^#+\s', line)  # Markdown header
        or re.match(r'^\*\*\d+\*\*', line)  # TOC entry like **1**
        or re.match(r'^[-*+]\s', line)  # List item
        or re.match(r'^\d+\.\s', line)  # Numbered list
        or line.startswith('|')  # Table
        or line.startswith('[')  # Link/reference
        or re.match(r'^Figure \d+', line)  # Figure caption
        or re.match(r'^Table \d+', line)  # Table caption
    )


def _should_join_lines(current: str, next_line: str) -> bool:
    """Determine if two lines should be joined."""
    if not next_line:
        return False

    # Don't join if next line is structural
    if _is_structural_line(next_line):
        return False

    # Join if current ends with comma/semicolon
    if re.search(r'[,;]\s*$', current):
        return True

    # Join if current doesn't end with sentence punctuation and next starts lowercase
    if not re.search(r'[.!?:]\s*$', current) and next_line[0].islower():
        return True

    # Join if next line starts with opening bracket (continuation)
    if next_line[0] in '({[':
        return True

    return False


def postprocess_text(text: str) -> str:
    """Clean up extracted PDF text.

    Handles:
    - Joins lines broken mid-sentence (including multiple consecutive lines)
    - Removes empty/garbage markdown tables
    - Collapses excessive blank lines
    - Fixes hyphenated word breaks
    """
    lines = text.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty markdown tables (common from figure extraction)
        # Pattern: |Col1|Col2|... followed by |---|---| and garbage rows
        if re.match(r'^\|Col\d+\|', line):
            while i < len(lines) and (
                lines[i].startswith('|') or lines[i].strip() == ''
            ):
                i += 1
            continue

        # Handle hyphenated line breaks: "word-\n" + "continuation"
        if line.rstrip().endswith('-') and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line and next_line[0].islower():
                line = line.rstrip()[:-1] + next_line
                i += 2
                # Continue to potentially join more lines
                while i < len(lines):
                    next_line = lines[i].strip()
                    if _should_join_lines(line, next_line):
                        line = line.rstrip() + ' ' + next_line
                        i += 1
                    else:
                        break
                result.append(line)
                continue

        # Skip structural lines without modification
        if _is_structural_line(line):
            result.append(line)
            i += 1
            continue

        # Accumulate lines that should be joined
        accumulated = line
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if _should_join_lines(accumulated, next_line):
                accumulated = accumulated.rstrip() + ' ' + next_line
                i += 1
            else:
                break

        result.append(accumulated)

    text = '\n'.join(result)

    # Collapse multiple blank lines to max 2
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Remove lines that are just whitespace
    text = re.sub(r'\n[ \t]+\n', '\n\n', text)

    return text.strip()


def extract_text_pymupdf(pdf_path: str, pages: Optional[list] = None) -> tuple[str, int]:
    """Extract text using PyMuPDF (recommended).

    Returns:
        Tuple of (extracted_text, page_count)
    """
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    page_count = len(doc)
    text_parts = []

    page_indices = pages if pages is not None else range(page_count)
    for page_num in page_indices:
        if 0 <= page_num < page_count:
            page = doc[page_num]
            text_parts.append(page.get_text())

    doc.close()
    return "\n\n".join(text_parts), page_count


def extract_text_pymupdf4llm(pdf_path: str, pages: Optional[list] = None) -> tuple[str, int]:
    """Extract text as markdown using pymupdf4llm.

    Returns:
        Tuple of (extracted_markdown, page_count)
    """
    import fitz
    import pymupdf4llm

    # Get page count
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    doc.close()

    # Extract as markdown
    md_text = pymupdf4llm.to_markdown(pdf_path, pages=pages)

    # Ensure we return a string (pymupdf4llm may return list in some modes)
    if isinstance(md_text, list):
        md_text = "\n\n".join(str(item) for item in md_text)

    return str(md_text), page_count


def extract_text_pypdf(pdf_path: str, pages: Optional[list] = None) -> tuple[str, int]:
    """Extract text using pypdf (fallback).

    Returns:
        Tuple of (extracted_text, page_count)
    """
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    page_count = len(reader.pages)
    text_parts = []

    page_indices = pages if pages is not None else range(page_count)
    for page_num in page_indices:
        if 0 <= page_num < page_count:
            text_parts.append(reader.pages[page_num].extract_text() or "")

    return "\n\n".join(text_parts), page_count


def detect_math_issues(text: str) -> list[str]:
    """Detect potential math/formula extraction issues.

    Returns list of warning messages.
    """
    warnings = []

    # Detect broken subscript patterns (common in academic PDFs)
    broken_subscript = re.findall(r'[a-zA-Z][!@#$%^&*()]+', text)
    if len(broken_subscript) > 5:
        warnings.append(
            "Detected potential broken math subscripts/superscripts. "
            "PDF may use custom fonts for mathematical notation."
        )

    # Detect Unicode math symbols that might be garbled
    garbled_patterns = re.findall(r'[\uf000-\uf8ff]', text)  # Private Use Area
    if garbled_patterns:
        warnings.append(
            f"Found {len(garbled_patterns)} characters from Unicode Private Use Area. "
            "These may be custom glyphs that didn't convert properly."
        )

    # Check for common LaTeX-like fragments that suggest equations
    latex_hints = re.findall(r'\\[a-zA-Z]+|[∑∏∫∂∇]|[αβγδεζηθλμνξπρστφχψω]', text)
    if latex_hints and len(broken_subscript) > 3:
        warnings.append(
            "Document appears to contain mathematical equations. "
            "Consider using OCR-based tools for better equation extraction."
        )

    return warnings


def handle(arguments: dict) -> dict:
    """MCP tool handler for PDF to text conversion.

    Args:
        arguments: Dict with:
            - pdf_path: Path to input PDF file
            - output_path: Optional path to write text output
            - format: 'text' (default) or 'markdown'
            - pages: Optional list of page numbers (0-indexed)

    Returns:
        Dict with:
            - text: Extracted text content
            - output_path: Path where text was written (if output_path provided)
            - page_count: Number of pages in document
            - pages_extracted: Number of pages actually extracted
            - word_count: Approximate word count
            - warnings: List of any extraction warnings
    """
    pdf_path = arguments.get("pdf_path")
    output_path = arguments.get("output_path")
    output_format = arguments.get("format", "text")
    pages = arguments.get("pages")

    if not pdf_path:
        raise ValueError("pdf_path is required")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    warnings = []

    # Extract based on format
    if output_format == "markdown":
        try:
            text, page_count = extract_text_pymupdf4llm(pdf_path, pages)
        except ImportError:
            warnings.append("pymupdf4llm not installed, falling back to plain text")
            text, page_count = extract_text_pymupdf(pdf_path, pages)
    else:
        # Plain text extraction
        try:
            text, page_count = extract_text_pymupdf(pdf_path, pages)
        except ImportError:
            try:
                text, page_count = extract_text_pypdf(pdf_path, pages)
            except ImportError:
                raise ImportError(
                    "No PDF library available. Install one of: "
                    "pip install pymupdf OR pip install pypdf"
                )

    # Clean up common PDF artifacts
    text = text.replace("\x00", "")  # null bytes

    # Post-process: fix line breaks, remove garbage tables, etc.
    text = postprocess_text(text)

    # Detect potential issues
    extraction_warnings = detect_math_issues(text)
    warnings.extend(extraction_warnings)

    # Calculate pages extracted
    pages_extracted = len(pages) if pages else page_count

    # Write output if requested
    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
            # Append warnings as comments if any
            if warnings:
                f.write("\n\n<!-- Extraction Warnings:\n")
                for w in warnings:
                    f.write(f"  - {w}\n")
                f.write("-->\n")

    result = {
        "text": text if not output_path else f"[Written to {output_path}]",
        "page_count": page_count,
        "pages_extracted": pages_extracted,
        "word_count": len(text.split()),
        "char_count": len(text),
        "format": output_format,
    }

    if output_path:
        result["output_path"] = output_path

    if warnings:
        result["warnings"] = warnings

    return result
