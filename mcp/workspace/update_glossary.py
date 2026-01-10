"""Update the translation glossary."""

import json
from typing import Any, Dict, List


def handle(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Add or update terms in the glossary."""
    glossary_path = arguments["glossary_path"]
    new_terms: List[Dict] = arguments["terms"]

    # Read current glossary
    with open(glossary_path, "r", encoding="utf-8") as f:
        glossary = json.load(f)

    # Create a lookup for existing terms
    existing_terms = {term["source"]: term for term in glossary["terms"]}

    # Add or update terms
    added = 0
    updated = 0
    for new_term in new_terms:
        source = new_term["source"]
        if source in existing_terms:
            # Update existing term
            existing_terms[source]["translation"] = new_term["translation"]
            if "notes" in new_term:
                existing_terms[source]["notes"] = new_term["notes"]
            updated += 1
        else:
            # Add new term
            term_entry = {
                "source": source,
                "translation": new_term["translation"]
            }
            if "notes" in new_term:
                term_entry["notes"] = new_term["notes"]
            glossary["terms"].append(term_entry)
            added += 1

    # Write updated glossary
    with open(glossary_path, "w", encoding="utf-8") as f:
        json.dump(glossary, f, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "glossary_path": glossary_path,
        "terms_added": added,
        "terms_updated": updated,
        "total_terms": len(glossary["terms"])
    }
