import re

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\([^)]*\)")

MAX_CHUNK_SIZE = 500


def split_by_headings(text: str) -> list[dict]:
    matches = list(HEADING_PATTERN.finditer(text))
    if not matches:
        return [{"heading": None, "content": text.strip()}]

    sections = []
    for idx, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections.append({"heading": heading, "content": text[start:end].strip()})
    return sections


def split_into_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def recursive_chunk(content: str, max_size: int = MAX_CHUNK_SIZE) -> list[str]:
    if len(content) <= max_size:
        return [content]

    paragraphs = split_into_paragraphs(content)
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        is_image_only = bool(IMAGE_PATTERN.fullmatch(para.strip()))
        if current and len(current) + len(para) + 2 > max_size and not is_image_only:
            chunks.append(current.strip())
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para

    if current:
        chunks.append(current.strip())

    return chunks


def chunk_document(text: str, source: str, max_size: int = MAX_CHUNK_SIZE) -> list[dict]:
    """Full pipeline: split by headings, then recursively split oversized
    sections. Returns a list of {"text": ..., "heading": ..., "source": ...}
    dicts - each one ready to be embedded and stored.
    """
    chunks = []
    for section in split_by_headings(text):
        for piece in recursive_chunk(section["content"], max_size):
            chunks.append({"text": piece, "heading": section["heading"], "source": source})
    return chunks
