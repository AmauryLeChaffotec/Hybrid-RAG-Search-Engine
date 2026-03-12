"""
index.py - Indexing engine for the Hybrid RAG Search Engine.

Builds and manages two complementary indexes:
  1. SQLite FTS5 virtual table for fast lexical (BM25-ranked) search.
  2. SQLite BLOB column storing float32 embeddings for semantic search.

Embedding model: sentence-transformers all-MiniLM-L6-v2 (384 dimensions).
"""

import sqlite3
import numpy as np
from typing import List, Dict, Tuple
from pathlib import Path
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DB_PATH = "rag_index.db"
EMBED_MODEL = "all-MiniLM-L6-v2"


# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Open and return a SQLite connection with WAL journal mode."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


# ---------------------------------------------------------------------------
# Schema initialisation
# ---------------------------------------------------------------------------

def init_db(conn: sqlite3.Connection) -> None:
    """
    (Re-)create the FTS5 and vector tables.

    WARNING: drops existing tables — intended to be called once during indexing.
    """
    conn.execute("DROP TABLE IF EXISTS chunks_fts")
    conn.execute("DROP TABLE IF EXISTS chunks_vec")

    # FTS5 virtual table for lexical search (BM25 ranking via `rank` column)
    conn.execute("""
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            chunk_id,
            source_id,
            path,
            text,
            chunk_index UNINDEXED
        )
    """)

    # Regular table for storing raw embeddings as BLOBs
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks_vec (
            chunk_id    TEXT PRIMARY KEY,
            source_id   TEXT,
            path        TEXT,
            text        TEXT,
            chunk_index INTEGER,
            embedding   BLOB
        )
    """)

    conn.commit()


# ---------------------------------------------------------------------------
# Index builder
# ---------------------------------------------------------------------------

def build_index(chunks: List[Dict], db_path: str = DB_PATH) -> None:
    """
    Build FTS5 and vector indexes from a list of chunk dicts.

    Args:
        chunks:  List of chunk dicts produced by chunking.chunk_documents().
        db_path: Path to the SQLite database file to create/overwrite.
    """
    print(f"Loading embedding model: {EMBED_MODEL}...")
    model = SentenceTransformer(EMBED_MODEL)

    texts = [c["text"] for c in chunks]
    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        batch_size=64,
    )

    conn = sqlite3.connect(db_path)
    init_db(conn)

    print("Inserting into FTS5 index...")
    conn.executemany(
        "INSERT INTO chunks_fts(chunk_id, source_id, path, text, chunk_index) VALUES (?,?,?,?,?)",
        [
            (c["chunk_id"], c["source_id"], c["path"], c["text"], c["chunk_index"])
            for c in chunks
        ],
    )

    print("Inserting embeddings...")
    conn.executemany(
        "INSERT INTO chunks_vec(chunk_id, source_id, path, text, chunk_index, embedding) VALUES (?,?,?,?,?,?)",
        [
            (
                c["chunk_id"],
                c["source_id"],
                c["path"],
                c["text"],
                c["chunk_index"],
                emb.astype(np.float32).tobytes(),
            )
            for c, emb in zip(chunks, embeddings)
        ],
    )

    conn.commit()
    conn.close()
    print(f"Index built: {len(chunks)} chunks indexed in '{db_path}'.")


# ---------------------------------------------------------------------------
# Embedding loader (used by search at query time)
# ---------------------------------------------------------------------------

def load_embeddings(db_path: str = DB_PATH) -> Tuple[List[str], List[Dict], np.ndarray]:
    """
    Load all stored embeddings from the database into memory.

    Returns:
        chunk_ids: List of chunk_id strings (same order as matrix rows).
        metadata:  List of metadata dicts (chunk_id, source_id, path, text, chunk_index).
        matrix:    numpy float32 array of shape (N, embedding_dim).
    """
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT chunk_id, source_id, path, text, chunk_index, embedding FROM chunks_vec"
    ).fetchall()
    conn.close()

    chunk_ids: List[str] = []
    metadata: List[Dict] = []
    vecs: List[np.ndarray] = []

    for row in rows:
        chunk_id, source_id, path, text, chunk_index, emb_blob = row
        chunk_ids.append(chunk_id)
        metadata.append({
            "chunk_id": chunk_id,
            "source_id": source_id,
            "path": path,
            "text": text,
            "chunk_index": chunk_index,
        })
        vec = np.frombuffer(emb_blob, dtype=np.float32)
        vecs.append(vec)

    matrix = np.stack(vecs) if vecs else np.array([])
    return chunk_ids, metadata, matrix
