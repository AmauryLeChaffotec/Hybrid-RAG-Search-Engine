"""
ingest.py - Document loader for the Hybrid RAG Search Engine.

Reads .txt and .md files from a given directory and returns structured
document dictionaries ready for chunking and indexing.
"""

import os
from pathlib import Path
from typing import List, Dict


def load_documents(docs_dir: str = "docs") -> List[Dict]:
    """
    Load all .txt and .md files from docs_dir.

    Args:
        docs_dir: Path to the directory containing documents.

    Returns:
        List of dicts with keys:
            - source_id: filename without extension
            - path: full file path as string
            - content: file text content (stripped)
    """
    docs = []
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"Documents directory not found: {docs_dir}")

    for filepath in sorted(docs_path.glob("**/*")):
        if filepath.suffix in (".txt", ".md") and filepath.is_file():
            try:
                content = filepath.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = filepath.read_text(encoding="latin-1")

            docs.append({
                "source_id": filepath.stem,
                "path": str(filepath),
                "content": content.strip(),
            })

    return docs


if __name__ == "__main__":
    # Quick smoke test
    docs = load_documents("docs")
    print(f"Loaded {len(docs)} documents:")
    for d in docs:
        print(f"  - {d['source_id']} ({len(d['content'])} chars)")
