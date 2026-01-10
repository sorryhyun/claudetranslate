#!/usr/bin/env python3
"""Test script for MCP workspace tools."""

import json
import os
import sys
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.workspace import init_workspace, read_manifest, update_manifest, update_glossary, assemble_translation
from mcp.text_split import split_text

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE = os.path.join(TEST_DIR, "sample.md")


def cleanup_workspace():
    """Remove test workspace if it exists."""
    workspace = os.path.join(TEST_DIR, "sample_translate_temp")
    if os.path.exists(workspace):
        shutil.rmtree(workspace)
    print("Cleaned up workspace")


def test_init_workspace():
    """Test init_workspace tool."""
    print("\n=== Testing init_workspace ===")
    result = init_workspace.handle({
        "source_file_path": SAMPLE_FILE,
        "target_language": "korean",
        "target_language_code": "ko",
        "skip_verify": False
    })
    print(f"Workspace created: {result['workspace_dir']}")
    print(f"Manifest: {result['manifest_path']}")
    print(f"Word count: {result['source_word_count']}")
    assert os.path.exists(result['manifest_path'])
    assert os.path.exists(result['glossary_path'])
    return result


def test_split_text(workspace_dir):
    """Test split_text tool."""
    print("\n=== Testing split_text ===")
    result = split_text.handle({
        "source_file_path": SAMPLE_FILE,
        "output_dir": workspace_dir,
        "target_words": 500,
        "min_words": 200,
        "max_words": 800
    })
    print(f"Chunks created: {result['chunk_count']}")
    print(f"Total words: {result['total_words']}")
    print(f"Chunk files: {result['chunk_files']}")

    # Verify chunk files exist
    for chunk_file in result['chunk_files']:
        chunk_path = os.path.join(workspace_dir, "chunks", "source", chunk_file)
        assert os.path.exists(chunk_path), f"Missing chunk: {chunk_path}"

    return result


def test_read_manifest(manifest_path):
    """Test read_manifest tool."""
    print("\n=== Testing read_manifest ===")
    result = read_manifest.handle({
        "manifest_path": manifest_path
    })
    print(f"Source file: {result['source']['file_path']}")
    print(f"Target language: {result['target']['language']}")
    print(f"Chunk count: {len(result['chunks'])}")
    return result


def test_update_manifest(manifest_path):
    """Test update_manifest tool."""
    print("\n=== Testing update_manifest ===")
    result = update_manifest.handle({
        "manifest_path": manifest_path,
        "phase": "context_analysis",
        "phase_status": "completed"
    })
    print(f"Updated: {result['success']}")

    # Verify update
    manifest = read_manifest.handle({"manifest_path": manifest_path})
    assert manifest['phases']['context_analysis']['status'] == 'completed'
    print("Phase status verified: completed")
    return result


def test_update_glossary(glossary_path):
    """Test update_glossary tool."""
    print("\n=== Testing update_glossary ===")
    result = update_glossary.handle({
        "glossary_path": glossary_path,
        "terms": [
            {"source": "API", "translation": "API", "notes": "Keep as-is"},
            {"source": "function", "translation": "함수", "notes": "Standard term"}
        ]
    })
    print(f"Terms added: {result['terms_added']}")
    print(f"Total terms: {result['total_terms']}")

    # Verify glossary
    with open(glossary_path, 'r') as f:
        glossary = json.load(f)
    assert len(glossary['terms']) == 2
    print("Glossary verified")
    return result


def test_assemble_translation(manifest_path, output_path, workspace_dir):
    """Test assemble_translation tool."""
    print("\n=== Testing assemble_translation ===")

    # First, create some mock translation files
    manifest = read_manifest.handle({"manifest_path": manifest_path})

    for chunk in manifest['chunks']:
        trans_path = os.path.join(workspace_dir, chunk['translation_file'])
        os.makedirs(os.path.dirname(trans_path), exist_ok=True)
        with open(trans_path, 'w') as f:
            f.write(f"""## Translation Output

### Translated Text
이것은 청크 {chunk['index']}의 번역입니다.

테스트 번역 내용입니다.

### Glossary Additions
| Source Term | Translation | Notes |
|-------------|-------------|-------|

### Translation Notes
- Test translation

### Confidence Level
High - Test

### Transition Notes
- Ending: Test ending
""")

    result = assemble_translation.handle({
        "manifest_path": manifest_path,
        "output_path": output_path
    })
    print(f"Output created: {result['output_path']}")
    print(f"Chunks assembled: {result['chunk_count']}")
    print(f"Output word count: {result['output_word_count']}")

    assert os.path.exists(output_path)
    print("Assembly verified")
    return result


def main():
    """Run all tests."""
    print("=" * 50)
    print("MCP Tools Test Suite")
    print("=" * 50)

    # Cleanup first
    cleanup_workspace()

    try:
        # Test init_workspace
        init_result = test_init_workspace()
        workspace_dir = init_result['workspace_dir']
        manifest_path = init_result['manifest_path']
        glossary_path = init_result['glossary_path']

        # Test split_text
        test_split_text(workspace_dir)

        # Test read_manifest
        test_read_manifest(manifest_path)

        # Test update_manifest
        test_update_manifest(manifest_path)

        # Test update_glossary
        test_update_glossary(glossary_path)

        # Test assemble_translation
        output_path = os.path.join(TEST_DIR, "sample_ko.md")
        test_assemble_translation(manifest_path, output_path, workspace_dir)

        print("\n" + "=" * 50)
        print("ALL TESTS PASSED!")
        print("=" * 50)

    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
