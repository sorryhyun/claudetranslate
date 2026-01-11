# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Translate is a multi-stage document translation plugin for Claude Code. It orchestrates a pipeline of specialized agents to analyze, split, summarize, translate, and verify documents using a **file-based workflow** where all intermediate results are persisted to disk.

## Commands

```bash
# Run MCP tools tests
python3 test/test_mcp_tools.py

# Test MCP server directly (JSON-RPC over stdin/stdout)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 -m mcp.mcp
```

## Architecture

### File-Based Workflow

The `/translate` command creates a workspace directory next to the source file:
```
source_translate_temp/
├── manifest.json           # Job state and chunk metadata
├── glossary.json           # Merged terminology glossary (after Phase 3)
├── context/
│   └── context_analysis.md
└── chunks/
    ├── source/             # chunk_001.txt, chunk_002.txt, ...
    ├── summaries/          # summary_001.md, ...
    ├── glossaries/         # glossary_001.json, ... (per-chunk glossaries)
    ├── translations/       # translation_001.md, ...
    └── verifications/      # verification_001.md, ...
```

All agents receive file paths (not text content) and write their output to files. The `manifest.json` tracks job state across all 6 pipeline phases.

### Translation Pipeline (6 Phases)

1. **Setup, Context Analysis, and Text Splitting** - Main agent parses args, inits workspace, spawns `context-analyzer` agent, and splits text via MCP tools
2. **Summarization** - `summarizer` agents write to `chunks/summaries/` and extract terms to `chunks/glossaries/` (parallel, batches of 5)
3. **Glossary Translation** - `glossary-translator` agents translate per-chunk glossaries in parallel, then merge into `glossary.json`
4. **Translation** - `translator` agents read pre-translated `glossary.json` and write to `chunks/translations/` (parallel, batches of 5)
5. **Verification** - `verifier` agents write to `chunks/verifications/` (parallel, optional)
6. **Assembly** - `assemble_translation` MCP tool combines chunks into final output

### MCP Server

The `mcp/` directory contains the MCP server with modular tool loading. Each tool group is a subdirectory with `schema.json` and Python modules exposing `handle(arguments)` functions.

**Tool Groups:**
- `text_split/` - Text chunking (`split_text`, `count_words`, `split_paragraphs`)
- `workspace/` - Workspace management (`init_workspace`, `read_manifest`, `update_manifest`, `update_glossary`, `assemble_translation`)

The server auto-discovers tool groups at startup via `_load_tool_groups()` in `mcp.py`.

### Agent System

Agents in `agents/` are markdown files with YAML frontmatter. All agents have access to `Read` and `Write` tools and work with file paths:

| Agent | Model | Purpose |
|-------|-------|---------|
| `context-analyzer` | sonnet | Document domain/tone/terminology analysis |
| `summarizer` | haiku | Chunk summarization and term extraction |
| `glossary-translator` | haiku | Glossary term translation |
| `translator` | sonnet | Translation execution |
| `verifier` | sonnet | Quality verification |

### Language Styles

Target languages are configured as output-style markdown files in `styles/`:
```
styles/
├── korean.md
├── japanese.md
├── chinese.md
└── ... (19 languages)
```

Each style file uses standard Claude Code output-style format:
```yaml
---
name: Korean
description: Translate to Korean (한국어) - code: ko
---
```

The filename (without `.md`) is the language identifier. Language codes are mapped in `commands/translate.md`.

### Key Files

- `commands/translate.md` - Main orchestration logic (6-phase pipeline)
- `agents/*.md` - 5 specialized agents (context-analyzer, summarizer, glossary-translator, translator, verifier)
- `styles/*.md` - 19 supported language styles with metadata
- `.mcp.json` - MCP server configuration

## Usage

```bash
/translate document.md --target korean
/translate doc.txt --target ja --output doc_ja.txt --skip-verify
```

## Output

- `{basename}_{lang_code}.{ext}` - Translated document
- `{basename}_{lang_code}_report.md` - Quality metrics, glossary, notes
- `{basename}_translate_temp/` - Workspace with all intermediate files (preserved for debugging)
