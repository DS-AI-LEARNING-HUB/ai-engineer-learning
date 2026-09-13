import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["DATABRICKS_TOKEN"],
    base_url=f"{os.environ['DATABRICKS_HOST']}/serving-endpoints",
)

# stream=True changes the return type: instead of one full response object,
# you get an iterator of small "chunks" as the model generates them.
stream = client.chat.completions.create(
    model="databricks-claude-opus-5",
    messages=[{"role": "user", "content": "Write a 4-line poem about debugging code."}],
    stream=True,
)

for chunk in stream:
    # Each chunk may or may not contain a piece of text - guard against None.
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)  # no newline, no buffering - prints as it arrives

print()  # final newline after streaming finishes
