import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

from chunking import chunk_document
from pdf_to_text import pdf_to_text

load_dotenv()

client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/ai-gateway/mlflow/v1",
)

DOCS_DIR = Path("data/docs")
CHROMA_DIR = Path("data/chroma_db")


def embed(text: str) -> list[float]:
    response = client.embeddings.create(input=text, model="system.ai.gte-large-en")
    return response.data[0].embedding


all_chunks: list[dict] = []

for md_path in sorted(DOCS_DIR.glob("*.md")):
    text = md_path.read_text(encoding="utf-8")
    all_chunks.extend(chunk_document(text, source=md_path.name))

for pdf_path in sorted(DOCS_DIR.glob("*.pdf")):
    text = pdf_to_text(pdf_path)
    all_chunks.extend(chunk_document(text, source=pdf_path.name))

print(f"Total chunks to embed: {len(all_chunks)}")

# PersistentClient writes to disk at CHROMA_DIR, so the index survives
# between script runs - you build it once, query it many times later.
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

# get_or_create so re-running this script doesn't error if it already exists.
collection = chroma_client.get_or_create_collection(name="nimbusflow_docs")

collection.add(
    ids=[f"chunk_{i}" for i in range(len(all_chunks))],
    embeddings=[embed(chunk["text"]) for chunk in all_chunks],
    documents=[chunk["text"] for chunk in all_chunks],
    metadatas=[{"source": chunk["source"], "heading": chunk["heading"] or ""} for chunk in all_chunks],
)

print(f"Stored {collection.count()} chunks in Chroma at {CHROMA_DIR}")
