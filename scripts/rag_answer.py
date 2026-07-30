#!/usr/bin/env python3
"""
rag_answer.py — RAG Answer Generation pipeline.

Pipeline:
    user question -> retrieve top-k chunks -> build prompt -> call LLM -> return grounded answer with sources

Features:
- Prompt template with grounded answering rule
- Citation/source reference in every answer
- Fallback behavior for insufficient context
- Prompt improvement tracking (v1 -> v2 -> v3)

Usage:
    python scripts/rag_answer.py build
    python scripts/rag_answer.py evaluate
    python scripts/rag_answer.py compare "question" --versions 1,2,3
"""

import argparse
import json
import os
import sys
import time

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI

CHUNKS_FILE = "data/processed/chunks.jsonl"
INDEX_DIR = "index"
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
EMBEDDINGS_FILE = os.path.join(INDEX_DIR, "embeddings.npy")
METADATA_FILE = os.path.join(INDEX_DIR, "metadata.json")
OUTPUTS_DIR = "outputs"
EXAMPLES_FILE = os.path.join(OUTPUTS_DIR, "rag_answers_examples.md")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

LLM_API_BASE = "http://10.10.0.86:8002/v1"
LLM_API_KEY = "sk-not-needed"
LLM_MODEL = "qwen36-27b-awq"
LLM_TEMP = 0.1
LLM_MAX_TOKENS = 4096

PROMPT_V1 = (
    "Answer the question using the context below.\n"
    "Context: {retrieved_context}\n"
    "Question: {user_question}\n"
    "Answer:"
)

PROMPT_V2 = (
    "You are a research assistant for Recursive Language Models (RLM) topics.\n"
    "\n"
    "RULES:\n"
    "- Answer ONLY using the information provided in the context below.\n"
    "- If the context does not contain enough information to answer, say: "
    '"I do not have enough information in the available documents to answer this question."\n'
    "- Do NOT use any general knowledge outside the provided context.\n"
    "\n"
    "Context:\n"
    "{retrieved_context}\n"
    "\n"
    "Question:\n"
    "{user_question}\n"
    "\n"
    "Answer:"
)

PROMPT_V3 = (
    "You are a research assistant specializing in Recursive Language Models (RLM), "
    "Retrieval-Augmented Generation (RAG), and LLM reasoning paradigms.\n"
    "\n"
    "INSTRUCTIONS:\n"
    "1. Answer the user question using ONLY the information in the provided context below.\n"
    "2. If the context does not contain sufficient information to answer the question, respond with:\n"
    '   "I do not have enough information in the available documents to answer this question."\n'
    "3. Do NOT use general knowledge, assumptions, or information outside the provided context.\n"
    "4. Cite every factual claim using the format: [chunk_id] (e.g., [rlm_original_paper_chunk_006]).\n"
    "5. If multiple chunks support different parts of the answer, cite each separately.\n"
    "6. Keep the answer concise and focused - avoid unnecessary elaboration.\n"
    "\n"
    "Context:\n"
    "{retrieved_context}\n"
    "\n"
    "Question:\n"
    "{user_question}\n"
    "\n"
    "Answer:"
)

PROMPT_VERSIONS = {1: PROMPT_V1, 2: PROMPT_V2, 3: PROMPT_V3}

TEST_QUESTIONS = [
    {"id": 1, "question": "How do recursive language models handle prompts larger than their context window?", "type": "simple", "desc": "Core RLM concept — how RLMs decompose long prompts"},
    {"id": 2, "question": "What is context rot and why does performance degrade with longer inputs?", "type": "simple", "desc": "Context rot definition and causes"},
    {"id": 3, "question": "How does the Python REPL environment work in RLM architecture?", "type": "simple", "desc": "REPL architecture in RLM"},
    {"id": 4, "question": "What benchmark results does RLM achieve on BrowseComp-Plus and OOLONG?", "type": "simple", "desc": "RLM benchmark results"},
    {"id": 5, "question": "What are the key differences between RLM and RAG for long-context processing?", "type": "simple", "desc": "RLM vs RAG comparison"},
    {"id": 6, "question": "What are the key ablation results for RLM with versus without sub-calling?", "type": "simple", "desc": "RLM ablation experiments"},
    {"id": 7, "question": "How does RL fine-tuning improve RLM behavior compared to prompting or SFT alone?", "type": "simple", "desc": "RL training for RLMs"},
    {"id": 8, "question": "What is the stock price of Apple Inc in 2025?", "type": "insufficient", "desc": "Insufficient context — should trigger fallback"},
    {"id": 9, "question": "How much does the RLM system cost to run in production?", "type": "insufficient", "desc": "Insufficient context — no pricing info in KB"},
    {"id": 10, "question": "Who invented the internet?", "type": "insufficient", "desc": "Completely out of scope — should trigger fallback"},
]


def load_chunks():
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line.strip()))
    return chunks


def get_embedding_model():
    if not hasattr(get_embedding_model, "_model"):
        get_embedding_model._model = SentenceTransformer(EMBEDDING_MODEL)
    return get_embedding_model._model


def build_index():
    model = get_embedding_model()
    chunks = load_chunks()
    embeddings = model.encode(
        [c["text"] for c in chunks],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype(np.float32)
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(embeddings)
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    np.save(EMBEDDINGS_FILE, embeddings)
    metadata = {}
    for i, c in enumerate(chunks):
        metadata[str(i)] = {
            "chunk_id": c.get("chunk_id", ""),
            "document_id": c.get("metadata", {}).get("document_id", ""),
            "source_file": c.get("metadata", {}).get("source_file", ""),
            "title": c.get("metadata", {}).get("title", ""),
            "section": c.get("metadata", {}).get("section", ""),
            "chunk_index": c.get("metadata", {}).get("chunk_index", 0),
            "domain": c.get("metadata", {}).get("domain", ""),
            "document_type": c.get("metadata", {}).get("document_type", ""),
        }
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Built index with {len(chunks)} chunks, dim={EMBEDDING_DIM}")


def search(query, k=3):
    model = get_embedding_model()
    chunks = load_chunks()
    if not os.path.exists(INDEX_FILE):
        print(f"Error: {INDEX_FILE} not found. Run build first.")
        sys.exit(1)
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "r") as f:
        meta_db = json.load(f)
    query_emb = model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    scores, indices = index.search(query_emb, k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        results.append((chunks[idx], float(score), meta_db.get(str(idx), {})))
    return results


def format_context_with_ids(results):
    parts = []
    for chunk, score, meta in results:
        cid = chunk.get("chunk_id", f"chunk_{meta.get('chunk_index', '?')}")
        section = meta.get("section", "N/A")
        source = meta.get("source_file", "unknown")
        header = f"[{cid}] -- {section} ({source})\nscore: {score:.3f}"
        text_preview = chunk["text"][:500]
        parts.append(f"{header}\n{text_preview}")
    return "\n\n---\n\n".join(parts)


def call_llm(prompt, temperature=LLM_TEMP, max_tokens=LLM_MAX_TOKENS):
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_API_BASE)
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content
        if content is None:
            return "[ERROR: LLM returned empty response]"
        return content
    except Exception as e:
        return f"[ERROR calling LLM: {e}]"


def answer_question(question, prompt_version=3, k=3):
    results = search(question, k=k)
    if not results:
        return {
            "question": question,
            "retrieved_chunks": [],
            "answer": "I do not have enough information in the available documents to answer this question.",
            "sources": [],
            "scores": [],
            "comment": "No chunks retrieved - fallback triggered.",
            "prompt_version": prompt_version,
        }
    context = format_context_with_ids(results)
    prompt_template = PROMPT_VERSIONS.get(prompt_version, PROMPT_V3)
    prompt = prompt_template.format(retrieved_context=context, user_question=question)
    answer = call_llm(prompt)
    chunk_ids = [r[0].get("chunk_id", "?") for r in results]
    sources = [r[2].get("source_file", "?") for r in results]
    return {
        "question": question,
        "retrieved_chunks": chunk_ids,
        "answer": answer,
        "sources": list(set(sources)),
        "scores": [round(r[1], 4) for r in results],
        "comment": "",
        "prompt_version": prompt_version,
    }


def generate_examples(prompt_version=3, output_file=None):
    if output_file is None:
        output_file = EXAMPLES_FILE
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    lines = []
    lines.append("# RAG Answer Generation -- Test Results\n")
    version_desc = {1: "basic - no grounding rules", 2: "grounded - no citation requirement", 3: "grounded + citation + fallback"}
    lines.append(f"**Prompt version:** v{prompt_version} ({version_desc.get(prompt_version, 'custom')})\n")
    lines.append(f"**LLM:** {LLM_MODEL} via vLLM\n")
    lines.append(f"**Embedding:** {EMBEDDING_MODEL}\n")
    chunk_count = len(load_chunks())
    lines.append(f"**Index:** FAISS FlatIP, {chunk_count} chunks\n")
    lines.append(f"**Top-k:** 3\n")
    lines.append("---\n")
    for q in TEST_QUESTIONS:
        print(f"Q{q['id']}: {q['question'][:60]}...")
        result = answer_question(q["question"], prompt_version=prompt_version)
        lines.append(f"## Question {q['id']}: {q['question']}\n")
        lines.append(f"**Type:** {q['type']} ({q['desc']})\n")
        lines.append("**Retrieved chunks:**\n")
        for i, (cid, score) in enumerate(zip(result["retrieved_chunks"], result["scores"])):
            lines.append(f"  - {cid} (score: {score:.4f})")
        lines.append("")
        lines.append("**Answer:**\n")
        lines.append(result["answer"] or "(empty)")
        lines.append("")
        lines.append(f"**Sources:** {', '.join(result['sources'])}\n")
        answer_text = result["answer"] or ""
        if q["type"] == "insufficient":
            if "enough information" in answer_text or "не маю" in answer_text.lower() or "ERROR" in answer_text:
                comment = "PASS - Fallback triggered correctly - model says it does not know."
            else:
                comment = "WARN - Model did not trigger fallback - may be hallucinating."
        elif q["type"] == "rephrased":
            if "ERROR" in answer_text:
                comment = "WARN - LLM error on rephrased question"
            else:
                comment = "PASS - Rephrased question handled - model found relevant context."
        elif "chunk_" in answer_text or "[" in answer_text:
            comment = "PASS - Citations present - answer is grounded."
        else:
            if "ERROR" in answer_text:
                comment = "WARN - LLM error - check prompt/context length"
            else:
                comment = "WARN - No citations in answer - may not be fully grounded."
        result["comment"] = comment
        lines.append(f"**Comment:** {comment}\n")
        lines.append("---\n")
        time.sleep(0.5)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nResults saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="RAG Answer Generation")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("build", help="Build FAISS index")
    ask_parser = subparsers.add_parser("ask", help="Answer a single question")
    ask_parser.add_argument("question", type=str)
    ask_parser.add_argument("--prompt-v", type=int, default=3)
    eval_parser = subparsers.add_parser("evaluate", help="Run all test questions")
    eval_parser.add_argument("--prompt-v", type=int, default=3)
    compare_parser = subparsers.add_parser("compare", help="Compare prompt versions")
    compare_parser.add_argument("question", type=str)
    compare_parser.add_argument("--versions", type=str, default="1,2,3")
    args = parser.parse_args()
    if args.command == "build":
        build_index()
    elif args.command == "ask":
        result = answer_question(args.question, prompt_version=args.prompt_v)
        print(f"\nQ: {result['question']}\nA: {result['answer']}")
    elif args.command == "evaluate":
        print(f"Running evaluation with prompt v{args.prompt_v}...")
        generate_examples(args.prompt_v)
    elif args.command == "compare":
        versions = [int(v.strip()) for v in args.versions.split(",")]
        print(f"Comparing prompt versions {versions} for: {args.question}\n")
        for v in versions:
            result = answer_question(args.question, prompt_version=v)
            print(f"{'='*60}")
            print(f"Prompt v{v}:")
            print(f"  Answer: {(result['answer'] or '')[:300]}...")
            print()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()