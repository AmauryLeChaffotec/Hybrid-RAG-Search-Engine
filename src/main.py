"""
main.py - CLI entry point for the Hybrid RAG Search Engine.

Two sub-commands:
    index   Build the FTS5 + vector index from documents in docs/.
    search  Query the index and (optionally) generate an LLM answer.

Usage:
    python -m src.main index [--docs docs/] [--chunk-size 700] [--overlap 120]
    python -m src.main search --query "..." [--mode hybrid|lexical|semantic]
                              [--top-k 5] [--no-llm] [--db rag_index.db]
"""

import argparse
import sys
import os
from pathlib import Path

# Ensure the project root is on sys.path when running as a module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingest import load_documents
from src.chunking import chunk_documents
from src.index import build_index, DB_PATH
from src.search import hybrid_search, lexical_search, semantic_search, invalidate_cache
from src.llm import generate_answer


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------

def cmd_index(args: argparse.Namespace) -> None:
    """Handle the 'index' sub-command."""
    print(f"Loading documents from '{args.docs}'...")
    try:
        docs = load_documents(args.docs)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not docs:
        print(f"No .txt or .md files found in '{args.docs}'. Aborting.")
        sys.exit(1)

    print(f"Loaded {len(docs)} documents:")
    for d in docs:
        print(f"  - {d['source_id']} ({len(d['content'])} chars)")

    print(f"\nChunking documents (size={args.chunk_size}, overlap={args.overlap})...")
    chunks = chunk_documents(docs, chunk_size=args.chunk_size, overlap=args.overlap)
    print(f"Created {len(chunks)} chunks.")

    build_index(chunks, db_path=args.db)

    # Invalidate any in-memory cache from a previous search in the same session
    invalidate_cache()

    print(f"\nIndexing complete. Database saved to '{args.db}'.")


def cmd_search(args: argparse.Namespace) -> None:
    """Handle the 'search' sub-command."""
    if not Path(args.db).exists():
        print(f"Index not found at '{args.db}'. Please run 'index' first.")
        sys.exit(1)

    query = args.query or input("Enter your question: ").strip()
    if not query:
        print("No query provided. Exiting.")
        sys.exit(1)

    print(f"\nSearching for: {query!r}")
    print(f"Mode: {args.mode}  |  Top-K: {args.top_k}")
    print("=" * 60)

    if args.mode == "lexical":
        results = lexical_search(query, k=args.top_k, db_path=args.db)
    elif args.mode == "semantic":
        results = semantic_search(query, k=args.top_k, db_path=args.db)
    else:  # hybrid (default)
        results = hybrid_search(query, k=args.top_k, db_path=args.db)

    if not results:
        print("No results found.")
        return

    print(f"\nTop {len(results)} passages retrieved:\n")
    for i, r in enumerate(results, 1):
        if args.mode == "hybrid":
            score_info = f"RRF score={r.get('rrf_score', 'N/A')}"
        elif args.mode == "semantic":
            score_info = f"cosine={r.get('score', 'N/A'):.4f}"
        else:
            score_info = f"rank={r.get('rank', 'N/A')}"

        print(f"[{i}] Source: {r['source_id']}  |  {score_info}")
        print(f"    {r['text'][:200].strip()}...")
        print()

    if not args.no_llm:
        print("=" * 60)
        print("Generating LLM answer...\n")
        try:
            answer = generate_answer(query, results)
            print("Answer:")
            print("-" * 60)
            print(answer)
            print("-" * 60)
        except ValueError as e:
            print(f"LLM skipped: {e}")
        except Exception as e:
            print(f"LLM error: {e}")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.main",
        description="Hybrid RAG Search Engine — index documents and answer questions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Index all documents in docs/
  python -m src.main index --docs docs/

  # Hybrid search (lexical + semantic) with LLM answer
  python -m src.main search --query "What are the EU invoice formatting requirements?"

  # Lexical-only search, skip LLM
  python -m src.main search --mode lexical --no-llm --query "GDPR data retention"

  # Semantic search with custom top-k
  python -m src.main search --mode semantic --top-k 8 --query "VAT exemptions"

  # Use a custom database path
  python -m src.main --db /tmp/my_index.db index --docs docs/
        """,
    )

    parser.add_argument(
        "--db",
        default=DB_PATH,
        help=f"Path to the SQLite index database (default: {DB_PATH})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # -- index sub-command ---------------------------------------------------
    idx_parser = subparsers.add_parser("index", help="Build the search index from documents")
    idx_parser.add_argument(
        "--docs",
        default="docs",
        help="Path to the documents directory (default: docs)",
    )
    idx_parser.add_argument(
        "--chunk-size",
        type=int,
        default=700,
        dest="chunk_size",
        help="Maximum characters per chunk (default: 700)",
    )
    idx_parser.add_argument(
        "--overlap",
        type=int,
        default=120,
        help="Overlap between consecutive chunks in characters (default: 120)",
    )

    # -- search sub-command --------------------------------------------------
    srch_parser = subparsers.add_parser(
        "search",
        help="Search indexed documents and optionally generate an LLM answer",
    )
    srch_parser.add_argument(
        "--query", "-q",
        default=None,
        help="Search query string (interactive prompt if omitted)",
    )
    srch_parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        dest="top_k",
        help="Number of passages to retrieve (default: 5)",
    )
    srch_parser.add_argument(
        "--mode",
        choices=["hybrid", "lexical", "semantic"],
        default="hybrid",
        help="Search mode (default: hybrid)",
    )
    srch_parser.add_argument(
        "--no-llm",
        action="store_true",
        dest="no_llm",
        help="Skip the LLM answer generation step",
    )

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "index":
        cmd_index(args)
    elif args.command == "search":
        cmd_search(args)


if __name__ == "__main__":
    main()
