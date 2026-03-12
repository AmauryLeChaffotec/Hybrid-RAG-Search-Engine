"""
test_search.py - Unit tests for search and scoring logic.

Tests cover:
- RRF scoring correctness (fusion of lexical + semantic ranks)
- Cosine similarity computation
- Edge cases (empty result sets, identical vectors, orthogonal vectors)

Note: These tests are pure unit tests that do not require a live database
or the sentence-transformer model to be loaded.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Ensure the project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Helper: RRF scoring logic (extracted from search.py for unit testing)
# ---------------------------------------------------------------------------

def compute_rrf(lex_results, sem_results, rrf_k=60):
    """Replicate the RRF fusion logic from search.hybrid_search."""
    scores = {}
    chunk_data = {}

    for result in lex_results:
        cid = result["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + result["rank"])
        chunk_data[cid] = result

    for result in sem_results:
        cid = result["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + result["rank"])
        if cid not in chunk_data:
            chunk_data[cid] = result

    return scores, chunk_data


# ---------------------------------------------------------------------------
# RRF scoring tests
# ---------------------------------------------------------------------------

def test_rrf_scoring_logic():
    """A chunk in both result lists must score higher than one in only one list."""
    rrf_k = 60
    lex_results = [
        {"chunk_id": "a", "rank": 1},
        {"chunk_id": "b", "rank": 2},
    ]
    sem_results = [
        {"chunk_id": "b", "rank": 1},
        {"chunk_id": "c", "rank": 2},
    ]

    scores, _ = compute_rrf(lex_results, sem_results, rrf_k=rrf_k)

    # "b" appears in both → must have the highest combined score
    assert scores["b"] > scores["a"], "'b' (in both lists) must beat 'a' (lexical only)"
    assert scores["b"] > scores["c"], "'b' (in both lists) must beat 'c' (semantic only)"


def test_rrf_formula():
    """Verify exact RRF score computation against manual calculation."""
    rrf_k = 60
    lex_results = [{"chunk_id": "x", "rank": 1}]
    sem_results = [{"chunk_id": "x", "rank": 1}]

    scores, _ = compute_rrf(lex_results, sem_results, rrf_k=rrf_k)

    expected = 2.0 / (rrf_k + 1)
    assert abs(scores["x"] - expected) < 1e-9, (
        f"Expected RRF score {expected}, got {scores['x']}"
    )


def test_rrf_unique_chunks():
    """Chunks appearing only in one list should still have a positive score."""
    rrf_k = 60
    lex_results = [{"chunk_id": "lex_only", "rank": 1}]
    sem_results = [{"chunk_id": "sem_only", "rank": 1}]

    scores, _ = compute_rrf(lex_results, sem_results, rrf_k=rrf_k)

    assert scores["lex_only"] > 0
    assert scores["sem_only"] > 0
    assert abs(scores["lex_only"] - scores["sem_only"]) < 1e-9, (
        "Equal rank in respective lists should give equal scores"
    )


def test_rrf_empty_results():
    """Empty result lists must produce empty scores."""
    scores, _ = compute_rrf([], [], rrf_k=60)
    assert scores == {}, "Empty inputs must yield empty scores"


def test_rrf_rank_ordering():
    """Lower rank values (better position) must translate to higher RRF contributions."""
    rrf_k = 60
    score_rank1 = 1.0 / (rrf_k + 1)
    score_rank5 = 1.0 / (rrf_k + 5)
    assert score_rank1 > score_rank5, "Rank 1 must contribute more to RRF than rank 5"


# ---------------------------------------------------------------------------
# Cosine similarity tests
# ---------------------------------------------------------------------------

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def test_cosine_identical_vectors():
    """Identical vectors must have cosine similarity of 1.0."""
    v = np.array([1.0, 0.0, 0.0])
    assert abs(cosine(v, v) - 1.0) < 1e-6, "Identical vectors must have cosine similarity = 1"


def test_cosine_orthogonal_vectors():
    """Orthogonal vectors must have cosine similarity of ~0.0."""
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0])
    assert abs(cosine(v1, v2)) < 1e-6, "Orthogonal vectors must have cosine similarity ≈ 0"


def test_cosine_opposite_vectors():
    """Opposite vectors must have cosine similarity of -1.0."""
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([-1.0, 0.0, 0.0])
    assert abs(cosine(v1, v2) + 1.0) < 1e-6, "Opposite vectors must have cosine similarity = -1"


def test_cosine_with_different_magnitudes():
    """Cosine similarity is magnitude-invariant."""
    v1 = np.array([1.0, 0.0])
    v2 = np.array([5.0, 0.0])  # Same direction, different magnitude
    assert abs(cosine(v1, v2) - 1.0) < 1e-6, (
        "Vectors with same direction but different magnitudes must still have similarity = 1"
    )


def test_cosine_high_dimensional():
    """Cosine similarity should work correctly in high-dimensional space (384-dim like MiniLM)."""
    np.random.seed(42)
    dim = 384
    v1 = np.random.randn(dim).astype(np.float32)
    v2 = v1.copy()  # Identical
    assert abs(cosine(v1, v2) - 1.0) < 1e-5

    v3 = np.random.randn(dim).astype(np.float32)
    sim = cosine(v1, v3)
    assert -1.0 <= sim <= 1.0, "Cosine similarity must always be in [-1, 1]"


# ---------------------------------------------------------------------------
# Matrix-based semantic search simulation
# ---------------------------------------------------------------------------

def test_matrix_cosine_top1():
    """The top-1 result in cosine search must be the most similar document."""
    query = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    matrix = np.array([
        [1.0, 0.0, 0.0],   # identical to query — must be top-1
        [0.0, 1.0, 0.0],   # orthogonal
        [0.5, 0.5, 0.0],   # partial match
    ], dtype=np.float32)

    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norm_matrix = matrix / (norms + 1e-9)
    query_norm = query / (np.linalg.norm(query) + 1e-9)
    scores = norm_matrix @ query_norm

    top_idx = int(np.argmax(scores))
    assert top_idx == 0, f"Expected row 0 as top result, got row {top_idx}"
