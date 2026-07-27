#!/usr/bin/env python3
"""
retrieval.py — Semantic retrieval layer for RLM knowledge base.

Pipeline: chunks.jsonl → embeddings (MiniLM-L6-v2) → FAISS index → top-k search

Usage:
    # Build index from chunks.jsonl:
        python scripts/retrieval.py build

    # Search with a query:
        python scripts/retrieval.py search "How do RLMs handle long context?"

    # Run all test queries and save results:
        python scripts/retrieval.py test

    # Search with custom k:
        python scripts/retrieval.py search "What is context rot?" --k 5
"""

import argparse
import json
import os
import sys

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ── Paths ───────────────────────────────────────────────────────────────────
CHUNKS_FILE = "data/processed/chunks.jsonl"
INDEX_DIR = "index"
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
EMBEDDINGS_FILE = os.path.join(INDEX_DIR, "embeddings.npy")
METADATA_FILE = os.path.join(INDEX_DIR, "metadata.json")
OUTPUTS_DIR = "outputs"
RESULTS_FILE = os.path.join(OUTPUTS_DIR, "retrieval_examples.md")

# ── Model ───────────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 outputs 384-dim vectors

# ── Test queries ────────────────────────────────────────────────────────────
TEST_QUERIES = [
    {
        "query": "How do RLMs handle arbitrarily long prompts?",
        "expect": "context-centric view, recursive decomposition, REPL environment",
    },
    {
        "query": "What is context rot and why does it happen?",
        "expect": "degradation of context quality with increasing length",
    },
    {
        "query": "How does HALO optimize agent loops?",
        "expect": "hierarchical agent loop, root LM + sub-LMs, trace analysis",
    },
    {
        "query": "What are the key differences between RLM and ReAct?",
        "expect": "RLM is recursive, ReAct is reasoning+acting with tools",
    },
    {
        "query": "What is the Griffin architecture used in RecurrentGemma?",
        "expect": "linear recurrences, fixed-size state, local attention",
    },
    {
        "query": "How does Prime Intellect implement RLM ablations?",
        "expect": "DeepDive, math-python, Oolong, verbatim-copy environments",
    },
    {
        "query": "What is context folding and how does RLM compare?",
        "expect": "agentic context engineering, AgentFold vs RLM delegation",
    },
    {
        "query": "How do you install and set up the RLM system?",
        "expect": "pip install, REPL environments, Docker setup",
    },
    {
        "query": "What benchmark results does RLM achieve on Oolong?",
        "expect": "Oolong benchmark, multi-step reasoning, accuracy",
    },
    {
        "query": "What are the training insights for RLMs in paper v3?",
        "expect": "training environment, reinforcement learning, scaling",
    },
]


def load_chunks() -> list[dict]:
    """Load chunks from JSONL file."""
    if not os.path.exists(CHUNKS_FILE):
        print(f"Error: {CHUNKS_FILE} not found. Run prepare_knowledge_base.py first.")
        sys.exit(1)
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def build_index():
    """Build FAISS index from chunks.jsonl."""
    print(f"Loading chunks from {CHUNKS_FILE}...")
    chunks = load_chunks()
    texts = [c["text"] for c in chunks]
    print(f"Loaded {len(chunks)} chunks. Encoding with {EMBEDDING_MODEL}...")

    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    print(f"Encoded: {embeddings.shape}")

    os.makedirs(INDEX_DIR, exist_ok=True)

    # Store embeddings as float32
    embeddings_f32 = embeddings.astype(np.float32)

    # Build FAISS index (IDMap + Flat L2)
    index = faiss.IndexFlatIP(EMBEDDING_DIM)  # Inner product for cosine similarity
    # Normalize embeddings for cosine similarity via inner product
    faiss.normalize_L2(embeddings_f32)
    index.add(embeddings_f32)

    # Save index
    index_path = INDEX_FILE
    faiss.write_index(index, index_path)
    print(f"FAISS index saved: {index_path}")

    # Save embeddings for later use
    np.save(EMBEDDINGS_FILE, embeddings_f32)
    print(f"Embeddings saved: {EMBEDDINGS_FILE}")

    # Save metadata (chunk_id, source_file, document_id, section)
    metadata = []
    for c in chunks:
        metadata.append({
            "chunk_id": c["chunk_id"],
            "source_file": c["metadata"]["source_file"],
            "document_id": c["metadata"]["document_id"],
            "title": c["metadata"]["title"],
            "section": c["metadata"]["section"],
            "chunk_index": c["metadata"]["chunk_index"],
            "domain": c["metadata"]["domain"],
            "document_type": c["metadata"]["document_type"],
        })
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Metadata saved: {METADATA_FILE}")

    print(f"\nDone! Index contains {len(chunks)} chunks, dim={EMBEDDING_DIM}")
    return index, metadata


def load_index():
    """Load FAISS index and metadata from disk."""
    if not os.path.exists(INDEX_FILE):
        print(f"Error: {INDEX_FILE} not found. Run 'build' first.")
        sys.exit(1)
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata


# ── Cached model & chunks ───────────────────────────────────────────────────
_model = None
_chunks_cache = None


def get_model() -> SentenceTransformer:
    """Get (cached) embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_chunks() -> list[dict]:
    """Get (cached) chunks from JSONL."""
    global _chunks_cache
    if _chunks_cache is None:
        _chunks_cache = load_chunks()
    return _chunks_cache


def search(query: str, k: int = 3) -> list[dict]:
    """Search for top-k chunks matching the query."""
    index, metadata = load_index()
    model = get_model()

    query_embedding = model.encode([query], convert_to_numpy=True)
    query_f32 = query_embedding.astype(np.float32)
    faiss.normalize_L2(query_f32)

    scores, indices = index.search(query_f32, k)

    results = []
    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < 0:
            continue
        meta = metadata[idx]
        results.append({
            "rank": i + 1,
            "chunk_id": meta["chunk_id"],
            "score": round(float(score), 4),
            "text": "",  # Will be filled from chunks
            "source_file": meta["source_file"],
            "document_id": meta["document_id"],
            "title": meta["title"],
            "section": meta["section"],
            "domain": meta["domain"],
            "document_type": meta["document_type"],
        })

    # Load full text for results (cached)
    all_chunks = get_chunks()
    chunk_map = {c["chunk_id"]: c["text"] for c in all_chunks}
    for r in results:
        r["text"] = chunk_map.get(r["chunk_id"], "")

    return results


def format_result(r: dict, max_text: int = 200) -> str:
    """Format a single result for display."""
    text = r["text"]
    if len(text) > max_text:
        text = text[:max_text] + "..."
    return (
        f"Top-{r['rank']}: {r['chunk_id']} | score: {r['score']:.4f}\n"
        f"  Text: {text}\n"
        f"  Source: {r['source_file']} | Section: {r['section']}\n"
    )


def run_tests() -> str:
    """Run all test queries and generate retrieval_examples.md."""
    print(f"Running {len(TEST_QUERIES)} test queries...")
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    lines = []
    lines.append("# Retrieval Test Results\n")
    lines.append(f"**Model:** {EMBEDDING_MODEL}\n")
    lines.append(f"**Index:** FAISS (Inner Product, dim={EMBEDDING_DIM})\n")
    lines.append(f"**Chunks indexed:** {sum(1 for _ in load_chunks())}\n")
    lines.append(f"**Top-k:** 3\n\n")
    lines.append("---\n")

    for i, tc in enumerate(TEST_QUERIES, 1):
        query = tc["query"]
        print(f"  Query {i}/{len(TEST_QUERIES)}: {query}")

        results = search(query, k=3)

        lines.append(f"## Query {i}: {query}\n")
        lines.append(f"**Expected:** {tc['expect']}\n\n")

        for r in results:
            lines.append(format_result(r))
            lines.append("\n")

        # Auto-comment based on score and keyword overlap
        if results:
            top1_score = results[0]["score"]
            top1_text_lower = results[0]["text"].lower()
            expect_lower = tc["expect"].lower()

            # Check keyword overlap
            expect_words = set(expect_lower.split())
            top_words = set(top1_text_lower.split())
            overlap = len(expect_words & top_words)
            overlap_ratio = overlap / max(len(expect_words), 1)

            if top1_score >= 0.6 and overlap_ratio >= 0.3:
                comment = "relevant"
            elif top1_score >= 0.4 or overlap_ratio >= 0.2:
                comment = "partially relevant"
            else:
                comment = "not relevant"
        else:
            comment = "no results"

        lines.append(f"**Comment:** {comment}\n\n")
        lines.append("---\n")

    # Write output
    content = "\n".join(lines)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nResults saved to {RESULTS_FILE}")
    print(f"Total queries: {len(TEST_QUERIES)}")
    return content


def main():
    parser = argparse.ArgumentParser(description="Semantic retrieval for RLM knowledge base")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Build
    subparsers.add_parser("build", help="Build FAISS index from chunks.jsonl")

    # Search
    search_parser = subparsers.add_parser("search", help="Search with a query")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--k", type=int, default=3, help="Number of results (default: 3)")

    # Test
    subparsers.add_parser("test", help="Run all test queries")

    args = parser.parse_args()

    if args.command == "build":
        build_index()
    elif args.command == "search":
        results = search(args.query, args.k)
        print(f"\nQuery: {args.query}\n")
        for r in results:
            print(format_result(r))
    elif args.command == "test":
        run_tests()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()