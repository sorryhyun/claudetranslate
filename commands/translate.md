---
description: Translate documents through a multi-stage pipeline with context analysis, chunking, summarization, translation, and verification
argument-hint: <source-file> --target <language> [--output <file>] [--skip-verify]
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "TodoWrite", "Task"]
hooks:
  PostToolUse:
    - matcher: "mcp__.*__init_workspace"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/apply_output_style.sh"
          timeout: 5
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/phase_check.sh"
          timeout: 5
---

# Document Translation Pipeline

You are orchestrating a multi-stage translation pipeline using a **file-based workflow**. All intermediate results are saved to a workspace directory next to the source file for debugging and transparency.

## Arguments

Source file and options: $ARGUMENTS

## File-Based Architecture

This pipeline creates a workspace directory next to the source file:
```
source_translate_temp/
├── manifest.json           # Job state and chunk metadata
├── glossary.json           # Merged terminology glossary (after Phase 3)
├── context/
│   └── context_analysis.md
└── chunks/
    ├── source/             # chunk_001.txt, chunk_002.txt, ...
    ├── summaries/          # summary_001.md, summary_002.md, ...
    ├── glossaries/         # glossary_001.json, glossary_002.json, ...
    ├── translations/       # translation_001.md, translation_002.md, ...
    └── verifications/      # verification_001.md, verification_002.md, ...
```

## Pipeline Phases

Execute each phase in order. Use TodoWrite to track progress through all 6 phases.

---

### Phase 1: Setup, Context Analysis, and Text Splitting

**Goal:** Validate inputs, initialize workspace, analyze document context, and split into chunks

**Actions:**

1. Create a todo list with all 6 phases using TodoWrite

2. Parse arguments to extract:
   - **Source file path** (required, first positional argument)
   - **Target language** via `--target` (required)
   - **Output file** via `--output` (optional)
   - **Skip verification** flag via `--skip-verify` (optional, default: false)

3. Validate source file:
   - Use Read tool to verify file exists and is readable
   - If file not found, report error and suggest checking the path

4. Validate target language:
   - Use Glob to list all style files in `${CLAUDE_PLUGIN_ROOT}/styles/*.md`
   - Match the target language against file names (without .md extension) or language codes
   - If not supported, list available languages and exit
   - Use the language code mapping below to get the ISO code:

   **Language Code Mapping:**
   | Filename | Code |
   |----------|------|
   | korean | ko |
   | japanese | ja |
   | chinese | zh |
   | chinese-traditional | zh-TW |
   | spanish | es |
   | french | fr |
   | german | de |
   | portuguese | pt |
   | russian | ru |
   | arabic | ar |
   | hindi | hi |
   | vietnamese | vi |
   | thai | th |
   | indonesian | id |
   | italian | it |
   | dutch | nl |
   | polish | pl |
   | turkish | tr |
   | english | en |

   - Also accept language codes directly (e.g., `ko` → `korean`)

5. Initialize the workspace using the **init_workspace MCP tool** `mcp__plugin_claude-translate_translator__init_workspace`:
   - `source_file_path`: Absolute path to source file
   - `target_language`: Full language name (e.g., "korean")
   - `target_language_code`: ISO code (e.g., "ko")
   - `output_path`: Custom output path if provided via `--output`
   - `skip_verify`: True if `--skip-verify` was passed

   The tool returns:
   - `workspace_dir`: Path to the created workspace directory
   - `manifest_path`: Path to manifest.json
   - `glossary_path`: Path to glossary.json
   - `output_path`: Where the final translation will be written
   - `source_word_count`: Word count of source document

6. Store the workspace paths for subsequent phases

7. Create symlink for Stop hook to track manifest:
   ```bash
   ln -sf "[manifest_path]" /tmp/claude_translate_manifest.json
   ```
   Replace `[manifest_path]` with the actual manifest path from step 5.

8. **Context Analysis** - Launch the context-analyzer agent:

   Update manifest phase status to "in_progress" for context_analysis.

   Launch the **context-analyzer** agent using the Task tool:
   ```
   Analyze this document for translation context.

   source_file_path: [source file path]
   output_file_path: [workspace_dir]/context/context_analysis.md

   Target language: [target language]

   Read the source document and write your analysis to the output file.
   ```

   Update manifest to mark context_analysis phase as completed.

9. **Text Splitting** - Split document into chunks:

    Update manifest phase status to "in_progress" for text_splitting.

    Use the **split_text MCP tool** `mcp__plugin_claude-translate_translator__split_text`:
    - `source_file_path`: Path to source document
    - `output_dir`: Path to workspace directory
    - `target_words`: 2000
    - `min_words`: 1500
    - `max_words`: 2500

    The tool:
    - Creates individual chunk files: `chunks/source/chunk_001.txt`, etc.
    - Updates `manifest.json` with chunk metadata
    - Returns: `manifest_path`, `chunk_count`, `total_words`, `chunk_files`

    Update manifest to mark text_splitting phase as completed.

10. Mark Phase 1 as complete in todo list

---

### Phase 2: Summarization

**Goal:** Create summaries for each chunk to maintain context across translations

**Actions:**

1. Mark Phase 2 as in_progress

2. Update manifest phase status to "in_progress" for summarization

3. Read the manifest to get the chunk list using **read_manifest MCP tool** `mcp__plugin_claude-translate_translator__read_manifest`

4. For each chunk, launch the **summarizer** agent using the Task tool with file paths:
   ```
   Create a summary for translation context and extract glossary terms.

   chunk_file_path: [workspace_dir]/chunks/source/chunk_[NNN].txt
   context_file_path: [workspace_dir]/context/context_analysis.md
   previous_summary_path: [workspace_dir]/chunks/summaries/summary_[NNN-1].md (or "none" for first chunk)
   output_file_path: [workspace_dir]/chunks/summaries/summary_[NNN].md
   glossary_output_path: [workspace_dir]/chunks/glossaries/glossary_[NNN].json

   Chunk index: [index] of [total]

   Read the input files, write your summary to the output file, and write extracted glossary terms to the glossary output file.
   ```

5. **Parallelization:** Launch up to 5 summarizer agents in parallel for efficiency. Wait for each batch to complete before launching the next batch.

6. After each batch, update manifest with chunk summary status and glossary status using update_manifest

7. Update manifest to mark summarization phase as completed

8. Mark Phase 2 as complete

---

### Phase 3: Glossary Translation

**Goal:** Translate all glossary terms before translation phase to enable parallel translation

**Actions:**

1. Mark Phase 3 as in_progress

2. Update manifest phase status to "in_progress" for glossary_translation

3. Read the manifest to get the chunk list

4. For each chunk, launch the **glossary-translator** agent using the Task tool with file paths:
   ```
   Translate the glossary terms for this chunk.

   glossary_file_path: [workspace_dir]/chunks/glossaries/glossary_[NNN].json
   context_file_path: [workspace_dir]/context/context_analysis.md
   target_language: [target language]

   Read the glossary JSON file and context, translate all terms, and write the updated glossary back to the same file.
   ```

5. **Parallelization:** Launch ALL glossary-translator agents in parallel since they are independent of each other.

6. After all glossary translations complete, merge all chunk glossaries into the main glossary.json:
   - Read each `chunks/glossaries/glossary_[NNN].json` file
   - Collect all translated terms
   - Deduplicate terms (keep first occurrence if duplicates exist)
   - Use **update_glossary MCP tool** `mcp__plugin_claude-translate_translator__update_glossary` to add all terms to the main glossary:
     - `glossary_path`: Path to glossary.json
     - `terms`: Array of all translated term objects

7. Update manifest with glossary status for each chunk

8. Update manifest to mark glossary_translation phase as completed

9. Mark Phase 3 as complete

---

### Phase 4: Translation

**Goal:** Translate each chunk using context, summaries, and pre-translated glossary

**Actions:**

1. Mark Phase 4 as in_progress

2. Update manifest phase status to "in_progress" for translation

3. For each chunk, launch the **translator** agent using the Task tool with file paths:
   ```
   Translate this text chunk to [target language].

   chunk_file_path: [workspace_dir]/chunks/source/chunk_[NNN].txt
   context_file_path: [workspace_dir]/context/context_analysis.md
   summary_file_path: [workspace_dir]/chunks/summaries/summary_[NNN].md
   prev_summary_path: [workspace_dir]/chunks/summaries/summary_[NNN-1].md (or "none" for first chunk)
   next_summary_path: [workspace_dir]/chunks/summaries/summary_[NNN+1].md (or "none" for last chunk)
   glossary_file_path: [workspace_dir]/glossary.json
   output_file_path: [workspace_dir]/chunks/translations/translation_[NNN].md

   Chunk index: [index] of [total]
   Target language: [target language] ([language code])

   Read all input files and write your translation to the output file. Use the pre-translated glossary terms consistently.
   ```

4. **Parallelization:** Launch up to 5 translator agents in parallel for efficiency. Wait for each batch to complete before launching the next batch.

5. After each batch, update manifest with chunk translation status and confidence levels

6. Update manifest to mark translation phase as completed

7. Mark Phase 4 as complete

---

### Phase 5: Verification and Revision (Optional)

**Goal:** Verify translation quality and automatically apply revisions for critical issues

**Skip this phase if:** `--skip-verify` flag was provided

**Actions:**

1. Mark Phase 5 as in_progress (or skip if --skip-verify)

2. Update manifest phase status to "in_progress" for verification

3. For each chunk, launch the **verifier** agent using the Task tool with file paths:
   ```
   Verify this translation for quality. If you find critical issues, provide a revised translation with all fixes applied.

   chunk_file_path: [workspace_dir]/chunks/source/chunk_[NNN].txt
   translation_file_path: [workspace_dir]/chunks/translations/translation_[NNN].md
   context_file_path: [workspace_dir]/context/context_analysis.md
   glossary_file_path: [workspace_dir]/glossary.json
   output_file_path: [workspace_dir]/chunks/verifications/verification_[NNN].md

   Target language: [target language] ([language code])

   Read all input files and write your verification report to the output file. If you identify critical issues, include a complete revised translation in the "Revised Translation" section.
   ```

4. **Parallelization:** Launch all verifier agents in parallel since verification is independent per chunk

5. Parse verification results from the output files:
   - Calculate overall quality score (average)
   - Collect all critical issues
   - Collect all warnings

6. **Check for revisions in each verification file:**
   - Read each verification file
   - Look for "## Revised Translation" section
   - If found and NOT "No revision needed":
     - Update manifest chunk: `revision_applied: true`
     - Log: "Chunk [N]: Revision applied"
   - Otherwise:
     - Update manifest chunk: `revision_applied: false`

7. Update manifest with verification status and scores for each chunk

8. Update manifest to mark verification phase as completed

9. Present verification summary to user:
   - Show overall quality score
   - List chunks that received automatic revisions
   - Summarize types of issues that were fixed

10. Mark Phase 5 as complete

---

### Phase 6: Assembly and Output

**Goal:** Combine translated chunks and write output file

**Actions:**

1. Mark Phase 6 as in_progress

2. Update manifest phase status to "in_progress" for assembly

3. Use the **assemble_translation MCP tool** `mcp__plugin_claude-translate_translator__assemble_translation`:
   - `manifest_path`: Path to manifest.json
   - `output_path`: Path for final translated document

   The tool:
   - Reads each translation file from the workspace
   - Extracts the "Translated Text" section from each
   - Joins them with double newlines
   - Writes to the output path

4. Generate a translation report and write to `{output_basename}_report.md`:
   ```markdown
   # Translation Report

   ## Summary
   - Source: [source file]
   - Target Language: [language] ([code])
   - Output: [output file]
   - Workspace: [workspace directory]
   - Total Words: [word count]
   - Chunks Processed: [chunk count]

   ## Quality Metrics
   - Overall Score: [X/10]
   - Critical Issues: [count]
   - Warnings: [count]

   ## Terminology Glossary
   | Source Term | Translation | Notes |
   |-------------|-------------|-------|
   [glossary entries from glossary.json]

   ## Translation Notes
   [Notable decisions made during translation - collected from translation files]

   ## Verification Summary
   [Summary of verification results, if verification was run]

   ## Workspace Files
   All intermediate files are preserved in: [workspace_dir]
   - Context analysis: context/context_analysis.md
   - Source chunks: chunks/source/
   - Summaries: chunks/summaries/
   - Glossaries: chunks/glossaries/
   - Translations: chunks/translations/
   - Verifications: chunks/verifications/
   ```

5. Update manifest to mark assembly phase as completed

6. Present final summary to user:
   - Confirm output file was written
   - Show quality score (if verification ran)
   - Highlight any issues that need attention
   - Provide path to the translation report
   - Note that workspace directory is preserved for debugging

7. Mark Phase 6 as complete

8. Clean up manifest symlink:
   ```bash
   rm -f /tmp/claude_translate_manifest.json
   ```

9. Mark all todos as complete

---

## Error Handling

- **File not found:** Report error with the exact path tried and suggest checking the path
- **Unsupported language:** List all supported languages with their codes
- **Agent failure:** Retry the agent once. If it fails again, report partial results and continue with remaining chunks
- **Large files (>50,000 words):** Warn user about expected processing time before starting

---

## Usage Examples

```bash
# Basic translation to Korean
/translate report.md --target korean

# Translation with custom output file
/translate docs/guide.txt --target japanese --output docs/guide_ja.txt

# Fast translation without verification
/translate article.md --target spanish --skip-verify

# Using language codes
/translate paper.md --target ko
/translate paper.md --target zh-tw
```

---

## Supported Languages

Use either full names or ISO codes:

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
