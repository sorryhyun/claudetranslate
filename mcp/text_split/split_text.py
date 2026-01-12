"""Main text chunking logic with file-based I/O."""

import json
import os
import re
from typing import Any, Dict, List

from .count_words import count_words
from .split_paragraphs import split_into_paragraphs


def find_section_headers(text: str) -> List[Dict[str, Any]]:
    """Find markdown-style headers in text."""
    headers = []
    lines = text.split('\n')
    char_pos = 0

    for i, line in enumerate(lines):
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            headers.append({
                'level': len(match.group(1)),
                'text': match.group(2),
                'line': i,
                'char_pos': char_pos
            })
        char_pos += len(line) + 1

    return headers


def split_paragraph_into_sentences(text: str) -> List[str]:
    """Split a paragraph into sentences."""
    sentence_pattern = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
    return sentence_pattern.split(text)


def create_chunks(
    text: str,
    target_words: int = 2000,
    min_words: int = 1500,
    max_words: int = 2500
) -> List[Dict[str, Any]]:
    """
    Split text into chunks of approximately target_words size.

    Respects paragraph boundaries where possible.
    Falls back to sentence boundaries for very long paragraphs.
    """
    paragraphs = split_into_paragraphs(text)
    headers = find_section_headers(text)
    chunks = []
    current_chunk = {
        'index': 0,
        'paragraphs': [],
        'text': '',
        'word_count': 0,
        'start_pos': 0,
        'headers': []
    }

    for para in paragraphs:
        para_words = para['word_count']

        if current_chunk['word_count'] + para_words > max_words and current_chunk['word_count'] >= min_words:
            current_chunk['text'] = '\n\n'.join(p['text'] for p in current_chunk['paragraphs'])
            current_chunk['end_pos'] = para['start_pos']
            chunks.append(current_chunk)

            current_chunk = {
                'index': len(chunks),
                'paragraphs': [],
                'text': '',
                'word_count': 0,
                'start_pos': para['start_pos'],
                'headers': []
            }

        if para_words > max_words:
            sentences = split_paragraph_into_sentences(para['text'])
            sentence_buffer = []
            sentence_words = 0

            for sentence in sentences:
                s_words = count_words(sentence)
                if sentence_words + s_words > max_words and sentence_words >= min_words:
                    para_text = ' '.join(sentence_buffer)
                    current_chunk['paragraphs'].append({
                        'text': para_text,
                        'word_count': sentence_words
                    })
                    current_chunk['word_count'] += sentence_words
                    current_chunk['text'] = '\n\n'.join(p['text'] for p in current_chunk['paragraphs'])
                    current_chunk['end_pos'] = para['start_pos'] + len(para_text)
                    chunks.append(current_chunk)

                    current_chunk = {
                        'index': len(chunks),
                        'paragraphs': [],
                        'text': '',
                        'word_count': 0,
                        'start_pos': para['start_pos'],
                        'headers': []
                    }
                    sentence_buffer = []
                    sentence_words = 0

                sentence_buffer.append(sentence)
                sentence_words += s_words

            if sentence_buffer:
                para_text = ' '.join(sentence_buffer)
                current_chunk['paragraphs'].append({
                    'text': para_text,
                    'word_count': sentence_words
                })
                current_chunk['word_count'] += sentence_words
        else:
            current_chunk['paragraphs'].append(para)
            current_chunk['word_count'] += para_words

        if current_chunk['word_count'] >= target_words:
            current_chunk['text'] = '\n\n'.join(p['text'] for p in current_chunk['paragraphs'])
            current_chunk['end_pos'] = para['start_pos'] + len(para['text'])
            chunks.append(current_chunk)

            current_chunk = {
                'index': len(chunks),
                'paragraphs': [],
                'text': '',
                'word_count': 0,
                'start_pos': current_chunk['end_pos'],
                'headers': []
            }

    if current_chunk['paragraphs']:
        current_chunk['text'] = '\n\n'.join(p['text'] for p in current_chunk['paragraphs'])
        current_chunk['end_pos'] = len(text)
        chunks.append(current_chunk)

    for header in headers:
        for chunk in chunks:
            if chunk['start_pos'] <= header['char_pos'] < chunk.get('end_pos', len(text)):
                chunk['headers'].append(header['text'])
                break

    result = []
    for chunk in chunks:
        result.append({
            'index': chunk['index'],
            'text': chunk['text'],
            'word_count': chunk['word_count'],
            'start_pos': chunk['start_pos'],
            'end_pos': chunk.get('end_pos', len(text)),
            'headers': chunk['headers']
        })

    return result


def handle(arguments: dict) -> dict:
    """MCP tool handler for file-based splitting."""
    source_file_path = arguments.get("source_file_path")
    output_dir = arguments.get("output_dir")

    if not source_file_path or not output_dir:
        raise ValueError("source_file_path and output_dir are required")

    # Read source file
    with open(source_file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Create chunks
    chunks = create_chunks(
        text,
        target_words=arguments.get("target_words", 1000),
        min_words=arguments.get("min_words", 500),
        max_words=arguments.get("max_words", 1500)
    )

    total_words = count_words(text)

    # Ensure chunks directory exists
    chunks_dir = os.path.join(output_dir, "chunks", "source")
    os.makedirs(chunks_dir, exist_ok=True)

    # Write individual chunk files
    for chunk in chunks:
        # Use 1-based index for filenames
        chunk_index = chunk['index'] + 1
        chunk_filename = f"chunk_{chunk_index:03d}.txt"
        chunk_path = os.path.join(chunks_dir, chunk_filename)

        # Write chunk text to file
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk['text'])

    # Update manifest.json with chunk count
    manifest_path = os.path.join(output_dir, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        manifest["chunk_count"] = len(chunks)
        manifest["source"]["word_count"] = total_words

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    return {
        "manifest_path": manifest_path,
        "chunks_dir": chunks_dir,
        "chunk_count": len(chunks),
        "total_words": total_words,
        "chunk_files": [f"chunk_{i+1:03d}.txt" for i in range(len(chunks))]
    }
