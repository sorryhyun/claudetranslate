"""Workspace management tools for translation pipeline."""

from . import init_workspace
from . import read_manifest
from . import update_manifest
from . import update_glossary
from . import assemble_translation

TOOLS = {
    "init_workspace": init_workspace,
    "read_manifest": read_manifest,
    "update_manifest": update_manifest,
    "update_glossary": update_glossary,
    "assemble_translation": assemble_translation,
}
