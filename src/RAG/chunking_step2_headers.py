import re
from pathlib import Path

DOCS_DIR = Path("data/docs")

# Matches a markdown heading line, e.g. "## Core Concepts" or "# Title"
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


def split_by_headings(text: str) -> list[dict]:
    """Split text into sections, each starting at a heading.

    Returns a list of {"heading": str, "content": str} dicts, so each
    chunk keeps track of which section it came from.
    """
    matches = list(HEADING_PATTERN.finditer(text))
    sections = []

    for idx, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.start()
        # This section's content runs until the next heading starts,
        # or until the end of the document for the last heading.
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        sections.append({"heading": heading, "content": content})

    return sections


for doc_path in sorted(DOCS_DIR.glob("*.md")):
    sections = split_by_headings(doc_path.read_text(encoding="utf-8"))
    print(f"\n=== {doc_path.name}: {len(sections)} sections ===")
    for s in sections:
        print(f"\n--- Section: {s['heading']!r} ({len(s['content'])} chars) ---")
        print(s["content"][:150], "..." if len(s["content"]) > 150 else "")
