"""
HW2: Semantic retrieval layer for RLM Knowledge Base
=====================================================
Pipeline: chunks.jsonl -> embeddings -> FAISS index -> top-k search -> results

Usage:
    python scripts/retrieval.py                 # Full pipeline
    python scripts/retrieval.py --rebuild       # Force rebuild embeddings + index
    python scripts/retrieval.py --search-only   # Search only (load existing index)
"""

import json
import os
import sys
import argparse
import logging

import numpy as np
import faiss

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────
CHUNKS_FILE = "data/processed/chunks.jsonl"
INDEX_DIR = "index"
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
OUTPUT_FILE = "outputs/retrieval_examples.md"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

# ── 10 RLM-focused test queries ───────────────────────
TEST_QUERIES = [
    # Core RLM concepts
    "How does the RLM REPL architecture process user prompts that exceed the base model's fixed context window?",
    "What is context rot in recursive language models and how does it affect performance on long-context tasks?",
    "How does the Python REPL environment function within the RLM agent architecture for recursive code execution?",

    # Results & benchmarks
    "How does RLM recursive reasoning compare to retrieval-augmented generation?",
    "How does RLM performance scale on long-context tasks like S-NIAH compared to non-recursive base LLMs?",

    # Comparisons
    "What are the architectural trade-offs between RLM recursive decomposition and retrieval-augmented generation for multi-hop reasoning?",
    "How does the evolution from flat prompting to recursive execution relate to context management in language models?",

    # Implementation & tools
    "What are the ablation results for RLM with and without sub-calling on information-dense tasks?",
    "How does the HALO agent optimizer implement RLM-based recursive loops for tool use?",

    # RL training
    "How does reinforcement learning fine-tuning improve RLM recursive behavior compared to supervised fine-tuning?",
]


def load_chunks(path: str) -> list[dict]:
    """Load chunks from JSONL file."""
    chunks = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    logger.info(f"Loaded {len(chunks)} chunks from {path}")
    return chunks


def build_embeddings(chunks: list[dict]) -> np.ndarray:
    """Compute embeddings for all chunks using sentence-transformers."""
    from sentence_transformers import SentenceTransformer

    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [c["text"] for c in chunks]
    logger.info(f"Computing embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    # Convert to float32
    embeddings = embeddings.astype(np.float32)
    logger.info(f"Embeddings shape: {embeddings.shape}")
    return embeddings


def save_index(embeddings: np.ndarray, path: str):
    """Save FAISS index to disk."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, path)
    logger.info(f"Saved FAISS index ({embeddings.shape[0]} vectors, dim={dim}) to {path}")


def load_index(path: str) -> faiss.IndexFlatIP:
    """Load FAISS index from disk."""
    index = faiss.read_index(path)
    logger.info(f"Loaded FAISS index: {index.ntotal} vectors, dim={index.d}")
    return index


def search(index: faiss.IndexFlatIP, query: str, chunks: list[dict], k: int = TOP_K) -> list[dict]:
    """Search for top-k most similar chunks to a query."""
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(EMBEDDING_MODEL)
    query_emb = model.encode([query], normalize_embeddings=True).astype(np.float32)

    scores, indices = index.search(query_emb, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        chunk = chunks[idx]
        results.append({
            "chunk_id": chunk["chunk_id"],
            "score": round(float(score), 4),
            "text": chunk["text"],
            "metadata": chunk.get("metadata", {}),
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="HW2: Semantic retrieval layer")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild embeddings + index")
    parser.add_argument("--search-only", action="store_true", help="Search with existing index")
    parser.add_argument("--k", type=int, default=TOP_K, help="Number of results per query")
    args = parser.parse_args()

    os.makedirs(INDEX_DIR, exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Load chunks
    logger.info(f"Loading chunks from {CHUNKS_FILE}")
    chunks = load_chunks(CHUNKS_FILE)

    # Build or load index
    if args.rebuild or not os.path.exists(INDEX_FILE):
        logger.info("Building embeddings...")
        embeddings = build_embeddings(chunks)
        save_index(embeddings, INDEX_FILE)
    else:
        logger.info(f"Loading existing index from {INDEX_FILE}")

    # Load index for search
    index = load_index(INDEX_FILE)

    # Run test queries
    logger.info(f"\nRunning {len(TEST_QUERIES)} test queries with top-k={args.k}")

    all_results = []
    for i, query in enumerate(TEST_QUERIES, 1):
        logger.info(f"  [{i}/{len(TEST_QUERIES)}] {query[:80]}")
        results = search(index, query, chunks, k=args.k)
        all_results.append({"query": query, "results": results})
        if results:
            logger.info(f"         -> top-1: score={results[0]['score']} ({results[0]['chunk_id']})")

    # Write output file
    logger.info(f"\nWriting results to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w") as f:
        f.write("# HW2: Semantic Retrieval — Test Results\n\n")
        f.write(f"**Embedding model:** {EMBEDDING_MODEL}\n")
        f.write(f"**FAISS index:** IndexFlatIP, {index.ntotal} vectors\n")
        f.write(f"**Chunks:** {len(chunks)}\n")
        f.write(f"**Queries:** {len(TEST_QUERIES)}\n")
        f.write(f"**Top-k:** {args.k}\n\n")
        f.write("---\n\n")

        for query_data in all_results:
            query = query_data["query"]
            results = query_data["results"]
            f.write(f"Query: {query}\n\n")
            for rank, r in enumerate(results, 1):
                preview = r["text"][:200].replace("\n", " ")
                source = r["metadata"].get("source_file", "N/A")
                f.write(f"Top-{rank}: {r['chunk_id']} | score: {r['score']}\n")
                f.write(f"  Text: {preview}\n")
                f.write(f"  Source: {source}\n\n")
            f.write("---\n\n")

    logger.info("Done!")

    # Print summary
    print("\n" + "=" * 80)
    print("RETRIEVAL SUMMARY")
    print("=" * 80)
    for i, query_data in enumerate(all_results, 1):
        query = query_data["query"]
        results = query_data["results"]
        if results:
            top = results[0]
            doc_id = top["metadata"].get("document_id", "?")
            print(f"  {i}. {query[:65]:65s} | {top['score']:5.4f} ({doc_id})")
        else:
            print(f"  {i}. {query[:65]:65s} | NO RESULTS")
    print("=" * 80)


if __name__ == "__main__":
    main()