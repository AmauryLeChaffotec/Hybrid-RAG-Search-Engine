"""
chunking.py - Text chunking utilities for the Hybrid RAG Search Engine.

Splits documents into overlapping fixed-size character chunks to ensure
that context windows remain manageable for embedding models while
preserving continuity across chunk boundaries via overlap.
"""

from typing import List, Dict


def chunk_document(doc: Dict, chunk_size: int = 700, overlap: int = 120) -> List[Dict]:
    """
    Split a single document into overlapping character-level chunks.

    Args:
        doc:        Document dict with keys: source_id, path, content.
        chunk_size: Maximum number of characters per chunk.
        overlap:    Number of characters to overlap between consecutive chunks.

    Returns:
        List of chunk dicts with keys:
            - chunk_id:    Unique identifier "<source_id>_<index>"
            - source_id:   Originating document identifier
            - path:        File path of the source document
            - text:        Chunk text content
            - chunk_index: Sequential index of this chunk within its document
    """
    text = doc["content"]
    chunks = []
    start = 0
    idx = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append({
                "chunk_id": f"{doc['source_id']}_{idx}",
                "source_id": doc["source_id"],
                "path": doc["path"],
                "text": chunk_text,
                "chunk_index": idx,
            })
            idx += 1

        start += chunk_size - overlap

    return chunks


def chunk_documents(docs: List[Dict], chunk_size: int = 700, overlap: int = 120) -> List[Dict]:
    """
    Chunk all documents in a collection.

    Args:
        docs:       List of document dicts (output of ingest.load_documents).
        chunk_size: Maximum number of characters per chunk.
        overlap:    Number of characters to overlap between consecutive chunks.

    Returns:
        Flat list of all chunk dicts across all documents.
    """
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc, chunk_size, overlap))
    return all_chunks


if __name__ == "__main__":
    # Quick smoke test
    sample_doc = {
        "source_id": "sample",
        "path": "docs/sample.md",
        "content": "Lorem ipsum " * 200,
    }
    chunks = chunk_document(sample_doc)
    print(f"Produced {len(chunks)} chunks from a {len(sample_doc['content'])}-char document.")
    for c in chunks[:3]:
        print(f"  chunk_id={c['chunk_id']}, len={len(c['text'])}")
