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
    messages=[{"role": "user", "content": "In one sentence, what are you?"}],
)

print("Content Response:" , response.choices[0].message.content,"\n")

print("Response:",response)
