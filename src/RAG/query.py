import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()

CHROMA_DIR = Path("data/chroma_db")

# Two separate clients: one for embeddings (AI Gateway route), one for chat (serving-endpoints route)
embed_client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/ai-gateway/mlflow/v1",
)
chat_client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/serving-endpoints",
)

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_collection(name="nimbusflow_docs")


def embed(text: str) -> list[float]:
    response = embed_client.embeddings.create(input=text, model="system.ai.gte-large-en")
    return response.data[0].embedding


def ask(question: str, top_k: int = 3) -> None:
    query_embedding = embed(question)

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    retrieved_texts = results["documents"][0]
    retrieved_metadata = results["metadatas"][0]

    print("--- Retrieved chunks ---")
    for text, meta in zip(retrieved_texts, retrieved_metadata):
        print(f"\n[source: {meta['source']} | heading: {meta['heading']}]")
        print(text[:200], "..." if len(text) > 200 else "")

    context = "\n\n---\n\n".join(retrieved_texts)

    response = chat_client.chat.completions.create(
        model="databricks-claude-opus-5",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using ONLY the provided context. "
                    "If the context doesn't contain the answer, say you don't know."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
    )

    content = response.choices[0].message.content
    if isinstance(content, list):
        answer = "".join(block["text"] for block in content if block.get("type") == "text")
    else:
        answer = content

    print("\n--- Answer ---")
    print(answer)


ask("How many active pipelines did the Team tier have in Q3, and what tier had a flat quarter?")
