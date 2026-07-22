"""
prepare_knowledge_base.py
========================
Script to prepare a knowledge base for RAG system.
Pipeline: raw sources -> normalized documents -> chunks -> metadata -> processed KB

Usage:
    python scripts/prepare_knowledge_base.py
    python scripts/prepare_knowledge_base.py --chunk_size 800 --overlap 150
    python scripts/prepare_knowledge_base.py --chunk_size 600 --overlap 100 --output custom_output.jsonl
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ──────────────────────────────────────────────────────────────
# Configuration defaults
# ──────────────────────────────────────────────────────────────
DEFAULT_CHUNK_SIZE = 700        # characters per chunk
DEFAULT_OVERLAP = 150           # character overlap between chunks
DEFAULT_INPUT_DIR = "data/raw"
DEFAULT_OUTPUT_FILE = "data/processed/chunks.jsonl"
MIN_CHUNK_SIZE = 500
MAX_CHUNK_SIZE = 1000
MIN_OVERLAP = 100
MAX_OVERLAP = 200

# Metadata mapping: maps raw filenames to document metadata
DOC_METADATA_MAP = {
    "recursive_transformers_overview.md": {
        "title": "Recursive Transformers: An Overview",
        "section": "Introduction & Overview",
        "language": "en",
        "domain": "machine_learning",
        "document_type": "survey",
        "source_type": "markdown",
    },
    "rlm_chiang_stoica_2023.md": {
        "title": "Chiang & Stoica (2023): A Recursive Language Model",
        "section": "Paper Analysis",
        "language": "en",
        "domain": "machine_learning",
        "document_type": "paper_summary",
        "source_type": "markdown",
    },
    "rlm_training_and_optimization.md": {
        "title": "Training and Optimization of Recursive Language Models",
        "section": "Training Methodology",
        "language": "en",
        "domain": "machine_learning",
        "document_type": "technical_guide",
        "source_type": "markdown",
    },
    "rlm_evaluation_and_benchmarks.md": {
        "title": "Evaluation and Benchmarking of Recursive Language Models",
        "section": "Evaluation Framework",
        "language": "en",
        "domain": "machine_learning",
        "document_type": "benchmark_report",
        "source_type": "markdown",
    },
    "rlm_applications_and_use_cases.md": {
        "title": "Applications and Use Cases of Recursive Language Models",
        "section": "Applications",
        "language": "en",
        "domain": "machine_learning",
        "document_type": "application_survey",
        "source_type": "markdown",
    },
    "rlm_future_directions_and_research.md": {
        "title": "Future Directions and Open Research Problems",
        "section": "Future Research",
        "language": "en",
        "domain": "machine_learning",
        "document_type": "research_outlook",
        "source_type": "markdown",
    },
    "rlm_foundations_and_background.md": {
        "title": "Foundations of Recursive Language Models: Background and Context",
        "section": "Background",
        "language": "en",
        "domain": "machine_learning",
        "document_type": "tutorial",
        "source_type": "markdown",
    },
}


# ──────────────────────────────────────────────────────────────
# Normalization
# ──────────────────────────────────────────────────────────────
def normalize_text(text: str) -> str:
    """
    Normalize raw text to a clean, consistent format.
    - Strip leading/trailing whitespace from each line.
    - Remove excessive blank lines (collapse 3+ blanks to 2).
    - Normalize ellipsis and dash characters.
    - Remove HTML tags if present.
    """
    import html

    # Decode HTML entities
    text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Normalize ellipsis
    text = text.replace("...", "\u2026")
    text = text.replace("...", "\u2026")

    # Normalize em-dash and en-dash
    text = text.replace("\u2014", " -- ")
    text = text.replace("\u2013", " - ")

    # Strip each line, then collapse 3+ blank lines into 2
    lines = [line.strip() for line in text.splitlines()]
    collapsed = []
    blank_count = 0
    for line in lines:
        if line == "":
            blank_count += 1
            if blank_count <= 2:
                collapsed.append(line)
        else:
            blank_count = 0
            collapsed.append(line)

    text = "\n".join(collapsed).strip()

    # Remove inline markdown image syntax ![...](...)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

    return text


def extract_sections(text: str) -> List[Dict[str, str]]:
    """
    Extract section headers from a Markdown document.
    Returns a list of (header_text, start_line, end_line) tuples.
    """
    sections = []
    lines = text.split("\n")
    current_header = None
    current_start = 0

    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            if current_header is not None:
                sections.append({
                    "header": current_header,
                    "level": len(m.group(1)),
                    "start": current_start,
                    "end": i,
                })
            current_header = m.group(2).strip()
            current_start = i

    # Don't forget the last section
    if current_header is not None:
        sections.append({
            "header": current_header,
            "level": None,  # will be set by caller
            "start": current_start,
            "end": len(lines),
        })

    return sections


def infer_section_for_chunk(
    chunk_text: str,
    sections: List[Dict[str, str]],
    primary_section: str,
    doc_text: str = "",
    chunk_start_pos: int = -1,
) -> str:
    """
    Infer the section name for a chunk based on the document sections.

    Strategy 1: look for each section header within the chunk text
    (since the chunk inherits context from its parent document).
    Return the last matching header found, which typically indicates
    the most specific sub-section.

    Strategy 2 (fallback): if chunk_start_pos is known, scan the original
    document text backward from that position to find the nearest ## or ###
    heading. This avoids returning generic placeholders like "General".
    """
    matched_sections = []
    for sec in sections:
        header = sec["header"]
        if header and len(header) > 3:  # skip very short headers
            if header in chunk_text[:800]:
                level_val = sec.get("level")
                matched_sections.append((level_val if level_val is not None else 2, header))

    if matched_sections:
        matched_sections.sort(key=lambda x: (x[0] if x[0] is not None else 99), reverse=True)
        return matched_sections[0][1]

    # Strategy 2: backward scan from chunk position in original text
    if doc_text and chunk_start_pos >= 0:
        before = doc_text[:chunk_start_pos]
        headers = re.findall(r"^#{2,3}\s+(.+)$", before, re.MULTILINE)
        if headers:
            return headers[-1].strip()

    # Strategy 3: if primary_section is generic, try to find the first real H2
    if primary_section in ("General", "Overview", "Introduction"):
        if doc_text:
            h2 = re.search(r"^##\s+(.+)$", doc_text, re.MULTILINE)
            if h2:
                return h2.group(1).strip()

    # Absolute fallback (should rarely reach here)
    return primary_section


# ──────────────────────────────────────────────────────────────
# Chunking
# ──────────────────────────────────────────────────────────────
def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
    preserve_paragraphs: bool = True,
) -> List[str]:
    """
    Split text into overlapping chunks.

    Strategy:
    1. If preserve_paragraphs is True, try to break at paragraph boundaries.
    2. Otherwise, split at word boundaries when reaching chunk_size.
    3. Apply overlap between consecutive chunks.

    Parameters:
        text: The input text to chunk.
        chunk_size: Maximum characters per chunk (500-1000).
        overlap: Overlap in characters between consecutive chunks (100-200).
        preserve_paragraphs: If True, prefer paragraph boundaries for splitting.

    Returns:
        A list of chunk strings.
    """
    if not text or not text.strip():
        return []

    chunks: List[str] = []
    remaining = text

    while remaining.strip():
        if len(remaining) <= chunk_size:
            # Last chunk — just add what's left (skip if empty/whitespace-only)
            if remaining.strip():
                chunks.append(remaining.strip())
            break

        if preserve_paragraphs:
            # Try to find a good split point: look for paragraph boundary
            # within chunk_size ± 50 chars
            target = min(chunk_size + 50, len(remaining))
            split_point = remaining.rfind("\n\n", 0, target)

            if split_point > chunk_size - 100:
                # Good paragraph boundary found
                chunks.append(remaining[:split_point].strip())
                remaining = remaining[split_point:]
            else:
                # No good boundary; split at word boundary
                split_point = _find_word_boundary(remaining, chunk_size)
                if split_point > 0:
                    chunks.append(remaining[:split_point].strip())
                    remaining = remaining[split_point:]
                else:
                    # Fallback: hard split
                    chunks.append(remaining[:chunk_size].strip())
                    remaining = remaining[chunk_size:]
        else:
            # Split at word boundary near chunk_size
            split_point = _find_word_boundary(remaining, chunk_size)
            if split_point > 0:
                chunks.append(remaining[:split_point].strip())
                remaining = remaining[split_point:]
            else:
                chunks.append(remaining[:chunk_size].strip())
                remaining = remaining[chunk_size:]

    # Apply overlap: prepend tail of previous chunk to current chunk
    if overlap > 0 and len(chunks) > 1:
        overlapped_chunks = [chunks[0]]
        for i in range(1, len(chunks)):
            prev_tail = overlapped_chunks[-1][-overlap:] if len(overlapped_chunks[-1]) >= overlap else overlapped_chunks[-1]
            current = chunks[i]
            # Only add overlap if it doesn't make the chunk too large
            if len(prev_tail) + len(current) <= chunk_size + overlap:
                overlapped_chunks.append(prev_tail + "\n\n" + current)
            else:
                overlapped_chunks.append(current)
        chunks = overlapped_chunks

    # Filter: remove empty or too-short chunks
    min_length = max(50, chunk_size // 4)
    chunks = [c.strip() for c in chunks if len(c.strip()) >= min_length]

    return chunks


def _find_word_boundary(text: str, max_pos: int) -> int:
    """
    Find the best word boundary at or before max_pos.
    Returns the split position.
    """
    if max_pos >= len(text):
        return len(text)

    # Try to find a space after max_pos first (to not cut mid-word)
    first_space = text.find(" ", max_pos)
    if first_space > 0:
        # Find the last space before first_space (the actual word boundary)
        last_space = text.rfind(" ", 0, first_space)
        return last_space if last_space > max_pos // 2 else first_space

    # Fallback: find last space before max_pos
    last_space = text.rfind(" ", 0, max_pos)
    if last_space > max_pos // 2:
        return last_space

    # Absolute fallback: hard split
    return max_pos


# ──────────────────────────────────────────────────────────────
# Document Processing Pipeline
# ──────────────────────────────────────────────────────────────
def process_document(
    filepath: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> List[Dict[str, Any]]:
    """
    Process a single document through the pipeline:
    raw -> normalized -> chunks with metadata.

    Returns:
        A list of chunk dictionaries, each with 'chunk_id', 'text', and 'metadata'.
    """
    filename = os.path.basename(filepath)

    # Load metadata from mapping
    doc_meta = DOC_METADATA_MAP.get(filename, {
        "title": filename,
        "section": "General",
        "language": "en",
        "domain": "machine_learning",
        "document_type": "general",
        "source_type": os.path.splitext(filename)[1].lstrip(".") or "markdown",
    })

    # Read raw content
    with open(filepath, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Normalize
    normalized_text = normalize_text(raw_text)

    # Extract sections for better metadata
    sections = extract_sections(normalized_text)

    # Determine primary section from header
    first_h1 = None
    first_h2 = None
    for line in normalized_text.split("\n"):
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            first_h1 = m.group(1).strip()
            break
    if not first_h1:
        for line in normalized_text.split("\n"):
            m = re.match(r"^##\s+(.+)$", line)
            if m:
                first_h2 = m.group(1).strip()
                break
    doc_meta["title"] = first_h1 or first_h2 or filename

    # Chunk the normalized text
    chunks = chunk_text(normalized_text, chunk_size, overlap)

    # Build chunk records with metadata
    chunk_records = []
    # Track positions in normalized text for backward scan fallback
    pos = 0
    for idx, chunk in enumerate(chunks):
        # Determine section for this chunk
        chunk_section = infer_section_for_chunk(
            chunk, sections, doc_meta["section"],
            doc_text=normalized_text, chunk_start_pos=pos,
        )
        pos += len(chunk)

        doc_id = Path(filename).stem
        chunk_id = f"{doc_id}_chunk_{idx + 1:03d}"

        record = {
            "chunk_id": chunk_id,
            "text": chunk,
            "metadata": {
                "document_id": doc_id,
                "source_file": f"data/raw/{filename}",
                "source_type": doc_meta["source_type"],
                "title": doc_meta["title"],
                "section": chunk_section,
                "chunk_index": idx + 1,
                "language": doc_meta["language"],
                "domain": doc_meta["domain"],
                "document_type": doc_meta["document_type"],
            },
        }
        chunk_records.append(record)

    return chunk_records


def process_all_documents(
    input_dir: str = DEFAULT_INPUT_DIR,
    output_file: str = DEFAULT_OUTPUT_FILE,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> Dict[str, Any]:
    """
    Process all documents in the input directory and write chunks to JSONL.

    Returns:
        A summary dictionary with processing statistics.
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Find all supported files
    supported_extensions = {".md", ".markdown", ".txt", ".html", ".htm"}
    doc_files = sorted([
        f for f in input_path.iterdir()
        if f.is_file() and f.suffix.lower() in supported_extensions
    ])

    if not doc_files:
        print(f"Error: No supported files found in '{input_dir}'.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(doc_files)} document(s) in '{input_dir}':")
    for df in doc_files:
        print(f"  - {df.name} ({df.stat().st_size:,} bytes)")
    print()

    # Process each document
    all_chunks: List[Dict[str, Any]] = []
    per_doc_stats: Dict[str, Dict[str, Any]] = {}

    for doc_file in doc_files:
        print(f"Processing: {doc_file.name} ...")
        chunks = process_document(str(doc_file), chunk_size, overlap)
        per_doc_stats[doc_file.name] = {
            "num_chunks": len(chunks),
            "total_chars": sum(len(c["text"]) for c in chunks),
            "avg_chunk_size": round(
                sum(len(c["text"]) for c in chunks) / len(chunks), 1
            ) if chunks else 0,
        }
        all_chunks.extend(chunks)
        print(f"  -> {len(chunks)} chunks, "
              f"avg size: {per_doc_stats[doc_file.name]['avg_chunk_size']} chars")

    # Create output directory
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSONL
    with open(output_path, "w", encoding="utf-8") as f:
        for record in all_chunks:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Print summary
    print()
    print("=" * 60)
    print("PROCESSED KNOWLEDGE BASE SUMMARY")
    print("=" * 60)
    print(f"Output file:  {output_path.absolute()}")
    print(f"Total docs:   {len(doc_files)}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Total chars:  {sum(len(c['text']) for c in all_chunks):,}")
    print(f"Chunk size:   {chunk_size} chars")
    print(f"Overlap:      {overlap} chars")
    print()
    print("Per-document statistics:")
    print(f"  {'Document':<45} {'Chunks':>8} {'Total Chars':>12} {'Avg Size':>10}")
    print(f"  {'─' * 45} {'─' * 8} {'─' * 12} {'─' * 10}")
    for doc_name, stats in per_doc_stats.items():
        print(f"  {doc_name:<45} {stats['num_chunks']:>8} "
              f"{stats['total_chars']:>12,} {stats['avg_chunk_size']:>10.0f}")

    return {
        "total_docs": len(doc_files),
        "total_chunks": len(all_chunks),
        "total_chars": sum(len(c["text"]) for c in all_chunks),
        "chunk_size": chunk_size,
        "overlap": overlap,
        "per_doc_stats": per_doc_stats,
        "output_file": str(output_path),
    }


# ──────────────────────────────────────────────────────────────
# Validation
# ──────────────────────────────────────────────────────────────
def validate_jsonl(filepath: str) -> Dict[str, Any]:
    """
    Validate the JSONL output file.
    Returns a validation report.
    """
    report = {
        "valid": True,
        "errors": [],
        "total_lines": 0,
        "valid_lines": 0,
        "invalid_lines": 0,
    }

    required_fields = {"chunk_id", "text", "metadata"}
    required_metadata = {"document_id", "source_file", "chunk_index"}

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            report["total_lines"] += 1

            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                report["valid"] = False
                report["invalid_lines"] += 1
                report["errors"].append(f"Line {line_num}: Invalid JSON — {e}")
                continue

            # Check required top-level fields
            missing = required_fields - set(record.keys())
            if missing:
                report["valid"] = False
                report["invalid_lines"] += 1
                report["errors"].append(
                    f"Line {line_num}: Missing fields: {missing}"
                )
                continue

            # Check required metadata fields
            meta = record.get("metadata", {})
            meta_missing = required_metadata - set(meta.keys())
            if meta_missing:
                report["valid"] = False
                report["invalid_lines"] += 1
                report["errors"].append(
                    f"Line {line_num}: Missing metadata: {meta_missing}"
                )
                continue

            report["valid_lines"] += 1

    return report


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Prepare knowledge base from raw documents."
    )
    parser.add_argument(
        "--input-dir", "-i",
        default=DEFAULT_INPUT_DIR,
        help=f"Input directory with raw documents (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output JSONL file (default: {DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "--chunk-size", "-c",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Chunk size in characters (default: {DEFAULT_CHUNK_SIZE}, "
             f"range: {MIN_CHUNK_SIZE}-{MAX_CHUNK_SIZE})",
    )
    parser.add_argument(
        "--overlap", "-l",
        type=int,
        default=DEFAULT_OVERLAP,
        help=f"Overlap in characters (default: {DEFAULT_OVERLAP}, "
             f"range: {MIN_OVERLAP}-{MAX_OVERLAP})",
    )
    parser.add_argument(
        "--validate", "-v",
        action="store_true",
        help="Validate the output JSONL file after processing.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate an existing JSONL file, do not process.",
    )

    args = parser.parse_args()

    # Validate hyperparameters
    if not MIN_CHUNK_SIZE <= args.chunk_size <= MAX_CHUNK_SIZE:
        print(
            f"Error: chunk_size must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE}. "
            f"Got {args.chunk_size}.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not MIN_OVERLAP <= args.overlap <= MAX_OVERLAP:
        print(
            f"Error: overlap must be between {MIN_OVERLAP} and {MAX_OVERLAP}. "
            f"Got {args.overlap}.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.validate_only:
        if not Path(args.output).exists():
            print(f"Error: Output file '{args.output}' not found.", file=sys.stderr)
            sys.exit(1)
        report = validate_jsonl(args.output)
        print(f"\nValidation report for '{args.output}':")
        print(f"  Valid:           {'YES' if report['valid'] else 'NO'}")
        print(f"  Total lines:     {report['total_lines']}")
        print(f"  Valid lines:     {report['valid_lines']}")
        print(f"  Invalid lines:   {report['invalid_lines']}")
        if report["errors"]:
            print(f"\nErrors:")
            for err in report["errors"]:
                print(f"  - {err}")
        return

    # Process documents
    summary = process_all_documents(
        input_dir=args.input_dir,
        output_file=args.output,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )

    # Validate if requested
    if args.validate:
        report = validate_jsonl(args.output)
        print(f"\nValidation report for '{args.output}':")
        print(f"  Valid:           {'YES' if report['valid'] else 'NO'}")
        print(f"  Total lines:     {report['total_lines']}")
        print(f"  Valid lines:     {report['valid_lines']}")
        print(f"  Invalid lines:   {report['invalid_lines']}")
        if report["errors"]:
            print(f"\nErrors:")
            for err in report["errors"]:
                print(f"  - {err}")


if __name__ == "__main__":
    main()