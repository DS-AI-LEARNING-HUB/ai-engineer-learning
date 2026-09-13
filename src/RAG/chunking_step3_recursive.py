import re
from pathlib import Path

DOCS_DIR = Path("data/docs")
MAX_CHUNK_SIZE = 400  # deliberately small, to force the fallback to trigger

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\([^)]*\)")  # matches ![alt](url)


def split_by_headings(text: str) -> list[dict]:
    matches = list(HEADING_PATTERN.finditer(text))
    sections = []
    for idx, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections.append({"heading": heading, "content": text[start:end].strip()})
    return sections


def split_into_paragraphs(text: str) -> list[str]:
    # Split on blank lines (one or more), which is how markdown separates
    # paragraphs, list blocks, and image lines from each other.
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def recursive_chunk(content: str, max_size: int) -> list[str]:
    if len(content) <= max_size:
        return [content]

    paragraphs = split_into_paragraphs(content)
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        # An image line is treated as atomic - never split inside it,
        # even if adding it would push this chunk over max_size.
        is_image_only = bool(IMAGE_PATTERN.fullmatch(para.strip()))

        if current and len(current) + len(para) + 2 > max_size and not is_image_only:
            chunks.append(current.strip())
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para

    if current:
        chunks.append(current.strip())

    return chunks


for doc_path in sorted(DOCS_DIR.glob("*.md")):
    sections = split_by_headings(doc_path.read_text(encoding="utf-8"))
    print(f"\n=== {doc_path.name} ===")
    for section in sections:
        sub_chunks = recursive_chunk(section["content"], MAX_CHUNK_SIZE)
        for i, chunk in enumerate(sub_chunks):
            print(f"\n--- {section['heading']!r} (part {i+1}/{len(sub_chunks)}, {len(chunk)} chars) ---")
            print(chunk)
