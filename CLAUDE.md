# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Translate is a multi-stage document translation plugin for Claude Code. It orchestrates a pipeline of specialized agents to analyze, split, summarize, translate, and verify documents.

## Architecture

### Translation Pipeline (7 Phases)

The `/translate` command executes sequentially:
1. **Input Validation** - Parse args, validate file/language, load config
2. **Context Analysis** - `context-analyzer` agent extracts domain, tone, terminology
3. **Text Splitting** - MCP tool splits into ~1000-word chunks at logical boundaries
4. **Summarization** - `summarizer` agents process chunks (parallel, batches of 5)
5. **Translation** - `translator` agents translate chunks (sequential for consistency)
6. **Verification** - `verifier` agents validate quality (parallel, optional)
7. **Assembly** - Combine chunks, generate translation report

### Agent System

Agents are defined in `agents/` as markdown files with YAML frontmatter:
- `context-analyzer.md` - Document analysis (model: sonnet)
- `summarizer.md` - Chunk summarization (model: haiku)
- `translator.md` - Translation execution (model: sonnet)
- `verifier.md` - Quality verification (model: sonnet)

### MCP Server

The `mcp/` directory contains the MCP server with modular tool loading:

```
mcp/
  mcp.py              # Main server with dynamic tool discovery
  text_split/         # Text splitting tool group
    __init__.py       # Exports TOOLS mapping
    schema.json       # Tool definitions
    count_words.py    # Word count utility
    split_text.py     # Main chunking logic
    split_paragraphs.py # Paragraph extraction
```

Each tool group is a subdirectory with `schema.json` and Python modules exposing `handle(arguments)` functions. The server auto-discovers groups at startup.

### Key Files

- `commands/translate.md` - Main orchestration logic and CLI interface
- `.claude-plugin/config/languages.json` - 19 supported languages with aliases
- `.mcp.json` - MCP server configuration

## Usage

```bash
# Basic translation
/translate document.md --target korean

# With options
/translate doc.txt --target ja --output doc_ja.txt --skip-verify
```

## Output

- `{basename}_{lang_code}.{ext}` - Translated document
- `{basename}_{lang_code}_report.md` - Quality metrics, glossary, notes
