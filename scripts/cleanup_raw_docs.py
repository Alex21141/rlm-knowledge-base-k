"""
HW1: Raw document quality checker for RAG readiness.

Requirements:
1. NO base64 blobs (data:text/plain;base64,...)
2. NO image markers (![IMAGE:...], ![[Uncaptioned image]]...)
3. NO URLs (https://, http://, markdown links [text](url))
4. NO email links (user@domain.tld)
5. NO squished lines (>50 chars with no spaces)
6. NO consecutive empty lines (max 1 blank between paragraphs)
7. NO HTML tags (<tag>...</tag>)
8. NO angle bracket URLs (<https://...>)
9. File size: 5KB - 200KB
10. Line count: 20 - 2000 lines
"""
import re
import glob
import json
import os
import sys

os.chdir("/home/hermes/rlm-knowledge-base-k")

REQUIREMENTS = {
    "base64": {
        "pattern": r"data:text/plain;base64,",
        "name": "Base64 blobs",
        "severity": "critical",
    },
    "image_markers": {
        "pattern": r"!\[IMAGE:",
        "name": "Image markers",
        "severity": "critical",
    },
    "uncaptioned": {
        "pattern": r"!\[\[Uncaptioned",
        "name": "Uncaptioned images",
        "severity": "critical",
    },
    "urls": {
        "pattern": r"https?://[^\s\)\]]+",
        "name": "URLs",
        "severity": "critical",
    },
    "email": {
        "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "name": "Email links",
        "severity": "warning",
    },
    "markdown_links": {
        "pattern": r"\[[^\]]+\]\([^)]+\)",
        "name": "Markdown links [text](url)",
        "severity": "warning",
    },
    "angle_urls": {
        "pattern": r"<https?://[^>]+>",
        "name": "Angle bracket URLs",
        "severity": "warning",
    },
    "html_tags": {
        "pattern": r"<[a-zA-Z][^>]*>",
        "name": "HTML tags",
        "severity": "warning",
    },
}

def check_file(filepath):
    """Check a single file against all requirements."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    issues = []
    name = os.path.basename(filepath)
    lines = content.split("\n")
    size = len(content)

    # --- Pattern-based checks ---
    for req_id, req in REQUIREMENTS.items():
        matches = re.findall(req["pattern"], content)
        if matches:
            issues.append({
                "rule": req_id,
                "name": req["name"],
                "count": len(matches),
                "severity": req["severity"],
                "examples": [m[:80] for m in matches[:3]],
            })

    # --- Squished lines (>50 chars, no spaces) ---
    squished = [l for l in lines if len(l) > 50 and " " not in l and "\t" not in l and l.strip()]
    if squished:
        issues.append({
            "rule": "squished",
            "name": "Squished lines (>50 chars, no spaces)",
            "count": len(squished),
            "severity": "critical",
            "examples": [l[:80] for l in squished[:3]],
        })

    # --- Consecutive empty lines ---
    consecutive_blanks = 0
    max_consecutive = 0
    for line in lines:
        if not line.strip():
            consecutive_blanks += 1
            max_consecutive = max(max_consecutive, consecutive_blanks)
        else:
            consecutive_blanks = 0

    if max_consecutive > 1:
        issues.append({
            "rule": "consecutive_blanks",
            "name": "Consecutive empty lines",
            "count": max_consecutive,
            "severity": "warning",
            "examples": [f"Max {max_consecutive} consecutive empty lines"],
        })

    # --- File size check ---
    if size < 5000:
        issues.append({
            "rule": "file_size_small",
            "name": "File too small",
            "count": size,
            "severity": "warning",
            "examples": [f"{size}B < 5KB minimum"],
        })
    if size > 200000:
        issues.append({
            "rule": "file_size_large",
            "name": "File too large",
            "count": size,
            "severity": "warning",
            "examples": [f"{size}B > 200KB maximum"],
        })

    # --- Line count check ---
    if len(lines) < 20:
        issues.append({
            "rule": "line_count_low",
            "name": "Too few lines",
            "count": len(lines),
            "severity": "warning",
            "examples": [f"{len(lines)} lines < 20 minimum"],
        })
    if len(lines) > 2000:
        issues.append({
            "rule": "line_count_high",
            "name": "Too many lines",
            "count": len(lines),
            "severity": "info",
            "examples": [f"{len(lines)} lines > 2000 (consider splitting)"],
        })

    # --- Empty line percentage ---
    empty_count = sum(1 for l in lines if not l.strip())
    empty_pct = empty_count * 100 // max(1, len(lines))
    if empty_pct > 50:
        issues.append({
            "rule": "high_empty_pct",
            "name": "Too many empty lines",
            "count": empty_pct,
            "severity": "warning",
            "examples": [f"{empty_pct}% of lines are empty ({empty_count}/{len(lines)})"],
        })

    return {
        "file": name,
        "size": size,
        "lines": len(lines),
        "empty_pct": empty_pct,
        "issues": issues,
    }


def auto_fix_file(filepath):
    """Apply automatic fixes to a raw document."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    fixes_applied = []

    # 1. Remove base64 blobs (with optional squished continuation)
    old = content
    content = re.sub(r'\[⬇\]\(data:text/plain;base64,[^)]*\)\s*\n\s*[A-Za-z]{20,}\s*\n?', '', content)
    content = re.sub(r'\[⬇\]\(data:text/plain;base64,[^)]*\)\s*\n?', '', content)
    if content != old:
        fixes_applied.append("base64 blobs removed")

    # 2. Remove uncaptioned images
    old = content
    content = re.sub(r'!\[\[Uncaptioned image\]\]\([^)]+\)\s*\n?', '', content)
    if content != old:
        fixes_applied.append("uncaptioned images removed")

    # 3. Clean IMAGE markers (keep text after ])
    old = content
    def replace_image_marker(m):
        full = m.group(0)
        bracket_end = full.find(']')
        if bracket_end >= 0:
            return full[bracket_end + 1:] + "\n"
        return "\n"
    content = re.sub(r'!\[IMAGE:[^\]]*\][^\n]*', replace_image_marker, content)
    if content != old:
        fixes_applied.append("image markers cleaned")

    # 4. Remove markdown links [text](url) -> text
    old = content
    def replace_md_link(m):
        full = m.group(0)
        bracket_start = full.index('[')
        bracket_end = full.index(']')
        link_text = full[bracket_start + 1:bracket_end]
        link_text = re.sub(r'!\[.*?\]', '', link_text)
        return link_text
    content = re.sub(r'\[[^\]]+\]\([^)]+\)', replace_md_link, content)
    if content != old:
        fixes_applied.append("markdown links cleaned")

    # 5. Remove bare URLs
    old = content
    content = re.sub(r'https?://[^\s\)]+', '', content)
    if content != old:
        fixes_applied.append("bare URLs removed")

    # 6. Remove angle bracket URLs
    old = content
    content = re.sub(r'<(https?://[^>]+)>', '', content)
    if content != old:
        fixes_applied.append("angle bracket URLs removed")

    # 7. Remove email links
    old = content
    content = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', content)
    if content != old:
        fixes_applied.append("email links removed")

    # 8. Remove HTML tags
    old = content
    content = re.sub(r'<[^>]+>', '', content)
    if content != old:
        fixes_applied.append("HTML tags removed")

    # 9. Remove squished lines (>50 chars, no spaces)
    old = content
    lines = content.split("\n")
    cleaned = [l for l in lines if not (len(l) > 50 and " " not in l and "\t" not in l and l.strip())]
    if len(cleaned) != len(lines):
        content = "\n".join(cleaned)
        fixes_applied.append(f"{len(lines) - len(cleaned)} squished lines removed")

    # 10. Reduce consecutive empty lines to max 1
    old = content
    lines = content.split("\n")
    final = []
    prev_empty = False
    for line in lines:
        is_empty = not line.strip()
        if is_empty and prev_empty:
            continue  # skip consecutive empty
        final.append(line)
        prev_empty = is_empty
    content = "\n".join(final)
    if content != old:
        fixes_applied.append("consecutive empty lines reduced")

    # 11. Final cleanup
    content = re.sub(r'  +', ' ', content)
    content = re.sub(r'\.\.\.', '', content)
    content = content.strip()

    if fixes_applied:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return fixes_applied


def main():
    files = sorted(glob.glob("data/raw/*.md"))
    if not files:
        print("❌ No raw documents found in data/raw/")
        sys.exit(1)

    print("=" * 70)
    print("RAW DOCUMENT QUALITY CHECK — RAG Requirements")
    print("=" * 70)
    print()
    print("Requirements:")
    print("  1. ✅ No base64 blobs")
    print("  2. ✅ No image markers (![IMAGE:], ![[Uncaptioned]])")
    print("  3. ✅ No URLs (https://, markdown links)")
    print("  4. ✅ No email links")
    print("  5. ✅ No squished lines (>50 chars, no spaces)")
    print("  6. ✅ No consecutive empty lines")
    print("  7. ✅ No HTML tags")
    print("  8. ✅ No angle bracket URLs")
    print("  9. ✅ File size: 5KB - 200KB")
    print(" 10. ✅ Line count: 20 - 2000 lines")
    print()
    print("-" * 70)

    all_results = []
    total_critical = 0
    total_warnings = 0

    for f in files:
        result = check_file(f)
        all_results.append(result)

        name = result["file"]
        critical = sum(1 for i in result["issues"] if i["severity"] == "critical")
        warnings = sum(1 for i in result["issues"] if i["severity"] == "warning")
        infos = sum(1 for i in result["issues"] if i["severity"] == "info")
        total_critical += critical
        total_warnings += warnings

        status = "✅ PASS" if critical == 0 and warnings == 0 else "❌ FAIL"
        if critical == 0 and warnings == 0 and infos > 0:
            status = "⚠️ INFO"

        print(f"\n  {status} {name}")
        print(f"         Size: {result['size']:,}B | Lines: {result['lines']} | Empty: {result['empty_pct']}%")

        if result["issues"]:
            for issue in result["issues"]:
                sev_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(issue["severity"], "⚪")
                print(f"         {sev_icon} {issue['name']}: {issue['count']}")
                for ex in issue["examples"][:2]:
                    print(f"            → {ex}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total files: {len(files)}")
    print(f"  Critical issues: {total_critical}")
    print(f"  Warnings: {total_warnings}")

    all_clean = total_critical == 0 and total_warnings == 0
    if all_clean:
        print(f"  ✅ All documents pass quality checks")
    else:
        print(f"  ❌ {total_critical} critical issues found")
        print()
        print("  Fix with: python scripts/cleanup_raw_docs.py --fix")

    return 0 if all_clean else 1


if __name__ == "__main__":
    sys.exit(main())