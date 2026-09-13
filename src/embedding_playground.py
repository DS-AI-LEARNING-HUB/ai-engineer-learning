import math
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/ai-gateway/mlflow/v1",
)


def embed(text: str) -> list[float]:
    response = client.embeddings.create(input=text, model="system.ai.gte-large-en")
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))
    return dot_product / (magnitude_a * magnitude_b)


sentences = [
    "How do I reset my password?",
    "I forgot my login credentials.",
    "What's the weather like today?",
    "Databricks is a data and AI platform.",
]

embeddings = [embed(s) for s in sentences]

print(f"Embedding length (dimensions): {len(embeddings[0])}\n")

# Compare every sentence to every other sentence
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        score = cosine_similarity(embeddings[i], embeddings[j])
        print(f"similarity({sentences[i]!r}, {sentences[j]!r}) = {score:.3f}")
