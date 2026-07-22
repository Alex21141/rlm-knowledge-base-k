#!/usr/bin/env python3
"""
prepare_knowledge_base.py

Script for preparing knowledge base for RAG system on Recursive Language Models.
Uses real data from: alexzhang13/rlm, context-labs/halo, primeintellect.ai/blog/rlm,
alexzhang13.github.io/blog/2025/rlm, arXiv:2404.07839 (RecurrentGemma), arXiv:2512.24601v3
Pipeline: raw sources → normalized documents → chunks → metadata → processed knowledge base

Usage:
    python scripts/prepare_knowledge_base.py

Configuration:
    CHUNK_SIZE: 900 characters per chunk
    OVERLAP: 180 characters between chunks
"""

import json
import re
import os

CHUNK_SIZE = 900
OVERLAP = 180
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def clean_text(text):
    text = re.sub(r'
{3,}', '

', text)
    text = re.sub(r'[ 	]+', ' ', text)
    return text.strip()

def split_into_paragraphs(text):
    paragraphs = []
    current = []
    in_code_block = False
    for line in text.split('\n'):
        if line.strip().startswith('```'):
            if current:
                paragraphs.append('\n'.join(current))
                current = []
            in_code_block = not in_code_block
            current.append(line)
            if not in_code_block:
                paragraphs.append('\n'.join(current))
                current = []
        elif in_code_block:
            current.append(line)
        elif line.strip() == '':
            if current:
                paragraphs.append('\n'.join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append('\n'.join(current))
    return [p.strip() for p in paragraphs if p.strip()]

def create_chunks(paragraphs, chunk_size, overlap):
    chunks = []
    current_chunk = []
    current_size = 0
    for para in paragraphs:
        para_size = len(para)
        if para_size > chunk_size:
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            sentences = re.split(r'(?<=[.!?])\s+', para)
            temp_chunk = []
            temp_size = 0
            for sent in sentences:
                if temp_size + len(sent) + 1 > chunk_size and temp_chunk:
                    chunks.append(' '.join(temp_chunk))
                    overlap_text = ' '.join(temp_chunk)
                    overlap_sentences = re.split(r'(?<=[.!?])\s+', overlap_text)
                    temp_chunk = []
                    temp_size = 0
                    overlap_accumulated = 0
                    for s in reversed(overlap_sentences):
                        if overlap_accumulated + len(s) + 1 <= overlap:
                            temp_chunk.insert(0, s)
                            overlap_accumulated += len(s) + 1
                        else:
                            break
                    temp_size = sum(len(s) + 1 for s in temp_chunk)
                temp_chunk.append(sent)
                temp_size += len(sent) + 1
            if temp_chunk:
                current_chunk = temp_chunk
                current_size = temp_size
        else:
            if current_size + para_size + 2 > chunk_size and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                overlap_text = '\n\n'.join(current_chunk)
                overlap_paras = overlap_text.split('\n\n')
                current_chunk = []
                current_size = 0
                overlap_accumulated = 0
                for p in reversed(overlap_paras):
                    if overlap_accumulated + len(p) + 2 <= overlap:
                        current_chunk.insert(0, p)
                        overlap_accumulated += len(p) + 2
                    else:
                        break
                current_size = sum(len(p) + 2 for p in current_chunk)
            current_chunk.append(para)
            current_size += para_size + 2
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    return chunks

def extract_section(chunk_text, full_text):
    pos = full_text.find(chunk_text[:50])
    if pos == -1:
        return "General"
    text_before = full_text[:pos]
    headings = re.findall(r'^#{2,3}\s+(.+)$', text_before, re.MULTILINE)
    if headings:
        return headings[-1].strip()
    return "General"

def process_document(filepath, doc_info):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    cleaned_text = clean_text(raw_text)
    paragraphs = split_into_paragraphs(cleaned_text)
    chunks = create_chunks(paragraphs, CHUNK_SIZE, OVERLAP)
    records = []
    for idx, chunk_text in enumerate(chunks, 1):
        section = extract_section(chunk_text, cleaned_text)
        chunk_id = f"{doc_info['doc_id']}_chunk_{idx:03d}"
        record = {
            "chunk_id": chunk_id,
            "text": chunk_text,
            "metadata": {
                "document_id": doc_info['doc_id'],
                "source_file": f"data/raw/{doc_info['file']}",
                "source_type": "markdown",
                "title": doc_info['title'],
                "section": section,
                "chunk_index": idx,
                "language": "en",
                "domain": doc_info['domain'],
                "document_type": doc_info['doc_type']
            }
        }
        records.append(record)
    return records

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    documents = [
        {
            'file': 'rlm_core_paper_and_github.md',
            'doc_id': 'rlm_core',
            'title': 'Recursive Language Models — Core Paper and Implementation (MIT)',
            'domain': 'machine-learning',
            'doc_type': 'research-paper'
        },
        {
            'file': 'halo_agent_optimizer.md',
            'doc_id': 'halo',
            'title': 'HALO: Hierarchical Agent Loop Optimizer (Context Labs)',
            'domain': 'agent-engineering',
            'doc_type': 'tool'
        },
        {
            'file': 'prime_intellect_ablations.md',
            'doc_id': 'prime_ablations',
            'title': 'Prime Intellect: RLM Ablations and Experimental Results',
            'domain': 'experimental-ml',
            'doc_type': 'experimental-report'
        },
        {
            'file': 'alexzhang_blog_context_rot.md',
            'doc_id': 'blog_context_rot',
            'title': 'Alex Zhang Blog: Context Rot and RLM Intuition',
            'domain': 'ml-theory',
            'doc_type': 'blog'
        },
        {
            'file': 'prime_intellect_context_folding.md',
            'doc_id': 'prime_context_folding',
            'title': 'Prime Intellect: Context Folding vs RLM Paradigm',
            'domain': 'ml-theory',
            'doc_type': 'analysis'
        },
        {
            'file': 'recurrentgemma_griffin_architecture.md',
            'doc_id': 'recurrentgemma',
            'title': 'RecurrentGemma: Griffin Architecture (Google DeepMind)',
            'domain': 'model-architecture',
            'doc_type': 'research-paper'
        },
        {
            'file': 'rlm_paper_v3_updates.md',
            'doc_id': 'rlm_v3',
            'title': 'RLM Paper v3 Updates (May 2026)',
            'domain': 'machine-learning',
            'doc_type': 'research-paper'
        },
        {
            'file': 'rlm_industry_analysis.md',
            'doc_id': 'rlm_industry',
            'title': 'RLM Industry Analysis and Future Outlook',
            'domain': 'industry-analysis',
            'doc_type': 'overview'
        }
    ]
    all_chunks = []
    for doc_info in documents:
        filepath = os.path.join(RAW_DIR, doc_info['file'])
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found, skipping.")
            continue
        records = process_document(filepath, doc_info)
        all_chunks.extend(records)
        print(f"Processed {doc_info['file']}: {len(records)} chunks")
    jsonl_path = os.path.join(PROCESSED_DIR, 'chunks.jsonl')
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Saved to: {jsonl_path}")

if __name__ == '__main__':
    main()
