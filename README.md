# Claude Translate Plugin

A multi-stage document translation pipeline for Claude Code that uses specialized agents to analyze, split, summarize, translate, and verify documents.

## Features

- **Context-Aware Translation**: Analyzes document domain, tone, and terminology before translating
- **Chunk-Based Processing**: Splits large documents into manageable pieces while preserving logical boundaries
- **Cross-Chunk Consistency**: Maintains terminology and style consistency across the entire document
- **Quality Verification**: Optional verification stage to catch errors and inconsistencies
- **Multi-Language Support**: Supports 18+ languages out of the box

## Installation

```bash
# Install the plugin for Claude Code
/plugin install ./claudetranslate
```

## Usage

### Basic Translation

```bash
# Translate a document to Korean
/translate report.md --target korean

# Using language codes
/translate report.md --target ko
```

### With Options

```bash
# Custom output file
/translate docs/guide.txt --target japanese --output docs/guide_ja.txt

# Skip verification for faster processing
/translate article.md --target spanish --skip-verify
```

## Pipeline Stages

1. **Context Analysis** - Understands document domain, tone, terminology, and style
2. **Text Splitting** - Divides document into ~1000-word chunks at logical boundaries
3. **Summarization** - Creates context summaries for each chunk (parallel)
4. **Translation** - Translates each chunk with full context awareness (sequential)
5. **Verification** - Validates translation quality and flags issues (parallel, optional)
6. **Assembly** - Combines chunks and generates translation report

## Supported Languages

| Language | Code | Native Name |
|----------|------|-------------|
| Korean | ko | 한국어 |
| Japanese | ja | 日本語 |
| Chinese (Simplified) | zh | 中文 |
| Chinese (Traditional) | zh-tw | 繁體中文 |
| Spanish | es | Español |
| French | fr | Français |
| German | de | Deutsch |
| Portuguese | pt | Português |
| Russian | ru | Русский |
| Arabic | ar | العربية |
| Hindi | hi | हिन्दी |
| Vietnamese | vi | Tiếng Việt |
| Thai | th | ไทย |
| Indonesian | id | Bahasa Indonesia |
| Italian | it | Italiano |
| Dutch | nl | Nederlands |
| Polish | pl | Polski |
| Turkish | tr | Türkçe |
| English | en | English |

## Plugin Structure

```
claudetranslate/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest
│   ├── servers/
│   │   └── text_splitter_mcp.py # MCP server for text splitting
│   └── utils/
│       └── text_splitter.py     # Text chunking utility
├── styles/
│   ├── korean.md                # Language style files
│   ├── japanese.md
│   └── ... (19 languages)
├── commands/
│   └── translate.md             # /translate slash command
├── agents/
│   ├── context-analyzer.md      # Document analysis agent
│   ├── summarizer.md            # Section summarization agent
│   ├── translator.md            # Translation agent
│   └── verifier.md              # Quality verification agent
├── test/
│   └── sample.md                # Sample document for testing
└── README.md
```

## Output Files

After translation:
- **Translation**: `{basename}_{lang_code}.{ext}` (e.g., `report_ko.md`)
- **Report**: `{basename}_{lang_code}_report.md` with quality metrics, glossary, and notes

## Tips

- **Large Documents**: Documents over 50,000 words may take significant time
- **Technical Content**: The context analyzer identifies technical domains for accurate translation
- **Consistency**: Run full verification on important documents
- **Iterative Improvement**: Re-translate problematic sections if verification flags issues

## License

MIT License
