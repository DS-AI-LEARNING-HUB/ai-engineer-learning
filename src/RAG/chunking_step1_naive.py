from pathlib import Path

DOCS_DIR = Path("data/docs")
CHUNK_SIZE = 300  # characters


def naive_chunk(text: str, chunk_size: int) -> list[str]:
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


for doc_path in sorted(DOCS_DIR.glob("*.md")):
    text = doc_path.read_text(encoding="utf-8")
    chunks = naive_chunk(text, CHUNK_SIZE)
    print(f"\n=== {doc_path.name}: {len(chunks)} chunks ===")
    for i, chunk in enumerate(chunks):
        print(f"\n--- chunk {i} ---")
        print(chunk)
