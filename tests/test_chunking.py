"""
test_chunking.py - Unit tests for the chunking module.

Tests cover:
- Single document chunking with overlapping windows
- Short document edge case (single chunk)
- Overlap correctness (tail of chunk N appears in head of chunk N+1)
- Unique chunk IDs across multiple documents
"""

import pytest
import sys
from pathlib import Path

# Ensure the project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chunking import chunk_document, chunk_documents


# ---------------------------------------------------------------------------
# Single-document chunking
# ---------------------------------------------------------------------------

def test_chunk_single_document():
    """A document longer than one chunk should produce multiple chunks."""
    doc = {"source_id": "test_doc", "path": "docs/test_doc.md", "content": "A" * 1500}
    chunks = chunk_document(doc, chunk_size=700, overlap=120)

    assert len(chunks) >= 2, "A 1500-char document with chunk_size=700 must yield >= 2 chunks"
    assert all(c["source_id"] == "test_doc" for c in chunks), "All chunks must inherit the source_id"
    assert all(len(c["text"]) <= 700 for c in chunks), "No chunk should exceed chunk_size characters"


def test_chunk_short_document():
    """A document shorter than one chunk should produce exactly one chunk."""
    doc = {"source_id": "short", "path": "docs/short.md", "content": "Short content."}
    chunks = chunk_document(doc)

    assert len(chunks) == 1, "A short document must produce exactly one chunk"
    assert chunks[0]["text"] == "Short content.", "The single chunk must preserve the full content"


def test_chunk_empty_document():
    """An empty document should produce no chunks."""
    doc = {"source_id": "empty", "path": "docs/empty.md", "content": ""}
    chunks = chunk_document(doc)
    assert len(chunks) == 0, "An empty document must produce zero chunks"


# ---------------------------------------------------------------------------
# Overlap correctness
# ---------------------------------------------------------------------------

def test_chunk_overlap():
    """The tail of chunk N should appear at the beginning of chunk N+1."""
    content = "word " * 300  # ~1500 characters
    doc = {"source_id": "overlap_test", "path": "", "content": content}
    chunks = chunk_document(doc, chunk_size=700, overlap=120)

    if len(chunks) >= 2:
        end_of_first = chunks[0]["text"][-120:]
        # The end of chunk 0 must be present somewhere in chunk 1
        assert end_of_first.strip() in chunks[1]["text"] or len(end_of_first.strip()) == 0, (
            "The last 120 characters of chunk 0 must appear in chunk 1 (overlap)"
        )


# ---------------------------------------------------------------------------
# Chunk metadata
# ---------------------------------------------------------------------------

def test_chunk_index_is_sequential():
    """chunk_index values within a document must be strictly sequential from 0."""
    doc = {"source_id": "seq_test", "path": "", "content": "X" * 3000}
    chunks = chunk_document(doc, chunk_size=700, overlap=120)

    for expected_idx, chunk in enumerate(chunks):
        assert chunk["chunk_index"] == expected_idx, (
            f"Expected chunk_index={expected_idx}, got {chunk['chunk_index']}"
        )


def test_chunk_id_format():
    """chunk_id must follow the pattern '<source_id>_<index>'."""
    doc = {"source_id": "myfile", "path": "", "content": "Hello " * 300}
    chunks = chunk_document(doc)

    for chunk in chunks:
        expected_id = f"myfile_{chunk['chunk_index']}"
        assert chunk["chunk_id"] == expected_id, (
            f"Expected chunk_id '{expected_id}', got '{chunk['chunk_id']}'"
        )


# ---------------------------------------------------------------------------
# Multi-document chunking
# ---------------------------------------------------------------------------

def test_chunk_ids_unique():
    """Chunk IDs must be unique across all documents."""
    docs = [
        {"source_id": "doc1", "path": "", "content": "A" * 2000},
        {"source_id": "doc2", "path": "", "content": "B" * 2000},
    ]
    chunks = chunk_documents(docs)
    ids = [c["chunk_id"] for c in chunks]
    assert len(ids) == len(set(ids)), "All chunk IDs across all documents must be unique"


def test_chunk_documents_aggregates_all():
    """chunk_documents must return chunks from every document."""
    docs = [
        {"source_id": "alpha", "path": "", "content": "Alpha text. " * 100},
        {"source_id": "beta", "path": "", "content": "Beta text. " * 100},
        {"source_id": "gamma", "path": "", "content": "Gamma text. " * 100},
    ]
    chunks = chunk_documents(docs)
    source_ids = {c["source_id"] for c in chunks}
    assert source_ids == {"alpha", "beta", "gamma"}, (
        "Chunks must cover all input documents"
    )


def test_chunk_documents_empty_list():
    """An empty document list should return an empty chunk list."""
    chunks = chunk_documents([])
    assert chunks == [], "Empty input must produce empty output"
