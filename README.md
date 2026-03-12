# Hybrid RAG Search Engine

A production-quality Retrieval-Augmented Generation (RAG) search engine that combines **lexical (BM25/FTS5)** and **semantic (dense vector)** search via **Reciprocal Rank Fusion (RRF)**, with LLM answer generation powered by the **Mistral API**.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Usage — CLI](#usage--cli)
6. [Example Queries](#example-queries)
7. [How It Works](#how-it-works)
8. [Design Decisions](#design-decisions)
9. [Running Tests](#running-tests)
10. [Docker](#docker)
11. [Configuration](#configuration)
12. [Extending the Engine](#extending-the-engine)

---

## Architecture Overview

```
                    ┌─────────────────────────────────────────┐
                    │              User Query                  │
                    └─────────────────┬───────────────────────┘
                                      │
                    ┌─────────────────▼───────────────────────┐
                    │           src/search.py                  │
                    │          hybrid_search()                 │
                    └──────────┬────────────────┬─────────────┘
                               │                │
              ┌────────────────▼──┐        ┌────▼────────────────┐
              │  lexical_search() │        │ semantic_search()    │
              │   SQLite FTS5     │        │ Cosine similarity    │
              │   BM25 ranking    │        │ all-MiniLM-L6-v2     │
              └────────────────┬──┘        └────┬────────────────┘
                               │                │
                    ┌──────────▼────────────────▼──────────────┐
                    │     Reciprocal Rank Fusion (RRF)          │
                    │   score = Σ 1/(k + rank)  for each list  │
                    └──────────────────┬───────────────────────┘
                                       │  Top-K passages
                    ┌──────────────────▼───────────────────────┐
                    │         src/llm.py — Mistral API          │
                    │   RAG prompt + context → grounded answer  │
                    └──────────────────────────────────────────┘
```

**Index build pipeline:**

```
docs/*.md → ingest.py → chunking.py → index.py → rag_index.db
                                        ├─ FTS5 virtual table (lexical)
                                        └─ embedding BLOBs   (semantic)
```

---

## Project Structure

```
Hybrid-RAG-Search-Engine/
├── src/
│   ├── __init__.py
│   ├── ingest.py       # Document loader (.txt, .md)
│   ├── chunking.py     # Overlapping fixed-size chunker
│   ├── index.py        # SQLite FTS5 + embedding index builder
│   ├── search.py       # Lexical, semantic, and hybrid search
│   ├── llm.py          # Mistral API prompt builder & caller
│   └── main.py         # CLI entry point (argparse)
├── docs/
│   ├── invoice_formatting_requirements.md
│   ├── gdpr_data_retention.md
│   ├── food_labeling_regulations.md
│   ├── vat_exemptions_2024.md
│   ├── electronic_invoicing_mandate.md
│   ├── contract_general_conditions.md
│   ├── data_breach_notification.md
│   ├── product_liability_directive.md
│   ├── consumer_protection_rights.md
│   ├── digital_services_act.md
│   ├── aml_kyc_requirements.md
│   └── accessibility_requirements.md
├── tests/
│   ├── test_chunking.py
│   └── test_search.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## Quick Start

```bash
# 1. Clone / navigate to the project
cd Hybrid-RAG-Search-Engine

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Set your Mistral API key
cp .env.example .env
# Edit .env: MISTRAL_API_KEY=sk-...

# Load env (Linux/macOS)
export $(grep -v '^#' .env | xargs)
# Windows PowerShell:
# $env:MISTRAL_API_KEY="sk-..."

# 4. Build the index
python -m src.main index --docs docs/

# 5. Search with LLM answer
python -m src.main search --query "What are the mandatory fields on an EU invoice?"
```

---

## Installation

### Requirements

- Python 3.9+
- Internet access on first run (downloads the `all-MiniLM-L6-v2` model, ~90 MB)
- A Mistral API key (obtain at https://console.mistral.ai/)

### Step-by-step

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Dependencies:
| Package | Purpose |
|---|---|
| `sentence-transformers` | Embedding model (`all-MiniLM-L6-v2`) |
| `mistralai` | Official Mistral Python SDK |
| `numpy` | Vector arithmetic (cosine similarity, matrix ops) |
| `pytest` | Test runner |

SQLite (including FTS5) is bundled with Python's standard library — no additional installation is required.

---

## Usage — CLI

### `index` command

Build the search index from all `.txt` and `.md` files in a directory.

```
python -m src.main index [OPTIONS]

Options:
  --docs PATH         Directory containing documents (default: docs)
  --chunk-size INT    Characters per chunk (default: 700)
  --overlap INT       Overlap between consecutive chunks (default: 120)
  --db PATH           Output database path (default: rag_index.db)
```

Example:
```bash
python -m src.main index --docs docs/ --chunk-size 700 --overlap 120
```

### `search` command

Search the index and generate an LLM answer.

```
python -m src.main search [OPTIONS]

Options:
  --query, -q TEXT    Search query (interactive if omitted)
  --mode CHOICE       hybrid | lexical | semantic (default: hybrid)
  --top-k INT         Number of passages to retrieve (default: 5)
  --no-llm            Skip LLM generation, print passages only
  --db PATH           Database path (default: rag_index.db)
```

Examples:
```bash
# Full hybrid RAG (retrieval + LLM answer)
python -m src.main search -q "What is the 72-hour rule for data breaches?"

# Keyword-only search, no LLM
python -m src.main search --mode lexical --no-llm -q "VAT exemption education"

# Semantic search with more results
python -m src.main search --mode semantic --top-k 8 -q "consumer withdrawal right"

# Interactive mode (prompts for query)
python -m src.main search --mode hybrid
```

---

## Example Queries

Below are example questions that work well with the 12 included documents:

```bash
python -m src.main search -q "What are the mandatory fields required on an EU invoice?"

python -m src.main search -q "How long must personal data be retained under GDPR?"

python -m src.main search -q "What is the 72-hour notification deadline after a data breach?"

python -m src.main search -q "Which food allergens must be highlighted on EU product labels?"

python -m src.main search -q "What are the VAT exemptions for healthcare services in France?"

python -m src.main search -q "When does the French electronic invoicing mandate apply to SMEs?"

python -m src.main search -q "What are the consumer's rights when withdrawing from an online purchase?"

python -m src.main search -q "What is the RRF scoring formula and what are the obligations for Very Large Online Platforms?"

python -m src.main search -q "What enhanced due diligence applies to politically exposed persons?"

python -m src.main search -q "What is the minimum font size for mandatory food label information?"
```

---

## How It Works

### 1. Ingestion (`src/ingest.py`)

Walks the `docs/` directory and reads all `.txt` and `.md` files. Each document becomes a dict with `source_id` (filename stem), `path`, and `content`.

### 2. Chunking (`src/chunking.py`)

Documents are split into overlapping fixed-size character windows:
- **chunk_size = 700 characters** — fits comfortably within the 512-token limit of `all-MiniLM-L6-v2`
- **overlap = 120 characters** — preserves sentence continuity across chunk boundaries, preventing information loss at split points

### 3. Indexing (`src/index.py`)

Two data structures are built and stored in a single SQLite file (`rag_index.db`):

**FTS5 virtual table (`chunks_fts`):**
SQLite's FTS5 extension provides BM25-ranked full-text search. Each chunk is inserted into the virtual table and indexed word-by-word with term frequency weighting. At query time, FTS5 returns results ordered by the `rank` column (BM25 score, lower is better).

**Embedding table (`chunks_vec`):**
The same chunks are encoded with `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional float32 vectors). Each vector is stored as a raw BLOB in SQLite. At query time, all embeddings are loaded into memory as a numpy matrix for batch cosine similarity computation.

### 4. Hybrid Search (`src/search.py`)

**Lexical search:** Escapes each query token and runs a `MATCH` query against the FTS5 table. Retrieves up to `2k` candidates.

**Semantic search:** Encodes the query into a 384-dim vector, normalises both the query vector and the full embedding matrix, and computes cosine similarity as a dot product. The top-`2k` results by score are returned.

**Reciprocal Rank Fusion:** For each candidate chunk, the RRF score is accumulated:

```
rrf_score(chunk) = Σ  1 / (60 + rank_in_list)
```

where the sum is taken over every result list in which the chunk appears. The constant 60 is the standard value from the original RRF paper (Cormack et al., 2009) and prevents top-ranked documents from dominating excessively. Chunks appearing in both lists receive contributions from both, making them rank higher than chunks present in only one list.

### 5. LLM Generation (`src/llm.py`)

The top-k retrieved passages are concatenated into a structured prompt with source labels. The prompt instructs the Mistral model to:
- Answer using only the provided context
- Cite sources explicitly
- Respond with "I don't have enough information" if the answer is not in the context

Temperature is set to 0.1 for factual consistency.

---

## Design Decisions

### Why SQLite with FTS5 instead of a dedicated vector database?

SQLite with FTS5 is the right choice for this use case because:
- **Zero infrastructure**: No external services (Elasticsearch, Qdrant, Weaviate) to deploy, configure, or maintain
- **Single file**: The entire index fits in one portable `rag_index.db` file
- **FTS5 BM25 quality**: SQLite's FTS5 BM25 implementation is competitive with dedicated search engines for small to medium corpora
- **Numpy cosine search**: For corpora up to ~100k chunks, in-memory numpy matrix multiplication is fast enough (sub-second queries)

For production scale (millions of chunks), a dedicated vector store such as Qdrant or pgvector would be more appropriate.

### Why Reciprocal Rank Fusion instead of score normalisation?

Score normalisation (e.g., min-max scaling and averaging) is sensitive to the scale and distribution of scores from different retrieval systems, which vary significantly between BM25 and cosine similarity. RRF is:
- **Distribution-free**: Only uses rank order, not raw scores
- **Simple**: The formula has a single intuitive hyperparameter (k=60)
- **Empirically strong**: Consistently competitive in TREC and BEIR benchmarks

### Why all-MiniLM-L6-v2?

- **Size vs performance trade-off**: At ~90 MB and 384 dimensions, it produces high-quality sentence embeddings while being fast to download and run on CPU
- **Wide adoption**: Well-supported by the sentence-transformers library with reliable tokenization and pooling
- For higher quality, swap to `BAAI/bge-large-en-v1.5` or `intfloat/multilingual-e5-large` (multilingual)

### Why chunk at 700 characters with 120-char overlap?

- 700 characters ≈ 100-150 tokens, well within the 512-token window of MiniLM and leaving room for longer sentences
- 120-char overlap (~17%) is enough to prevent sentence splitting from silently cutting information at boundaries, without creating excessive index duplication

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only chunking tests
pytest tests/test_chunking.py -v

# Run only search/scoring tests
pytest tests/test_search.py -v
```

Tests do not require a database or API key — they are pure unit tests.

---

## Docker

### Build

```bash
docker build -t rag-engine .
```

### Run

```bash
# Index documents (mount docs/ and persist the database)
docker run --rm \
  -v "$(pwd)/docs:/app/docs" \
  -v "$(pwd):/app/data" \
  -e MISTRAL_API_KEY=sk-... \
  rag-engine \
  python -m src.main index --docs docs/ --db /app/data/rag_index.db

# Search
docker run --rm \
  -v "$(pwd):/app/data" \
  -e MISTRAL_API_KEY=sk-... \
  rag-engine \
  python -m src.main search --db /app/data/rag_index.db \
    -q "What are GDPR data retention rules?"
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `MISTRAL_API_KEY` | (required) | Mistral API key from console.mistral.ai |
| `--db` | `rag_index.db` | Path to the SQLite index database |
| `--docs` | `docs` | Directory containing source documents |
| `--chunk-size` | `700` | Max characters per chunk |
| `--overlap` | `120` | Overlap between consecutive chunks |
| `--top-k` | `5` | Number of passages to retrieve |
| `--mode` | `hybrid` | Search mode: hybrid / lexical / semantic |

To change the Mistral model, edit `src/llm.py` and update the `model` parameter in `generate_answer()`. Available options:
- `mistral-small-latest` — Fast and cost-effective
- `mistral-large-latest` — More capable, better reasoning

---

## Extending the Engine

### Adding new documents

Simply add `.md` or `.txt` files to the `docs/` directory and re-run:
```bash
python -m src.main index --docs docs/
```

### Changing the embedding model

In `src/index.py`, update:
```python
EMBED_MODEL = "intfloat/multilingual-e5-large"  # or any SBERT-compatible model
```
Then rebuild the index.

### Adding a REST API

Wrap `hybrid_search` and `generate_answer` in a FastAPI application:
```python
from fastapi import FastAPI
from src.search import hybrid_search
from src.llm import generate_answer

app = FastAPI()

@app.post("/search")
def search(query: str, top_k: int = 5):
    passages = hybrid_search(query, k=top_k)
    answer = generate_answer(query, passages)
    return {"passages": passages, "answer": answer}
```

### Using a vector database (production scale)

Replace `src/index.py` and the `semantic_search` function in `src/search.py` with calls to Qdrant, Weaviate, or pgvector while keeping the same chunk dict interface. The FTS5 lexical search and RRF fusion layers remain unchanged.

---

## License

This project is provided as an educational reference implementation. Adapt freely for your own use cases.
