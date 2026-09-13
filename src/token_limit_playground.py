import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/serving-endpoints",
)

response = client.chat.completions.create(
    model="databricks-claude-opus-5",
    messages=[{"role": "user", "content": "Explain how RAG works in detail."}],
    max_tokens=15,  # deliberately tiny, to force truncation
)

print("Content:", response.choices[0].message.content)
print("finish_reason:", response.choices[0].finish_reason)
print("completion_tokens used:", response.usage.completion_tokens)
