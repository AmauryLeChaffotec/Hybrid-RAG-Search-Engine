"""
search.py - Hybrid search engine combining lexical and semantic retrieval.

Three search modes are available:
  - lexical:  FTS5 BM25 keyword search only.
  - semantic: Cosine-similarity vector search only.
  - hybrid:   Reciprocal Rank Fusion (RRF) of both modes (default).

Module-level caches for the embedding model and the in-memory embedding
matrix avoid repeated disk reads and model reloads across successive queries.
"""

import sqlite3
import numpy as np
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
from src.index import DB_PATH, EMBED_MODEL, load_embeddings

# ---------------------------------------------------------------------------
# Module-level caches
# ---------------------------------------------------------------------------

_model: Optional[SentenceTransformer] = None
_embeddings_cache: Optional[Tuple[List[str], List[Dict], np.ndarray]] = None


def get_model() -> SentenceTransformer:
    """Lazily load and cache the sentence-transformer model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def get_embeddings_cache(db_path: str = DB_PATH) -> Tuple[List[str], List[Dict], np.ndarray]:
    """Lazily load and cache embeddings from the database."""
    global _embeddings_cache
    if _embeddings_cache is None:
        _embeddings_cache = load_embeddings(db_path)
    return _embeddings_cache


def invalidate_cache() -> None:
    """Clear module-level caches (useful after re-indexing)."""
    global _model, _embeddings_cache
    _model = None
    _embeddings_cache = None


# ---------------------------------------------------------------------------
# Lexical search (FTS5)
# ---------------------------------------------------------------------------

def lexical_search(query: str, k: int = 10, db_path: str = DB_PATH) -> List[Dict]:
    """
    FTS5 BM25 keyword search.

    Each query token is quoted to prevent FTS5 syntax errors from special
    characters. Results are ordered by BM25 rank (lower rank = better match).

    Args:
        query:   Natural-language search query.
        k:       Maximum number of results to return.
        db_path: Path to the SQLite database.

    Returns:
        List of chunk dicts with an additional 'rank' key (1-based).
    """
    conn = sqlite3.connect(db_path)

    # Safely quote each token for FTS5 MATCH syntax
    tokens = [w.strip() for w in query.split() if w.strip()]
    safe_query = " ".join(f'"{t}"' for t in tokens)

    try:
        rows = conn.execute(
            """
            SELECT chunk_id, source_id, path, text, chunk_index, rank
            FROM   chunks_fts
            WHERE  chunks_fts MATCH ?
            ORDER  BY rank
            LIMIT  ?
            """,
            (safe_query, k),
        ).fetchall()
    except Exception:
        rows = []
    finally:
        conn.close()

    results = []
    for rank_idx, row in enumerate(rows):
        chunk_id, source_id, path, text, chunk_index, fts_rank = row
        results.append({
            "chunk_id": chunk_id,
            "source_id": source_id,
            "path": path,
            "text": text,
            "chunk_index": chunk_index,
            "rank": rank_idx + 1,
        })
    return results


# ---------------------------------------------------------------------------
# Semantic search (cosine similarity)
# ---------------------------------------------------------------------------

def semantic_search(query: str, k: int = 10, db_path: str = DB_PATH) -> List[Dict]:
    """
    Dense vector search using cosine similarity.

    Encodes the query with the same sentence-transformer used at index time,
    then computes cosine similarity against the full embedding matrix loaded
    into memory.

    Args:
        query:   Natural-language search query.
        k:       Maximum number of results to return.
        db_path: Path to the SQLite database.

    Returns:
        List of chunk dicts with additional 'score' and 'rank' keys.
    """
    model = get_model()
    query_vec = model.encode([query], convert_to_numpy=True)[0].astype(np.float32)

    chunk_ids, metadata, matrix = get_embeddings_cache(db_path)
    if len(matrix) == 0:
        return []

    # Normalise rows and query vector for cosine similarity via dot product
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norm_matrix = matrix / (norms + 1e-9)

    query_norm = query_vec / (np.linalg.norm(query_vec) + 1e-9)
    scores = norm_matrix @ query_norm  # shape: (N,)

    top_indices = np.argsort(scores)[::-1][:k]

    results = []
    for rank_idx, idx in enumerate(top_indices):
        meta = metadata[idx].copy()
        meta["score"] = float(scores[idx])
        meta["rank"] = rank_idx + 1
        results.append(meta)

    return results


# ---------------------------------------------------------------------------
# Hybrid search — Reciprocal Rank Fusion
# ---------------------------------------------------------------------------

def hybrid_search(
    query: str,
    k: int = 5,
    db_path: str = DB_PATH,
    rrf_k: int = 60,
) -> List[Dict]:
    """
    Hybrid search using Reciprocal Rank Fusion (RRF).

    RRF formula: score(d) = Σ 1 / (rrf_k + rank(d))
    where the sum is taken over all result lists in which document d appears.

    A chunk appearing in both the lexical and semantic result lists receives
    a higher fused score than one appearing in only one list.

    Args:
        query:   Natural-language search query.
        k:       Number of final results to return.
        db_path: Path to the SQLite database.
        rrf_k:   RRF smoothing constant (default: 60, per the original paper).

    Returns:
        List of k chunk dicts ordered by descending RRF score, each with an
        additional 'rrf_score' key.
    """
    # Retrieve broader candidate sets before fusion
    lex_results = lexical_search(query, k=k * 2, db_path=db_path)
    sem_results = semantic_search(query, k=k * 2, db_path=db_path)

    scores: Dict[str, float] = {}
    chunk_data: Dict[str, Dict] = {}

    for result in lex_results:
        cid = result["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + result["rank"])
        chunk_data[cid] = result

    for result in sem_results:
        cid = result["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + result["rank"])
        if cid not in chunk_data:
            chunk_data[cid] = result

    # Sort by descending RRF score and take top-k
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]

    final = []
    for cid, rrf_score in ranked:
        entry = chunk_data[cid].copy()
        entry["rrf_score"] = round(rrf_score, 6)
        final.append(entry)

    return final
